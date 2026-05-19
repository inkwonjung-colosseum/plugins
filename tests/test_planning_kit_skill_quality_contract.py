import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "planning-kit"
DOCS_PLANNING_FORMAT = ROOT / "docs" / "planning-kit" / "skill-resources" / "planning-format"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def markdown_table_widths(text: str):
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|") and "---" not in stripped:
            yield stripped.count("|") - 1


class SkillQualityContractTest(unittest.TestCase):
    def test_skill_resources_are_packaged_inside_plugin_root(self):
        required = [
            PLUGIN / "skills" / "planning-format" / "references" / "runtime-contract.md",
            PLUGIN / "skills" / "planning-format" / "references" / "output-contract.md",
            PLUGIN / "skills" / "planning-format" / "references" / "connector-routing.md",
            PLUGIN / "skills" / "planning-format" / "references" / "conversion-rules.md",
            PLUGIN / "skills" / "planning-format" / "references" / "exclusion-rules.md",
            PLUGIN / "skills" / "planning-format" / "references" / "self-review-rules.md",
            PLUGIN / "skills" / "planning-format" / "templates" / "정책서.md",
            PLUGIN / "skills" / "planning-format" / "templates" / "기능설계서.md",
            PLUGIN / "skills" / "planning-review" / "references" / "runtime-contract.md",
            PLUGIN / "skills" / "planning-review" / "references" / "ssot-rules.md",
            PLUGIN / "skills" / "planning-review" / "references" / "ac-rules.md",
            PLUGIN / "skills" / "planning-review" / "references" / "deps-rules.md",
            PLUGIN / "skills" / "planning-publish-confluence" / "references" / "runtime-contract.md",
            PLUGIN / "skills" / "planning-publish-confluence" / "references" / "context-gate.md",
            PLUGIN / "skills" / "planning-publish-confluence" / "references" / "confluence-page-contract.md",
            PLUGIN / "skills" / "ssot-audit" / "references" / "runtime-contract.md",
            PLUGIN / "skills" / "ssot-audit" / "references" / "structure-rules.md",
            PLUGIN / "skills" / "ssot-audit" / "references" / "content-rules.md",
        ]

        for path in required:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), path)
                if path.is_symlink():
                    self.assertTrue(path.resolve().exists(), path)
                self.assertGreater(len(read(path)), 200)

    def test_planning_format_resources_are_packaged_and_synced_with_docs(self):
        skill_root = PLUGIN / "skills" / "planning-format"

        for dirname in ["references", "templates"]:
            with self.subTest(dirname=dirname):
                skill_dir = skill_root / dirname
                docs_dir = DOCS_PLANNING_FORMAT / dirname
                self.assertTrue(skill_dir.is_dir(), skill_dir)
                self.assertFalse(skill_dir.is_symlink(), skill_dir)

                skill_files = sorted(path.name for path in skill_dir.glob("*.md"))
                docs_files = sorted(path.name for path in docs_dir.glob("*.md"))
                self.assertEqual(skill_files, docs_files)

                for name in skill_files:
                    self.assertEqual(read(skill_dir / name), read(docs_dir / name), name)

    def test_planning_format_templates_prefer_field_lists_over_wide_tables(self):
        templates = [
            PLUGIN / "skills" / "planning-format" / "templates" / "정책서.md",
            PLUGIN / "skills" / "planning-format" / "templates" / "기능설계서.md",
        ]

        for path in templates:
            with self.subTest(path=path):
                text = read(path)
                self.assertNotIn("|  화면 / 영역", text)
                self.assertNotIn("|  현재 상태", text)
                self.assertNotIn("|  예외 상황", text)
                self.assertIn("작성 원칙", text)
                self.assertIn("관련", text)
                self.assertGreaterEqual(text.count("### "), 4)
                self.assertGreaterEqual(text.count("- "), 20)
                for width in markdown_table_widths(text):
                    self.assertLessEqual(width, 4, path)

    def test_public_skill_files_keep_operational_boundaries_visible(self):
        planning_format = read(PLUGIN / "skills" / "planning-format" / "SKILL.md")
        planning_review = read(PLUGIN / "skills" / "planning-review" / "SKILL.md")
        publish = read(PLUGIN / "skills" / "planning-publish-confluence" / "SKILL.md")
        ssot = read(PLUGIN / "skills" / "ssot-audit" / "SKILL.md")

        self.assertIn("default/no-op alias", planning_format)
        self.assertIn("## 저장 파일", planning_format)

        self.assertIn("one consolidated pass", planning_review)
        self.assertIn("not a public option", planning_review)
        self.assertNotIn("`--axes`", planning_review)

        self.assertIn("Forbidden inputs stop before", publish)
        self.assertIn("ask final confirmation", publish)
        self.assertIn("readback", publish)

        self.assertIn("Never fall back to all project Markdown", ssot)
        self.assertIn("exclusion summary and backlog", ssot)

    def test_review_public_docs_do_not_advertise_axes_option(self):
        readme = read(PLUGIN / "README.md")
        review_skill = read(PLUGIN / "skills" / "planning-review" / "SKILL.md")
        review_runtime = read(PLUGIN / "skills" / "planning-review" / "references" / "runtime-contract.md")

        self.assertNotIn("planning-review --axes", readme)
        self.assertNotIn("[--axes", review_skill)
        self.assertNotIn("[--axes", review_runtime)
        self.assertIn("축 단위 부분 리뷰 옵션은 공개 계약이 아니다", review_runtime)

    def test_manifests_are_descriptive_enough_for_routing(self):
        codex = json.loads(read(PLUGIN / ".codex-plugin" / "plugin.json"))
        claude = json.loads(read(PLUGIN / ".claude-plugin" / "plugin.json"))

        for manifest in [codex, claude]:
            self.assertIn("planning-format", manifest["description"])
            self.assertIn("planning-review", manifest["description"])
            self.assertIn("ssot-audit", manifest["description"])
            self.assertIn("planning-publish-confluence", manifest["description"])
            self.assertGreater(len(manifest["description"]), 60)

        interface = codex["interface"]
        self.assertIn("planning-review", interface["longDescription"])
        self.assertIn("readback", interface["longDescription"])
        self.assertEqual(len(interface["defaultPrompt"]), 3)


if __name__ == "__main__":
    unittest.main()
