# Ansible Tower Mcp
## CLI or API | MCP | Agent

![PyPI - Version](https://img.shields.io/pypi/v/ansible-tower-mcp)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/ansible-tower-mcp)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/ansible-tower-mcp)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/ansible-tower-mcp)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/ansible-tower-mcp)
![PyPI - License](https://img.shields.io/pypi/l/ansible-tower-mcp)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/ansible-tower-mcp)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/ansible-tower-mcp)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/ansible-tower-mcp)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/ansible-tower-mcp)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/ansible-tower-mcp)
![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/ansible-tower-mcp)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/ansible-tower-mcp)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/ansible-tower-mcp)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/ansible-tower-mcp)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/ansible-tower-mcp)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/ansible-tower-mcp)

*Version: 1.15.0*

---

## Overview

**Ansible Tower Mcp** is a production-grade Agent and Model Context Protocol (MCP) server designed to interface directly with Ansible Tower MCP Server for Agentic AI!.

---

## Key Features

- **Consolidated Action-Routed MCP Tools:** Minimizes token overhead and eliminates tool bloat in LLM contexts by grouping methods into optimized, togglable tool modules.
- **Enterprise-Grade Security:** Comprehensive support for Eunomia policies, OIDC token delegation, and granular execution context tracking.
- **Integrated Graph Agent:** Built-in Pydantic AI agent supporting the Agent Control Protocol (ACP) and standard Web interfaces (AG-UI).
- **Native Telemetry & Tracing:** Out-of-the-box OpenTelemetry exports and native Langfuse tracing.

---

## CLI or API

This agent wraps the Ansible Tower MCP Server for Agentic AI! API. You can interact with it programmatically or via its integrated execution entrypoints.

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](file:///home/apps/workspace/agent-packages/agents/ansible-tower-mcp/docs/index.md).

---

## MCP

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools
| Tool Module | Toggle Env Var | Enabled by Default | Description & Nested Methods |
|-------------|----------------|--------------------|------------------------------|
| **Inventory** | `INVENTORYTOOL` | `True` | Manage ansible tower inventory operations. Action-routed methods: `list_inventories`, `get_inventory`, `create_inventory`, `update_inventory`, `delete_inventory`. |
| **Hosts** | `HOSTSTOOL` | `True` | Manage ansible tower hosts operations. Action-routed methods: `list_hosts`, `get_host`, `create_host`, `update_host`, `delete_host`. |
| **Groups** | `GROUPSTOOL` | `True` | Manage ansible tower groups operations. Action-routed methods: `list_groups`, `get_group`, `create_group`, `update_group`, `delete_group`, `add_host_to_group`, `remove_host_from_group`. |
| **Job Templates** | `JOB_TEMPLATESTOOL` | `True` | Manage ansible tower job templates operations. Action-routed methods: `list_job_templates`, `get_job_template`, `create_job_template`, `update_job_template`, `delete_job_template`, `launch_job`. |
| **Jobs** | `JOBSTOOL` | `True` | Manage ansible tower jobs operations. Action-routed methods: `list_jobs`, `get_job`, `cancel_job`, `relaunch_job`, `get_job_events`, `get_job_stdout`. |
| **Projects** | `PROJECTSTOOL` | `True` | Manage ansible tower projects operations. Action-routed methods: `list_projects`, `get_project`, `create_project`, `update_project`, `delete_project`, `sync_project`. |
| **Credentials** | `CREDENTIALSTOOL` | `True` | Manage ansible tower credentials operations. Action-routed methods: `list_credentials`, `get_credential`, `list_credential_types`, `create_credential`, `update_credential`, `delete_credential`. |
| **Organizations** | `ORGANIZATIONSTOOL` | `True` | Manage ansible tower organizations operations. Action-routed methods: `list_organizations`, `get_organization`, `create_organization`, `update_organization`, `delete_organization`. |
| **Teams** | `TEAMSTOOL` | `True` | Manage ansible tower teams operations. Action-routed methods: `list_teams`, `get_team`, `create_team`, `update_team`, `delete_team`. |
| **Users** | `USERSTOOL` | `True` | Manage ansible tower users operations. Action-routed methods: `list_users`, `get_user`, `create_user`, `update_user`, `delete_user`. |
| **Ad Hoc Commands** | `AD_HOC_COMMANDSTOOL` | `True` | Manage ansible tower ad hoc commands operations. Action-routed methods: `run_ad_hoc_command`, `get_ad_hoc_command`, `cancel_ad_hoc_command`. |
| **Workflow Templates** | `WORKFLOW_TEMPLATESTOOL` | `True` | Manage ansible tower workflow templates operations. Action-routed methods: `list_workflow_templates`, `get_workflow_template`, `launch_workflow`. |
| **Workflow Jobs** | `WORKFLOW_JOBSTOOL` | `True` | Manage ansible tower workflow jobs operations. Action-routed methods: `list_workflow_jobs`, `get_workflow_job`, `cancel_workflow_job`. |
| **Schedules** | `SCHEDULESTOOL` | `True` | Manage ansible tower schedules operations. Action-routed methods: `list_schedules`, `get_schedule`, `create_schedule`, `update_schedule`, `delete_schedule`. |
| **System** | `SYSTEMTOOL` | `True` | Manage ansible tower system operations. Action-routed methods: `get_ansible_version`, `get_dashboard_stats`, `get_metrics`. |

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/mcp.md](file:///home/apps/workspace/agent-packages/agents/ansible-tower-mcp/docs/mcp.md).

### MCP Configuration Examples

#### stdio Transport (Recommended for local IDEs e.g., Cursor, Claude Desktop)
Configure your IDE's `mcp.json` to launch the MCP server via `uvx`:

```json
{
  "mcpServers": {
    "ansible-tower-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "ansible-tower-mcp",
        "ansible-tower-mcp"
      ],
      "env": {
      }
    }
  }
}
```

#### Streamable-HTTP Transport (Recommended for production deployments)
Configure your client's `mcp.json` to launch the Streamable-HTTP server via `uvx` with explicit host and port definition:

```json
{
  "mcpServers": {
    "ansible-tower-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "ansible-tower-mcp",
        "ansible-tower-mcp"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed remote or local Streamable-HTTP instance:

```json
{
  "mcpServers": {
    "ansible-tower-mcp": {
      "url": "http://localhost:8000/ansible-tower-mcp/mcp"
    }
  }
}
```

Deploying the Streamable-HTTP server via Docker:

```bash
docker run -d \
  --name ansible-tower-mcp-mcp \
  -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e PORT=8000 \
  knucklessg1/ansible-tower-mcp:latest
```

---

## Agent

This repository features a fully integrated Pydantic AI Graph Agent. It communicates over the **Agent Control Protocol (ACP)** and interacts seamlessly with the **Agent Web UI (AG-UI)** and Terminal interface.

### Running the Agent CLI
To start the interactive command-line agent:

```bash
# Set credentials

# Run the agent server
ansible-tower-agent --provider openai --model-id gpt-4o
```

### Docker Compose Orchestration
The following `docker/agent.compose.yml` configures the Agent, Web UI, and Terminal Interface together:

```yaml
version: '3.8'

services:
  ansible-tower-mcp-mcp:
    image: knucklessg1/ansible-tower-mcp:latest
    container_name: ansible-tower-mcp-mcp
    hostname: ansible-tower-mcp-mcp
    restart: always
    env_file:
      - ../.env
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  ansible-tower-mcp-agent:
    image: knucklessg1/ansible-tower-mcp:latest
    container_name: ansible-tower-mcp-agent
    hostname: ansible-tower-mcp-agent
    restart: always
    depends_on:
      - ansible-tower-mcp-mcp
    env_file:
      - ../.env
    command: [ "ansible-tower-agent" ]
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=9012
      - MCP_URL=http://ansible-tower-mcp-mcp:8000/mcp
      - PROVIDER=${PROVIDER:-openai}
      - MODEL_ID=${MODEL_ID:-gpt-4o}
      - ENABLE_WEB_UI=True
      - ENABLE_OTEL=True
    ports:
      - "9012:9012"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:9012/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

```

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/agent.md](file:///home/apps/workspace/agent-packages/agents/ansible-tower-mcp/docs/agent.md).

---

## Security & Governance

Built directly upon the enterprise-ready [`agent-utilities`](https://github.com/Knuckles-Team/agent-utilities) core, standard security parameters are fully supported:

### Access Control & Policy Enforcement
- **Eunomia Policies:** Fine-grained, policy-driven tool authorization. Supports `none`, local `embedded` (`mcp_policies.json`), or centralized `remote` modes.
- **OIDC Token Delegation:** Compliant with RFC 8693 token exchange for flowing authenticating user credentials from Web UI / ACP → Agent → MCP.
- **Scoped Credentials:** Execution context runs restricted to the specific caller identity.

### Runtime Security Grid
| Feature | Functionality | Enablement |
|---------|---------------|------------|
| **Tool Guard** | Sensitivity inspection with human-in-the-loop validation | Enabled by default |
| **Prompt Injection Defense** | Input scanning, repetition monitoring, and recursive loop blocks | Enabled by default |
| **Context Safety Guard** | Stuck-loop detectors and contextual overflow preemptive alerts | Enabled by default |

---

## Installation

Install the Python package locally:

```bash
# Using uv (highly recommended)
uv pip install ansible-tower-mcp[all]

# Using standard pip
python -m pip install ansible-tower-mcp[all]
```

---

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)

---

## Contribute

Contributions are welcome! Please ensure code quality by executing local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Execute test suites using `pytest`
