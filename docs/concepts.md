# Concept Registry — ansible-tower-mcp

> **Prefix**: `CONCEPT:ANSIBLE-*`
> **Version**: 1.16.0
> **Bridge**: [`CONCEPT:AU-ECO.messaging.native-backend-abstraction`](https://github.com/Knuckles-Team/scion-sdk/blob/main/docs/concepts.md) (Unified Toolkit Ingestion)

---

## Project-Specific Concepts

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:AT-OS.governance.ansible` | Ad Hoc Commands Operations | MCP tool domain `ad_hoc_commands` — Action-routed dynamic tool registration |
| `CONCEPT:AT-OS.governance.ansible-2` | Credentials Operations | MCP tool domain `credentials` — Action-routed dynamic tool registration |
| `CONCEPT:AT-OS.governance.ansible-3` | Group Management | MCP tool domain `groups` — Action-routed dynamic tool registration |
| `CONCEPT:AT-OS.governance.ansible-4` | Hosts Operations | MCP tool domain `hosts` — Action-routed dynamic tool registration |
| `CONCEPT:AT-OS.governance.ansible-5` | Inventory Operations | MCP tool domain `inventory` — Action-routed dynamic tool registration |
| `CONCEPT:AT-OS.governance.ansible-6` | Job Templates Operations | MCP tool domain `job_templates` — Action-routed dynamic tool registration |
| `CONCEPT:AT-OS.governance.ansible-7` | Jobs Operations | MCP tool domain `jobs` — Action-routed dynamic tool registration |
| `CONCEPT:AT-OS.governance.ansible-8` | Organizations Operations | MCP tool domain `organizations` — Action-routed dynamic tool registration |
| `CONCEPT:AT-OS.governance.ansible-9` | Projects Operations | MCP tool domain `projects` — Action-routed dynamic tool registration |
| `CONCEPT:AT-OS.governance.ansible-10` | Schedules Operations | MCP tool domain `schedules` — Action-routed dynamic tool registration |
| `CONCEPT:AT-OS.governance.ansible-11` | System Information & Health | MCP tool domain `system` — Action-routed dynamic tool registration |
| `CONCEPT:AT-OS.governance.ansible-12` | Teams Operations | MCP tool domain `teams` — Action-routed dynamic tool registration |
| `CONCEPT:AT-OS.governance.ansible-13` | Users Operations | MCP tool domain `users` — Action-routed dynamic tool registration |
| `CONCEPT:AT-OS.governance.ansible-14` | Workflow Jobs Operations | MCP tool domain `workflow_jobs` — Action-routed dynamic tool registration |
| `CONCEPT:AT-OS.governance.ansible-15` | Workflow Templates Operations | MCP tool domain `workflow_templates` — Action-routed dynamic tool registration |

## Cross-Project References (from scion-sdk)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:AU-ECO.messaging.native-backend-abstraction` | Unified Toolkit Ingestion | scion-sdk |
| `CONCEPT:AU-ORCH.adapter.hot-cache-invalidation` | Confidence-Gated Router | scion-sdk |
| `CONCEPT:AU-OS.config.secrets-authentication` | Prompt Injection Defense | scion-sdk |
| `CONCEPT:AU-OS.state.cognitive-scheduler-preemption` | Cognitive Scheduler | scion-sdk |
| `CONCEPT:AU-OS.governance.reactive-multi-axis-budget` | Guardrail Engine | scion-sdk |
| `CONCEPT:AU-OS.governance.wasm-micro-agent-sandbox` | Audit Logging | scion-sdk |
| `CONCEPT:AU-KG.query.object-graph-mapper` | Knowledge Graph Core | scion-sdk |

## Synergy with scion-sdk

This project integrates with `scion-sdk` via `CONCEPT:AU-ECO.messaging.native-backend-abstraction` (Unified Toolkit Ingestion). The `ansible_tower_mcp` MCP server registers its tools with the scion-sdk FastMCP middleware, enabling automatic discovery, telemetry, and Knowledge Graph ingestion of all ANSIBLE-* concepts.
