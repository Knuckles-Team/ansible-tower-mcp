"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_jobs`` / ``ingest_job_templates`` /
``ingest_inventories`` / ``ingest_hosts`` seam with a fake engine client (no engine
required), asserting the txn add_node/commit + edge calls and the Ansible Tower record
→ typed-node mapping. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

import pytest
from agent_utilities.knowledge_graph.memory.native_ingest import NativeIngestError

from ansible_tower_mcp.kg_ingest import (
    ingest_entities,
    ingest_hosts,
    ingest_inventories,
    ingest_job_templates,
    ingest_jobs,
)


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def add_edge(self, txn, src, dst, props):
        self.edges.append((src, dst, props))

    def commit(self, txn):
        self.committed = True
        return True



class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "Job", "name": "j"},
            {"id": "b", "node_type": "JobTemplate"},
        ],
        [{"source": "a", "target": "b", "relationship": "launchedFrom"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "b"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "ansible-tower-mcp"
    assert c.txn.nodes["a"]["domain"] == "ansible"
    assert c.txn.edges == [("a", "b", {"relationship": "launchedFrom"})]


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
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 2}
    node = c.txn.nodes["ansible:job:512"]
    assert node["node_type"] == "Job"
    assert node["jobStatus"] == "successful"
    assert node["externalToolId"] == "512"
    assert (
        "ansible:job:512",
        "ansible:jobtemplate:7",
        {"relationship": "launchedFrom"},
    ) in c.txn.edges
    assert (
        "ansible:job:512",
        "ansible:inventory:4",
        {"relationship": "usesInventory"},
    ) in c.txn.edges


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
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 2}
    node = c.txn.nodes["ansible:jobtemplate:7"]
    assert node["node_type"] == "JobTemplate"
    assert node["playbook"] == "site.yml"
    assert (
        "ansible:jobtemplate:7",
        "ansible:project:5",
        {"relationship": "usesProject"},
    ) in c.txn.edges


def test_ingest_inventories_and_hosts():
    c = _FakeClient()
    inv = ingest_inventories(
        [{"id": 4, "name": "prod", "organization": 1, "total_hosts": 3}],
        client=c,
        graph="__commons__",
    )
    assert inv == {"nodes": 1, "edges": 1}
    assert c.txn.nodes["ansible:inventory:4"]["node_type"] == "Inventory"
    assert (
        "ansible:inventory:4",
        "ansible:organization:1",
        {"relationship": "inOrganization"},
    ) in c.txn.edges

    c2 = _FakeClient()
    hosts = ingest_hosts(
        [{"id": 22, "name": "web01", "inventory": 4, "enabled": True}],
        client=c2,
        graph="__commons__",
    )
    assert hosts == {"nodes": 1, "edges": 1}
    assert c2.txn.nodes["ansible:host:22"]["node_type"] == "Host"
    assert (
        "ansible:host:22",
        "ansible:inventory:4",
        {"relationship": "belongsToInventory"},
    ) in c2.txn.edges


def test_ingest_rejects_legacy_structural_fields():
    with pytest.raises(NativeIngestError, match="canonical node_type"):
        ingest_entities([{"id": "legacy", "type": "Legacy"}], client=_FakeClient())

def test_ingest_empty_is_rejected():
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_entities([], client=_FakeClient())
