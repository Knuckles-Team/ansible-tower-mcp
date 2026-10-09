"""Epistemic-graph blob ingestion for Ansible Tower job logs.

CONCEPT:AU-KG.ingest.list-durable-media. A job's raw stdout log — potentially large,
ANSI-coloured playbook output — is stored as a content-addressed **blob** with a
``:Blob`` graph node in ONE cross-modal ACID commit, via the
``agent_connector_sdk.ingest`` knowledge-ingest facade (``ChangeSet.media`` +
``KnowledgeIngest.submit``). This makes the raw log bytes durable, deduped, and
queryable inside the knowledge graph, not just a transient API response.
"""

from __future__ import annotations

import logging
from typing import Any

from agent_connector_sdk.ingest import (
    ChangeSet,
    IngestBinding,
    KnowledgeIngest,
    MediaAsset,
    current_ingest,
)

logger = logging.getLogger("ansible_tower_mcp.kg_media")

_BINDING = IngestBinding(connector="ansible-tower-mcp", stream="ansible")


async def ingest_job_log(
    job_id: int | str | None,
    stdout: str | bytes | None,
    *,
    job_status: str | None = None,
    name: str | None = None,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, Any] | None:
    """Store a job's stdout log as a ``:Blob`` in the knowledge graph.

    Returns ``{asset_id, digest, size_bytes}`` on success. Invalid input returns
    ``None``; a refused commit raises ``IngestError``.
    """
    if job_id is None or not stdout:
        return None
    data = stdout.encode("utf-8", "replace") if isinstance(stdout, str) else stdout
    if not data:
        return None

    extra: dict[str, Any] = {"job_id": str(job_id)}
    if job_status is not None:
        extra["status"] = job_status
    blob_name = name or f"ansible-job-{job_id}.log"

    asset = MediaAsset(data=data, mime_type="text/plain", name=blob_name, properties=extra)
    change_set = ChangeSet(media=(asset,))
    service = ingest or current_ingest()
    receipt = await service.submit(_BINDING, change_set)
    admission = next(
        (a for a in receipt.raw_admissions if a.record_id.startswith("blob:")), None
    )
    if admission is None:
        return None

    logger.info(
        "KG blob ingest: stored job %s log (%d bytes) as asset %s",
        job_id,
        len(data),
        admission.record_id,
    )
    return {
        "asset_id": admission.record_id,
        "digest": admission.raw_digest,
        "size_bytes": len(data),
    }
