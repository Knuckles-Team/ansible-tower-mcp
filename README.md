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

*Version: 3.0.0*

> **Documentation** — Installation, deployment, and usage across the API, CLI,
> MCP, and A2A agent interfaces are maintained in the
> [official documentation](https://knuckles-team.github.io/ansible-tower-mcp/).

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

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](docs/index.md).

---

## MCP

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools

The table below is auto-generated from the live server — do not edit by hand.

<!-- MCP-TOOLS-TABLE:START -->

#### Condensed action-routed tools (default — `MCP_TOOL_MODE=condensed`)

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `ansible_tower_ad_hoc_commands` | `AD_HOC_COMMANDSTOOL` | Manage ansible tower ad hoc commands operations. |
| `ansible_tower_credentials` | `CREDENTIALSTOOL` | Manage ansible tower credentials operations. |
| `ansible_tower_groups` | `GROUPSTOOL` | Manage ansible tower groups operations. |
| `ansible_tower_hosts` | `HOSTSTOOL` | Manage ansible tower hosts operations. |
| `ansible_tower_inventory` | `INVENTORYTOOL` | Manage ansible tower inventory operations. |
| `ansible_tower_job_templates` | `JOB_TEMPLATESTOOL` | Manage ansible tower job templates operations. |
| `ansible_tower_jobs` | `JOBSTOOL` | Manage ansible tower jobs operations. |
| `ansible_tower_organizations` | `ORGANIZATIONSTOOL` | Manage ansible tower organizations operations. |
| `ansible_tower_projects` | `PROJECTSTOOL` | Manage ansible tower projects operations. |
| `ansible_tower_schedules` | `SCHEDULESTOOL` | Manage ansible tower schedules operations. |
| `ansible_tower_system` | `SYSTEMTOOL` | Manage ansible tower system operations. |
| `ansible_tower_teams` | `TEAMSTOOL` | Manage ansible tower teams operations. |
| `ansible_tower_users` | `USERSTOOL` | Manage ansible tower users operations. |
| `ansible_tower_workflow_jobs` | `WORKFLOW_JOBSTOOL` | Manage ansible tower workflow jobs operations. |
| `ansible_tower_workflow_templates` | `WORKFLOW_TEMPLATESTOOL` | Manage ansible tower workflow templates operations. |

#### Verbose 1:1 API-mapped tools (`MCP_TOOL_MODE=verbose` or `both`)

<details>
<summary>76 per-operation tools — one per public API method (click to expand)</summary>

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `ansible_tower_add_host_to_group` | `APITOOL` | Invoke the add_host_to_group operation. |
| `ansible_tower_cancel_ad_hoc_command` | `APITOOL` | Invoke the cancel_ad_hoc_command operation. |
| `ansible_tower_cancel_job` | `APITOOL` | Invoke the cancel_job operation. |
| `ansible_tower_cancel_workflow_job` | `APITOOL` | Invoke the cancel_workflow_job operation. |
| `ansible_tower_create_credential` | `APITOOL` | Invoke the create_credential operation. |
| `ansible_tower_create_group` | `APITOOL` | Invoke the create_group operation. |
| `ansible_tower_create_host` | `APITOOL` | Invoke the create_host operation. |
| `ansible_tower_create_inventory` | `APITOOL` | Invoke the create_inventory operation. |
| `ansible_tower_create_job_template` | `APITOOL` | Invoke the create_job_template operation. |
| `ansible_tower_create_organization` | `APITOOL` | Invoke the create_organization operation. |
| `ansible_tower_create_project` | `APITOOL` | Invoke the create_project operation. |
| `ansible_tower_create_schedule` | `APITOOL` | Invoke the create_schedule operation. |
| `ansible_tower_create_team` | `APITOOL` | Invoke the create_team operation. |
| `ansible_tower_create_user` | `APITOOL` | Invoke the create_user operation. |
| `ansible_tower_delete_credential` | `APITOOL` | Invoke the delete_credential operation. |
| `ansible_tower_delete_group` | `APITOOL` | Invoke the delete_group operation. |
| `ansible_tower_delete_host` | `APITOOL` | Invoke the delete_host operation. |
| `ansible_tower_delete_inventory` | `APITOOL` | Invoke the delete_inventory operation. |
| `ansible_tower_delete_job_template` | `APITOOL` | Invoke the delete_job_template operation. |
| `ansible_tower_delete_organization` | `APITOOL` | Invoke the delete_organization operation. |
| `ansible_tower_delete_project` | `APITOOL` | Invoke the delete_project operation. |
| `ansible_tower_delete_schedule` | `APITOOL` | Invoke the delete_schedule operation. |
| `ansible_tower_delete_team` | `APITOOL` | Invoke the delete_team operation. |
| `ansible_tower_delete_user` | `APITOOL` | Invoke the delete_user operation. |
| `ansible_tower_get_ad_hoc_command` | `APITOOL` | Invoke the get_ad_hoc_command operation. |
| `ansible_tower_get_ansible_version` | `APITOOL` | Invoke the get_ansible_version operation. |
| `ansible_tower_get_credential` | `APITOOL` | Invoke the get_credential operation. |
| `ansible_tower_get_dashboard_stats` | `APITOOL` | Invoke the get_dashboard_stats operation. |
| `ansible_tower_get_group` | `APITOOL` | Invoke the get_group operation. |
| `ansible_tower_get_headers` | `BASE_API_CLIENTTOOL` | Get request headers with authorization. |
| `ansible_tower_get_host` | `APITOOL` | Invoke the get_host operation. |
| `ansible_tower_get_inventory` | `APITOOL` | Invoke the get_inventory operation. |
| `ansible_tower_get_job` | `APITOOL` | Invoke the get_job operation. |
| `ansible_tower_get_job_events` | `APITOOL` | Invoke the get_job_events operation. |
| `ansible_tower_get_job_stdout` | `APITOOL` | Invoke the get_job_stdout operation. |
| `ansible_tower_get_job_template` | `APITOOL` | Invoke the get_job_template operation. |
| `ansible_tower_get_metrics` | `APITOOL` | Invoke the get_metrics operation. |
| `ansible_tower_get_organization` | `APITOOL` | Invoke the get_organization operation. |
| `ansible_tower_get_project` | `APITOOL` | Invoke the get_project operation. |
| `ansible_tower_get_schedule` | `APITOOL` | Invoke the get_schedule operation. |
| `ansible_tower_get_team` | `APITOOL` | Invoke the get_team operation. |
| `ansible_tower_get_token` | `BASE_API_CLIENTTOOL` | Authenticate and get token using web session approach. |
| `ansible_tower_get_user` | `APITOOL` | Invoke the get_user operation. |
| `ansible_tower_get_workflow_job` | `APITOOL` | Invoke the get_workflow_job operation. |
| `ansible_tower_get_workflow_template` | `APITOOL` | Invoke the get_workflow_template operation. |
| `ansible_tower_handle_pagination` | `BASE_API_CLIENTTOOL` | Handle paginated results from Ansible API. |
| `ansible_tower_launch_job` | `APITOOL` | Invoke the launch_job operation. |
| `ansible_tower_launch_workflow` | `APITOOL` | Invoke the launch_workflow operation. |
| `ansible_tower_list_credential_types` | `APITOOL` | Invoke the list_credential_types operation. |
| `ansible_tower_list_credentials` | `APITOOL` | Invoke the list_credentials operation. |
| `ansible_tower_list_groups` | `APITOOL` | Invoke the list_groups operation. |
| `ansible_tower_list_hosts` | `APITOOL` | Invoke the list_hosts operation. |
| `ansible_tower_list_inventories` | `APITOOL` | Invoke the list_inventories operation. |
| `ansible_tower_list_job_templates` | `APITOOL` | Invoke the list_job_templates operation. |
| `ansible_tower_list_jobs` | `APITOOL` | Invoke the list_jobs operation. |
| `ansible_tower_list_organizations` | `APITOOL` | Invoke the list_organizations operation. |
| `ansible_tower_list_projects` | `APITOOL` | Invoke the list_projects operation. |
| `ansible_tower_list_schedules` | `APITOOL` | Invoke the list_schedules operation. |
| `ansible_tower_list_teams` | `APITOOL` | Invoke the list_teams operation. |
| `ansible_tower_list_users` | `APITOOL` | Invoke the list_users operation. |
| `ansible_tower_list_workflow_jobs` | `APITOOL` | Invoke the list_workflow_jobs operation. |
| `ansible_tower_list_workflow_templates` | `APITOOL` | Invoke the list_workflow_templates operation. |
| `ansible_tower_remove_host_from_group` | `APITOOL` | Invoke the remove_host_from_group operation. |
| `ansible_tower_request` | `BASE_API_CLIENTTOOL` | Make a request to the Ansible API. |
| `ansible_tower_run_ad_hoc_command` | `APITOOL` | Invoke the run_ad_hoc_command operation. |
| `ansible_tower_sync_project` | `APITOOL` | Invoke the sync_project operation. |
| `ansible_tower_update_credential` | `APITOOL` | Invoke the update_credential operation. |
| `ansible_tower_update_group` | `APITOOL` | Invoke the update_group operation. |
| `ansible_tower_update_host` | `APITOOL` | Invoke the update_host operation. |
| `ansible_tower_update_inventory` | `APITOOL` | Invoke the update_inventory operation. |
| `ansible_tower_update_job_template` | `APITOOL` | Invoke the update_job_template operation. |
| `ansible_tower_update_organization` | `APITOOL` | Invoke the update_organization operation. |
| `ansible_tower_update_project` | `APITOOL` | Invoke the update_project operation. |
| `ansible_tower_update_schedule` | `APITOOL` | Invoke the update_schedule operation. |
| `ansible_tower_update_team` | `APITOOL` | Invoke the update_team operation. |
| `ansible_tower_update_user` | `APITOOL` | Invoke the update_user operation. |

</details>

_15 action-routed tool(s) (default) · 76 verbose 1:1 tool(s). Each is enabled unless its `<DOMAIN>TOOL` toggle is set false; `MCP_TOOL_MODE` selects the surface (`condensed` default · `verbose` 1:1 · `both`). Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/usage.md](docs/usage.md).

### Dynamic Tool Selection & Visibility

This MCP server supports dynamic toolset selection and visibility filtering at runtime. This allows you to restrict the set of exposed tools in order to prevent blowing up the LLM's context window.

You can configure tool filtering via multiple input channels:

- **CLI Arguments:** Pass `--tools` or `--toolsets` (or their disabled counterparts `--disabled-tools` and `--disabled-toolsets`) during startup.
- **Environment Variables:** Define standard environment variables:
  - `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS`
  - `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS`
- **HTTP SSE Request Headers:** Pass custom headers during transport initialization:
  - `x-mcp-enabled-tools` / `x-mcp-disabled-tools`
  - `x-mcp-enabled-tags` / `x-mcp-disabled-tags`
- **HTTP SSE Request Query Parameters:** Append query parameters directly to your transport connection URL:
  - `?tools=tool1,tool2`
  - `?tags=tag1`

When query strings or parameters are supplied, an LLM-free **Knowledge Graph resolution layer** (using `DynamicToolOrchestrator`) matches query intents against known tool tags, names, or descriptions, with safe fallback and automated 24-hour background cache refreshing.

---

### MCP Configuration Examples

<!-- MCP-CONFIG-EXAMPLES:START -->

> **Install the connector-focused `[mcp]` extra.** Examples use `ansible-tower-mcp[mcp]` to add
> FastMCP / FastAPI through `agent-utilities[mcp]`; the required Agent Utilities core
> still carries `epistemic-graph[full]`. The `[agent-runtime]` extra additionally
> enables model orchestration.

#### stdio Transport (local IDEs — Cursor, Claude Desktop, VS Code)

```json
{
  "mcpServers": {
    "ansible-tower-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "ansible-tower-mcp[mcp]",
        "ansible-tower-mcp"
      ],
      "env": {
        "MCP_TOOL_MODE": "intent",
        "AD_HOC_COMMANDSTOOL": "True",
        "ANSIBLE_BASE_URL": "https://ansible.example.com",
        "ANSIBLE_CLIENT_ID": "<YOUR_ANSIBLE_CLIENT_ID>",
        "ANSIBLE_CLIENT_SECRET": "<YOUR_ANSIBLE_CLIENT_SECRET>",
        "ANSIBLE_PASSWORD": "<YOUR_ANSIBLE_PASSWORD>",
        "ANSIBLE_USERNAME": "<YOUR_ANSIBLE_USERNAME>",
        "CREDENTIALSTOOL": "True",
        "DELEGATED_SCOPES": "api",
        "GROUPSTOOL": "True",
        "HOSTSTOOL": "True",
        "INVENTORYTOOL": "True",
        "JOBSTOOL": "True",
        "JOB_TEMPLATESTOOL": "True",
        "ORGANIZATIONSTOOL": "True",
        "PROJECTSTOOL": "True",
        "SCHEDULESTOOL": "True",
        "SYSTEMTOOL": "True",
        "TEAMSTOOL": "True",
        "USERSTOOL": "True",
        "WORKFLOW_JOBSTOOL": "True",
        "WORKFLOW_TEMPLATESTOOL": "True"
      }
    }
  }
}
```

Runtime references require an alias-aware launcher such as GraphOS. Other
launchers must omit those entries and inject the resolved values through their
own runtime secret boundary.

#### Streamable-HTTP Transport (networked / production)

```json
{
  "mcpServers": {
    "ansible-tower-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "ansible-tower-mcp[mcp]",
        "ansible-tower-mcp",
        "--transport",
        "streamable-http",
        "--port",
        "8000"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "127.0.0.1",
        "PORT": "8000",
        "MCP_TOOL_MODE": "intent",
        "AD_HOC_COMMANDSTOOL": "True",
        "ANSIBLE_BASE_URL": "https://ansible.example.com",
        "ANSIBLE_CLIENT_ID": "<YOUR_ANSIBLE_CLIENT_ID>",
        "ANSIBLE_CLIENT_SECRET": "<YOUR_ANSIBLE_CLIENT_SECRET>",
        "ANSIBLE_PASSWORD": "<YOUR_ANSIBLE_PASSWORD>",
        "ANSIBLE_USERNAME": "<YOUR_ANSIBLE_USERNAME>",
        "CREDENTIALSTOOL": "True",
        "DELEGATED_SCOPES": "api",
        "GROUPSTOOL": "True",
        "HOSTSTOOL": "True",
        "INVENTORYTOOL": "True",
        "JOBSTOOL": "True",
        "JOB_TEMPLATESTOOL": "True",
        "ORGANIZATIONSTOOL": "True",
        "PROJECTSTOOL": "True",
        "SCHEDULESTOOL": "True",
        "SYSTEMTOOL": "True",
        "TEAMSTOOL": "True",
        "USERSTOOL": "True",
        "WORKFLOW_JOBSTOOL": "True",
        "WORKFLOW_TEMPLATESTOOL": "True"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed Streamable-HTTP instance by `url`:

```json
{
  "mcpServers": {
    "ansible-tower-mcp": {
      "url": "http://localhost:8000/ansible-tower-mcp/mcp"
    }
  }
}
```

Run a reviewed container image as a least-privilege stdio child (no
listener or published port):

```bash
docker run -i --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --pids-limit=256 \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  -e TRANSPORT=stdio \
  -e MCP_TOOL_MODE=intent \
  -e AD_HOC_COMMANDSTOOL=True \
  -e ANSIBLE_BASE_URL=https://ansible.example.com \
  -e ANSIBLE_CLIENT_ID="<YOUR_ANSIBLE_CLIENT_ID>" \
  -e ANSIBLE_CLIENT_SECRET="<YOUR_ANSIBLE_CLIENT_SECRET>" \
  -e ANSIBLE_PASSWORD="<YOUR_ANSIBLE_PASSWORD>" \
  -e ANSIBLE_USERNAME="<YOUR_ANSIBLE_USERNAME>" \
  -e CREDENTIALSTOOL=True \
  -e DELEGATED_SCOPES=api \
  -e GROUPSTOOL=True \
  -e HOSTSTOOL=True \
  -e INVENTORYTOOL=True \
  -e JOBSTOOL=True \
  -e JOB_TEMPLATESTOOL=True \
  -e ORGANIZATIONSTOOL=True \
  -e PROJECTSTOOL=True \
  -e SCHEDULESTOOL=True \
  -e SYSTEMTOOL=True \
  -e TEAMSTOOL=True \
  -e USERSTOOL=True \
  -e WORKFLOW_JOBSTOOL=True \
  -e WORKFLOW_TEMPLATESTOOL=True \
  registry.example.invalid/ansible-tower-mcp@sha256:<digest> ansible-tower-mcp
```

For containerized network HTTP, supply an authenticated TLS ingress (or
direct server TLS), exact `MCP_ALLOWED_HOSTS`, and an exact trusted-proxy
CIDR policy through the operator-owned deployment profile. The generator
does not emit an unauthenticated non-loopback listener.

_Auto-generated from the code-read env surface (`MCP_TOOL_MODE` + package vars) — do not edit._
<!-- MCP-CONFIG-EXAMPLES:END -->

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`ansible-tower-mcp` can run as a local stdio process or container, or behind a remote
network boundary. The
[Deployment guide](https://knuckles-team.github.io/ansible-tower-mcp/deployment/) carries
the detailed transport contract.

- **Local container** — launch a reviewed immutable image as a least-privilege
  stdio child with no listener or published port.
- **Remote URL** — connect through an operator-supplied authenticated HTTPS
  ingress. Keep its URL, outbound identity references, trust profile, and exact
  `MCP_ALLOWED_HOSTS` in `AgentConfig`.
<!-- END GENERATED: additional-deployment-options -->

---

## Environment Variables

<!-- ENV-VARS-TABLE:START -->

#### Package environment variables

| Variable | Example | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` |  |
| `PORT` | `8000` |  |
| `TRANSPORT` | `stdio` | options: stdio, streamable-http, sse |
| `ANSIBLE_BASE_URL` | `https://ansible.example.com` | Ansible Tower / AWX base URL |
| `ANSIBLE_TOWER_TLS_PROFILE` | _(unset)_ | Optional runtime TLS profile selector; verification is mandatory |
| `ANSIBLE_USERNAME` | `<YOUR_ANSIBLE_USERNAME>` | Path 3: username / password auth |
| `ANSIBLE_PASSWORD` | `<YOUR_ANSIBLE_PASSWORD>` |  |
| `ANSIBLE_CLIENT_ID` | `<YOUR_ANSIBLE_CLIENT_ID>` | Path 2: OAuth client-credentials auth |
| `ANSIBLE_CLIENT_SECRET` | `<YOUR_ANSIBLE_CLIENT_SECRET>` |  |
| `AUDIENCE` | — | token-exchange audience (defaults to ANSIBLE_BASE_URL) |
| `DELEGATED_SCOPES` | `api` | space-delimited delegated scopes |
| `ENABLE_OTEL` | `True` |  |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:8080/api/public/otel` |  |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` | `pk-...` |  |
| `OTEL_EXPORTER_OTLP_SECRET_KEY` | `sk-...` |  |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` |  |
| `EUNOMIA_TYPE` | `none` | options: none, embedded, remote |
| `EUNOMIA_POLICY_FILE` | `mcp_policies.json` |  |
| `EUNOMIA_REMOTE_URL` | `http://eunomia-server:8000` |  |
| `INVENTORYTOOL` | `True` |  |
| `HOSTSTOOL` | `True` |  |
| `GROUPSTOOL` | `True` |  |
| `JOB_TEMPLATESTOOL` | `True` |  |
| `JOBSTOOL` | `True` |  |
| `PROJECTSTOOL` | `True` |  |
| `CREDENTIALSTOOL` | `True` |  |
| `ORGANIZATIONSTOOL` | `True` |  |
| `TEAMSTOOL` | `True` |  |
| `USERSTOOL` | `True` |  |
| `AD_HOC_COMMANDSTOOL` | `True` |  |
| `WORKFLOW_TEMPLATESTOOL` | `True` |  |
| `WORKFLOW_JOBSTOOL` | `True` |  |
| `SCHEDULESTOOL` | `True` |  |
| `SYSTEMTOOL` | `True` |  |

#### Inherited agent-utilities variables (apply to every connector)

| Variable | Example | Description |
|----------|---------|-------------|
| `MCP_TOOL_MODE` | `condensed` | Tool surface: `condensed` | `verbose` | `both` |
| `MCP_ENABLED_TOOLS` | — | Comma-separated tool allow-list |
| `MCP_DISABLED_TOOLS` | — | Comma-separated tool deny-list |
| `MCP_ENABLED_TAGS` | — | Comma-separated tag allow-list |
| `MCP_DISABLED_TAGS` | — | Comma-separated tag deny-list |
| `MCP_CLIENT_AUTH` | — | Outbound MCP auth (`oidc-client-credentials` for fleet calls) |
| `OIDC_CLIENT_ID` | — | OIDC client id (service-account auth) |
| `OIDC_CLIENT_SECRET` | — | OIDC client secret (service-account auth) |
| `DEBUG` | `False` | Verbose logging |
| `PYTHONUNBUFFERED` | `1` | Unbuffered stdout (recommended in containers) |
| `MCP_URL` | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to |
| `PROVIDER` | `openai` | LLM provider for the agent |
| `MODEL_ID` | `gpt-4o` | Model id for the agent |
| `ENABLE_WEB_UI` | `True` | Serve the AG-UI web interface |

_34 package + 14 inherited variable(s). Auto-generated from `.env.example` + the shared agent-utilities set — do not edit._
<!-- ENV-VARS-TABLE:END -->


Every variable the server reads, grouped by concern.

### Connection & Credentials
| Variable | Description | Default |
|----------|-------------|---------|
| `ANSIBLE_BASE_URL` | Base URL of the Ansible Tower / AWX instance | — |
| `ANSIBLE_TOWER_TLS_PROFILE` | Optional runtime TLS profile selector | _(unset)_ |
| `ANSIBLE_CLIENT_ID` | OAuth application client id | — |
| `ANSIBLE_CLIENT_SECRET` | OAuth application client secret | — |
| `ANSIBLE_USERNAME` | Username (username/password fallback auth) | — |
| `ANSIBLE_PASSWORD` | Password (username/password fallback auth) | — |

### Authentication mode
Resolved in priority order (first match wins).

| Variable | Auth mode | Notes |
|----------|-----------|-------|
| `ENABLE_DELEGATION` | **1. OIDC delegation** (RFC 8693 token exchange) | Set `true` to flow the caller's IdP token through to Ansible Tower |
| `OIDC_CONFIG_URL` / `OIDC_CLIENT_ID` / `OIDC_CLIENT_SECRET` | OIDC delegation IdP config | Required when delegation is enabled |
| `AUDIENCE` | OIDC delegation token audience | Defaults to `ANSIBLE_BASE_URL` |
| `DELEGATED_SCOPES` | OIDC delegation scopes | `api` |
| `ANSIBLE_CLIENT_ID` (+ `ANSIBLE_CLIENT_SECRET`) | **2. OAuth client credentials** | Used when both are set |
| `ANSIBLE_USERNAME` (+ `ANSIBLE_PASSWORD`) | **3. Username / password** (fallback) | Native token-based auth |

### MCP server / transport
| Variable | Description | Default |
|----------|-------------|---------|
| `TRANSPORT` | `stdio`, `streamable-http`, or `sse` | `stdio` |
| `HOST` | Bind host (HTTP transports) | `0.0.0.0` |
| `PORT` | Bind port (HTTP transports) | `8000` |
| `MCP_TOOL_MODE` | Tool surface: `condensed`, `verbose`, or `both` | `condensed` |
| `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS` | Comma-separated tool allow/deny list | — |
| `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS` | Comma-separated tag allow/deny list | — |
| `DEBUG` | Verbose logging | `False` |
| `PYTHONUNBUFFERED` | Unbuffered stdout (recommended in containers) | `1` |

### Tool toggles
Each action-routed tool can be disabled individually via its toggle env var (set to `false`).
The full list is in the [Available MCP Tools](#available-mcp-tools) table above
(e.g. `JOBSTOOL`, `INVENTORYTOOL`, `JOB_TEMPLATESTOOL`).

### Telemetry & governance
| Variable | Description | Default |
|----------|-------------|---------|
| `ENABLE_OTEL` | Enable OpenTelemetry export | `True` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP collector endpoint | — |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` / `OTEL_EXPORTER_OTLP_SECRET_KEY` | OTLP auth keys | — |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | OTLP protocol (e.g. `http/protobuf`) | — |
| `EUNOMIA_TYPE` | Authorization mode: `none`, `embedded`, `remote` | `none` |
| `EUNOMIA_POLICY_FILE` | Embedded policy file | `mcp_policies.json` |
| `EUNOMIA_REMOTE_URL` | Remote Eunomia server URL | — |

### Agent CLI (full `[agent]` runtime only)
| Variable | Description | Default |
|----------|-------------|---------|
| `MCP_URL` | URL of the MCP server the agent connects to | `http://localhost:8000/mcp` |
| `PROVIDER` | LLM provider (e.g. `openai`) | `openai` |
| `MODEL_ID` | Model id (e.g. `gpt-4o`) | `gpt-4o` |
| `ENABLE_WEB_UI` | Serve the AG-UI web interface | `True` |

See [`.env.example`](.env.example) for a copy-paste starting point.

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
    image: example/ansible-tower-mcp:mcp
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
    image: example/ansible-tower-mcp@sha256:<digest>
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

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/deployment.md](docs/deployment.md).

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

Pick the extra that matches what you want to run:

| Extra | Installs | Use when |
|-------|----------|----------|
| `ansible-tower-mcp[mcp]` | Connector-focused MCP server (`agent-utilities[mcp]` — FastMCP/FastAPI + `epistemic-graph[full]`) | You only run the **MCP server** (smallest install / image) |
| `ansible-tower-mcp[agent]` | Agent runtime (`agent-utilities[agent-runtime,logfire]` — model orchestration + `epistemic-graph[full]`) | You run the **integrated agent** |
| `ansible-tower-mcp[all]` | Everything (`mcp` + `agent` + `logfire`) | Development / both surfaces |

```bash
# Connector-focused MCP server (includes the shared graph engine)
uv pip install "ansible-tower-mcp[mcp]"

# Agent runtime (adds model orchestration to the shared graph engine)
uv pip install "ansible-tower-mcp[agent]"

# Everything (development)
uv pip install "ansible-tower-mcp[all]"      # or: python -m pip install "ansible-tower-mcp[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `example/ansible-tower-mcp:mcp` | `--target mcp` | `ansible-tower-mcp[mcp]` — **connector-focused**, includes `epistemic-graph[full]`; no model-orchestration stack | `ansible-tower-mcp` |
| `example/ansible-tower-mcp@sha256:<digest>` | `--target agent` (default) | `ansible-tower-mcp[agent]` — **agent runtime**, model orchestration + `epistemic-graph[full]` | `ansible-tower-agent` |

```bash
docker build --target mcp   -t example/ansible-tower-mcp:mcp    docker/   # connector-focused MCP server
docker build --target agent -t example/ansible-tower-mcp:agent-local docker/   # agent runtime
```

`docker/mcp.compose.yml` runs the connector-focused `:mcp` server; `docker/agent.compose.yml` runs the
agent (`immutable agent digest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

Both `[mcp]` and `[agent]` carry the **epistemic-graph** engine through the required
Agent Utilities core dependency (`epistemic-graph[full]`). The `[mcp]` extra keeps
the server connector-focused; `[agent]` additionally enables model orchestration. Local
deployments can use the bundled engine. For production or shared state, run
**epistemic-graph as a dedicated database service** and configure the runtime to use it.
Deployment recipes (single-node + Raft HA), connection configuration, and architecture
diagrams are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).

---

## Documentation

The complete documentation is published as the
[official documentation site](https://knuckles-team.github.io/ansible-tower-mcp/)
and is the recommended reference for installation, deployment, and day-to-day
operation.

| Page | Contents |
|---|---|
| [Installation](https://knuckles-team.github.io/ansible-tower-mcp/installation/) | pip, source, extras, prebuilt Docker image |
| [Deployment](https://knuckles-team.github.io/ansible-tower-mcp/deployment/) | run the MCP and agent servers, Compose, Caddy + Technitium, env config |
| [Usage](https://knuckles-team.github.io/ansible-tower-mcp/usage/) | the MCP tools, the `Api` client, the CLI |
| [Overview](https://knuckles-team.github.io/ansible-tower-mcp/overview/) | ecosystem role, concept registry, architecture |
| [Concepts](https://knuckles-team.github.io/ansible-tower-mcp/concepts/) | concept registry (`CONCEPT:ANSIBLE-*`) |

---

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=example&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/example)
![GitHub User's stars](https://img.shields.io/github/stars/example)

---

## Contribute

Contributions are welcome! Please ensure code quality by executing local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Execute test suites using `pytest`


<!-- BEGIN agent-utilities-deployment (generated; do not edit between markers) -->

## Deploy with `agent-utilities-deployment`

Provision this package with the consolidated **`agent-utilities-deployment`**
workflow. It selects an installed-package, editable-source, or immutable-container
path; records only runtime secret and TLS-profile references in `AgentConfig`; and
runs doctor, registration, policy, observability, and rollback gates. Ask your agent
to **"deploy `ansible-tower-mcp` with agent-utilities-deployment"**.

| Install mode | Command |
|------|---------|
| Installed package | `uv tool install "ansible-tower-mcp[mcp]"`, then run `ansible-tower-mcp` |
| Editable source | `uv pip install -e ".[agent]"`, then run `ansible-tower-mcp` |
| Immutable container | deploy `registry.example.invalid/ansible-tower-mcp@sha256:<digest>` through the operator-selected orchestrator |

The repository embeds no deployment profile, credential value, certificate path, or
environment-specific endpoint. Supply those at runtime through `AgentConfig` and the
configured secret provider.

<!-- END agent-utilities-deployment -->

<!-- GOVERNED-CAPABILITY:START -->
## Governed capability contract

This package ships a compact canonical skill surface with specialist procedures
kept as referenced workflows. The current MCP tools, skill metadata,
`connector_manifest.yml`, ontology, mappings, shapes, fixtures, migrations,
tool-schema fingerprints, and certification metadata form one versioned
capability contract. Validate them together; do not rely on stale tool names or
historical per-task skill wrappers.

Runtime endpoints, credentials, certificate trust, tenant identity, retention,
and observability policy are deployment inputs and are never packaged values.
See [Configuration, trust, and privacy](docs/configuration.md) before enabling a
network transport, connector ingestion, GraphOS delegation, or trace export.
<!-- GOVERNED-CAPABILITY:END -->
