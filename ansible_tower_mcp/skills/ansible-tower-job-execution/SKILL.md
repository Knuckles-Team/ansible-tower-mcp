---
name: ansible-tower-job-execution
skill_type: skill
description: >-
  Launch and monitor Ansible Tower / AWX automation via the ansible-tower-mcp MCP
  server — run job templates and workflows, watch job status, stream stdout, cancel
  runs, and fire ad hoc module commands. Use when the agent must kick off a playbook
  run, check whether a job succeeded or failed, pull a failed job's log, rerun a
  job, or run a one-off ad hoc command against an inventory. Do NOT use for defining
  inventories/hosts (use ansible-tower-inventory-management) or wiring SCM-backed
  playbook sources (use ansible-tower-project-scm).
license: MIT
tags: [ansible-tower, awx, jobs, automation, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---
# Ansible Tower Job Execution

Domain-typed control of Ansible Tower **job templates**, **workflow templates**,
**jobs**, and **ad hoc commands** for launching and monitoring automation runs.

## When to use
- Launch a job template (optionally with `extra_vars`) or a workflow template.
- Poll a running job's `status`, read its stdout, or fetch its structured events.
- Triage a failed run (get the job, pull its stdout log).
- Cancel a job (launch its template again to rerun it); run a one-off ad hoc module command.

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
| `ANSIBLE_VERIFY` | optional | TLS verification toggle (default false) |


## Tools
One typed tool per operation; pass each argument by name.

| Tool | Use |
|------|-----|
| `ansible_tower_list_job_templates`, `ansible_tower_get_job_template` | Find and read a job template |
| `ansible_tower_create_job_template`, `ansible_tower_update_job_template`, `ansible_tower_delete_job_template` | Define, change or retire a template |
| `ansible_tower_launch_job` | Launch a template (optionally with `extra_vars`) |
| `ansible_tower_list_jobs`, `ansible_tower_get_job` | Poll runs and read a run's status |
| `ansible_tower_get_job_events`, `ansible_tower_get_job_stdout` | Structured events and the log of a run |
| `ansible_tower_cancel_job` | Cancel a running job |
| `ansible_tower_list_workflow_templates`, `ansible_tower_get_workflow_template`, `ansible_tower_launch_workflow` | Find and launch workflows |
| `ansible_tower_list_workflow_jobs`, `ansible_tower_get_workflow_job`, `ansible_tower_cancel_workflow_job` | Follow or cancel a workflow run |
| `ansible_tower_run_ad_hoc_command`, `ansible_tower_get_ad_hoc_command`, `ansible_tower_cancel_ad_hoc_command` | One-off module commands |
| `ansible_ingest_resources`, `ansible_ingest_job_log` | Push runs and logs into the knowledge graph |

### Key parameters
- `template_id` — required to launch a job/workflow template.
- `extra_vars` — a **JSON string** of playbook variables (validated as JSON).
- `job_id` — required for `ansible_tower_get_job`, `ansible_tower_get_job_stdout` and `ansible_tower_cancel_job`.
- Ad hoc: `inventory_id`, `credential_id`, `module_name`, `module_args`, `verbosity` (0-4).

## Recipes (tool arguments)
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
