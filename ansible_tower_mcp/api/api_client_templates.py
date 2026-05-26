#!/usr/bin/env python
import json
from typing import Any

from ansible_tower_mcp.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def list_job_templates(self, page_size: int = 100) -> list[dict[str, Any]]:
        params = {"page_size": page_size}
        return self.handle_pagination("/api/v2/job_templates/", params)

    def get_job_template(self, template_id: int) -> dict[str, Any]:
        return self.request("GET", f"/api/v2/job_templates/{template_id}/")

    def create_job_template(
        self,
        name: str,
        inventory_id: int,
        project_id: int,
        playbook: str,
        credential_id: int | None = None,
        description: str = "",
        extra_vars: str = "{}",
    ) -> dict[str, Any]:
        try:
            json.loads(extra_vars)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON") from None
        data: dict[str, Any] = {
            "name": name,
            "inventory": inventory_id,
            "project": project_id,
            "playbook": playbook,
            "description": description,
            "extra_vars": extra_vars,
            "job_type": "run",
            "verbosity": 0,
        }
        if credential_id:
            data["credential"] = credential_id
        return self.request("POST", "/api/v2/job_templates/", data=data)

    def update_job_template(
        self,
        template_id: int,
        name: str | None = None,
        inventory_id: int | None = None,
        playbook: str | None = None,
        description: str | None = None,
        extra_vars: str | None = None,
    ) -> dict[str, Any]:
        if extra_vars:
            try:
                json.loads(extra_vars)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON") from None
        data: dict[str, Any] = {}
        if name:
            data["name"] = name
        if inventory_id:
            data["inventory"] = inventory_id
        if playbook:
            data["playbook"] = playbook
        if description:
            data["description"] = description
        if extra_vars:
            data["extra_vars"] = extra_vars
        return self.request("PATCH", f"/api/v2/job_templates/{template_id}/", data=data)

    def delete_job_template(self, template_id: int) -> dict[str, Any]:
        self.request("DELETE", f"/api/v2/job_templates/{template_id}/")
        return {"status": "success", "message": f"Job template {template_id} deleted"}

    def list_workflow_templates(self, page_size: int = 100) -> list[dict[str, Any]]:
        params = {"page_size": page_size}
        return self.handle_pagination("/api/v2/workflow_job_templates/", params)

    def get_workflow_template(self, template_id: int) -> dict[str, Any]:
        return self.request("GET", f"/api/v2/workflow_job_templates/{template_id}/")
