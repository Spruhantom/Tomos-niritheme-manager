#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/Spruhantom/Tomos-niritheme-manager.git"
WORKDIR="$(mktemp -d -t niri-theme-manager.XXXXXX)"
cleanup() { rm -rf "$WORKDIR"; }
trap cleanup EXIT

if [[ ! -r /etc/os-release ]]; then
  echo "Cannot identify this Linux distribution: /etc/os-release is missing." >&2
  exit 1
fi
# shellcheck disable=SC1091
. /etc/os-release
DISTRO_ID="${ID:-unknown}"
DISTRO_LIKE="${ID_LIKE:-}"
FAMILY="$DISTRO_ID $DISTRO_LIKE"

as_root() {
  if [[ "$(id -u)" -eq 0 ]]; then
    "$@"
  elif command -v sudo >/dev/null 2>&1; then
    sudo "$@"
  else
    echo "This step needs root privileges; install sudo or run this script as root." >&2
    exit 1
  fi
}

check_python_version() {
  if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 is required but was not found." >&2
    exit 1
  fi
  if ! python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)'; then
    echo "Python 3.10 or newer is required to install Niri Theme Manager." >&2
    python3 --version >&2
    exit 1
  fi
  echo "Python version check passed: $(python3 --version)"
}

echo "Detected distribution: ${PRETTY_NAME:-$DISTRO_ID}"

if [[ "$FAMILY" =~ (arch|manjaro|endeavouros) ]]; then
  if [[ "$(id -u)" -eq 0 ]]; then
    echo "On Arch-based systems, run this installer as a normal user (not with sudo)." >&2
    echo "The script will use sudo for package installation and makepkg will run safely as your user." >&2
    exit 1
  fi
  as_root pacman -S --needed --noconfirm git base-devel tk python
  check_python_version
  command -v makepkg >/dev/null 2>&1 || { echo "makepkg is unavailable; install base-devel." >&2; exit 1; }
  git clone --depth 1 "$REPO_URL" "$WORKDIR/source"
  cd "$WORKDIR/source"
  makepkg --syncdeps --install --noconfirm

elif [[ "$FAMILY" =~ (debian|ubuntu|linuxmint|pop) ]]; then
  as_root apt-get update
  as_root apt-get install -y git dpkg-dev python3 python3-tk
  check_python_version
  git clone --depth 1 "$REPO_URL" "$WORKDIR/source"
  cd "$WORKDIR/source"
  bash packaging/build-deb.sh
  as_root apt-get install -y "$PWD"/dist/niri-theme-manager_0.1.0-1_all.deb

elif [[ "$FAMILY" =~ (fedora|rhel|centos|rocky|almalinux) ]]; then
  if command -v dnf >/dev/null 2>&1; then
    as_root dnf install -y git rpm-build python3 python3-tkinter tar gzip
  elif command -v yum >/dev/null 2>&1; then
    as_root yum install -y git rpm-build python3 python3-tkinter tar gzip
  else
    echo "Neither dnf nor yum was found." >&2
    exit 1
  fi
  check_python_version
  git clone --depth 1 "$REPO_URL" "$WORKDIR/source"
  cd "$WORKDIR/source"
  bash packaging/build-rpm.sh
  RPM_FILE="$(find "$PWD/dist" -maxdepth 1 -type f -name '*.rpm' -print -quit)"
  [[ -n "$RPM_FILE" ]] || { echo "RPM build did not produce a package." >&2; exit 1; }
  if command -v dnf >/dev/null 2>&1; then
    as_root dnf install -y "$RPM_FILE"
  else
    as_root yum localinstall -y "$RPM_FILE"
  fi

elif [[ "$FAMILY" =~ (opensuse|suse|sles) ]]; then
  as_root zypper --non-interactive install git rpm-build python3 python3-tk tar gzip
  check_python_version
  git clone --depth 1 "$REPO_URL" "$WORKDIR/source"
  cd "$WORKDIR/source"
  bash packaging/build-rpm.sh
  RPM_FILE="$(find "$PWD/dist" -maxdepth 1 -type f -name '*.rpm' -print -quit)"
  [[ -n "$RPM_FILE" ]] || { echo "RPM build did not produce a package." >&2; exit 1; }
  as_root zypper --non-interactive install "$RPM_FILE"

else
  echo "Unsupported distribution: ID=${ID:-unknown}, ID_LIKE=${ID_LIKE:-none}" >&2
  echo "Supported families: Arch, Debian/Ubuntu, Fedora/RHEL, and openSUSE." >&2
  exit 1
fi

echo
echo "Niri Theme Manager has been installed."
echo "Launch it from your application menu or run: niri-theme-manager"
