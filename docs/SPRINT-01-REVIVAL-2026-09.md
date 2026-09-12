# HomeNest revival sprint 1 — follows Sonic

Status: ready for planning review; no runtime implementation claimed.
Objective: a repeatable standalone Linux media-and-Steam journey, with HA
owned separately. Scope is ordered by dependencies, not a promised calendar.

| ID | Deliverable / owner | Acceptance |
|---|---|---|
| HN-01 | HomeNest: characterize existing stacks | Isolated baseline report for Python tests and Vue build; compare duplicate server/React/Rust paths, route/asset inventory and one selected implementation; list failures explicitly |
| HN-02 | HomeNest + HA adapter: enforce boundary | HomeNest installs/starts with HA and all uDOS repos absent; HA adapter starts with HomeNest absent; no default HA routes/imports; extracted code retains provenance/tests; no duplicate scheduler |
| HN-03 | HomeNest: honest media/Steam lifecycle | Film plays with audio; Steam game launches; exit restores focus; process death, wrong provider credentials and unreachable provider report failure; queued request never reports playback success |
| HN-04 | HomeNest: standalone console and LAN client | Controller-only browse/play/back/settings and Steam return; second LAN client playback; authenticated commands; no secret material in UI/logs; optional providers degrade independently |
| HN-05 | HomeNest: state and packaged install | Installed wheel/console works outside checkout; UDOS_HOME override; backup/migrate legacy state; reboot; upgrade and rollback; uninstall retains media and HA |
| HN-06 | HomeNest + Sonic: distribution handoff | Versioned manifest/checksums and application health contract; same artifact works manually and through qualified Sonic operations; no duplicate disk writer; unsupported operations remain explicit |
| HA-01 | Separate HA repo: connection/API contract | Real HA REST + WebSocket auth, reconnect and unavailable states; own command allowlist; device state observed from upstream; no HomeNest dependency |
| INT-01 | uCore/uCode/uFlow: optional cards/contracts | Separate HomeNest and HA uihub cards; each disabled independently; existing host registration mechanism reused; cross-product workflow calls public contracts and records outcomes |

HN-01 → HN-02 → HN-03 → HN-04 → HN-05 → HN-06 is the critical path.
HA-01 and INT-01 are independent integration work; they must not prevent the
standalone HomeNest acceptance demo. Do not expand the sprint into a full HA
or Matter commissioning UI rebuild. Upstream HA provides commissioning.

Required test assets: one qualified Linux x86-64 host with display/GPU/audio,
a controller, a user-owned Steam game/account, lawful sample media, a Jellyfin
instance and a second LAN client. HA integration acceptance additionally needs
an HA instance and, for a Matter claim, an actual supported device/network.
Record distro/kernel/GPU/driver, package versions, test procedure and results.
Mock tests support development; they do not substitute for these acceptance runs.

Release exit: clean-machine installation and reboot reproduce the journey;
failures are visible; standalone survives uDOS/HA absence; rollback and uninstall
are documented and tested. Otherwise label the build experimental and list
unmet gates. Start DVR, advanced streaming and appliance recipes afterward.

## Implementation handover — 12 September 2026

Pre-work is consolidated in [Gemini handover](GEMINI-HANDOVER.md).
Planning is complete; runtime implementation and real-provider qualification
remain open. Follow the handover for current entry points and acceptance gates.
