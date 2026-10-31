# Niri Theme Manager

A small Python/Tkinter desktop app for switching Niri compositor themes.

## Universal Linux installer

The distro detector reads `/etc/os-release`, installs the required build tools,
builds the native package, and installs it using the system package manager.

Supported distribution families:
- Arch Linux, Manjaro, EndeavourOS
- Debian, Ubuntu, Linux Mint, Pop!_OS
- Fedora, RHEL, CentOS, Rocky Linux, AlmaLinux
- openSUSE and SUSE Linux Enterprise

Run the universal installer:

```bash
curl -fsSL https://raw.githubusercontent.com/Spruhantom/Tomos-niritheme-manager/main/install-linux.sh | bash
```

The script uses `sudo` when needed, or can be run as root. It installs build
dependencies through the detected distribution's package manager. Review
`install-linux.sh` before piping it into Bash if you want to inspect it first.

Unsupported distributions are stopped with a clear message; the installer does
not guess a package manager.

## Build packages manually

### Arch Linux

```bash
sudo pacman -S --needed base-devel git
makepkg -si
```

### Debian / Ubuntu (.deb)

```bash
sudo apt install dpkg-dev python3-tk
bash packaging/build-deb.sh
sudo apt install ./dist/niri-theme-manager_0.1.0-1_all.deb
```

### Fedora / RHEL / openSUSE (.rpm)

Install `rpm-build`, Git, and Tkinter development/runtime packages using your
distribution's package manager, then run:

```bash
bash packaging/build-rpm.sh
```

The package will be written to `dist/`.

GitHub Actions also builds Debian and RPM packages as workflow artifacts.
The Debian package is architecture-independent (`all`); the RPM is
architecture-independent (`noarch`).

## Included themes

- **Neon Blue** — deep navy overview with a bright cyan focus ring.
- **Dark** — charcoal background and soft grey focus ring.
- **Light** — pale background with a blue focus ring.

## How it works

The app writes `~/.config/niri/themes/active-theme.kdl` and adds this top-level
include to your Niri config (only once):

```kdl
include "themes/active-theme.kdl"
```

Niri watches included config files and reloads changes automatically. The manager
makes timestamped backups of files it changes. If `niri validate` is available
and validation fails, it restores the previous files.

Existing settings are preserved. The include is appended to the config so these
theme values take precedence over earlier settings.

## Requirements

- Linux running Niri
- Python 3.10+
- Tkinter
- Niri on PATH for automatic validation (optional)
- `xdg-utils` to open the Niri configuration folder from the app (optional)

## Run from source

```bash
python3 niri_theme_manager.py
```

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT. See [LICENSE](LICENSE).
