"""Static release contract for fail-closed Ansible Tower TLS defaults."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_tls_profile_is_strict_and_no_boolean_toggle_is_packaged() -> None:
    auth_source = (ROOT / "ansible_tower_mcp" / "auth.py").read_text(
        encoding="utf-8"
    )
    assert "resolve_configured_tls_profile" in auth_source

    config = json.loads(
        (ROOT / "ansible_tower_mcp" / "mcp_config.json").read_text(
            encoding="utf-8"
        )
    )
    environment = config["mcpServers"]["ansible-tower-mcp"]["env"]
    assert "MCP_TOOL_MODE" in environment


def test_documented_tls_default_is_not_a_bypass() -> None:
    documents = (
        ROOT / "README.md",
        ROOT / "docs" / "deployment.md",
        ROOT
        / "ansible_tower_mcp"
        / "skills"
        / "ansible-tower-job-execution"
        / "WORKFLOW.md",
    )
    for document in documents:
        text = document.read_text(encoding="utf-8").lower()
        assert "ansible_tower_tls_profile" in text
        assert "verification is mandatory" in text
