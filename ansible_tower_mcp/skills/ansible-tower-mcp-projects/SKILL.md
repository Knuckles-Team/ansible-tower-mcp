---
name: ansible-tower-mcp-projects
description: Ansible Tower Mcp Projects capabilities for A2A Agent.
---
### Overview
This skill provides access to projects operations.

### Capabilities
- **list_projects**: Retrieves a paginated list of projects from Ansible Tower. Returns a list of dictionaries, each with project details like id, name, and scm_type. Display in a markdown table.
- **get_project**: Fetches details of a specific project by ID from Ansible Tower. Returns a dictionary with project information such as name, scm_url, and status.
- **create_project**: Creates a new project in Ansible Tower. Returns a dictionary with the created project's details, including its ID.
- **update_project**: Updates an existing project in Ansible Tower. Returns a dictionary with the updated project's details.
- **delete_project**: Deletes a specific project by ID from Ansible Tower. Returns a dictionary confirming the deletion status.
- **sync_project**: Syncs (updates from SCM) a project in Ansible Tower. Returns a dictionary with the sync job's details.

### Common Tools
- `list_projects`: Retrieves a paginated list of projects from Ansible Tower. Returns a list of dictionaries, each with project details like id, name, and scm_type. Display in a markdown table.
- `get_project`: Fetches details of a specific project by ID from Ansible Tower. Returns a dictionary with project information such as name, scm_url, and status.
- `create_project`: Creates a new project in Ansible Tower. Returns a dictionary with the created project's details, including its ID.
- `update_project`: Updates an existing project in Ansible Tower. Returns a dictionary with the updated project's details.
- `delete_project`: Deletes a specific project by ID from Ansible Tower. Returns a dictionary confirming the deletion status.
- `sync_project`: Syncs (updates from SCM) a project in Ansible Tower. Returns a dictionary with the sync job's details.

### Usage Rules
- Use these tools when the user requests actions related to **projects**.
- Always interpret the output of these tools to provide a concise summary to the user.

### Example Prompts
- "Please delete project"
- "Please update project"
- "Please create project"
- "Please list projects"
- "Please get project"
