"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_jobs`` / ``ingest_job_templates`` /
``ingest_inventories`` / ``ingest_hosts`` seam with a fake engine client (no engine
required), asserting the txn add_node/commit + edge calls and the Ansible Tower record
→ typed-node mapping. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from typing import Any

import msgpack
import pytest
from agent_utilities.knowledge_graph.memory.native_ingest import NativeIngestError
from agent_utilities.security.brain_context import ActorContext, use_actor
from agent_utilities.models.company_brain import ActorType
from agent_utilities.knowledge_graph.core.session import GraphSession, use_session

from ansible_tower_mcp.kg_ingest import (
    ingest_entities,
    ingest_hosts,
    ingest_inventories,
    ingest_job_templates,
    ingest_jobs,
)


@pytest.fixture(autouse=True)
def _governed_session():
    actor = ActorContext(
        actor_id="subject:opaque:synthetic",
        actor_type=ActorType.AUTOMATED_SERVICE,
        roles=(),
        tenant_id="tenant:opaque:synthetic",
        authenticated=True,
    )
    session = GraphSession(
        actor=actor,
        tenant=actor.tenant_id,
        scopes=frozenset({"kg:write"}),
        graph="graph:opaque:synthetic",
        policy_version="policy:opaque:synthetic",
        audience="epistemic-graph",
    )
    with use_actor(actor), use_session(session):
        yield


class _FakeNodes:
    def __init__(self) -> None:
        self.values: dict[str, dict[str, Any]] = {}

    def properties(self, node_id: str) -> dict[str, Any] | None:
        return self.values.get(node_id)

    def list(self) -> list[tuple[str, dict[str, Any]]]:
        return list(self.values.items())


class _FakeChanges:
    def __init__(self, nodes: _FakeNodes) -> None:
        self.nodes = nodes
        self.edges: list[tuple[str, str, dict[str, Any]]] = []
        self.applied: list[dict[str, Any]] = []
        self.records: dict[str, dict[str, Any]] = {}
        self.versions: dict[str, dict[str, Any]] = {}

    def get(self, envelope_id: str) -> dict[str, Any] | None:
        return self.records.get(envelope_id)

    def content_version(self, object_id: str) -> dict[str, Any] | None:
        return self.versions.get(object_id)

    def cursor(self, _source: str, _partition: str = "") -> None:
        return None

    def apply(self, envelope: dict[str, Any]) -> dict[str, Any]:
        self.applied.append(envelope)
        mutation = envelope["mutation"]
        for operation in mutation["operations"]:
            method = operation["method"]
            params = method["params"]
            properties = msgpack.unpackb(params["properties_msgpack"], raw=False)
            if method["method"] == "AddNode":
                self.nodes.values[params["node_id"]] = properties
            elif method["method"] == "AddEdge":
                self.edges.append(
                    (params["source_id"], params["target_id"], properties)
                )
        version = envelope["content_version"]
        self.versions[version["object_id"]] = version
        self.records[envelope["envelope_id"]] = envelope
        return {
            "batch_id": mutation["batch_id"],
            "replayed": False,
            "projection_pending": False,
        }


class _FakeRdf:
    def validate_shacl(self, _shapes: str, _data_graph: str) -> dict[str, Any]:
        return {"conforms": True, "results": []}


class _FakeClient:
    def __init__(self) -> None:
        self.nodes = _FakeNodes()
        self.changes = _FakeChanges(self.nodes)
        self.rdf = _FakeRdf()

    @staticmethod
    def supports(operation: str) -> bool:
        return operation == "ApplyChangeEnvelope"


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "Job", "name": "j"},
            {"id": "b", "node_type": "JobTemplate"},
        ],
        [{"source": "a", "target": "b", "relationship": "launchedFrom"}],
        client=c,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert len(c.changes.applied) == 1
    assert set(c.nodes.values) == {"a", "b"}
    # provenance is stamped
    assert c.nodes.values["a"]["source"] == "ansible-tower-mcp"
    assert c.nodes.values["a"]["domain"] == "ansible"
    assert c.changes.edges == [("a", "b", {"relationship": "launchedFrom"})]


def test_ingest_jobs_maps_job_and_links():
    c = _FakeClient()
    res = ingest_jobs(
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
        client=c,
    )
    assert res == {"nodes": 1, "edges": 2}
    node = c.nodes.values["ansible:job:512"]
    assert node["node_type"] == "Job"
    assert node["jobStatus"] == "successful"
    assert node["externalToolId"] == "512"
    assert (
        "ansible:job:512",
        "ansible:jobtemplate:7",
        {"relationship": "launchedFrom"},
    ) in c.changes.edges
    assert (
        "ansible:job:512",
        "ansible:inventory:4",
        {"relationship": "usesInventory"},
    ) in c.changes.edges


def test_ingest_job_templates_maps_template_and_project():
    c = _FakeClient()
    res = ingest_job_templates(
        [
            {
                "id": 7,
                "name": "site",
                "playbook": "site.yml",
                "inventory": 4,
                "project": 5,
            }
        ],
        client=c,
    )
    assert res == {"nodes": 1, "edges": 2}
    node = c.nodes.values["ansible:jobtemplate:7"]
    assert node["node_type"] == "JobTemplate"
    assert node["playbook"] == "site.yml"
    assert (
        "ansible:jobtemplate:7",
        "ansible:project:5",
        {"relationship": "usesProject"},
    ) in c.changes.edges


def test_ingest_inventories_and_hosts():
    c = _FakeClient()
    inv = ingest_inventories(
        [{"id": 4, "name": "prod", "organization": 1, "total_hosts": 3}],
        client=c,
    )
    assert inv == {"nodes": 1, "edges": 1}
    assert c.nodes.values["ansible:inventory:4"]["node_type"] == "Inventory"
    assert (
        "ansible:inventory:4",
        "ansible:organization:1",
        {"relationship": "inOrganization"},
    ) in c.changes.edges

    c2 = _FakeClient()
    hosts = ingest_hosts(
        [{"id": 22, "name": "web01", "inventory": 4, "enabled": True}],
        client=c2,
    )
    assert hosts == {"nodes": 1, "edges": 1}
    assert c2.nodes.values["ansible:host:22"]["node_type"] == "Host"
    assert (
        "ansible:host:22",
        "ansible:inventory:4",
        {"relationship": "belongsToInventory"},
    ) in c2.changes.edges


def test_ingest_rejects_legacy_structural_fields():
    with pytest.raises(NativeIngestError, match="canonical node_type"):
        ingest_entities([{"id": "legacy", "type": "Legacy"}], client=_FakeClient())

def test_ingest_empty_is_rejected():
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_entities([], client=_FakeClient())
