"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_jobs`` / ``ingest_job_templates`` /
``ingest_inventories`` / ``ingest_hosts`` seam with a fake engine client (no engine
required), asserting the txn add_node/commit + edge calls and the Ansible Tower record
→ typed-node mapping. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

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
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def commit(self, txn):
        self.committed = True
        return True


class _FakeEdges:
    def __init__(self):
        self.edges = []

    def add(self, src, dst, props):
        self.edges.append((src, dst, props))


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()
        self.edges = _FakeEdges()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "type": "Job", "name": "j"},
            {"id": "b", "type": "JobTemplate"},
        ],
        [{"source": "a", "target": "b", "type": "launchedFrom"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "b"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "ansible-tower-mcp"
    assert c.txn.nodes["a"]["domain"] == "ansible"
    assert c.edges.edges == [("a", "b", {"type": "launchedFrom"})]


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
    assert node["type"] == "Job"
    assert node["jobStatus"] == "successful"
    assert node["externalToolId"] == "512"
    assert (
        "ansible:job:512",
        "ansible:jobtemplate:7",
        {"type": "launchedFrom"},
    ) in c.edges.edges
    assert (
        "ansible:job:512",
        "ansible:inventory:4",
        {"type": "usesInventory"},
    ) in c.edges.edges


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
    assert node["type"] == "JobTemplate"
    assert node["playbook"] == "site.yml"
    assert (
        "ansible:jobtemplate:7",
        "ansible:project:5",
        {"type": "usesProject"},
    ) in c.edges.edges


def test_ingest_inventories_and_hosts():
    c = _FakeClient()
    inv = ingest_inventories(
        [{"id": 4, "name": "prod", "organization": 1, "total_hosts": 3}],
        client=c,
        graph="__commons__",
    )
    assert inv == {"nodes": 1, "edges": 1}
    assert c.txn.nodes["ansible:inventory:4"]["type"] == "Inventory"
    assert (
        "ansible:inventory:4",
        "ansible:organization:1",
        {"type": "inOrganization"},
    ) in c.edges.edges

    c2 = _FakeClient()
    hosts = ingest_hosts(
        [{"id": 22, "name": "web01", "inventory": 4, "enabled": True}],
        client=c2,
        graph="__commons__",
    )
    assert hosts == {"nodes": 1, "edges": 1}
    assert c2.txn.nodes["ansible:host:22"]["type"] == "Host"
    assert (
        "ansible:host:22",
        "ansible:inventory:4",
        {"type": "belongsToInventory"},
    ) in c2.edges.edges


def test_ingest_noops_without_engine():
    # No injected client + no reachable engine -> clean no-op.
    assert ingest_entities([{"id": "a", "type": "Job"}]) is None


def test_ingest_empty_is_noop():
    assert ingest_entities([], client=_FakeClient()) is None
    assert ingest_jobs([], client=_FakeClient()) is None
    assert ingest_hosts([], client=_FakeClient()) is None
