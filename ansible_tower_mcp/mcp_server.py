from scion_sdk.connector_identity import connector_version

# Thin delegation wrapper for backward compatibility with external scripts, pyproject.toml scripts, and eager imports.
__version__ = connector_version("ansible_tower_mcp")

from ansible_tower_mcp.mcp.mcp_server import (
    get_mcp_instance,
    mcp_server,
    register_kg_ingest_tools,
)

__all__ = [
    "__version__",
    "get_mcp_instance",
    "mcp_server",
    "register_kg_ingest_tools",
]

if __name__ == "__main__":
    mcp_server()
