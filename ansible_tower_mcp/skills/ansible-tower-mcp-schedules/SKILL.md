---
name: ansible-tower-mcp-schedules
description: Ansible Tower Mcp Schedules capabilities for A2A Agent.
---
### Overview
This skill provides access to schedules operations.

### Capabilities
- **list_schedules**: Retrieves a paginated list of schedules from Ansible Tower, optionally filtered by template. Returns a list of dictionaries, each with schedule details like id, name, and rrule. Display in a markdown table.
- **get_schedule**: Fetches details of a specific schedule by ID from Ansible Tower. Returns a dictionary with schedule information such as name and rrule.
- **create_schedule**: Creates a new schedule for a template in Ansible Tower. Returns a dictionary with the created schedule's details, including its ID.
- **update_schedule**: Updates an existing schedule in Ansible Tower. Returns a dictionary with the updated schedule's details.
- **delete_schedule**: Deletes a specific schedule by ID from Ansible Tower. Returns a dictionary confirming the deletion status.

### Common Tools
- `list_schedules`: Retrieves a paginated list of schedules from Ansible Tower, optionally filtered by template. Returns a list of dictionaries, each with schedule details like id, name, and rrule. Display in a markdown table.
- `get_schedule`: Fetches details of a specific schedule by ID from Ansible Tower. Returns a dictionary with schedule information such as name and rrule.
- `create_schedule`: Creates a new schedule for a template in Ansible Tower. Returns a dictionary with the created schedule's details, including its ID.
- `update_schedule`: Updates an existing schedule in Ansible Tower. Returns a dictionary with the updated schedule's details.
- `delete_schedule`: Deletes a specific schedule by ID from Ansible Tower. Returns a dictionary confirming the deletion status.

### Usage Rules
- Use these tools when the user requests actions related to **schedules**.
- Always interpret the output of these tools to provide a concise summary to the user.

### Example Prompts
- "Please get schedule"
- "Please delete schedule"
- "Please list schedules"
- "Please update schedule"
- "Please create schedule"
