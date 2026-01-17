---
name: ansible-tower-mcp-hosts
description: Ansible Tower Mcp Hosts capabilities for A2A Agent.
---
### Overview
This skill provides access to hosts operations.

### Capabilities
- **list_hosts**: Retrieves a paginated list of hosts from Ansible Tower, optionally filtered by inventory. Returns a list of dictionaries, each with host details like id, name, and variables. Display in a markdown table.
- **get_host**: Fetches details of a specific host by ID from Ansible Tower. Returns a dictionary with host information such as name, variables, and inventory.
- **create_host**: Creates a new host in a specified inventory in Ansible Tower. Returns a dictionary with the created host's details, including its ID.
- **update_host**: Updates an existing host in Ansible Tower. Returns a dictionary with the updated host's details.
- **delete_host**: Deletes a specific host by ID from Ansible Tower. Returns a dictionary confirming the deletion status.

### Common Tools
- `list_hosts`: Retrieves a paginated list of hosts from Ansible Tower, optionally filtered by inventory. Returns a list of dictionaries, each with host details like id, name, and variables. Display in a markdown table.
- `get_host`: Fetches details of a specific host by ID from Ansible Tower. Returns a dictionary with host information such as name, variables, and inventory.
- `create_host`: Creates a new host in a specified inventory in Ansible Tower. Returns a dictionary with the created host's details, including its ID.
- `update_host`: Updates an existing host in Ansible Tower. Returns a dictionary with the updated host's details.
- `delete_host`: Deletes a specific host by ID from Ansible Tower. Returns a dictionary confirming the deletion status.

### Usage Rules
- Use these tools when the user requests actions related to **hosts**.
- Always interpret the output of these tools to provide a concise summary to the user.

### Example Prompts
- "Please create host"
- "Please get host"
- "Please delete host"
- "Please list hosts"
- "Please update host"
