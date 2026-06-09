# Installation

`ansible-tower-mcp` is a standard Python package and a prebuilt container image.
Pick the path that matches how you want to run it.

## Requirements

- **Python 3.11 – 3.14**.
- A reachable **Ansible Tower / AWX controller** (Ansible Automation Platform)
  with API access — see the [Backing Service](deployment.md#backing-service) note
  for connection guidance.

## From PyPI (recommended)

```bash
pip install ansible-tower-mcp
```

### Optional extras

The base install is intentionally minimal. Install the extra for what you need:

| Extra | Install | Pulls in |
|---|---|---|
| `mcp` | `pip install "ansible-tower-mcp[mcp]"` | FastMCP MCP-server runtime (`agent-utilities[mcp]`) |
| `agent` | `pip install "ansible-tower-mcp[agent]"` | Pydantic-AI agent server + Logfire tracing |
| `all` | `pip install "ansible-tower-mcp[all]"` | Everything above (MCP + agent + Logfire) |
| `test` | `pip install "ansible-tower-mcp[test]"` | `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-xdist` |

```bash
# Typical: run the MCP server and the A2A agent server
pip install "ansible-tower-mcp[all]"
```

## From source

```bash
git clone https://github.com/Knuckles-Team/ansible-tower-mcp.git
cd ansible-tower-mcp
pip install -e ".[all]"          # editable install with every extra
```

With [`uv`](https://docs.astral.sh/uv/):

```bash
uv pip install -e ".[all]"
uv run ansible-tower-mcp
```

## Prebuilt Docker image

A multi-stage, slim image is published on every release (entrypoint
`ansible-tower-mcp`):

```bash
docker pull knucklessg1/ansible-tower-mcp:latest

docker run --rm -i \
  -e ANSIBLE_BASE_URL=https://your-tower.example.com \
  -e ANSIBLE_USERNAME=admin \
  -e ANSIBLE_PASSWORD=secret \
  knucklessg1/ansible-tower-mcp:latest        # stdio transport (default)
```

For an HTTP server with a published port and the agent server, see
[Deployment](deployment.md).

## Verify the install

```bash
ansible-tower-mcp --help
python -c "import ansible_tower_mcp; print(ansible_tower_mcp.__version__)"
```

## Next steps

- **[Deployment](deployment.md)** — run it as a long-lived MCP / agent server behind Caddy + DNS.
- **[Usage](usage.md)** — call the tools, the `Api` client, and the CLI.
- **[Configuration](deployment.md#configuration-environment)** — every environment variable.
