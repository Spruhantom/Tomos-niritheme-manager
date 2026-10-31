#!/usr/bin/env bash
set -euo pipefail

repo='https://github.com/Spruhantom/Tomos-niritheme-manager.git'
workdir="$(mktemp -d -t niri-theme-manager.XXXXXX)"
cleanup() { rm -rf "$workdir"; }
trap cleanup EXIT

if [[ ! -r /etc/arch-release ]] || ! command -v pacman >/dev/null 2>&1; then
  printf '%s\n' 'This installer is for Arch Linux and Arch-based distributions.' >&2
  exit 1
fi
if ! command -v git >/dev/null 2>&1; then
  printf '%s\n' 'Git is required. Install it with: sudo pacman -S git' >&2
  exit 1
fi
if [[ "$(id -u)" -eq 0 ]]; then
  printf '%s\\n' 'Do not run this installer as root; makepkg must run as a normal user.' >&2
  exit 1
fi
if ! command -v makepkg >/dev/null 2>&1; then
  printf '%s\n' 'makepkg is required. Install the base-devel group first.' >&2
  exit 1
fi

git clone --depth 1 "$repo" "$workdir/source"
cd "$workdir/source"
makepkg --syncdeps --install --noconfirm
printf '\n%s\n' 'Niri Theme Manager installation finished.'
