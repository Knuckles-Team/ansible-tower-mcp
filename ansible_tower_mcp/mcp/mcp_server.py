# ansible_tower_mcp/mcp/mcp_server.py
import warnings

from fastmcp.utilities.logging import get_logger

# FastMCP Server & Command-Line Interfaces

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
from starlette.requests import Request
from starlette.responses import JSONResponse

from ansible_tower_mcp.mcp import tools
from ansible_tower_mcp.mcp.tools import (
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

__version__ = "1.16.0"

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

logger = get_logger(name="ansible-tower-mcp")
logger.setLevel(logging.INFO)

def get_mcp_instance() -> tuple[Any, ...]:
    """Initialize and return the MCP instance.

    Bootstraps FastMCP instance, custom routes, and conditionally registers tools.
    """
    load_dotenv(find_dotenv())
    args, mcp, middlewares = create_mcp_server(
        name="ansible-tower-mcp MCP",
        version=__version__,
        instructions="ansible-tower-mcp MCP Server — Condensed Action-Routed Tools.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        """Standard Starlette endpoint for health status checking."""
        return JSONResponse({"status": "OK"})

    # Map environment variable toggles to registration functions
    tool_registrations = [
        ("INVENTORYTOOL", tools.register_inventory_tools),
        ("HOSTSTOOL", tools.register_hosts_tools),
        ("GROUPSTOOL", tools.register_groups_tools),
        ("JOB_TEMPLATESTOOL", tools.register_job_templates_tools),
        ("JOBSTOOL", tools.register_jobs_tools),
        ("PROJECTSTOOL", tools.register_projects_tools),
        ("CREDENTIALSTOOL", tools.register_credentials_tools),
        ("ORGANIZATIONSTOOL", tools.register_organizations_tools),
        ("TEAMSTOOL", tools.register_teams_tools),
        ("USERSTOOL", tools.register_users_tools),
        ("AD_HOC_COMMANDSTOOL", tools.register_ad_hoc_commands_tools),
        ("WORKFLOW_TEMPLATESTOOL", tools.register_workflow_templates_tools),
        ("WORKFLOW_JOBSTOOL", tools.register_workflow_jobs_tools),
        ("SCHEDULESTOOL", tools.register_schedules_tools),
        ("SYSTEMTOOL", tools.register_system_tools),
    ]

    # Modular iteration to register active tools with FastMCP (CC=2)
    for env_var, register_func in tool_registrations:
        if to_boolean(os.getenv(env_var, "True")):
            register_func(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)
    return mcp, args, middlewares

def mcp_server() -> None:
    """Run the MCP server application.

    Configures transport mechanisms and executes the FastMCP runner.
    """
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