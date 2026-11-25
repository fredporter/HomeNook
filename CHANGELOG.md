# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Versioning:** `pyproject.toml` is the single source of truth for the
> installable `uhome-server` package; the runtime reads the same value from the
> installed distribution metadata. The repo-root `VERSION` file mirrors it.

## [0.1.0] - 2026-11-25

First published release, published from `main` as HomeNook v0.1.0. Earlier
product lines were never released from this repository; their notes remain in
git history.

### Added

- FastAPI server (`uhome_server.app`) covering health, dashboard, household,
  channels, playback, library, launcher, client, platform, containers, network,
  runtime and USX routes, plus the server-rendered thin kiosk pages.
- Thin kiosk UI for home, media and automation, shipped as package data
  (`uhome_server/templates/thin`, `uhome_server/static/thin`) so an installed
  wheel renders the pages without a source checkout.
- `homenook` operator CLI with `launcher`, `installer`, `backup`, `contracts` and
  `migrate` subcommands, `homenook-launcher` and `homenook-installer` entry
  points, and `homenook --version`.
- Installer lane: bundle manifest and checksum helpers, preflight, plan, staging,
  execute, apply, verify, promotion and rollback commands, with Linux and Sonic
  asset adapters.
- Shared contract assets for sync records and the network policy, checked in with
  JSON Schema companions.
- Job queue, rules engine, household, channel, client-capability, cluster,
  playback and Home Assistant services.
- Backup and restore, sync stores, and the wizard-to-kiosk migration.

### Changed

- The version is stated once in `pyproject.toml`; `__version__`, the wheel
  metadata, the FastAPI version and `homenook --version` all report it.
- `uhome` is kept as the short form for the package, module and CLI aliases
  alongside the `homenook` command names.

### Release engineering

- Publishing is a GitHub Release from a `v*.*.*` tag. The workflow refuses to
  publish unless the tag and `project.version` agree, runs `twine check --strict`,
  installs the wheel outside the checkout to assert `homenook --version` and
  render the thin home page, then attaches the wheel and sdist.
- PyPI is not configured; enabling it requires `PYPI_API_TOKEN` or trusted
  publishing. See `docs/RELEASE-POLICY.md`.
