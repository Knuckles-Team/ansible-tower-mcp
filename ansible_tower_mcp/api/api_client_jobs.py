#!/usr/bin/env python
import json
from typing import Any
from urllib.parse import urljoin

from ansible_tower_mcp.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def list_jobs(
        self, status: str | None = None, page_size: int = 100
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"page_size": page_size}
        if status:
            params["status"] = status
        return self.handle_pagination("/api/v2/jobs/", params)

    def get_job(self, job_id: int) -> dict[str, Any]:
        return self.request("GET", f"/api/v2/jobs/{job_id}/")

    def cancel_job(self, job_id: int) -> dict[str, Any]:
        return self.request("POST", f"/api/v2/jobs/{job_id}/cancel/")

    def get_job_events(self, job_id: int, page_size: int = 100) -> list[dict[str, Any]]:
        params = {"page_size": page_size}
        return self.handle_pagination(f"/api/v2/jobs/{job_id}/job_events/", params)

    def get_job_stdout(self, job_id: int, format: str = "txt") -> dict[str, Any]:
        if format not in ["txt", "html", "json", "ansi"]:
            raise ValueError("Invalid format")
        url = f"/api/v2/jobs/{job_id}/stdout/?format={format}"
        if format == "json":
            return self.request("GET", url)
        else:
            response = self._session.get(
                urljoin(self.base_url, url), headers=self.get_headers()
            )
            response.raise_for_status()
            return {"status": "success", "stdout": response.text}

    def launch_job(
        self, template_id: int, extra_vars: str | None = None
    ) -> dict[str, Any]:
        if extra_vars:
            try:
                json.loads(extra_vars)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON") from None
        data: dict[str, Any] = {}
        if extra_vars:
            data["extra_vars"] = extra_vars
        return self.request(
            "POST", f"/api/v2/job_templates/{template_id}/launch/", data=data
        )

    def run_ad_hoc_command(
        self,
        inventory_id: int,
        credential_id: int,
        module_name: str,
        module_args: str,
        limit: str = "",
        verbosity: int = 0,
    ) -> dict[str, Any]:
        if verbosity not in range(5):
            raise ValueError("Verbosity must be between 0 and 4")
        data = {
            "inventory": inventory_id,
            "credential": credential_id,
            "module_name": module_name,
            "module_args": module_args,
            "verbosity": verbosity,
        }
        if limit:
            data["limit"] = limit
        return self.request("POST", "/api/v2/ad_hoc_commands/", data=data)

    def get_ad_hoc_command(self, command_id: int) -> dict[str, Any]:
        return self.request("GET", f"/api/v2/ad_hoc_commands/{command_id}/")

    def cancel_ad_hoc_command(self, command_id: int) -> dict[str, Any]:
        try:
            return self.request("POST", f"/api/v2/ad_hoc_commands/{command_id}/cancel/")
        except Exception as e:
            try:
                response = self.get_ad_hoc_command(command_id)
                status = response.get("status")
                if status in ["pending", "waiting", "running"]:
                    self.request("DELETE", f"/api/v2/ad_hoc_commands/{command_id}/")
                    return {
                        "status": "success",
                        "message": f"Ad hoc command {command_id} cancelled via DELETE",
                    }
                else:
                    raise ValueError(f"Cannot cancel command in status: {status}")
            except Exception as inner_e:
                raise Exception(
                    f"Failed both cancel methods: {e}, then: {inner_e}"
                ) from None

    def launch_workflow(
        self, template_id: int, extra_vars: str | None = None
    ) -> dict[str, Any]:
        if extra_vars:
            try:
                json.loads(extra_vars)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON") from None
        data: dict[str, Any] = {}
        if extra_vars:
            data["extra_vars"] = extra_vars
        return self.request(
            "POST", f"/api/v2/workflow_job_templates/{template_id}/launch/", data=data
        )

    def list_workflow_jobs(
        self, status: str | None = None, page_size: int = 100
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"page_size": page_size}
        if status:
            params["status"] = status
        return self.handle_pagination("/api/v2/workflow_jobs/", params)

    def get_workflow_job(self, job_id: int) -> dict[str, Any]:
        return self.request("GET", f"/api/v2/workflow_jobs/{job_id}/")

    def cancel_workflow_job(self, job_id: int) -> dict[str, Any]:
        return self.request("POST", f"/api/v2/workflow_jobs/{job_id}/cancel/")
