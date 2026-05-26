#!/usr/bin/env python
import json
from typing import Any

from ansible_tower_mcp.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def list_hosts(
        self, inventory_id: int | None = None, page_size: int = 100
    ) -> list[dict[str, Any]]:
        params = {"page_size": page_size}
        if inventory_id:
            endpoint = f"/api/v2/inventories/{inventory_id}/hosts/"
        else:
            endpoint = "/api/v2/hosts/"
        return self.handle_pagination(endpoint, params)

    def get_host(self, host_id: int) -> dict[str, Any]:
        return self.request("GET", f"/api/v2/hosts/{host_id}/")

    def create_host(
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
        return self.request("POST", "/api/v2/hosts/", data=data)

    def update_host(
        self,
        host_id: int,
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
        return self.request("PATCH", f"/api/v2/hosts/{host_id}/", data=data)

    def delete_host(self, host_id: int) -> dict[str, Any]:
        self.request("DELETE", f"/api/v2/hosts/{host_id}/")
        return {"status": "success", "message": f"Host {host_id} deleted"}
