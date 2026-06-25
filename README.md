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

*Version: 1.36.0*

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

_15 action-routed tools (default `MCP_TOOL_MODE=condensed`). Each is enabled unless its toggle is set false; set `MCP_TOOL_MODE=verbose` (or `both`) for the 1:1 per-operation surface. Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/mcp.md](docs/mcp.md).

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

> **Install the slim `[mcp]` extra.** All examples below install
> `ansible-tower-mcp[mcp]` — the MCP-server extra that pulls only the FastMCP /
> FastAPI tooling (`agent-utilities[mcp]`). It deliberately **excludes** the heavy
> agent runtime (the epistemic-graph engine, `pydantic-ai`, `dspy`, `llama-index`,
> `tree-sitter`), so `uvx`/container installs are dramatically smaller and faster.
> Use the full `[agent]` extra only when you need the integrated Pydantic AI agent
> (see [Installation](#installation)).

#### stdio Transport (Recommended for local IDEs e.g., Cursor, Claude Desktop)
Configure your IDE's `mcp.json` to launch the MCP server via `uvx`:

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
        "ansible-tower-mcp[mcp]",
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
  knucklessg1/ansible-tower-mcp:mcp
```

> The `:mcp` tag is the **slim MCP-server image** (built from
> `docker/Dockerfile --target mcp`, installing `ansible-tower-mcp[mcp]`). The default
> `:latest` tag is the **full agent image** (`--target agent`, `ansible-tower-mcp[agent]`)
> which also bundles the Pydantic AI agent and the epistemic-graph engine — use it
> when you run `ansible-tower-agent` (the agent), not just the MCP server. See
> [Container images](#container-images-mcp-vs-agent).

---

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`ansible-tower-mcp` can also run as a **local container** (Docker / Podman / `uv`) or be
consumed from a **remote deployment**. The
[Deployment guide](https://knuckles-team.github.io/ansible-tower-mcp/deployment/) has full, copy-paste
`mcp_config.json` for all four transports — **stdio**, **streamable-http**,
**local container / uv**, and **remote URL**:

- **Local container / uv** — launch the server from `mcp_config.json` via `uvx`,
  `docker run`, or `podman run`, or point at a local streamable-http container by `url`.
- **Remote URL** — connect to a server deployed behind Caddy at
  `http://ansible-tower-mcp.arpa/mcp` using the `"url"` key.
<!-- END GENERATED: additional-deployment-options -->

---

## Environment Variables

Every variable the server reads, grouped by concern.

### Connection & Credentials
| Variable | Description | Default |
|----------|-------------|---------|
| `ANSIBLE_BASE_URL` | Base URL of the Ansible Tower / AWX instance | — |
| `ANSIBLE_VERIFY` | TLS certificate verification | `False` |
| `ANSIBLE_TOKEN` | Pre-issued Ansible Tower API token (bearer) | — |
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
    image: knucklessg1/ansible-tower-mcp:mcp
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

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/agent.md](docs/agent.md).

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
| `ansible-tower-mcp[mcp]` | Slim MCP server only (`agent-utilities[mcp]` — FastMCP/FastAPI) | You only run the **MCP server** (smallest install / image) |
| `ansible-tower-mcp[agent]` | Full agent runtime (`agent-utilities[agent,logfire]` — Pydantic AI + the epistemic-graph engine) | You run the **integrated agent** |
| `ansible-tower-mcp[all]` | Everything (`mcp` + `agent` + `logfire`) | Development / both surfaces |

```bash
# MCP server only (recommended for tool hosting — slim deps)
uv pip install "ansible-tower-mcp[mcp]"

# Full agent runtime (Pydantic AI + epistemic-graph engine)
uv pip install "ansible-tower-mcp[agent]"

# Everything (development)
uv pip install "ansible-tower-mcp[all]"      # or: python -m pip install "ansible-tower-mcp[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `knucklessg1/ansible-tower-mcp:mcp` | `--target mcp` | `ansible-tower-mcp[mcp]` — **slim**, no engine/`pydantic-ai`/`dspy`/`llama-index`/`tree-sitter` | `ansible-tower-mcp` |
| `knucklessg1/ansible-tower-mcp:latest` | `--target agent` (default) | `ansible-tower-mcp[agent]` — **full** agent runtime + epistemic-graph engine | `ansible-tower-agent` |

```bash
docker build --target mcp   -t knucklessg1/ansible-tower-mcp:mcp    docker/   # slim MCP server
docker build --target agent -t knucklessg1/ansible-tower-mcp:latest docker/   # full agent
```

`docker/mcp.compose.yml` runs the slim `:mcp` server; `docker/agent.compose.yml` runs the
agent (`:latest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

The **full agent** (`[agent]` / `:latest`) embeds the **epistemic-graph** engine (pulled in
transitively via `agent-utilities[agent]`). For production — or to share one knowledge graph
across multiple agents — run **epistemic-graph as its own database container** and point the
agent at it instead of embedding it. Deployment recipes (single-node + Raft HA), connection
config, and the full database architecture (with diagrams) are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).
The slim `[mcp]` server does **not** require the database.

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


<!-- BEGIN agent-os-genesis-deploy (generated; do not edit between markers) -->

## Deploy with `agent-os-genesis`

This package can be provisioned for you — skill-guided — by the **`agent-os-genesis`**
universal skill (its *single-package deploy mode*): it picks your install method, seeds
secrets to OpenBao/Vault (or `.env`), trusts your enterprise CA, registers the MCP
server, and verifies it — the same machinery that stands up the whole Agent OS, narrowed
to just this package. Ask your agent to **"deploy `ansible-tower-mcp` with agent-os-genesis"**.

| Install mode | Command |
|------|---------|
| Bare-metal, prod (PyPI) | `uvx ansible-tower-mcp` · or `uv tool install ansible-tower-mcp` |
| Bare-metal, dev (editable) | `uv pip install -e ".[all]"` · or `pip install -e ".[all]"` |
| Container, prod | deploy `knucklessg1/ansible-tower-mcp:latest` via docker-compose / swarm / podman / podman-compose / kubernetes |
| Container, dev (editable) | deploy `docker/compose.dev.yml` (source-mounted at `/src`; edits live on restart) |

Secrets are read-existing + seeded via `vault_sync` — you are only prompted for what's missing.

<!-- END agent-os-genesis-deploy -->
