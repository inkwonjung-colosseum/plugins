from __future__ import annotations

from pathlib import Path
import unittest


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
REMOVED_SETUP_SHORTCUTS = ("set-" + "api-key", "set-" + "output-path")


class RemovedSetupShortcutSkillTests(unittest.TestCase):
    def test_removed_setup_shortcut_skill_directories_do_not_exist(self) -> None:
        for skill_name in REMOVED_SETUP_SHORTCUTS:
            with self.subTest(skill_name=skill_name):
                self.assertFalse((PLUGIN_ROOT / "skills" / skill_name).exists())

    def test_user_facing_docs_do_not_reference_removed_setup_shortcuts(self) -> None:
        docs = [
            PLUGIN_ROOT / "README.md",
            PLUGIN_ROOT / "docs" / "confluence-markdown-exporter-supported-features.md",
            PLUGIN_ROOT / ".claude-plugin" / "plugin.json",
            PLUGIN_ROOT / ".codex-plugin" / "plugin.json",
        ]
        for doc_path in docs:
            content = doc_path.read_text()
            for skill_name in REMOVED_SETUP_SHORTCUTS:
                with self.subTest(doc=doc_path.name, skill_name=skill_name):
                    self.assertNotIn(skill_name, content)


if __name__ == "__main__":
    unittest.main()
