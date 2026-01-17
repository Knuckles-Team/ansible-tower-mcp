---
name: ansible-tower-mcp-jobs
description: Ansible Tower Mcp Jobs capabilities for A2A Agent.
---
### Overview
This skill provides access to jobs operations.

### Capabilities
- **list_jobs**: Retrieves a paginated list of jobs from Ansible Tower, optionally filtered by status. Returns a list of dictionaries, each with job details like id, status, and elapsed time. Display in a markdown table.
- **get_job**: Fetches details of a specific job by ID from Ansible Tower. Returns a dictionary with job information such as status, start time, and artifacts.
- **cancel_job**: Cancels a running job in Ansible Tower. Returns a dictionary confirming the cancellation status.
- **get_job_events**: Retrieves a paginated list of events for a specific job from Ansible Tower. Returns a list of dictionaries, each with event details like type, host, and stdout. Display in a markdown table.
- **get_job_stdout**: Fetches the stdout output of a job in the specified format from Ansible Tower. Returns a dictionary with the output content.

### Common Tools
- `list_jobs`: Retrieves a paginated list of jobs from Ansible Tower, optionally filtered by status. Returns a list of dictionaries, each with job details like id, status, and elapsed time. Display in a markdown table.
- `get_job`: Fetches details of a specific job by ID from Ansible Tower. Returns a dictionary with job information such as status, start time, and artifacts.
- `cancel_job`: Cancels a running job in Ansible Tower. Returns a dictionary confirming the cancellation status.
- `get_job_events`: Retrieves a paginated list of events for a specific job from Ansible Tower. Returns a list of dictionaries, each with event details like type, host, and stdout. Display in a markdown table.
- `get_job_stdout`: Fetches the stdout output of a job in the specified format from Ansible Tower. Returns a dictionary with the output content.

### Usage Rules
- Use these tools when the user requests actions related to **jobs**.
- Always interpret the output of these tools to provide a concise summary to the user.

### Example Prompts
- "Please get job stdout"
- "Please list jobs"
- "Please get job events"
- "Please cancel job"
- "Please get job"
