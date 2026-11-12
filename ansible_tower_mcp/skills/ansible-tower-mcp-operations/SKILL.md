---
name: ansible-tower-mcp-operations
skill_type: skill
description: >-
  Operate ansible-tower-mcp through its governed MCP and Arbora capabilities, including ansible tower inventory management, ansible tower job execution, ansible tower project scm. Use when a request requires this provider's read, change, automation, ingestion, troubleshooting, or evidence workflows.
---

# Ansible Tower Mcp Operations

Use the provider's governed MCP tools through Arbora delegation.

## Workflow

1. Establish the verified GraphSession and tenant before discovery or retrieval.
2. Discover the current tool surface; never assume a stale tool name or schema.
3. Prefer read-only inspection first. For changes, present impact and use the provider's
   dry-run or preview mode when available.
4. Execute mutations as fenced WorkItems so retries remain idempotent and auditable.
5. Ingest source data only through the signed connector preset and ChangeEnvelope path.
6. Verify the durable result and its trace/evidence before reporting completion.

## Safety contract

- Never persist credentials, endpoints, raw personal identifiers, hostnames, or local paths.
- Resolve TLS trust and verification from environment/configuration; never hardcode bypasses.
- Treat unknown ACL, tenant, schema, or tool-contract state as a hard failure.
- Require explicit approval for destructive, externally visible, or irreversible actions.
- Keep runtime traces policy-scoped and privacy-sanitized.

## Specialized workflows

Read [the workflow catalog](references/catalog.md) only when the request needs a
provider-specific procedure, parameter map, script, or reference asset.

## Tools

One typed tool per operation. The domain skills name the job, inventory and project tools; this skill covers the rest.

| Area | Tools |
|------|-------|
| Credentials | `ansible_tower_list_credential_types`, `ansible_tower_list_credentials`, `ansible_tower_get_credential`, `ansible_tower_create_credential`, `ansible_tower_update_credential`, `ansible_tower_delete_credential` |
| Organizations | `ansible_tower_list_organizations`, `ansible_tower_get_organization`, `ansible_tower_create_organization`, `ansible_tower_update_organization`, `ansible_tower_delete_organization` |
| Teams | `ansible_tower_list_teams`, `ansible_tower_get_team`, `ansible_tower_create_team`, `ansible_tower_update_team`, `ansible_tower_delete_team` |
| Users | `ansible_tower_list_users`, `ansible_tower_get_user`, `ansible_tower_create_user`, `ansible_tower_update_user`, `ansible_tower_delete_user` |
| Platform | `ansible_tower_get_ansible_version`, `ansible_tower_get_dashboard_stats`, `ansible_tower_get_metrics` |
