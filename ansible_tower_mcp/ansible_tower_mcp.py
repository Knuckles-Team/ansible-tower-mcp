#!/usr/bin/env python
# coding: utf-8

"""
Ansible MCP Server

This server provides tools for interacting with the Ansible API through the Model Context Protocol.
"""

import os
import sys
import argparse
import logging
from typing import Optional, List, Dict
from pydantic import Field
from fastmcp import FastMCP
from .ansible_tower_api import Api

mcp = FastMCP("ansible")


def to_boolean(string):
    # Normalize the string: strip whitespace and convert to lowercase
    normalized = str(string).strip().lower()

    # Define valid true/false values
    true_values = {"t", "true", "y", "yes", "1"}
    false_values = {"f", "false", "n", "no", "0"}

    if normalized in true_values:
        return True
    elif normalized in false_values:
        return False
    else:
        raise ValueError(f"Cannot convert '{string}' to boolean")


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
def list_inventories(
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
def get_inventory(
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
def create_inventory(
    name: str = Field(description="Name of the inventory"),
    organization_id: int = Field(description="ID of the organization"),
    description: str = Field(default="", description="Description of the inventory"),
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
def update_inventory(
    inventory_id: int = Field(description="ID of the inventory"),
    name: Optional[str] = Field(default=None, description="New name for the inventory"),
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
) -> Dict:
    """
    Updates an existing inventory in Ansible Tower. Returns a dictionary with the updated inventory's details.
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
def delete_inventory(
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
    Deletes a specific inventory by ID from Ansible Tower. Returns a dictionary confirming the deletion status.
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
def list_hosts(
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
def get_host(
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
def create_host(
    name: str = Field(description="Name or IP address of the host"),
    inventory_id: int = Field(description="ID of the inventory to add the host to"),
    variables: str = Field(default="{}", description="JSON string of host variables"),
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
def update_host(
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
) -> Dict:
    """
    Updates an existing host in Ansible Tower. Returns a dictionary with the updated host's details.
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
def delete_host(
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
    Deletes a specific host by ID from Ansible Tower. Returns a dictionary confirming the deletion status.
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
def list_groups(
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
def get_group(
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
def create_group(
    name: str = Field(description="Name of the group"),
    inventory_id: int = Field(description="ID of the inventory to add the group to"),
    variables: str = Field(default="{}", description="JSON string of group variables"),
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
def update_group(
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
def delete_group(
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
def add_host_to_group(
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
def remove_host_from_group(
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
def list_job_templates(
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
def get_job_template(
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
def create_job_template(
    name: str = Field(description="Name of the job template"),
    inventory_id: int = Field(description="ID of the inventory"),
    project_id: int = Field(description="ID of the project"),
    playbook: str = Field(description="Name of the playbook (e.g., 'playbook.yml')"),
    credential_id: Optional[int] = Field(
        default=None, description="Optional ID of the credential"
    ),
    description: str = Field(default="", description="Description of the job template"),
    extra_vars: str = Field(default="{}", description="JSON string of extra variables"),
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
def update_job_template(
    template_id: int = Field(description="ID of the job template"),
    name: Optional[str] = Field(
        default=None, description="New name for the job template"
    ),
    inventory_id: Optional[int] = Field(default=None, description="New inventory ID"),
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
) -> Dict:
    """
    Updates an existing job template in Ansible Tower. Returns a dictionary with the updated template's details.
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
def delete_job_template(
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
    Deletes a specific job template by ID from Ansible Tower. Returns a dictionary confirming the deletion status.
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
def launch_job(
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
) -> Dict:
    """
    Launches a job from a template in Ansible Tower, optionally with extra variables. Returns a dictionary with the launched job's details, including its ID.
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
def list_jobs(
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
def get_job(
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
def cancel_job(
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
    Cancels a running job in Ansible Tower. Returns a dictionary confirming the cancellation status.
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
def get_job_events(
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
def get_job_stdout(
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
def list_projects(
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
def get_project(
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
def create_project(
    name: str = Field(description="Name of the project"),
    organization_id: int = Field(description="ID of the organization"),
    scm_type: str = Field(description="SCM type (git, hg, svn, manual)"),
    scm_url: Optional[str] = Field(default=None, description="URL for the repository"),
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
def update_project(
    project_id: int = Field(description="ID of the project"),
    name: Optional[str] = Field(default=None, description="New name for the project"),
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
def delete_project(
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
def sync_project(
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
def list_credentials(
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
def get_credential(
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
def list_credential_types(
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
def create_credential(
    name: str = Field(description="Name of the credential"),
    credential_type_id: int = Field(description="ID of the credential type"),
    organization_id: int = Field(description="ID of the organization"),
    inputs: str = Field(
        description="JSON string of credential inputs (e.g., username, password)"
    ),
    description: str = Field(default="", description="Description of the credential"),
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
def update_credential(
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
        credential_id=credential_id, name=name, inputs=inputs, description=description
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
def delete_credential(
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
def list_organizations(
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
def get_organization(
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
def create_organization(
    name: str = Field(description="Name of the organization"),
    description: str = Field(default="", description="Description of the organization"),
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
def update_organization(
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
def delete_organization(
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
def list_teams(
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
def get_team(
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
def create_team(
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
def update_team(
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
def delete_team(
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
def list_users(
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
def get_user(
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
def create_user(
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
def update_user(
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
def delete_user(
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
def run_ad_hoc_command(
    inventory_id: int = Field(description="ID of the inventory"),
    credential_id: int = Field(description="ID of the credential"),
    module_name: str = Field(description="Module name (e.g., command, shell, ping)"),
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
def get_ad_hoc_command(
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
def cancel_ad_hoc_command(
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
def list_workflow_templates(
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
def get_workflow_template(
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
def launch_workflow(
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
def list_workflow_jobs(
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
def get_workflow_job(
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
def cancel_workflow_job(
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
def list_schedules(
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
def get_schedule(
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
def create_schedule(
    name: str = Field(description="Name of the schedule"),
    unified_job_template_id: int = Field(
        description="ID of the job or workflow template"
    ),
    rrule: str = Field(
        description="iCal recurrence rule (e.g., 'DTSTART:20231001T120000Z RRULE:FREQ=DAILY;INTERVAL=1')"
    ),
    description: str = Field(default="", description="Description of the schedule"),
    extra_data: str = Field(default="{}", description="JSON string of extra variables"),
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
def update_schedule(
    schedule_id: int = Field(description="ID of the schedule"),
    name: Optional[str] = Field(default=None, description="New name for the schedule"),
    rrule: Optional[str] = Field(default=None, description="New iCal recurrence rule"),
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
def delete_schedule(
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
def get_ansible_version(
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
def get_dashboard_stats(
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
def get_metrics(
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


def ansible_tower_mcp():
    parser = argparse.ArgumentParser(description="Ansible Tower MCP")

    parser.add_argument(
        "-t",
        "--transport",
        default="stdio",
        choices=["stdio", "http", "sse"],
        help="Transport method: 'stdio', 'http', or 'sse' [legacy] (default: stdio)",
    )
    parser.add_argument(
        "-s",
        "--host",
        default="0.0.0.0",
        help="Host address for HTTP transport (default: 0.0.0.0)",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Port number for HTTP transport (default: 8000)",
    )

    args = parser.parse_args()

    if args.port < 0 or args.port > 65535:
        print(f"Error: Port {args.port} is out of valid range (0-65535).")
        sys.exit(1)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "http":
        mcp.run(transport="http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger = logging.getLogger("AnsibleMCP")
        logger.error("Transport not supported")
        sys.exit(1)


if __name__ == "__main__":
    ansible_tower_mcp()
