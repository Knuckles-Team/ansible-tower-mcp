"""Native epistemic-graph ingestion for Ansible Tower records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. The package natively pushes its
Ansible Tower / AWX data into the ONE epistemic-graph knowledge graph as **typed OWL
nodes** (`:JobTemplate`, `:Job`, `:Inventory`, `:Host`, `:AnsibleProject`, …) + links,
using the lightweight engine client (``GraphComputeEngine()._client`` + ``txn``) — the
same fast client the blob ``MediaStore`` uses, NOT the heavy in-process engine.

This is a thin mapper over the shared primitive
``agent_utilities.knowledge_graph.memory.native_ingest``. The import is GUARDED: when
that primitive (or any KG stack / reachable engine) is absent, a self-contained txn
fallback is used, and if even that is unavailable every entry point **no-ops**
(returns ``None``), so the connector keeps working with zero KG infrastructure. Node
ids follow ``ansible:<class>:<extId>``; ``type`` matches the classes federated by
``ansible_tower_mcp.ontology`` (``ansible.ttl``).
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("ansible_tower_mcp.kg")

_SOURCE = "ansible-tower-mcp"
_DOMAIN = "ansible"


# --------------------------------------------------------------------------- #
# Shared-primitive delegation (guarded) with a self-contained txn fallback.
# --------------------------------------------------------------------------- #
def _shared_ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None,
    *,
    client: Any | None,
    graph: str | None,
) -> dict[str, int] | None:
    """Delegate to the shared native_ingest primitive if importable."""
    try:
        from agent_utilities.knowledge_graph.memory.native_ingest import (
            ingest_entities as _ingest,
        )
    except Exception:  # noqa: BLE001 — primitive not in installed agent_utilities
        return _fallback_ingest_entities(
            entities, relationships, client=client, graph=graph
        )
    return _ingest(
        entities,
        relationships,
        source=_SOURCE,
        domain=_DOMAIN,
        client=client,
        graph=graph,
    )


def _fallback_client() -> tuple[Any | None, str]:
    """Return ``(engine_client, graph_name)`` or ``(None, "")`` when unavailable."""
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
    except Exception as e:  # noqa: BLE001 — KG stack absent
        logger.debug("KG ingest unavailable (import): %s", e)
        return None, ""
    try:
        engine = GraphComputeEngine()
        client = getattr(engine, "_client", None)
        if client is None:
            return None, ""
        graph = getattr(engine, "graph_name", None) or "__commons__"
        return client, graph
    except Exception as e:  # noqa: BLE001 — engine unreachable
        logger.debug("KG ingest: engine unreachable: %s", e)
        return None, ""


def _fallback_ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Self-contained txn write path (used only if the shared primitive is absent)."""
    entities = [e for e in (entities or []) if e.get("id")]
    if not entities:
        return None
    if client is None:
        client, graph = _fallback_client()
    if client is None:
        return None
    graph = graph or "__commons__"
    try:
        txn = client.txn.begin(graph=graph)
        for ent in entities:
            props = {k: v for k, v in ent.items() if k != "id" and v is not None}
            props.setdefault("source", _SOURCE)
            props.setdefault("domain", _DOMAIN)
            client.txn.add_node(txn, ent["id"], props)
        committed = client.txn.commit(txn)
    except Exception as e:  # noqa: BLE001 — engine/txn failure is non-fatal
        logger.warning("KG ingest: txn failed: %s", e)
        return None
    if not committed:
        logger.warning("KG ingest: txn not committed (conflict)")
        return None
    edges = 0
    for rel in relationships or []:
        try:
            client.edges.add(
                rel["source"], rel["target"], {"type": rel.get("type", "RELATED")}
            )
            edges += 1
        except Exception as e:  # noqa: BLE001 — pure edge link, best-effort
            logger.debug("KG ingest: edge skipped: %s", e)
    logger.info("KG ingest: wrote %d nodes, %d edges", len(entities), edges)
    return {"nodes": len(entities), "edges": edges}


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
) -> dict[str, int] | None:
    """Write typed nodes (+ edges) into epistemic-graph via the shared primitive.

    ``entities``: ``[{"id":..., "type":<owl:Class>, ...props}]``.
    ``relationships``: ``[{"source":id, "target":id, "type":rel}]``.
    Returns ``{"nodes":n, "edges":m}`` or ``None`` (no engine / failure; never raises).
    ``client``/``graph`` may be injected (tests); otherwise resolved on demand.
    """
    return _shared_ingest_entities(entities, relationships, client=client, graph=graph)


def ingest_documents(
    docs: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write text records (e.g. job stdout) as ``:Document`` nodes for semantic search.

    Each doc: ``{"id":..., "text":..., "title"?:..., "source_uri"?:..., ...props}``.
    Delegates to the shared ``native_ingest.ingest_documents``; if that primitive is
    absent, falls back to writing ``:Document`` typed nodes via the local txn path.
    """
    try:
        from agent_utilities.knowledge_graph.memory.native_ingest import (
            ingest_documents as _ingest_docs,
        )
    except Exception:  # noqa: BLE001 — primitive absent, map to typed nodes locally
        nodes: list[dict[str, Any]] = []
        for doc in docs or []:
            did = doc.get("id")
            text = doc.get("text") or doc.get("content")
            if not did or not text:
                continue
            node = {k: v for k, v in doc.items() if k != "content" and v is not None}
            node["id"] = did
            node["type"] = "Document"
            node["text"] = text
            nodes.append(node)
        return _fallback_ingest_entities(nodes, None, client=client, graph=graph)
    return _ingest_docs(docs, source=source, domain=domain, client=client, graph=graph)


def _clean(props: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in props.items() if v is not None}


def ingest_job_templates(
    templates: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
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
                    "type": "JobTemplate",
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
                    "type": "usesInventory",
                }
            )
        proj = tpl.get("project")
        if proj is not None:
            relationships.append(
                {
                    "source": tpl_id,
                    "target": f"ansible:project:{proj}",
                    "type": "usesProject",
                }
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)


def ingest_jobs(
    jobs: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
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
                    "type": "Job",
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
                    "type": "launchedFrom",
                }
            )
        inv = job.get("inventory")
        if inv is not None:
            relationships.append(
                {
                    "source": job_id,
                    "target": f"ansible:inventory:{inv}",
                    "type": "usesInventory",
                }
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)


def ingest_inventories(
    inventories: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
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
                    "type": "Inventory",
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
                    "type": "inOrganization",
                }
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)


def ingest_hosts(
    hosts: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
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
                    "type": "Host",
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
                    "type": "belongsToInventory",
                }
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)


_INGESTORS = {
    "job_templates": ingest_job_templates,
    "jobs": ingest_jobs,
    "inventories": ingest_inventories,
    "hosts": ingest_hosts,
}
