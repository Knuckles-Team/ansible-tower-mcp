# CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION — Design and implementation plan

Governing specification: [spec.md](spec.md).

## Existing system and reuse

The connector reuses `scion_sdk.http.create_http_client` for all vendor requests.
The SDK retry policy replaces connector-local retry handling.

## Implementation units

- `ansible_tower_mcp/api/api_client_base.py`: builds the governed client from the runtime TLS profile.
- `ansible_tower_mcp/api/api_client_base.py`: `handle_pagination` drives the SDK `PaginationIterator` in `next_url` mode. A sweep stops after 10,000 pages or 1,000,000 records.

## Interfaces and live integration path

Tools call the API client, which sends requests through the governed client.
