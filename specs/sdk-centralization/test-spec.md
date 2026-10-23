# CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION — Verification plan

Governing specification: [spec.md](spec.md).

| Requirement | Verification target |
|---|---|
| `CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R001` | `tests/test_sdk_centralization.py::test_api_client_uses_sdk_http_client` must observe an SDK client and no `requests` import. |
| `CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R002` | `tests/test_sdk_centralization.py::test_pagination_rejects_cross_origin_cursor` must reject a cursor that leaves the API origin. |
