# ansible_tower_mcp/mcp/tools.py
"""Ansible Tower tools that are not client-method wrappers.

Every Tower operation is one typed tool per ``Api`` client method, registered by
the SDK. Only the knowledge-graph ingest tools are written by hand here.
"""

import json

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ansible_tower_mcp.auth import get_client


def register_kg_ingest_tools(mcp: FastMCP):
    """Wire-First native KG ingestion tools (AU-KG.ingest.enterprise-source-extractor)."""

    _LISTERS = {
        "job_templates": "list_job_templates",
        "jobs": "list_jobs",
        "inventories": "list_inventories",
        "hosts": "list_hosts",
    }

    @mcp.tool(tags={"kg_ingest", "kg"})
    async def ansible_ingest_resources(
        resource_type: str = Field(
            description="Resource to ingest. One of: 'job_templates', 'jobs', 'inventories', 'hosts'."
        ),
        params_json: str = Field(
            default="{}",
            description="JSON string of list filters (e.g. {'status':'failed'} for jobs, {'inventory_id':1} for hosts).",
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Natively ingest Ansible Tower resources into medulla as typed nodes.

        Lists the resource via the Ansible Tower API and pushes the records (with their
        ontology links) into the knowledge graph via the fast engine client. Best-effort:
        returns ``{"ingested": None}`` when no engine is reachable.
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        if ctx:
            await ctx.info(f"Ingesting {resource_type}...")

        from ansible_tower_mcp.kg_ingest import _INGESTORS

        method = _LISTERS.get(resource_type)
        ingestor = _INGESTORS.get(resource_type)
        if method is None or ingestor is None:
            return {"error": f"Unknown resource_type: {resource_type}"}

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        records = getattr(client, method)(**kwargs)
        if isinstance(records, dict):
            records = records.get("results", [records])
        result = await ingestor(records)
        return {
            "resource_type": resource_type,
            "listed": len(records),
            "ingested": result,
        }

    @mcp.tool(tags={"kg_ingest", "kg"})
    async def ansible_ingest_job_log(
        params_json: str = Field(
            default="{}",
            description="JSON string with 'job_id' (int, required) to fetch and store the job's stdout log as a KG blob.",
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Store an Ansible Tower job's stdout log as a durable :Blob in the KG.

        Fetches the job record + stdout and stores the raw log bytes content-addressed
        via MediaStore. Best-effort: returns ``{"stored": None}`` when no engine.
        CONCEPT:AU-KG.ingest.list-durable-media.
        """
        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}
        job_id = kwargs.get("job_id")
        if job_id is None:
            return {"error": "job_id is required"}
        if ctx:
            await ctx.info(f"Ingesting job {job_id} log...")

        from ansible_tower_mcp.kg_media import ingest_job_log

        job = client.get_job(job_id)
        stdout_resp = client.get_job_stdout(job_id, format="txt")
        stdout = (
            stdout_resp.get("stdout") if isinstance(stdout_resp, dict) else stdout_resp
        )
        stored = await ingest_job_log(
            job_id,
            stdout,
            job_status=job.get("status") if isinstance(job, dict) else None,
        )
        return {"job_id": job_id, "stored": stored}
