#!/usr/bin/python
import warnings

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

import logging
import os
import sys
from typing import Any

from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import create_mcp_server
from dotenv import find_dotenv, load_dotenv
from starlette.requests import Request
from starlette.responses import JSONResponse

from ansible_tower_mcp.auth import get_client

__version__ = "1.16.0"

logger = get_logger(name="ansible-tower-mcp")
logger.setLevel(logging.INFO)


def register_inventory_tools(mcp: FastMCP):
    @mcp.tool(tags={"inventory"})
    async def ansible_tower_inventory(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_inventories', 'get_inventory', 'create_inventory', 'update_inventory', 'delete_inventory'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower inventory operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_inventories":
            return client.list_inventories(**kwargs)
        if action == "get_inventory":
            return client.get_inventory(**kwargs)
        if action == "create_inventory":
            return client.create_inventory(**kwargs)
        if action == "update_inventory":
            return client.update_inventory(**kwargs)
        if action == "delete_inventory":
            return client.delete_inventory(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_hosts_tools(mcp: FastMCP):
    @mcp.tool(tags={"hosts"})
    async def ansible_tower_hosts(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_hosts', 'get_host', 'create_host', 'update_host', 'delete_host'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower hosts operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_hosts":
            return client.list_hosts(**kwargs)
        if action == "get_host":
            return client.get_host(**kwargs)
        if action == "create_host":
            return client.create_host(**kwargs)
        if action == "update_host":
            return client.update_host(**kwargs)
        if action == "delete_host":
            return client.delete_host(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_groups_tools(mcp: FastMCP):
    @mcp.tool(tags={"groups"})
    async def ansible_tower_groups(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_groups', 'get_group', 'create_group', 'update_group', 'delete_group', 'add_host_to_group', 'remove_host_from_group'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower groups operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_groups":
            return client.list_groups(**kwargs)
        if action == "get_group":
            return client.get_group(**kwargs)
        if action == "create_group":
            return client.create_group(**kwargs)
        if action == "update_group":
            return client.update_group(**kwargs)
        if action == "delete_group":
            return client.delete_group(**kwargs)
        if action == "add_host_to_group":
            return client.add_host_to_group(**kwargs)
        if action == "remove_host_from_group":
            return client.remove_host_from_group(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_job_templates_tools(mcp: FastMCP):
    @mcp.tool(tags={"job-templates"})
    async def ansible_tower_job_templates(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_job_templates', 'get_job_template', 'create_job_template', 'update_job_template', 'delete_job_template', 'launch_job'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower job templates operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_job_templates":
            return client.list_job_templates(**kwargs)
        if action == "get_job_template":
            return client.get_job_template(**kwargs)
        if action == "create_job_template":
            return client.create_job_template(**kwargs)
        if action == "update_job_template":
            return client.update_job_template(**kwargs)
        if action == "delete_job_template":
            return client.delete_job_template(**kwargs)
        if action == "launch_job":
            return client.launch_job(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_jobs_tools(mcp: FastMCP):
    @mcp.tool(tags={"jobs"})
    async def ansible_tower_jobs(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_jobs', 'get_job', 'cancel_job', 'relaunch_job', 'get_job_events', 'get_job_stdout'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower jobs operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_jobs":
            return client.list_jobs(**kwargs)
        if action == "get_job":
            return client.get_job(**kwargs)
        if action == "cancel_job":
            return client.cancel_job(**kwargs)
        if action == "relaunch_job":
            return client.relaunch_job(**kwargs)
        if action == "get_job_events":
            return client.get_job_events(**kwargs)
        if action == "get_job_stdout":
            return client.get_job_stdout(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_projects_tools(mcp: FastMCP):
    @mcp.tool(tags={"projects"})
    async def ansible_tower_projects(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_projects', 'get_project', 'create_project', 'update_project', 'delete_project', 'sync_project'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower projects operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_projects":
            return client.list_projects(**kwargs)
        if action == "get_project":
            return client.get_project(**kwargs)
        if action == "create_project":
            return client.create_project(**kwargs)
        if action == "update_project":
            return client.update_project(**kwargs)
        if action == "delete_project":
            return client.delete_project(**kwargs)
        if action == "sync_project":
            return client.sync_project(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_credentials_tools(mcp: FastMCP):
    @mcp.tool(tags={"credentials"})
    async def ansible_tower_credentials(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_credentials', 'get_credential', 'list_credential_types', 'create_credential', 'update_credential', 'delete_credential'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower credentials operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_credentials":
            return client.list_credentials(**kwargs)
        if action == "get_credential":
            return client.get_credential(**kwargs)
        if action == "list_credential_types":
            return client.list_credential_types(**kwargs)
        if action == "create_credential":
            return client.create_credential(**kwargs)
        if action == "update_credential":
            return client.update_credential(**kwargs)
        if action == "delete_credential":
            return client.delete_credential(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_organizations_tools(mcp: FastMCP):
    @mcp.tool(tags={"organizations"})
    async def ansible_tower_organizations(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_organizations', 'get_organization', 'create_organization', 'update_organization', 'delete_organization'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower organizations operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_organizations":
            return client.list_organizations(**kwargs)
        if action == "get_organization":
            return client.get_organization(**kwargs)
        if action == "create_organization":
            return client.create_organization(**kwargs)
        if action == "update_organization":
            return client.update_organization(**kwargs)
        if action == "delete_organization":
            return client.delete_organization(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_teams_tools(mcp: FastMCP):
    @mcp.tool(tags={"teams"})
    async def ansible_tower_teams(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_teams', 'get_team', 'create_team', 'update_team', 'delete_team'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower teams operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_teams":
            return client.list_teams(**kwargs)
        if action == "get_team":
            return client.get_team(**kwargs)
        if action == "create_team":
            return client.create_team(**kwargs)
        if action == "update_team":
            return client.update_team(**kwargs)
        if action == "delete_team":
            return client.delete_team(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_users_tools(mcp: FastMCP):
    @mcp.tool(tags={"users"})
    async def ansible_tower_users(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_users', 'get_user', 'create_user', 'update_user', 'delete_user'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower users operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_users":
            return client.list_users(**kwargs)
        if action == "get_user":
            return client.get_user(**kwargs)
        if action == "create_user":
            return client.create_user(**kwargs)
        if action == "update_user":
            return client.update_user(**kwargs)
        if action == "delete_user":
            return client.delete_user(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_ad_hoc_commands_tools(mcp: FastMCP):
    @mcp.tool(tags={"ad_hoc_commands"})
    async def ansible_tower_ad_hoc_commands(
        action: str = Field(
            description="Action to perform. Must be one of: 'run_ad_hoc_command', 'get_ad_hoc_command', 'cancel_ad_hoc_command'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower ad hoc commands operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "run_ad_hoc_command":
            return client.run_ad_hoc_command(**kwargs)
        if action == "get_ad_hoc_command":
            return client.get_ad_hoc_command(**kwargs)
        if action == "cancel_ad_hoc_command":
            return client.cancel_ad_hoc_command(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_workflow_templates_tools(mcp: FastMCP):
    @mcp.tool(tags={"workflow_templates"})
    async def ansible_tower_workflow_templates(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_workflow_templates', 'get_workflow_template', 'launch_workflow'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower workflow templates operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_workflow_templates":
            return client.list_workflow_templates(**kwargs)
        if action == "get_workflow_template":
            return client.get_workflow_template(**kwargs)
        if action == "launch_workflow":
            return client.launch_workflow(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_workflow_jobs_tools(mcp: FastMCP):
    @mcp.tool(tags={"workflow_jobs"})
    async def ansible_tower_workflow_jobs(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_workflow_jobs', 'get_workflow_job', 'cancel_workflow_job'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower workflow jobs operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_workflow_jobs":
            return client.list_workflow_jobs(**kwargs)
        if action == "get_workflow_job":
            return client.get_workflow_job(**kwargs)
        if action == "cancel_workflow_job":
            return client.cancel_workflow_job(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_schedules_tools(mcp: FastMCP):
    @mcp.tool(tags={"schedules"})
    async def ansible_tower_schedules(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_schedules', 'get_schedule', 'create_schedule', 'update_schedule', 'delete_schedule'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower schedules operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_schedules":
            return client.list_schedules(**kwargs)
        if action == "get_schedule":
            return client.get_schedule(**kwargs)
        if action == "create_schedule":
            return client.create_schedule(**kwargs)
        if action == "update_schedule":
            return client.update_schedule(**kwargs)
        if action == "delete_schedule":
            return client.delete_schedule(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_system_tools(mcp: FastMCP):
    @mcp.tool(tags={"system"})
    async def ansible_tower_system(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_ansible_version', 'get_dashboard_stats', 'get_metrics'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower system operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_ansible_version":
            return client.get_ansible_version(**kwargs)
        if action == "get_dashboard_stats":
            return client.get_dashboard_stats(**kwargs)
        if action == "get_metrics":
            return client.get_metrics(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def get_mcp_instance() -> tuple[Any, ...]:
    """Initialize and return the MCP instance."""
    load_dotenv(find_dotenv())
    args, mcp, middlewares = create_mcp_server(
        name="ansible-tower-mcp MCP",
        version=__version__,
        instructions="ansible-tower-mcp MCP Server — Condensed Action-Routed Tools.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    DEFAULT_INVENTORYTOOL = to_boolean(os.getenv("INVENTORYTOOL", "True"))
    if DEFAULT_INVENTORYTOOL:
        register_inventory_tools(mcp)
    DEFAULT_HOSTSTOOL = to_boolean(os.getenv("HOSTSTOOL", "True"))
    if DEFAULT_HOSTSTOOL:
        register_hosts_tools(mcp)
    DEFAULT_GROUPSTOOL = to_boolean(os.getenv("GROUPSTOOL", "True"))
    if DEFAULT_GROUPSTOOL:
        register_groups_tools(mcp)
    DEFAULT_JOB_TEMPLATESTOOL = to_boolean(os.getenv("JOB_TEMPLATESTOOL", "True"))
    if DEFAULT_JOB_TEMPLATESTOOL:
        register_job_templates_tools(mcp)
    DEFAULT_JOBSTOOL = to_boolean(os.getenv("JOBSTOOL", "True"))
    if DEFAULT_JOBSTOOL:
        register_jobs_tools(mcp)
    DEFAULT_PROJECTSTOOL = to_boolean(os.getenv("PROJECTSTOOL", "True"))
    if DEFAULT_PROJECTSTOOL:
        register_projects_tools(mcp)
    DEFAULT_CREDENTIALSTOOL = to_boolean(os.getenv("CREDENTIALSTOOL", "True"))
    if DEFAULT_CREDENTIALSTOOL:
        register_credentials_tools(mcp)
    DEFAULT_ORGANIZATIONSTOOL = to_boolean(os.getenv("ORGANIZATIONSTOOL", "True"))
    if DEFAULT_ORGANIZATIONSTOOL:
        register_organizations_tools(mcp)
    DEFAULT_TEAMSTOOL = to_boolean(os.getenv("TEAMSTOOL", "True"))
    if DEFAULT_TEAMSTOOL:
        register_teams_tools(mcp)
    DEFAULT_USERSTOOL = to_boolean(os.getenv("USERSTOOL", "True"))
    if DEFAULT_USERSTOOL:
        register_users_tools(mcp)
    DEFAULT_AD_HOC_COMMANDSTOOL = to_boolean(os.getenv("AD_HOC_COMMANDSTOOL", "True"))
    if DEFAULT_AD_HOC_COMMANDSTOOL:
        register_ad_hoc_commands_tools(mcp)
    DEFAULT_WORKFLOW_TEMPLATESTOOL = to_boolean(
        os.getenv("WORKFLOW_TEMPLATESTOOL", "True")
    )
    if DEFAULT_WORKFLOW_TEMPLATESTOOL:
        register_workflow_templates_tools(mcp)
    DEFAULT_WORKFLOW_JOBSTOOL = to_boolean(os.getenv("WORKFLOW_JOBSTOOL", "True"))
    if DEFAULT_WORKFLOW_JOBSTOOL:
        register_workflow_jobs_tools(mcp)
    DEFAULT_SCHEDULESTOOL = to_boolean(os.getenv("SCHEDULESTOOL", "True"))
    if DEFAULT_SCHEDULESTOOL:
        register_schedules_tools(mcp)
    DEFAULT_SYSTEMTOOL = to_boolean(os.getenv("SYSTEMTOOL", "True"))
    if DEFAULT_SYSTEMTOOL:
        register_system_tools(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)
    return mcp, args, middlewares


def mcp_server() -> None:
    mcp, args, middlewares = get_mcp_instance()
    print(f"ansible-tower-mcp MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error("Invalid transport", extra={"transport": args.transport})
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
