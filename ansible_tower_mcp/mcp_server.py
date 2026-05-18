#!/usr/bin/python
import warnings

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

import logging
import os
import sys
from typing import Any

from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import create_mcp_server
from dotenv import find_dotenv, load_dotenv
from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field
from starlette.requests import Request
from starlette.responses import JSONResponse

from ansible_tower_mcp.auth import get_client

__version__ = "1.13.0"

logger = get_logger(name="ansible-tower-mcp")
logger.setLevel(logging.INFO)


def register_inventory_tools(mcp: FastMCP):
    @mcp.tool(tags={"inventory"})
    async def ansible_tower_inventory(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_inventories', 'get_inventory', 'create_inventory', 'update_inventory', 'delete_inventory'"
        ),
        page_size: int | None = Field(default=None, description="page size"),
        inventory_id: int | None = Field(default=None, description="inventory id"),
        name: Any | None = Field(default=None, description="name"),
        organization_id: int | None = Field(
            default=None, description="organization id"
        ),
        description: Any | None = Field(default=None, description="description"),
        client=Depends(get_client),
    ) -> dict:
        """Manage inventory operations.

        Actions:
          - 'list_inventories': Call list_inventories
          - 'get_inventory': Call get_inventory
          - 'create_inventory': Call create_inventory
          - 'update_inventory': Call update_inventory
          - 'delete_inventory': Call delete_inventory
        """
        kwargs: dict[str, Any]
        if action == "list_inventories":
            kwargs = {"page_size": page_size}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_inventories(**kwargs)
        if action == "get_inventory":
            kwargs = {"inventory_id": inventory_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_inventory(**kwargs)
        if action == "create_inventory":
            kwargs = {
                "name": name,
                "organization_id": organization_id,
                "description": description,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_inventory(**kwargs)
        if action == "update_inventory":
            kwargs = {
                "inventory_id": inventory_id,
                "name": name,
                "description": description,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_inventory(**kwargs)
        if action == "delete_inventory":
            kwargs = {"inventory_id": inventory_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_inventory(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_inventories', 'get_inventory', 'create_inventory', 'update_inventory', 'delete_inventory"
        )


def register_hosts_tools(mcp: FastMCP):
    @mcp.tool(tags={"hosts"})
    async def ansible_tower_hosts(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_hosts', 'get_host', 'create_host', 'update_host', 'delete_host'"
        ),
        inventory_id: Any | None = Field(default=None, description="inventory id"),
        page_size: int | None = Field(default=None, description="page size"),
        host_id: int | None = Field(default=None, description="host id"),
        name: Any | None = Field(default=None, description="name"),
        variables: Any | None = Field(default=None, description="variables"),
        description: Any | None = Field(default=None, description="description"),
        client=Depends(get_client),
    ) -> dict:
        """Manage hosts operations.

        Actions:
          - 'list_hosts': Call list_hosts
          - 'get_host': Call get_host
          - 'create_host': Call create_host
          - 'update_host': Call update_host
          - 'delete_host': Call delete_host
        """
        kwargs: dict[str, Any]
        if action == "list_hosts":
            kwargs = {"inventory_id": inventory_id, "page_size": page_size}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_hosts(**kwargs)
        if action == "get_host":
            kwargs = {"host_id": host_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_host(**kwargs)
        if action == "create_host":
            kwargs = {
                "name": name,
                "inventory_id": inventory_id,
                "variables": variables,
                "description": description,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_host(**kwargs)
        if action == "update_host":
            kwargs = {
                "host_id": host_id,
                "name": name,
                "variables": variables,
                "description": description,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_host(**kwargs)
        if action == "delete_host":
            kwargs = {"host_id": host_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_host(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_hosts', 'get_host', 'create_host', 'update_host', 'delete_host"
        )


def register_groups_tools(mcp: FastMCP):
    @mcp.tool(tags={"groups"})
    async def ansible_tower_groups(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_groups', 'get_group', 'create_group', 'update_group', 'delete_group', 'add_host_to_group', 'remove_host_from_group'"
        ),
        inventory_id: int | None = Field(default=None, description="inventory id"),
        page_size: int | None = Field(default=None, description="page size"),
        group_id: int | None = Field(default=None, description="group id"),
        name: Any | None = Field(default=None, description="name"),
        variables: Any | None = Field(default=None, description="variables"),
        description: Any | None = Field(default=None, description="description"),
        host_id: int | None = Field(default=None, description="host id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage groups operations.

        Actions:
          - 'list_groups': Call list_groups
          - 'get_group': Call get_group
          - 'create_group': Call create_group
          - 'update_group': Call update_group
          - 'delete_group': Call delete_group
          - 'add_host_to_group': Call add_host_to_group
          - 'remove_host_from_group': Call remove_host_from_group
        """
        kwargs: dict[str, Any]
        if action == "list_groups":
            kwargs = {"inventory_id": inventory_id, "page_size": page_size}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_groups(**kwargs)
        if action == "get_group":
            kwargs = {"group_id": group_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_group(**kwargs)
        if action == "create_group":
            kwargs = {
                "name": name,
                "inventory_id": inventory_id,
                "variables": variables,
                "description": description,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_group(**kwargs)
        if action == "update_group":
            kwargs = {
                "group_id": group_id,
                "name": name,
                "variables": variables,
                "description": description,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_group(**kwargs)
        if action == "delete_group":
            kwargs = {"group_id": group_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_group(**kwargs)
        if action == "add_host_to_group":
            kwargs = {"group_id": group_id, "host_id": host_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.add_host_to_group(**kwargs)
        if action == "remove_host_from_group":
            kwargs = {"group_id": group_id, "host_id": host_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.remove_host_from_group(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_groups', 'get_group', 'create_group', 'update_group', 'delete_group', 'add_host_to_group', 'remove_host_from_group"
        )


def register_job_templates_tools(mcp: FastMCP):
    @mcp.tool(tags={"job-templates"})
    async def ansible_tower_job_templates(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_job_templates', 'get_job_template', 'create_job_template', 'update_job_template', 'delete_job_template', 'launch_job'"
        ),
        page_size: int | None = Field(default=None, description="page size"),
        template_id: int | None = Field(default=None, description="template id"),
        name: Any | None = Field(default=None, description="name"),
        inventory_id: Any | None = Field(default=None, description="inventory id"),
        project_id: int | None = Field(default=None, description="project id"),
        playbook: Any | None = Field(default=None, description="playbook"),
        credential_id: int | None = Field(default=None, description="credential id"),
        description: Any | None = Field(default=None, description="description"),
        extra_vars: Any | None = Field(default=None, description="extra vars"),
        client=Depends(get_client),
    ) -> dict:
        """Manage job templates operations.

        Actions:
          - 'list_job_templates': Call list_job_templates
          - 'get_job_template': Call get_job_template
          - 'create_job_template': Call create_job_template
          - 'update_job_template': Call update_job_template
          - 'delete_job_template': Call delete_job_template
          - 'launch_job': Call launch_job
        """
        kwargs: dict[str, Any]
        if action == "list_job_templates":
            kwargs = {"page_size": page_size}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_job_templates(**kwargs)
        if action == "get_job_template":
            kwargs = {"template_id": template_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_job_template(**kwargs)
        if action == "create_job_template":
            kwargs = {
                "name": name,
                "inventory_id": inventory_id,
                "project_id": project_id,
                "playbook": playbook,
                "credential_id": credential_id,
                "description": description,
                "extra_vars": extra_vars,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_job_template(**kwargs)
        if action == "update_job_template":
            kwargs = {
                "template_id": template_id,
                "name": name,
                "inventory_id": inventory_id,
                "playbook": playbook,
                "description": description,
                "extra_vars": extra_vars,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_job_template(**kwargs)
        if action == "delete_job_template":
            kwargs = {"template_id": template_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_job_template(**kwargs)
        if action == "launch_job":
            kwargs = {"template_id": template_id, "extra_vars": extra_vars}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.launch_job(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_job_templates', 'get_job_template', 'create_job_template', 'update_job_template', 'delete_job_template', 'launch_job"
        )


def register_jobs_tools(mcp: FastMCP):
    @mcp.tool(tags={"jobs"})
    async def ansible_tower_jobs(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_jobs', 'get_job', 'cancel_job', 'relaunch_job', 'get_job_events', 'get_job_stdout'"
        ),
        status: str | None = Field(default=None, description="status"),
        page_size: int | None = Field(default=None, description="page size"),
        job_id: int | None = Field(default=None, description="job id"),
        format: str | None = Field(default=None, description="format"),
        client=Depends(get_client),
    ) -> dict:
        """Manage jobs operations.

        Actions:
          - 'list_jobs': Call list_jobs
          - 'get_job': Call get_job
          - 'cancel_job': Call cancel_job
          - 'relaunch_job': Call relaunch_job
          - 'get_job_events': Call get_job_events
          - 'get_job_stdout': Call get_job_stdout
        """
        kwargs: dict[str, Any]
        if action == "list_jobs":
            kwargs = {"status": status, "page_size": page_size}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_jobs(**kwargs)
        if action == "get_job":
            kwargs = {"job_id": job_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_job(**kwargs)
        if action == "cancel_job":
            kwargs = {"job_id": job_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.cancel_job(**kwargs)
        if action == "relaunch_job":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.relaunch_job(**kwargs)
        if action == "get_job_events":
            kwargs = {"job_id": job_id, "page_size": page_size}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_job_events(**kwargs)
        if action == "get_job_stdout":
            kwargs = {"job_id": job_id, "format": format}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_job_stdout(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_jobs', 'get_job', 'cancel_job', 'relaunch_job', 'get_job_events', 'get_job_stdout"
        )


def register_projects_tools(mcp: FastMCP):
    @mcp.tool(tags={"projects"})
    async def ansible_tower_projects(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_projects', 'get_project', 'create_project', 'update_project', 'delete_project', 'sync_project'"
        ),
        page_size: int | None = Field(default=None, description="page size"),
        project_id: int | None = Field(default=None, description="project id"),
        name: Any | None = Field(default=None, description="name"),
        organization_id: int | None = Field(
            default=None, description="organization id"
        ),
        scm_type: Any | None = Field(default=None, description="scm type"),
        scm_url: str | None = Field(default=None, description="scm url"),
        scm_branch: str | None = Field(default=None, description="scm branch"),
        credential_id: int | None = Field(default=None, description="credential id"),
        description: Any | None = Field(default=None, description="description"),
        client=Depends(get_client),
    ) -> dict:
        """Manage projects operations.

        Actions:
          - 'list_projects': Call list_projects
          - 'get_project': Call get_project
          - 'create_project': Call create_project
          - 'update_project': Call update_project
          - 'delete_project': Call delete_project
          - 'sync_project': Call sync_project
        """
        kwargs: dict[str, Any]
        if action == "list_projects":
            kwargs = {"page_size": page_size}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_projects(**kwargs)
        if action == "get_project":
            kwargs = {"project_id": project_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_project(**kwargs)
        if action == "create_project":
            kwargs = {
                "name": name,
                "organization_id": organization_id,
                "scm_type": scm_type,
                "scm_url": scm_url,  # type: ignore
                "scm_branch": scm_branch,  # type: ignore
                "credential_id": credential_id,
                "description": description,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_project(**kwargs)
        if action == "update_project":
            kwargs = {
                "project_id": project_id,
                "name": name,
                "scm_type": scm_type,
                "scm_url": scm_url,  # type: ignore
                "scm_branch": scm_branch,  # type: ignore
                "description": description,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_project(**kwargs)
        if action == "delete_project":
            kwargs = {"project_id": project_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_project(**kwargs)
        if action == "sync_project":
            kwargs = {"project_id": project_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.sync_project(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_projects', 'get_project', 'create_project', 'update_project', 'delete_project', 'sync_project"
        )


def register_credentials_tools(mcp: FastMCP):
    @mcp.tool(tags={"credentials"})
    async def ansible_tower_credentials(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_credentials', 'get_credential', 'list_credential_types', 'create_credential', 'update_credential', 'delete_credential'"
        ),
        page_size: int | None = Field(default=None, description="page size"),
        credential_id: int | None = Field(default=None, description="credential id"),
        name: Any | None = Field(default=None, description="name"),
        credential_type_id: int | None = Field(
            default=None, description="credential type id"
        ),
        organization_id: int | None = Field(
            default=None, description="organization id"
        ),
        inputs: Any | None = Field(default=None, description="inputs"),
        description: Any | None = Field(default=None, description="description"),
        client=Depends(get_client),
    ) -> dict:
        """Manage credentials operations.

        Actions:
          - 'list_credentials': Call list_credentials
          - 'get_credential': Call get_credential
          - 'list_credential_types': Call list_credential_types
          - 'create_credential': Call create_credential
          - 'update_credential': Call update_credential
          - 'delete_credential': Call delete_credential
        """
        kwargs: dict[str, Any]
        if action == "list_credentials":
            kwargs = {"page_size": page_size}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_credentials(**kwargs)
        if action == "get_credential":
            kwargs = {"credential_id": credential_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_credential(**kwargs)
        if action == "list_credential_types":
            kwargs = {"page_size": page_size}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_credential_types(**kwargs)
        if action == "create_credential":
            kwargs = {
                "name": name,
                "credential_type_id": credential_type_id,
                "organization_id": organization_id,
                "inputs": inputs,
                "description": description,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_credential(**kwargs)
        if action == "update_credential":
            kwargs = {
                "credential_id": credential_id,
                "name": name,
                "inputs": inputs,
                "description": description,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_credential(**kwargs)
        if action == "delete_credential":
            kwargs = {"credential_id": credential_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_credential(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_credentials', 'get_credential', 'list_credential_types', 'create_credential', 'update_credential', 'delete_credential"
        )


def register_organizations_tools(mcp: FastMCP):
    @mcp.tool(tags={"organizations"})
    async def ansible_tower_organizations(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_organizations', 'get_organization', 'create_organization', 'update_organization', 'delete_organization'"
        ),
        page_size: int | None = Field(default=None, description="page size"),
        organization_id: int | None = Field(
            default=None, description="organization id"
        ),
        name: Any | None = Field(default=None, description="name"),
        description: Any | None = Field(default=None, description="description"),
        client=Depends(get_client),
    ) -> dict:
        """Manage organizations operations.

        Actions:
          - 'list_organizations': Call list_organizations
          - 'get_organization': Call get_organization
          - 'create_organization': Call create_organization
          - 'update_organization': Call update_organization
          - 'delete_organization': Call delete_organization
        """
        kwargs: dict[str, Any]
        if action == "list_organizations":
            kwargs = {"page_size": page_size}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_organizations(**kwargs)
        if action == "get_organization":
            kwargs = {"organization_id": organization_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_organization(**kwargs)
        if action == "create_organization":
            kwargs = {"name": name, "description": description}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_organization(**kwargs)
        if action == "update_organization":
            kwargs = {
                "organization_id": organization_id,
                "name": name,
                "description": description,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_organization(**kwargs)
        if action == "delete_organization":
            kwargs = {"organization_id": organization_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_organization(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_organizations', 'get_organization', 'create_organization', 'update_organization', 'delete_organization"
        )


def register_teams_tools(mcp: FastMCP):
    @mcp.tool(tags={"teams"})
    async def ansible_tower_teams(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_teams', 'get_team', 'create_team', 'update_team', 'delete_team'"
        ),
        organization_id: Any | None = Field(
            default=None, description="organization id"
        ),
        page_size: int | None = Field(default=None, description="page size"),
        team_id: int | None = Field(default=None, description="team id"),
        name: Any | None = Field(default=None, description="name"),
        description: Any | None = Field(default=None, description="description"),
        client=Depends(get_client),
    ) -> dict:
        """Manage teams operations.

        Actions:
          - 'list_teams': Call list_teams
          - 'get_team': Call get_team
          - 'create_team': Call create_team
          - 'update_team': Call update_team
          - 'delete_team': Call delete_team
        """
        kwargs: dict[str, Any]
        if action == "list_teams":
            kwargs = {"organization_id": organization_id, "page_size": page_size}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_teams(**kwargs)
        if action == "get_team":
            kwargs = {"team_id": team_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_team(**kwargs)
        if action == "create_team":
            kwargs = {
                "name": name,
                "organization_id": organization_id,
                "description": description,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_team(**kwargs)
        if action == "update_team":
            kwargs = {"team_id": team_id, "name": name, "description": description}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_team(**kwargs)
        if action == "delete_team":
            kwargs = {"team_id": team_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_team(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_teams', 'get_team', 'create_team', 'update_team', 'delete_team"
        )


def register_users_tools(mcp: FastMCP):
    @mcp.tool(tags={"users"})
    async def ansible_tower_users(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_users', 'get_user', 'create_user', 'update_user', 'delete_user'"
        ),
        page_size: int | None = Field(default=None, description="page size"),
        user_id: int | None = Field(default=None, description="user id"),
        username: Any | None = Field(default=None, description="username"),
        password: Any | None = Field(default=None, description="password"),
        first_name: Any | None = Field(default=None, description="first name"),
        last_name: Any | None = Field(default=None, description="last name"),
        email: Any | None = Field(default=None, description="email"),
        is_superuser: Any | None = Field(default=None, description="is superuser"),
        is_system_auditor: Any | None = Field(
            default=None, description="is system auditor"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage users operations.

        Actions:
          - 'list_users': Call list_users
          - 'get_user': Call get_user
          - 'create_user': Call create_user
          - 'update_user': Call update_user
          - 'delete_user': Call delete_user
        """
        kwargs: dict[str, Any]
        if action == "list_users":
            kwargs = {"page_size": page_size}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_users(**kwargs)
        if action == "get_user":
            kwargs = {"user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_user(**kwargs)
        if action == "create_user":
            kwargs = {
                "username": username,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "is_superuser": is_superuser,
                "is_system_auditor": is_system_auditor,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_user(**kwargs)
        if action == "update_user":
            kwargs = {
                "user_id": user_id,
                "username": username,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "is_superuser": is_superuser,
                "is_system_auditor": is_system_auditor,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_user(**kwargs)
        if action == "delete_user":
            kwargs = {"user_id": user_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_user(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_users', 'get_user', 'create_user', 'update_user', 'delete_user"
        )


def register_ad_hoc_commands_tools(mcp: FastMCP):
    @mcp.tool(tags={"ad_hoc_commands"})
    async def ansible_tower_ad_hoc_commands(
        action: str = Field(
            description="Action to perform. Must be one of: 'run_ad_hoc_command', 'get_ad_hoc_command', 'cancel_ad_hoc_command'"
        ),
        inventory_id: int | None = Field(default=None, description="inventory id"),
        credential_id: int | None = Field(default=None, description="credential id"),
        module_name: str | None = Field(default=None, description="module name"),
        module_args: str | None = Field(default=None, description="module args"),
        limit: str | None = Field(default=None, description="limit"),
        verbosity: int | None = Field(default=None, description="verbosity"),
        command_id: int | None = Field(default=None, description="command id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage ad hoc commands operations.

        Actions:
          - 'run_ad_hoc_command': Call run_ad_hoc_command
          - 'get_ad_hoc_command': Call get_ad_hoc_command
          - 'cancel_ad_hoc_command': Call cancel_ad_hoc_command
        """
        kwargs: dict[str, Any]
        if action == "run_ad_hoc_command":
            kwargs = {
                "inventory_id": inventory_id,
                "credential_id": credential_id,
                "module_name": module_name,
                "module_args": module_args,
                "limit": limit,
                "verbosity": verbosity,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.run_ad_hoc_command(**kwargs)
        if action == "get_ad_hoc_command":
            kwargs = {"command_id": command_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_ad_hoc_command(**kwargs)
        if action == "cancel_ad_hoc_command":
            kwargs = {"command_id": command_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.cancel_ad_hoc_command(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: run_ad_hoc_command', 'get_ad_hoc_command', 'cancel_ad_hoc_command"
        )


def register_workflow_templates_tools(mcp: FastMCP):
    @mcp.tool(tags={"workflow_templates"})
    async def ansible_tower_workflow_templates(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_workflow_templates', 'get_workflow_template', 'launch_workflow'"
        ),
        page_size: int | None = Field(default=None, description="page size"),
        template_id: int | None = Field(default=None, description="template id"),
        extra_vars: str | None = Field(default=None, description="extra vars"),
        client=Depends(get_client),
    ) -> dict:
        """Manage workflow templates operations.

        Actions:
          - 'list_workflow_templates': Call list_workflow_templates
          - 'get_workflow_template': Call get_workflow_template
          - 'launch_workflow': Call launch_workflow
        """
        kwargs: dict[str, Any]
        if action == "list_workflow_templates":
            kwargs = {"page_size": page_size}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_workflow_templates(**kwargs)
        if action == "get_workflow_template":
            kwargs = {"template_id": template_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_workflow_template(**kwargs)
        if action == "launch_workflow":
            kwargs = {"template_id": template_id, "extra_vars": extra_vars}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.launch_workflow(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_workflow_templates', 'get_workflow_template', 'launch_workflow"
        )


def register_workflow_jobs_tools(mcp: FastMCP):
    @mcp.tool(tags={"workflow_jobs"})
    async def ansible_tower_workflow_jobs(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_workflow_jobs', 'get_workflow_job', 'cancel_workflow_job'"
        ),
        status: str | None = Field(default=None, description="status"),
        page_size: int | None = Field(default=None, description="page size"),
        job_id: int | None = Field(default=None, description="job id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage workflow jobs operations.

        Actions:
          - 'list_workflow_jobs': Call list_workflow_jobs
          - 'get_workflow_job': Call get_workflow_job
          - 'cancel_workflow_job': Call cancel_workflow_job
        """
        kwargs: dict[str, Any]
        if action == "list_workflow_jobs":
            kwargs = {"status": status, "page_size": page_size}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_workflow_jobs(**kwargs)
        if action == "get_workflow_job":
            kwargs = {"job_id": job_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_workflow_job(**kwargs)
        if action == "cancel_workflow_job":
            kwargs = {"job_id": job_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.cancel_workflow_job(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_workflow_jobs', 'get_workflow_job', 'cancel_workflow_job"
        )


def register_schedules_tools(mcp: FastMCP):
    @mcp.tool(tags={"schedules"})
    async def ansible_tower_schedules(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_schedules', 'get_schedule', 'create_schedule', 'update_schedule', 'delete_schedule'"
        ),
        unified_job_template_id: Any | None = Field(
            default=None, description="unified job template id"
        ),
        page_size: int | None = Field(default=None, description="page size"),
        schedule_id: int | None = Field(default=None, description="schedule id"),
        name: Any | None = Field(default=None, description="name"),
        rrule: Any | None = Field(default=None, description="rrule"),
        description: Any | None = Field(default=None, description="description"),
        extra_data: Any | None = Field(default=None, description="extra data"),
        client=Depends(get_client),
    ) -> dict:
        """Manage schedules operations.

        Actions:
          - 'list_schedules': Call list_schedules
          - 'get_schedule': Call get_schedule
          - 'create_schedule': Call create_schedule
          - 'update_schedule': Call update_schedule
          - 'delete_schedule': Call delete_schedule
        """
        kwargs: dict[str, Any]
        if action == "list_schedules":
            kwargs = {
                "unified_job_template_id": unified_job_template_id,
                "page_size": page_size,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_schedules(**kwargs)
        if action == "get_schedule":
            kwargs = {"schedule_id": schedule_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_schedule(**kwargs)
        if action == "create_schedule":
            kwargs = {
                "name": name,
                "rrule": rrule,
                "unified_job_template_id": unified_job_template_id,
                "description": description,
                "extra_data": extra_data,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_schedule(**kwargs)
        if action == "update_schedule":
            kwargs = {
                "schedule_id": schedule_id,
                "name": name,
                "rrule": rrule,
                "description": description,
                "extra_data": extra_data,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_schedule(**kwargs)
        if action == "delete_schedule":
            kwargs = {"schedule_id": schedule_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_schedule(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_schedules', 'get_schedule', 'create_schedule', 'update_schedule', 'delete_schedule"
        )


def register_system_tools(mcp: FastMCP):
    @mcp.tool(tags={"system"})
    async def ansible_tower_system(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_ansible_version', 'get_dashboard_stats', 'get_metrics'"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage system operations.

        Actions:
          - 'get_ansible_version': Call get_ansible_version
          - 'get_dashboard_stats': Call get_dashboard_stats
          - 'get_metrics': Call get_metrics
        """
        kwargs: dict[str, Any]
        if action == "get_ansible_version":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_ansible_version(**kwargs)
        if action == "get_dashboard_stats":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_dashboard_stats(**kwargs)
        if action == "get_metrics":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_metrics(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_ansible_version', 'get_dashboard_stats', 'get_metrics"
        )


def get_mcp_instance() -> tuple[Any, ...]:
    """Initialize and return the MCP instance."""
    load_dotenv(find_dotenv())
    args, mcp, middlewares = create_mcp_server(
        name="ansible-tower-mcp MCP",
        version=__version__,
        instructions="ansible-tower-mcp MCP Server — Condensed Action-Routed Tools.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    DEFAULT_INVENTORYTOOL = to_boolean(os.getenv("INVENTORYTOOL", "True"))
    if DEFAULT_INVENTORYTOOL:
        register_inventory_tools(mcp)
    DEFAULT_HOSTSTOOL = to_boolean(os.getenv("HOSTSTOOL", "True"))
    if DEFAULT_HOSTSTOOL:
        register_hosts_tools(mcp)
    DEFAULT_GROUPSTOOL = to_boolean(os.getenv("GROUPSTOOL", "True"))
    if DEFAULT_GROUPSTOOL:
        register_groups_tools(mcp)
    DEFAULT_JOB_TEMPLATESTOOL = to_boolean(os.getenv("JOB_TEMPLATESTOOL", "True"))
    if DEFAULT_JOB_TEMPLATESTOOL:
        register_job_templates_tools(mcp)
    DEFAULT_JOBSTOOL = to_boolean(os.getenv("JOBSTOOL", "True"))
    if DEFAULT_JOBSTOOL:
        register_jobs_tools(mcp)
    DEFAULT_PROJECTSTOOL = to_boolean(os.getenv("PROJECTSTOOL", "True"))
    if DEFAULT_PROJECTSTOOL:
        register_projects_tools(mcp)
    DEFAULT_CREDENTIALSTOOL = to_boolean(os.getenv("CREDENTIALSTOOL", "True"))
    if DEFAULT_CREDENTIALSTOOL:
        register_credentials_tools(mcp)
    DEFAULT_ORGANIZATIONSTOOL = to_boolean(os.getenv("ORGANIZATIONSTOOL", "True"))
    if DEFAULT_ORGANIZATIONSTOOL:
        register_organizations_tools(mcp)
    DEFAULT_TEAMSTOOL = to_boolean(os.getenv("TEAMSTOOL", "True"))
    if DEFAULT_TEAMSTOOL:
        register_teams_tools(mcp)
    DEFAULT_USERSTOOL = to_boolean(os.getenv("USERSTOOL", "True"))
    if DEFAULT_USERSTOOL:
        register_users_tools(mcp)
    DEFAULT_AD_HOC_COMMANDSTOOL = to_boolean(os.getenv("AD_HOC_COMMANDSTOOL", "True"))
    if DEFAULT_AD_HOC_COMMANDSTOOL:
        register_ad_hoc_commands_tools(mcp)
    DEFAULT_WORKFLOW_TEMPLATESTOOL = to_boolean(
        os.getenv("WORKFLOW_TEMPLATESTOOL", "True")
    )
    if DEFAULT_WORKFLOW_TEMPLATESTOOL:
        register_workflow_templates_tools(mcp)
    DEFAULT_WORKFLOW_JOBSTOOL = to_boolean(os.getenv("WORKFLOW_JOBSTOOL", "True"))
    if DEFAULT_WORKFLOW_JOBSTOOL:
        register_workflow_jobs_tools(mcp)
    DEFAULT_SCHEDULESTOOL = to_boolean(os.getenv("SCHEDULESTOOL", "True"))
    if DEFAULT_SCHEDULESTOOL:
        register_schedules_tools(mcp)
    DEFAULT_SYSTEMTOOL = to_boolean(os.getenv("SYSTEMTOOL", "True"))
    if DEFAULT_SYSTEMTOOL:
        register_system_tools(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)
    return mcp, args, middlewares


def mcp_server() -> None:
    mcp, args, middlewares = get_mcp_instance()
    print(f"ansible-tower-mcp MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error("Invalid transport", extra={"transport": args.transport})
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
