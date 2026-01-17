---
name: ansible-tower-mcp-workflow-jobs
description: Ansible Tower Mcp Workflow Jobs capabilities for A2A Agent.
---
### Overview
This skill provides access to workflow_jobs operations.

### Capabilities
- **list_workflow_jobs**: Retrieves a paginated list of workflow jobs from Ansible Tower, optionally filtered by status. Returns a list of dictionaries, each with job details like id and status. Display in a markdown table.
- **get_workflow_job**: Fetches details of a specific workflow job by ID from Ansible Tower. Returns a dictionary with job information such as status and start time.
- **cancel_workflow_job**: Cancels a running workflow job in Ansible Tower. Returns a dictionary confirming the cancellation status.

### Common Tools
- `list_workflow_jobs`: Retrieves a paginated list of workflow jobs from Ansible Tower, optionally filtered by status. Returns a list of dictionaries, each with job details like id and status. Display in a markdown table.
- `get_workflow_job`: Fetches details of a specific workflow job by ID from Ansible Tower. Returns a dictionary with job information such as status and start time.
- `cancel_workflow_job`: Cancels a running workflow job in Ansible Tower. Returns a dictionary confirming the cancellation status.

### Usage Rules
- Use these tools when the user requests actions related to **workflow_jobs**.
- Always interpret the output of these tools to provide a concise summary to the user.

### Example Prompts
- "Please cancel workflow job"
- "Please list workflow jobs"
- "Please get workflow job"
