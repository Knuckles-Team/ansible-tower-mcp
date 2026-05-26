#!/usr/bin/env python
import json
from typing import Any

from ansible_tower_mcp.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def list_credentials(self, page_size: int = 100) -> list[dict[str, Any]]:
        params = {"page_size": page_size}
        return self.handle_pagination("/api/v2/credentials/", params)

    def get_credential(self, credential_id: int) -> dict[str, Any]:
        return self.request("GET", f"/api/v2/credentials/{credential_id}/")

    def list_credential_types(self, page_size: int = 100) -> list[dict[str, Any]]:
        params = {"page_size": page_size}
        return self.handle_pagination("/api/v2/credential_types/", params)

    def create_credential(
        self,
        name: str,
        credential_type_id: int,
        organization_id: int,
        inputs: str,
        description: str = "",
    ) -> dict[str, Any]:
        try:
            inputs_dict = json.loads(inputs)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON") from None
        data = {
            "name": name,
            "credential_type": credential_type_id,
            "organization": organization_id,
            "inputs": inputs_dict,
            "description": description,
        }
        return self.request("POST", "/api/v2/credentials/", data=data)

    def update_credential(
        self,
        credential_id: int,
        name: str | None = None,
        inputs: str | None = None,
        description: str | None = None,
    ) -> dict[str, Any]:
        data: dict[str, Any] = {}
        if name:
            data["name"] = name
        if inputs:
            try:
                inputs_dict = json.loads(inputs)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON") from None
            data["inputs"] = inputs_dict
        if description:
            data["description"] = description
        return self.request("PATCH", f"/api/v2/credentials/{credential_id}/", data=data)

    def delete_credential(self, credential_id: int) -> dict[str, Any]:
        self.request("DELETE", f"/api/v2/credentials/{credential_id}/")
        return {"status": "success", "message": f"Credential {credential_id} deleted"}
