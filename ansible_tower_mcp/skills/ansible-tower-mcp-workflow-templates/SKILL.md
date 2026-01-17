---
name: ansible-tower-mcp-workflow-templates
description: Ansible Tower Mcp Workflow Templates capabilities for A2A Agent.
---
### Overview
This skill provides access to workflow_templates operations.

### Capabilities
- **list_workflow_templates**: Retrieves a paginated list of workflow templates from Ansible Tower. Returns a list of dictionaries, each with template details like id and name. Display in a markdown table.
- **get_workflow_template**: Fetches details of a specific workflow template by ID from Ansible Tower. Returns a dictionary with template information such as name and extra_vars.
- **launch_workflow**: Launches a workflow from a template in Ansible Tower, optionally with extra variables. Returns a dictionary with the launched workflow job's details, including its ID.

### Common Tools
- `list_workflow_templates`: Retrieves a paginated list of workflow templates from Ansible Tower. Returns a list of dictionaries, each with template details like id and name. Display in a markdown table.
- `get_workflow_template`: Fetches details of a specific workflow template by ID from Ansible Tower. Returns a dictionary with template information such as name and extra_vars.
- `launch_workflow`: Launches a workflow from a template in Ansible Tower, optionally with extra variables. Returns a dictionary with the launched workflow job's details, including its ID.

### Usage Rules
- Use these tools when the user requests actions related to **workflow_templates**.
- Always interpret the output of these tools to provide a concise summary to the user.

### Example Prompts
- "Please list workflow templates"
- "Please launch workflow"
- "Please get workflow template"
