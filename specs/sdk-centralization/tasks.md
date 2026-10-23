# CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION — Implementation tasks

Governing specification: [spec.md](spec.md).

- [ ] `CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R001` — Governed HTTP. `tests/test_sdk_centralization.py::test_api_client_uses_sdk_http_client` must observe an SDK client and no `requests` import.
- [ ] `CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R002` — Shared pagination. `tests/test_sdk_centralization.py::test_pagination_rejects_cross_origin_cursor` must reject a cursor that leaves the API origin.
- [x] `CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R002` — Replace the page loop with the SDK `PaginationIterator` in `next_url` mode and bind the follow, origin, and loop tests.
