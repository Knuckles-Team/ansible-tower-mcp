# CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION — Implementation plan

Governing spec: [spec.md](spec.md). Rows: [requirements.md](requirements.md).

## Summary

The connector reuses `scion_sdk.http.create_http_client` for all vendor requests. The SDK retry policy replaces connector-local retry handling.

## Technical Context

- **Language/Version**: Python 3.14 (floor 3.12)
- **Primary Dependencies**: scion-sdk, fastmcp
- **Storage**: N/A; the connector stores nothing
- **Testing**: pytest; the proof level each row names
- **Target Platform**: Linux containers
- **Project Type**: connector (MCP server)
- **Performance Goals**: N/A
- **Constraints**: one tool per API operation; shared capabilities come from the SDK
- **Scale/Scope**: 2 rows

## Constitution Check

- One owner per concept: pass. The connector owns one external system's calls, mappings and tools only.
- Connectors depend on the SDK and are called through arbora: pass.
- No ratchets: pass. The rows add no suppression.

## Project Structure

```text
ansible_tower_mcp/api/api_client_base.py  existing
ansible_tower_mcp/mcp/tools.py  existing
ansible_tower_mcp/auth.py  existing
tests/test_sdk_centralization.py  existing
```

## Phase 0: Research

No unknowns. Each row names the code it touches.

## Phase 1: Design

### Implementation units

- `ansible_tower_mcp/api/api_client_base.py`: builds the governed client from the runtime TLS profile.
- `ansible_tower_mcp/api/api_client_base.py`: `handle_pagination` drives the SDK `PaginationIterator` in `next_url` mode. A sweep stops after 10,000 pages or 1,000,000 records.

### Interfaces and live integration path

Tools call the API client, which sends requests through the governed client.

## Phase 2: Task approach

`tasks.md` holds one task line per row, producer first.

## Complexity Tracking

None. The constitution check passed.

## Build contract

The repository pre-commit hooks apply: `ruff-format`, `connector-standard`, `secrets`, `tests-fast`. Each row names its proving test. No suppression and no duplicate implementation.

## Production caller chain

1. `CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R001`: any Tower tool (`ansible_tower_mcp/mcp/tools.py`) -> `get_client` (`ansible_tower_mcp/auth.py`) -> `BaseApiClient` (`ansible_tower_mcp/api/api_client_base.py` line 21) -> `create_http_client` (line 41) from `scion_sdk.http.client`.
2. `CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R002`: list tools such as `ansible_tower_jobs` -> `api_client_jobs.py::list_jobs` -> `BaseApiClient.handle_pagination` (`ansible_tower_mcp/api/api_client_base.py` line 202) -> `scion_sdk.httpsupport.pagination.PaginationIterator`.

## Cross-repo seams

none. The cited owner rows are library capabilities the connector calls in process; spec.md names them.
