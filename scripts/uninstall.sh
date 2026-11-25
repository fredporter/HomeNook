#!/usr/bin/env bash
# ============================================================================
# HomeNook Uninstaller
# ============================================================================
# Removes HomeNook services, systemd units, and optionally the install
# directory. Does NOT remove Jellyfin, nginx, or system dependencies
# (they may be used by other services).
#
# Usage:
#   sudo bash scripts/uninstall.sh
#   sudo bash scripts/uninstall.sh --purge  (also remove /opt/homenook + media)
# ============================================================================

set -euo pipefail

PURGE=0
if [[ "${1:-}" == "--purge" ]]; then
  PURGE=1
fi

HOMENOOK_HOME="${HOMENOOK_HOME:-/opt/homenook}"

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'
log()  { echo -e "${GREEN}[HomeNook]${NC} $1"; }
warn() { echo -e "${RED}[HomeNook]${NC} $1"; }

if [[ "$(id -u)" -ne 0 ]]; then
  warn "This script must be run as root (sudo bash scripts/uninstall.sh)"
  exit 1
fi

log "HomeNook Uninstaller"
log "===================="
echo ""

# 1. Stop services
log "[1/5] Stopping services..."
systemctl stop homenook-server.service 2>/dev/null || true
systemctl stop nginx 2>/dev/null || true
log "  Services stopped"

# 2. Disable + remove systemd units
log "[2/5] Removing systemd units..."
systemctl disable homenook-server.service 2>/dev/null || true
systemctl disable homenook-console.service 2>/dev/null || true
rm -f /etc/systemd/system/homenook-server.service
rm -f /etc/systemd/system/homenook-console.service
rm -f /etc/nginx/sites-available/homenook
rm -f /etc/nginx/sites-enabled/homenook
systemctl daemon-reload
log "  systemd units removed"

# 3. udev rules
log "[3/5] Removing udev rules..."
rm -f /etc/udev/rules.d/99-uhome.rules
udevadm control --reload-rules 2>/dev/null || true
log "  udev rules removed"

# 4. nginx default site restore
log "[4/5] Restoring nginx default..."
if [[ ! -f /etc/nginx/sites-enabled/default ]]; then
  if [[ -f /etc/nginx/sites-available/default ]]; then
    ln -sf /etc/nginx/sites-available/default \
      /etc/nginx/sites-enabled/default
  fi
fi
systemctl reload nginx 2>/dev/null || true
log "  nginx restored"

# 5. Purge (optional)
if [[ "${PURGE}" -eq 1 ]]; then
  log "[5/5] Purging HomeNook files..."
  rm -rf "${HOMENOOK_HOME}"
  if id homenook &>/dev/null; then
    userdel homenook 2>/dev/null || true
    log "  User 'homenook' removed"
  fi
  log "  ${HOMENOOK_HOME} removed"
else
  log "[5/5] Skipping purge (use --purge to remove ${HOMENOOK_HOME})"
fi

log ""
log "Uninstall complete."
log ""
if [[ "${PURGE}" -eq 0 ]]; then
  warn "Note: ${HOMENOOK_HOME} was NOT removed."
  warn "Run with --purge to fully remove."
fi

log ""
log "To reinstall:"
log "  sudo bash scripts/install.sh"