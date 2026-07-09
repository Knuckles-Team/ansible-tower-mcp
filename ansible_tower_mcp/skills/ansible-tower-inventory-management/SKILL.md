---
name: ansible-tower-inventory-management
skill_type: skill
description: >-
  Manage Ansible Tower / AWX inventories, groups, and managed hosts via the
  ansible-tower-mcp MCP server — create and update inventories, add/remove hosts,
  organize hosts into groups, and set host/group variables. Use when the agent must
  define what automation runs against: build an inventory, register hosts, group
  them, or edit host variables. Do NOT use for launching runs against an inventory
  (use ansible-tower-job-execution) or managing playbook SCM sources (use
  ansible-tower-project-scm).
license: MIT
tags: [ansible-tower, awx, inventory, hosts, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# Ansible Tower Inventory Management

Domain-typed control of Ansible Tower **inventories**, **groups**, and **hosts** —
the targets automation runs against, plus their organization and variables.

## When to use
- Create/update/delete an inventory under an organization.
- Register, edit, or remove a managed host; set its `variables`.
- Create groups and add/remove hosts to organize an inventory.
- List an inventory's hosts or groups.

## When NOT to use
- Launching or monitoring jobs against the inventory → `ansible-tower-job-execution`.
- SCM-backed playbook projects → `ansible-tower-project-scm`.
- Organization / team / user RBAC beyond inventory ownership → the
  `ansible_tower_organizations` / `ansible_tower_teams` / `ansible_tower_users` tools.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`ansible-tower-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `ANSIBLE_BASE_URL` | ✅ | Tower/AWX base URL |
| `ANSIBLE_USERNAME` / `ANSIBLE_PASSWORD` | ✅* | Basic auth |
| `ANSIBLE_CLIENT_ID` / `ANSIBLE_CLIENT_SECRET` | optional | OAuth2 |
| `ANSIBLE_VERIFY` | optional | TLS verification toggle |

## Tools & actions
Prefer the **condensed** tools; each takes `action` + a `params_json` **JSON string**.

| Condensed tool | Actions |
|----------------|---------|
| `ansible_tower_inventory` | `list_inventories`, `get_inventory`, `create_inventory`, `update_inventory`, `delete_inventory` |
| `ansible_tower_hosts` | `list_hosts`, `get_host`, `create_host`, `update_host`, `delete_host` |
| `ansible_tower_groups` | `list_groups`, `get_group`, `create_group`, `update_group`, `delete_group`, `add_host_to_group`, `remove_host_from_group` |

### Key parameters
- `organization_id` — required to `create_inventory`.
- `inventory_id` — required for host/group creation and scoped listing.
- `variables` — a **JSON string** of host/group variables (validated as JSON).
- `group_id` + `host_id` — for `add_host_to_group` / `remove_host_from_group`.

## Recipes (`params_json`)
Create an inventory under org 1:
```json
{"name": "prod-web", "organization_id": 1, "description": "Production web tier"}
```
Register a host with variables:
```json
{"name": "web01.example.com", "inventory_id": 4, "variables": "{\"ansible_host\":\"10.0.0.11\"}"}
```
List hosts in one inventory:
```json
{"inventory_id": 4}
```
Add a host to a group:
```json
{"group_id": 9, "host_id": 22}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- `variables` must be a valid JSON string; the client raises "Invalid JSON" otherwise.
- `ansible_tower_groups` `list_groups` requires an `inventory_id` (groups are scoped).
- `remove_host_from_group` disassociates (does not delete) the host.
- Deleting an inventory cascades to its hosts and groups in Tower — confirm first.

## Related
- **KG ingestion:** `ansible_ingest_resources` with `resource_type` `inventories`
  or `hosts` maps them into the knowledge graph as `:Inventory` / `:Host` nodes
  linked by `:belongsToInventory` / `:inOrganization`.
- Run automation against these targets: `ansible-tower-job-execution`.
