---
name: ansible-tower-mcp-system
description: Ansible Tower Mcp System capabilities for A2A Agent.
---
### Overview
This skill provides access to system operations.

### Capabilities
- **get_ansible_version**: Retrieves the Ansible version information from Ansible Tower. Returns a dictionary with version details.
- **get_dashboard_stats**: Fetches dashboard statistics from Ansible Tower. Returns a dictionary with stats like host counts and recent jobs.
- **get_metrics**: Retrieves system metrics from Ansible Tower. Returns a dictionary with performance and usage metrics.

### Common Tools
- `get_ansible_version`: Retrieves the Ansible version information from Ansible Tower. Returns a dictionary with version details.
- `get_dashboard_stats`: Fetches dashboard statistics from Ansible Tower. Returns a dictionary with stats like host counts and recent jobs.
- `get_metrics`: Retrieves system metrics from Ansible Tower. Returns a dictionary with performance and usage metrics.

### Usage Rules
- Use these tools when the user requests actions related to **system**.
- Always interpret the output of these tools to provide a concise summary to the user.

### Example Prompts
- "Please get ansible version"
- "Please get metrics"
- "Please get dashboard stats"
