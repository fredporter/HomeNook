# Historical README snapshot — superseded

Captured before the 2026-09-10 revival plan. Claims below are historical.

# HomeNook — Legacy Implementation Inventory

> **Architecture reset (2026-08-20):** HomeNook is a separate household media
> and automation product, not uCode3 and not part of the uCode 1/2 sprint
> sequence. The repository appears to contain useful working vertical slices;
> duplicated layouts and old boundaries need consolidation before further
> expansion. See
> [`docs/RESET_AND_RESCAFFOLD_PLAN.md`](docs/RESET_AND_RESCAFFOLD_PLAN.md).
> The content below is retained as historical implementation context.

# Historical: uCode3 — HomeNook (Application Layer)

**Ownership:** uDosGo  
**Core Language:** Python + Rust  
**CLI Command:** `uhome-server`  
**Status:** 🟢 Active  
**Size:** ~6.3M / 11K lines

---

## Overview

uCode3 is the **application layer** of the uDos ecosystem — a home media server, home automation bridge, and kiosk/console UI. It provides the HomeNook product line: household media, kiosk/thin UI, LAN server, and Matter/Home Assistant bridges.

uCode3 may import from uCode2 (MCP client, vault reads, feed queries) but never from uCode4.

### What uCode3 Owns

- **Home Media Server** — Jellyfin integration, media scanning, playback
- **Home Assistant Bridge** — Matter contracts, device management, automation
- **Kiosk/Console UI** — Thin client runtime, controller-first UX
- **Installer/Bundle System** — Sonic installer, bundle management, health checks
- **Rust Crates (homenook-*):**
  - `homenook-mcp` — MCP server for HomeNook (media, TV, automation, system)
  - `homenook-media` — Media scanner, metadata workflow, mpv controller, subtitles
  - `homenook-tv` — EPG parser, HDHomeRun tuner, DVR scheduler, storage manager
  - `homenook-feed` — Feed spool, RSS poller
  - `homenook-automation` — Scene manager, rule engine, OBF launcher
  - `homenook-voice` — HomeKit bridge, Wyoming STT client, command dispatcher
  - `homenook-docs` — Documentation generator
  - `homenook-flatpak` — Flatpak packaging
  - `homenook-debian` — Debian packaging
  - `homenook-grid` — Grid system
  - `homenook-spec` — USX bundle compiler

### What Belongs to Other Layers

| Feature | Layer | Why |
|---------|-------|-----|
| Grid/cell coordinate system | uCode1 | Foundation layer |
| MCP Gateway (Python) | uCode2 | Services layer — uCode3 consumes via client |
| Vault Bridge | uCode2 | Services layer |
| Feed Spool | uCode2 | Services layer |
| Spatial primitives | uCode2 | Services layer |
| Sprites & BOBs | uCode2 | Services layer |
| 3D worlds, portals | uCode4 | Spatial/3D layer |

### Dependency Rule

```
uCode1 ──► uCode2 ──► uCode3 ──► uCode4
```

uCode3 may import from uCode2 (MCP client, vault API). uCode3 has no dependencies on uCode4.

---

## Quick Start

```bash
# Install
bash scripts/install.sh

# Start server
bash scripts/start.sh

# Health check
curl http://localhost:7890/api/health
```

See: `QUICKSTART.md`, `FIRST-TIME-INSTALL.md`, `docs/`

---

## Architecture

```
uCode3 (Python + Rust)
├── src/uhome_server/     — Python server (FastAPI)
│   ├── routes/           — API endpoints
│   ├── services/         — Business logic
│   ├── installer/        — Bundle/install system
│   ├── sonic/            — Sonic installer integration
│   └── ...
├── tinshed/              — Rust crates (homenook-*)
│   ├── homenook-mcp/     — MCP server for HomeNook
│   ├── homenook-media/   — Media scanner & player
│   ├── homenook-tv/      — TV/DVR system
│   ├── homenook-feed/    — Feed spool
│   ├── homenook-automation/ — Scene & rules
│   ├── homenook-voice/   — Voice assistant
│   └── ...
├── ui/                   — Tailwind + USXD browser surface
├── apps/                 — Application configs
├── config/               — Configuration files
└── scripts/              — Install/start/stop/healthcheck
```

---

## Development

```bash
git clone git@github.com:uDosGo/uCode3.git
cd uCode3
# Python server
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
# Rust workspace (tinshed)
cd tinshed
cargo build
```

---

## License

MIT

---

*Part of the uDos ecosystem. See [uCode2](https://github.com/uDosGo/uCode2) for the services layer and [uCode4](https://github.com/uDosGo/uCode4) for spatial/3D.*
.*
