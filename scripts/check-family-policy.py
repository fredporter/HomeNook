#!/usr/bin/env python3
"""Family policy check for this repository's GitHub Actions wiring.

The family used to share reusable workflows from ``fredporter/uDOS-dev``:
``validate.yml``, ``family-policy-check.yml``, ``promote.yml`` and
``release.yml``. That repository was deleted. A call to a missing reusable
workflow fails to load, so the calling workflows ran no jobs at all and the
checks went quiet instead of failing loudly.

Each repository now owns its pipeline scripts and its workflows invoke them
locally. This check keeps that arrangement honest:

* every workflow file parses and declares ``on`` and ``jobs``;
* no workflow calls a retired upstream through ``uses:``;
* every external ``uses:`` carries an explicit ``@ref``;
* every ``scripts/`` path a workflow runs exists, is executable and stays
  inside the repository;
* the repository keeps its readme and licence.

Usage: ``python3 scripts/check-family-policy.py`` from the repository root.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - CI installs PyYAML
    sys.exit("pyyaml is required: python3 -m pip install pyyaml")

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOW_DIR = REPO_ROOT / ".github" / "workflows"

# Upstreams whose reusable workflows were retired. Keep this list explicit so a
# caller that reaches for a deleted upstream fails the policy check.
RETIRED_UPSTREAMS = ("fredporter/udos-dev",)

REQUIRED_FILES = ("README.md", "LICENSE")

SCRIPT_REFERENCE = re.compile(r"(?<![\w/.-])((?:\./)?scripts/[A-Za-z0-9._/-]+)")


def workflow_files() -> list[Path]:
    """Return the workflow files for this repository."""
    if not WORKFLOW_DIR.is_dir():
        return []
    return sorted(
        path
        for path in WORKFLOW_DIR.iterdir()
        if path.suffix in {".yml", ".yaml"} and path.is_file()
    )


def iter_uses(node: object) -> list[str]:
    """Collect every string held by a ``uses`` key in a parsed workflow."""
    found: list[str] = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "uses" and isinstance(value, str):
                found.append(value)
            else:
                found.extend(iter_uses(value))
    elif isinstance(node, list):
        for item in node:
            found.extend(iter_uses(item))
    return found


def iter_run_commands(node: object) -> list[str]:
    """Collect every string held by a ``run`` key in a parsed workflow."""
    found: list[str] = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "run" and isinstance(value, str):
                found.append(value)
            else:
                found.extend(iter_run_commands(value))
    elif isinstance(node, list):
        for item in node:
            found.extend(iter_run_commands(item))
    return found


def check_triggers(relative: Path, document: dict, problems: list[str]) -> None:
    # YAML 1.1 resolves a bare ``on`` key to the boolean True.
    if "on" not in document and True not in document:
        problems.append(f"{relative}: has no `on` trigger block")


def check_uses(relative: Path, document: dict, problems: list[str]) -> None:
    for reference in iter_uses(document):
        target = reference.split("@", 1)[0].strip().lower()
        if any(target.startswith(retired) for retired in RETIRED_UPSTREAMS):
            problems.append(
                f"{relative}: calls the retired reusable workflow `{reference}`; "
                "call a repository-owned script instead"
            )
        elif not reference.startswith("./") and "@" not in reference:
            problems.append(f"{relative}: `uses: {reference}` has no @ref pin")


def check_scripts(relative: Path, document: dict, problems: list[str]) -> None:
    for command in iter_run_commands(document):
        for candidate in SCRIPT_REFERENCE.findall(command):
            script = (REPO_ROOT / candidate).resolve()
            if REPO_ROOT not in script.parents:
                problems.append(f"{relative}: `{candidate}` escapes the repository")
            elif not script.is_file():
                problems.append(f"{relative}: runs missing script `{candidate}`")
            elif not script.stat().st_mode & 0o111:
                problems.append(f"{relative}: runs non-executable script `{candidate}`")


def check_workflow(path: Path, problems: list[str]) -> None:
    relative = path.relative_to(REPO_ROOT)
    try:
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        problems.append(f"{relative}: does not parse as YAML ({error})")
        return
    if not isinstance(document, dict):
        problems.append(f"{relative}: is not a YAML mapping")
        return
    check_triggers(relative, document, problems)
    if "jobs" not in document:
        problems.append(f"{relative}: has no `jobs` block")
    check_uses(relative, document, problems)
    check_scripts(relative, document, problems)


def main() -> int:
    problems: list[str] = []
    workflows = workflow_files()
    if not workflows:
        problems.append(".github/workflows: no workflow files found")
    for path in workflows:
        check_workflow(path, problems)
    for name in REQUIRED_FILES:
        if not (REPO_ROOT / name).is_file():
            problems.append(f"{name}: required repository file is missing")

    print(f"family policy: {len(workflows)} workflow file(s) checked")
    for problem in problems:
        print(f"  FAIL {problem}")
    if problems:
        print(f"family policy: {len(problems)} problem(s)")
        return 1
    print("family policy: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
