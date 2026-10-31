#!/usr/bin/env python3
import os
import re
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

APP_NAME = "Niri Theme Manager"
THEME_FILE = "active-theme.kdl"

THEMES = {
    "Neon Blue": {
        "accent": "#00bfff", "background": "#07111f", "muted": "#183047", "text": "#d9f4ff",
        "kdl": '''// Niri Theme Manager — Neon Blue
layout {
    gaps 10
    focus-ring {
        width 3
        active-color "#00bfff"
        inactive-color "#24506b"
    }
    border { off }
}
overview {
    backdrop-color "#07111f"
}
'''
    },
    "Dark": {
        "accent": "#a0a0a0", "background": "#17191d", "muted": "#343941", "text": "#eeeeee",
        "kdl": '''// Niri Theme Manager — Dark
layout {
    gaps 8
    focus-ring {
        width 2
        active-color "#a0a0a0"
        inactive-color "#454a52"
    }
    border { off }
}
overview {
    backdrop-color "#17191d"
}
'''
    },
    "Light": {
        "accent": "#3978c5", "background": "#edf2f8", "muted": "#cbd6e4", "text": "#182536",
        "kdl": '''// Niri Theme Manager — Light
layout {
    gaps 8
    focus-ring {
        width 2
        active-color "#3978c5"
        inactive-color "#9aaabd"
    }
    border { off }
}
overview {
    backdrop-color "#edf2f8"
}
'''
    },
}

def niri_config_path():
    override = os.environ.get("NIRI_CONFIG")
    if override:
        return Path(override).expanduser()
    xdg = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return xdg / "niri" / "config.kdl"

def theme_path(config_path):
    return config_path.parent / "themes" / THEME_FILE

def add_include(config_text):
    line = 'include "themes/active-theme.kdl"'
    include_pattern = re.compile(
        r'^[ \t]*include[ \t]+"themes/active-theme\.kdl"[ \t]*(?://.*)?

def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise

def backup_file(path):
    if not path.exists():
        return None
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = path.with_name(f"{path.name}.backup-{stamp}")
    index = 1
    while backup.exists():
        backup = path.with_name(f"{path.name}.backup-{stamp}-{index}")
        index += 1
    shutil.copy2(path, backup)
    return backup

def apply_theme(name, config_path=None):
    if name not in THEMES:
        raise ValueError(f"Unknown theme: {name}")
    config = config_path or niri_config_path()
    target_theme = theme_path(config)
    config.parent.mkdir(parents=True, exist_ok=True)
    old_config = config.read_text(encoding="utf-8") if config.exists() else ""
    old_theme = target_theme.read_text(encoding="utf-8") if target_theme.exists() else None
    config_backup = backup_file(config)
    backup_file(target_theme)
    try:
        atomic_write(target_theme, THEMES[name]["kdl"])
        atomic_write(config, add_include(old_config))
        validator = shutil.which("niri")
        if validator:
            env = os.environ.copy()
            env["NIRI_CONFIG"] = str(config)
            result = subprocess.run([validator, "validate"], env=env,
                                    capture_output=True, text=True, timeout=15, check=False)
            if result.returncode:
                detail = (result.stderr or result.stdout or "Unknown validation error").strip()
                raise RuntimeError("Niri rejected the configuration:\n" + detail)
            return f"{name} applied. Niri validated the configuration."
        return f"{name} applied. Niri was not found, so validation was skipped."
    except Exception:
        if old_theme is None:
            target_theme.unlink(missing_ok=True)
        else:
            atomic_write(target_theme, old_theme)
        if config_backup is None:
            config.unlink(missing_ok=True)
        else:
            shutil.copy2(config_backup, config)
        raise

class ThemeManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("690x470")
        self.minsize(600, 420)
        self.configure(bg="#0b1220")
        self.selected = tk.StringVar(value="Neon Blue")
        self.status = tk.StringVar(value="Choose a theme, then select Apply Theme.")
        self.build()
        self.select_theme("Neon Blue")

    def build(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TButton", padding=9, font=("TkDefaultFont", 10, "bold"))
        style.configure("TLabel", background="#0b1220", foreground="#e7f3ff")
        style.configure("Header.TLabel", font=("TkDefaultFont", 22, "bold"))
        style.configure("Sub.TLabel", foreground="#9fb5ca")
        outer = tk.Frame(self, bg="#0b1220", padx=28, pady=24)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="NIRI THEME MANAGER", style="Header.TLabel").pack(anchor="w")
        ttk.Label(outer, text="Switch your Niri look in one click.",
                  style="Sub.TLabel").pack(anchor="w", pady=(4, 20))
        cards = tk.Frame(outer, bg="#0b1220")
        cards.pack(fill="x")
        for name, theme in THEMES.items():
            card = tk.Frame(cards, bg="#111d2e", padx=14, pady=14,
                            highlightthickness=2, highlightbackground="#26384c")
            card.pack(side="left", fill="both", expand=True, padx=(0, 10))
            tk.Label(card, text=name, bg="#111d2e", fg="#e7f3ff",
                     font=("TkDefaultFont", 12, "bold")).pack(anchor="w")
            swatches = tk.Frame(card, bg="#111d2e")
            swatches.pack(anchor="w", pady=12)
            for color in (theme["background"], theme["muted"], theme["accent"]):
                tk.Label(swatches, bg=color, width=4, height=2).pack(side="left", padx=(0, 5))
            ttk.Radiobutton(card, text="Select", variable=self.selected, value=name,
                            command=lambda n=name: self.select_theme(n)).pack(anchor="w")
            card.bind("<Button-1>", lambda _event, n=name: self.choose(n))
        self.preview = tk.Frame(outer, bg="#07111f", height=95, padx=18, pady=14)
        self.preview.pack(fill="x", pady=(22, 14))
        self.preview.pack_propagate(False)
        self.preview_title = tk.Label(self.preview, text="", font=("TkDefaultFont", 14, "bold"))
        self.preview_title.pack(anchor="w")
        self.preview_desc = tk.Label(self.preview, text="")
        self.preview_desc.pack(anchor="w", pady=(5, 0))
        actions = tk.Frame(outer, bg="#0b1220")
        actions.pack(fill="x")
        ttk.Button(actions, text="Apply Theme", command=self.apply).pack(side="left")
        ttk.Button(actions, text="Open Niri Config Folder", command=self.open_config).pack(
            side="left", padx=10)
        ttk.Label(outer, textvariable=self.status, style="Sub.TLabel",
                  wraplength=620).pack(anchor="w", pady=(16, 0))
        ttk.Label(outer, text="Your config is backed up before changes are made.",
                  style="Sub.TLabel").pack(anchor="w", pady=(8, 0))

    def choose(self, name):
        self.selected.set(name)
        self.select_theme(name)

    def select_theme(self, name):
        theme = THEMES[name]
        self.preview.configure(bg=theme["background"])
        self.preview_title.configure(text=name, bg=theme["background"], fg=theme["accent"])
        self.preview_desc.configure(
            text="Accent " + theme["accent"] + "  •  Overview " + theme["background"],
            bg=theme["background"], fg=theme["text"])

    def apply(self):
        try:
            result = apply_theme(self.selected.get())
            self.status.set(result)
            messagebox.showinfo(APP_NAME, result)
        except Exception as exc:
            self.status.set("Could not apply theme: " + str(exc))
            messagebox.showerror(APP_NAME, str(exc))

    def open_config(self):
        folder = niri_config_path().parent
        folder.mkdir(parents=True, exist_ok=True)
        opener = shutil.which("xdg-open")
        if opener:
            subprocess.Popen([opener, str(folder)])
        else:
            self.status.set("Config folder: " + str(folder))

if __name__ == "__main__":
    ThemeManager().mainloop()
,
        re.MULTILINE,
    )
    if include_pattern.search(config_text):
        return config_text if config_text.endswith("\n") else config_text + "\n"
    prefix = config_text.rstrip()
    return (prefix + "\n\n" if prefix else "") + line + "\n"

def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise

def backup_file(path):
    if not path.exists():
        return None
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = path.with_name(f"{path.name}.backup-{stamp}")
    index = 1
    while backup.exists():
        backup = path.with_name(f"{path.name}.backup-{stamp}-{index}")
        index += 1
    shutil.copy2(path, backup)
    return backup

def apply_theme(name, config_path=None):
    if name not in THEMES:
        raise ValueError(f"Unknown theme: {name}")
    config = config_path or niri_config_path()
    target_theme = theme_path(config)
    config.parent.mkdir(parents=True, exist_ok=True)
    old_config = config.read_text(encoding="utf-8") if config.exists() else ""
    old_theme = target_theme.read_text(encoding="utf-8") if target_theme.exists() else None
    config_backup = backup_file(config)
    backup_file(target_theme)
    try:
        atomic_write(target_theme, THEMES[name]["kdl"])
        atomic_write(config, add_include(old_config))
        validator = shutil.which("niri")
        if validator:
            env = os.environ.copy()
            env["NIRI_CONFIG"] = str(config)
            result = subprocess.run([validator, "validate"], env=env,
                                    capture_output=True, text=True, timeout=15, check=False)
            if result.returncode:
                detail = (result.stderr or result.stdout or "Unknown validation error").strip()
                raise RuntimeError("Niri rejected the configuration:\n" + detail)
            return f"{name} applied. Niri validated the configuration."
        return f"{name} applied. Niri was not found, so validation was skipped."
    except Exception:
        if old_theme is None:
            target_theme.unlink(missing_ok=True)
        else:
            atomic_write(target_theme, old_theme)
        if config_backup is None:
            config.unlink(missing_ok=True)
        else:
            shutil.copy2(config_backup, config)
        raise

class ThemeManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("690x470")
        self.minsize(600, 420)
        self.configure(bg="#0b1220")
        self.selected = tk.StringVar(value="Neon Blue")
        self.status = tk.StringVar(value="Choose a theme, then select Apply Theme.")
        self.build()
        self.select_theme("Neon Blue")

    def build(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TButton", padding=9, font=("TkDefaultFont", 10, "bold"))
        style.configure("TLabel", background="#0b1220", foreground="#e7f3ff")
        style.configure("Header.TLabel", font=("TkDefaultFont", 22, "bold"))
        style.configure("Sub.TLabel", foreground="#9fb5ca")
        outer = tk.Frame(self, bg="#0b1220", padx=28, pady=24)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="NIRI THEME MANAGER", style="Header.TLabel").pack(anchor="w")
        ttk.Label(outer, text="Switch your Niri look in one click.",
                  style="Sub.TLabel").pack(anchor="w", pady=(4, 20))
        cards = tk.Frame(outer, bg="#0b1220")
        cards.pack(fill="x")
        for name, theme in THEMES.items():
            card = tk.Frame(cards, bg="#111d2e", padx=14, pady=14,
                            highlightthickness=2, highlightbackground="#26384c")
            card.pack(side="left", fill="both", expand=True, padx=(0, 10))
            tk.Label(card, text=name, bg="#111d2e", fg="#e7f3ff",
                     font=("TkDefaultFont", 12, "bold")).pack(anchor="w")
            swatches = tk.Frame(card, bg="#111d2e")
            swatches.pack(anchor="w", pady=12)
            for color in (theme["background"], theme["muted"], theme["accent"]):
                tk.Label(swatches, bg=color, width=4, height=2).pack(side="left", padx=(0, 5))
            ttk.Radiobutton(card, text="Select", variable=self.selected, value=name,
                            command=lambda n=name: self.select_theme(n)).pack(anchor="w")
            card.bind("<Button-1>", lambda _event, n=name: self.choose(n))
        self.preview = tk.Frame(outer, bg="#07111f", height=95, padx=18, pady=14)
        self.preview.pack(fill="x", pady=(22, 14))
        self.preview.pack_propagate(False)
        self.preview_title = tk.Label(self.preview, text="", font=("TkDefaultFont", 14, "bold"))
        self.preview_title.pack(anchor="w")
        self.preview_desc = tk.Label(self.preview, text="")
        self.preview_desc.pack(anchor="w", pady=(5, 0))
        actions = tk.Frame(outer, bg="#0b1220")
        actions.pack(fill="x")
        ttk.Button(actions, text="Apply Theme", command=self.apply).pack(side="left")
        ttk.Button(actions, text="Open Niri Config Folder", command=self.open_config).pack(
            side="left", padx=10)
        ttk.Label(outer, textvariable=self.status, style="Sub.TLabel",
                  wraplength=620).pack(anchor="w", pady=(16, 0))
        ttk.Label(outer, text="Your config is backed up before changes are made.",
                  style="Sub.TLabel").pack(anchor="w", pady=(8, 0))

    def choose(self, name):
        self.selected.set(name)
        self.select_theme(name)

    def select_theme(self, name):
        theme = THEMES[name]
        self.preview.configure(bg=theme["background"])
        self.preview_title.configure(text=name, bg=theme["background"], fg=theme["accent"])
        self.preview_desc.configure(
            text="Accent " + theme["accent"] + "  •  Overview " + theme["background"],
            bg=theme["background"], fg=theme["text"])

    def apply(self):
        try:
            result = apply_theme(self.selected.get())
            self.status.set(result)
            messagebox.showinfo(APP_NAME, result)
        except Exception as exc:
            self.status.set("Could not apply theme: " + str(exc))
            messagebox.showerror(APP_NAME, str(exc))

    def open_config(self):
        folder = niri_config_path().parent
        folder.mkdir(parents=True, exist_ok=True)
        opener = shutil.which("xdg-open")
        if opener:
            subprocess.Popen([opener, str(folder)])
        else:
            self.status.set("Config folder: " + str(folder))

if __name__ == "__main__":
    ThemeManager().mainloop()
