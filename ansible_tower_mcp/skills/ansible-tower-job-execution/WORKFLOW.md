# Ansible Tower Job Execution

Launch and monitor Ansible Tower / AWX automation via the ansible-tower-mcp MCP server — run job templates and workflows, watch job status, stream stdout, cancel runs, and fire ad hoc module commands. Use when the agent must kick off a playbook run, check whether a job succeeded or failed, pull a failed job's log, relaunch a job, or run a one-off ad hoc command against an inventory. Do NOT use for defining inventories/hosts (use ansible-tower-inventory-management) or wiring SCM-backed playbook sources (use ansible-tower-project-scm).

# Ansible Tower Job Execution

Domain-typed control of Ansible Tower **job templates**, **workflow templates**,
**jobs**, and **ad hoc commands** for launching and monitoring automation runs.

## When to use
- Launch a job template (optionally with `extra_vars`) or a workflow template.
- Poll a running job's `status`, read its stdout, or fetch its structured events.
- Triage a failed run (get the job, pull its stdout log).
- Cancel or relaunch a job; run a one-off ad hoc module command.

## When NOT to use
- Creating/updating inventories, hosts, or groups → `ansible-tower-inventory-management`.
- Managing SCM-backed projects that supply the playbooks → `ansible-tower-project-scm`.
- Bulk semantic search over historical runs → query the knowledge graph after
  ingesting via `ansible_ingest_resources` / `ansible_ingest_job_log`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`ansible-tower-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `ANSIBLE_BASE_URL` | ✅ | Tower/AWX base URL |
| `ANSIBLE_USERNAME` / `ANSIBLE_PASSWORD` | ✅* | Basic auth (token minted automatically) |
| `ANSIBLE_CLIENT_ID` / `ANSIBLE_CLIENT_SECRET` | optional | OAuth2 client credentials |
| `ANSIBLE_TOKEN` | optional | Pre-minted OAuth token |
| `ANSIBLE_TOWER_TLS_PROFILE` | optional | Runtime TLS profile selector; verification is mandatory |

`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed surface (below)
vs. the 1:1 verbose tools.

## Tools & actions
Prefer the **condensed** tools; each takes `action` + a `params_json` **JSON string**
whose keys are passed straight to the client method.

| Condensed tool | Actions |
|----------------|---------|
| `ansible_tower_job_templates` | `list_job_templates`, `get_job_template`, `create_job_template`, `update_job_template`, `delete_job_template` |
| `ansible_tower_jobs` | `list_jobs`, `get_job`, `cancel_job`, `relaunch_job`, `get_job_events`, `get_job_stdout` |
| `ansible_tower_workflow_templates` | `list_workflow_templates`, `get_workflow_template`, `launch_workflow` |
| `ansible_tower_workflow_jobs` | `list_workflow_jobs`, `get_workflow_job`, `cancel_workflow_job` |
| `ansible_tower_ad_hoc_commands` | `run_ad_hoc_command`, `get_ad_hoc_command`, `cancel_ad_hoc_command` |

### Key parameters
- `template_id` — required to launch a job/workflow template.
- `extra_vars` — a **JSON string** of playbook variables (validated as JSON).
- `job_id` — required for `get_job`, `get_job_stdout`, `cancel_job`, `relaunch_job`.
- Ad hoc: `inventory_id`, `credential_id`, `module_name`, `module_args`, `verbosity` (0-4).

## Recipes (`params_json`)
Launch a job template with vars:
```json
{"template_id": 7, "extra_vars": "{\"env\":\"prod\",\"limit\":\"web\"}"}
```
List only failed jobs:
```json
{"status": "failed"}
```
Fetch a job's stdout (text):
```json
{"job_id": 512, "format": "txt"}
```
Run an ad hoc ping against an inventory:
```json
{"inventory_id": 3, "credential_id": 2, "module_name": "ping", "module_args": ""}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- `extra_vars` / `module_args` must themselves be valid JSON strings; the client
  raises "Invalid JSON" otherwise.
- Launching returns immediately with a job record — the run is async; poll
  `get_job` for terminal `status` (`successful`, `failed`, `canceled`).
- `get_job_stdout` accepts `format` in `txt|html|json|ansi`; `txt` is best for logs.
- `verbosity` for ad hoc commands must be 0-4.

## Related
- **KG ingestion:** `ansible_ingest_resources` (resource_type `jobs`/`job_templates`)
  pushes runs into the knowledge graph as typed `:Job`/`:JobTemplate` nodes;
  `ansible_ingest_job_log` stores a job's raw stdout as a durable `:Blob`.
- Inventory targets: `ansible-tower-inventory-management`.
- Playbook sources: `ansible-tower-project-scm`.
