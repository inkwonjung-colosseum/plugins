"""
Codex marketplace metadata visibility tests.
"""

import json
import re
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CODEX_MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def contains_korean(text):
    return bool(re.search(r"[가-힣]", text))


class TestCodexMarketplaceMetadata(unittest.TestCase):

    def test_marketplace_display_name_is_korean(self):
        marketplace = load_json(CODEX_MARKETPLACE)
        self.assertTrue(contains_korean(marketplace["interface"]["displayName"]))

    def test_codex_visible_plugin_copy_is_korean_first(self):
        plugin_dirs = [
            entry["source"]["path"]
            for entry in load_json(CODEX_MARKETPLACE)["plugins"]
        ]

        for plugin_dir in plugin_dirs:
            manifest_path = ROOT / plugin_dir / ".codex-plugin" / "plugin.json"
            manifest = load_json(manifest_path)
            interface = manifest["interface"]
            fields = [
                manifest["description"],
                interface["shortDescription"],
                interface["longDescription"],
                *interface["defaultPrompt"],
            ]

            for field in fields:
                with self.subTest(plugin=manifest["name"], field=field):
                    self.assertTrue(contains_korean(field))


if __name__ == "__main__":
    unittest.main()
