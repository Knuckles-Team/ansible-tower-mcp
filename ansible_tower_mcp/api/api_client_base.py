#!/usr/bin/env python
import json
import logging
import re
from typing import Any
from urllib.parse import urljoin

import requests
from agent_utilities.core.transport_security import (
    ResolvedTLSProfile,
    resolve_tls_profile,
)

logger = logging.getLogger(__name__)


class BaseApiClient:
    def __init__(
        self,
        base_url: str | None,
        username: str | None = None,
        password: str | None = None,
        token: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        tls_profile: ResolvedTLSProfile | None = None,
    ):
        if not base_url:
            raise ValueError("base_url is required")
        self.base_url = base_url
        self.username = username
        self.password = password
        self.token = token
        self.client_id = client_id
        self.client_secret = client_secret
        self._session = requests.Session()
        self.tls_profile = tls_profile or resolve_tls_profile("ANSIBLE_TOWER")
        self.tls_profile.configure_requests_session(self._session)

        if (
            not token
            and not (client_id and client_secret)
            and not (username and password)
        ):
            raise ValueError(
                "Must provide either a token, or (username and password), "
                "or (client_id and client_secret) for authentication."
            )

    def _authenticate_oauth(self) -> None:
        """Authenticate using OAuth 2.0."""
        auth_url = urljoin(self.base_url, "/api/o/token/")
        grant_type = (
            "password" if self.username and self.password else "client_credentials"
        )
        payload = {
            "grant_type": grant_type,
            "username": self.username,
            "password": self.password,
            "scope": "write",
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = self._session.post(
            url=auth_url,
            data=payload,
            headers=headers,
            auth=(str(self.client_id), str(self.client_secret)),
        )

        if response.status_code != 200:
            raise Exception(
                f"OAuth authentication failed with HTTP {response.status_code}"
            )

        token_info = response.json()
        self.token = token_info.get("access_token")
        if not self.token:
            raise Exception("No access_token received from OAuth response")

    def get_token(self) -> str:
        """Authenticate and get token using web session approach."""
        login_page = self._session.get(f"{self.base_url}/api/login/")

        csrf_token = None
        if "csrftoken" in login_page.cookies:
            csrf_token = login_page.cookies["csrftoken"]
        else:
            match = re.search(
                r'name="csrfmiddlewaretoken" value="([^"]+)"', login_page.text
            )
            if match:
                csrf_token = match.group(1)

        if not csrf_token:
            raise Exception("Could not obtain CSRF token")

        headers = {"Referer": f"{self.base_url}/api/login/", "X-CSRFToken": csrf_token}

        login_data = {
            "username": self.username,
            "password": self.password,
            "next": "/api/v2/",
        }

        login_response = self._session.post(
            f"{self.base_url}/api/login/", data=login_data, headers=headers
        )

        if login_response.status_code >= 400:
            raise Exception(f"Login failed with HTTP {login_response.status_code}")

        token_headers = {
            "Content-Type": "application/json",
            "Referer": f"{self.base_url}/api/v2/",
        }

        if "csrftoken" in self._session.cookies:
            token_headers["X-CSRFToken"] = str(self._session.cookies["csrftoken"])

        token_data = {
            "description": "MCP Server Token",
            "application": None,
            "scope": "write",
        }

        token_response = self._session.post(
            f"{self.base_url}/api/v2/tokens/", json=token_data, headers=token_headers
        )

        if token_response.status_code == 201:
            token_data = token_response.json()
            self.token = token_data.get("token")
            return str(self.token)
        else:
            raise Exception(
                f"Token creation failed: {token_response.status_code} - "
                f"{token_response.text}"
            )

    def get_headers(self) -> dict[str, str]:
        """Get request headers with authorization."""
        if not self.token:
            if self.client_id and self.client_secret:
                self._authenticate_oauth()
            elif self.username and self.password:
                self.get_token()

        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        data: Any | None = None,
    ) -> dict[str, Any]:
        """Make a request to the Ansible API."""
        if endpoint.startswith("http"):
            url = endpoint
        else:
            url = urljoin(self.base_url, endpoint)

        headers = self.get_headers()

        response = self._session.request(
            method=method, url=url, headers=headers, params=params, json=data
        )

        if response.status_code >= 400:
            error_message = f"Ansible API error: {response.status_code}"
            raise Exception(error_message)

        if response.status_code == 204:
            return {"status": "success"}

        if not response.text.strip():
            return {"status": "success", "message": "Empty response"}

        try:
            return response.json()
        except json.JSONDecodeError:
            return {
                "status": "success",
                "content_type": response.headers.get("Content-Type", "unknown"),
                "text": response.text[:1000],
            }

    def handle_pagination(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Handle paginated results from Ansible API."""
        results = []
        next_url: str | None = urljoin(self.base_url, endpoint)
        first_request = True

        while next_url:
            if first_request:
                response = self.request("GET", str(next_url), params=params)
                first_request = False
            else:
                response = self.request("GET", str(next_url))
            if "results" in response:
                results.extend(response["results"])
                next_url = response.get("next")
            else:
                break
        return results
