# CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION — Design and implementation plan

Governing specification: [spec.md](spec.md).

## Existing system and reuse

The connector reuses `agent_connector_sdk.http.create_http_client` for all vendor requests.
The SDK retry policy replaces connector-local retry handling.

## Implementation units

- `ansible_tower_mcp/api/api_client_base.py`: builds the governed client from the runtime TLS profile.

## Interfaces and live integration path

Tools call the API client, which sends requests through the governed client.
