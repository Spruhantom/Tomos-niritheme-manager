# Niri Theme Manager

A small Python/Tkinter desktop app for switching Niri compositor themes.

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

Niri watches included config files and automatically reloads changes. The manager
makes timestamped backups of files it changes. If `niri validate` is available
and validation fails, it restores the previous files.

Existing settings are preserved. The include is appended to the config so these
theme values take precedence over earlier settings. This changes Niri compositor
settings (focus ring, gaps, border state and overview backdrop); it does not
re-theme applications or desktop panels.

## Requirements

- Linux running Niri
- Python 3.10+
- Tkinter (`python3-tk`)
- Niri on PATH for automatic validation (optional)

## Run

Debian/Ubuntu: `sudo apt install python3-tk`
Fedora: `sudo dnf install python3-tkinter`

Then run:

```bash
python3 niri_theme_manager.py
```

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT. See [LICENSE](LICENSE).
