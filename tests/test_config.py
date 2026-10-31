import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from niri_theme_manager import THEMES, add_include, apply_theme, theme_path

class ConfigTests(unittest.TestCase):
    def test_include_added_once(self):
        first = add_include("layout { gaps 6 }\n")
        self.assertEqual(first, add_include(first))
        self.assertEqual(first.count('include "themes/active-theme.kdl"'), 1)

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

if __name__ == "__main__":
    unittest.main()
