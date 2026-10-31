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

This downloads and runs the installer directly from this repository. For safety,
review `install-arch.sh` before executing it if you want to inspect the commands.

The installer clones the repository into a temporary directory and builds and
installs the package using `makepkg`.

To build the package manually:

```bash
git clone https://github.com/Spruhantom/Tomos-niritheme-manager.git
cd Tomos-niritheme-manager
makepkg --syncdeps --install
```

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
theme values take precedence over earlier settings. This changes Niri compositor
settings (focus ring, gaps, border state and overview backdrop); it does not
re-theme applications or desktop panels.

## Requirements

- Linux running Niri
- Python 3.10+
- Tkinter (`tk` on Arch Linux)
- Niri on PATH for automatic validation (optional)
- `xdg-utils` to open the configuration folder from the app (optional)

## Run from source

```bash
python3 niri_theme_manager.py
```

## Tests

```bash
python3 -m unittest discover -s tests -v
```

The Arch package's `check()` function runs this test suite during `makepkg`.

## License

MIT. See [LICENSE](LICENSE).
