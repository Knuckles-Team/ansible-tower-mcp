# CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION — Requirements

Governing specification: [spec.md](spec.md).

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R001` | **Governed HTTP.** The connector must reach Ansible Tower only through the SDK governed HTTP client in `ansible_tower_mcp/api/api_client_base.py`. It must not import `requests`. | `tests/test_sdk_centralization.py::test_api_client_uses_sdk_http_client` must observe an SDK client and no `requests` import. |
| `CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R002` | **Shared pagination.** `handle_pagination` in `ansible_tower_mcp/api/api_client_base.py` must walk list pages with the SDK `PaginationIterator` in `next_url` mode (SDK `SDK-CENTRALIZED-CAPABILITIES-R004`). It reads the body `next` link and records from `results`. The connector must ship no page loop of its own. A `next` link that changes the scheme, host, or port must raise `PaginationOriginError` before the client requests it. A repeated `next` link must end the sweep. | `tests/test_sdk_centralization.py::test_pagination_rejects_cross_origin_cursor`, `test_pagination_follows_relative_and_absolute_next`, `test_pagination_rejects_origin_change`, and `test_pagination_stops_on_a_repeated_next` pass. |
