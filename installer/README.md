# HomeNook Installer

Linux Mint Cinnamon deployment via `scripts/install.sh`.

## Verify a bundle from Depot

Select a versioned HomeNook bundle from Depot, the successor to Vendor.
Keep `uhome-bundle.json` with its component files at their declared paths.
Set `bundle_dir` to that directory in Depot or to its copy on an offline
machine, then verify the component checksums.

```bash
uhome verify-bundle --bundle-dir "$bundle_dir"
```

Use the same bundle directory for `uhome plan` and `uhome stage`. Keep staged
and installed files outside the Depot bundle. HomeNook owns the release
manifest and component pins. Sonic owns device provisioning.

## Quick Install

```bash
sudo bash scripts/install.sh
```

Opens the console at `http://localhost:8080` after install.

## What's Installed

| Component | Path |
|---|---|
| HomeNook root | `/opt/homenook/` |
| API server (systemd) | `homenook-server.service` on port 7890 |
| Console (nginx) | port 8080 |
| Media vault | `/home/homenook/media/` |
| udev rules | `/etc/udev/rules.d/99-uhome.rules` |

## Uninstall

```bash
sudo bash scripts/uninstall.sh          # services only
sudo bash scripts/uninstall.sh --purge  # full removal
```

Full documentation: `docs/INSTALLER.md`