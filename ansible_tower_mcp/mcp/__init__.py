# ansible_tower_mcp/mcp/__init__.py
from typing import Any


def __getattr__(name: str) -> Any:
    if name in ("get_mcp_instance", "mcp_server"):
        from ansible_tower_mcp.mcp.mcp_server import get_mcp_instance, mcp_server

        if name == "get_mcp_instance":
            return get_mcp_instance
        return mcp_server
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["get_mcp_instance", "mcp_server"]
