"""CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R001 and R002."""

from __future__ import annotations

from pathlib import Path

import httpx
import pytest
from agent_connector_sdk.http.errors import HttpProblemError
from agent_connector_sdk.httpsupport.pagination import PaginationOriginError

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


def _paged_client(monkeypatch, pages: dict[str, dict]) -> tuple[BaseApiClient, list]:
    client = BaseApiClient(base_url="https://tower.example", token="t")
    calls: list[tuple[str, dict | None]] = []

    def request(method, url, params=None, data=None):
        calls.append((url, params))
        return pages[url]

    monkeypatch.setattr(client, "request", request)
    return client, calls


def test_pagination_follows_relative_and_absolute_next(monkeypatch):
    first = "https://tower.example/api/v2/hosts/"
    second = "https://tower.example/api/v2/hosts/?page=2"
    third = "https://tower.example/api/v2/hosts/?page=3"
    client, calls = _paged_client(
        monkeypatch,
        {
            first: {"results": [{"id": 1}], "next": "/api/v2/hosts/?page=2"},
            second: {"results": [{"id": 2}], "next": third},
            third: {"results": [{"id": 3}], "next": None},
        },
    )
    rows = client.handle_pagination("/api/v2/hosts/", params={"page_size": 1})
    assert rows == [{"id": 1}, {"id": 2}, {"id": 3}]
    assert calls == [(first, {"page_size": 1}), (second, None), (third, None)]


@pytest.mark.parametrize(
    "next_url",
    [
        "https://evil.example/api/v2/hosts/?page=2",
        "http://tower.example/api/v2/hosts/?page=2",
        "https://tower.example:8443/api/v2/hosts/?page=2",
    ],
)
def test_pagination_rejects_origin_change(monkeypatch, next_url):
    first = "https://tower.example/api/v2/hosts/"
    client, calls = _paged_client(
        monkeypatch, {first: {"results": [{"id": 1}], "next": next_url}}
    )
    with pytest.raises(PaginationOriginError):
        client.handle_pagination("/api/v2/hosts/")
    assert calls == [(first, None)]


def test_pagination_stops_on_a_repeated_next(monkeypatch):
    first = "https://tower.example/api/v2/hosts/"
    second = "https://tower.example/api/v2/hosts/?page=2"
    client, calls = _paged_client(
        monkeypatch,
        {
            first: {"results": [{"id": 1}], "next": "?page=2"},
            second: {"results": [{"id": 2}], "next": "/api/v2/hosts/?page=2"},
        },
    )
    assert client.handle_pagination("/api/v2/hosts/") == [{"id": 1}, {"id": 2}]
    assert len(calls) == 2
