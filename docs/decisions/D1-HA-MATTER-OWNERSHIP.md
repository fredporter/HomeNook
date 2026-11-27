# D1 — Home Assistant and Matter gateway ownership

- **Status:** ratified, 27 November 2026
- **Decision owner:** Wizard/owner
- **Supersedes:** the September proposal to extract the bridge into a separate
  `udos-home-assistant` repository

## Decision

HomeNook owns the uDOS-facing Home Assistant gateway, the Matter bridge
contracts, their deployment guidance and their integration tests.

There is no standalone `udos-home-assistant` repository, and the gateway is not
folded into uCore.

## Why

- The active automation roadmap already assigns this ownership to HomeNook:
  `uCore/docs/plans/OK_ASSISTANCE_AND_LOCAL_RUNS.md` ("HomeNook ownership").
- The working code already lives here: `src/uhome_server/routes/home_assistant.py`,
  `src/uhome_server/services/home_assistant_service.py`,
  `src/uhome_server/services/home_assistant/service.py`, gated by
  `HOMENOOK_ENABLE_HA` in `app.py` and `config.py`, with notes under
  `docs/home-assistant/`.
- The bridge exists to serve the living-room appliance. Splitting it creates a
  sixth runtime with its own lifecycle, secrets and release process for one
  adapter.
- Folding it into uCore would couple media playback to core services and
  contradict the standalone guarantee HomeNook v0.1.0 already ships.

## Boundaries that do not move

| Concern | Owner |
| --- | --- |
| Gateway adapter, bridge contracts, deployment guidance, integration tests | HomeNook |
| Grants, workflow bindings, runs and receipts | uFlow (invoked through uCore) |
| Commissioning, Matter fabric, device state and service calls | Upstream Home Assistant and its Matter Server |
| Canon and knowledge | `~/Public/global-knowledge` (Wizard) |

HomeNook media and uCore startup stay independent of Home Assistant. The gateway
remains opt-in: without `HOMENOOK_ENABLE_HA`, HomeNook boots and plays media with
HA absent.

## Consequences

- The three references that pointed at a non-existent sibling repository are
  corrected to point at this decision and the in-repo gateway.
- Gate C (closed-loop Matter pilot) stays queued on card `7029f` until a real
  Home Assistant instance and an explicitly approved Matter light exist. This
  decision unblocks the paperwork, not the hardware.
- Removal or disablement: clear `HOMENOOK_ENABLE_HA` and remove the HA routes from
  the app; no separate service, database or credential store is introduced by this
  decision.

## Alternatives rejected

| Option | Why not |
| --- | --- |
| Separate `udos-home-assistant` repository | Duplicates lifecycle, secrets and release tooling for one adapter, and no code exists there today |
| Fold the gateway into uCore | Couples a media appliance to core hosting and breaks HomeNook's standalone boot guarantee |
