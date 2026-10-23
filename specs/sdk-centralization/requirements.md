# CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION — Requirements

Governing specification: [spec.md](spec.md).

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R001` | **Governed HTTP.** The connector must reach Ansible Tower only through the SDK governed HTTP client in `ansible_tower_mcp/api/api_client_base.py`. It must not import `requests`. | `tests/test_sdk_centralization.py::test_api_client_uses_sdk_http_client` must observe an SDK client and no `requests` import. |
| `CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R002` | **Shared pagination.** The connector must validate every follow-up page cursor with the SDK pagination check in `ansible_tower_mcp/api/api_client_base.py`. | `tests/test_sdk_centralization.py::test_pagination_rejects_cross_origin_cursor` must reject a cursor that leaves the API origin. |
