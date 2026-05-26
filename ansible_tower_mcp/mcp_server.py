# Thin delegation wrapper for backward compatibility with external scripts, pyproject.toml scripts, and eager imports.
__version__ = "1.16.0"

from ansible_tower_mcp.mcp.mcp_server import (
    get_mcp_instance,
    mcp_server,
    register_ad_hoc_commands_tools,
    register_credentials_tools,
    register_groups_tools,
    register_hosts_tools,
    register_inventory_tools,
    register_job_templates_tools,
    register_jobs_tools,
    register_organizations_tools,
    register_projects_tools,
    register_schedules_tools,
    register_system_tools,
    register_teams_tools,
    register_users_tools,
    register_workflow_jobs_tools,
    register_workflow_templates_tools,
)

__all__ = [
    "__version__",
    "get_mcp_instance",
    "mcp_server",
    "register_inventory_tools",
    "register_hosts_tools",
    "register_groups_tools",
    "register_job_templates_tools",
    "register_jobs_tools",
    "register_projects_tools",
    "register_credentials_tools",
    "register_organizations_tools",
    "register_teams_tools",
    "register_users_tools",
    "register_ad_hoc_commands_tools",
    "register_workflow_templates_tools",
    "register_workflow_jobs_tools",
    "register_schedules_tools",
    "register_system_tools",
]

if __name__ == "__main__":
    mcp_server()
