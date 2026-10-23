# CONN-ANSIBLE-TOWER-MCP-SDK-CENTRALIZATION — SDK centralization

## Outcome

The connector must use the shared SDK for HTTP transport, retries, and pagination.
It must keep every tool and its behavior unchanged.

## Scope and owner

The `ansible-tower-mcp` repository owns Ansible Tower operations and mappings.
The shared connector SDK owns the governed HTTP client, retry policy, and pagination checks.
Rows are governed by SDK-CENTRALIZED-CAPABILITIES-R014 in the SDK specification.

Component: Connector integration
References: [Connector SDK](https://github.com/Knuckles-Team/agent-connector-sdk/blob/main/specs/centralized-capabilities/plan.md)
Code: ../../ansible_tower_mcp/api/api_client_base.py ../../tests/test_sdk_centralization.py

## Non-goals

This specification grants no service access, credential creation, or deployment exception.
The connector must not carry its own retry loops or direct HTTP library pins.

## Requirements

See [requirements.md](requirements.md), [plan.md](plan.md), and [test-spec.md](test-spec.md).
