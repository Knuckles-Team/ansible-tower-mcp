---
name: ansible-tower-mcp-development
skill_type: skill
domain: development
description: >-
  Develop, test, gate, and release the ansible-tower-mcp connector. Use this
  skill when changing the connector's API mappings, MCP tools, packaging,
  documentation, or repository gates.
license: MIT
tags: [ansible-tower-mcp, development, connector, test, gates]
tier: repository
metadata:
  author: Genius
  version: '0.1.0'
---

# ansible-tower-mcp development

This repository owns the Ansible Tower/AWX transport, mappings, MCP tools, and
agent entry points. Shared connector contracts and transports belong to
`agent-connector-sdk`; admission, serving, and durable graph state belong to
their owning repositories. Read `AGENTS.md` before changing code and keep
provider credentials and endpoints out of source, logs, and skill content.

## Rapid delivery: the 5-minute contract

Specs are already designed. Deliver small, reviewable slices and cite the
owning spec row in the commit trailer.

- Find the owning row first with `git grep -n "<term>" -- specs` and extend
  that spec before adding new requirement text.
- Reuse existing SDK clients, transport policies, and tool factories. Do not
  create a second implementation of a connector capability.
- Keep changes scoped to this connector. A change owned by the SDK, Arbora,
  or the knowledge graph belongs in that repository instead.
- Every delivered requirement needs a bound test. Generated `status.json`
  files are produced by `pipelines-hook spec-status`; never hand-edit them.
- One logical change per commit, with `Spec: <ID>` and the assisting agent
  trailer adjacent in the final paragraph.

## Setup and gates

Use the pinned environment from `uv sync --locked`. Run the repository
gate from the checkout root:

```bash
uvx pre-commit run --all-files
```

For focused feedback, run the relevant tests with the repository's pinned
environment, for example:

```bash
uv run --all-extras pytest tests/test_basic.py -q
uv run --all-extras pytest tests/test_connector_tool_parity.py -q
```

The canonical `.pre-commit-config.yaml` delegates connector-standard,
secrets, spec, tests-fast, and dependency-readiness checks to
`Knuckles-Team/pipelines` at `rev: main`. Do not replace those shared hooks
with local copies or bypass a failing check.

## Connector-specific checks

- Keep the MCP and agent surfaces aligned with `agent-connector-sdk`.
- Validate environment and TLS settings before making provider calls.
- Mock external Tower/AWX calls in tests; never use live credentials in a
  local gate.
- Keep `ansible_tower_mcp/skills/` package data intact when adding skills.
- Documentation lives under `docs/` and is published by the shared Pages
  workflow; source status records live under `specs/`.

## Delivery discipline

Work in a real Git worktree based on `origin/main`. Inspect the complete diff,
stage only reviewed paths, and verify `git status --short` after every gate.
Do not use `git stash`, `git add -A`, or `git add .`; do not claim Pages
publication until a successful exact-source workflow run and the public page
are both observed.
