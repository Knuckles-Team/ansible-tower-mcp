"""Native epistemic-graph blob ingestion for job logs — Wire-First coverage.

Exercises ``ingest_job_log`` with a fake ``MediaStore`` (no engine required),
asserting the store_media call, byte encoding, and provenance/extra fields.
CONCEPT:AU-KG.ingest.list-durable-media.
"""

from __future__ import annotations

import pytest
from agent_utilities.knowledge_graph.memory.native_ingest import NativeIngestError

import ansible_tower_mcp.kg_media as kg_media
from ansible_tower_mcp.kg_media import ingest_job_log


class _Stored:
    def __init__(self, asset_id, digest):
        self.asset_id = asset_id
        self.digest = digest


class _FakeStore:
    def __init__(self):
        self.calls = []

    def store_media(self, data, *, media_type, mime_type, source, name, extra):
        self.calls.append(
            {
                "data": data,
                "media_type": media_type,
                "mime_type": mime_type,
                "source": source,
                "name": name,
                "extra": extra,
            }
        )
        return _Stored("asset-1", "deadbeef")


def test_ingest_job_log_stores_blob():
    store = _FakeStore()
    res = ingest_job_log(
        512,
        "PLAY [all] ***\nok: [web01]\n",
        job_status="successful",
        media_store=store,
    )
    assert res == {"asset_id": "asset-1", "digest": "deadbeef", "size_bytes": 27}
    call = store.calls[0]
    assert call["media_type"] == "file"
    assert call["mime_type"] == "text/plain"
    assert call["source"] == "ansible-tower-mcp"
    assert call["name"] == "ansible-job-512.log"
    assert call["extra"] == {"job_id": "512", "status": "successful"}
    assert isinstance(call["data"], bytes)


def test_ingest_job_log_accepts_bytes():
    store = _FakeStore()
    res = ingest_job_log(9, b"raw-bytes", media_store=store)
    assert res is not None
    assert res["size_bytes"] == len(b"raw-bytes")
    assert store.calls[0]["data"] == b"raw-bytes"


def test_ingest_job_log_noops_on_empty():
    store = _FakeStore()
    assert ingest_job_log(1, "", media_store=store) is None
    assert ingest_job_log(None, "x", media_store=store) is None
    assert store.calls == []


def test_ingest_job_log_propagates_native_failure(monkeypatch):
    def fail():
        raise NativeIngestError("native media store is unavailable")

    monkeypatch.setattr(kg_media, "_native_media_store", fail)
    with pytest.raises(NativeIngestError, match="unavailable"):
        ingest_job_log(1, "some log")
