# Concept Registry — ansible-tower-mcp

> **Prefix**: `CONCEPT:ANSIBLE-*`
> **Version**: 1.16.0
> **Bridge**: [`CONCEPT:ECO-4.0`](https://github.com/Knuckles-Team/agent-utilities/blob/main/docs/concepts.md) (Unified Toolkit Ingestion)

---

## Project-Specific Concepts

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:ANSIBLE-001` | Ad Hoc Commands Operations | MCP tool domain `ad_hoc_commands` — Action-routed dynamic tool registration |
| `CONCEPT:ANSIBLE-002` | Credentials Operations | MCP tool domain `credentials` — Action-routed dynamic tool registration |
| `CONCEPT:ANSIBLE-003` | Group Management | MCP tool domain `groups` — Action-routed dynamic tool registration |
| `CONCEPT:ANSIBLE-004` | Hosts Operations | MCP tool domain `hosts` — Action-routed dynamic tool registration |
| `CONCEPT:ANSIBLE-005` | Inventory Operations | MCP tool domain `inventory` — Action-routed dynamic tool registration |
| `CONCEPT:ANSIBLE-006` | Job Templates Operations | MCP tool domain `job_templates` — Action-routed dynamic tool registration |
| `CONCEPT:ANSIBLE-007` | Jobs Operations | MCP tool domain `jobs` — Action-routed dynamic tool registration |
| `CONCEPT:ANSIBLE-008` | Organizations Operations | MCP tool domain `organizations` — Action-routed dynamic tool registration |
| `CONCEPT:ANSIBLE-009` | Projects Operations | MCP tool domain `projects` — Action-routed dynamic tool registration |
| `CONCEPT:ANSIBLE-010` | Schedules Operations | MCP tool domain `schedules` — Action-routed dynamic tool registration |
| `CONCEPT:ANSIBLE-011` | System Information & Health | MCP tool domain `system` — Action-routed dynamic tool registration |
| `CONCEPT:ANSIBLE-012` | Teams Operations | MCP tool domain `teams` — Action-routed dynamic tool registration |
| `CONCEPT:ANSIBLE-013` | Users Operations | MCP tool domain `users` — Action-routed dynamic tool registration |
| `CONCEPT:ANSIBLE-014` | Workflow Jobs Operations | MCP tool domain `workflow_jobs` — Action-routed dynamic tool registration |
| `CONCEPT:ANSIBLE-015` | Workflow Templates Operations | MCP tool domain `workflow_templates` — Action-routed dynamic tool registration |

## Cross-Project References (from agent-utilities)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:ECO-4.0` | Unified Toolkit Ingestion | agent-utilities |
| `CONCEPT:ORCH-1.2` | Confidence-Gated Router | agent-utilities |
| `CONCEPT:OS-5.1` | Prompt Injection Defense | agent-utilities |
| `CONCEPT:OS-5.2` | Cognitive Scheduler | agent-utilities |
| `CONCEPT:OS-5.3` | Guardrail Engine | agent-utilities |
| `CONCEPT:OS-5.4` | Audit Logging | agent-utilities |
| `CONCEPT:KG-2.0` | Knowledge Graph Core | agent-utilities |

## Synergy with agent-utilities

This project integrates with `agent-utilities` via `CONCEPT:ECO-4.0` (Unified Toolkit Ingestion). The `ansible_tower_mcp` MCP server registers its tools with the agent-utilities FastMCP middleware, enabling automatic discovery, telemetry, and Knowledge Graph ingestion of all ANSIBLE-* concepts.
