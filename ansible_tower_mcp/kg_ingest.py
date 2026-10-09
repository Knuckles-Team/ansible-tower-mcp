"""Epistemic-graph ingestion for Ansible Tower records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. The package pushes its Ansible
Tower / AWX data into the ONE epistemic-graph knowledge graph as **typed OWL
nodes** (`:JobTemplate`, `:Job`, `:Inventory`, `:Host`, `:AnsibleProject`, …) +
links, through `agent_connector_sdk.ingest` -- the generated `SourceIngest`
client, not a local ingestion helper. Node ids follow `ansible:<class>:<extId>`;
`node_type` matches the classes federated by `ansible_tower_mcp.ontology`
(`ansible.ttl`).
"""

from __future__ import annotations

from typing import Any

from agent_connector_sdk.ingest import (
    ChangeSet,
    Document,
    Entity,
    IngestBinding,
    IngestError,
    KnowledgeIngest,
    Relationship,
    current_ingest,
)

_BINDING = IngestBinding(connector="ansible-tower-mcp", stream="ansible")

_ENTITY_RESERVED_KEYS = frozenset({"id", "node_type"})
_RELATIONSHIP_RESERVED_KEYS = frozenset({"source", "target", "relationship"})


def _to_entity(record: dict[str, Any]) -> Entity:
    return Entity(
        id=record.get("id"),
        node_type=record.get("node_type"),
        properties={
            key: value
            for key, value in record.items()
            if key not in _ENTITY_RESERVED_KEYS
        },
    )


def _to_relationship(record: dict[str, Any]) -> Relationship:
    properties = {
        key: value
        for key, value in record.items()
        if key not in _RELATIONSHIP_RESERVED_KEYS
    }
    return Relationship(
        source=record["source"],
        target=record["target"],
        relationship=record["relationship"],
        properties=properties or None,
    )


# --------------------------------------------------------------------------- #
# Public API — thin mappers (records -> typed entity/relationship dicts).
# --------------------------------------------------------------------------- #
async def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Write typed nodes (+ edges) into epistemic-graph via the SDK ingest facade.

    ``entities`` use canonical ``node_type`` and relationships use canonical
    ``relationship``. A malformed change set or a refused commit raises
    ``IngestError``.
    """
    if not entities:
        raise IngestError("ingest_entities needs at least one entity")
    change_set = ChangeSet(
        entities=tuple(_to_entity(entity) for entity in entities),
        relationships=tuple(
            _to_relationship(relationship) for relationship in relationships or ()
        ),
    )
    service = ingest or current_ingest()
    receipt = await service.submit(_BINDING, change_set)
    return {"nodes": receipt.affected_count, "edges": receipt.relationship_count}


async def ingest_documents(
    docs: list[dict[str, Any]],
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Write text records (e.g. job stdout) as ``:Document`` nodes for semantic search.

    Each doc: ``{"id":..., "text":..., "title"?:..., "source_uri"?:..., ...props}``.
    """
    if not docs:
        raise IngestError("ingest_documents needs at least one document")
    change_set = ChangeSet(
        documents=tuple(
            Document(
                id=doc["id"],
                text=doc["text"],
                title=doc.get("title"),
                source_uri=doc.get("source_uri"),
                properties={
                    key: value
                    for key, value in doc.items()
                    if key not in {"id", "text", "title", "source_uri"}
                },
            )
            for doc in docs
        )
    )
    service = ingest or current_ingest()
    receipt = await service.submit(_BINDING, change_set)
    return {"nodes": receipt.affected_count, "edges": receipt.relationship_count}


def _clean(props: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in props.items() if v is not None}


async def ingest_job_templates(
    templates: list[dict[str, Any]],
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Map Ansible Tower job-template records → ``:JobTemplate`` nodes (+ links)."""
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for tpl in templates or []:
        tid = tpl.get("id")
        if tid is None:
            continue
        tpl_id = f"ansible:jobtemplate:{tid}"
        entities.append(
            _clean(
                {
                    "id": tpl_id,
                    "node_type": "JobTemplate",
                    "name": tpl.get("name"),
                    "description": tpl.get("description"),
                    "playbook": tpl.get("playbook"),
                    "job_type": tpl.get("job_type"),
                    "externalToolId": str(tid),
                }
            )
        )
        inv = tpl.get("inventory")
        if inv is not None:
            relationships.append(
                {
                    "source": tpl_id,
                    "target": f"ansible:inventory:{inv}",
                    "relationship": "usesInventory",
                }
            )
        proj = tpl.get("project")
        if proj is not None:
            relationships.append(
                {
                    "source": tpl_id,
                    "target": f"ansible:project:{proj}",
                    "relationship": "usesProject",
                }
            )
    return await ingest_entities(entities, relationships, ingest=ingest)


async def ingest_jobs(
    jobs: list[dict[str, Any]],
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Map Ansible Tower job records → ``:Job`` nodes (+ launchedFrom/usesInventory)."""
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for job in jobs or []:
        jid = job.get("id")
        if jid is None:
            continue
        job_id = f"ansible:job:{jid}"
        entities.append(
            _clean(
                {
                    "id": job_id,
                    "node_type": "Job",
                    "name": job.get("name"),
                    "jobStatus": job.get("status"),
                    "elapsed": job.get("elapsed"),
                    "playbook": job.get("playbook"),
                    "finished": job.get("finished"),
                    "failed": job.get("failed"),
                    "externalToolId": str(jid),
                }
            )
        )
        tpl = job.get("job_template")
        if tpl is not None:
            relationships.append(
                {
                    "source": job_id,
                    "target": f"ansible:jobtemplate:{tpl}",
                    "relationship": "launchedFrom",
                }
            )
        inv = job.get("inventory")
        if inv is not None:
            relationships.append(
                {
                    "source": job_id,
                    "target": f"ansible:inventory:{inv}",
                    "relationship": "usesInventory",
                }
            )
    return await ingest_entities(entities, relationships, ingest=ingest)


async def ingest_inventories(
    inventories: list[dict[str, Any]],
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Map Ansible Tower inventory records → ``:Inventory`` nodes (+ inOrganization)."""
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for inv in inventories or []:
        iid = inv.get("id")
        if iid is None:
            continue
        inv_id = f"ansible:inventory:{iid}"
        entities.append(
            _clean(
                {
                    "id": inv_id,
                    "node_type": "Inventory",
                    "name": inv.get("name"),
                    "description": inv.get("description"),
                    "total_hosts": inv.get("total_hosts"),
                    "externalToolId": str(iid),
                }
            )
        )
        org = inv.get("organization")
        if org is not None:
            relationships.append(
                {
                    "source": inv_id,
                    "target": f"ansible:organization:{org}",
                    "relationship": "inOrganization",
                }
            )
    return await ingest_entities(entities, relationships, ingest=ingest)


async def ingest_hosts(
    hosts: list[dict[str, Any]],
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Map Ansible Tower host records → ``:Host`` nodes (+ belongsToInventory)."""
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for host in hosts or []:
        hid = host.get("id")
        if hid is None:
            continue
        host_id = f"ansible:host:{hid}"
        entities.append(
            _clean(
                {
                    "id": host_id,
                    "node_type": "Host",
                    "name": host.get("name"),
                    "description": host.get("description"),
                    "enabled": host.get("enabled"),
                    "externalToolId": str(hid),
                }
            )
        )
        inv = host.get("inventory")
        if inv is not None:
            relationships.append(
                {
                    "source": host_id,
                    "target": f"ansible:inventory:{inv}",
                    "relationship": "belongsToInventory",
                }
            )
    return await ingest_entities(entities, relationships, ingest=ingest)


_INGESTORS = {
    "job_templates": ingest_job_templates,
    "jobs": ingest_jobs,
    "inventories": ingest_inventories,
    "hosts": ingest_hosts,
}
