# CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION — SDK centralization

## Outcome

The connector must use the shared SDK for HTTP transport, retries, and pagination.
It must keep every tool and its behavior unchanged.

## Scope and owner

The `ansible-tower-mcp` repository owns Ansible Tower operations and mappings.
The shared connector SDK owns the governed HTTP client, retry policy, and pagination checks.
Rows are governed by SCION-CENTRALIZED-CAPABILITIES-R014 in the SDK specification.

Component: Connector integration
References: [Connector SDK](https://github.com/Knuckles-Team/scion-sdk/blob/main/specs/centralized-capabilities/plan.md)
Code: ../../ansible_tower_mcp/api/api_client_base.py ../../tests/test_sdk_centralization.py

## Non-goals

This specification grants no service access, credential creation, or deployment exception.
The connector must not carry its own retry loops or direct HTTP library pins.

## Requirements

See [requirements.md](requirements.md), [plan.md](plan.md), and [test-spec.md](test-spec.md).

## Why a new spec

The specs of this repository were read; none owns this capability. This spec states it for this connector only.

## Scope and interfaces

In scope: the rows of [requirements.md](requirements.md). Out of scope: the SDK modules and the engine, which own the shared capabilities.

## User Scenarios & Testing

### User Story 1 - SDK centralization (Priority: P1)

The connector must use the shared SDK for HTTP transport, retries, and pagination.

**Acceptance Scenarios**:

1. **Given** the connector is configured, **When** the behaviour of row `CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R001` (governed http) is exercised, **Then** `tests/test_sdk_centralization.py::test_api_client_uses_sdk_http_client` must observe an SDK client and no `requests` import.
2. **Given** the connector is configured, **When** the behaviour of row `CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R002` (shared pagination) is exercised, **Then** `tests/test_sdk_centralization.py::test_pagination_rejects_cross_origin_cursor`, `test_pagination_follows_relative_and_absolute_next`, `test_pagination_rejects_origin_change`, and `test_pagination_stops_on_a_repeated_next` pass.

### Edge Cases

- If `CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R001` is not met, its proving test fails: governed http.
- If `CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R002` is not met, its proving test fails: shared pagination.

## Requirements

- **FR-001**: Governed HTTP. Rows: `CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R001`.
- **FR-002**: Shared pagination. Rows: `CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R002`.

## Success Criteria

- **SC-001**: `tests/test_sdk_centralization.py::test_api_client_uses_sdk_http_client` must observe an SDK client and no `requests` import. Rows: `CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R001`.
- **SC-002**: `tests/test_sdk_centralization.py::test_pagination_rejects_cross_origin_cursor`, `test_pagination_follows_relative_and_absolute_next`, `test_pagination_rejects_origin_change`, and `test_pagination_stops_on_a_repeated_next` pass. Rows: `CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R002`.

## Assumptions

- The external system is reachable with operator-supplied credentials.
- The SDK and engine contracts the rows cite are at the floors declared in `pyproject.toml`.

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R001` | [plan.md](plan.md) | T-001 | [test-spec.md](test-spec.md) |
| FR-002 | `CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION-R002` | [plan.md](plan.md) | T-002 | [test-spec.md](test-spec.md) |
