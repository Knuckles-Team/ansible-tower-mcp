#!/usr/bin/env python
from typing import Any

from ansible_tower_mcp.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def list_inventories(self, page_size: int = 100) -> list[dict[str, Any]]:
        params = {"page_size": page_size}
        return self.handle_pagination("/api/v2/inventories/", params)

    def get_inventory(self, inventory_id: int) -> dict[str, Any]:
        return self.request("GET", f"/api/v2/inventories/{inventory_id}/")

    def create_inventory(
        self, name: str, organization_id: int, description: str = ""
    ) -> dict[str, Any]:
        data = {
            "name": name,
            "description": description,
            "organization": organization_id,
        }
        return self.request("POST", "/api/v2/inventories/", data=data)

    def update_inventory(
        self,
        inventory_id: int,
        name: str | None = None,
        description: str | None = None,
    ) -> dict[str, Any]:
        data: dict[str, Any] = {}
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        return self.request("PATCH", f"/api/v2/inventories/{inventory_id}/", data=data)

    def delete_inventory(self, inventory_id: int) -> dict[str, Any]:
        self.request("DELETE", f"/api/v2/inventories/{inventory_id}/")
        return {"status": "success", "message": f"Inventory {inventory_id} deleted"}
