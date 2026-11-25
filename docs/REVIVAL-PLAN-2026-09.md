# HomeNook revival — canonical plan

## HomeNook rename and integration ownership

The checkout and Git remote already use `HomeNook`. Complete the rename across
active docs and UI labels, workspace files, package and artifact names, CI and
installer references, and discovery metadata. Audit existing CLI commands,
environment variables, endpoints, configuration and data paths before changing
those contracts. Document any compatibility aliases, migrations and rollback
steps. Keep historical records searchable under the names used at the time.

HomeNook owns the uDOS-facing Home Assistant gateway, Matter bridge contracts,
deployment guidance and integration tests. This replaces the separate adapter
ownership proposed in the September plan below. Upstream Home Assistant and
Matter Server own commissioning and device control. uFlow owns cross-product
workflows, grants and run receipts. HomeNook's media and Steam functions remain
independently usable while the automation pilot is delivered.

Validate the rename with a clean install and an upgrade from an existing
installation. Exercise the gateway against the uFlow automation pilot and
verify media startup with the gateway disabled.

Date: 2026-09-10. Status: assessed and planned; implementation sprint not started.
This supersedes the August reset where it assigned HA/Matter to HomeNook, the
July v1 “Released” claim, and the historical uCode3 product architecture.
User confirmed: Steam gaming **plus** films, music and TV.

## Product and boundaries

HomeNook is an independently installable Linux Steam and media host with a
controller-friendly living-room console, local playback and LAN clients.
It is its own product, repository, API and release stream. It is not uCode3.
A working installation must not need uCore, uCode, Sonic or Home Assistant.
Those products add provisioning, integration and presentation capabilities.

| Owner | Responsibilities | Boundary |
|---|---|---|
| HomeNook | Media browsing/session control; Steam launch/return; living-room console; provider adapters; media-specific settings | No general device registry, Matter stack, secrets server or automation engine |
| Jellyfin | Media indexing, metadata, streaming/transcoding and accounts | Consume its API; do not rebuild its server |
| Steam | Game library, login, game launch and Remote Play | User-installed proprietary dependency; not a redistributable open-source payload |
| Separate `udos-home-assistant` | HA connection, entity/service projection, own uihub card/API/command adapter | Depends on upstream HA, not on HomeNook |
| Home Assistant / Matter server | Home devices, commissioning, device state and local home automations | Run upstream services; do not implement another protocol stack |
| uCore | Optional identity, secrets, extension hosting and module lifecycle | Thin adapter; standalone configuration must still work |
| uFlow | Optional durable cross-product workflows | Movie-night workflow calls HomeNook and HA independently; no second scheduler |
| uCode / GridCore | Optional terminal rendering, fonts, shared interaction contracts | Reuse packages; no copy of uCode or its runtime into HomeNook |
| SonicScrewdriver | Hardware qualification, OS/device provisioning and artifact installation | Installs HomeNook and HA as separate choices; no HomeNook-only disk writer |
| uKnowledge | Shared documents/manuals and knowledge indexing | HomeNook media catalog is not a global knowledge vault |

## First supported journey

On one qualified Linux x86-64 desktop host: install HomeNook, connect an
existing Jellyfin server (which may be on this host), browse and play one film
with audio, launch Steam Big Picture, launch a game, return to HomeNook with
controller focus restored, restart the host and repeat. HA and uDOS are absent.
Also verify a second LAN client can browse/play media. Steam Remote Play is the
first game-streaming route; evaluate Sunshine/Moonlight only if its tested
capabilities are needed. A headless media-only profile is distinct from a
GPU/display/audio game host; do not promise universal headless Steam support.

macOS/uIHub is a client/control surface for the Linux server. It is not the
initial Linux appliance build target. Linux distribution/version and GPU driver
support must be pinned from a successful test machine, not inherited from an
old Mint claim. Low-spec Sonic machines may qualify only for media-client roles.

## Implementation choice and reuse

Prefer the packaged Python FastAPI `src/uhome_server` as the backend candidate,
and the Vue console in `apps/console` as the frontend candidate. This is a
selection hypothesis, not a declaration that either works. HN-01 must compare
actual routes/imports/builds with `server/`, the React root and Rust crates.
Retain functioning pieces only after characterization. Keep the existing
`uhome-server` package identity temporarily until compatibility/migration is
specified; the product name and future CLI are HomeNook (`homenook`).

The presentation service currently persists intent rather than managing a
Steam process. Add observed process/session state, real launch/exit and display
session ownership. A queued media handoff is accepted work, not successful
playback: obtain provider/player acknowledgement, report failures/timeouts,
and distinguish requested, starting, running, stopped and failed.

HomeNook's installer staging/health/promotion code is a Sonic reuse candidate.
Do not copy it to Sonic and continue two implementations. Characterize the
standalone HomeNook path first; then let Sonic own generic installation while
HomeNook owns artifact contents and application migrations. Neither product
should require an editable sibling checkout at runtime.

### Depot handoff

Depot is the successor to the local Vendor catalogue. Keep upstream source
and provenance in its catalogue lanes and retained release bundles in its
artifact lane. HomeNook owns the release manifest, component versions and
checksums, and downstream patches. Sonic owns generic provisioning and
consumes the same verified bundle as a manual installation.

Pass the selected bundle directory to the existing installer CLI. Verify
the bundle before staging into a separate directory. A standalone install
can use the same verified bundle copied from Depot without access to the
development workspace or network.

## State, services and removal

Proposed state: `$UDOS_HOME/homenook` (default `~/Code/.udos/homenook`), owned
by HomeNook. Migrate legacy `memory/` data explicitly with backup and a receipt;
do not write new state into the source checkout. Media stays in configured user
libraries; uninstall never deletes media. Standalone local credentials use a
permission-restricted application config; connected mode uses uCore references.
Do not create a new credential service. No tokens in browser bundles or logs.

Separate the unprivileged always-on API/media adapter from the interactive
user-session Steam/console launcher. Bind locally by default; authenticated
LAN access is explicitly configured. Service stop/removal must not stop HA.
Measure startup time, idle RAM/CPU, media-scan I/O and playback/transcode load
on the reference machine. Do not publish hardware minimums before measurement.
Optional providers have individual enable/disable and dependency checks.

## Development and distribution pathway

1. Complete Sonic's agreed sprint/handoff: stable diagnostic/artifact contract,
   qualified host description, clear distinction between planned and supported
   install operations. HomeNook development can use manual installation if
   Sonic disk-writing is still unqualified; do not claim a bootable release.
2. Run [HomeNook revival sprint](SPRINT-01-REVIVAL-2026-09.md): one standalone
   end-to-end media + Steam journey and explicit HA separation contracts.
3. Publish a tested prerelease wheel plus compiled console assets, dependency
   lock/constraints, source/license inventory, checksums, release manifest,
   compatibility matrix, upgrade/rollback and uninstall instructions. Install
   from that artifact in a clean machine, not from developer source paths.
4. Add a Linux packaging/service recipe. Keep Jellyfin and Steam provider
   installation separate; use upstream packages, no bundled user accounts or
   proprietary game content. Containerize headless media services only where
   supported; don't force desktop Steam into the backend container.
5. Sonic consumes the same immutable HomeNook release manifest as manual
   install. Add uCore module registration and the optional HomeNook uihub card
   against supported extension contracts. Test standalone/connected parity.
6. Qualify optional remote gaming, DVR/EPG/tuner support, additional hardware,
   and a later Sonic/Mint appliance recipe. A custom ISO is not the first
   delivery milestone and Classic Modern Mint is not a required dependency.

Each product versions independently. Record supported HomeNook API, HA adapter,
uCore extension, uCode rendering package and Sonic artifact versions in a
compatibility matrix; no synchronized version numbers or lockstep releases.

## Related records

- [Evidence and disposition](REVIVAL-ASSESSMENT-2026-09.md)
- [Sprint and acceptance](SPRINT-01-REVIVAL-2026-09.md)
- [HA separation and upstream intake](../../udos-home-assistant/README.md)
- [Pre-edit source inventory](REVIVAL-SOURCE-INVENTORY-2026-09.json)
- [Sonic revival](../../SonicScrewdriver/docs/REVIVAL-PLAN-2026-09.md)

## Planning handoff — 11 September 2026

The user authorized completing these plans and beginning Sonic redevelopment.
The boundaries and ordered acceptance gates above are the implementation
baseline. HomeNook follows Sonic; HA remains independently owned. No further
scope confirmation is required to begin the defined work. Hardware-dependent
acceptance and deployment-version qualification remain execution gates, not
unresolved product scope. Runtime extraction has not begun in this repository.

## Implementation handover — 12 September 2026

Pre-work is consolidated in [Gemini handover](GEMINI-HANDOVER.md).
Planning is complete; runtime implementation and real-provider qualification
remain open. Follow the handover for current entry points and acceptance gates.
