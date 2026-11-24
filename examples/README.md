# Examples

`examples/` is a transitional but active root for runnable and inspectable
examples.

Current contents focus on installer bundles and hardware probes that make the
current server and `sonic-screwdriver` integration testable without
pretending those examples are the final course structure.

Current example lanes:

- `installer/bundles/` for standalone and dual-boot reference bundles
- `installer/probes/` for sample hardware probe input
- `basic-uhome-server-session.md` for the smallest local runtime walkthrough
- `basic-base-runtime-profile.json` for the smallest checked-in base runtime
  profile example

Phase 1 rule:

- keep examples stable for runtime and test use
- point courses and pathway docs at these examples rather than duplicating them

Example bundle payloads are deterministic fixtures, not vendor binaries: each
component is a small `payload.tar.gz` whose bytes depend only on the component
identity. `python3 scripts/build_example_bundles.py` rewrites them and updates the
committed SHA-256 values in each `uhome-bundle.json`, so the bundles verify on a
fresh clone and a copied (Depot-shaped) bundle installs standalone without the
repository present.
