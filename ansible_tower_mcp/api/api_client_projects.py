#!/usr/bin/env python
from typing import Any

from ansible_tower_mcp.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def list_projects(self, page_size: int = 100) -> list[dict[str, Any]]:
        params = {"page_size": page_size}
        return self.handle_pagination("/api/v2/projects/", params)

    def get_project(self, project_id: int) -> dict[str, Any]:
        return self.request("GET", f"/api/v2/projects/{project_id}/")

    def create_project(
        self,
        name: str,
        organization_id: int,
        scm_type: str,
        scm_url: str | None = None,
        scm_branch: str | None = None,
        credential_id: int | None = None,
        description: str = "",
    ) -> dict[str, Any]:
        if scm_type not in ["", "git", "hg", "svn", "manual"]:
            raise ValueError("Invalid SCM type. Must be one of: git, hg, svn, manual")
        if scm_type != "manual" and not scm_url:
            raise ValueError("SCM URL is required for non-manual SCM types")
        data: dict[str, Any] = {
            "name": name,
            "organization": organization_id,
            "scm_type": scm_type,
            "description": description,
        }
        if scm_url:
            data["scm_url"] = scm_url
        if scm_branch:
            data["scm_branch"] = scm_branch
        if credential_id:
            data["credential"] = credential_id
        return self.request("POST", "/api/v2/projects/", data=data)

    def update_project(
        self,
        project_id: int,
        name: str | None = None,
        scm_type: str | None = None,
        scm_url: str | None = None,
        scm_branch: str | None = None,
        description: str | None = None,
    ) -> dict[str, Any]:
        if scm_type and scm_type not in ["", "git", "hg", "svn", "manual"]:
            raise ValueError("Invalid SCM type. Must be one of: git, hg, svn, manual")
        data: dict[str, Any] = {}
        if name:
            data["name"] = name
        if scm_type:
            data["scm_type"] = scm_type
        if scm_url:
            data["scm_url"] = scm_url
        if scm_branch:
            data["scm_branch"] = scm_branch
        if description:
            data["description"] = description
        return self.request("PATCH", f"/api/v2/projects/{project_id}/", data=data)

    def delete_project(self, project_id: int) -> dict[str, Any]:
        self.request("DELETE", f"/api/v2/projects/{project_id}/")
        return {"status": "success", "message": f"Project {project_id} deleted"}

    def sync_project(self, project_id: int) -> dict[str, Any]:
        return self.request("POST", f"/api/v2/projects/{project_id}/update/")
