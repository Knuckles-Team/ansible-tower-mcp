---
name: ansible-tower-mcp-organizations
description: Ansible Tower Mcp Organizations capabilities for A2A Agent.
---
### Overview
This skill provides access to organizations operations.

### Capabilities
- **list_organizations**: Retrieves a paginated list of organizations from Ansible Tower. Returns a list of dictionaries, each with organization details like id and name. Display in a markdown table.
- **get_organization**: Fetches details of a specific organization by ID from Ansible Tower. Returns a dictionary with organization information such as name and description.
- **create_organization**: Creates a new organization in Ansible Tower. Returns a dictionary with the created organization's details, including its ID.
- **update_organization**: Updates an existing organization in Ansible Tower. Returns a dictionary with the updated organization's details.
- **delete_organization**: Deletes a specific organization by ID from Ansible Tower. Returns a dictionary confirming the deletion status.

### Common Tools
- `list_organizations`: Retrieves a paginated list of organizations from Ansible Tower. Returns a list of dictionaries, each with organization details like id and name. Display in a markdown table.
- `get_organization`: Fetches details of a specific organization by ID from Ansible Tower. Returns a dictionary with organization information such as name and description.
- `create_organization`: Creates a new organization in Ansible Tower. Returns a dictionary with the created organization's details, including its ID.
- `update_organization`: Updates an existing organization in Ansible Tower. Returns a dictionary with the updated organization's details.
- `delete_organization`: Deletes a specific organization by ID from Ansible Tower. Returns a dictionary confirming the deletion status.

### Usage Rules
- Use these tools when the user requests actions related to **organizations**.
- Always interpret the output of these tools to provide a concise summary to the user.

### Example Prompts
- "Please list organizations"
- "Please get organization"
- "Please delete organization"
- "Please update organization"
- "Please create organization"
