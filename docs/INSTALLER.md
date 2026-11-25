# HomeNook Installer — Linux Mint Cinnamon

**Target:** Linux Mint 21.x/22.x with Cinnamon desktop
**Status:** active
**Last updated:** 2026-07-08

---

## Overview

The HomeNook installer deploys the full stack on a fresh Linux Mint Cinnamon machine:

- **Jellyfin** — media server (optional, can skip with `SKIP_JELLYFIN=1`)
- **HomeNook API** — Python HTTP server on port 7890
- **HomeNook Console** — Vue 3 SPA served by nginx on port 8080
- **systemd** — both services managed as system units

Sonic Home Express has been separated into its own experimental lane/project and is no longer part of the core HomeNook installer.

---

## Quick Install

```bash
# Clone the repo
git clone https://github.com/fredporter/HomeNook.git
cd HomeNook

# Install (requires sudo)
sudo bash scripts/install.sh
```

After install, open `http://localhost:8080` in your browser.

---

## What Gets Installed

| Component | Path | Port |
|---|---|---|
| HomeNook root | `/opt/homenook/` | — |
| API server | `/opt/homenook/server/api/main.py` | 7890 |
| Console (built) | `/opt/homenook/apps/console/dist/` | 8080 (nginx) |
| Config file | `/opt/homenook/config/environment.env` | — |
| Media vault | `/home/homenook/media/` (movies, tv, music) | — |
| systemd unit | `/etc/systemd/system/homenook-server.service` | — |
| nginx site | `/etc/nginx/sites-available/homenook` | — |
| udev rules | `/etc/udev/rules.d/99-uhome.rules` | — |
| System user | `homenook` (no login shell) | — |

---

## Customizing the Install

Environment variables control the installer:

```bash
# Custom user and paths
sudo HOMENOOK_USER=media HOMENOOK_MEDIA_ROOT=/mnt/nas/media bash scripts/install.sh

# Skip Jellyfin (if you already have a media server)
sudo SKIP_JELLYFIN=1 bash scripts/install.sh

# Custom ports
sudo HOMENOOK_PORT=9000 bash scripts/install.sh
```

| Variable | Default | Description |
|---|---|---|
| `HOMENOOK_USER` | `homenook` | System service user |
| `HOMENOOK_HOME` | `/opt/homenook` | Install root |
| `HOMENOOK_MEDIA_ROOT` | `/home/homenook/media` | Media vault path |
| `HOMENOOK_PORT` | `7890` | API listen port |
| `SKIP_JELLYFIN` | `0` | Set to `1` to skip Jellyfin installation |

---

## Service Management

```bash
# Start / stop / restart
sudo systemctl start homenook-server
sudo systemctl stop homenook-server
sudo systemctl restart homenook-server

# View logs
sudo journalctl -u homenook-server -f
sudo journalctl -u homenook-server -n 50

# Check status
sudo systemctl status homenook-server
```

---

## Uninstalling

```bash
# Remove services and config (keeps /opt/homenook and media vault)
sudo bash scripts/uninstall.sh

# Full purge — removes /opt/homenook and the homenook user
sudo bash scripts/uninstall.sh --purge
```

Jellyfin, nginx, and system dependencies are NOT removed by the uninstaller (they may be used by other services).

---

## Post-Install Configuration

1. **Connect Jellyfin** — Open `http://localhost:8080`, go to Settings, expand "Connect Jellyfin". Enter your Jellyfin URL and API key (get one at Jellyfin Dashboard → API Keys).

2. **Connect Home Assistant** — In Settings, expand "Connect Home Assistant". Enter your HA URL and a long-lived access token (get one at HA Profile → Security → Long-Lived Access Tokens).

3. **Add media** — Drop files into `/home/homenook/media/movies/`, `/tv/`, `/music/`. They'll be picked up by Jellyfin's library scan.

4. **Access from other devices** — The console is available at `http://<your-mint-ip>:8080` on your local network.

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│  Linux Mint Cinnamon                            │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ nginx    │  │ HomeNook│  │ Jellyfin │       │
│  │ :8080    │──│ API :7890│──│ :8096    │       │
│  │ (console)│  │          │  │          │       │
│  └──────────┘  └──────────┘  └──────────┘       │
│                      │                            │
│               ┌──────┴──────┐                    │
│               │ Home        │                    │
│               │ Assistant   │                    │
│               │ :8123       │                    │
│               └─────────────┘                    │
│                                                  │
│  /opt/homenook/   — install root                 │
│  /home/homenook/  — media vault                  │
│  ~/.uhomenook/    — SQLite state db              │
└─────────────────────────────────────────────────┘
```

---

## Troubleshooting

### API server won't start
```bash
sudo journalctl -u homenook-server -n 30
# Common issues:
# - Python not found → ensure python3 is installed
# - Port 7890 in use → set HOMENOOK_PORT to another port
```

### Console shows blank page
```bash
# Ensure the Vue app was built
ls /opt/homenook/apps/console/dist/index.html
# If missing, rebuild:
cd /opt/homenook/apps/console && npm install && npm run build
```

### Jellyfin not detected
```bash
sudo systemctl status jellyfin
# If not running, start it:
sudo systemctl start jellyfin
```

### Non-Mint OS
The installer checks for Mint in `/etc/os-release`. If you're on another Debian-based distro, it will prompt for confirmation. For non-Debian systems, manual installation is required — see `docs/SETUP.md` for the manual dev setup guide.