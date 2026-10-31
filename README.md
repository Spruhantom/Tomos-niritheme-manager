# Niri Theme Manager

A small Python/Tkinter desktop app for switching Niri compositor themes.

## Included themes

- **Neon Blue** — deep navy overview with a bright cyan focus ring.
- **Dark** — charcoal background and soft grey focus ring.
- **Light** — pale background with a blue focus ring.

## Arch Linux installation

Install the `base-devel` group and Git if they are not already installed:

```bash
sudo pacman -S --needed base-devel git
```

Then run the one-line installer:

```bash
curl -fsSL https://raw.githubusercontent.com/Spruhantom/Tomos-niritheme-manager/main/install-arch.sh | bash
```

The installer clones this repository into a temporary directory and builds and
installs the package using `makepkg`. Review `install-arch.sh` before running a
remote installer if you prefer to inspect the commands first.

To build the package manually:

```bash
git clone https://github.com/Spruhantom/Tomos-niritheme-manager.git
cd Tomos-niritheme-manager
makepkg -si
```

## Debian / Ubuntu (.deb)

Install a downloaded package with:

```bash
sudo apt install ./niri-theme-manager_0.1.0-1_all.deb
```

To build from a source checkout, install `dpkg-deb` and run:

```bash
packaging/build-deb.sh
```

## Fedora / RPM-based distributions (.rpm)

Install a downloaded package with:

```bash
sudo dnf install ./niri-theme-manager-0.1.0-1*.noarch.rpm
```

To build from source, install `rpm-build` and `python3-tkinter`, then run:

```bash
packaging/build-rpm.sh
```

GitHub Actions builds both package formats and publishes them as downloadable
workflow artifacts. The Debian package is architecture-independent (`all`);
the RPM is architecture-independent (`noarch`).

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
- Tkinter (`tk` on Arch Linux)
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
