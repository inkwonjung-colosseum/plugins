from __future__ import annotations

import json
from pathlib import Path
import unittest


PLUGIN_ROOT = Path(__file__).resolve().parents[1]


class SkeletonPluginStructureTests(unittest.TestCase):
    def test_claude_manifest_does_not_duplicate_standard_hooks_file(self) -> None:
        manifest = json.loads(
            (PLUGIN_ROOT / ".claude-plugin" / "plugin.json").read_text()
        )

        self.assertTrue((PLUGIN_ROOT / "hooks" / "hooks.json").exists())
        self.assertNotEqual(manifest.get("hooks"), "./hooks/hooks.json")


if __name__ == "__main__":
    unittest.main()
