"""Epistemic-graph blob ingestion for job logs — Wire-First coverage.

Exercises ``ingest_job_log`` against a fake ``agent_connector_sdk.ingest``
transport (no engine required), asserting the stored media asset's bytes,
mime type, provenance/extra fields, and the asset id/digest returned from the
commit receipt's raw admissions. CONCEPT:AU-KG.ingest.list-durable-media.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from agent_connector_sdk.ingest import IngestError, KnowledgeIngest

from ansible_tower_mcp.kg_media import ingest_job_log


class _FakeTransport:
    def __init__(self) -> None:
        self.stored_blobs: list[bytes] = []
        self.requests: list[Any] = []

    async def source_status(self, _connector: str, _stream: str) -> Any:
        return SimpleNamespace(accepted_checkpoint=None)

    async def store_blob(self, data: bytes) -> str:
        self.stored_blobs.append(data)
        return "deadbeef"

    async def submit(self, request: Any) -> Any:
        self.requests.append(request)
        media_records = [r for r in request.records if r.record_id == "blob:deadbeef"]
        return SimpleNamespace(
            affected_count=len(request.records),
            relationship_count=len(request.relationships),
            raw_admissions=[
                SimpleNamespace(
                    record_id=record.record_id, raw_digest="deadbeef", deduplicated=False
                )
                for record in media_records
            ],
        )


@pytest.fixture
def ingest() -> tuple[KnowledgeIngest, _FakeTransport]:
    transport = _FakeTransport()
    return KnowledgeIngest(transport, loop=None), transport


@pytest.mark.asyncio
async def test_ingest_job_log_stores_blob(ingest):
    service, transport = ingest
    res = await ingest_job_log(
        512,
        "PLAY [all] ***\nok: [web01]\n",
        job_status="successful",
        ingest=service,
    )
    assert res == {"asset_id": "blob:deadbeef", "digest": "deadbeef", "size_bytes": 27}
    assert transport.stored_blobs == [b"PLAY [all] ***\nok: [web01]\n"]
    request = transport.requests[0]
    media_record = next(r for r in request.records if r.record_id == "blob:deadbeef")
    assert media_record.payload["mime_type"] == "text/plain"
    assert media_record.payload["name"] == "ansible-job-512.log"
    assert media_record.payload["job_id"] == "512"
    assert media_record.payload["status"] == "successful"


@pytest.mark.asyncio
async def test_ingest_job_log_accepts_bytes(ingest):
    service, transport = ingest
    res = await ingest_job_log(9, b"raw-bytes", ingest=service)
    assert res is not None
    assert res["size_bytes"] == len(b"raw-bytes")
    assert transport.stored_blobs == [b"raw-bytes"]


@pytest.mark.asyncio
async def test_ingest_job_log_noops_on_empty(ingest):
    service, transport = ingest
    assert await ingest_job_log(1, "", ingest=service) is None
    assert await ingest_job_log(None, "x", ingest=service) is None
    assert transport.stored_blobs == []


@pytest.mark.asyncio
async def test_ingest_job_log_propagates_commit_failure():
    class _FailingTransport(_FakeTransport):
        async def submit(self, request: Any) -> Any:
            raise RuntimeError("epistemic-graph is unreachable")

    service = KnowledgeIngest(_FailingTransport(), loop=None)
    with pytest.raises(IngestError):
        await ingest_job_log(1, "some log", ingest=service)
