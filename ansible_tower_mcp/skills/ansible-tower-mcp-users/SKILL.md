---
name: ansible-tower-mcp-users
description: Ansible Tower Mcp Users capabilities for A2A Agent.
---
### Overview
This skill provides access to users operations.

### Capabilities
- **list_users**: Retrieves a paginated list of users from Ansible Tower. Returns a list of dictionaries, each with user details like id, username, and email. Display in a markdown table.
- **get_user**: Fetches details of a specific user by ID from Ansible Tower. Returns a dictionary with user information such as username, email, and roles.
- **create_user**: Creates a new user in Ansible Tower. Returns a dictionary with the created user's details, including its ID.
- **update_user**: Updates an existing user in Ansible Tower. Returns a dictionary with the updated user's details.
- **delete_user**: Deletes a specific user by ID from Ansible Tower. Returns a dictionary confirming the deletion status.

### Common Tools
- `list_users`: Retrieves a paginated list of users from Ansible Tower. Returns a list of dictionaries, each with user details like id, username, and email. Display in a markdown table.
- `get_user`: Fetches details of a specific user by ID from Ansible Tower. Returns a dictionary with user information such as username, email, and roles.
- `create_user`: Creates a new user in Ansible Tower. Returns a dictionary with the created user's details, including its ID.
- `update_user`: Updates an existing user in Ansible Tower. Returns a dictionary with the updated user's details.
- `delete_user`: Deletes a specific user by ID from Ansible Tower. Returns a dictionary confirming the deletion status.

### Usage Rules
- Use these tools when the user requests actions related to **users**.
- Always interpret the output of these tools to provide a concise summary to the user.

### Example Prompts
- "Please list users"
- "Please delete user"
- "Please create user"
- "Please get user"
- "Please update user"
