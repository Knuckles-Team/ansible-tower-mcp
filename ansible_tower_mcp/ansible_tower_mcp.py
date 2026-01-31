#!/usr/bin/env python
# coding: utf-8

"""
Ansible MCP Server

This server provides tools for interacting with the Ansible API through the Model Context Protocol.
"""

import os
import argparse
import sys
import logging
from typing import Optional, List, Dict, Union

import requests
from pydantic import Field
from eunomia_mcp.middleware import EunomiaMcpMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastmcp import FastMCP, Context
from fastmcp.server.auth.oidc_proxy import OIDCProxy
from fastmcp.server.auth import OAuthProxy, RemoteAuthProvider
from fastmcp.server.auth.providers.jwt import JWTVerifier, StaticTokenVerifier
from fastmcp.server.middleware.logging import LoggingMiddleware
from fastmcp.server.middleware.timing import TimingMiddleware
from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from fastmcp.utilities.logging import get_logger
from ansible_tower_mcp.ansible_tower_api import Api
from ansible_tower_mcp.utils import to_boolean, to_integer
from ansible_tower_mcp.middlewares import (
    UserTokenMiddleware,
    JWTClaimsLoggingMiddleware,
)

__version__ = "1.2.25"

logger = get_logger(name="TokenMiddleware")
logger.setLevel(logging.DEBUG)

config = {
    "enable_delegation": to_boolean(os.environ.get("ENABLE_DELEGATION", "False")),
    "audience": os.environ.get("AUDIENCE", None),
    "delegated_scopes": os.environ.get("DELEGATED_SCOPES", "api"),
    "token_endpoint": None,  # Will be fetched dynamically from OIDC config
    "oidc_client_id": os.environ.get("OIDC_CLIENT_ID", None),
    "oidc_client_secret": os.environ.get("OIDC_CLIENT_SECRET", None),
    "oidc_config_url": os.environ.get("OIDC_CONFIG_URL", None),
    "jwt_jwks_uri": os.getenv("FASTMCP_SERVER_AUTH_JWT_JWKS_URI", None),
    "jwt_issuer": os.getenv("FASTMCP_SERVER_AUTH_JWT_ISSUER", None),
    "jwt_audience": os.getenv("FASTMCP_SERVER_AUTH_JWT_AUDIENCE", None),
    "jwt_algorithm": os.getenv("FASTMCP_SERVER_AUTH_JWT_ALGORITHM", None),
    "jwt_secret": os.getenv("FASTMCP_SERVER_AUTH_JWT_PUBLIC_KEY", None),
    "jwt_required_scopes": os.getenv("FASTMCP_SERVER_AUTH_JWT_REQUIRED_SCOPES", None),
}

DEFAULT_TRANSPORT = os.getenv("TRANSPORT", "stdio")
DEFAULT_HOST = os.getenv("HOST", "0.0.0.0")
DEFAULT_PORT = to_integer(string=os.getenv("PORT", "8000"))


def register_tools(mcp: FastMCP):
    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    # MCP Tools - Inventory Management
    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"inventory"},
    )
    async def list_inventories(
        page_size: int = Field(10, description="Number of results per page"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> List[Dict]:
        """
        Retrieves a paginated list of inventories from Ansible Tower. Returns a list of dictionaries, each containing inventory details like id, name, and description. Display results in a markdown table for clarity.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.list_inventories(page_size=page_size)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"inventory"},
    )
    async def get_inventory(
        inventory_id: int = Field(description="ID of the inventory"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Fetches details of a specific inventory by ID from Ansible Tower. Returns a dictionary with inventory information such as name, description, and hosts count.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.get_inventory(inventory_id=inventory_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"inventory"},
    )
    async def create_inventory(
        name: str = Field(description="Name of the inventory"),
        organization_id: int = Field(description="ID of the organization"),
        description: str = Field(
            default="", description="Description of the inventory"
        ),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Creates a new inventory in Ansible Tower. Returns a dictionary with the created inventory's details, including its ID.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.create_inventory(
            name=name, organization_id=organization_id, description=description
        )

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"inventory"},
    )
    async def update_inventory(
        inventory_id: int = Field(description="ID of the inventory"),
        name: Optional[str] = Field(
            default=None, description="New name for the inventory"
        ),
        description: Optional[str] = Field(
            default=None, description="New description for the inventory"
        ),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
        ctx: Context = None,
    ) -> Dict:
        """
        Updates an existing inventory in Ansible Tower. Returns a dictionary with the updated inventory's details.
        """
        if ctx:
            message = f"Are you sure you want to UPDATE inventory {inventory_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {
                    "status": "cancelled",
                    "message": "Operation cancelled by user.",
                }

        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.update_inventory(
            inventory_id=inventory_id, name=name, description=description
        )

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"inventory"},
    )
    async def delete_inventory(
        inventory_id: int = Field(description="ID of the inventory"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
        ctx: Context = None,
    ) -> Dict:
        """
        Deletes a specific inventory by ID from Ansible Tower. Returns a dictionary confirming the deletion status.
        """
        if ctx:
            message = f"Are you sure you want to DELETE inventory {inventory_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {
                    "status": "cancelled",
                    "message": "Operation cancelled by user.",
                }

        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.delete_inventory(inventory_id=inventory_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"hosts"},
    )
    async def list_hosts(
        inventory_id: Optional[int] = Field(
            default=None, description="Optional ID of inventory to filter hosts"
        ),
        page_size: int = Field(10, description="Number of results per page"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> List[Dict]:
        """
        Retrieves a paginated list of hosts from Ansible Tower, optionally filtered by inventory. Returns a list of dictionaries, each with host details like id, name, and variables. Display in a markdown table.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.list_hosts(inventory_id=inventory_id, page_size=page_size)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"hosts"},
    )
    async def get_host(
        host_id: int = Field(description="ID of the host"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Fetches details of a specific host by ID from Ansible Tower. Returns a dictionary with host information such as name, variables, and inventory.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.get_host(host_id=host_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"hosts"},
    )
    async def create_host(
        name: str = Field(description="Name or IP address of the host"),
        inventory_id: int = Field(description="ID of the inventory to add the host to"),
        variables: str = Field(
            default="{}", description="JSON string of host variables"
        ),
        description: str = Field(default="", description="Description of the host"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Creates a new host in a specified inventory in Ansible Tower. Returns a dictionary with the created host's details, including its ID.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.create_host(
            name=name,
            inventory_id=inventory_id,
            variables=variables,
            description=description,
        )

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"hosts"},
    )
    async def update_host(
        host_id: int = Field(description="ID of the host"),
        name: Optional[str] = Field(default=None, description="New name for the host"),
        variables: Optional[str] = Field(
            default=None, description="JSON string of host variables"
        ),
        description: Optional[str] = Field(
            default=None, description="New description for the host"
        ),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
        ctx: Context = None,
    ) -> Dict:
        """
        Updates an existing host in Ansible Tower. Returns a dictionary with the updated host's details.
        """
        if ctx:
            message = f"Are you sure you want to UPDATE host {host_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {
                    "status": "cancelled",
                    "message": "Operation cancelled by user.",
                }

        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.update_host(
            host_id=host_id, name=name, variables=variables, description=description
        )

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"hosts"},
    )
    async def delete_host(
        host_id: int = Field(description="ID of the host"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
        ctx: Context = None,
    ) -> Dict:
        """
        Deletes a specific host by ID from Ansible Tower. Returns a dictionary confirming the deletion status.
        """
        if ctx:
            message = f"Are you sure you want to DELETE host {host_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {
                    "status": "cancelled",
                    "message": "Operation cancelled by user.",
                }

        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.delete_host(host_id=host_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"groups"},
    )
    async def list_groups(
        inventory_id: int = Field(description="ID of the inventory"),
        page_size: int = Field(10, description="Number of results per page"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> List[Dict]:
        """
        Retrieves a paginated list of groups in a specified inventory from Ansible Tower. Returns a list of dictionaries, each with group details like id, name, and variables. Display in a markdown table.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.list_groups(inventory_id=inventory_id, page_size=page_size)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"groups"},
    )
    async def get_group(
        group_id: int = Field(description="ID of the group"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Fetches details of a specific group by ID from Ansible Tower. Returns a dictionary with group information such as name, variables, and inventory.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.get_group(group_id=group_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"groups"},
    )
    async def create_group(
        name: str = Field(description="Name of the group"),
        inventory_id: int = Field(
            description="ID of the inventory to add the group to"
        ),
        variables: str = Field(
            default="{}", description="JSON string of group variables"
        ),
        description: str = Field(default="", description="Description of the group"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Creates a new group in a specified inventory in Ansible Tower. Returns a dictionary with the created group's details, including its ID.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.create_group(
            name=name,
            inventory_id=inventory_id,
            variables=variables,
            description=description,
        )

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"groups"},
    )
    async def update_group(
        group_id: int = Field(description="ID of the group"),
        name: Optional[str] = Field(default=None, description="New name for the group"),
        variables: Optional[str] = Field(
            default=None, description="JSON string of group variables"
        ),
        description: Optional[str] = Field(
            default=None, description="New description for the group"
        ),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Updates an existing group in Ansible Tower. Returns a dictionary with the updated group's details.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.update_group(
            group_id=group_id, name=name, variables=variables, description=description
        )

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"groups"},
    )
    async def delete_group(
        group_id: int = Field(description="ID of the group"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Deletes a specific group by ID from Ansible Tower. Returns a dictionary confirming the deletion status.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.delete_group(group_id=group_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"groups"},
    )
    async def add_host_to_group(
        group_id: int = Field(description="ID of the group"),
        host_id: int = Field(description="ID of the host"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Adds a host to a group in Ansible Tower. Returns a dictionary confirming the association.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.add_host_to_group(group_id=group_id, host_id=host_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"groups"},
    )
    async def remove_host_from_group(
        group_id: int = Field(description="ID of the group"),
        host_id: int = Field(description="ID of the host"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Removes a host from a group in Ansible Tower. Returns a dictionary confirming the disassociation.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.remove_host_from_group(group_id=group_id, host_id=host_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"job_templates"},
    )
    async def list_job_templates(
        page_size: int = Field(10, description="Number of results per page"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> List[Dict]:
        """
        Retrieves a paginated list of job templates from Ansible Tower. Returns a list of dictionaries, each with template details like id, name, and playbook. Display in a markdown table.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.list_job_templates(page_size=page_size)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"job_templates"},
    )
    async def get_job_template(
        template_id: int = Field(description="ID of the job template"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Fetches details of a specific job template by ID from Ansible Tower. Returns a dictionary with template information such as name, inventory, and extra_vars.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.get_job_template(template_id=template_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"job_templates"},
    )
    async def create_job_template(
        name: str = Field(description="Name of the job template"),
        inventory_id: int = Field(description="ID of the inventory"),
        project_id: int = Field(description="ID of the project"),
        playbook: str = Field(
            description="Name of the playbook (e.g., 'playbook.yml')"
        ),
        credential_id: Optional[int] = Field(
            default=None, description="Optional ID of the credential"
        ),
        description: str = Field(
            default="", description="Description of the job template"
        ),
        extra_vars: str = Field(
            default="{}", description="JSON string of extra variables"
        ),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Creates a new job template in Ansible Tower. Returns a dictionary with the created template's details, including its ID.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.create_job_template(
            name=name,
            inventory_id=inventory_id,
            project_id=project_id,
            playbook=playbook,
            credential_id=credential_id,
            description=description,
            extra_vars=extra_vars,
        )

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"job_templates"},
    )
    async def update_job_template(
        template_id: int = Field(description="ID of the job template"),
        name: Optional[str] = Field(
            default=None, description="New name for the job template"
        ),
        inventory_id: Optional[int] = Field(
            default=None, description="New inventory ID"
        ),
        playbook: Optional[str] = Field(default=None, description="New playbook name"),
        description: Optional[str] = Field(default=None, description="New description"),
        extra_vars: Optional[str] = Field(
            default=None, description="JSON string of extra variables"
        ),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
        ctx: Context = None,
    ) -> Dict:
        """
        Updates an existing job template in Ansible Tower. Returns a dictionary with the updated template's details.
        """
        if ctx:
            message = f"Are you sure you want to UPDATE job template {template_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {
                    "status": "cancelled",
                    "message": "Operation cancelled by user.",
                }

        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.update_job_template(
            template_id=template_id,
            name=name,
            inventory_id=inventory_id,
            playbook=playbook,
            description=description,
            extra_vars=extra_vars,
        )

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"job_templates"},
    )
    async def delete_job_template(
        template_id: int = Field(description="ID of the job template"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
        ctx: Context = None,
    ) -> Dict:
        """
        Deletes a specific job template by ID from Ansible Tower. Returns a dictionary confirming the deletion status.
        """
        if ctx:
            message = f"Are you sure you want to DELETE job template {template_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {
                    "status": "cancelled",
                    "message": "Operation cancelled by user.",
                }

        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.delete_job_template(template_id=template_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"job_templates"},
    )
    async def launch_job(
        template_id: int = Field(description="ID of the job template"),
        extra_vars: Optional[str] = Field(
            default=None,
            description="JSON string of extra variables to override the template's variables",
        ),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
        ctx: Context = None,
    ) -> Dict:
        """
        Launches a job from a template in Ansible Tower, optionally with extra variables. Returns a dictionary with the launched job's details, including its ID.
        """
        if ctx:
            message = (
                f"Are you sure you want to LAUNCH job from template {template_id}?"
            )
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {
                    "status": "cancelled",
                    "message": "Operation cancelled by user.",
                }

        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.launch_job(template_id=template_id, extra_vars=extra_vars)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"jobs"},
    )
    async def list_jobs(
        status: Optional[str] = Field(
            default=None,
            description="Filter by job status (pending, waiting, running, successful, failed, canceled)",
        ),
        page_size: int = Field(10, description="Number of results per page"),
        page: int = Field(1, description="Page number to retrieve"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> List[Dict]:
        """
        Retrieves a paginated list of jobs from Ansible Tower, optionally filtered by status. Returns a list of dictionaries, each with job details like id, status, and elapsed time. Display in a markdown table.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.list_jobs(status=status, page_size=page_size)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"jobs"},
    )
    async def get_job(
        job_id: int = Field(description="ID of the job"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Fetches details of a specific job by ID from Ansible Tower. Returns a dictionary with job information such as status, start time, and artifacts.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.get_job(job_id=job_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"jobs"},
    )
    async def cancel_job(
        job_id: int = Field(description="ID of the job"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
        ctx: Context = None,
    ) -> Dict:
        """
        Cancels a running job in Ansible Tower. Returns a dictionary confirming the cancellation status.
        """
        if ctx:
            message = f"Are you sure you want to CANCEL job {job_id}?"
            result = await ctx.elicit(message, response_type=bool)
            if result.action != "accept" or not result.data:
                return {
                    "status": "cancelled",
                    "message": "Operation cancelled by user.",
                }

        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.cancel_job(job_id=job_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"jobs"},
    )
    async def get_job_events(
        job_id: int = Field(description="ID of the job"),
        page_size: int = Field(10, description="Number of results per page"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> List[Dict]:
        """
        Retrieves a paginated list of events for a specific job from Ansible Tower. Returns a list of dictionaries, each with event details like type, host, and stdout. Display in a markdown table.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.get_job_events(job_id=job_id, page_size=page_size)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"jobs"},
    )
    async def get_job_stdout(
        job_id: int = Field(description="ID of the job"),
        format: str = Field(
            default="txt", description="Format of the output (txt, html, json, ansi)"
        ),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Fetches the stdout output of a job in the specified format from Ansible Tower. Returns a dictionary with the output content.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.get_job_stdout(job_id=job_id, format=format)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"projects"},
    )
    async def list_projects(
        page_size: int = Field(10, description="Number of results per page"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> List[Dict]:
        """
        Retrieves a paginated list of projects from Ansible Tower. Returns a list of dictionaries, each with project details like id, name, and scm_type. Display in a markdown table.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.list_projects(page_size=page_size)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"projects"},
    )
    async def get_project(
        project_id: int = Field(description="ID of the project"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Fetches details of a specific project by ID from Ansible Tower. Returns a dictionary with project information such as name, scm_url, and status.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.get_project(project_id=project_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"projects"},
    )
    async def create_project(
        name: str = Field(description="Name of the project"),
        organization_id: int = Field(description="ID of the organization"),
        scm_type: str = Field(description="SCM type (git, hg, svn, manual)"),
        scm_url: Optional[str] = Field(
            default=None, description="URL for the repository"
        ),
        scm_branch: Optional[str] = Field(
            default=None, description="Branch/tag/commit to checkout"
        ),
        credential_id: Optional[int] = Field(
            default=None, description="ID of the credential for SCM access"
        ),
        description: str = Field(default="", description="Description of the project"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Creates a new project in Ansible Tower. Returns a dictionary with the created project's details, including its ID.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.create_project(
            name=name,
            organization_id=organization_id,
            scm_type=scm_type,
            scm_url=scm_url,
            scm_branch=scm_branch,
            credential_id=credential_id,
            description=description,
        )

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"projects"},
    )
    async def update_project(
        project_id: int = Field(description="ID of the project"),
        name: Optional[str] = Field(
            default=None, description="New name for the project"
        ),
        scm_type: Optional[str] = Field(
            default=None, description="New SCM type (git, hg, svn, manual)"
        ),
        scm_url: Optional[str] = Field(
            default=None, description="New URL for the repository"
        ),
        scm_branch: Optional[str] = Field(
            default=None, description="New branch/tag/commit to checkout"
        ),
        description: Optional[str] = Field(default=None, description="New description"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Updates an existing project in Ansible Tower. Returns a dictionary with the updated project's details.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.update_project(
            project_id=project_id,
            name=name,
            scm_type=scm_type,
            scm_url=scm_url,
            scm_branch=scm_branch,
            description=description,
        )

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"projects"},
    )
    async def delete_project(
        project_id: int = Field(description="ID of the project"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Deletes a specific project by ID from Ansible Tower. Returns a dictionary confirming the deletion status.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.delete_project(project_id=project_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"projects"},
    )
    async def sync_project(
        project_id: int = Field(description="ID of the project"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Syncs (updates from SCM) a project in Ansible Tower. Returns a dictionary with the sync job's details.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.sync_project(project_id=project_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"credentials"},
    )
    async def list_credentials(
        page_size: int = Field(10, description="Number of results per page"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> List[Dict]:
        """
        Retrieves a paginated list of credentials from Ansible Tower. Returns a list of dictionaries, each with credential details like id, name, and type. Display in a markdown table.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.list_credentials(page_size=page_size)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"credentials"},
    )
    async def get_credential(
        credential_id: int = Field(description="ID of the credential"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Fetches details of a specific credential by ID from Ansible Tower. Returns a dictionary with credential information such as name and inputs (masked).
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.get_credential(credential_id=credential_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"credentials"},
    )
    async def list_credential_types(
        page_size: int = Field(10, description="Number of results per page"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> List[Dict]:
        """
        Retrieves a paginated list of credential types from Ansible Tower. Returns a list of dictionaries, each with type details like id and name. Display in a markdown table.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.list_credential_types(page_size=page_size)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"credentials"},
    )
    async def create_credential(
        name: str = Field(description="Name of the credential"),
        credential_type_id: int = Field(description="ID of the credential type"),
        organization_id: int = Field(description="ID of the organization"),
        inputs: str = Field(
            description="JSON string of credential inputs (e.g., username, password)"
        ),
        description: str = Field(
            default="", description="Description of the credential"
        ),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Creates a new credential in Ansible Tower. Returns a dictionary with the created credential's details, including its ID.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.create_credential(
            name=name,
            credential_type_id=credential_type_id,
            organization_id=organization_id,
            inputs=inputs,
            description=description,
        )

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"credentials"},
    )
    async def update_credential(
        credential_id: int = Field(description="ID of the credential"),
        name: Optional[str] = Field(
            default=None, description="New name for the credential"
        ),
        inputs: Optional[str] = Field(
            default=None, description="JSON string of credential inputs"
        ),
        description: Optional[str] = Field(default=None, description="New description"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Updates an existing credential in Ansible Tower. Returns a dictionary with the updated credential's details.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.update_credential(
            credential_id=credential_id,
            name=name,
            inputs=inputs,
            description=description,
        )

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"credentials"},
    )
    async def delete_credential(
        credential_id: int = Field(description="ID of the credential"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Deletes a specific credential by ID from Ansible Tower. Returns a dictionary confirming the deletion status.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.delete_credential(credential_id=credential_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"organizations"},
    )
    async def list_organizations(
        page_size: int = Field(10, description="Number of results per page"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> List[Dict]:
        """
        Retrieves a paginated list of organizations from Ansible Tower. Returns a list of dictionaries, each with organization details like id and name. Display in a markdown table.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.list_organizations(page_size=page_size)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"organizations"},
    )
    async def get_organization(
        organization_id: int = Field(description="ID of the organization"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Fetches details of a specific organization by ID from Ansible Tower. Returns a dictionary with organization information such as name and description.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.get_organization(organization_id=organization_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"organizations"},
    )
    async def create_organization(
        name: str = Field(description="Name of the organization"),
        description: str = Field(
            default="", description="Description of the organization"
        ),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Creates a new organization in Ansible Tower. Returns a dictionary with the created organization's details, including its ID.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.create_organization(name=name, description=description)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"organizations"},
    )
    async def update_organization(
        organization_id: int = Field(description="ID of the organization"),
        name: Optional[str] = Field(
            default=None, description="New name for the organization"
        ),
        description: Optional[str] = Field(default=None, description="New description"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Updates an existing organization in Ansible Tower. Returns a dictionary with the updated organization's details.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.update_organization(
            organization_id=organization_id, name=name, description=description
        )

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"organizations"},
    )
    async def delete_organization(
        organization_id: int = Field(description="ID of the organization"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Deletes a specific organization by ID from Ansible Tower. Returns a dictionary confirming the deletion status.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.delete_organization(organization_id=organization_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"teams"},
    )
    async def list_teams(
        organization_id: Optional[int] = Field(
            default=None, description="Optional ID of organization to filter teams"
        ),
        page_size: int = Field(10, description="Number of results per page"),
        page: int = Field(1, description="Page number to retrieve"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> List[Dict]:
        """
        Retrieves a paginated list of teams from Ansible Tower, optionally filtered by organization. Returns a list of dictionaries, each with team details like id and name. Display in a markdown table.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.list_teams(organization_id=organization_id, page_size=page_size)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"teams"},
    )
    async def get_team(
        team_id: int = Field(description="ID of the team"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Fetches details of a specific team by ID from Ansible Tower. Returns a dictionary with team information such as name and organization.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.get_team(team_id=team_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"teams"},
    )
    async def create_team(
        name: str = Field(description="Name of the team"),
        organization_id: int = Field(description="ID of the organization"),
        description: str = Field(default="", description="Description of the team"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Creates a new team in a specified organization in Ansible Tower. Returns a dictionary with the created team's details, including its ID.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.create_team(
            name=name, organization_id=organization_id, description=description
        )

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"teams"},
    )
    async def update_team(
        team_id: int = Field(description="ID of the team"),
        name: Optional[str] = Field(default=None, description="New name for the team"),
        description: Optional[str] = Field(default=None, description="New description"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Updates an existing team in Ansible Tower. Returns a dictionary with the updated team's details.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.update_team(team_id=team_id, name=name, description=description)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"teams"},
    )
    async def delete_team(
        team_id: int = Field(description="ID of the team"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Deletes a specific team by ID from Ansible Tower. Returns a dictionary confirming the deletion status.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.delete_team(team_id=team_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"users"},
    )
    async def list_users(
        page_size: int = Field(10, description="Page number to retrieve"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> List[Dict]:
        """
        Retrieves a paginated list of users from Ansible Tower. Returns a list of dictionaries, each with user details like id, username, and email. Display in a markdown table.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.list_users(page_size=page_size)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"users"},
    )
    async def get_user(
        user_id: int = Field(description="ID of the user"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Fetches details of a specific user by ID from Ansible Tower. Returns a dictionary with user information such as username, email, and roles.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.get_user(user_id=user_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"users"},
    )
    async def create_user(
        new_username: str = Field(description="Username for the new user"),
        new_password: str = Field(description="Password for the new user"),
        first_name: str = Field(default="", description="First name of the user"),
        last_name: str = Field(default="", description="Last name of the user"),
        email: str = Field(default="", description="Email address of the user"),
        is_superuser: bool = Field(
            default=False, description="Whether the user should be a superuser"
        ),
        is_system_auditor: bool = Field(
            default=False, description="Whether the user should be a system auditor"
        ),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Creates a new user in Ansible Tower. Returns a dictionary with the created user's details, including its ID.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.create_user(
            username=new_username,
            password=new_password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_superuser=is_superuser,
            is_system_auditor=is_system_auditor,
        )

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"users"},
    )
    async def update_user(
        user_id: int = Field(description="ID of the user"),
        new_username: Optional[str] = Field(default=None, description="New username"),
        new_password: Optional[str] = Field(default=None, description="New password"),
        first_name: Optional[str] = Field(default=None, description="New first name"),
        last_name: Optional[str] = Field(default=None, description="New last name"),
        email: Optional[str] = Field(default=None, description="New email address"),
        is_superuser: Optional[bool] = Field(
            default=None, description="Whether the user should be a superuser"
        ),
        is_system_auditor: Optional[bool] = Field(
            default=None, description="Whether the user should be a system auditor"
        ),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Updates an existing user in Ansible Tower. Returns a dictionary with the updated user's details.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.update_user(
            user_id=user_id,
            username=new_username,
            password=new_password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_superuser=is_superuser,
            is_system_auditor=is_system_auditor,
        )

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"users"},
    )
    async def delete_user(
        user_id: int = Field(description="ID of the user"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Deletes a specific user by ID from Ansible Tower. Returns a dictionary confirming the deletion status.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.delete_user(user_id=user_id)

    # MCP Tools - Ad Hoc Commands
    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"ad_hoc_commands"},
    )
    async def run_ad_hoc_command(
        inventory_id: int = Field(description="ID of the inventory"),
        credential_id: int = Field(description="ID of the credential"),
        module_name: str = Field(
            description="Module name (e.g., command, shell, ping)"
        ),
        module_args: str = Field(description="Module arguments"),
        limit: str = Field(default="", description="Host pattern to target"),
        verbosity: int = Field(default=0, description="Verbosity level (0-4)"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Runs an ad hoc command on hosts in Ansible Tower. Returns a dictionary with the command job's details, including its ID.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.run_ad_hoc_command(
            inventory_id=inventory_id,
            credential_id=credential_id,
            module_name=module_name,
            module_args=module_args,
            limit=limit,
            verbosity=verbosity,
        )

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"ad_hoc_commands"},
    )
    async def get_ad_hoc_command(
        command_id: int = Field(description="ID of the ad hoc command"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Fetches details of a specific ad hoc command by ID from Ansible Tower. Returns a dictionary with command information such as status and module_args.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.get_ad_hoc_command(command_id=command_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"ad_hoc_commands"},
    )
    async def cancel_ad_hoc_command(
        command_id: int = Field(description="ID of the ad hoc command"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Cancels a running ad hoc command in Ansible Tower. Returns a dictionary confirming the cancellation status.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.cancel_ad_hoc_command(command_id=command_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"workflow_templates"},
    )
    async def list_workflow_templates(
        page_size: int = Field(10, description="Number of results per page"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> List[Dict]:
        """
        Retrieves a paginated list of workflow templates from Ansible Tower. Returns a list of dictionaries, each with template details like id and name. Display in a markdown table.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.list_workflow_templates(page_size=page_size)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"workflow_templates"},
    )
    async def get_workflow_template(
        template_id: int = Field(description="ID of the workflow template"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Fetches details of a specific workflow template by ID from Ansible Tower. Returns a dictionary with template information such as name and extra_vars.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.get_workflow_template(template_id=template_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"workflow_templates"},
    )
    async def launch_workflow(
        template_id: int = Field(description="ID of the workflow template"),
        extra_vars: Optional[str] = Field(
            default=None,
            description="JSON string of extra variables to override the template's variables",
        ),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Launches a workflow from a template in Ansible Tower, optionally with extra variables. Returns a dictionary with the launched workflow job's details, including its ID.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.launch_workflow(template_id=template_id, extra_vars=extra_vars)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"workflow_jobs"},
    )
    async def list_workflow_jobs(
        status: Optional[str] = Field(
            default=None,
            description="Filter by job status (pending, waiting, running, successful, failed, canceled)",
        ),
        page_size: int = Field(10, description="Number of results per page"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> List[Dict]:
        """
        Retrieves a paginated list of workflow jobs from Ansible Tower, optionally filtered by status. Returns a list of dictionaries, each with job details like id and status. Display in a markdown table.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.list_workflow_jobs(status=status, page_size=page_size)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"workflow_jobs"},
    )
    async def get_workflow_job(
        job_id: int = Field(description="ID of the workflow job"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Fetches details of a specific workflow job by ID from Ansible Tower. Returns a dictionary with job information such as status and start time.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.get_workflow_job(job_id=job_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"workflow_jobs"},
    )
    async def cancel_workflow_job(
        job_id: int = Field(description="ID of the workflow job"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Cancels a running workflow job in Ansible Tower. Returns a dictionary confirming the cancellation status.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.cancel_workflow_job(job_id=job_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"schedules"},
    )
    async def list_schedules(
        unified_job_template_id: Optional[int] = Field(
            default=None,
            description="Optional ID of job or workflow template to filter schedules",
        ),
        page_size: int = Field(10, description="Number of results per page"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> List[Dict]:
        """
        Retrieves a paginated list of schedules from Ansible Tower, optionally filtered by template. Returns a list of dictionaries, each with schedule details like id, name, and rrule. Display in a markdown table.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.list_schedules(
            unified_job_template_id=unified_job_template_id, page_size=page_size
        )

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"schedules"},
    )
    async def get_schedule(
        schedule_id: int = Field(description="ID of the schedule"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Fetches details of a specific schedule by ID from Ansible Tower. Returns a dictionary with schedule information such as name and rrule.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.get_schedule(schedule_id=schedule_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"schedules"},
    )
    async def create_schedule(
        name: str = Field(description="Name of the schedule"),
        unified_job_template_id: int = Field(
            description="ID of the job or workflow template"
        ),
        rrule: str = Field(
            description="iCal recurrence rule (e.g., 'DTSTART:20231001T120000Z RRULE:FREQ=DAILY;INTERVAL=1')"
        ),
        description: str = Field(default="", description="Description of the schedule"),
        extra_data: str = Field(
            default="{}", description="JSON string of extra variables"
        ),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Creates a new schedule for a template in Ansible Tower. Returns a dictionary with the created schedule's details, including its ID.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.create_schedule(
            name=name,
            unified_job_template_id=unified_job_template_id,
            rrule=rrule,
            description=description,
            extra_data=extra_data,
        )

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"schedules"},
    )
    async def update_schedule(
        schedule_id: int = Field(description="ID of the schedule"),
        name: Optional[str] = Field(
            default=None, description="New name for the schedule"
        ),
        rrule: Optional[str] = Field(
            default=None, description="New iCal recurrence rule"
        ),
        description: Optional[str] = Field(default=None, description="New description"),
        extra_data: Optional[str] = Field(
            default=None, description="JSON string of extra variables"
        ),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Updates an existing schedule in Ansible Tower. Returns a dictionary with the updated schedule's details.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.update_schedule(
            schedule_id=schedule_id,
            name=name,
            rrule=rrule,
            description=description,
            extra_data=extra_data,
        )

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"schedules"},
    )
    async def delete_schedule(
        schedule_id: int = Field(description="ID of the schedule"),
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Deletes a specific schedule by ID from Ansible Tower. Returns a dictionary confirming the deletion status.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.delete_schedule(schedule_id=schedule_id)

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"system"},
    )
    async def get_ansible_version(
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Retrieves the Ansible version information from Ansible Tower. Returns a dictionary with version details.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.get_ansible_version()

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"system"},
    )
    async def get_dashboard_stats(
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Fetches dashboard statistics from Ansible Tower. Returns a dictionary with stats like host counts and recent jobs.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.get_dashboard_stats()

    @mcp.tool(
        exclude_args=[
            "base_url",
            "username",
            "password",
            "token",
            "verify",
            "client_id",
            "client_secret",
        ],
        tags={"system"},
    )
    async def get_metrics(
        base_url: str = Field(
            default=os.environ.get("ANSIBLE_BASE_URL", None),
            description="The base URL of the Ansible Tower instance",
        ),
        username: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_USERNAME", None),
            description="Username for authentication",
        ),
        password: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_PASSWORD", None),
            description="Password for authentication",
        ),
        token: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_TOKEN", None),
            description="API token for authentication",
        ),
        client_id: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_ID", None),
            description="Client ID for OAuth authentication",
        ),
        client_secret: Optional[str] = Field(
            default=os.environ.get("ANSIBLE_CLIENT_SECRET", None),
            description="Client secret for OAuth authentication",
        ),
        verify: bool = Field(
            default=to_boolean(os.environ.get("ANSIBLE_VERIFY", "False")),
            description="Whether to verify SSL certificates",
        ),
    ) -> Dict:
        """
        Retrieves system metrics from Ansible Tower. Returns a dictionary with performance and usage metrics.
        """
        client = Api(
            base_url=base_url,
            username=username,
            password=password,
            token=token,
            client_id=client_id,
            client_secret=client_secret,
            verify=verify,
        )
        return client.get_metrics()


def register_prompts(mcp: FastMCP):
    # Prompts
    @mcp.prompt
    def list_inventories_prompt(
        page_size: int = 10,
    ) -> str:
        """
        Generates a prompt for listing inventories in Ansible Tower.
        """
        return f"List inventories in Ansible Tower. Page size: {page_size}. Use the `list_inventories` tool."

    @mcp.prompt
    def manage_inventory_prompt(
        inventory_id: int,
        action: str = "get",
    ) -> str:
        """
        Generates a prompt for managing a specific inventory (get, update, delete).
        """
        return f"Perform action '{action}' on inventory with ID {inventory_id}. Use `get_inventory`, `update_inventory`, or `delete_inventory`."

    @mcp.prompt
    def create_inventory_prompt(
        name: str,
        organization_id: int,
        description: str = "",
    ) -> str:
        """
        Generates a prompt for creating a new inventory.
        """
        return f"Create a new inventory named '{name}' in organization {organization_id}. Description: '{description}'. Use the `create_inventory` tool."

    @mcp.prompt
    def list_hosts_prompt(
        inventory_id: int = 0,
        page_size: int = 10,
    ) -> str:
        """
        Generates a prompt for listing hosts, optionally filtered by inventory.
        """
        if inventory_id:
            return f"List hosts for inventory ID {inventory_id}. Page size: {page_size}. Use the `list_hosts` tool."
        return f"List all hosts. Page size: {page_size}. Use the `list_hosts` tool."

    @mcp.prompt
    def manage_host_prompt(
        host_id: int,
        action: str = "get",
    ) -> str:
        """
        Generates a prompt for managing a specific host (get, update, delete).
        """
        return f"Perform action '{action}' on host with ID {host_id}. Use `get_host`, `update_host`, or `delete_host`."

    @mcp.prompt
    def create_host_prompt(
        name: str,
        inventory_id: int,
        variables: str = "{}",
    ) -> str:
        """
        Generates a prompt for creating a new host.
        """
        return f"Create a new host named '{name}' in inventory {inventory_id}. Variables: '{variables}'. Use the `create_host` tool."

    @mcp.prompt
    def list_job_templates_prompt(
        page_size: int = 10,
    ) -> str:
        """
        Generates a prompt for listing job templates.
        """
        return f"List job templates. Page size: {page_size}. Use the `list_job_templates` tool."

    @mcp.prompt
    def launch_job_prompt(
        template_id: int,
        extra_vars: str = "{}",
    ) -> str:
        """
        Generates a prompt for launching a job from a template.
        """
        return f"Launch a job using template ID {template_id}. Extra vars: '{extra_vars}'. Use the `launch_job` tool."

    @mcp.prompt
    def list_jobs_prompt(
        status: str = "",
        page_size: int = 10,
    ) -> str:
        """
        Generates a prompt for listing jobs, optionally filtered by status.
        """
        return f"List jobs. Status: '{status}', Page size: {page_size}. Use the `list_jobs` tool."

    @mcp.prompt
    def get_job_details_prompt(
        job_id: int,
        detail_type: str = "info",
    ) -> str:
        """
        Generates a prompt for getting job details, events, or stdout.
        """
        return f"Get '{detail_type}' for job ID {job_id}. Use `get_job` (info), `get_job_events`, or `get_job_stdout`."

    @mcp.prompt
    def list_projects_prompt(
        page_size: int = 10,
    ) -> str:
        """
        Generates a prompt for listing projects.
        """
        return f"List projects. Page size: {page_size}. Use the `list_projects` tool."

    @mcp.prompt
    def sync_project_prompt(
        project_id: int,
    ) -> str:
        """
        Generates a prompt for syncing a project.
        """
        return f"Sync project with ID {project_id}. Use the `sync_project` tool."


def ansible_tower_mcp():
    print(f"ansible_tower_mcp v{__version__}")
    parser = argparse.ArgumentParser(description="Ansible Tower MCP")

    parser.add_argument(
        "-t",
        "--transport",
        default=DEFAULT_TRANSPORT,
        choices=["stdio", "streamable-http", "sse"],
        help="Transport method: 'stdio', 'streamable-http', or 'sse' [legacy] (default: stdio)",
    )
    parser.add_argument(
        "-s",
        "--host",
        default=DEFAULT_HOST,
        help="Host address for HTTP transport (default: 0.0.0.0)",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="Port number for HTTP transport (default: 8000)",
    )
    parser.add_argument(
        "--auth-type",
        default="none",
        choices=["none", "static", "jwt", "oauth-proxy", "oidc-proxy", "remote-oauth"],
        help="Authentication type for MCP server: 'none' (disabled), 'static' (internal), 'jwt' (external token verification), 'oauth-proxy', 'oidc-proxy', 'remote-oauth' (external) (default: none)",
    )
    # JWT/Token params
    parser.add_argument(
        "--token-jwks-uri", default=None, help="JWKS URI for JWT verification"
    )
    parser.add_argument(
        "--token-issuer", default=None, help="Issuer for JWT verification"
    )
    parser.add_argument(
        "--token-audience", default=None, help="Audience for JWT verification"
    )
    parser.add_argument(
        "--token-algorithm",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_ALGORITHM"),
        choices=[
            "HS256",
            "HS384",
            "HS512",
            "RS256",
            "RS384",
            "RS512",
            "ES256",
            "ES384",
            "ES512",
        ],
        help="JWT signing algorithm (required for HMAC or static key). Auto-detected for JWKS.",
    )
    parser.add_argument(
        "--token-secret",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_PUBLIC_KEY"),
        help="Shared secret for HMAC (HS*) or PEM public key for static asymmetric verification.",
    )
    parser.add_argument(
        "--token-public-key",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_PUBLIC_KEY"),
        help="Path to PEM public key file or inline PEM string (for static asymmetric keys).",
    )
    parser.add_argument(
        "--required-scopes",
        default=os.getenv("FASTMCP_SERVER_AUTH_JWT_REQUIRED_SCOPES"),
        help="Comma-separated list of required scopes (e.g., ansible.read,ansible.write).",
    )
    # OAuth Proxy params
    parser.add_argument(
        "--oauth-upstream-auth-endpoint",
        default=None,
        help="Upstream authorization endpoint for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-upstream-token-endpoint",
        default=None,
        help="Upstream token endpoint for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-upstream-client-id",
        default=None,
        help="Upstream client ID for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-upstream-client-secret",
        default=None,
        help="Upstream client secret for OAuth Proxy",
    )
    parser.add_argument(
        "--oauth-base-url", default=None, help="Base URL for OAuth Proxy"
    )
    # OIDC Proxy params
    parser.add_argument(
        "--oidc-config-url", default=None, help="OIDC configuration URL"
    )
    parser.add_argument("--oidc-client-id", default=None, help="OIDC client ID")
    parser.add_argument("--oidc-client-secret", default=None, help="OIDC client secret")
    parser.add_argument("--oidc-base-url", default=None, help="Base URL for OIDC Proxy")
    # Remote OAuth params
    parser.add_argument(
        "--remote-auth-servers",
        default=None,
        help="Comma-separated list of authorization servers for Remote OAuth",
    )
    parser.add_argument(
        "--remote-base-url", default=None, help="Base URL for Remote OAuth"
    )
    # Common
    parser.add_argument(
        "--allowed-client-redirect-uris",
        default=None,
        help="Comma-separated list of allowed client redirect URIs",
    )
    # Eunomia params
    parser.add_argument(
        "--eunomia-type",
        default="none",
        choices=["none", "embedded", "remote"],
        help="Eunomia authorization type: 'none' (disabled), 'embedded' (built-in), 'remote' (external) (default: none)",
    )
    parser.add_argument(
        "--eunomia-policy-file",
        default="mcp_policies.json",
        help="Policy file for embedded Eunomia (default: mcp_policies.json)",
    )
    parser.add_argument(
        "--eunomia-remote-url", default=None, help="URL for remote Eunomia server"
    )
    # Delegation params
    parser.add_argument(
        "--enable-delegation",
        action="store_true",
        default=to_boolean(os.environ.get("ENABLE_DELEGATION", "False")),
        help="Enable OIDC token delegation",
    )
    parser.add_argument(
        "--audience",
        default=os.environ.get("AUDIENCE", None),
        help="Audience for the delegated token",
    )
    parser.add_argument(
        "--delegated-scopes",
        default=os.environ.get("DELEGATED_SCOPES", "api"),
        help="Scopes for the delegated token (space-separated)",
    )
    parser.add_argument(
        "--openapi-file",
        default=None,
        help="Path to the OpenAPI JSON file to import additional tools from",
    )
    parser.add_argument(
        "--openapi-base-url",
        default=None,
        help="Base URL for the OpenAPI client (overrides instance URL)",
    )
    parser.add_argument(
        "--openapi-use-token",
        action="store_true",
        help="Use the incoming Bearer token (from MCP request) to authenticate OpenAPI import",
    )

    parser.add_argument(
        "--openapi-username",
        default=os.getenv("OPENAPI_USERNAME"),
        help="Username for basic auth during OpenAPI import",
    )

    parser.add_argument(
        "--openapi-password",
        default=os.getenv("OPENAPI_PASSWORD"),
        help="Password for basic auth during OpenAPI import",
    )

    parser.add_argument(
        "--openapi-client-id",
        default=os.getenv("OPENAPI_CLIENT_ID"),
        help="OAuth client ID for OpenAPI import",
    )

    parser.add_argument(
        "--openapi-client-secret",
        default=os.getenv("OPENAPI_CLIENT_SECRET"),
        help="OAuth client secret for OpenAPI import",
    )

    args = parser.parse_args()

    if args.port < 0 or args.port > 65535:
        print(f"Error: Port {args.port} is out of valid range (0-65535).")
        sys.exit(1)

    # Update config with CLI arguments
    config["enable_delegation"] = args.enable_delegation
    config["audience"] = args.audience or config["audience"]
    config["delegated_scopes"] = args.delegated_scopes or config["delegated_scopes"]
    config["oidc_config_url"] = args.oidc_config_url or config["oidc_config_url"]
    config["oidc_client_id"] = args.oidc_client_id or config["oidc_client_id"]
    config["oidc_client_secret"] = (
        args.oidc_client_secret or config["oidc_client_secret"]
    )

    # Configure delegation if enabled
    if config["enable_delegation"]:
        if args.auth_type != "oidc-proxy":
            logger.error("Token delegation requires auth-type=oidc-proxy")
            sys.exit(1)
        if not config["audience"]:
            logger.error("audience is required for delegation")
            sys.exit(1)
        if not all(
            [
                config["oidc_config_url"],
                config["oidc_client_id"],
                config["oidc_client_secret"],
            ]
        ):
            logger.error(
                "Delegation requires complete OIDC configuration (oidc-config-url, oidc-client-id, oidc-client-secret)"
            )
            sys.exit(1)

        # Fetch OIDC configuration to get token_endpoint
        try:
            logger.info(
                "Fetching OIDC configuration",
                extra={"oidc_config_url": config["oidc_config_url"]},
            )
            oidc_config_resp = requests.get(config["oidc_config_url"])
            oidc_config_resp.raise_for_status()
            oidc_config = oidc_config_resp.json()
            config["token_endpoint"] = oidc_config.get("token_endpoint")
            if not config["token_endpoint"]:
                logger.error("No token_endpoint found in OIDC configuration")
                raise ValueError("No token_endpoint found in OIDC configuration")
            logger.info(
                "OIDC configuration fetched successfully",
                extra={"token_endpoint": config["token_endpoint"]},
            )
        except Exception as e:
            print(f"Failed to fetch OIDC configuration: {e}")
            logger.error(
                "Failed to fetch OIDC configuration",
                extra={"error_type": type(e).__name__, "error_message": str(e)},
            )
            sys.exit(1)

    # Set auth based on type
    auth = None
    allowed_uris = (
        args.allowed_client_redirect_uris.split(",")
        if args.allowed_client_redirect_uris
        else None
    )

    if args.auth_type == "none":
        auth = None
    elif args.auth_type == "static":
        auth = StaticTokenVerifier(
            tokens={
                "test-token": {"client_id": "test-user", "scopes": ["read", "write"]},
                "admin-token": {"client_id": "admin", "scopes": ["admin"]},
            }
        )
    elif args.auth_type == "jwt":
        # Fallback to env vars if not provided via CLI
        jwks_uri = args.token_jwks_uri or os.getenv("FASTMCP_SERVER_AUTH_JWT_JWKS_URI")
        issuer = args.token_issuer or os.getenv("FASTMCP_SERVER_AUTH_JWT_ISSUER")
        audience = args.token_audience or os.getenv("FASTMCP_SERVER_AUTH_JWT_AUDIENCE")
        algorithm = args.token_algorithm
        secret_or_key = args.token_secret or args.token_public_key
        public_key_pem = None

        if not (jwks_uri or secret_or_key):
            logger.error(
                "JWT auth requires either --token-jwks-uri or --token-secret/--token-public-key"
            )
            sys.exit(1)
        if not (issuer and audience):
            logger.error("JWT requires --token-issuer and --token-audience")
            sys.exit(1)

        # Load static public key from file if path is given
        if args.token_public_key and os.path.isfile(args.token_public_key):
            try:
                with open(args.token_public_key, "r") as f:
                    public_key_pem = f.read()
                logger.info(f"Loaded static public key from {args.token_public_key}")
            except Exception as e:
                print(f"Failed to read public key file: {e}")
                logger.error(f"Failed to read public key file: {e}")
                sys.exit(1)
        elif args.token_public_key:
            public_key_pem = args.token_public_key  # Inline PEM

        # Validation: Conflicting options
        if jwks_uri and (algorithm or secret_or_key):
            logger.warning(
                "JWKS mode ignores --token-algorithm and --token-secret/--token-public-key"
            )

        # HMAC mode
        if algorithm and algorithm.startswith("HS"):
            if not secret_or_key:
                logger.error(f"HMAC algorithm {algorithm} requires --token-secret")
                sys.exit(1)
            if jwks_uri:
                logger.error("Cannot use --token-jwks-uri with HMAC")
                sys.exit(1)
            public_key = secret_or_key
        else:
            public_key = public_key_pem

        # Required scopes
        required_scopes = None
        if args.required_scopes:
            required_scopes = [
                s.strip() for s in args.required_scopes.split(",") if s.strip()
            ]

        try:
            auth = JWTVerifier(
                jwks_uri=jwks_uri,
                public_key=public_key,
                issuer=issuer,
                audience=audience,
                algorithm=(
                    algorithm if algorithm and algorithm.startswith("HS") else None
                ),
                required_scopes=required_scopes,
            )
            logger.info(
                "JWTVerifier configured",
                extra={
                    "mode": (
                        "JWKS"
                        if jwks_uri
                        else (
                            "HMAC"
                            if algorithm and algorithm.startswith("HS")
                            else "Static Key"
                        )
                    ),
                    "algorithm": algorithm,
                    "required_scopes": required_scopes,
                },
            )
        except Exception as e:
            print(f"Failed to initialize JWTVerifier: {e}")
            logger.error(f"Failed to initialize JWTVerifier: {e}")
            sys.exit(1)
    elif args.auth_type == "oauth-proxy":
        if not (
            args.oauth_upstream_auth_endpoint
            and args.oauth_upstream_token_endpoint
            and args.oauth_upstream_client_id
            and args.oauth_upstream_client_secret
            and args.oauth_base_url
            and args.token_jwks_uri
            and args.token_issuer
            and args.token_audience
        ):
            print(
                "oauth-proxy requires oauth-upstream-auth-endpoint, oauth-upstream-token-endpoint, "
                "oauth-upstream-client-id, oauth-upstream-client-secret, oauth-base-url, token-jwks-uri, "
                "token-issuer, token-audience"
            )
            logger.error(
                "oauth-proxy requires oauth-upstream-auth-endpoint, oauth-upstream-token-endpoint, "
                "oauth-upstream-client-id, oauth-upstream-client-secret, oauth-base-url, token-jwks-uri, "
                "token-issuer, token-audience",
                extra={
                    "auth_endpoint": args.oauth_upstream_auth_endpoint,
                    "token_endpoint": args.oauth_upstream_token_endpoint,
                    "client_id": args.oauth_upstream_client_id,
                    "base_url": args.oauth_base_url,
                    "jwks_uri": args.token_jwks_uri,
                    "issuer": args.token_issuer,
                    "audience": args.token_audience,
                },
            )
            sys.exit(1)
        token_verifier = JWTVerifier(
            jwks_uri=args.token_jwks_uri,
            issuer=args.token_issuer,
            audience=args.token_audience,
        )
        auth = OAuthProxy(
            upstream_authorization_endpoint=args.oauth_upstream_auth_endpoint,
            upstream_token_endpoint=args.oauth_upstream_token_endpoint,
            upstream_client_id=args.oauth_upstream_client_id,
            upstream_client_secret=args.oauth_upstream_client_secret,
            token_verifier=token_verifier,
            base_url=args.oauth_base_url,
            allowed_client_redirect_uris=allowed_uris,
        )
    elif args.auth_type == "oidc-proxy":
        if not (
            args.oidc_config_url
            and args.oidc_client_id
            and args.oidc_client_secret
            and args.oidc_base_url
        ):
            logger.error(
                "oidc-proxy requires oidc-config-url, oidc-client-id, oidc-client-secret, oidc-base-url",
                extra={
                    "config_url": args.oidc_config_url,
                    "client_id": args.oidc_client_id,
                    "base_url": args.oidc_base_url,
                },
            )
            sys.exit(1)
        auth = OIDCProxy(
            config_url=args.oidc_config_url,
            client_id=args.oidc_client_id,
            client_secret=args.oidc_client_secret,
            base_url=args.oidc_base_url,
            allowed_client_redirect_uris=allowed_uris,
        )
    elif args.auth_type == "remote-oauth":
        if not (
            args.remote_auth_servers
            and args.remote_base_url
            and args.token_jwks_uri
            and args.token_issuer
            and args.token_audience
        ):
            logger.error(
                "remote-oauth requires remote-auth-servers, remote-base-url, token-jwks-uri, token-issuer, token-audience",
                extra={
                    "auth_servers": args.remote_auth_servers,
                    "base_url": args.remote_base_url,
                    "jwks_uri": args.token_jwks_uri,
                    "issuer": args.token_issuer,
                    "audience": args.token_audience,
                },
            )
            sys.exit(1)
        auth_servers = [url.strip() for url in args.remote_auth_servers.split(",")]
        token_verifier = JWTVerifier(
            jwks_uri=args.token_jwks_uri,
            issuer=args.token_issuer,
            audience=args.token_audience,
        )
        auth = RemoteAuthProvider(
            token_verifier=token_verifier,
            authorization_servers=auth_servers,
            base_url=args.remote_base_url,
        )

    # === 2. Build Middleware List ===
    middlewares: List[
        Union[
            UserTokenMiddleware,
            ErrorHandlingMiddleware,
            RateLimitingMiddleware,
            TimingMiddleware,
            LoggingMiddleware,
            JWTClaimsLoggingMiddleware,
            EunomiaMcpMiddleware,
        ]
    ] = [
        ErrorHandlingMiddleware(include_traceback=True, transform_errors=True),
        RateLimitingMiddleware(max_requests_per_second=10.0, burst_capacity=20),
        TimingMiddleware(),
        LoggingMiddleware(),
        JWTClaimsLoggingMiddleware(),
    ]
    if config["enable_delegation"] or args.auth_type == "jwt":
        middlewares.insert(0, UserTokenMiddleware(config=config))

    if args.eunomia_type in ["embedded", "remote"]:
        try:
            from eunomia_mcp import create_eunomia_middleware

            policy_file = args.eunomia_policy_file or "mcp_policies.json"
            eunomia_endpoint = (
                args.eunomia_remote_url if args.eunomia_type == "remote" else None
            )
            eunomia_mw = create_eunomia_middleware(
                policy_file=policy_file, eunomia_endpoint=eunomia_endpoint
            )
            middlewares.append(eunomia_mw)
            logger.info(f"Eunomia middleware enabled ({args.eunomia_type})")
        except Exception as e:
            print(f"Failed to load Eunomia middleware: {e}")
            logger.error("Failed to load Eunomia middleware", extra={"error": str(e)})
            sys.exit(1)

    mcp = FastMCP("AnsibleTower", auth=auth)
    register_tools(mcp)
    register_prompts(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)

    print(f"Ansible Tower MCP v{__version__}")
    print("\nStarting Ansible Tower MCP Server")
    print(f"  Transport: {args.transport.upper()}")
    print(f"  Auth: {args.auth_type}")
    print(f"  Delegation: {'ON' if config['enable_delegation'] else 'OFF'}")
    print(f"  Eunomia: {args.eunomia_type}")

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
    ansible_tower_mcp()
