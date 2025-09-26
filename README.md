# Ansible Tower MCP Server

![PyPI - Version](https://img.shields.io/pypi/v/ansible-tower-mcp)
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

*Version: 1.2.1*

The **Ansible Tower MCP Server** provides a Model Context Protocol (MCP) interface to interact with the Ansible Tower (AWX) API, enabling automation and management of Ansible Tower resources such as inventories, hosts, groups, job templates, projects, credentials, organizations, teams, users, ad hoc commands, workflow templates, workflow jobs, schedules, and system information. This server is designed to integrate seamlessly with AI-driven workflows and can be deployed as a standalone service or used programmatically.

This repository is actively maintained - This is a fork of a37ai/ansible-tower-mcp, which had not been updated in 6 months.

Contributions are welcome!

## Features

- **Comprehensive API Coverage**: Manage Ansible Tower resources including inventories, hosts, groups, job templates, projects, credentials, organizations, teams, users, ad hoc commands, workflows, and schedules.
- **MCP Integration**: Exposes Ansible Tower API functionalities as MCP tools for use with AI agents or direct API calls.
- **Flexible Authentication**: Supports both username/password and token-based authentication.
- **Environment Variable Support**: Securely configure credentials and settings via environment variables.
- **Docker Support**: Easily deployable as a Docker container for scalable environments.
- **Extensive Documentation**: Clear examples and instructions for setup, usage, and testing.

## Prerequisites

- Python 3.8 or higher
- Ansible Tower (AWX) instance with API access
- `fastmcp` and `requests` Python packages
- Docker (optional, for containerized deployment)
- Node.js and `npx` (optional, for MCP validation)

<details>
  <summary><b>Usage:</b></summary>

### Using as an MCP Server

The Ansible Tower MCP Server can be run in two modes: `stdio` (for local testing) or `http` (for networked access). To start the server, use the following commands:

#### Run in stdio mode (default):
```bash
python -m ansible_tower_mcp
```

#### Run in HTTP mode:
```bash
python -m ansible_tower_mcp --transport http --host 0.0.0.0 --port 8012
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
from ansible_tower_api import Api

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

### Use with AI

To integrate with AI-driven workflows, configure the MCP server in `mcp.json`. This allows AI agents to interact with Ansible Tower via the MCP protocol.

#### Configure `mcp.json`

Recommended: Use environment variables for sensitive information.

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

### Use with Docker

Deploy the MCP server as a Docker container for scalable and isolated environments.

#### Pull the Docker image
```bash
docker pull knucklessg1/ansible-tower-mcp:latest
```

#### Create a `compose.yml` file
```yaml
services:
  ansible-tower-mcp:
    image: knucklessg1/ansible-tower-mcp:latest
    environment:
      - ANSIBLE_BASE_URL=https://your-ansible-tower-instance.com
      - ANSIBLE_USERNAME=your-username
      - ANSIBLE_PASSWORD=your-password
      - ANSIBLE_TOKEN=your-api-token
      - VERIFY=False
      - HOST=0.0.0.0
      - PORT=8012
    ports:
      - 8012:8012
```

#### Run the Docker container
```bash
docker-compose up -d
```

</details>

<details>
  <summary><b>Installation Instructions:</b></summary>

### Install Python Package

Install the `ansible-tower-mcp` package using pip:

```bash
python -m pip install ansible-tower-mcp
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

</details>

<details>
  <summary><b>Tests:</b></summary>

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

</details>

<details>
  <summary><b>Available MCP Tools:</b></summary>

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

</details>

<details>
  <summary><b>Repository Owners:</b></summary>

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)

</details>

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
