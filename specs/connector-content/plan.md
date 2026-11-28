# CONN-ANSIBLE-TOWER-MCP-CONNECTOR-CONTENT — Implementation plan

Governing spec: [spec.md](spec.md). Rows: [requirements.md](requirements.md).

## Summary

`pyproject.toml` declares `ansible-tower-mcp` as the connector identity. `create_mcp_server` resolves the packaged content of `ansible_tower_mcp` from it.

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
pyproject.toml  existing
tests/test_default_content_surfaces.py  existing
ansible_tower_mcp/mcp/mcp_server.py  existing
ansible_tower_mcp/__init__.py  existing
ansible_tower_mcp/connector_sources.py  existing
```

## Phase 0: Research

No unknowns. Each row names the code it touches.

## Phase 1: Design

### Machine roll-up design

1. **Owner.** ansible-tower-mcp owns its host class and ingest. Medulla owns the machine class.
2. **Cohesion.** The class parent, the mapping and the link change together in the host ingest.
3. **Dependency direction.** The connector imports `scion_sdk.machine`, which imports the engine client. Nothing points upward.
4. **Interface depth.** none. The row reuses the SDK helper.
5. **Special cases.** A refused key skips one link and never fails the record write.
6. **State.** none. The connector holds no lifecycle. The lifecycle machine belongs to medulla.
7. **Environment.** none. The roll-up and the link need no configuration.

The rows are delivered in place; the design is the caller chain below.

## Phase 2: Task approach

`tasks.md` holds one task line per row, producer first.

## Complexity Tracking

None. The constitution check passed.

## Build contract

The repository pre-commit hooks apply: `ruff-format`, `connector-standard`, `secrets`, `tests-fast`. Each row names its proving test. No suppression and no duplicate implementation.

## Production caller chain

1. `CONN-ANSIBLE-TOWER-MCP-CONNECTOR-CONTENT-R001`: the `ansible-tower-mcp` console script (`ansible_tower_mcp.mcp.mcp_server:mcp_server`, line 107) -> `get_mcp_instance` (`ansible_tower_mcp/mcp/mcp_server.py` line 72) -> `create_mcp_server(content=ConnectorContent.for_package("ansible_tower_mcp", ...))`; the entry point `ansible_tower_mcp:connector` is `ansible_tower_mcp/__init__.py` line 107.
2. `CONN-ANSIBLE-TOWER-MCP-CONNECTOR-CONTENT-R002`: arbora `fleet.call` -> tool `ansible_tower_jobs` (`ansible_tower_mcp/mcp/tools.py::register_jobs_tools`, line 225) with actions `list_jobs` and `get_job` -> `ansible_tower_mcp/api/api_client_jobs.py::list_jobs` and `get_job`; `ontology/access_contracts.ttl` does not exist yet.

## Cross-repo seams

- `CONN-ANSIBLE-TOWER-MCP-CONNECTOR-CONTENT-R003.1` consumes the observer helper of `SCION-CENTRALIZED-CAPABILITIES-R057.1`. Contract: `contracts/machine-observer.md`.
