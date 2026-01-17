---
name: ansible-tower-mcp-job-templates
description: Ansible Tower Mcp Job Templates capabilities for A2A Agent.
---
### Overview
This skill provides access to job_templates operations.

### Capabilities
- **list_job_templates**: Retrieves a paginated list of job templates from Ansible Tower. Returns a list of dictionaries, each with template details like id, name, and playbook. Display in a markdown table.
- **get_job_template**: Fetches details of a specific job template by ID from Ansible Tower. Returns a dictionary with template information such as name, inventory, and extra_vars.
- **create_job_template**: Creates a new job template in Ansible Tower. Returns a dictionary with the created template's details, including its ID.
- **update_job_template**: Updates an existing job template in Ansible Tower. Returns a dictionary with the updated template's details.
- **delete_job_template**: Deletes a specific job template by ID from Ansible Tower. Returns a dictionary confirming the deletion status.
- **launch_job**: Launches a job from a template in Ansible Tower, optionally with extra variables. Returns a dictionary with the launched job's details, including its ID.

### Common Tools
- `list_job_templates`: Retrieves a paginated list of job templates from Ansible Tower. Returns a list of dictionaries, each with template details like id, name, and playbook. Display in a markdown table.
- `get_job_template`: Fetches details of a specific job template by ID from Ansible Tower. Returns a dictionary with template information such as name, inventory, and extra_vars.
- `create_job_template`: Creates a new job template in Ansible Tower. Returns a dictionary with the created template's details, including its ID.
- `update_job_template`: Updates an existing job template in Ansible Tower. Returns a dictionary with the updated template's details.
- `delete_job_template`: Deletes a specific job template by ID from Ansible Tower. Returns a dictionary confirming the deletion status.
- `launch_job`: Launches a job from a template in Ansible Tower, optionally with extra variables. Returns a dictionary with the launched job's details, including its ID.

### Usage Rules
- Use these tools when the user requests actions related to **job_templates**.
- Always interpret the output of these tools to provide a concise summary to the user.

### Example Prompts
- "Please update job template"
- "Please launch job"
- "Please delete job template"
- "Please list job templates"
- "Please get job template"
