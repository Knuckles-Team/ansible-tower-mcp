#!/usr/bin/env python
import json
from typing import Any

from ansible_tower_mcp.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def list_groups(
        self, inventory_id: int, page_size: int = 100
    ) -> list[dict[str, Any]]:
        params = {"page_size": page_size}
        return self.handle_pagination(
            f"/api/v2/inventories/{inventory_id}/groups/", params
        )

    def get_group(self, group_id: int) -> dict[str, Any]:
        return self.request("GET", f"/api/v2/groups/{group_id}/")

    def create_group(
        self,
        name: str,
        inventory_id: int,
        variables: str = "{}",
        description: str = "",
    ) -> dict[str, Any]:
        try:
            json.loads(variables)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON") from None
        data = {
            "name": name,
            "inventory": inventory_id,
            "variables": variables,
            "description": description,
        }
        return self.request("POST", "/api/v2/groups/", data=data)

    def update_group(
        self,
        group_id: int,
        name: str | None = None,
        variables: str | None = None,
        description: str | None = None,
    ) -> dict[str, Any]:
        if variables:
            try:
                json.loads(variables)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON") from None
        data: dict[str, Any] = {}
        if name:
            data["name"] = name
        if variables:
            data["variables"] = variables
        if description:
            data["description"] = description
        return self.request("PATCH", f"/api/v2/groups/{group_id}/", data=data)

    def delete_group(self, group_id: int) -> dict[str, Any]:
        self.request("DELETE", f"/api/v2/groups/{group_id}/")
        return {"status": "success", "message": f"Group {group_id} deleted"}

    def add_host_to_group(self, group_id: int, host_id: int) -> dict[str, Any]:
        data = {"id": host_id}
        return self.request("POST", f"/api/v2/groups/{group_id}/hosts/", data=data)

    def remove_host_from_group(self, group_id: int, host_id: int) -> dict[str, Any]:
        data = {"id": host_id, "disassociate": True}
        self.request("POST", f"/api/v2/groups/{group_id}/hosts/", data=data)
        return {
            "status": "success",
            "message": f"Host {host_id} removed from group {group_id}",
        }
