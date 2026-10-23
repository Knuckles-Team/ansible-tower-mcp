# CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION — Verification plan

Governing specification: [spec.md](spec.md).

| Requirement | Verification target |
|---|---|
| `CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R001` | `tests/test_sdk_centralization.py::test_api_client_uses_sdk_http_client` must observe an SDK client and no `requests` import. |
| `CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R002` | `tests/test_sdk_centralization.py::test_pagination_rejects_cross_origin_cursor` must reject a cursor that leaves the API origin. `test_pagination_follows_relative_and_absolute_next` must fetch three pages and send the base query only on the first. `test_pagination_rejects_origin_change` must raise `PaginationOriginError` for a host, scheme, or port change. `test_pagination_stops_on_a_repeated_next` must stop after two pages. |
