"""
ai-utility-kit v0.1.0 structure tests.
"""

import json
import os
from pathlib import Path
import unittest


BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_ROOT = os.path.dirname(BASE)
SKILLS = os.path.join(BASE, "skills")
DOCS = os.path.join(BASE, "docs")
CLAUDE_PLUGIN = os.path.join(BASE, ".claude-plugin", "plugin.json")
CODEX_PLUGIN = os.path.join(BASE, ".codex-plugin", "plugin.json")
CLAUDE_MARKETPLACE = os.path.join(WORKSPACE_ROOT, ".claude-plugin", "marketplace.json")
CODEX_MARKETPLACE = os.path.join(WORKSPACE_ROOT, ".agents", "plugins", "marketplace.json")
ROOT_README = os.path.join(WORKSPACE_ROOT, "README.md")
PLUGIN_README = os.path.join(BASE, "README.md")


REQUIRED_SKILLS = [
    "ai-grill",
    "context-map",
    "meeting-brief",
    "term-clarifier",
]

PUBLIC_FILES = [
    ROOT_README,
    PLUGIN_README,
    CLAUDE_PLUGIN,
    CODEX_PLUGIN,
    CLAUDE_MARKETPLACE,
    CODEX_MARKETPLACE,
]

PACKAGED_TEXT_ROOTS = [
    os.path.join(BASE, "skills"),
    os.path.join(BASE, "docs"),
]


def packaged_text_files():
    files = [
        PLUGIN_README,
        CLAUDE_PLUGIN,
        CODEX_PLUGIN,
        CLAUDE_MARKETPLACE,
        CODEX_MARKETPLACE,
    ]
    for root in PACKAGED_TEXT_ROOTS:
        for path in Path(root).rglob("*"):
            if path.is_file() and path.suffix in {".md", ".json", ".yaml", ".yml"}:
                files.append(str(path))
    return sorted(set(files))


def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_json(path):
    return json.loads(read_text(path))


def skill_path(skill_name, *parts):
    return os.path.join(SKILLS, skill_name, *parts)


class TestManifests(unittest.TestCase):

    def test_manifest_files_exist(self):
        self.assertTrue(os.path.isfile(CLAUDE_PLUGIN))
        self.assertTrue(os.path.isfile(CODEX_PLUGIN))

    def test_manifest_identity_is_synced(self):
        claude = load_json(CLAUDE_PLUGIN)
        codex = load_json(CODEX_PLUGIN)
        self.assertEqual(claude["name"], "ai-utility-kit")
        self.assertEqual(codex["name"], "ai-utility-kit")
        self.assertEqual(claude["version"], "0.1.0")
        self.assertEqual(codex["version"], "0.1.0")
        self.assertEqual(claude["skills"], "./skills/")
        self.assertEqual(codex["skills"], "./skills/")

    def test_codex_interface_is_read_interactive_only(self):
        interface = load_json(CODEX_PLUGIN)["interface"]
        self.assertEqual(interface["category"], "Productivity")
        self.assertEqual(interface["capabilities"], ["Read", "Interactive"])
        self.assertIn("privacy-policy.md", interface["privacyPolicyURL"])
        self.assertIn("terms-of-service.md", interface["termsOfServiceURL"])
        self.assertGreaterEqual(len(interface["defaultPrompt"]), 4)


class TestSkills(unittest.TestCase):

    def test_required_skills_exist(self):
        for skill in REQUIRED_SKILLS:
            with self.subTest(skill=skill):
                self.assertTrue(os.path.isdir(skill_path(skill)))
                self.assertTrue(os.path.isfile(skill_path(skill, "SKILL.md")))

    def test_skill_frontmatter_matches_folder_name(self):
        for skill in REQUIRED_SKILLS:
            with self.subTest(skill=skill):
                content = read_text(skill_path(skill, "SKILL.md"))
                self.assertTrue(content.startswith("---\n"))
                self.assertIn(f"name: {skill}", content)
                self.assertIn("description:", content)
                self.assertIn("argument-hint:", content)

    def test_skills_are_korean_first_and_conversation_only(self):
        required_phrases = [
            "기본 출력은 한국어",
            "영어로 요청하면 영어",
            "파일을 생성하거나 수정하지 않습니다",
        ]
        for skill in REQUIRED_SKILLS:
            content = read_text(skill_path(skill, "SKILL.md"))
            for phrase in required_phrases:
                with self.subTest(skill=skill, phrase=phrase):
                    self.assertIn(phrase, content)


class TestPolicyDocs(unittest.TestCase):

    def test_policy_docs_exist(self):
        self.assertTrue(os.path.isfile(os.path.join(DOCS, "privacy-policy.md")))
        self.assertTrue(os.path.isfile(os.path.join(DOCS, "terms-of-service.md")))

    def test_policy_docs_describe_no_file_writes_or_external_calls(self):
        combined = "\n".join(
            read_text(os.path.join(DOCS, filename))
            for filename in ["privacy-policy.md", "terms-of-service.md"]
        )
        self.assertIn("does not create files", combined)
        self.assertIn("external services", combined)


class TestPublicDocsAndMarketplace(unittest.TestCase):

    def test_root_and_plugin_readmes_document_all_skills(self):
        for path in [ROOT_README, PLUGIN_README]:
            content = read_text(path)
            for skill in REQUIRED_SKILLS:
                with self.subTest(path=path, skill=skill):
                    self.assertIn(skill, content)

    def test_marketplaces_include_plugin(self):
        claude_plugins = load_json(CLAUDE_MARKETPLACE)["plugins"]
        codex_plugins = load_json(CODEX_MARKETPLACE)["plugins"]

        claude_entry = next((p for p in claude_plugins if p["name"] == "ai-utility-kit"), None)
        codex_entry = next((p for p in codex_plugins if p["name"] == "ai-utility-kit"), None)

        self.assertIsNotNone(claude_entry)
        self.assertEqual(claude_entry["source"], "./ai-utility-kit")
        self.assertEqual(claude_entry["version"], "0.1.0")

        self.assertIsNotNone(codex_entry)
        self.assertEqual(codex_entry["source"]["path"], "./ai-utility-kit")
        self.assertEqual(codex_entry["category"], "Productivity")

    def test_public_files_do_not_claim_company_specific_knowledge(self):
        forbidden_phrases = [
            "COLO-NOVA",
            "Colonova",
            "colosseum.atlassian.net",
            "콜로세움",
            "WMS 화면",
            "내부 정책",
        ]
        for path in packaged_text_files() + [ROOT_README]:
            content = read_text(path)
            for phrase in forbidden_phrases:
                with self.subTest(path=path, phrase=phrase):
                    self.assertNotIn(phrase, content)


if __name__ == "__main__":
    unittest.main()
