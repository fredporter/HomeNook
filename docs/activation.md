---
title: "HomeNook activation (uHOME server)"
status: draft
last_updated: 2026-04-22T23:26:13+10:00
category: documentation
tags: [ucode3]
description: "This document marks the first active implementation tranche for"
---
# HomeNook activation (uHOME server)

## Purpose

This document marks the first active implementation tranche for
**HomeNook** (**v3.9.x**).

The activation goal is to make the server runnable, testable, and teachable as
the always-on local-service runtime without broadening its ownership beyond:

- persistent local services
- scheduling and recurrence
- home/server infrastructure modules
- operator-facing install and runtime checks for server-owned surfaces

## Activated Surfaces

- `src/uhome_server/app.py` as the current FastAPI runtime entrypoint
- `src/uhome_server/cli.py` as the local operator command lane
- `tests/` as the server validation lane
- `scripts/run-uhome-server-checks.sh` as the repo validation entrypoint
- `examples/basic-uhome-server-session.md` as the smallest operator walkthrough

## Current Validation Contract

Run:

```bash
scripts/run-uhome-server-checks.sh
```

This command:

- bootstraps a local `~/.udos/venv/uhome-server` runtime only when needed
- installs the editable dev dependencies
- runs the current `pytest` suite for the active server package

## GitHub Actions

The family reusable workflows that used to live in `fredporter/uDOS-dev`
(`validate.yml`, `family-policy-check.yml`, `promote.yml`, `release.yml`) were
retired when that repository was deleted. A call to a missing reusable workflow
fails to load, so the calling workflows ran no jobs and reported nothing. Every
workflow in this repository is now self-contained and invokes a repository-owned
script.

| Workflow | Triggers | Entrypoint |
| --- | --- | --- |
| `ci.yml` | push `main`, `develop`; pull request | inline `ruff`, `mypy`, `pytest` |
| `python-ci.yml` | push `main`; pull request `main` | inline `pytest` matrix, lint, build |
| `validate.yml` | push `develop`; pull request `develop`, `main`; dispatch | `scripts/run-uhome-server-checks.sh` |
| `family-policy-check.yml` | push/pull request `develop`, `main`; dispatch | `scripts/check-family-policy.py` |
| `release.yml` | tag `v*.*.*`; dispatch | inline `python -m build`, PyPI publish, GitHub release |

`promote.yml` was retired with the same upstream. This repository has no
`develop` release train, so promotion is a maintainer merge into `main`.
Reinstate a promotion job only once a `develop` branch exists, and keep it a
local job that calls a repository script.

`release.yml` stays tag- and dispatch-driven and is not part of validation.
`scripts/check-family-policy.py` fails the build if any workflow starts calling
a retired upstream again, or if a workflow runs a script that is missing, not
executable, or outside the repository.

## Boundaries

This activation does not move ownership into **HomeNook** for:

- canonical runtime semantics
- shell interaction ownership
- provider bridge ownership
- packaging bootstrap ownership outside server-specific runtime and install
  checks
