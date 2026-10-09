"""Epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_jobs`` / ``ingest_job_templates`` /
``ingest_inventories`` / ``ingest_hosts`` seam against a fake
``agent_connector_sdk.ingest`` transport (no engine required). The real SDK request
builder (``agent_connector_sdk.ingest.request.build_request``) still runs, so a
malformed change set is still caught by the SDK's own contract, not re-derived here;
only the final network commit is faked. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from agent_connector_sdk.ingest import IngestError, KnowledgeIngest
from epistemic_graph.generated.source_ingestion import SourceIngestionRequest

from ansible_tower_mcp.kg_ingest import (
    ingest_entities,
    ingest_hosts,
    ingest_inventories,
    ingest_job_templates,
    ingest_jobs,
)


class _FakeTransport:
    """Records every submitted request; no epistemic-graph engine required."""

    def __init__(self) -> None:
        self.requests: list[SourceIngestionRequest] = []

    async def source_status(self, _connector: str, _stream: str) -> Any:
        return SimpleNamespace(accepted_checkpoint=None)

    async def submit(self, request: SourceIngestionRequest) -> Any:
        self.requests.append(request)
        return SimpleNamespace(
            affected_count=len(request.records),
            relationship_count=len(request.relationships),
        )

    async def store_blob(self, _data: bytes) -> str:
        raise AssertionError("ansible-tower-mcp topology ingestion carries no media")


@pytest.fixture
def ingest() -> tuple[KnowledgeIngest, _FakeTransport]:
    transport = _FakeTransport()
    return KnowledgeIngest(transport, loop=None), transport


@pytest.mark.asyncio
async def test_ingest_entities_writes_nodes_and_edges(ingest):
    service, transport = ingest
    res = await ingest_entities(
        [
            {"id": "a", "node_type": "Job", "name": "j"},
            {"id": "b", "node_type": "JobTemplate"},
        ],
        [{"source": "a", "target": "b", "relationship": "launchedFrom"}],
        ingest=service,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert len(transport.requests) == 1
    request = transport.requests[0]
    record_ids = {record.record_id for record in request.records}
    assert record_ids == {"a", "b"}
    a_record = next(r for r in request.records if r.record_id == "a")
    assert a_record.payload["name"] == "j"
    assert request.relationships[0].relation_reference.endswith(
        "resources/Job/relations/launchedFrom"
    )


@pytest.mark.asyncio
async def test_ingest_jobs_maps_job_and_links(ingest):
    service, transport = ingest
    res = await ingest_jobs(
        [
            {
                "id": 512,
                "name": "deploy",
                "status": "successful",
                "elapsed": 12.3,
                "job_template": 7,
                "inventory": 4,
            }
        ],
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 2}
    request = transport.requests[0]
    record = next(r for r in request.records if r.record_id == "ansible:job:512")
    assert record.payload["jobStatus"] == "successful"
    assert record.payload["externalToolId"] == "512"
    relation_refs = {r.relation_reference for r in request.relationships}
    assert any(ref.endswith("relations/launchedFrom") for ref in relation_refs)
    assert any(ref.endswith("relations/usesInventory") for ref in relation_refs)


@pytest.mark.asyncio
async def test_ingest_job_templates_maps_template_and_project(ingest):
    service, transport = ingest
    res = await ingest_job_templates(
        [
            {
                "id": 7,
                "name": "site",
                "playbook": "site.yml",
                "inventory": 4,
                "project": 5,
            }
        ],
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 2}
    request = transport.requests[0]
    record = next(
        r for r in request.records if r.record_id == "ansible:jobtemplate:7"
    )
    assert record.payload["playbook"] == "site.yml"
    relation_refs = {r.relation_reference for r in request.relationships}
    assert any(ref.endswith("relations/usesProject") for ref in relation_refs)


@pytest.mark.asyncio
async def test_ingest_inventories_and_hosts(ingest):
    service, transport = ingest
    inv = await ingest_inventories(
        [{"id": 4, "name": "prod", "organization": 1, "total_hosts": 3}],
        ingest=service,
    )
    assert inv == {"nodes": 1, "edges": 1}
    inv_record = next(
        r for r in transport.requests[0].records if r.record_id == "ansible:inventory:4"
    )
    assert inv_record.payload["name"] == "prod"

    service2 = KnowledgeIngest(_FakeTransport(), loop=None)
    hosts = await ingest_hosts(
        [{"id": 22, "name": "web01", "inventory": 4, "enabled": True}],
        ingest=service2,
    )
    assert hosts == {"nodes": 1, "edges": 1}


@pytest.mark.asyncio
async def test_ingest_rejects_missing_node_type(ingest):
    service, _ = ingest
    with pytest.raises(IngestError):
        await ingest_entities([{"id": "legacy"}], ingest=service)


@pytest.mark.asyncio
async def test_ingest_empty_is_rejected(ingest):
    service, _ = ingest
    with pytest.raises(IngestError, match="at least one entity"):
        await ingest_entities([], ingest=service)
