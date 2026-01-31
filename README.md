# Ansible Tower API - A2A | AG-UI | MCP

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

*Version: 1.2.25*

## Overview

The **Ansible Tower MCP Server** provides a Model Context Protocol (MCP) interface to interact with the Ansible Tower (AWX) API, enabling automation and management of Ansible Tower resources such as inventories, hosts, groups, job templates, projects, credentials, organizations, teams, users, ad hoc commands, workflow templates, workflow jobs, schedules, and system information. This server is designed to integrate seamlessly with AI-driven workflows and can be deployed as a standalone service or used programmatically.

This repository is actively maintained - This is a fork of a37ai/ansible-tower-mcp, which had not been updated in 6 months.

Contributions are welcome!

### Features

- **Comprehensive API Coverage**: Manage Ansible Tower resources including inventories, hosts, groups, job templates, projects, credentials, organizations, teams, users, ad hoc commands, workflows, and schedules.
- **MCP Integration**: Exposes Ansible Tower API functionalities as MCP tools for use with AI agents or direct API calls.
- **Flexible Authentication**: Supports both username/password and token-based authentication.
- **Environment Variable Support**: Securely configure credentials and settings via environment variables.
- **Docker Support**: Easily deployable as a Docker container for scalable environments.
- **Extensive Documentation**: Clear examples and instructions for setup, usage, and testing.

## MCP


### MCP Tools

The `ansible-tower-mcp` package exposes the following MCP tools, organized by category:

### Inventory Management
- `list_inventories(limit, offset)`: List all inventories.
- `get_inventory(inventory_id)`: Get details of a specific inventory.
- `create_inventory(name, organization_id, description)`: Create a new inventory.
- `update_inventory(inventory_id, name, description)`: Update an existing inventory.
- `delete_inventory(inventory_id)`: Delete an inventory.

### Host Management
- `list_hosts(inventory_id, limit, offset)`: List hosts, optionally filtered by inventory.
- `get_host(host_id)`: Get details of a specific host.
- `create_host(name, inventory_id, variables, description)`: Create a new host.
- `update_host(host_id, name, variables, description)`: Update an existing host.
- `delete_host(host_id)`: Delete a host.

### Group Management
- `list_groups(inventory_id, limit, offset)`: List groups in an inventory.
- `get_group(group_id)`: Get details of a specific group.
- `create_group(name, inventory_id, variables, description)`: Create a new group.
- `update_group(group_id, name, variables, description)`: Update an existing group.
- `delete_group(group_id)`: Delete a group.
- `add_host_to_group(group_id, host_id)`: Add a host to a group.
- `remove_host_from_group(group_id, host_id)`: Remove a host from a group.

### Job Template Management
- `list_job_templates(limit, offset)`: List all job templates.
- `get_job_template(template_id)`: Get details of a specific job template.
- `create_job_template(name, inventory_id, project_id, playbook, credential_id, description, extra_vars)`: Create a new job template.
- `update_job_template(template_id, name, inventory_id, playbook, description, extra_vars)`: Update an existing job template.
- `delete_job_template(template_id)`: Delete a job template.
- `launch_job(template_id, extra_vars)`: Launch a job from a template.

### Job Management
- `list_jobs(status, limit, offset)`: List jobs, optionally filtered by status.
- `get_job(job_id)`: Get details of a specific job.
- `cancel_job(job_id)`: Cancel a running job.
- `get_job_events(job_id, limit, offset)`: Get events for a job.
- `get_job_stdout(job_id, format)`: Get the output of a job in specified format (txt, html, json, ansi).

### Project Management
- `list_projects(limit, offset)`: List all projects.
- `get_project(project_id)`: Get details of a specific project.
- `create_project(name, organization_id, scm_type, scm_url, scm_branch, credential_id, description)`: Create a new project.
- `update_project(project_id, name, scm_type, scm_url, scm_branch, description)`: Update an existing project.
- `delete_project(project_id)`: Delete a project.
- `sync_project(project_id)`: Sync a project with its SCM.

### Credential Management
- `list_credentials(limit, offset)`: List all credentials.
- `get_credential(credential_id)`: Get details of a specific credential.
- `list_credential_types(limit, offset)`: List all credential types.
- `create_credential(name, credential_type_id, organization_id, inputs, description)`: Create a new credential.
- `update_credential(credential_id, name, inputs, description)`: Update an existing credential.
- `delete_credential(credential_id)`: Delete a credential.

### Organization Management
- `list_organizations(limit, offset)`: List all organizations.
- `get_organization(organization_id)`: Get details of a specific organization.
- `create_organization(name, description)`: Create a new organization.
- `update_organization(organization_id, name, description)`: Update an existing organization.
- `delete_organization(organization_id)`: Delete an organization.

### Team Management
- `list_teams(organization_id, limit, offset)`: List teams, optionally filtered by organization.
- `get_team(team_id)`: Get details of a specific team.
- `create_team(name, organization_id, description)`: Create a new team.
- `update_team(team_id, name, description)`: Update an existing team.
- `delete_team(team_id)`: Delete a team.

### User Management
- `list_users(limit, offset)`: List all users.
- `get_user(user_id)`: Get details of a specific user.
- `create_user(username, password, first_name, last_name, email, is_superuser, is_system_auditor)`: Create a new user.
- `update_user(user_id, username, password, first_name, last_name, email, is_superuser, is_system_auditor)`: Update an existing user.
- `delete_user(user_id)`: Delete a user.

### Ad Hoc Commands
- `run_ad_hoc_command(inventory_id, credential_id, module_name, module_args, limit, verbosity)`: Run an ad hoc command.
- `get_ad_hoc_command(command_id)`: Get details of an ad hoc command.
- `cancel_ad_hoc_command(command_id)`: Cancel an ad hoc command.

### Workflow Templates
- `list_workflow_templates(limit, offset)`: List all workflow templates.
- `get_workflow_template(template_id)`: Get details of a specific workflow template.
- `launch_workflow(template_id, extra_vars)`: Launch a workflow from a template.

### Workflow Jobs
- `list_workflow_jobs(status, limit, offset)`: List workflow jobs, optionally filtered by status.
- `get_workflow_job(job_id)`: Get details of a specific workflow job.
- `cancel_workflow_job(job_id)`: Cancel a running workflow job.

### Schedule Management
- `list_schedules(unified_job_template_id, limit, offset)`: List schedules, optionally filtered by job/workflow template.
- `get_schedule(schedule_id)`: Get details of a specific schedule.
- `create_schedule(name, unified_job_template_id, rrule, description, extra_data)`: Create a new schedule.
- `update_schedule(schedule_id, name, rrule, description, extra_data)`: Update an existing schedule.
- `delete_schedule(schedule_id)`: Delete a schedule.

### System Information
- `get_ansible_version()`: Get the Ansible Tower version.
- `get_dashboard_stats()`: Get dashboard statistics.
- `get_metrics()`: Get system metrics.


## A2A Agent

### Architecture:

```mermaid
---
config:
  layout: dagre
---
flowchart TB
 subgraph subGraph0["Agent Capabilities"]
        C["Agent"]
        B["A2A Server - Uvicorn/FastAPI"]
        D["MCP Tools"]
        F["Agent Skills"]
  end
    C --> D & F
    A["User Query"] --> B
    B --> C
    D --> E["Platform API"]

     C:::agent
     B:::server
     A:::server
    classDef server fill:#f9f,stroke:#333
    classDef agent fill:#bbf,stroke:#333,stroke-width:2px
    style B stroke:#000000,fill:#FFD600
    style D stroke:#000000,fill:#BBDEFB
    style F fill:#BBDEFB
    style A fill:#C8E6C9
    style subGraph0 fill:#FFF9C4
```

### Component Interaction Diagram

```mermaid
sequenceDiagram
    participant User
    participant Server as A2A Server
    participant Agent as Agent
    participant Skill as Agent Skills
    participant MCP as MCP Tools

    User->>Server: Send Query
    Server->>Agent: Invoke Agent
    Agent->>Skill: Analyze Skills Available
    Skill->>Agent: Provide Guidance on Next Steps
    Agent->>MCP: Invoke Tool
    MCP-->>Agent: Tool Response Returned
    Agent-->>Agent: Return Results Summarized
    Agent-->>Server: Final Response
    Server-->>User: Output
```

## Usage


### MCP CLI

| Short Flag | Long Flag                          | Description                                                                 |
|------------|------------------------------------|-----------------------------------------------------------------------------|
| -h         | --help                             | Display help information                                                    |
| -t         | --transport                        | Transport method: 'stdio', 'http', or 'sse' [legacy] (default: stdio)       |
| -s         | --host                             | Host address for HTTP transport (default: 0.0.0.0)                          |
| -p         | --port                             | Port number for HTTP transport (default: 8000)                              |
|            | --auth-type                        | Authentication type: 'none', 'static', 'jwt', 'oauth-proxy', 'oidc-proxy', 'remote-oauth' (default: none) |
|            | --oauth-upstream-client-id         | Upstream client ID for OAuth Proxy                                         |
|            | --oauth-upstream-client-secret     | Upstream client secret for OAuth Proxy                                     |
|            | --oauth-base-url                   | Base URL for OAuth Proxy                                                   |
|            | --oidc-config-url                  | OIDC configuration URL                                                     |
|            | --oidc-client-id                   | OIDC client ID                                                             |
|            | --oidc-client-secret               | OIDC client secret                                                         |
|            | --oidc-base-url                    | Base URL for OIDC Proxy                                                    |
|            | --remote-auth-servers              | Comma-separated list of authorization servers for Remote OAuth             |
|            | --remote-base-url                  | Base URL for Remote OAuth                                                  |
|            | --allowed-client-redirect-uris     | Comma-separated list of allowed client redirect URIs                       |
|            | --eunomia-type                     | Eunomia authorization type: 'none', 'embedded', 'remote' (default: none)   |
|            | --eunomia-policy-file              | Policy file for embedded Eunomia (default: mcp_policies.json)              |
|            | --eunomia-remote-url               | URL for remote Eunomia server                                              |


### A2A CLI
#### Endpoints
- **Web UI**: `http://localhost:8000/` (if enabled)
- **A2A**: `http://localhost:8000/a2a` (Discovery: `/a2a/.well-known/agent.json`)
- **AG-UI**: `http://localhost:8000/ag-ui` (POST)

| Long Flag        | Description                                      | Default                     |
|------------------|--------------------------------------------------|-----------------------------|
| --host           | Host to bind the server to                       | 0.0.0.0                     |
| --port           | Port to bind the server to                       | 9000                        |
| --reload         | Enable auto-reload                               | False                       |
| --provider       | LLM Provider (openai, anthropic, google, etc)    | openai                      |
| --model-id       | LLM Model ID                                     | qwen/qwen3-4b-2507               |
| --base-url       | LLM Base URL (for OpenAI compatible providers)   | http://host.docker.internal:1234/v1    |
| --api-key        | LLM API Key                                      | ollama                      |
| --mcp-url        | MCP Server URL to connect to                     | None                        |
| --mcp-config     | MCP Server Config                                | .../mcp_config.json         |
| --skills-directory| Directory containing agent skills               | ...                         |
| --web            | Enable Pydantic AI Web UI                        | False (Env: ENABLE_WEB_UI)  |

### Using as an MCP Server

The MCP Server can be run in two modes: `stdio` (for local testing) or `http` (for networked access). To start the server, use the following commands:

#### Run in stdio mode (default):
```bash
ansible-tower-mcp
```

#### Run in HTTP mode:
```bash
ansible-tower-mcp --transport http --host 0.0.0.0 --port 8012
```

Set environment variables for authentication:
```bash
export ANSIBLE_BASE_URL="https://your-ansible-tower-instance.com"
export ANSIBLE_USERNAME="your-username"
export ANSIBLE_PASSWORD="your-password"
# or
export ANSIBLE_TOKEN="your-api-token"
export VERIFY="False"  # Set to True to enable SSL verification
```

### Use API Directly

You can interact with the Ansible Tower API directly using the `Api` class from `ansible_tower_api.py`. Below is an example of creating an inventory and launching a job:

```python
from ansible_tower_mcp.ansible_tower_api import Api

# Initialize the API client
client = Api(
    base_url="https://your-ansible-tower-instance.com",
    username="your-username",
    password="your-password",
    verify=False
)

# Create an inventory
inventory = client.create_inventory(
    name="Test Inventory",
    organization_id=1,
    description="A test inventory"
)
print(inventory)

# Launch a job from a job template
job = client.launch_job(template_id=123, extra_vars='{"key": "value"}')
print(job)
```

### Deploy MCP Server as a Service

The ServiceNow MCP server can be deployed using Docker, with configurable authentication, middleware, and Eunomia authorization.

#### Using Docker Run

```bash
docker pull knucklessg1/ansible-tower-mcp:latest

docker run -d \
  --name ansible-tower-mcp \
  -p 8004:8004 \
  -e HOST=0.0.0.0 \
  -e PORT=8004 \
  -e TRANSPORT=http \
  -e AUTH_TYPE=none \
  -e EUNOMIA_TYPE=none \
  -e ANSIBLE_BASE_URL=https://your-ansible-tower-instance.com \
  -e ANSIBLE_USERNAME=your-username \
  -e ANSIBLE_PASSWORD=your-password \
  -e ANSIBLE_TOKEN=your-api-token \
  knucklessg1/ansible-tower-mcp:latest
```

For advanced authentication (e.g., JWT, OAuth Proxy, OIDC Proxy, Remote OAuth) or Eunomia, add the relevant environment variables:

```bash
docker run -d \
  --name ansible-tower-mcp \
  -p 8004:8004 \
  -e HOST=0.0.0.0 \
  -e PORT=8004 \
  -e TRANSPORT=http \
  -e AUTH_TYPE=oidc-proxy \
  -e OIDC_CONFIG_URL=https://provider.com/.well-known/openid-configuration \
  -e OIDC_CLIENT_ID=your-client-id \
  -e OIDC_CLIENT_SECRET=your-client-secret \
  -e OIDC_BASE_URL=https://your-server.com \
  -e ALLOWED_CLIENT_REDIRECT_URIS=http://localhost:*,https://*.example.com/* \
  -e EUNOMIA_TYPE=embedded \
  -e EUNOMIA_POLICY_FILE=/app/mcp_policies.json \
  -e ANSIBLE_BASE_URL=https://your-ansible-tower-instance.com \
  -e ANSIBLE_USERNAME=your-username \
  -e ANSIBLE_PASSWORD=your-password \
  -e ANSIBLE_TOKEN=your-api-token \
  knucklessg1/ansible-tower-mcp:latest
```

#### Using Docker Compose

Create a `docker-compose.yml` file:

```yaml
services:
  ansible-tower-mcp:
    image: knucklessg1/ansible-tower-mcp:latest
    environment:
      - HOST=0.0.0.0
      - PORT=8004
      - TRANSPORT=http
      - AUTH_TYPE=none
      - EUNOMIA_TYPE=none
      - ANSIBLE_BASE_URL=https://your-ansible-tower-instance.com
      - ANSIBLE_USERNAME=your-username
      - ANSIBLE_PASSWORD=your-password
      - ANSIBLE_TOKEN=your-api-token
      - ANSIBLE_VERIFY=False
    ports:
      - 8004:8004
```

For advanced setups with authentication and Eunomia:

```yaml
services:
  ansible-tower-mcp:
    image: knucklessg1/ansible-tower-mcp:latest
    environment:
      - HOST=0.0.0.0
      - PORT=8004
      - TRANSPORT=http
      - AUTH_TYPE=oidc-proxy
      - OIDC_CONFIG_URL=https://provider.com/.well-known/openid-configuration
      - OIDC_CLIENT_ID=your-client-id
      - OIDC_CLIENT_SECRET=your-client-secret
      - OIDC_BASE_URL=https://your-server.com
      - ALLOWED_CLIENT_REDIRECT_URIS=http://localhost:*,https://*.example.com/*
      - EUNOMIA_TYPE=embedded
      - EUNOMIA_POLICY_FILE=/app/mcp_policies.json
      - ANSIBLE_BASE_URL=https://your-ansible-tower-instance.com
      - ANSIBLE_USERNAME=your-username
      - ANSIBLE_PASSWORD=your-password
      - ANSIBLE_TOKEN=your-api-token
      - ANSIBLE_VERIFY=False
    ports:
      - 8004:8004
    volumes:
      - ./mcp_policies.json:/app/mcp_policies.json
```

Run the service:

```bash
docker-compose up -d
```

#### Configure `mcp.json` for AI Integration

```json
{
  "mcpServers": {
    "ansible-tower": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "ansible-tower-mcp>=0.0.4",
        "ansible-tower-mcp",
        "--transport",
        "stdio"
      ],
      "env": {
        "ANSIBLE_BASE_URL": "${ANSIBLE_BASE_URL}",
        "ANSIBLE_USERNAME": "${ANSIBLE_USERNAME}",
        "ANSIBLE_PASSWORD": "${ANSIBLE_PASSWORD}",
        "ANSIBLE_CLIENT_ID": "${ANSIBLE_CLIENT_ID}",
        "ANSIBLE_CLIENT_SECRET": "${ANSIBLE_CLIENT_SECRET}",
        "ANSIBLE_TOKEN": "${ANSIBLE_TOKEN}",
        "ANSIBLE_VERIFY": "${VERIFY:False}"
      },
      "timeout": 200000
    }
  }
}
```

Set environment variables:
```bash
export ANSIBLE_BASE_URL="https://your-ansible-tower-instance.com"
export ANSIBLE_USERNAME="your-username"
export ANSIBLE_PASSWORD="your-password"
export ANSIBLE_TOKEN="your-api-token"
export VERIFY="False"
```

For **testing only**, you can store credentials directly in `mcp.json` (not recommended for production):
```json
{
  "mcpServers": {
    "ansible-tower": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "ansible-tower-mcp",
        "ansible-tower-mcp",
        "--transport",
        "http",
        "--host",
        "0.0.0.0",
        "--port",
        "8012"
      ],
      "env": {
        "ANSIBLE_BASE_URL": "https://your-ansible-tower-instance.com",
        "ANSIBLE_USERNAME": "your-username",
        "ANSIBLE_PASSWORD": "your-password",
        "ANSIBLE_TOKEN": "your-api-token",
        "VERIFY": "False"
      },
      "timeout": 200000
    }
  }
}
```

## Install Python Package

Install the `ansible-tower-mcp` package using pip:

```bash
python -m pip install ansible-tower-mcp[all]
```

### Dependencies

Ensure the following Python packages are installed:
- `requests`
- `fastmcp`
- `pydantic`

Install dependencies manually if needed:
```bash
python -m pip install requests fastmcp pydantic
```

## Tests

### Pre-commit Checks

Run pre-commit checks to ensure code quality and formatting:
```bash
pre-commit run --all-files
```

To set up pre-commit hooks:
```bash
pre-commit install
```

### Validate MCP Server

Validate the MCP server configuration and tools using the MCP inspector:
```bash
npx @modelcontextprotocol/inspector ansible-tower-mcp
```

### Unit Tests

Run unit tests (if available in your project setup):
```bash
python -m pytest tests/
```

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)


## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please ensure your code passes pre-commit checks and includes relevant tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

For issues or feature requests, please open an issue on the [GitHub repository](https://github.com/Knuckles-Team/ansible-tower-mcp). For general inquiries, contact the maintainers via GitHub.
