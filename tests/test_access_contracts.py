"""CONN-ANSIBLE-TOWER-MCP-CONNECTOR-CONTENT-R002: the competency read is
declared as an access contract and the recorded response satisfies it."""

import asyncio
import json
from importlib import resources
from pathlib import Path

import pytest
from fastmcp import Client
from scion_sdk.access_contract import parse_access_contracts
from scion_sdk.connector import build_server

from ansible_tower_mcp.api.api_client_base import BaseApiClient

ID = "CONN-ANSIBLE-TOWER-MCP-CONNECTOR-CONTENT-R002"
ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = parse_access_contracts(
    (ROOT / "ansible_tower_mcp/ontology/access_contracts.ttl").read_text()
)
ONTOLOGY = (
    resources.files("ansible_tower_mcp").joinpath("ontology", "ansible.ttl").read_text()
)
KG = "http://knuckles.team/kg#"


def _serve(monkeypatch, operation, recording):
    monkeypatch.setenv("ANSIBLE_BASE_URL", "https://tower.test")
    monkeypatch.setenv("ANSIBLE_USERNAME", "fixture")
    monkeypatch.setenv("ANSIBLE_PASSWORD", "fixture")
    monkeypatch.setenv("MCP_FLEET_REGISTRATION", "false")
    page = {"count": len(recording), "next": None, "results": recording}
    monkeypatch.setattr(BaseApiClient, "request", lambda self, *a, **kw: page)

    async def call():
        _, mcp = build_server("ansible_tower_mcp", command_args=[])
        async with Client(mcp) as client:
            assert operation in {t.name for t in await client.list_tools()}
            result = await client.call_tool(operation, {})
            return json.loads(result.content[0].text)

    return asyncio.run(call())


@pytest.mark.spec(ID)
def test_competency_contracts_certified(monkeypatch):
    (contract,) = CONTRACTS
    assert contract.entity == "job_run"
    assert contract.source_id == "ansible-tower-mcp"
    assert contract.access_kind == "mcp_tool"
    assert contract.pagination == "none"
    assert contract.key_field == "id"
    assert contract.class_iri == "http://knuckles.team/kg/infrastructure#AutomationJob"
    for prop, _field in contract.predicates:
        assert prop.startswith(KG)
        assert f"\n:{prop.removeprefix(KG)} a owl:" in ONTOLOGY, prop
    recording = json.loads((ROOT / "tests/recordings/job_run.json").read_text())
    assert recording
    served = _serve(monkeypatch, contract.operation, recording)
    assert served == recording
    for record in served:
        assert contract.key_field in record
        assert all(field in record for _, field in contract.predicates)


@pytest.mark.spec(ID)
def test_contract_refuses_a_recording_missing_a_bound_field():
    (contract,) = CONTRACTS
    record = {"id": 1, "status": "failed"}
    assert not all(field in record for _, field in contract.predicates)
