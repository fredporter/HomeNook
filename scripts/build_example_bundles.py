#!/usr/bin/env python3
"""Regenerate the deterministic example bundle payloads and their digests.

The examples are illustrations, not vendor binaries: every component payload is a
tiny, deterministic tar.gz whose bytes depend only on the component identity.
Running this script is idempotent, so the hashes committed in
`examples/installer/bundles/*/uhome-bundle.json` can be reproduced on any machine
and the example bundles verify on a fresh clone.
"""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import tarfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLES_ROOT = REPO_ROOT / "examples" / "installer" / "bundles"

README_TEMPLATE = """HomeNook example component payload
component: {component_id}
display name: {display_name}
version: {version}
bundle: {bundle_id}

This is a deterministic fixture for the installer examples, not a vendored
binary. Regenerate with scripts/build_example_bundles.py.
"""


def payload_bytes(component: dict, bundle_id: str) -> bytes:
    """Build a byte-stable tar.gz for one component."""
    text = README_TEMPLATE.format(
        component_id=component["component_id"],
        display_name=component["display_name"],
        version=component["version"],
        bundle_id=bundle_id,
    ).encode("utf-8")
    info = tarfile.TarInfo(name="README.txt")
    info.size = len(text)
    info.mtime = 0
    info.mode = 0o644
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb", mtime=0) as compressed:
        with tarfile.open(fileobj=compressed, mode="w", format=tarfile.USTAR_FORMAT) as archive:
            archive.addfile(info, io.BytesIO(text))
    return buffer.getvalue()


def rebuild(bundle_dir: Path) -> None:
    manifest_path = bundle_dir / "uhome-bundle.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    bundle_id = manifest["bundle_id"]
    for component in manifest.get("components", []):
        artifact = bundle_dir / component["artifact_path"]
        artifact.parent.mkdir(parents=True, exist_ok=True)
        data = payload_bytes(component, bundle_id)
        artifact.write_bytes(data)
        component["sha256"] = hashlib.sha256(data).hexdigest()
        print(f"{artifact.relative_to(REPO_ROOT)}  {component['sha256']}  {len(data)} bytes")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    bundles = sorted(path for path in BUNDLES_ROOT.iterdir() if (path / "uhome-bundle.json").is_file())
    if not bundles:
        raise SystemExit(f"No example bundles found under {BUNDLES_ROOT}")
    for bundle_dir in bundles:
        print(f"== {bundle_dir.name}")
        rebuild(bundle_dir)


if __name__ == "__main__":
    main()
