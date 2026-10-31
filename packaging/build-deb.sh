#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
command -v dpkg-deb >/dev/null || { echo 'dpkg-deb is required.' >&2; exit 1; }
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT
install -Dpm0755 "$ROOT/niri-theme-manager" "$STAGE/usr/bin/niri-theme-manager"
install -Dpm0644 "$ROOT/niri_theme_manager.py" "$STAGE/usr/share/niri-theme-manager/niri_theme_manager.py"
install -Dpm0644 "$ROOT/niri-theme-manager.desktop" "$STAGE/usr/share/applications/niri-theme-manager.desktop"
install -Dpm0644 "$ROOT/LICENSE" "$STAGE/usr/share/doc/niri-theme-manager/copyright"
install -Dpm0644 "$ROOT/README.md" "$STAGE/usr/share/doc/niri-theme-manager/README.md"
mkdir -p "$STAGE/DEBIAN"
cat > "$STAGE/DEBIAN/control" <<'CONTROL'
Package: niri-theme-manager
Version: 0.1.0-1
Section: utils
Priority: optional
Architecture: all
Depends: python3 (>= 3.10), python3-tk
Recommends: niri
Maintainer: Tom's Tech Support <tom@tomserver.co.uk>
Description: Desktop theme switcher for the Niri compositor
 A small Python/Tkinter desktop application for switching between
 Neon Blue, Dark, and Light themes for the Niri Wayland compositor.
CONTROL
mkdir -p "$ROOT/dist"
dpkg-deb --root-owner-group --build "$STAGE" "$ROOT/dist/niri-theme-manager_0.1.0-1_all.deb"
dpkg-deb --info "$ROOT/dist/niri-theme-manager_0.1.0-1_all.deb"
