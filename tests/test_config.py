import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from niri_theme_manager import THEMES, add_include, apply_theme, theme_path


class ConfigTests(unittest.TestCase):
    def test_include_added_once(self):
        first = add_include("layout { gaps 6 }\n")
        self.assertEqual(first, add_include(first))
        self.assertEqual(first.count('include "themes/active-theme.kdl"'), 1)

    def test_include_with_extra_whitespace_is_not_duplicated(self):
        config = 'layout { gaps 6 }\ninclude   "themes/active-theme.kdl"   \n'
        self.assertEqual(config, add_include(config))

    def test_empty_config(self):
        self.assertEqual(add_include(""), 'include "themes/active-theme.kdl"\n')

    def test_theme_fragments(self):
        for theme in THEMES.values():
            self.assertIn("layout {", theme["kdl"])
            self.assertIn("focus-ring {", theme["kdl"])
            self.assertIn("overview {", theme["kdl"])

    def test_apply(self):
        with TemporaryDirectory() as temp:
            config = Path(temp) / "niri" / "config.kdl"
            config.parent.mkdir()
            config.write_text("// existing config\n", encoding="utf-8")
            apply_theme("Neon Blue", config)
            self.assertIn('include "themes/active-theme.kdl"',
                          config.read_text(encoding="utf-8"))
            self.assertIn("#00bfff", theme_path(config).read_text(encoding="utf-8"))

    def test_validation_failure_restores_existing_files(self):
        with TemporaryDirectory() as temp:
            config = Path(temp) / "niri" / "config.kdl"
            config.parent.mkdir()
            config.write_text("// original config\n", encoding="utf-8")
            theme = theme_path(config)
            theme.parent.mkdir(parents=True)
            theme.write_text("// original theme\n", encoding="utf-8")
            failed_validation = subprocess.CompletedProcess(
                args=["niri", "validate"], returncode=1, stdout="", stderr="invalid config"
            )
            with patch("niri_theme_manager.shutil.which", return_value="/usr/bin/niri"), \
                 patch("niri_theme_manager.subprocess.run", return_value=failed_validation):
                with self.assertRaisesRegex(RuntimeError, "Niri rejected"):
                    apply_theme("Dark", config)
            self.assertEqual("// original config\n", config.read_text(encoding="utf-8"))
            self.assertEqual("// original theme\n", theme.read_text(encoding="utf-8"))

    def test_validation_failure_removes_new_files(self):
        with TemporaryDirectory() as temp:
            config = Path(temp) / "niri" / "config.kdl"
            failed_validation = subprocess.CompletedProcess(
                args=["niri", "validate"], returncode=1, stdout="", stderr="invalid config"
            )
            with patch("niri_theme_manager.shutil.which", return_value="/usr/bin/niri"), \
                 patch("niri_theme_manager.subprocess.run", return_value=failed_validation):
                with self.assertRaises(RuntimeError):
                    apply_theme("Light", config)
            self.assertFalse(config.exists())
            self.assertFalse(theme_path(config).exists())


if __name__ == "__main__":
    unittest.main()
