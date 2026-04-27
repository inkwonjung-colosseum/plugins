from __future__ import annotations

import json
from pathlib import Path
import re
import unittest


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
PLUGIN_ROOT = WORKSPACE_ROOT / "confluence-export-kit"
SUPPORTED_FEATURES_DOC = (
    PLUGIN_ROOT / "docs" / "confluence-markdown-exporter-supported-features.md"
)


class CurrentDocumentationStateTests(unittest.TestCase):
    def test_supported_features_plugin_version_matches_manifests(self) -> None:
        claude_manifest = json.loads((PLUGIN_ROOT / ".claude-plugin" / "plugin.json").read_text())
        codex_manifest = json.loads((PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text())
        self.assertEqual(claude_manifest["version"], codex_manifest["version"])

        doc = SUPPORTED_FEATURES_DOC.read_text()
        expected = f"로컬 래퍼 플러그인 버전: `confluence-export-kit {claude_manifest['version']}`"
        self.assertIn(expected, doc)

    def test_supported_features_local_evidence_paths_exist(self) -> None:
        doc = SUPPORTED_FEATURES_DOC.read_text()
        local_refs = re.findall(r"- `((?:confluence-export-kit)/[^`]+)`", doc)
        self.assertGreater(local_refs, [])

        for ref in local_refs:
            with self.subTest(ref=ref):
                self.assertTrue((WORKSPACE_ROOT / ref).exists())

    def test_readme_scope_mentions_single_and_multiple_page_export(self) -> None:
        readme = (PLUGIN_ROOT / "README.md").read_text()
        self.assertIn("page 단건/다건 export", readme)
        self.assertIn("local export-index", readme)
        self.assertIn("--skip-jira", readme)
        self.assertIn("현재 helper의 기본 output path는", readme)

    def test_set_config_documents_config_path_override(self) -> None:
        skill_doc = (PLUGIN_ROOT / "skills" / "set-config" / "SKILL.md").read_text()
        self.assertIn("--config-path", skill_doc)
        self.assertNotIn("--skip-validate", skill_doc)

    def test_index_export_documents_agent_file_override(self) -> None:
        skill_doc = (PLUGIN_ROOT / "skills" / "index-export" / "SKILL.md").read_text()
        supported_features_doc = SUPPORTED_FEATURES_DOC.read_text()

        self.assertIn("--agent-files <file> ...", skill_doc)
        self.assertIn("--agent-files <file> ...", supported_features_doc)

    def test_export_docs_explain_current_flag_defaults(self) -> None:
        supported_features_doc = SUPPORTED_FEATURES_DOC.read_text()

        self.assertIn("--no-skip-unchanged", supported_features_doc)
        self.assertIn("--no-cleanup-stale", supported_features_doc)
        self.assertIn("no-override 기본값은 `confluence`", supported_features_doc)

    def test_agent_metadata_reflects_plural_export_support(self) -> None:
        export_space = (
            PLUGIN_ROOT / "skills" / "export-space" / "agents" / "openai.yaml"
        ).read_text()
        export_org = (
            PLUGIN_ROOT / "skills" / "export-org" / "agents" / "openai.yaml"
        ).read_text()
        export_page = (
            PLUGIN_ROOT / "skills" / "export-page" / "agents" / "openai.yaml"
        ).read_text()
        export_page_with_descendant = (
            PLUGIN_ROOT
            / "skills"
            / "export-page-with-descendant"
            / "agents"
            / "openai.yaml"
        ).read_text()
        codex_manifest = (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text()

        self.assertIn("one or more Confluence spaces", export_space)
        self.assertIn("one or more Confluence instances", export_org)
        self.assertIn("<page-url> [<page-url> ...]", export_page_with_descendant)
        self.assertNotIn("<page-url-1> <page-url-2>", export_page)
        self.assertNotIn("<page-url> and <page-url>", codex_manifest)

    def test_executable_skills_do_not_document_preflight_runner(self) -> None:
        executable_skills = [
            "export-org",
            "export-page",
            "export-page-with-descendant",
            "export-space",
            "index-export",
            "set-config",
            "show-config",
        ]

        for skill_name in executable_skills:
            with self.subTest(skill=skill_name):
                skill_doc = (PLUGIN_ROOT / "skills" / skill_name / "SKILL.md").read_text()
                self.assertNotIn("PYTHON_BIN", skill_doc)
                self.assertNotIn("Python 3.10+", skill_doc)
                self.assertNotIn("Get-Command", skill_doc)
                self.assertNotIn("$env:CLAUDE_SKILL_DIR", skill_doc)


if __name__ == "__main__":
    unittest.main()
