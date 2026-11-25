#!/usr/bin/env bash
# ============================================================================
# HomeNook Installer — Linux Mint Cinnamon
# ============================================================================
# Installs HomeNook as a system service with Jellyfin, the HomeNook API,
# and the web console. Designed for Linux Mint 21.x/22.x (Cinnamon).
#
# Usage:
#   sudo bash scripts/install.sh
#
# Environment variables (optional):
#   HOMENOOK_USER       — system user to run services (default: homenook)
#   HOMENOOK_HOME       — install root (default: /opt/homenook)
#   HOMENOOK_MEDIA_ROOT — media vault path (default: /home/$HOMENOOK_USER/media)
#   HOMENOOK_PORT       — API listen port (default: 7890)
#   SKIP_JELLYFIN       — set to 1 to skip Jellyfin install
# ============================================================================

set -euo pipefail

# ── helpers ────────────────────────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log()  { echo -e "${GREEN}[HomeNook]${NC} $1"; }
warn() { echo -e "${YELLOW}[HomeNook]${NC} $1"; }
err()  { echo -e "${RED}[HomeNook]${NC} $1" >&2; }

# ── config ─────────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

HOMENOOK_USER="${HOMENOOK_USER:-homenook}"
HOMENOOK_HOME="${HOMENOOK_HOME:-/opt/homenook}"
HOMENOOK_MEDIA_ROOT="${HOMENOOK_MEDIA_ROOT:-/home/${HOMENOOK_USER}/media}"
HOMENOOK_PORT="${HOMENOOK_PORT:-7890}"
SKIP_JELLYFIN="${SKIP_JELLYFIN:-0}"
SYSTEMD_DIR="/etc/systemd/system"

# ── preflight ──────────────────────────────────────────────────────────────

if [[ "$(id -u)" -ne 0 ]]; then
  err "This script must be run as root (sudo bash scripts/install.sh)"
  exit 1
fi

if ! grep -qi "mint" /etc/os-release 2>/dev/null; then
  warn "This installer is designed for Linux Mint. Your OS may not be"
  warn "fully supported. Detected:"
  warn "  $(grep PRETTY_NAME /etc/os-release 2>/dev/null | cut -d= -f2 | tr -d '"' || echo 'Unknown')"
  read -p "Continue anyway? [y/N] " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi

log "HomeNook Installer for Linux Mint Cinnamon"
log "==========================================="
log "User:        ${HOMENOOK_USER}"
log "Install:     ${HOMENOOK_HOME}"
log "Media Root:  ${HOMENOOK_MEDIA_ROOT}"
log "API Port:    ${HOMENOOK_PORT}"
log "Repo Root:   ${REPO_ROOT}"
echo ""

# ── 1. System dependencies ─────────────────────────────────────────────────

log "[1/7] Installing system dependencies..."

apt-get update -qq
apt-get install -y -qq \
  python3 python3-pip python3-venv \
  curl git \
  sqlite3 \
  nginx \
  nodejs npm \
  2>&1 | tail -1

log "  System dependencies installed"

# ── 2. Create system user ──────────────────────────────────────────────────

log "[2/7] Creating homenook system user..."

if ! id "${HOMENOOK_USER}" &>/dev/null; then
  useradd --system --home-dir "${HOMENOOK_HOME}" \
    --shell /usr/sbin/nologin \
    --comment "HomeNook Service" \
    "${HOMENOOK_USER}"
  log "  User '${HOMENOOK_USER}' created"
else
  log "  User '${HOMENOOK_USER}' already exists"
fi

# ── 3. Media vault ─────────────────────────────────────────────────────────

log "[3/7] Setting up media vault..."

mkdir -p "${HOMENOOK_MEDIA_ROOT}/movies"
mkdir -p "${HOMENOOK_MEDIA_ROOT}/tv"
mkdir -p "${HOMENOOK_MEDIA_ROOT}/music"
chown -R "${HOMENOOK_USER}:${HOMENOOK_USER}" "${HOMENOOK_MEDIA_ROOT}"
chmod 755 "${HOMENOOK_MEDIA_ROOT}"
log "  Media vault at ${HOMENOOK_MEDIA_ROOT}"

# ── 4. Jellyfin ────────────────────────────────────────────────────────────

if [[ "${SKIP_JELLYFIN}" -eq 0 ]]; then
  log "[4/7] Installing Jellyfin..."
  if ! command -v jellyfin &>/dev/null; then
    curl -fsSL https://repo.jellyfin.org/install-debuntu.sh \
      | bash -s -- --yes 2>&1 | tail -3
    log "  Jellyfin installed"
  else
    log "  Jellyfin already installed"
  fi
else
  log "[4/7] Skipping Jellyfin (SKIP_JELLYFIN=1)"
fi

# ── 5. Copy HomeNook files ─────────────────────────────────────────────────

log "[5/7] Installing HomeNook to ${HOMENOOK_HOME}..."

mkdir -p "${HOMENOOK_HOME}"
cp -r "${REPO_ROOT}/server" "${HOMENOOK_HOME}/server"
cp -r "${REPO_ROOT}/apps" "${HOMENOOK_HOME}/apps"
cp -r "${REPO_ROOT}/config" "${HOMENOOK_HOME}/config"
cp -r "${REPO_ROOT}/packages" "${HOMENOOK_HOME}/packages"
[[ -f "${REPO_ROOT}/requirements.txt" ]] && \
  cp "${REPO_ROOT}/requirements.txt" "${HOMENOOK_HOME}/requirements.txt" || true
chown -R "${HOMENOOK_USER}:${HOMENOOK_USER}" "${HOMENOOK_HOME}"

log "  HomeNook files copied"

# Python dependencies
log "  Installing Python dependencies..."
if [[ -f "${HOMENOOK_HOME}/requirements.txt" ]]; then
  sudo -u "${HOMENOOK_USER}" python3 -m pip install --quiet \
    -r "${HOMENOOK_HOME}/requirements.txt" 2>&1 | tail -1
fi
log "  Python deps installed"

# Console build
log "  Building console..."
if [[ -d "${HOMENOOK_HOME}/apps/console" ]]; then
  cd "${HOMENOOK_HOME}/apps/console"
  npm install --silent 2>&1 | tail -1
  npm run build 2>&1 | tail -3
  cd "${REPO_ROOT}"
fi
log "  Console built"

# ── 6. systemd units ───────────────────────────────────────────────────────

log "[6/7] Installing systemd service units..."

# API server unit
cat > "${SYSTEMD_DIR}/homenook-server.service" << SYSTEMDEOF
[Unit]
Description=HomeNook API Server
After=network.target jellyfin.service
Wants=jellyfin.service

[Service]
Type=simple
User=${HOMENOOK_USER}
WorkingDirectory=${HOMENOOK_HOME}/server
Environment="PYTHONUNBUFFERED=1"
Environment="UHOME_MEDIA_ROOT=${HOMENOOK_MEDIA_ROOT}"
EnvironmentFile=-${HOMENOOK_HOME}/config/environment.env
ExecStart=python3 ${HOMENOOK_HOME}/server/api/main.py
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
SYSTEMDEOF

# Console unit (placeholder — nginx serves the static build)
cat > "${SYSTEMD_DIR}/homenook-console.service" << SYSTEMDEOF
[Unit]
Description=HomeNook Console (nginx frontend)
After=network.target homenook-server.service

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/bin/true
ExecStop=/bin/true

[Install]
WantedBy=multi-user.target
SYSTEMDEOF

# nginx site config
cat > /etc/nginx/sites-available/homenook << NGINXEOF
server {
    listen 8080;
    server_name _;

    root ${HOMENOOK_HOME}/apps/console/dist;
    index index.html;

    location / {
        try_files \$uri \$uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:${HOMENOOK_PORT};
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
NGINXEOF

rm -f /etc/nginx/sites-enabled/default 2>/dev/null || true
ln -sf /etc/nginx/sites-available/homenook \
  /etc/nginx/sites-enabled/homenook 2>/dev/null || true

systemctl daemon-reload
systemctl enable homenook-server.service
systemctl enable homenook-console.service 2>/dev/null || true
systemctl enable nginx 2>/dev/null || true

log "  systemd units installed"

# ── 6b. Cinnamon desktop shortcut ──────────────────────────────────────────

log "  Installing Cinnamon desktop shortcut..."
if [[ -d /usr/share/applications ]]; then
  if [[ -f "${REPO_ROOT}/installer/homenook.desktop" ]]; then
    cp "${REPO_ROOT}/installer/homenook.desktop" \
      /usr/share/applications/homenook.desktop
    log "    Desktop shortcut installed"
  fi
fi

# ── 6c. First-run-launch script ────────────────────────────────────────────

log "  Installing first-run-launch script..."
mkdir -p "${HOMENOOK_HOME}/scripts"
cp "${REPO_ROOT}/scripts/first-run-launch.sh" \
  "${HOMENOOK_HOME}/scripts/first-run-launch.sh"
chmod +x "${HOMENOOK_HOME}/scripts/first-run-launch.sh"
log "    first-run-launch.sh at ${HOMENOOK_HOME}/scripts/"

# ── 7. udev rules ──────────────────────────────────────────────────────────

log "[7/7] Installing udev rules..."

if [[ -f "${REPO_ROOT}/installer/udev/99-uhome.rules" ]]; then
  cp "${REPO_ROOT}/installer/udev/99-uhome.rules" \
    /etc/udev/rules.d/99-uhome.rules
  udevadm control --reload-rules 2>/dev/null || true
  udevadm trigger 2>/dev/null || true
  log "  udev rules installed"
else
  log "  No udev rules to install"
fi

# ── Start services ─────────────────────────────────────────────────────────

log ""
log "==========================================="
log "Installation complete!"
log ""
log "Starting services..."
systemctl restart homenook-server.service
systemctl restart nginx
sleep 2

if systemctl is-active --quiet homenook-server.service; then
  log "  API server running on http://localhost:${HOMENOOK_PORT}"
else
  warn "  API server may not have started."
  warn "  Check: journalctl -u homenook-server -n 20"
fi

log "  Console at http://localhost:8080"
log ""
log "Next steps:"
log "  1. Open http://localhost:8080 in your browser"
log "  2. Settings → Connect Jellyfin (Dashboard → API Keys)"
log "  3. Settings → Connect Home Assistant (Profile → Tokens)"
log ""
log "Manage services:"
log "  sudo systemctl {start|stop|restart} homenook-server"
log "  sudo journalctl -u homenook-server -f"
log ""
log "Uninstall:"
log "  sudo bash ${REPO_ROOT}/scripts/uninstall.sh"