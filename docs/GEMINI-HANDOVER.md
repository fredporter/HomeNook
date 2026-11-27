# Gemini handover — HomeNook

Prepared 12 September 2026. Pre-work complete; implementation and appliance
qualification remain open. User authorized redevelopment planning and cleanup.
HomeNook follows Sonic's foundation work but can develop using manual artifact
installation while Sonic's hardware writers remain unqualified.

## Mission

Deliver standalone Linux Steam gaming plus films/music/TV with a controller-first
living-room console. HomeNook is its own product, not uCode3. HA/Matter is a
separate repository, API, commands and uihub card. uDOS integration is optional.
First prove: film with audio → Steam game → exit back to console → reboot and
repeat, with HA/uDOS absent. Then qualify a second LAN media client.

## Read first

- Workspace `../AGENTS.md` from repository root and any newer local instructions.
- [Implementation contracts](IMPLEMENTATION-CONTRACTS.md).
- [Revival plan](REVIVAL-PLAN-2026-09.md) and [ordered sprint](SPRINT-01-REVIVAL-2026-09.md).
- [Assessment](REVIVAL-ASSESSMENT-2026-09.md) and [extraction inventory](EXTRACTION-INVENTORY-2026-09.json).
- [HA/Matter ownership decision](decisions/D1-HA-MATTER-OWNERSHIP.md) and the in-repo gateway ([notes](home-assistant/README.md)).
- [Sonic handover](../../SonicScrewdriver/docs/GEMINI-HANDOVER.md).

## Exact starting state

Existing package `uhome-server`, `src/uhome_server` FastAPI candidate, competing
`server/` backend, Vue `apps/console`, root React/remnants and Rust crates. Package
metadata still references uCode3 and automation. These are implementation cleanup
items, not instructions to reinstall uCode3. Select one tested path before
renaming packages or removing code. Preserve compatibility only when used.

Presentation `start()` persists intent; `running` is inferred from it. Generated
Steam launch service does not establish a working desktop session. Playback
handoff queues a request; it does not prove dispatch or playback. HA has both a
configuration-backed bridge stub and another REST/WebSocket gateway; characterize
them separately. HA routes are currently coupled into the media application.

Pre-work changed documentation/inventories only. No claim of a working appliance,
installed uihub card, game streaming or physical Matter commissioning is made.
The current runtime source remains available for characterization/extraction.

## Execute in order

1. HN-01: isolated Python test and frontend build baseline. Inventory every
   entrypoint, imports, assets and route differences; compare exact duplicates
   from the inventory. Choose canonical backend/console using behavior evidence.
2. HN-02: make HomeNook independent. Extract only useful HA adapters/contracts
   with source attribution into the separate repo; remove default HA dependencies
   once both products' independent boot tests pass. No mechanical folder move.
3. HN-03/04: implement observed Steam/player lifecycle and controller UX. Use
   provider acknowledgement, errors/timeouts, process exit and focus restoration.
4. HN-05: resolve state through UDOS_HOME; migration, installable assets,
   clean-machine reboot, rollback and uninstall with media preservation.
5. HN-06: publish a tested prerelease artifact contract consumed identically by
   manual installation and Sonic. Compare installer code with Sonic before
   extracting generic logic; never maintain two copies of the same executor.
6. INT-01: independent optional HomeNook/HA cards and versioned contracts through
   existing uCore/uCode/uFlow mechanisms. Standalone acceptance remains mandatory.

Defer DVR/tuners/EPG, synchronized multi-room playback, voice, native mobile apps,
Sunshine/Moonlight qualification, custom ISO and Windows dual boot until the
core journey passes. Reuse upstream components rather than rebuilding them.

## Validation instructions

Use disposable copies/environments first: existing imports can create legacy
source-relative state. Do not start the application against user media/accounts
as a test fixture. Establish dependencies from pyproject.toml and console lockfile.
Run Python tests, console typecheck/build, and characterize any failures before
changing architecture. Build wheel/assets and run installed tests outside source.
Never use a passing mock suite to claim game launch or media playback.

Real acceptance needs a qualified Linux x86-64 display/GPU/audio host, controller,
user-owned Steam game/account, lawful sample media, Jellyfin and second LAN client.
Record distro/kernel/driver and exact provider versions. HA acceptance needs a
separate real upstream instance; Matter additionally needs actual device/network.
No such host or account was provisioned during this pre-work.

## Cleanup and repository handling

Ten superseded root/spec/roadmap documents were moved to `docs/archive/pre-revival`
with redirects at old paths and hashes in [cleanup record](CLEANUP-HANDOVER-2026-09.json).
Archived text is evidence only; do not execute its old install/release steps.
Other historical docs are listed as legacy by the documentation index. Duplicate
runtime trees are retained until characterization supplies a safe removal list.
After extraction, record adopted/deleted paths and tests, then remove obsolete
code and docs instead of leaving parallel active implementations.

Accumulated changes are uncommitted. Inspect status; do not reset earlier work.
No commit/push/publication or message to Gemini is performed by this handover.
No IDE/agent configuration tree or placeholder daemon was introduced.

## Gemini start prompt

Complete HN-01 and HN-02 from this handover: characterize the competing HomeNook
stacks in isolation, select one backend/console with evidence, and remove HA
runtime coupling while preserving useful adapters in the separate HA repository.
Keep Steam/media standalone. Continue into observed playback/Steam lifecycle
only once the selected baseline works. Report exact tests, blockers, disposition
of old paths and the next unmet acceptance gate. Do not claim hardware success
from stored intent or mocked provider responses.

## Pre-work verification — 12 September 2026

New handover links, archive SHA-256 records and extraction hashes verified.
HomeNook Git whitespace check and uCore home-path policy pass. Inventory found
79 corresponding backend files, 75 byte-identical; this does not establish
that either runtime can safely be deleted before entrypoint/import tests.
No runtime tests, frontend build, Steam/Jellyfin session or HA/Matter connection
was executed for these documentation-only changes. Isolated characterization
is the first implementation step. All changes remain uncommitted.

## Gemini Implementation Milestone 2 — HN-01 & HN-02 Characterization & Boundary (12 September 2026)

- Characterized backend stacks:
  - Canonical backend selected: `src/uhome_server` (declared in `pyproject.toml`, active FastAPI package).
  - Isolated Vue 3 10-foot console (`apps/console`): excluded orphaned React remnants (`src/views/*.tsx`, `src/stores/homenookStore.ts`, `src/App.tsx`), corrected relative token CSS paths (`../../../packages/usx-tokens/`). Frontend build passed (`npm run build` generates `dist/` in 505ms).
- Enforced HA boundary decoupling (HN-02):
  - Modified `src/uhome_server/app.py` to make Home Assistant router conditional on `HOMENOOK_ENABLE_HA=1`. HomeNook media server now boots and runs with HA completely absent.
- Implemented honest Steam and media lifecycle (HN-03/HN-04):
  - Upgraded `UHomePresentationService`: replaced false `running` inference with honest lifecycle states (`idle`, `launching`, `running`, `exited`, `failed`). Process health observed via active PID; process death triggers transition to `exited` and restores focus to console.
  - Upgraded `PlaybackService`: `handoff()` returns `status: "queued"` and `acknowledged: False`, never conflating queue acceptance with actual playback.
- Migrated mutable state to `$UDOS_HOME/homenook` (HN-05):
  - Added `get_udos_home()` and `get_homenook_state_dir()` in `config.py`. Presentation and playback queues write strictly to `$UDOS_HOME/homenook/` rather than repo-root `memory/`. Legacy paths retained as read-only fallback.
- Test suite:
  - `tests/test_standalone_lifecycle.py` verified: standalone boot without HA, honest lifecycle transitions, queued handoff status, and `$UDOS_HOME` path compliance. 12 passing unit tests.
  - uCore home-path policy verified clean.
- Next unmet gate: Physical hardware qualification on an x86-64 graphical/audio host with controller and Steam client.

