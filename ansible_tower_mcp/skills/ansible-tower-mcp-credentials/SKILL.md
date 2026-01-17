---
name: ansible-tower-mcp-credentials
description: Ansible Tower Mcp Credentials capabilities for A2A Agent.
---
### Overview
This skill provides access to credentials operations.

### Capabilities
- **list_credentials**: Retrieves a paginated list of credentials from Ansible Tower. Returns a list of dictionaries, each with credential details like id, name, and type. Display in a markdown table.
- **get_credential**: Fetches details of a specific credential by ID from Ansible Tower. Returns a dictionary with credential information such as name and inputs (masked).
- **list_credential_types**: Retrieves a paginated list of credential types from Ansible Tower. Returns a list of dictionaries, each with type details like id and name. Display in a markdown table.
- **create_credential**: Creates a new credential in Ansible Tower. Returns a dictionary with the created credential's details, including its ID.
- **update_credential**: Updates an existing credential in Ansible Tower. Returns a dictionary with the updated credential's details.
- **delete_credential**: Deletes a specific credential by ID from Ansible Tower. Returns a dictionary confirming the deletion status.

### Common Tools
- `list_credentials`: Retrieves a paginated list of credentials from Ansible Tower. Returns a list of dictionaries, each with credential details like id, name, and type. Display in a markdown table.
- `get_credential`: Fetches details of a specific credential by ID from Ansible Tower. Returns a dictionary with credential information such as name and inputs (masked).
- `list_credential_types`: Retrieves a paginated list of credential types from Ansible Tower. Returns a list of dictionaries, each with type details like id and name. Display in a markdown table.
- `create_credential`: Creates a new credential in Ansible Tower. Returns a dictionary with the created credential's details, including its ID.
- `update_credential`: Updates an existing credential in Ansible Tower. Returns a dictionary with the updated credential's details.
- `delete_credential`: Deletes a specific credential by ID from Ansible Tower. Returns a dictionary confirming the deletion status.

### Usage Rules
- Use these tools when the user requests actions related to **credentials**.
- Always interpret the output of these tools to provide a concise summary to the user.

### Example Prompts
- "Please create credential"
- "Please delete credential"
- "Please list credentials"
- "Please update credential"
- "Please get credential"
