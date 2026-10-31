# CONN-ANSIBLE-TOWER-MCP-CONNECTOR-CONTENT — Requirements

Governing spec: [spec.md](spec.md).

Each row is one requirement. A row names the file it touches and the test that proves it. The generator sets each row's state in `status.json`.

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-ANSIBLE-TOWER-MCP-CONNECTOR-CONTENT-R001` | **Default content.** `pyproject.toml` declares `ansible-tower-mcp` as the single `scion_sdk.connector` entry point. The server lists the packaged `skill://` and `ontology://` resources and the packaged prompts with no `content=` argument. Proving test: `tests/test_default_content_surfaces.py`. | `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. |
| `CONN-ANSIBLE-TOWER-MCP-CONNECTOR-CONTENT-R002` | **Declare access contracts for the competency reads of ansible-tower-mcp.** Subsystem: connector `ansible-tower-mcp`. Caller: the connector's existing read tool, called by arbora through `fleet.call`. Declare in `ansible_tower_mcp/ontology/access_contracts.ttl` one `ac:AccessContract` per entity. Entities: entity `job_run` (class infra:AutomationJob, key `id`, columns jobStatus, finishedAt, templateName, hostId). Each row sets `ac:classIri`, `ac:sourceId`, `ac:entity`, `ac:keyField`, `ac:accessKind` `mcp_tool`, `ac:operation` (the existing tool name) and `ac:pagination`. Column names equal the ontology property local names. Follow `container_manager_mcp/ontology/access_contracts.ttl`. Save one recorded response per entity in `tests/recordings/<entity>.json`. Medulla copies these into its competency fixtures. The consumer is the medulla table row EG-CQ-CONN-R086. | Test: `tests/test_access_contracts.py::test_competency_contracts_certified` (L2) runs the connector ontology certification and validates each recording against its contract. |
