#!/usr/bin/env python
import json
from typing import Any

from ansible_tower_mcp.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def list_schedules(
        self, unified_job_template_id: int | None = None, page_size: int = 100
    ) -> list[dict[str, Any]]:
        params = {"page_size": page_size}
        if unified_job_template_id:
            params["unified_job_template"] = unified_job_template_id
        return self.handle_pagination("/api/v2/schedules/", params)

    def get_schedule(self, schedule_id: int) -> dict[str, Any]:
        return self.request("GET", f"/api/v2/schedules/{schedule_id}/")

    def create_schedule(
        self,
        name: str,
        rrule: str,
        unified_job_template_id: int,
        description: str = "",
        extra_data: str = "{}",
    ) -> dict[str, Any]:
        try:
            json.loads(extra_data)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON") from None
        data = {
            "name": name,
            "rrule": rrule,
            "unified_job_template": unified_job_template_id,
            "description": description,
            "extra_data": extra_data,
        }
        return self.request("POST", "/api/v2/schedules/", data=data)

    def update_schedule(
        self,
        schedule_id: int,
        name: str | None = None,
        rrule: str | None = None,
        description: str | None = None,
        extra_data: str | None = None,
    ) -> dict[str, Any]:
        if extra_data:
            try:
                json.loads(extra_data)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON") from None
        data: dict[str, Any] = {}
        if name:
            data["name"] = name
        if rrule:
            data["rrule"] = rrule
        if description:
            data["description"] = description
        if extra_data:
            data["extra_data"] = extra_data
        return self.request("PATCH", f"/api/v2/schedules/{schedule_id}/", data=data)

    def delete_schedule(self, schedule_id: int) -> dict[str, Any]:
        self.request("DELETE", f"/api/v2/schedules/{schedule_id}/")
        return {"status": "success", "message": f"Schedule {schedule_id} deleted"}
