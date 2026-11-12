# Ansible Tower Inventory Management

Manage Ansible Tower / AWX inventories, groups, and managed hosts via the ansible-tower-mcp MCP server — create and update inventories, add/remove hosts, organize hosts into groups, and set host/group variables. Use when the agent must define what automation runs against: build an inventory, register hosts, group them, or edit host variables. Do NOT use for launching runs against an inventory (use ansible-tower-job-execution) or managing playbook SCM sources (use ansible-tower-project-scm).

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
  organization, team and user tools (`ansible_tower_list_organizations`, `ansible_tower_list_teams`, `ansible_tower_list_users`).

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`ansible-tower-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `ANSIBLE_BASE_URL` | ✅ | Tower/AWX base URL |
| `ANSIBLE_USERNAME` / `ANSIBLE_PASSWORD` | ✅* | Basic auth |
| `ANSIBLE_CLIENT_ID` / `ANSIBLE_CLIENT_SECRET` | optional | OAuth2 |
| `ANSIBLE_TOWER_TLS_PROFILE` | optional | Runtime TLS profile selector; verification is mandatory |

## Tools
One typed tool per operation; pass each argument by name.

| Tool | Use |
|------|-----|
| `ansible_tower_list_inventories`, `ansible_tower_get_inventory`, `ansible_tower_create_inventory`, `ansible_tower_update_inventory`, `ansible_tower_delete_inventory` | Inventories |
| `ansible_tower_list_hosts`, `ansible_tower_get_host`, `ansible_tower_create_host`, `ansible_tower_update_host`, `ansible_tower_delete_host` | Hosts |
| `ansible_tower_list_groups`, `ansible_tower_get_group`, `ansible_tower_create_group`, `ansible_tower_update_group`, `ansible_tower_delete_group` | Groups (scoped by `inventory_id`) |
| `ansible_tower_add_host_to_group`, `ansible_tower_remove_host_from_group` | Group membership |

## Recipes (tool arguments)
Create an inventory under org 1:
```json
{"name": "prod-web", "organization_id": 1, "description": "Production web tier"}
```
Register a host with variables:
```json
{"name": "web01.example.com", "inventory_id": 4, "variables": "{\"ansible_host\":\"[REDACTED_IPV4]\"}"}
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
- `variables` must be a valid JSON string; the client raises "Invalid JSON" otherwise.
- `ansible_tower_list_groups` requires an `inventory_id` (groups are scoped).
- `remove_host_from_group` disassociates (does not delete) the host.
- Deleting an inventory cascades to its hosts and groups in Tower — confirm first.

## Related
- **KG ingestion:** `ansible_ingest_resources` with `resource_type` `inventories`
  or `hosts` maps them into the knowledge graph as `:Inventory` / `:Host` nodes
  linked by `:belongsToInventory` / `:inOrganization`.
- Run automation against these targets: `ansible-tower-job-execution`.
