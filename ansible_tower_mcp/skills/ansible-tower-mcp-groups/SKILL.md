---
name: ansible-tower-mcp-groups
description: Ansible Tower Mcp Groups capabilities for A2A Agent.
---
### Overview
This skill provides access to groups operations.

### Capabilities
- **list_groups**: Retrieves a paginated list of groups in a specified inventory from Ansible Tower. Returns a list of dictionaries, each with group details like id, name, and variables. Display in a markdown table.
- **get_group**: Fetches details of a specific group by ID from Ansible Tower. Returns a dictionary with group information such as name, variables, and inventory.
- **create_group**: Creates a new group in a specified inventory in Ansible Tower. Returns a dictionary with the created group's details, including its ID.
- **update_group**: Updates an existing group in Ansible Tower. Returns a dictionary with the updated group's details.
- **delete_group**: Deletes a specific group by ID from Ansible Tower. Returns a dictionary confirming the deletion status.
- **add_host_to_group**: Adds a host to a group in Ansible Tower. Returns a dictionary confirming the association.
- **remove_host_from_group**: Removes a host from a group in Ansible Tower. Returns a dictionary confirming the disassociation.

### Common Tools
- `list_groups`: Retrieves a paginated list of groups in a specified inventory from Ansible Tower. Returns a list of dictionaries, each with group details like id, name, and variables. Display in a markdown table.
- `get_group`: Fetches details of a specific group by ID from Ansible Tower. Returns a dictionary with group information such as name, variables, and inventory.
- `create_group`: Creates a new group in a specified inventory in Ansible Tower. Returns a dictionary with the created group's details, including its ID.
- `update_group`: Updates an existing group in Ansible Tower. Returns a dictionary with the updated group's details.
- `delete_group`: Deletes a specific group by ID from Ansible Tower. Returns a dictionary confirming the deletion status.
- `add_host_to_group`: Adds a host to a group in Ansible Tower. Returns a dictionary confirming the association.
- `remove_host_from_group`: Removes a host from a group in Ansible Tower. Returns a dictionary confirming the disassociation.

### Usage Rules
- Use these tools when the user requests actions related to **groups**.
- Always interpret the output of these tools to provide a concise summary to the user.

### Example Prompts
- "Please list groups"
- "Please remove host from group"
- "Please update group"
- "Please delete group"
- "Please get group"
