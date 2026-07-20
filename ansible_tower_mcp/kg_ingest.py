"""Native epistemic-graph ingestion for Ansible Tower records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. The package natively pushes its
Ansible Tower / AWX data into the ONE epistemic-graph knowledge graph as **typed OWL
nodes** (`:JobTemplate`, `:Job`, `:Inventory`, `:Host`, `:AnsibleProject`, …) + links,
through the required
``agent_utilities.knowledge_graph.memory.native_ingest`` authority. Node ids follow
``ansible:<class>:<extId>``; ``node_type`` matches the classes federated by
``ansible_tower_mcp.ontology`` (``ansible.ttl``).
"""

from __future__ import annotations

from typing import Any

from agent_utilities.knowledge_graph.memory.native_ingest import (
    ingest_documents as _native_ingest_documents,
)
from agent_utilities.knowledge_graph.memory.native_ingest import (
    ingest_entities as _native_ingest_entities,
)

_SOURCE = "ansible-tower-mcp"
_DOMAIN = "ansible"


# --------------------------------------------------------------------------- #
# Public API — thin mappers (records -> typed entity/relationship dicts).
# --------------------------------------------------------------------------- #
def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Write typed nodes (+ edges) into epistemic-graph via the shared primitive.

    ``entities`` use canonical ``node_type`` and relationships use canonical
    ``relationship``. Engine and validation failures raise ``NativeIngestError``.
    """
    return _native_ingest_entities(
        entities,
        relationships,
        source=source,
        domain=domain,
        client=client,
        graph=graph,
    )


def ingest_documents(
    docs: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Write text records (e.g. job stdout) as ``:Document`` nodes for semantic search.

    Each doc: ``{"id":..., "text":..., "title"?:..., "source_uri"?:..., ...props}``.
    Delegates directly to the required native ingestion authority.
    """
    return _native_ingest_documents(
        docs, source=source, domain=domain, client=client, graph=graph
    )


def _clean(props: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in props.items() if v is not None}


def ingest_job_templates(
    templates: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
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
    return ingest_entities(entities, relationships, client=client, graph=graph)


def ingest_jobs(
    jobs: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
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
    return ingest_entities(entities, relationships, client=client, graph=graph)


def ingest_inventories(
    inventories: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
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
    return ingest_entities(entities, relationships, client=client, graph=graph)


def ingest_hosts(
    hosts: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
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
    return ingest_entities(entities, relationships, client=client, graph=graph)


_INGESTORS = {
    "job_templates": ingest_job_templates,
    "jobs": ingest_jobs,
    "inventories": ingest_inventories,
    "hosts": ingest_hosts,
}
