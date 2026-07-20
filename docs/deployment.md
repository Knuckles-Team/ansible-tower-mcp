# Deployment

<!-- BEGIN GENERATED: deployment-options -->
## Deployment Options

`ansible-tower-mcp` supports local stdio, a loopback-only development listener, a
least-privilege stdio container, and a remote authenticated HTTPS boundary.
Provider endpoint, credential, selector, identity, and trust material are supplied
at runtime through `AgentConfig`; none is stored in this repository.

### Installed stdio process

```json
{
  "mcpServers": {
    "ansible-tower": {
      "command": "ansible-tower-mcp",
      "args": [],
      "env": {"MCP_TOOL_MODE": "intent"}
    }
  }
}
```

### Loopback development listener

```bash
ansible-tower-mcp --transport streamable-http --host 127.0.0.1 --port 8000
```

Do not expose this listener beyond loopback. Network deployments require direct TLS
or an explicitly trusted TLS-terminating ingress, configured authentication, exact
`MCP_ALLOWED_HOSTS`, and an exact trusted-proxy CIDR policy.

### Least-privilege local container

```bash
docker run -i --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --pids-limit=256 \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  -e TRANSPORT=stdio \
  registry.example.invalid/ansible-tower-mcp@sha256:<digest> ansible-tower-mcp
```

The operator projects the selected AgentConfig profile into the process at runtime;
the image remains immutable and contains no environment connection profile.

### Remote authenticated HTTPS endpoint

```json
{
  "mcpServers": {
    "ansible-tower": {"url": "https://service.example.invalid/mcp"}
  }
}
```

Store the real remote URL, outbound identity reference, and TLS-profile reference in
`AgentConfig`, not in MCP client JSON or documentation.
<!-- END GENERATED: deployment-options -->

This page covers running `ansible-tower-mcp` as a long-lived server: the
transports, the companion A2A agent server, a Docker Compose stack, putting it
behind a Caddy reverse proxy, and giving it a DNS name with Technitium.

> `ansible-tower-mcp` ships **two** servers: an **MCP server** (console script
> `ansible-tower-mcp`) and an **A2A agent server** (console script
> `ansible-tower-agent`). The MCP server is a typed, deterministic tool surface;
> the agent server is a graph-routed Pydantic-AI agent that calls those tools
> over an `MCP_URL`.

## Run the MCP server

The transport is selected with `--transport` (or the `TRANSPORT` env var):

=== "stdio (default)"

    ```bash
    ansible-tower-mcp
    ```
    For IDE / desktop MCP clients that launch the server as a subprocess.

=== "streamable-http"

    ```bash
    ansible-tower-mcp --transport streamable-http --host 0.0.0.0 --port 8000
    ```
    A network server with a `/health` endpoint and `/mcp` route.

=== "sse"

    ```bash
    ansible-tower-mcp --transport sse --host 0.0.0.0 --port 8000
    ```

Health check (HTTP transports):

```bash
curl -s http://localhost:8000/health        # {"status":"OK"}
```

## Configuration (environment)

`ansible-tower-mcp` is configured entirely from the environment. The connection
to the Tower / AWX controller uses the following **required** set (provide a
token, or a username / password pair, or an OAuth client id / secret pair):

| Var | Default | Meaning |
|---|---|---|
| `ANSIBLE_BASE_URL` | _none_ | Tower / AWX controller base URL (e.g. `https://tower.example.com`) |
| `ANSIBLE_USERNAME` | _none_ | Controller user id |
| `ANSIBLE_PASSWORD` | _none_ | Controller password |
| `ANSIBLE_TOKEN` | _none_ | Pre-issued API token (bypasses username / password) |
| `ANSIBLE_CLIENT_ID` | _none_ | OAuth application client id |
| `ANSIBLE_CLIENT_SECRET` | _none_ | OAuth application client secret |
| `ANSIBLE_TOWER_TLS_PROFILE` | _(unset)_ | Optional runtime TLS profile selector; verification is mandatory |

Transport and server settings:

| Var | Default | Meaning |
|---|---|---|
| `HOST` | `0.0.0.0` | Bind address (HTTP transports) |
| `PORT` | `8000` | Bind port (HTTP transports) |
| `TRANSPORT` | `stdio` | `stdio`, `streamable-http`, or `sse` |
| `ENABLE_OTEL` | `True` | OpenTelemetry / Langfuse export |
| `EUNOMIA_TYPE` | `none` | Access-governance mode: `none`, `embedded`, `remote` |

Every per-resource tool can be toggled with its `*TOOL` switch (for example
`INVENTORYTOOL`, `JOBSTOOL`, `JOB_TEMPLATESTOOL`, `SYSTEMTOOL`). The full set,
with defaults, is documented in
[`.env.example`](https://github.com/Knuckles-Team/ansible-tower-mcp/blob/main/.env.example).
Copy it to `.env` and fill in only what you use.

### Backing Service

The Ansible Tower / AWX controller this connector targets is an external
**Ansible Automation Platform** — Red Hat Ansible Automation Platform is a
managed / commercial product, and the upstream AWX project is deployed through
the AWX Operator on Kubernetes. This package does not provision the controller;
only **connection configuration** (the `ANSIBLE_*` variables above) is required.
Point `ANSIBLE_BASE_URL` at an already-running controller and supply credentials.

## Docker Compose

The repo ships [`docker/mcp.compose.yml`](https://github.com/Knuckles-Team/ansible-tower-mcp/blob/main/docker/mcp.compose.yml).
It reads a sibling `.env` and publishes the HTTP server on `:8000`:

```yaml
services:
  ansible-tower-mcp-mcp:
    image: example/ansible-tower-mcp@sha256:<digest>
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
```

```bash
cp .env.example .env          # then set ANSIBLE_* values
docker compose -f docker/mcp.compose.yml up -d
docker compose -f docker/mcp.compose.yml logs -f
```

## Run the agent server

The companion **A2A agent server** is the `ansible-tower-agent` console script.
It is a graph-routed Pydantic-AI agent that connects to the MCP server over
`MCP_URL` and exposes an AG-UI web interface and an A2A endpoint on its own port
(default `9012`):

```bash
export MCP_URL=http://localhost:8000/mcp
export PROVIDER=openai
export MODEL_ID=gpt-4o
ansible-tower-agent --host 0.0.0.0 --port 9012
```

The repo ships [`docker/agent.compose.yml`](https://github.com/Knuckles-Team/ansible-tower-mcp/blob/main/docker/agent.compose.yml),
which runs the MCP server and the agent server together. The agent service wires
`MCP_URL` to the MCP container and publishes the agent on `:9012`:

```yaml
services:
  ansible-tower-mcp-agent:
    image: example/ansible-tower-mcp@sha256:<digest>
    container_name: ansible-tower-mcp-agent
    depends_on:
      - ansible-tower-mcp-mcp
    command: [ "ansible-tower-agent" ]
    environment:
      - HOST=0.0.0.0
      - PORT=9012
      - MCP_URL=http://ansible-tower-mcp-mcp:8000/mcp
      - PROVIDER=${PROVIDER:-openai}
      - MODEL_ID=${MODEL_ID:-gpt-4o}
      - ENABLE_WEB_UI=True
    ports:
      - "9012:9012"
```

```bash
docker compose -f docker/agent.compose.yml up -d
```

## Behind a Caddy reverse proxy

Expose the HTTP server on a hostname with automatic TLS. Add to your `Caddyfile`:

```caddy
# Internal (self-signed) — homelab .example.invalid zone
ansible-tower-mcp.example.invalid {
    tls internal
    reverse_proxy ansible-tower-mcp-mcp:8000
}
```

```caddy
# Public — automatic Let's Encrypt
ansible-tower-mcp.example.com {
    reverse_proxy ansible-tower-mcp-mcp:8000
}
```

Reload Caddy:

```bash
docker compose -f services/caddy/compose.yml exec caddy caddy reload --config /etc/caddy/Caddyfile
```

## DNS with Technitium

Point the hostname at the host running Caddy. Via the Technitium API:

```bash
curl -s "http://technitium.example.invalid:5380/api/zones/records/add" \
  --data-urlencode "token=$TECHNITIUM_DNS_TOKEN" \
  --data-urlencode "domain=ansible-tower-mcp.example.invalid" \
  --data-urlencode "zone=arpa" \
  --data-urlencode "type=A" \
  --data-urlencode "ipAddress=192.0.2.10" \
  --data-urlencode "ttl=3600"
```

…or add an **A record** `ansible-tower-mcp.example.invalid → <caddy-host-ip>` in the
Technitium web console (`http://technitium.example.invalid:5380`). The ecosystem
[`technitium-dns-mcp`](https://knuckles-team.github.io/technitium-dns-mcp/)
automates this as a tool.

## Register with an MCP client

Add to your client's `mcp_config.json`:

```json
{
  "mcpServers": {
    "ansible-tower-mcp": {
      "command": "uv",
      "args": ["run", "ansible-tower-mcp"],
      "env": {
        "ANSIBLE_BASE_URL": "https://your-tower.example.com",
        "ANSIBLE_USERNAME": "admin",
        "ANSIBLE_PASSWORD": "secret",
        "ANSIBLE_TOWER_TLS_PROFILE": "private-pki"
      }
    }
  }
}
```

For a remote HTTP server, point the client at
`http://ansible-tower-mcp.example.invalid/mcp` instead.
