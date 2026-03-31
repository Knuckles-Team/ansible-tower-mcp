"""Ansible Tower graph configuration — tag prompts and env var mappings.

This is the only file needed to enable graph mode for this agent.
Provides TAG_PROMPTS and TAG_ENV_VARS for create_graph_agent_server().
"""

                                                                       
TAG_PROMPTS: dict[str, str] = {
    "ad_hoc_commands": (
        "You are a Ansible Tower Ad Hoc Commands specialist. Help users manage and interact with Ad Hoc Commands functionality using the available tools."
    ),
    "credentials": (
        "You are a Ansible Tower Credentials specialist. Help users manage and interact with Credentials functionality using the available tools."
    ),
    "groups": (
        "You are a Ansible Tower Groups specialist. Help users manage and interact with Groups functionality using the available tools."
    ),
    "hosts": (
        "You are a Ansible Tower Hosts specialist. Help users manage and interact with Hosts functionality using the available tools."
    ),
    "inventory": (
        "You are a Ansible Tower Inventory specialist. Help users manage and interact with Inventory functionality using the available tools."
    ),
    "job-templates": (
        "You are a Ansible Tower Job Templates specialist. Help users manage and interact with Job Templates functionality using the available tools."
    ),
    "jobs": (
        "You are a Ansible Tower Jobs specialist. Help users manage and interact with Jobs functionality using the available tools."
    ),
    "organizations": (
        "You are a Ansible Tower Organizations specialist. Help users manage and interact with Organizations functionality using the available tools."
    ),
    "projects": (
        "You are a Ansible Tower Projects specialist. Help users manage and interact with Projects functionality using the available tools."
    ),
    "schedules": (
        "You are a Ansible Tower Schedules specialist. Help users manage and interact with Schedules functionality using the available tools."
    ),
    "system": (
        "You are a Ansible Tower System specialist. Help users manage and interact with System functionality using the available tools."
    ),
    "teams": (
        "You are a Ansible Tower Teams specialist. Help users manage and interact with Teams functionality using the available tools."
    ),
    "users": (
        "You are a Ansible Tower Users specialist. Help users manage and interact with Users functionality using the available tools."
    ),
    "workflow_jobs": (
        "You are a Ansible Tower Workflow Jobs specialist. Help users manage and interact with Workflow Jobs functionality using the available tools."
    ),
    "workflow_templates": (
        "You are a Ansible Tower Workflow Templates specialist. Help users manage and interact with Workflow Templates functionality using the available tools."
    ),
}


                                                                        
TAG_ENV_VARS: dict[str, str] = {
    "ad_hoc_commands": "AD_HOC_COMMANDSTOOL",
    "credentials": "CREDENTIALSTOOL",
    "groups": "GROUPSTOOL",
    "hosts": "HOSTSTOOL",
    "inventory": "INVENTORYTOOL",
    "job-templates": "JOB_TEMPLATESTOOL",
    "jobs": "JOBSTOOL",
    "organizations": "ORGANIZATIONSTOOL",
    "projects": "PROJECTSTOOL",
    "schedules": "SCHEDULESTOOL",
    "system": "SYSTEMTOOL",
    "teams": "TEAMSTOOL",
    "users": "USERSTOOL",
    "workflow_jobs": "WORKFLOW_JOBSTOOL",
    "workflow_templates": "WORKFLOW_TEMPLATESTOOL",
}
