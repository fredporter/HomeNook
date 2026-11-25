> Historical/superseded scope (2026-09-10). See the [canonical revival plan](docs/REVIVAL-PLAN-2026-09.md). HA/Matter is a separate product integration; prior release/install claims remain unqualified.

# HomeNook

> **Living-room console for the uDos ecosystem**
> 
> HomeNook is a controller-first, 10-foot viewing console for media playback, home automation, TV/DVR, and system management — all powered by uCode3.

## Overview

HomeNook provides a unified living-room experience:

- **Media Browser** — Browse and play movies, TV shows, music
- **TV Guide** — EPG schedule grid with DVR scheduling
- **Automation Panel** — Launch OBF automation sheets
- **Feed Viewer** — Unified timeline for RSS, HA events, media scans
- **Music Player** — Album art with visualizer
- **Settings** — System configuration and first-run wizard

## Architecture

```
HomeNook Console (Vue 3 + Tailwind)
    ↓ MCP (Unix socket)
homenook-mcp (Rust)
    ↓
├── homenook-media   — Media scanner, mpv playback
├── homenook-tv      — EPG, DVR, live TV
├── homenook-spec    — OBF automation compiler
├── homenook-feed    — Feed/Spool viewer
├── homenook-grid    — Grid cell mapping
├── homenook-voice   — Voice assistant (HomeKit)
└── homenook-settings — System configuration
```

## Repositories

| Component | Location | Language |
|-----------|----------|----------|
| Console UI | `~/Code/uDosGo/ui/src/views/surfaces/homenook/` | Vue 3 |
| MCP Server | `~/Code/uDosGo/uCode3/homenook-mcp/` | Rust |
| Media | `~/Code/uDosGo/uCode3/homenook-media/` | Rust |
| TV/DVR | `~/Code/uDosGo/uCode3/homenook-tv/` | Rust |
| SpecLang | `~/Code/uDosGo/uCode3/homenook-spec/` | Rust |
| Feed | `~/Code/uDosGo/uCode3/homenook-feed/` | Rust |
| Grid | `~/Code/uDosGo/uCode3/homenook-grid/` | Rust |
| Voice | `~/Code/uDosGo/uCode3/homenook-voice/` | Rust |
| Settings | `~/Code/uDosGo/ui/src/views/surfaces/homenook/settings/` | Vue 3 |
| CLI Skill | `~/Code/uDosGo/udo/skills/homenook/` | Bash |

## Development

See [HOMENOOK_ROADMAP.md](../../docs/HOMENOOK_ROADMAP.md) for the full implementation plan.

## Status

| Phase | Status |
|-------|--------|
| Phase 0: Foundation Cleanup | 🟡 In Progress |
| Phase 1: Core Infrastructure | 🔴 Not Started |
| Phase 2: Media & TV | 🔴 Not Started |
| Phase 3: Feed & Automation | 🔴 Not Started |
| Phase 4: Voice & Settings | 🔴 Not Started |
| Phase 5: Polish & Deploy | 🔴 Not Started |
