from __future__ import annotations

from pathlib import Path
import unittest


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PLUGIN_ROOT.parent
REMOVED_SKILLS = ("export-by-" + "keyword", "export-by-" + "label", "export-page-tree")
REMOVED_USER_FACING_TERMS = REMOVED_SKILLS + ("keyword export", "page-tree export")


class RemovedSearchExportSkillTests(unittest.TestCase):
    def test_removed_search_export_skill_directories_do_not_exist(self) -> None:
        for skill_name in REMOVED_SKILLS:
            with self.subTest(skill_name=skill_name):
                self.assertFalse((PLUGIN_ROOT / "skills" / skill_name).exists())

    def test_user_facing_docs_do_not_reference_removed_skills(self) -> None:
        docs = [
            PLUGIN_ROOT / "README.md",
            PLUGIN_ROOT / "docs" / "confluence-markdown-exporter-supported-features.md",
            PLUGIN_ROOT / "skills" / "help" / "SKILL.md",
            PLUGIN_ROOT / ".claude-plugin" / "plugin.json",
            PLUGIN_ROOT / ".codex-plugin" / "plugin.json",
            WORKSPACE_ROOT / ".claude-plugin" / "marketplace.json",
        ]
        for doc_path in docs:
            content = doc_path.read_text()
            for removed_term in REMOVED_USER_FACING_TERMS:
                with self.subTest(doc=doc_path.name, removed_term=removed_term):
                    self.assertNotIn(removed_term, content)


if __name__ == "__main__":
    unittest.main()
