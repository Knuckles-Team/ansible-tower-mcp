#!/usr/bin/python
import sys

# coding: utf-8
import json
import os
import argparse
import logging
import uvicorn
import httpx
from typing import Optional, Any, List
from contextlib import asynccontextmanager

from pydantic_ai import Agent, ModelSettings, RunContext
from pydantic_ai.mcp import (
    load_mcp_servers,
    MCPServerStreamableHTTP,
    MCPServerSSE,
)
from pydantic_ai_skills import SkillsToolset
from fasta2a import Skill
from ansible_tower_mcp.utils import (
    to_integer,
    to_boolean,
    to_float,
    to_list,
    to_dict,
    get_mcp_config_path,
    get_skills_path,
    load_skills_from_directory,
    create_model,
    tool_in_tag,
    prune_large_messages,
)

from fastapi import FastAPI, Request
from starlette.responses import Response, StreamingResponse
from pydantic import ValidationError
from pydantic_ai.ui import SSE_CONTENT_TYPE
from pydantic_ai.ui.ag_ui import AGUIAdapter

__version__ = "1.3.13"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logging.getLogger("pydantic_ai").setLevel(logging.INFO)
logging.getLogger("fastmcp").setLevel(logging.INFO)
logging.getLogger("httpx").setLevel(logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_HOST = os.getenv("HOST", "0.0.0.0")
DEFAULT_PORT = to_integer(string=os.getenv("PORT", "9000"))
DEFAULT_DEBUG = to_boolean(string=os.getenv("DEBUG", "False"))
DEFAULT_PROVIDER = os.getenv("PROVIDER", "openai")
DEFAULT_MODEL_ID = os.getenv("MODEL_ID", "qwen/qwen3-coder-next")
DEFAULT_LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://host.docker.internal:1234/v1")
DEFAULT_LLM_API_KEY = os.getenv("LLM_API_KEY", "ollama")
DEFAULT_MCP_URL = os.getenv("MCP_URL", None)
DEFAULT_MCP_CONFIG = os.getenv("MCP_CONFIG", get_mcp_config_path())
DEFAULT_CUSTOM_SKILLS_DIRECTORY = os.getenv("CUSTOM_SKILLS_DIRECTORY", None)
DEFAULT_ENABLE_WEB_UI = to_boolean(os.getenv("ENABLE_WEB_UI", "False"))
DEFAULT_SSL_VERIFY = to_boolean(os.getenv("SSL_VERIFY", "True"))

DEFAULT_MAX_TOKENS = to_integer(os.getenv("MAX_TOKENS", "16384"))
DEFAULT_TEMPERATURE = to_float(os.getenv("TEMPERATURE", "0.7"))
DEFAULT_TOP_P = to_float(os.getenv("TOP_P", "1.0"))
DEFAULT_TIMEOUT = to_float(os.getenv("TIMEOUT", "32400.0"))
DEFAULT_TOOL_TIMEOUT = to_float(os.getenv("TOOL_TIMEOUT", "32400.0"))
DEFAULT_PARALLEL_TOOL_CALLS = to_boolean(os.getenv("PARALLEL_TOOL_CALLS", "True"))
DEFAULT_SEED = to_integer(os.getenv("SEED", None))
DEFAULT_PRESENCE_PENALTY = to_float(os.getenv("PRESENCE_PENALTY", "0.0"))
DEFAULT_FREQUENCY_PENALTY = to_float(os.getenv("FREQUENCY_PENALTY", "0.0"))
DEFAULT_LOGIT_BIAS = to_dict(os.getenv("LOGIT_BIAS", None))
DEFAULT_STOP_SEQUENCES = to_list(os.getenv("STOP_SEQUENCES", None))
DEFAULT_EXTRA_HEADERS = to_dict(os.getenv("EXTRA_HEADERS", None))
DEFAULT_EXTRA_BODY = to_dict(os.getenv("EXTRA_BODY", None))

AGENT_NAME = "AnsibleTower"
AGENT_DESCRIPTION = "A multi-agent system for managing Ansible Tower resources via delegated specialists."


SUPERVISOR_SYSTEM_PROMPT = os.environ.get(
    "SUPERVISOR_SYSTEM_PROMPT",
    default=(
        "You are the Ansible Tower Supervisor Agent.\n"
        "Your goal is to assist the user by assigning tasks to specialized child agents through your available toolset.\n"
        "Analyze the user's request and determine which domain(s) it falls into (e.g., inventory, hosts, jobs, templates, etc.).\n"
        "Then, call the appropriate tool(s) to delegate the task.\n"
        "Synthesize the results from the child agents into a final helpful response.\n"
        "Always be warm, professional, and helpful."
        "Note: The final response should contain all the relevant information from the tool executions. Never leave out any relevant information or leave it to the user to find it. "
        "You are the final authority on the user's request and the final communicator to the user. Present information as logically and concisely as possible. "
        "Explore using organized output with headers, sections, lists, and tables to make the information easy to navigate. "
        "If there are gaps in the information, clearly state that information is missing. Do not make assumptions or invent placeholder information, only use the information which is available."
    ),
)

AD_HOC_COMMANDS_AGENT_PROMPT = os.environ.get(
    "AD_HOC_COMMANDS_AGENT_PROMPT",
    default=(
        "You are the Ansible Tower Ad Hoc Commands Agent.\n"
        "Your goal is to manage ad hoc commands.\n"
        "You can:\n"
        "- Run commands: `run_ad_hoc_command` (execute modules directly)\n"
        "- Manage: `get_ad_hoc_command`, `cancel_ad_hoc_command`\n"
        "Use this for quick, one-off tasks without a playbook."
    ),
)

CREDENTIALS_AGENT_PROMPT = os.environ.get(
    "CREDENTIALS_AGENT_PROMPT",
    default=(
        "You are the Ansible Tower Credentials Agent.\n"
        "Your goal is to manage credentials.\n"
        "Note: Specific tool availability for credentials depends on the current MCP configuration.\n"
        "If no specific tools are available, you cannot create or modify credentials."
    ),
)

GROUPS_AGENT_PROMPT = os.environ.get(
    "GROUPS_AGENT_PROMPT",
    default=(
        "You are the Ansible Tower Groups Agent.\n"
        "Your goal is to manage inventory groups.\n"
        "You can:\n"
        "- CRUD: `create_group`, `get_group`, `update_group`, `delete_group`\n"
        "- List: `list_groups`\n"
        "- Members: `add_host_to_group`, `remove_host_from_group`\n"
        "Use groups to organize hosts logically."
    ),
)

HOSTS_AGENT_PROMPT = os.environ.get(
    "HOSTS_AGENT_PROMPT",
    default=(
        "You are the Ansible Tower Hosts Agent.\n"
        "Your goal is to manage hosts in inventories.\n"
        "You can:\n"
        "- CRUD: `create_host` (requires inventory ID), `get_host`, `update_host`, `delete_host`\n"
        "- List: `list_hosts`\n"
        "Ensure you have the correct inventory ID when adding hosts."
    ),
)

INVENTORY_AGENT_PROMPT = os.environ.get(
    "INVENTORY_AGENT_PROMPT",
    default=(
        "You are the Ansible Tower Inventory Agent.\n"
        "Your goal is to manage inventories.\n"
        "You can:\n"
        "- CRUD: `create_inventory`, `get_inventory`, `update_inventory`, `delete_inventory`\n"
        "- List: `list_inventories`\n"
        "Inventories are the containers for your hosts and groups."
    ),
)

JOB_TEMPLATES_AGENT_PROMPT = os.environ.get(
    "JOB_TEMPLATES_AGENT_PROMPT",
    default=(
        "You are the Ansible Tower Job Templates Agent.\n"
        "Your goal is to manage job templates.\n"
        "You can:\n"
        "- CRUD: `create_job_template` (needs project/playbook), `get_job_template`, `update_job_template`, `delete_job_template`\n"
        "- List: `list_job_templates`\n"
        "- Action: `launch_job` (runs the template)\n"
        "When creating, ensure the playbook exists in the project."
    ),
)

JOBS_AGENT_PROMPT = os.environ.get(
    "JOBS_AGENT_PROMPT",
    default=(
        "You are the Ansible Tower Jobs Agent.\n"
        "Your goal is to monitor and manage job executions.\n"
        "You can:\n"
        "- List: `list_jobs` (filter by status like 'running', 'failed')\n"
        "- Details: `get_job`\n"
        "Use this for checking the status and output of launched jobs."
    ),
)

ORGANIZATIONS_AGENT_PROMPT = os.environ.get(
    "ORGANIZATIONS_AGENT_PROMPT",
    default=(
        "You are the Ansible Tower Organizations Agent.\n"
        "Your goal is to manage organizations.\n"
        "You can:\n"
        "- CRUD: `create_organization`, `get_organization`, `update_organization`, `delete_organization`\n"
        "- List: `list_organizations`\n"
        "Organizations are the top-level hierarchy for access and resources."
    ),
)

PROJECTS_AGENT_PROMPT = os.environ.get(
    "PROJECTS_AGENT_PROMPT",
    default=(
        "You are the Ansible Tower Projects Agent.\n"
        "Your goal is to manage projects (SCM links).\n"
        "Note: Specific tool availability for projects depends on configuration.\n"
        "Usually involves syncing playbooks from Git/SVN."
    ),
)

SCHEDULES_AGENT_PROMPT = os.environ.get(
    "SCHEDULES_AGENT_PROMPT",
    default=(
        "You are the Ansible Tower Schedules Agent.\n"
        "Your goal is to manage job schedules.\n"
        "You can:\n"
        "- CRUD: `create_schedule`, `get_schedule`, `update_schedule`, `delete_schedule`\n"
        "- List: `list_schedules`\n"
        "Schedules allow periodic execution of templates."
    ),
)

SYSTEM_AGENT_PROMPT = os.environ.get(
    "SYSTEM_AGENT_PROMPT",
    default=(
        "You are the Ansible Tower System Agent.\n"
        "Your goal is to retrieve system information.\n"
        "You can:\n"
        "- Info: `get_ansible_version`, `get_dashboard_stats`, `get_metrics`\n"
        "Use this for checking health and platform statistics."
    ),
)

TEAMS_AGENT_PROMPT = os.environ.get(
    "TEAMS_AGENT_PROMPT",
    default=(
        "You are the Ansible Tower Teams Agent.\n"
        "Your goal is to manage teams within organizations.\n"
        "You can:\n"
        "- CRUD: `create_team`, `get_team`, `update_team`, `delete_team`\n"
        "- List: `list_teams`\n"
        "Teams allow grouping of users for permissions."
    ),
)

USERS_AGENT_PROMPT = os.environ.get(
    "USERS_AGENT_PROMPT",
    default=(
        "You are the Ansible Tower Users Agent.\n"
        "Your goal is to manage user accounts.\n"
        "You can:\n"
        "- CRUD: `create_user`, `get_user`, `update_user`, `delete_user`\n"
        "- List: `list_users`\n"
        "Manage access and credentials for individuals."
    ),
)

WORKFLOW_JOBS_AGENT_PROMPT = os.environ.get(
    "WORKFLOW_JOBS_AGENT_PROMPT",
    default=(
        "You are the Ansible Tower Workflow Jobs Agent.\n"
        "Your goal is to manage workflow executions.\n"
        "You can:\n"
        "- List: `list_workflow_jobs`\n"
        "- Details: `get_workflow_job`\n"
        "- Action: `cancel_workflow_job`\n"
        "Workflow jobs are instances of running workflow templates."
    ),
)

WORKFLOW_TEMPLATES_AGENT_PROMPT = os.environ.get(
    "WORKFLOW_TEMPLATES_AGENT_PROMPT",
    default=(
        "You are the Ansible Tower Workflow Templates Agent.\n"
        "Your goal is to manage workflow templates.\n"
        "You can:\n"
        "- List: `list_workflow_templates`\n"
        "- Details: `get_workflow_template`\n"
        "- Action: `launch_workflow`\n"
        "Workflows orchestrate multiple job templates."
    ),
)


def create_agent(
    provider: str = DEFAULT_PROVIDER,
    model_id: str = DEFAULT_MODEL_ID,
    base_url: Optional[str] = DEFAULT_LLM_BASE_URL,
    api_key: Optional[str] = DEFAULT_LLM_API_KEY,
    mcp_url: str = DEFAULT_MCP_URL,
    mcp_config: str = DEFAULT_MCP_CONFIG,
    custom_skills_directory: Optional[str] = DEFAULT_CUSTOM_SKILLS_DIRECTORY,
    ssl_verify: bool = DEFAULT_SSL_VERIFY,
) -> Agent:
    """
    Creates the Supervisor Agent with sub-agents registered as tools.
    """
    logger.info("Initializing Multi-Agent System for Ansible Tower...")

    model = create_model(
        provider=provider,
        model_id=model_id,
        base_url=base_url,
        api_key=api_key,
        ssl_verify=ssl_verify,
        timeout=DEFAULT_TIMEOUT,
    )
    settings = ModelSettings(
        max_tokens=DEFAULT_MAX_TOKENS,
        temperature=DEFAULT_TEMPERATURE,
        top_p=DEFAULT_TOP_P,
        timeout=DEFAULT_TIMEOUT,
        parallel_tool_calls=DEFAULT_PARALLEL_TOOL_CALLS,
        seed=DEFAULT_SEED,
        presence_penalty=DEFAULT_PRESENCE_PENALTY,
        frequency_penalty=DEFAULT_FREQUENCY_PENALTY,
        logit_bias=DEFAULT_LOGIT_BIAS,
        stop_sequences=DEFAULT_STOP_SEQUENCES,
        extra_headers=DEFAULT_EXTRA_HEADERS,
        extra_body=DEFAULT_EXTRA_BODY,
    )

    agent_toolsets = []
    if mcp_url:
        if "sse" in mcp_url.lower():
            server = MCPServerSSE(
                mcp_url,
                http_client=httpx.AsyncClient(
                    verify=ssl_verify, timeout=DEFAULT_TIMEOUT
                ),
            )
        else:
            server = MCPServerStreamableHTTP(
                mcp_url,
                http_client=httpx.AsyncClient(
                    verify=ssl_verify, timeout=DEFAULT_TIMEOUT
                ),
            )
        agent_toolsets.append(server)
        logger.info(f"Connected to MCP Server: {mcp_url}")
    elif mcp_config:
        mcp_toolset = load_mcp_servers(mcp_config)
        for server in mcp_toolset:
            if hasattr(server, "http_client"):
                server.http_client = httpx.AsyncClient(
                    verify=ssl_verify, timeout=DEFAULT_TIMEOUT
                )
        agent_toolsets.extend(mcp_toolset)
        logger.info(f"Connected to MCP Config JSON: {mcp_toolset}")

    # Skills are loaded per-agent based on tags

    agent_defs = {
        "ad_hoc_commands": (
            AD_HOC_COMMANDS_AGENT_PROMPT,
            "AnsibleTower_Ad_Hoc_Commands_Agent",
        ),
        "credentials": (CREDENTIALS_AGENT_PROMPT, "AnsibleTower_Credentials_Agent"),
        "groups": (GROUPS_AGENT_PROMPT, "AnsibleTower_Groups_Agent"),
        "hosts": (HOSTS_AGENT_PROMPT, "AnsibleTower_Hosts_Agent"),
        "inventory": (INVENTORY_AGENT_PROMPT, "AnsibleTower_Inventory_Agent"),
        "job_templates": (
            JOB_TEMPLATES_AGENT_PROMPT,
            "AnsibleTower_Job_Templates_Agent",
        ),
        "jobs": (JOBS_AGENT_PROMPT, "AnsibleTower_Jobs_Agent"),
        "organizations": (
            ORGANIZATIONS_AGENT_PROMPT,
            "AnsibleTower_Organizations_Agent",
        ),
        "projects": (PROJECTS_AGENT_PROMPT, "AnsibleTower_Projects_Agent"),
        "schedules": (SCHEDULES_AGENT_PROMPT, "AnsibleTower_Schedules_Agent"),
        "system": (SYSTEM_AGENT_PROMPT, "AnsibleTower_System_Agent"),
        "teams": (TEAMS_AGENT_PROMPT, "AnsibleTower_Teams_Agent"),
        "users": (USERS_AGENT_PROMPT, "AnsibleTower_Users_Agent"),
        "workflow_jobs": (
            WORKFLOW_JOBS_AGENT_PROMPT,
            "AnsibleTower_Workflow_Jobs_Agent",
        ),
        "workflow_templates": (
            WORKFLOW_TEMPLATES_AGENT_PROMPT,
            "AnsibleTower_Workflow_Templates_Agent",
        ),
    }

    supervisor_skills = []
    child_agents = {}
    supervisor_skills_directories = [get_skills_path()]

    for tag, (system_prompt, agent_name) in agent_defs.items():
        tag_toolsets = []
        for ts in agent_toolsets:

            def filter_func(ctx, tool_def, t=tag):
                return tool_in_tag(tool_def, t)

            if hasattr(ts, "filtered"):
                filtered_ts = ts.filtered(filter_func)
                tag_toolsets.append(filtered_ts)
            else:
                pass

        # Load specific skills for this tag
        skill_dir_name = f"ansible-tower-mcp-{tag.replace('_', '-')}"

        child_skills_directories = []

        # Check custom skills directory
        if custom_skills_directory:
            skill_dir_path = os.path.join(custom_skills_directory, skill_dir_name)
            if os.path.exists(skill_dir_path):
                child_skills_directories.append(skill_dir_path)

        # Check default skills directory
        default_skill_path = os.path.join(get_skills_path(), skill_dir_name)
        if os.path.exists(default_skill_path):
            child_skills_directories.append(default_skill_path)

        if child_skills_directories:
            ts = SkillsToolset(directories=child_skills_directories)
            tag_toolsets.append(ts)
            logger.info(
                f"Loaded specialized skills for {tag} from {child_skills_directories}"
            )

        # Collect tool names for logging
        all_tool_names = []
        for ts in tag_toolsets:
            try:
                # Unwrap FilteredToolset
                current_ts = ts
                while hasattr(current_ts, "wrapped"):
                    current_ts = current_ts.wrapped

                # Check for .tools (e.g. SkillsToolset)
                if hasattr(current_ts, "tools") and isinstance(current_ts.tools, dict):
                    all_tool_names.extend(current_ts.tools.keys())
                # Check for ._tools (some implementations might use private attr)
                elif hasattr(current_ts, "_tools") and isinstance(
                    current_ts._tools, dict
                ):
                    all_tool_names.extend(current_ts._tools.keys())
                else:
                    # Fallback for MCP or others where tools are not available sync
                    all_tool_names.append(f"<{type(current_ts).__name__}>")
            except Exception as e:
                logger.info(f"Unable to retrieve toolset: {e}")
                pass

        tool_list_str = ", ".join(all_tool_names)
        logger.info(f"Available tools for {agent_name} ({tag}): {tool_list_str}")
        agent = Agent(
            model=model,
            system_prompt=system_prompt,
            name=agent_name,
            toolsets=tag_toolsets,
            tool_timeout=DEFAULT_TOOL_TIMEOUT,
            model_settings=settings,
        )
        child_agents[tag] = agent

    if custom_skills_directory:
        supervisor_skills_directories.append(custom_skills_directory)
    supervisor_skills.append(SkillsToolset(directories=supervisor_skills_directories))
    logger.info(f"Loaded supervisor skills from: {supervisor_skills_directories}")

    supervisor = Agent(
        name=AGENT_NAME,
        system_prompt=SUPERVISOR_SYSTEM_PROMPT,
        model=model,
        model_settings=settings,
        toolsets=supervisor_skills,
        deps_type=Any,
    )

    @supervisor.tool
    async def assign_task_to_ad_hoc_commands_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to ad_hoc_commands to the Ad Hoc Commands Agent."""
        return (
            await child_agents["ad_hoc_commands"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_credentials_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to credentials to the Credentials Agent."""
        return (
            await child_agents["credentials"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_groups_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to groups to the Groups Agent."""
        return (
            await child_agents["groups"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_hosts_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to hosts to the Hosts Agent."""
        return (
            await child_agents["hosts"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_inventory_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to inventory to the Inventory Agent."""
        return (
            await child_agents["inventory"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_job_templates_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to job_templates to the Job Templates Agent."""
        return (
            await child_agents["job_templates"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_jobs_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to jobs to the Jobs Agent."""
        return (
            await child_agents["jobs"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_organizations_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to organizations to the Organizations Agent."""
        return (
            await child_agents["organizations"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_projects_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to projects to the Projects Agent."""
        return (
            await child_agents["projects"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_schedules_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to schedules to the Schedules Agent."""
        return (
            await child_agents["schedules"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_system_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to system information and settings to the System Agent."""
        return (
            await child_agents["system"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_teams_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to teams to the Teams Agent."""
        return (
            await child_agents["teams"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_users_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to users to the Users Agent."""
        return (
            await child_agents["users"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_workflow_jobs_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to workflow_jobs to the Workflow Jobs Agent."""
        return (
            await child_agents["workflow_jobs"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_workflow_templates_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to workflow_templates to the Workflow Templates Agent."""
        return (
            await child_agents["workflow_templates"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    return supervisor


async def chat(agent: Agent, prompt: str):
    result = await agent.run(prompt)
    print(f"Response:\n\n{result.output}")


async def node_chat(agent: Agent, prompt: str) -> List:
    nodes = []
    async with agent.iter(prompt) as agent_run:
        async for node in agent_run:
            nodes.append(node)
            print(node)
    return nodes


async def stream_chat(agent: Agent, prompt: str) -> None:
    async with agent.run_stream(prompt) as result:
        async for text_chunk in result.stream_text(delta=True):
            print(text_chunk, end="", flush=True)
        print("\nDone!")


def create_agent_server(
    provider: str = DEFAULT_PROVIDER,
    model_id: str = DEFAULT_MODEL_ID,
    base_url: Optional[str] = DEFAULT_LLM_BASE_URL,
    api_key: Optional[str] = DEFAULT_LLM_API_KEY,
    mcp_url: str = DEFAULT_MCP_URL,
    mcp_config: str = DEFAULT_MCP_CONFIG,
    custom_skills_directory: Optional[str] = DEFAULT_CUSTOM_SKILLS_DIRECTORY,
    debug: Optional[bool] = DEFAULT_DEBUG,
    host: Optional[str] = DEFAULT_HOST,
    port: Optional[int] = DEFAULT_PORT,
    enable_web_ui: bool = DEFAULT_ENABLE_WEB_UI,
    ssl_verify: bool = DEFAULT_SSL_VERIFY,
):
    print(
        f"Starting {AGENT_NAME}:"
        f"\tprovider={provider}"
        f"\tmodel={model_id}"
        f"\tbase_url={base_url}"
        f"\tmcp={mcp_url} | {mcp_config}"
        f"\tssl_verify={ssl_verify}"
    )
    agent = create_agent(
        provider=provider,
        model_id=model_id,
        base_url=base_url,
        api_key=api_key,
        mcp_url=mcp_url,
        mcp_config=mcp_config,
        custom_skills_directory=custom_skills_directory,
        ssl_verify=ssl_verify,
    )

    # Always load default skills

    skills = load_skills_from_directory(get_skills_path())

    logger.info(f"Loaded {len(skills)} default skills from {get_skills_path()}")

    # Load custom skills if provided

    if custom_skills_directory and os.path.exists(custom_skills_directory):

        custom_skills = load_skills_from_directory(custom_skills_directory)

        skills.extend(custom_skills)

        logger.info(
            f"Loaded {len(custom_skills)} custom skills from {custom_skills_directory}"
        )

    if not skills:

        skills = [
            Skill(
                id="ansible_tower_agent",
                name="Ansible Tower Agent",
                description="General access to Ansible Tower tools",
                tags=["ansible-tower"],
                input_modes=["text"],
                output_modes=["text"],
            )
        ]

    a2a_app = agent.to_a2a(
        name=AGENT_NAME,
        description=AGENT_DESCRIPTION,
        version=__version__,
        skills=skills,
        debug=debug,
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if hasattr(a2a_app, "router") and hasattr(a2a_app.router, "lifespan_context"):
            async with a2a_app.router.lifespan_context(a2a_app):
                yield
        else:
            yield

    app = FastAPI(
        title=f"{AGENT_NAME} - A2A + AG-UI Server",
        description=AGENT_DESCRIPTION,
        debug=debug,
        lifespan=lifespan,
    )

    @app.get("/health")
    async def health_check():
        return {"status": "OK"}

    app.mount("/a2a", a2a_app)

    @app.post("/ag-ui")
    async def ag_ui_endpoint(request: Request) -> Response:
        accept = request.headers.get("accept", SSE_CONTENT_TYPE)
        try:
            run_input = AGUIAdapter.build_run_input(await request.body())
        except ValidationError as e:
            return Response(
                content=json.dumps(e.json()),
                media_type="application/json",
                status_code=422,
            )

        if hasattr(run_input, "messages"):
            run_input.messages = prune_large_messages(run_input.messages)

        adapter = AGUIAdapter(agent=agent, run_input=run_input, accept=accept)
        event_stream = adapter.run_stream()
        sse_stream = adapter.encode_stream(event_stream)

        return StreamingResponse(
            sse_stream,
            media_type=accept,
        )

    if enable_web_ui:
        web_ui = agent.to_web(instructions=SUPERVISOR_SYSTEM_PROMPT)
        app.mount("/", web_ui)
        logger.info(
            "Starting server on %s:%s (A2A at /a2a, AG-UI at /ag-ui, Web UI: %s)",
            host,
            port,
            "Enabled at /" if enable_web_ui else "Disabled",
        )

    uvicorn.run(
        app,
        host=host,
        port=port,
        timeout_keep_alive=1800,
        timeout_graceful_shutdown=60,
        log_level="debug" if debug else "info",
    )


def agent_server():
    print(f"ansible_tower_agent v{__version__}")
    parser = argparse.ArgumentParser(
        add_help=False, description=f"Run the {AGENT_NAME} A2A + AG-UI Server"
    )
    parser.add_argument(
        "--host", default=DEFAULT_HOST, help="Host to bind the server to"
    )
    parser.add_argument(
        "--port", type=int, default=DEFAULT_PORT, help="Port to bind the server to"
    )
    parser.add_argument("--debug", type=bool, default=DEFAULT_DEBUG, help="Debug mode")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")

    parser.add_argument(
        "--provider",
        default=DEFAULT_PROVIDER,
        choices=["openai", "anthropic", "google", "huggingface"],
        help="LLM Provider",
    )
    parser.add_argument("--model-id", default=DEFAULT_MODEL_ID, help="LLM Model ID")
    parser.add_argument(
        "--base-url",
        default=DEFAULT_LLM_BASE_URL,
        help="LLM Base URL (for OpenAI compatible providers)",
    )
    parser.add_argument("--api-key", default=DEFAULT_LLM_API_KEY, help="LLM API Key")
    parser.add_argument("--mcp-url", default=DEFAULT_MCP_URL, help="MCP Server URL")
    parser.add_argument(
        "--mcp-config", default=DEFAULT_MCP_CONFIG, help="MCP Server Config"
    )
    parser.add_argument(
        "--custom-skills-directory",
        default=DEFAULT_CUSTOM_SKILLS_DIRECTORY,
        help="Directory containing additional custom agent skills",
    )
    parser.add_argument(
        "--web",
        action="store_true",
        default=DEFAULT_ENABLE_WEB_UI,
        help="Enable Pydantic AI Web UI",
    )

    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable SSL verification for LLM requests (Use with caution)",
    )
    parser.add_argument("--help", action="store_true", help="Show usage")

    args = parser.parse_args()

    if hasattr(args, "help") and args.help:

        parser.print_help()

        sys.exit(0)

    if args.debug:
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler()],
            force=True,
        )
        logging.getLogger("pydantic_ai").setLevel(logging.DEBUG)
        logging.getLogger("fastmcp").setLevel(logging.DEBUG)
        logging.getLogger("httpcore").setLevel(logging.DEBUG)
        logging.getLogger("httpx").setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")

    create_agent_server(
        provider=args.provider,
        model_id=args.model_id,
        base_url=args.base_url,
        api_key=args.api_key,
        mcp_url=args.mcp_url,
        mcp_config=args.mcp_config,
        custom_skills_directory=args.custom_skills_directory,
        debug=args.debug,
        host=args.host,
        port=args.port,
        enable_web_ui=args.web,
        ssl_verify=not args.insecure,
    )


if __name__ == "__main__":
    agent_server()
