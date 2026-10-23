"""CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R001 and R002."""

from pathlib import Path

import httpx
import pytest
from agent_connector_sdk.http.errors import HttpProblemError

from ansible_tower_mcp.api.api_client_base import BaseApiClient


def test_api_client_uses_sdk_http_client():
    client = BaseApiClient(base_url="https://tower.example", token="t")
    assert isinstance(client._session, httpx.Client)
    root = Path(__file__).resolve().parents[1] / "ansible_tower_mcp"
    for source in root.rglob("*.py"):
        text = source.read_text()
        assert "import requests" not in text, source


def test_pagination_rejects_cross_origin_cursor(monkeypatch):
    client = BaseApiClient(base_url="https://tower.example", token="t")
    pages = iter(
        [{"results": [{"id": 1}], "next": "https://evil.example/api/v2/x/?page=2"}]
    )
    monkeypatch.setattr(client, "request", lambda *a, **k: next(pages))
    with pytest.raises(HttpProblemError):
        client.handle_pagination("/api/v2/jobs/")
