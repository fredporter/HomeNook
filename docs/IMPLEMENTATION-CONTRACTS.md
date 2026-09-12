# HomeNest implementation contracts

Design baseline, 12 September 2026. Proposed paths/API names below are not
installed services. Keep the current package scaffold until HN-01 selects and
verifies the canonical runtime. No extra IDE, agent or service trees are needed.

## Component map

| Component | Starting point / next responsibility | Ownership and lifecycle |
|---|---|---|
| Python API | `src/uhome_server`, compare `server/` before consolidation | HomeNest; unprivileged service, independent of uDOS/HA |
| Living-room console | `apps/console` Vue candidate; compare root React remnants | HomeNest; compiled assets served with the artifact; no dev server in deployment |
| Steam session adapter | Existing presentation intent + generated `steam -tenfoot` command | HomeNest adapter, Steam upstream process; interactive user session |
| Media provider | Existing Jellyfin probe and playback queue | HomeNest adapter; Jellyfin owns catalog/streaming/transcoding |
| Installer | `src/uhome_server/installer/` | App payload/migrations HomeNest; generic device application Sonic |
| HA/Matter | Existing `matter/`, HA gateways/routes/rules | Extract reviewed adapter behavior to separate repo; upstream owns home control |
| Rust crates | Existing `rust-workspace/` | Retain only independently tested unique media functionality; no automatic rewrite |
| Runtime state | Proposed `$UDOS_HOME/homenest` | HomeNest; explicit legacy migration, bounded logs/cache, removal preserves media |

Before removal compare tests, imports, entrypoints and assets, not just identical
filenames. Use EXTRACTION-INVENTORY-2026-09.json. Do not copy an entire runtime
into a new package and leave both active. Preserve provenance for adopted files.

## Media and Steam contracts

HomeNest logical API namespace: `homenest/v1`; actual host prefix must follow
uCore registration conventions when integrated. Standalone owns its endpoint.
Operations: capabilities, provider health, library browse/search, playback
request/status/stop, launcher request/status/stop. Validate IDs/arguments;
no arbitrary shell command from a browser, catalog or API parameter.

Every mutating request returns an operation ID and state: accepted, starting,
running, stopped or failed. Include timestamps, provider/session identity,
structured error and observed state; an accepted queue entry is not playback.
Correlate requests with provider acknowledgement; timeout and process death
must reach a visible terminal failure. Reconnect reads state instead of
replaying launch commands. Specify cancellation and retry/idempotency semantics.

Steam adapter: find a qualified installation, launch as the desktop user in
an existing graphical/audio session, observe actual launch/exit, restore
console focus and distinguish an already-running client from a new process.
Do not run Steam as root or from the headless API service. The user's Steam
account/game installation stays upstream-owned; never bundle login data or
games. First qualify local game launch and Steam Remote Play; Sunshine/Moonlight
is an optional later provider, not a parallel mandatory stack.

Jellyfin adapter: connect configured upstream, authenticate, browse and obtain
playback/session acknowledgement. Define which player receives a handoff;
verify actual video/audio on that player. Distinguish direct play, transcode,
unsupported media and unreachable player. A media-only headless server is a
separate profile from the display/GPU/audio Steam host. Do not rebuild Jellyfin
indexing, metadata, transcoding or account management.

Console: controller-only browse/play/back/settings and Steam return; visible
focus, keyboard fallback and readable error/reconnect states. macOS uihub is
initially a Linux-host control/client surface. Avoid assuming browser APIs can
launch host Steam without an authenticated local adapter.

## Independence, state and security

HomeNest must install/start with HA/uCore/uCode absent. Optional integrations
have their own enablement and failure states. No unconditional HA routes/imports
in the selected media entrypoint. Standalone config stores local credentials
with restricted permissions; connected mode references uCore secrets. Never
place provider tokens in browser assets, telemetry or URLs written to logs.
Bind locally by default, require authentication for configured LAN control,
validate origins/session permissions and use upstream TLS appropriately.

Migrate old `memory/` and competing JSON/SQLite state explicitly with backups,
receipts and rollback. Media paths remain user-configured and external to the
package. Uninstall stops only HomeNest services, unregisters its optional card,
and retains media; it never stops HA or removes Matter fabric data.
Measure API idle RAM/CPU, startup time, indexing I/O and playback load on the
reference host before claiming minimum hardware. Budget logs/cache and expose
clear cleanup behavior. No new background process is created by this handoff.

## Distribution and integration gates

Produce a wheel with built console assets and pinned tested dependencies,
then test outside the source checkout on Linux. Include source/license notices,
checksums, release manifest, compatibility matrix, upgrade/rollback and uninstall.
Use supported upstream packages for Steam/Jellyfin; research snapshots are not
release pins. Manual installation precedes Sonic consumption of the same artifact.
A container can host qualified headless media services; it is not automatically
suitable for Steam's desktop session. Custom Mint/ISO is a later Sonic recipe.

Separate uihub cards: HomeNest for media/gaming; HA for entities/scenes. Reuse
uCode/GridCore rendering packages where needed, not copied application trees.
uCore owns identity/secrets/module lifecycle. uFlow owns cross-product workflows;
HA owns local home rules. A movie-night workflow observes HomeNest playback then
requests an HA scene and records partial failure without breaking playback.

## Release acceptance matrix

| Gate | Required evidence |
|---|---|
| Standalone | Clean Linux artifact install with no sibling repositories/uDOS/HA; reboot and repeat |
| Media | Browse and play lawful sample with audio; second LAN client; invalid token/outage/unsupported file behavior |
| Steam | User-owned game launch, exit, focus return, restart and already-running behavior; separate Remote Play evidence |
| State | UDOS_HOME override, backup/migrate, rollback and uninstall retain media |
| Boundaries | HA unavailable/removed does not prevent media; HomeNest removed does not affect HA |
| Integration | Optional cards independent; authentication and outcome correlation; no duplicate retry |

Mocks characterize contracts; a real Linux host/controller/display/audio and
actual providers are required to mark these acceptance gates passed.
