#!/usr/bin/env python
from typing import Any

from ansible_tower_mcp.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def list_teams(
        self, organization_id: int | None = None, page_size: int = 100
    ) -> list[dict[str, Any]]:
        params = {"page_size": page_size}
        if organization_id:
            endpoint = f"/api/v2/organizations/{organization_id}/teams/"
        else:
            endpoint = "/api/v2/teams/"
        return self.handle_pagination(endpoint, params)

    def get_team(self, team_id: int) -> dict[str, Any]:
        return self.request("GET", f"/api/v2/teams/{team_id}/")

    def create_team(
        self, name: str, organization_id: int, description: str = ""
    ) -> dict[str, Any]:
        data = {
            "name": name,
            "organization": organization_id,
            "description": description,
        }
        return self.request("POST", "/api/v2/teams/", data=data)

    def update_team(
        self, team_id: int, name: str | None = None, description: str | None = None
    ) -> dict[str, Any]:
        data: dict[str, Any] = {}
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        return self.request("PATCH", f"/api/v2/teams/{team_id}/", data=data)

    def delete_team(self, team_id: int) -> dict[str, Any]:
        self.request("DELETE", f"/api/v2/teams/{team_id}/")
        return {"status": "success", "message": f"Team {team_id} deleted"}
