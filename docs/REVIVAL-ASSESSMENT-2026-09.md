# HomeNook evidence and disposition

Assessed 2026-09-10 at `1408cafef2aaff848d4e19d32cb4dee52997c01a`.
This is a static source audit, not a successful appliance test. Inventory hashes
preserve pre-edit documentation provenance. Older docs are historical evidence,
not current release instructions. No runtime code was removed in this planning pass.

| Evidence | Finding | Disposition / first task |
|---|---|---|
| `README.md`, `HOMENOOK_README.md`, `docs/RESET_AND_RESCAFFOLD_PLAN.md` | Successive uCode3, uHOME and reset narratives coexist | Canonical revival replaces product identity; preserve old text as history |
| `docs/specs/HOMENOOK_v1_SPEC.md` | Claims Released; Vue + stdlib HTTP + Jellyfin + HA | Retain media UX requirements; supersede release and HA-ownership claims |
| `pyproject.toml` | `uhome-server`, FastAPI, old uCode3 URLs | Preferred backend candidate; repair packaging after characterization |
| `package.json`, `src/`, `apps/console/package.json` | Root React dependencies; Vue console; React remnants inside console | Choose one console after build and controller smoke test; remove duplicate path only with migration evidence |
| `server/src/uhome_server`, `server/core`, `src/uhome_server` | Competing backend copies and persistence models | Compare routes and behavior before consolidating; never delete by matching filenames alone |
| `src/uhome_server/services/uhome_presentation_service.py` | `start()` writes JSON intent; `running` derives from saved active presentation | Retain UX contract, replace false process-health inference |
| `src/uhome_server/installer/linux_assets.py` | Generates a `steam -tenfoot` service command | Useful launch intent; does not prove correct graphical-session lifecycle or actual game playback |
| `src/uhome_server/services/playback_service.py` | Jellyfin session probe exists; handoff appends JSON queue | Retain adapter evidence; require real dispatch and player acknowledgement |
| `src/uhome_server/services/home_assistant_service.py` | Enabled config yields `ok`; discover reads declared entities | Historical stub contract, not observed HA connection health |
| `src/uhome_server/services/home_assistant/` | Separate REST/WebSocket gateway implementation exists | Study actual gateway before extracting; do not generalize stub findings to every HA code path |
| `src/uhome_server/app.py` | Registers HA routes with media app | Remove HA dependency from default HomeNook boot during boundary sprint |
| `matter/` | Former standalone uHOME-matter folded into repo; contracts/catalogs, not the upstream Matter stack | Provenance-preserving extraction candidate into separate integration repo; replace obsolete mappings |
| `host/`, `apps/tablet-kiosk`, `apps/dashboard`, `services/`, `modules/` | Prior client/server decomposition and wrappers | Retain only tested client/media responsibilities; defer secondary apps |
| `src/uhome_server/installer/` + installer tests | Bundle/preflight/stage/promotion/health concepts survive from archived uCode3 | Reuse assessment with Sonic; generic installer owner Sonic, application payload owner HomeNook |
| `rust-workspace/` | Media/TV plus automation/feed/voice/system scope from previous architecture | No blanket Rust rewrite or restoration; retain only proven unique media functionality; shared services return to ecosystem owners |
| `tests/test_uhome_presentation_service.py` | Asserts workspace preferences and intent persistence | Useful characterization; not proof Steam runs |
| `tests/test_playback_routes.py` and installer tests | API/fixture coverage exists | Run isolated baseline; add real-provider integration and installed-artifact tests |
| `memory/` paths in playback and presentation | Source-relative mutable state | Migrate to UDOS_HOME; preserve user media and rollback data |

## Backlog decisions

Retain now: Steam launch/return, Jellyfin media, controller navigation, LAN media
clients, honest health, install/upgrade/uninstall, optional uihub media card.

Extract/adapt: HA/Matter bridge and entity contracts to `udos-home-assistant`;
generic provisioning to Sonic after characterization; identity/secrets/module
lifecycle to uCore; durable cross-product automation to uFlow; terminal/font
rendering to uCode; manuals/knowledge to uKnowledge.

Defer: DVR/tuners/EPG, multi-room synchronized playback, native mobile apps,
Sunshine/Moonlight qualification, voice control, custom appliance ISO, Windows
dual boot, broad hardware support. These are not prerequisites for the first
working Linux media and Steam journey.

Retire from active scope: HomeNook as uCode3, general home automation engine,
embedded Matter protocol implementation, duplicate RSS/knowledge/secrets
platforms, and unverified “released”/single-command installation claims.
Historical source stays until HN-01 records unique behavior and HN-02/HN-06
prove replacement. Record deletions and replacement paths before removal;
archive evidence once, not another active implementation tree.

## Evidence limits

No real Steam game, Jellyfin playback, controller, tuner or Matter device was
exercised in this planning pass. No full backend/frontend build was claimed.
Upstream clones are research intake, not installed services or production forks.
