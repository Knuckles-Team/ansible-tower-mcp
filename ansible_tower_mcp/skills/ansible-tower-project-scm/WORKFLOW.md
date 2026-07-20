# Ansible Tower Project Scm

Manage Ansible Tower / AWX projects (SCM-backed playbook sources) and their recurring schedules via the ansible-tower-mcp MCP server — create git/hg/svn/manual projects, trigger an SCM sync, and define rrule schedules that launch job or workflow templates. Use when the agent must wire a playbook repository into Tower, refresh project content, or schedule automation to run on a cadence. Do NOT use for launching ad hoc runs (use ansible-tower-job-execution) or defining target inventories/hosts (use ansible-tower-inventory-management).

# Ansible Tower Project & Schedule Management

Domain-typed control of Ansible Tower **projects** (the SCM-backed source of
playbooks) and **schedules** (rrule triggers that launch templates on a cadence).

## When to use
- Create/update a project pointing at a git/hg/svn repo (or a manual project).
- Trigger a project SCM sync to pull the latest playbooks.
- List/get projects; check what a job template's playbook source is.
- Define, update, or remove an rrule schedule for a job/workflow template.

## When NOT to use
- Launching or monitoring the resulting runs → `ansible-tower-job-execution`.
- Defining the hosts a project's playbooks target → `ansible-tower-inventory-management`.
- Storing repository **credentials** beyond referencing a `credential_id` → the
  `ansible_tower_credentials` tool.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`ansible-tower-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `ANSIBLE_BASE_URL` | ✅ | Tower/AWX base URL |
| `ANSIBLE_USERNAME` / `ANSIBLE_PASSWORD` | ✅* | Basic auth |
| `ANSIBLE_CLIENT_ID` / `ANSIBLE_CLIENT_SECRET` | optional | OAuth2 |
| `ANSIBLE_TOWER_TLS_PROFILE` | optional | Runtime TLS profile selector; verification is mandatory |

## Tools & actions
Prefer the **condensed** tools; each takes `action` + a `params_json` **JSON string**.

| Condensed tool | Actions |
|----------------|---------|
| `ansible_tower_projects` | `list_projects`, `get_project`, `create_project`, `update_project`, `delete_project`, `sync_project` |
| `ansible_tower_schedules` | `list_schedules`, `get_schedule`, `create_schedule`, `update_schedule`, `delete_schedule` |

### Key parameters
- `organization_id` + `scm_type` — required to `create_project` (`git|hg|svn|manual`).
- `scm_url` — required for non-manual SCM types; `scm_branch` optional.
- `project_id` — required for `sync_project` / `get_project`.
- `rrule` — iCal RFC 5545 recurrence string for a schedule.
- `unified_job_template_id` — the job/workflow template a schedule triggers.

## Recipes (`params_json`)
Create a git-backed project:
```json
{"name": "infra-playbooks", "organization_id": 1, "scm_type": "git", "scm_url": "[configured-endpoint] "scm_branch": "main"}
```
Trigger a project sync:
```json
{"project_id": 5}
```
Schedule a template to run nightly:
```json
{"name": "nightly-patch", "rrule": "DTSTART:20260101T020000Z RRULE:FREQ=DAILY;INTERVAL=1", "unified_job_template_id": 7}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- `scm_type` must be one of `git|hg|svn|manual`; non-manual types require `scm_url`.
- `sync_project` is async — it POSTs a project update; poll `get_project` for
  `status` / `last_job_run` to confirm the sync finished.
- `rrule` must be a valid iCal recurrence; Tower rejects malformed rules.
- `list_schedules` accepts an optional `unified_job_template_id` filter.

## Related
- **KG ingestion:** `ansible_ingest_resources` with `resource_type` `job_templates`
  maps templates (which reference a project via `:usesProject`) into the graph.
- Run/monitor the scheduled automation: `ansible-tower-job-execution`.
