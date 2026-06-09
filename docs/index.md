# ansible-tower-mcp

Ansible Tower / AWX automation **API + MCP Server + A2A Agent** for the
agent-utilities ecosystem — a typed, deterministic control surface for Ansible
Automation Platform job templates, inventories, jobs, and credentials.

!!! info "Official documentation"
    This site is the canonical reference for `ansible-tower-mcp`, maintained
    alongside every release.

[![PyPI](https://img.shields.io/pypi/v/ansible-tower-mcp)](https://pypi.org/project/ansible-tower-mcp/)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
[![License](https://img.shields.io/pypi/l/ansible-tower-mcp)](https://github.com/Knuckles-Team/ansible-tower-mcp/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/source-GitHub-181717?logo=github)](https://github.com/Knuckles-Team/ansible-tower-mcp)

## Overview

`ansible-tower-mcp` wraps the Ansible Tower / AWX REST API (Ansible Automation
Platform) with typed, action-routed MCP tools and an optional Pydantic-AI agent
server. It provides:

- **`Api`** — a `requests`-based REST client for the Tower / AWX `/api/v2/`
  surface, organized by resource (inventories, hosts, groups, job templates,
  jobs, projects, credentials, organizations, teams, users, schedules, system).
- **Action-routed MCP tools** — one consolidated tool per resource domain,
  individually togglable through environment switches to keep the LLM tool
  surface compact.
- **An A2A agent server** — a graph-routed Pydantic-AI agent (console script
  `ansible-tower-agent`) that calls the MCP tools over an `MCP_URL`.

Authentication resolves automatically across OIDC token delegation, OAuth
client credentials, and username / password — and the server remains inactive
when credentials are absent.

## Explore the documentation

<div class="grid cards" markdown>

- :material-rocket-launch: **[Installation](installation.md)** — pip, source, extras, and the prebuilt Docker image.
- :material-server-network: **[Deployment](deployment.md)** — run the MCP and agent servers, Docker Compose, Caddy + Technitium.
- :material-console: **[Usage](usage.md)** — the MCP tools, the `Api` client, and the CLI.
- :material-sitemap: **[Overview](overview.md)** — ecosystem role, concept registry, and architecture.
- :material-tag-multiple: **[Concepts](concepts.md)** — the `CONCEPT:ANSIBLE-*` registry.

</div>

## Quick start

```bash
pip install "ansible-tower-mcp[mcp]"
ansible-tower-mcp                # stdio MCP server (default transport)
```

Connect it to an Ansible Tower / AWX controller:

```bash
export ANSIBLE_BASE_URL=https://your-tower.example.com
export ANSIBLE_USERNAME=admin
export ANSIBLE_PASSWORD=secret
ansible-tower-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

See **[Installation](installation.md)** and **[Deployment](deployment.md)** for
the full matrix (PyPI extras, Docker image, all transports, the agent server,
reverse proxy, DNS).
