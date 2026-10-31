#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
command -v rpmbuild >/dev/null || { echo 'rpmbuild is required (install rpm-build).' >&2; exit 1; }
TOPDIR="$(mktemp -d)"
trap 'rm -rf "$TOPDIR"' EXIT
mkdir -p "$TOPDIR"/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
TAR="$TOPDIR/SOURCES/niri-theme-manager-0.1.0.tar.gz"
tar --exclude="$(basename "$ROOT")/dist" \
  --exclude="$(basename "$ROOT")/__pycache__" \
  --exclude="$(basename "$ROOT")/.git" \
  --transform="s,^$(basename "$ROOT"),$(basename "$ROOT")-0.1.0," \
  -czf "$TAR" -C "$(dirname "$ROOT")" "$(basename "$ROOT")"
rpmbuild -ba "$ROOT/packaging/rpm/niri-theme-manager.spec" \
  --define "_topdir $TOPDIR" --define "_sourcedir $TOPDIR/SOURCES"
mkdir -p "$ROOT/dist"
cp "$TOPDIR"/RPMS/noarch/*.rpm "$ROOT/dist/"
