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
        self.assertIn("확인 일자: 2026-04-27", doc)
        self.assertIn(
            "upstream 패키지 최신 확인 버전: `confluence-markdown-exporter 4.1.1`",
            doc,
        )

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
        self.assertNotIn("--skip-jira", readme)
        self.assertIn("export.output_path=./confluence", readme)
        self.assertIn("고정 output path를 강제", readme)
        self.assertIn("CME_EXPORT__OUTPUT_PATH=./confluence", readme)

    def test_set_config_documents_current_input_surface(self) -> None:
        skill_doc = (PLUGIN_ROOT / "skills" / "set-config" / "SKILL.md").read_text()
        self.assertIn("export.skip_unchanged", skill_doc)
        self.assertIn("export.cleanup_stale", skill_doc)
        self.assertIn("export.enable_jira_enrichment", skill_doc)
        self.assertIn("export.include_document_title", skill_doc)
        self.assertIn("export.page_breadcrumbs", skill_doc)
        self.assertNotIn("--output-path", skill_doc)
        self.assertNotIn("--config-path", skill_doc)
        self.assertNotIn("--skip-jira", skill_doc)
        self.assertNotIn("--skip-validate", skill_doc)

    def test_index_export_documents_agent_file_override(self) -> None:
        skill_doc = (PLUGIN_ROOT / "skills" / "index-export" / "SKILL.md").read_text()
        agent_doc = (
            PLUGIN_ROOT / "skills" / "index-export" / "agents" / "openai.yaml"
        ).read_text()
        supported_features_doc = SUPPORTED_FEATURES_DOC.read_text()
        readme = (PLUGIN_ROOT / "README.md").read_text()

        self.assertIn("--agent-files <file> ...", skill_doc)
        self.assertIn("--agent-files <file> ...", supported_features_doc)
        self.assertIn("user-invocable: false", skill_doc)
        self.assertIn("allow_implicit_invocation: false", agent_doc)
        self.assertIn("user-invocable: false", readme)
        self.assertIn("user-invocable: false", supported_features_doc)
        self.assertIn("Codex에는 Claude의 `user-invocable: false`", supported_features_doc)
        self.assertIn("allow_implicit_invocation=false", supported_features_doc)
        self.assertNotIn("$index-export", readme)

    def test_index_export_documents_metadata_and_append_log_behavior(self) -> None:
        skill_doc = (PLUGIN_ROOT / "skills" / "index-export" / "SKILL.md").read_text()
        supported_features_doc = SUPPORTED_FEATURES_DOC.read_text()
        readme = (PLUGIN_ROOT / "README.md").read_text()

        for doc in [skill_doc, supported_features_doc, readme]:
            with self.subTest():
                doc_lower = doc.lower()
                self.assertIn("scalar front matter", doc)
                self.assertIn("append", doc_lower)
                self.assertIn("log.md", doc)

    def test_export_docs_explain_current_flag_defaults(self) -> None:
        supported_features_doc = SUPPORTED_FEATURES_DOC.read_text()

        self.assertNotIn("--no-skip-unchanged", supported_features_doc)
        self.assertNotIn("--cleanup-stale", supported_features_doc)
        self.assertNotIn("--no-cleanup-stale", supported_features_doc)
        self.assertNotIn("--jira-enrichment", supported_features_doc)
        self.assertIn("export.skip_unchanged=true", supported_features_doc)
        self.assertIn("export.cleanup_stale=true", supported_features_doc)
        self.assertIn("export.enable_jira_enrichment=false", supported_features_doc)
        self.assertIn("output path override는 미노출", supported_features_doc)
        self.assertIn("export.page_properties_as_front_matter", supported_features_doc)
        self.assertIn("relative`, `absolute`, 또는 `wiki`", supported_features_doc)

    def test_export_docs_do_not_expose_output_path_overrides(self) -> None:
        readme = (PLUGIN_ROOT / "README.md").read_text()
        supported_features_doc = SUPPORTED_FEATURES_DOC.read_text()
        export_docs = [
            (PLUGIN_ROOT / "skills" / skill_name / "SKILL.md").read_text()
            for skill_name in [
                "export-org",
                "export-page",
                "export-page-with-descendant",
                "export-space",
            ]
        ]

        for doc in [readme, supported_features_doc, *export_docs]:
            with self.subTest():
                self.assertNotIn("[output-path]", doc)
                self.assertNotIn("<output-path>", doc)
                self.assertNotIn("--output-path", doc)
                self.assertIn("CME_EXPORT__OUTPUT_PATH=./confluence", doc)

    def test_help_skill_is_not_exposed(self) -> None:
        self.assertFalse((PLUGIN_ROOT / "skills" / "help").exists())

        readme = (PLUGIN_ROOT / "README.md").read_text()
        supported_features_doc = SUPPORTED_FEATURES_DOC.read_text()
        root_readme = (WORKSPACE_ROOT / "README.md").read_text()

        self.assertNotIn("skills/help", readme)
        self.assertNotIn("/confluence-export-kit:help", supported_features_doc)
        confluence_row = next(
            line
            for line in root_readme.splitlines()
            if line.startswith("| `confluence-export-kit` |")
        )
        self.assertNotIn("`help`", confluence_row)

    def test_workflow_diagram_reflects_fixed_export_defaults(self) -> None:
        diagram = (WORKSPACE_ROOT / "docs" / "diagrams" / "confluence-export-kit-workflow.html").read_text()

        self.assertIn("fixed export defaults", diagram)
        self.assertIn("uses set-config defaults", diagram)
        self.assertIn("7 skills · no help command", diagram)
        self.assertIn("targets passed through; cme validates", diagram)
        self.assertIn("index-export + AGENTS/CLAUDE rules", diagram)
        self.assertNotIn("skip / cleanup / workers", diagram)
        self.assertNotIn("no title/breadcrumb", diagram)

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
