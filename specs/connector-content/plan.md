# CONN-ANSIBLE-TOWER-MCP-CONNECTOR-CONTENT — Design and implementation plan

Governing spec: [spec.md](spec.md).

## Architecture

`pyproject.toml` declares `ansible-tower-mcp` as the connector identity. `create_mcp_server` resolves the packaged content of `ansible_tower_mcp` from it.
