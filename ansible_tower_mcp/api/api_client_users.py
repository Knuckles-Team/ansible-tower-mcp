#!/usr/bin/env python
from typing import Any

from ansible_tower_mcp.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def list_users(self, page_size: int = 100) -> list[dict[str, Any]]:
        params = {"page_size": page_size}
        return self.handle_pagination("/api/v2/users/", params)

    def get_user(self, user_id: int) -> dict[str, Any]:
        return self.request("GET", f"/api/v2/users/{user_id}/")

    def create_user(
        self,
        username: str,
        password: str,
        first_name: str = "",
        last_name: str = "",
        email: str = "",
        is_superuser: bool = False,
        is_system_auditor: bool = False,
    ) -> dict[str, Any]:
        data = {
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "is_superuser": is_superuser,
            "is_system_auditor": is_system_auditor,
        }
        return self.request("POST", "/api/v2/users/", data=data)

    def update_user(
        self,
        user_id: int,
        username: str | None = None,
        password: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        is_superuser: bool | None = None,
        is_system_auditor: bool | None = None,
    ) -> dict[str, Any]:
        data: dict[str, Any] = {}
        if username:
            data["username"] = username
        if password:
            data["password"] = password
        if first_name is not None:
            data["first_name"] = first_name
        if last_name is not None:
            data["last_name"] = last_name
        if email:
            data["email"] = email
        if is_superuser is not None:
            data["is_superuser"] = is_superuser
        if is_system_auditor is not None:
            data["is_system_auditor"] = is_system_auditor
        return self.request("PATCH", f"/api/v2/users/{user_id}/", data=data)

    def delete_user(self, user_id: int) -> dict[str, Any]:
        self.request("DELETE", f"/api/v2/users/{user_id}/")
        return {"status": "success", "message": f"User {user_id} deleted"}
