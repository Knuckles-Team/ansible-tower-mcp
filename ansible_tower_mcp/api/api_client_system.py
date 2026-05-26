#!/usr/bin/env python
from typing import Any

from ansible_tower_mcp.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def get_ansible_version(self) -> dict[str, Any]:
        return self.request("GET", "/api/v2/config/")

    def get_dashboard_stats(self) -> dict[str, Any]:
        return self.request("GET", "/api/v2/dashboard/")

    def get_metrics(self) -> dict[str, Any]:
        return self.request("GET", "/api/metrics/")
