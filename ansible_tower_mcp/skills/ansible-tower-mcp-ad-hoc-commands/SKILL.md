---
name: ansible-tower-mcp-ad-hoc-commands
description: Ansible Tower Mcp Ad Hoc Commands capabilities for A2A Agent.
---
### Overview
This skill provides access to ad_hoc_commands operations.

### Capabilities
- **run_ad_hoc_command**: Runs an ad hoc command on hosts in Ansible Tower. Returns a dictionary with the command job's details, including its ID.
- **get_ad_hoc_command**: Fetches details of a specific ad hoc command by ID from Ansible Tower. Returns a dictionary with command information such as status and module_args.
- **cancel_ad_hoc_command**: Cancels a running ad hoc command in Ansible Tower. Returns a dictionary confirming the cancellation status.

### Common Tools
- `run_ad_hoc_command`: Runs an ad hoc command on hosts in Ansible Tower. Returns a dictionary with the command job's details, including its ID.
- `get_ad_hoc_command`: Fetches details of a specific ad hoc command by ID from Ansible Tower. Returns a dictionary with command information such as status and module_args.
- `cancel_ad_hoc_command`: Cancels a running ad hoc command in Ansible Tower. Returns a dictionary confirming the cancellation status.

### Usage Rules
- Use these tools when the user requests actions related to **ad_hoc_commands**.
- Always interpret the output of these tools to provide a concise summary to the user.

### Example Prompts
- "Please run ad hoc command"
- "Please get ad hoc command"
- "Please cancel ad hoc command"
