#!/bin/bash
# Report the HomeNook checkout and its local delivery catalogue.

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
workspace_root="$(dirname "$repo_root")"

echo "HomeNook checkout: $repo_root"
git -C "$repo_root" status --short --branch

if [ -d "$workspace_root/Depot" ]; then
    echo "Depot catalogue: $workspace_root/Depot"
elif [ -d "$workspace_root/Vendor" ]; then
    echo "Depot transition: existing source catalogue at $workspace_root/Vendor"
else
    echo "Depot catalogue unavailable at $workspace_root/Depot"
fi
