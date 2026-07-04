"""Native epistemic-graph blob ingestion for Ansible Tower job logs.

CONCEPT:AU-KG.ingest.list-durable-media. A job's raw stdout log — potentially large,
ANSI-coloured playbook output — is stored as a content-addressed **blob** with a
``:Blob`` graph node in ONE cross-modal ACID commit, via the agent-utilities
``MediaStore`` (obtained through the shared ``native_ingest.media_store``). This makes
the raw log bytes durable, deduped, and queryable inside the knowledge graph, not just
a transient API response.

Entirely best-effort and dependency-/engine-guarded: with no agent-utilities KG stack
or no reachable engine, every entry point **no-ops** (returns ``None``), so the
connector keeps working with zero KG infrastructure.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("ansible_tower_mcp.kg_media")

_SOURCE = "ansible-tower-mcp"


def _media_store(media_store: Any | None = None) -> Any | None:
    """Return a ``MediaStore`` over a live engine, or ``None`` when unavailable."""
    if media_store is not None:
        return media_store
    try:
        from agent_utilities.knowledge_graph.memory.native_ingest import (
            media_store as _ms,
        )
    except Exception as e:  # noqa: BLE001 — shared primitive absent
        logger.debug("KG blob ingest unavailable (import): %s", e)
        return None
    try:
        return _ms()
    except Exception as e:  # noqa: BLE001 — engine unreachable
        logger.debug("KG blob ingest: engine unreachable: %s", e)
        return None


def ingest_job_log(
    job_id: int | str | None,
    stdout: str | bytes | None,
    *,
    job_status: str | None = None,
    name: str | None = None,
    source: str = _SOURCE,
    media_store: Any | None = None,
) -> dict[str, Any] | None:
    """Store a job's stdout log as a ``:Blob`` in the knowledge graph.

    Returns ``{asset_id, digest, size_bytes}`` on success, or ``None`` when there is
    no engine, no log, or the store failed (never raises). ``media_store`` may be
    injected (tests); otherwise one is built on demand.
    """
    if job_id is None or not stdout:
        return None
    store = _media_store(media_store)
    if store is None:
        return None

    data = stdout.encode("utf-8", "replace") if isinstance(stdout, str) else stdout
    if not data:
        return None

    extra = {"job_id": str(job_id)}
    if job_status is not None:
        extra["status"] = job_status
    blob_name = name or f"ansible-job-{job_id}.log"

    try:
        stored = store.store_media(
            data,
            media_type="file",
            mime_type="text/plain",
            source=source,
            name=blob_name,
            extra=extra,
        )
    except Exception as e:  # noqa: BLE001 — engine/store failure is non-fatal
        logger.warning("KG blob ingest: store_media failed: %s", e)
        return None
    if stored is None:
        return None

    logger.info(
        "KG blob ingest: stored job %s log (%d bytes) as asset %s",
        job_id,
        len(data),
        getattr(stored, "asset_id", "?"),
    )
    return {
        "asset_id": getattr(stored, "asset_id", None),
        "digest": getattr(stored, "digest", None),
        "size_bytes": len(data),
    }
