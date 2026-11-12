# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.3.8] - 2026-11-12

### Changed
- Every Tower operation is one typed tool per client method (`ansible_tower_list_jobs`, `ansible_tower_launch_job`, ...). The hand-written `action`-routed tools (`ansible_tower_jobs`, `ansible_tower_hosts`, ...) are removed; the knowledge-graph ingest tools stay.
- Declare tool-use contracts, prompt and skill links, data locations and business roles; ship an operator and three business-role agent prompts; root every ontology class in a core class.
- Skills name the typed tools. Require `scion-sdk>=0.9.0,<0.10.0`.

## [3.3.7] - 2026-10-30

### Changed
- Require `scion-sdk>=0.6.4,<0.7.0`; `uv.lock` relocked.

## [3.3.3] - 2026-10-23

### Changed
- Requires `agent-connector-sdk>=0.4.1`; data sources are declared in code (`connector_sources`).

## [Unreleased]

### Added
-

### Changed
-

### Fixed
-

## [1.3.54] - 2026-04-29

### Added
- Initial release
