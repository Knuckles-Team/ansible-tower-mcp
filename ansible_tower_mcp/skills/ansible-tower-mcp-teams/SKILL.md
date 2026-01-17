---
name: ansible-tower-mcp-teams
description: Ansible Tower Mcp Teams capabilities for A2A Agent.
---
### Overview
This skill provides access to teams operations.

### Capabilities
- **list_teams**: Retrieves a paginated list of teams from Ansible Tower, optionally filtered by organization. Returns a list of dictionaries, each with team details like id and name. Display in a markdown table.
- **get_team**: Fetches details of a specific team by ID from Ansible Tower. Returns a dictionary with team information such as name and organization.
- **create_team**: Creates a new team in a specified organization in Ansible Tower. Returns a dictionary with the created team's details, including its ID.
- **update_team**: Updates an existing team in Ansible Tower. Returns a dictionary with the updated team's details.
- **delete_team**: Deletes a specific team by ID from Ansible Tower. Returns a dictionary confirming the deletion status.

### Common Tools
- `list_teams`: Retrieves a paginated list of teams from Ansible Tower, optionally filtered by organization. Returns a list of dictionaries, each with team details like id and name. Display in a markdown table.
- `get_team`: Fetches details of a specific team by ID from Ansible Tower. Returns a dictionary with team information such as name and organization.
- `create_team`: Creates a new team in a specified organization in Ansible Tower. Returns a dictionary with the created team's details, including its ID.
- `update_team`: Updates an existing team in Ansible Tower. Returns a dictionary with the updated team's details.
- `delete_team`: Deletes a specific team by ID from Ansible Tower. Returns a dictionary confirming the deletion status.

### Usage Rules
- Use these tools when the user requests actions related to **teams**.
- Always interpret the output of these tools to provide a concise summary to the user.

### Example Prompts
- "Please update team"
- "Please create team"
- "Please delete team"
- "Please list teams"
- "Please get team"
