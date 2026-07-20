# ansible_tower_mcp/mcp/tools.py
import json

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ansible_tower_mcp.auth import get_client

# CONCEPT:AT-OS.config.route-workflow-templates-operations: Ansible Tower Resource API Adapters


def register_inventory_tools(mcp: FastMCP):
    """CONCEPT:AT-OS.config.route-workflow-templates-operations: Register inventory tools with FastMCP."""

    @mcp.tool(tags={"inventory"})
    async def ansible_tower_inventory(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_inventories', 'get_inventory', 'create_inventory', 'update_inventory', 'delete_inventory'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower inventory operations.

        CONCEPT:AT-OS.config.route-workflow-templates-operations: Route inventory operations to standard API client methods.
        """
        if ctx:
            await ctx.info("Executing tool...")

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_inventories":
            return client.list_inventories(**kwargs)
        if action == "get_inventory":
            return client.get_inventory(**kwargs)
        if action == "create_inventory":
            return client.create_inventory(**kwargs)
        if action == "update_inventory":
            return client.update_inventory(**kwargs)
        if action == "delete_inventory":
            return client.delete_inventory(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_hosts_tools(mcp: FastMCP):
    """CONCEPT:AT-OS.config.route-workflow-templates-operations: Register host tools with FastMCP."""

    @mcp.tool(tags={"hosts"})
    async def ansible_tower_hosts(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_hosts', 'get_host', 'create_host', 'update_host', 'delete_host'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower hosts operations.

        CONCEPT:AT-OS.config.route-workflow-templates-operations: Route host operations to standard API client methods.
        """
        if ctx:
            await ctx.info("Executing tool...")

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_hosts":
            return client.list_hosts(**kwargs)
        if action == "get_host":
            return client.get_host(**kwargs)
        if action == "create_host":
            return client.create_host(**kwargs)
        if action == "update_host":
            return client.update_host(**kwargs)
        if action == "delete_host":
            return client.delete_host(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_groups_tools(mcp: FastMCP):
    """CONCEPT:AT-OS.config.route-workflow-templates-operations: Register group tools with FastMCP."""

    @mcp.tool(tags={"groups"})
    async def ansible_tower_groups(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_groups', 'get_group', 'create_group', 'update_group', 'delete_group', 'add_host_to_group', 'remove_host_from_group'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower groups operations.

        CONCEPT:AT-OS.config.route-workflow-templates-operations: Route group operations to standard API client methods.
        """
        if ctx:
            await ctx.info("Executing tool...")

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_groups":
            return client.list_groups(**kwargs)
        if action == "get_group":
            return client.get_group(**kwargs)
        if action == "create_group":
            return client.create_group(**kwargs)
        if action == "update_group":
            return client.update_group(**kwargs)
        if action == "delete_group":
            return client.delete_group(**kwargs)
        if action == "add_host_to_group":
            return client.add_host_to_group(**kwargs)
        if action == "remove_host_from_group":
            return client.remove_host_from_group(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_job_templates_tools(mcp: FastMCP):
    """CONCEPT:AT-OS.config.route-workflow-templates-operations: Register job templates tools with FastMCP."""

    @mcp.tool(tags={"job-templates"})
    async def ansible_tower_job_templates(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_job_templates', 'get_job_template', 'create_job_template', 'update_job_template', 'delete_job_template', 'launch_job'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower job templates operations.

        CONCEPT:AT-OS.config.route-workflow-templates-operations: Route job templates operations to standard API client methods.
        """
        if ctx:
            await ctx.info("Executing tool...")

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_job_templates":
            return client.list_job_templates(**kwargs)
        if action == "get_job_template":
            return client.get_job_template(**kwargs)
        if action == "create_job_template":
            return client.create_job_template(**kwargs)
        if action == "update_job_template":
            return client.update_job_template(**kwargs)
        if action == "delete_job_template":
            return client.delete_job_template(**kwargs)
        if action == "launch_job":
            return client.launch_job(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_jobs_tools(mcp: FastMCP):
    """CONCEPT:AT-OS.config.route-workflow-templates-operations: Register jobs tools with FastMCP."""

    @mcp.tool(tags={"jobs"})
    async def ansible_tower_jobs(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_jobs', 'get_job', 'cancel_job', 'relaunch_job', 'get_job_events', 'get_job_stdout'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower jobs operations.

        CONCEPT:AT-OS.config.route-workflow-templates-operations: Route jobs operations to standard API client methods.
        """
        if ctx:
            await ctx.info("Executing tool...")

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_jobs":
            return client.list_jobs(**kwargs)
        if action == "get_job":
            return client.get_job(**kwargs)
        if action == "cancel_job":
            return client.cancel_job(**kwargs)
        if action == "relaunch_job":
            return client.relaunch_job(**kwargs)
        if action == "get_job_events":
            return client.get_job_events(**kwargs)
        if action == "get_job_stdout":
            return client.get_job_stdout(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_projects_tools(mcp: FastMCP):
    """CONCEPT:AT-OS.config.route-workflow-templates-operations: Register projects tools with FastMCP."""

    @mcp.tool(tags={"projects"})
    async def ansible_tower_projects(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_projects', 'get_project', 'create_project', 'update_project', 'delete_project', 'sync_project'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower projects operations.

        CONCEPT:AT-OS.config.route-workflow-templates-operations: Route projects operations to standard API client methods.
        """
        if ctx:
            await ctx.info("Executing tool...")

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_projects":
            return client.list_projects(**kwargs)
        if action == "get_project":
            return client.get_project(**kwargs)
        if action == "create_project":
            return client.create_project(**kwargs)
        if action == "update_project":
            return client.update_project(**kwargs)
        if action == "delete_project":
            return client.delete_project(**kwargs)
        if action == "sync_project":
            return client.sync_project(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_credentials_tools(mcp: FastMCP):
    """CONCEPT:AT-OS.config.route-workflow-templates-operations: Register credentials tools with FastMCP."""

    @mcp.tool(tags={"credentials"})
    async def ansible_tower_credentials(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_credentials', 'get_credential', 'list_credential_types', 'create_credential', 'update_credential', 'delete_credential'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower credentials operations.

        CONCEPT:AT-OS.config.route-workflow-templates-operations: Route credentials operations to standard API client methods.
        """
        if ctx:
            await ctx.info("Executing tool...")

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_credentials":
            return client.list_credentials(**kwargs)
        if action == "get_credential":
            return client.get_credential(**kwargs)
        if action == "list_credential_types":
            return client.list_credential_types(**kwargs)
        if action == "create_credential":
            return client.create_credential(**kwargs)
        if action == "update_credential":
            return client.update_credential(**kwargs)
        if action == "delete_credential":
            return client.delete_credential(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_organizations_tools(mcp: FastMCP):
    """CONCEPT:AT-OS.config.route-workflow-templates-operations: Register organizations tools with FastMCP."""

    @mcp.tool(tags={"organizations"})
    async def ansible_tower_organizations(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_organizations', 'get_organization', 'create_organization', 'update_organization', 'delete_organization'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower organizations operations.

        CONCEPT:AT-OS.config.route-workflow-templates-operations: Route organizations operations to standard API client methods.
        """
        if ctx:
            await ctx.info("Executing tool...")

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_organizations":
            return client.list_organizations(**kwargs)
        if action == "get_organization":
            return client.get_organization(**kwargs)
        if action == "create_organization":
            return client.create_organization(**kwargs)
        if action == "update_organization":
            return client.update_organization(**kwargs)
        if action == "delete_organization":
            return client.delete_organization(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_teams_tools(mcp: FastMCP):
    """CONCEPT:AT-OS.config.route-workflow-templates-operations: Register teams tools with FastMCP."""

    @mcp.tool(tags={"teams"})
    async def ansible_tower_teams(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_teams', 'get_team', 'create_team', 'update_team', 'delete_team'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower teams operations.

        CONCEPT:AT-OS.config.route-workflow-templates-operations: Route teams operations to standard API client methods.
        """
        if ctx:
            await ctx.info("Executing tool...")

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_teams":
            return client.list_teams(**kwargs)
        if action == "get_team":
            return client.get_team(**kwargs)
        if action == "create_team":
            return client.create_team(**kwargs)
        if action == "update_team":
            return client.update_team(**kwargs)
        if action == "delete_team":
            return client.delete_team(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_users_tools(mcp: FastMCP):
    """CONCEPT:AT-OS.config.route-workflow-templates-operations: Register users tools with FastMCP."""

    @mcp.tool(tags={"users"})
    async def ansible_tower_users(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_users', 'get_user', 'create_user', 'update_user', 'delete_user'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower users operations.

        CONCEPT:AT-OS.config.route-workflow-templates-operations: Route users operations to standard API client methods.
        """
        if ctx:
            await ctx.info("Executing tool...")

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_users":
            return client.list_users(**kwargs)
        if action == "get_user":
            return client.get_user(**kwargs)
        if action == "create_user":
            return client.create_user(**kwargs)
        if action == "update_user":
            return client.update_user(**kwargs)
        if action == "delete_user":
            return client.delete_user(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_ad_hoc_commands_tools(mcp: FastMCP):
    """CONCEPT:AT-OS.config.route-workflow-templates-operations: Register ad-hoc commands tools with FastMCP."""

    @mcp.tool(tags={"ad_hoc_commands"})
    async def ansible_tower_ad_hoc_commands(
        action: str = Field(
            description="Action to perform. Must be one of: 'run_ad_hoc_command', 'get_ad_hoc_command', 'cancel_ad_hoc_command'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower ad hoc commands operations.

        CONCEPT:AT-OS.config.route-workflow-templates-operations: Route ad-hoc commands operations to standard API client methods.
        """
        if ctx:
            await ctx.info("Executing tool...")

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "run_ad_hoc_command":
            return client.run_ad_hoc_command(**kwargs)
        if action == "get_ad_hoc_command":
            return client.get_ad_hoc_command(**kwargs)
        if action == "cancel_ad_hoc_command":
            return client.cancel_ad_hoc_command(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_workflow_templates_tools(mcp: FastMCP):
    """CONCEPT:AT-OS.config.route-workflow-templates-operations: Register workflow templates tools with FastMCP."""

    @mcp.tool(tags={"workflow_templates"})
    async def ansible_tower_workflow_templates(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_workflow_templates', 'get_workflow_template', 'launch_workflow'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower workflow templates operations.

        CONCEPT:AT-OS.config.route-workflow-templates-operations: Route workflow templates operations to standard API client methods.
        """
        if ctx:
            await ctx.info("Executing tool...")

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_workflow_templates":
            return client.list_workflow_templates(**kwargs)
        if action == "get_workflow_template":
            return client.get_workflow_template(**kwargs)
        if action == "launch_workflow":
            return client.launch_workflow(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_workflow_jobs_tools(mcp: FastMCP):
    """CONCEPT:AT-OS.config.route-workflow-templates-operations: Register workflow jobs tools with FastMCP."""

    @mcp.tool(tags={"workflow_jobs"})
    async def ansible_tower_workflow_jobs(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_workflow_jobs', 'get_workflow_job', 'cancel_workflow_job'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower workflow jobs operations.

        CONCEPT:AT-OS.config.route-workflow-templates-operations: Route workflow jobs operations to standard API client methods.
        """
        if ctx:
            await ctx.info("Executing tool...")

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_workflow_jobs":
            return client.list_workflow_jobs(**kwargs)
        if action == "get_workflow_job":
            return client.get_workflow_job(**kwargs)
        if action == "cancel_workflow_job":
            return client.cancel_workflow_job(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_schedules_tools(mcp: FastMCP):
    """CONCEPT:AT-OS.config.route-workflow-templates-operations: Register schedules tools with FastMCP."""

    @mcp.tool(tags={"schedules"})
    async def ansible_tower_schedules(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_schedules', 'get_schedule', 'create_schedule', 'update_schedule', 'delete_schedule'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower schedules operations.

        CONCEPT:AT-OS.config.route-workflow-templates-operations: Route schedules operations to standard API client methods.
        """
        if ctx:
            await ctx.info("Executing tool...")

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_schedules":
            return client.list_schedules(**kwargs)
        if action == "get_schedule":
            return client.get_schedule(**kwargs)
        if action == "create_schedule":
            return client.create_schedule(**kwargs)
        if action == "update_schedule":
            return client.update_schedule(**kwargs)
        if action == "delete_schedule":
            return client.delete_schedule(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_system_tools(mcp: FastMCP):
    """CONCEPT:AT-OS.config.route-workflow-templates-operations: Register system tools with FastMCP."""

    @mcp.tool(tags={"system"})
    async def ansible_tower_system(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_ansible_version', 'get_dashboard_stats', 'get_metrics'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage ansible tower system operations.

        CONCEPT:AT-OS.config.route-workflow-templates-operations: Route system operations to standard API client methods.
        """
        if ctx:
            await ctx.info("Executing tool...")

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_ansible_version":
            return client.get_ansible_version(**kwargs)
        if action == "get_dashboard_stats":
            return client.get_dashboard_stats(**kwargs)
        if action == "get_metrics":
            return client.get_metrics(**kwargs)
        raise ValueError(f"Unknown action: {action}")


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
        """Natively ingest Ansible Tower resources into epistemic-graph as typed nodes.

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
        except Exception as e:
            return {"error": "Operation failed"}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        records = getattr(client, method)(**kwargs)
        if isinstance(records, dict):
            records = records.get("results", [records])
        result = ingestor(records)
        return {"resource_type": resource_type, "listed": len(records), "ingested": result}

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
        except Exception as e:
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
            stdout_resp.get("stdout")
            if isinstance(stdout_resp, dict)
            else stdout_resp
        )
        stored = ingest_job_log(
            job_id, stdout, job_status=job.get("status") if isinstance(job, dict) else None
        )
        return {"job_id": job_id, "stored": stored}
