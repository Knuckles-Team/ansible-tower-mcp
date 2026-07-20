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
import sys
from typing import Any

from agent_utilities.core.config import load_config
from agent_utilities.mcp.server_factory import create_mcp_server
from agent_utilities.mcp.verbose_tools import register_tool_surface
from starlette.requests import Request
from starlette.responses import JSONResponse

from ansible_tower_mcp.api_client import Api
from ansible_tower_mcp.auth import get_client
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
    load_config()
    args, mcp, middlewares = create_mcp_server(
        name="ansible-tower-mcp MCP",
        version=__version__,
        instructions="ansible-tower-mcp MCP Server — Condensed Action-Routed Tools.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        """Standard Starlette endpoint for health status checking."""
        return JSONResponse({"status": "OK"})

    register_tool_surface(
        mcp,
        client_cls=Api,
        get_client=get_client,
        service="ansible-tower-mcp",
        tools_module=tools,
    )

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
