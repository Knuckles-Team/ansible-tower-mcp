# Usage — MCP / API / CLI

`ansible-tower-mcp` exposes the same capability three ways: as **MCP tools** an
agent calls, as a **Python API** (`Api`) you import, and as a **CLI** that runs
the server processes. The complete tool surface and the ecosystem role are
described in [Overview](overview.md).

## As an MCP server

Once [deployed](deployment.md), the server registers one consolidated,
action-routed tool per resource domain. Each tool takes an `action` argument
and a JSON `params` string, and each domain can be enabled or disabled with its
`*TOOL` environment switch.

| Domain | Toggle | Representative actions |
|---|---|---|
| Inventory | `INVENTORYTOOL` | `list_inventories`, `get_inventory`, `create_inventory`, `update_inventory`, `delete_inventory` |
| Hosts | `HOSTSTOOL` | `list_hosts`, `get_host`, `create_host`, `update_host`, `delete_host` |
| Groups | `GROUPSTOOL` | `list_groups`, `create_group`, `add_host_to_group`, `remove_host_from_group` |
| Job Templates | `JOB_TEMPLATESTOOL` | `list_job_templates`, `launch_job`, `create_job_template`, `update_job_template` |
| Jobs | `JOBSTOOL` | `list_jobs`, `get_job`, `cancel_job`, `get_job_stdout`, `get_job_events` |
| Projects | `PROJECTSTOOL` | `list_projects`, `get_project`, `update_project` |
| Credentials | `CREDENTIALSTOOL` | `list_credentials`, `get_credential`, `create_credential` |
| Organizations / Teams / Users | `ORGANIZATIONSTOOL` / `TEAMSTOOL` / `USERSTOOL` | list / get / create / update |
| Schedules | `SCHEDULESTOOL` | `list_schedules`, `create_schedule` |
| System | `SYSTEMTOOL` | `get_ansible_version`, `get_dashboard_stats`, `get_metrics` |

Example agent prompts that map onto these tools:

- *"List the job templates in Tower"* → Job Templates → `list_job_templates`
- *"Launch job template 42 and show me the output"* → Job Templates → `launch_job`, then Jobs → `get_job_stdout`
- *"What hosts are in the production inventory?"* → Hosts → `list_hosts`

## As a Python API

`Api` is a `requests`-based facade over the Tower / AWX `/api/v2/` REST surface.
It resolves authentication from a token, a username / password pair, or an OAuth
client id / secret pair.

```python
from ansible_tower_mcp.api_client import Api
from agent_utilities.core.transport_security import resolve_configured_tls_profile

api = Api(
    base_url="https://your-tower.example.com",
    username="admin",
    password="secret",
    tls_profile=resolve_configured_tls_profile("ANSIBLE_TOWER"),
)

# Reads
version = api.get_ansible_version()            # controller version
stats = api.get_dashboard_stats()              # dashboard counters
inventories = api.list_inventories()           # paginated records
templates = api.list_job_templates()           # job templates
jobs = api.list_jobs()                          # recent jobs
```

Build a client straight from the environment (resolves OIDC delegation, OAuth,
or username / password automatically):

```python
from ansible_tower_mcp.auth import get_client
api = get_client()        # reads ANSIBLE_* from the environment / .env
```

### Launching work

```python
# Launch a job template and follow its output
launched = api.launch_job(template_id=42)
job_id = launched["id"]
events = api.get_job_events(job_id)
stdout = api.get_job_stdout(job_id, format="txt")

# Cancel a running job
api.cancel_job(job_id)
```

## As a CLI

The package installs two console scripts:

```bash
# The MCP server (stdio by default; see Deployment for transports)
ansible-tower-mcp --transport streamable-http --host 0.0.0.0 --port 8000

# The A2A agent server (graph-routed Pydantic-AI agent)
ansible-tower-agent --host 0.0.0.0 --port 9012 --mcp-url http://localhost:8000/mcp
```

Both scripts accept `--help` to list every flag. The agent server reads
`PROVIDER` / `MODEL_ID` (and the provider's API key) to select its language
model; see [Deployment](deployment.md#run-the-agent-server).
