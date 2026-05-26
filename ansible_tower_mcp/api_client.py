#!/usr/bin/env python
from ansible_tower_mcp.api.api_client_credentials import Api as CredentialsApi
from ansible_tower_mcp.api.api_client_groups import Api as GroupsApi
from ansible_tower_mcp.api.api_client_hosts import Api as HostsApi
from ansible_tower_mcp.api.api_client_inventories import Api as InventoriesApi
from ansible_tower_mcp.api.api_client_jobs import Api as JobsApi
from ansible_tower_mcp.api.api_client_organizations import Api as OrganizationsApi
from ansible_tower_mcp.api.api_client_projects import Api as ProjectsApi
from ansible_tower_mcp.api.api_client_schedules import Api as SchedulesApi
from ansible_tower_mcp.api.api_client_system import Api as SystemApi
from ansible_tower_mcp.api.api_client_teams import Api as TeamsApi
from ansible_tower_mcp.api.api_client_templates import Api as TemplatesApi
from ansible_tower_mcp.api.api_client_users import Api as UsersApi

__version__ = "1.16.0"


class Api(
    CredentialsApi,
    GroupsApi,
    HostsApi,
    InventoriesApi,
    JobsApi,
    OrganizationsApi,
    ProjectsApi,
    SchedulesApi,
    SystemApi,
    TeamsApi,
    TemplatesApi,
    UsersApi,
):
    pass
