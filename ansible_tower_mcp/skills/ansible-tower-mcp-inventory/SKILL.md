---
name: ansible-tower-mcp-inventory
description: Ansible Tower Mcp Inventory capabilities for A2A Agent.
---
### Overview
This skill provides access to inventory operations.

### Capabilities
- **list_inventories**: Retrieves a paginated list of inventories from Ansible Tower. Returns a list of dictionaries, each containing inventory details like id, name, and description. Display results in a markdown table for clarity.
- **get_inventory**: Fetches details of a specific inventory by ID from Ansible Tower. Returns a dictionary with inventory information such as name, description, and hosts count.
- **create_inventory**: Creates a new inventory in Ansible Tower. Returns a dictionary with the created inventory's details, including its ID.
- **update_inventory**: Updates an existing inventory in Ansible Tower. Returns a dictionary with the updated inventory's details.
- **delete_inventory**: Deletes a specific inventory by ID from Ansible Tower. Returns a dictionary confirming the deletion status.

### Common Tools
- `list_inventories`: Retrieves a paginated list of inventories from Ansible Tower. Returns a list of dictionaries, each containing inventory details like id, name, and description. Display results in a markdown table for clarity.
- `get_inventory`: Fetches details of a specific inventory by ID from Ansible Tower. Returns a dictionary with inventory information such as name, description, and hosts count.
- `create_inventory`: Creates a new inventory in Ansible Tower. Returns a dictionary with the created inventory's details, including its ID.
- `update_inventory`: Updates an existing inventory in Ansible Tower. Returns a dictionary with the updated inventory's details.
- `delete_inventory`: Deletes a specific inventory by ID from Ansible Tower. Returns a dictionary confirming the deletion status.

### Usage Rules
- Use these tools when the user requests actions related to **inventory**.
- Always interpret the output of these tools to provide a concise summary to the user.

### Example Prompts
- "Please get inventory"
- "Please delete inventory"
- "Please list inventories"
- "Please update inventory"
- "Please create inventory"
