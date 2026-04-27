from __future__ import annotations

import ast
import json
from pathlib import Path
import re
import unittest


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
PLUGIN_ROOT = WORKSPACE_ROOT / "planning-team-kit"
PLANNING_DRAFTS_TEMPLATES_ROOT = PLUGIN_ROOT / "skills" / "planning-drafts" / "templates"
GENERATED_SUITE_FIXTURE_ROOT = PLUGIN_ROOT / "tests" / "fixtures" / "generated-core-suite"
PLATFORM_KEYWORDS = {"claude-plugin", "codex-plugin"}
CORE_TEMPLATE_NAMES = [
    "index",
    "planning-brief",
    "requirements",
    "behavior-spec",
]
RESERVED_TEMPLATE_NAMES = [
    "metrics-brief",
    "option-memo",
    "qa-scenario",
    "stakeholder-brief",
]
LEGACY_TEMPLATE_NAMES = [
    "planning-context",
    "brief",
    "prd",
    "user-stories",
    "feature-spec",
]
ALL_TEMPLATE_NAMES = CORE_TEMPLATE_NAMES + RESERVED_TEMPLATE_NAMES + LEGACY_TEMPLATE_NAMES
CORE_GENERATED_FILES = [
    "00-index.md",
    "01-planning-brief.md",
    "02-requirements.md",
    "03-behavior-spec.md",
]


def _parse_scalar(raw: str) -> object:
    value = raw.strip()
    if value == "true":
        return True
    if value == "false":
        return False
    if value in {"[]", "[ ]"}:
        return []
    if value in {"{}", "{ }"}:
        return {}
    if value and value[0] in {'"', "'"}:
        return ast.literal_eval(value)
    return value


def _parse_mapping(lines: list[str], start: int, indent: int) -> tuple[dict[str, object], int]:
    mapping: dict[str, object] = {}
    index = start

    while index < len(lines):
        line = lines[index]
        current_indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            index += 1
            continue
        if current_indent < indent:
            break
        if current_indent != indent:
            raise AssertionError(f"Unexpected indent in line: {line!r}")
        if stripped.startswith("- "):
            raise AssertionError(f"Unexpected list item at mapping level: {line!r}")

        key, separator, raw_value = stripped.partition(":")
        if not separator:
            raise AssertionError(f"Expected key/value pair: {line!r}")

        value = raw_value.lstrip()
        index += 1

        if value:
            mapping[key] = _parse_scalar(value)
            continue

        while index < len(lines) and not lines[index].strip():
            index += 1

        if index >= len(lines):
            mapping[key] = {}
            break

        next_line = lines[index]
        next_indent = len(next_line) - len(next_line.lstrip(" "))
        next_stripped = next_line.strip()

        if next_indent <= current_indent:
            mapping[key] = {}
            continue
        if next_stripped.startswith("- "):
            items: list[object] = []
            while index < len(lines):
                list_line = lines[index]
                list_indent = len(list_line) - len(list_line.lstrip(" "))
                list_stripped = list_line.strip()
                if not list_stripped:
                    index += 1
                    continue
                if list_indent != next_indent or not list_stripped.startswith("- "):
                    break
                items.append(_parse_scalar(list_stripped[2:]))
                index += 1
            mapping[key] = items
            continue

        nested, index = _parse_mapping(lines, index, next_indent)
        mapping[key] = nested

    return mapping, index


def parse_simple_yaml(text: str) -> dict[str, object]:
    parsed, index = _parse_mapping(text.splitlines(), 0, 0)
    if index < len(text.splitlines()):
        remaining = [line for line in text.splitlines()[index:] if line.strip()]
        if remaining:
            raise AssertionError(f"Unexpected trailing YAML lines: {remaining!r}")
    return parsed


def parse_front_matter(markdown: str) -> tuple[dict[str, object], str]:
    if not markdown.startswith("---\n"):
        raise AssertionError("Markdown file is missing front matter")

    _, front_matter, body = markdown.split("---\n", 2)
    return parse_simple_yaml(front_matter), body


def extract_headings(markdown_body: str) -> list[str]:
    return re.findall(r"^##\s+(.+)$", markdown_body, re.MULTILINE)


def extract_subheadings(markdown_body: str) -> list[str]:
    return re.findall(r"^###\s+(.+)$", markdown_body, re.MULTILINE)


class PlanningTeamKitStructureTests(unittest.TestCase):
    def test_manifests_are_dual_platform_and_synchronized(self) -> None:
        claude_manifest = json.loads(
            (PLUGIN_ROOT / ".claude-plugin" / "plugin.json").read_text()
        )
        codex_manifest = json.loads(
            (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text()
        )

        self.assertEqual(claude_manifest["name"], "planning-team-kit")
        self.assertEqual(codex_manifest["name"], "planning-team-kit")
        self.assertEqual(claude_manifest["version"], codex_manifest["version"])
        self.assertEqual(claude_manifest["description"], codex_manifest["description"])
        self.assertEqual(claude_manifest["skills"], "./skills/")
        self.assertEqual(codex_manifest["skills"], "./skills/")
        self.assertNotIn("interface", claude_manifest)
        self.assertIn("interface", codex_manifest)
        self.assertIn("defaultPrompt", codex_manifest["interface"])

    def test_required_skills_and_agent_metadata_exist(self) -> None:
        skill_names = [
            "help",
            "planning-intake",
            "planning-grill",
            "planning-drafts",
            "quality-review",
        ]

        for skill_name in skill_names:
            with self.subTest(skill=skill_name):
                skill_doc = PLUGIN_ROOT / "skills" / skill_name / "SKILL.md"
                agent_meta = PLUGIN_ROOT / "skills" / skill_name / "agents" / "openai.yaml"

                self.assertTrue(skill_doc.exists())
                self.assertTrue(agent_meta.exists())
                text = skill_doc.read_text()
                self.assertIn(f"/planning-team-kit:{skill_name}", text)
                self.assertIn(f"${skill_name}", text)
                self.assertIn("draft-only", text)

                agent_config = parse_simple_yaml(agent_meta.read_text())
                self.assertIn("interface", agent_config)
                self.assertIn("policy", agent_config)
                self.assertEqual(
                    agent_config["policy"]["allow_implicit_invocation"],
                    True,
                )

                interface = agent_config["interface"]
                for key in (
                    "display_name",
                    "short_description",
                    "brand_color",
                    "default_prompt",
                ):
                    self.assertIn(key, interface)
                    self.assertTrue(interface[key])

    def test_planning_coach_is_not_exposed_as_v0_1_skill(self) -> None:
        self.assertFalse((PLUGIN_ROOT / "skills" / "planning-coach").exists())

    def test_handoff_summary_is_not_exposed_as_v0_1_skill(self) -> None:
        self.assertFalse((PLUGIN_ROOT / "skills" / "handoff-summary").exists())

    def test_legacy_doc_suite_skill_name_is_not_exposed(self) -> None:
        legacy_name = "doc" + "-suite"
        legacy_codex_invocation = "$" + legacy_name
        legacy_claude_invocation = "planning-team-kit:" + legacy_name
        legacy_skill_path = "skills/" + legacy_name
        legacy_title = "Doc" + " Suite"

        self.assertFalse((PLUGIN_ROOT / "skills" / legacy_name).exists())

        public_files = [
            WORKSPACE_ROOT / "README.md",
            WORKSPACE_ROOT / "docs" / "diagrams" / "planning-team-kit-workflow.html",
            WORKSPACE_ROOT
            / "docs"
            / "superpowers"
            / "specs"
            / "2026-04-24-planning-team-kit-design.md",
            PLUGIN_ROOT / "README.md",
            PLUGIN_ROOT / "docs" / "examples.md",
            PLUGIN_ROOT / "docs" / "privacy-policy.md",
            PLUGIN_ROOT / "docs" / "terms-of-service.md",
            PLUGIN_ROOT / "skills" / "help" / "SKILL.md",
            PLUGIN_ROOT / "skills" / "planning-intake" / "SKILL.md",
            PLUGIN_ROOT / "skills" / "planning-grill" / "SKILL.md",
            PLUGIN_ROOT / "skills" / "planning-drafts" / "SKILL.md",
            PLUGIN_ROOT / "skills" / "planning-drafts" / "agents" / "openai.yaml",
        ]

        for public_file in public_files:
            with self.subTest(path=public_file):
                if not public_file.exists():
                    continue
                text = public_file.read_text()
                self.assertNotIn(legacy_name, text)
                self.assertNotIn(legacy_codex_invocation, text)
                self.assertNotIn(legacy_claude_invocation, text)
                self.assertNotIn(legacy_skill_path, text)
                self.assertNotIn(legacy_title, text)

    def test_handoff_summary_is_not_a_v0_1_document_contract(self) -> None:
        planning_drafts = (PLUGIN_ROOT / "skills" / "planning-drafts" / "SKILL.md").read_text()
        header_schema = json.loads(
            (PLUGIN_ROOT / "schemas" / "doc-header.schema.json").read_text()
        )
        section_map = parse_simple_yaml(
            (PLUGIN_ROOT / "schemas" / "section-map.yaml").read_text()
        )

        self.assertFalse((PLANNING_DRAFTS_TEMPLATES_ROOT / "handoff-summary.md").exists())
        self.assertNotIn("handoff-summary", planning_drafts)
        self.assertNotIn("handoff-summary", header_schema["properties"]["doc_type"]["enum"])
        self.assertNotIn("handoff-summary", section_map)

    def test_planning_intake_requires_iterative_clarification_until_ready(self) -> None:
        text = (PLUGIN_ROOT / "skills" / "planning-intake" / "SKILL.md").read_text()

        self.assertIn("## Clarification Loop", text)
        self.assertIn("Ask one question per turn", text)
        self.assertIn("as many turns as needed", text)
        self.assertIn("Required readiness criteria", text)
        self.assertIn("before recommending `planning-drafts`", text)
        self.assertIn("approval_state` to `needs_review`", text)

    def test_questioning_skills_prefer_interactive_choice_tools_with_fallback(self) -> None:
        skill_paths = (
            PLUGIN_ROOT / "skills" / "planning-intake" / "SKILL.md",
            PLUGIN_ROOT / "skills" / "planning-grill" / "SKILL.md",
            PLUGIN_ROOT / "skills" / "quality-review" / "SKILL.md",
        )

        for skill_path in skill_paths:
            with self.subTest(skill=skill_path):
                text = skill_path.read_text()
                self.assertIn("## Question Delivery", text)
                self.assertIn("request_user_input", text)
                self.assertIn("askUserQuestion", text)
                self.assertIn("plain Markdown", text)

    def test_planning_drafts_requires_readiness_check_before_generating_artifacts(self) -> None:
        text = (PLUGIN_ROOT / "skills" / "planning-drafts" / "SKILL.md").read_text()

        self.assertIn("## Readiness Check", text)
        self.assertIn("Do not generate draft artifacts", text)
        self.assertIn("route to `planning-intake`", text)
        self.assertNotIn("planning-coach", text)
        self.assertIn("approval_state: needs_review", text)

    def test_planning_grill_is_optional_and_one_question_at_a_time(self) -> None:
        text = (PLUGIN_ROOT / "skills" / "planning-grill" / "SKILL.md").read_text()

        self.assertIn("not a required workflow gate", text)
        self.assertIn("optional pre-draft or pre-handoff", text)
        self.assertIn("Ask one question at a time", text)
        self.assertIn("recommended answer", text)
        self.assertIn("If a question can be answered", text)
        self.assertIn("must not generate the standard draft suite", text)

    def test_planning_drafts_is_standard_only_for_now(self) -> None:
        text = (PLUGIN_ROOT / "skills" / "planning-drafts" / "SKILL.md").read_text()

        self.assertNotIn("--mode", text)
        self.assertNotIn("## Modes", text)
        self.assertNotIn("`lite`", text)
        self.assertNotIn("`full`", text)
        self.assertIn("## Standard Suite", text)
        self.assertIn("Always generate the core standard suite", text)

        for artifact_name in CORE_TEMPLATE_NAMES:
            self.assertIn(f"`{artifact_name}`", text)

        generated_artifacts = text.split("## Generated Artifact Types", 1)[1].split(
            "## Template Map",
            1,
        )[0]
        for artifact_name in CORE_TEMPLATE_NAMES:
            self.assertIn(f"`{artifact_name}`", generated_artifacts)
        for artifact_name in RESERVED_TEMPLATE_NAMES + LEGACY_TEMPLATE_NAMES:
            self.assertNotIn(f"`{artifact_name}`", generated_artifacts)
        self.assertNotIn("`qa-scenario`", generated_artifacts)
        self.assertNotIn("`handoff-summary`", generated_artifacts)
        self.assertNotIn("`engineering-brief`", generated_artifacts)

    def test_planning_drafts_always_saves_generated_standard_suite(self) -> None:
        text = (PLUGIN_ROOT / "skills" / "planning-drafts" / "SKILL.md").read_text()

        self.assertIn("## Local Draft Persistence", text)
        self.assertIn("Always save generated artifacts", text)
        self.assertIn("docs/planning/drafts/topic-slug--YYYY-MM-DD-HHMMSS/", text)
        self.assertIn("docs/planning/drafts/login-onboarding--2026-04-24-143205/", text)
        self.assertIn("Do not overwrite existing suite directories", text)
        self.assertIn("append `-2`, `-3`, or the next available numeric suffix", text)

        for relative_path in CORE_GENERATED_FILES:
            self.assertIn(relative_path, text)

        for removed_path in (
            "00-suite-index.md",
            "00-planning-context.md",
            "00-planning-context.yaml",
            "01-brief.md",
            "02-prd.md",
            "03-user-stories.md",
            "04-feature-spec.md",
            "03-metrics-brief.md",
            "05-metrics-brief.md",
            "04-engineering-brief.md",
            "03-qa-scenario.md",
            "05-handoff-summary.md",
        ):
            self.assertNotIn(removed_path, text)

    def test_codex_manifest_declares_write_capability_for_saved_drafts(self) -> None:
        codex_manifest = json.loads(
            (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text()
        )

        self.assertIn("Write", codex_manifest["interface"]["capabilities"])

    def test_quality_review_uses_multi_agent_review_contract(self) -> None:
        text = (PLUGIN_ROOT / "skills" / "quality-review" / "SKILL.md").read_text()

        for section_name in (
            "## Input Contract",
            "## Review Orchestration",
            "## Reviewer Agents",
            "## Gate Results",
            "## Quality Scores",
            "## Consolidation Rules",
            "## Fallback Mode",
        ):
            self.assertIn(section_name, text)

        for reviewer_name in (
            "Product Context Reviewer",
            "Story & Testability Reviewer",
            "Feature Behavior & Policy Reviewer",
            "Metrics & Evidence Reviewer",
            "Cross-Artifact Consistency Reviewer",
            "Handoff Governance Reviewer",
        ):
            self.assertIn(reviewer_name, text)

        for input_contract_term in (
            "`full standard suite`",
            "`partial suite`",
            "`single document`",
            "`00-index.md`",
            "`01-planning-brief.md`",
            "`02-requirements.md`",
            "`03-behavior-spec.md`",
        ):
            self.assertIn(input_contract_term, text)

        for gate_status in ("`pass`", "`warn`", "`fail`"):
            self.assertIn(gate_status, text)

        for response_field in (
            "`Input Type`",
            "`Documents Reviewed`",
            "`Documents Missing`",
            "`Gate Results`",
            "`Review Execution Mode`",
            "`Agent Review Summary`",
            "`Conflict Resolution`",
        ):
            self.assertIn(response_field, text)

        for verdict in ("`pass`", "`conditional pass`", "`needs revision`"):
            self.assertIn(verdict, text)

        for score_rule in (
            "`0`",
            "`1`",
            "`2`",
            "critical failure",
            "`needs revision`",
        ):
            self.assertIn(score_rule, text)

        for finding_field in (
            "`reviewer`",
            "`severity`",
            "`document`",
            "`location`",
            "`section`",
            "`evidence`",
            "`issue`",
            "`why it matters`",
            "`suggested fix`",
        ):
            self.assertIn(finding_field, text)

        for guardrail in (
            "API endpoint",
            "DB schema",
            "concrete query",
            "instrumentation event",
        ):
            self.assertIn(guardrail, text)

    def test_planning_drafts_owns_template_resources(self) -> None:
        text = (PLUGIN_ROOT / "skills" / "planning-drafts" / "SKILL.md").read_text()

        for template_name in ALL_TEMPLATE_NAMES:
            with self.subTest(template=template_name):
                template_path = PLANNING_DRAFTS_TEMPLATES_ROOT / f"{template_name}.md"
                self.assertTrue(template_path.exists())
                self.assertIn(
                    f"`{template_name}` -> `templates/{template_name}.md`",
                    text,
                )

    def test_templates_match_header_schema_and_section_map(self) -> None:
        header_schema = json.loads(
            (PLUGIN_ROOT / "schemas" / "doc-header.schema.json").read_text()
        )
        section_map = parse_simple_yaml(
            (PLUGIN_ROOT / "schemas" / "section-map.yaml").read_text()
        )
        expected_defaults = {
            "index": {"decision_required": True},
            "planning-brief": {"decision_required": True},
            "requirements": {"decision_required": True},
            "behavior-spec": {"decision_required": True},
            "planning-context": {"decision_required": True},
            "brief": {"decision_required": True},
            "option-memo": {"decision_required": True},
            "prd": {"decision_required": True},
            "user-stories": {"decision_required": True},
            "feature-spec": {"decision_required": True},
            "qa-scenario": {"decision_required": False},
            "metrics-brief": {"decision_required": True},
            "stakeholder-brief": {"decision_required": True},
        }
        expected_subheadings = {
            "option-memo": ["Option A", "Option B", "Option C"],
        }

        for template_name in ALL_TEMPLATE_NAMES:
            with self.subTest(template=template_name):
                template = PLANNING_DRAFTS_TEMPLATES_ROOT / f"{template_name}.md"
                header, body = parse_front_matter(template.read_text())

                self.assertEqual(header["doc_type"], template_name)

                for required_key in header_schema["required"]:
                    self.assertIn(required_key, header)

                for key, property_schema in header_schema["properties"].items():
                    if key not in header:
                        continue
                    if "enum" in property_schema:
                        self.assertIn(header[key], property_schema["enum"])

                self.assertIsInstance(header["title"], str)
                self.assertIsInstance(header["related_docs"], list)
                self.assertIsInstance(header["decision_required"], bool)
                self.assertEqual(header["last_updated"], "YYYY-MM-DD")
                self.assertEqual(header["mode"], "standard")
                self.assertEqual(header["status"], "draft")
                self.assertEqual(header["sensitivity"], "internal")
                self.assertEqual(header["approval_state"], "draft")
                self.assertIsInstance(header["source_of_truth"], str)
                self.assertEqual(
                    header["decision_required"],
                    expected_defaults[template_name]["decision_required"],
                )

                headings = extract_headings(body)
                self.assertEqual(headings, section_map[template_name]["required"])

                if template_name in expected_subheadings:
                    self.assertEqual(
                        extract_subheadings(body),
                        expected_subheadings[template_name],
                    )

                if template_name == "index":
                    self.assertIn("How to Read This Suite", body)
                    self.assertIn("01-planning-brief.md", body)
                    self.assertIn("02-requirements.md", body)
                    self.assertIn("03-behavior-spec.md", body)

                if template_name == "planning-brief":
                    self.assertIn("Current State", body)
                    self.assertIn("Failure Criteria", body)
                    self.assertIn("Options Considered", body)

                if template_name == "requirements":
                    self.assertIn("Requirement ID", body)
                    self.assertIn("Acceptance Criteria", body)
                    self.assertIn("Source", body)
                    self.assertIn("Assumption", body)

                if template_name == "behavior-spec":
                    self.assertIn("Requirement ID", body)
                    self.assertIn("Surface/Flow", body)
                    self.assertIn("State/Permission Rule", body)
                    self.assertIn("Failure Case", body)

                if template_name == "prd":
                    self.assertIn("- Must have:", body)
                    self.assertIn("- Should have:", body)
                    self.assertIn("- Could have:", body)
                    self.assertIn("- Out of scope:", body)
                    self.assertIn("story-level detail", body)
                    self.assertNotIn("acceptance criteria", body)

                if template_name == "user-stories":
                    self.assertIn("As a", body)
                    self.assertIn("Acceptance Criteria", body)
                    self.assertIn("Priority and Release Scope", body)

                if template_name == "feature-spec":
                    self.assertIn("State and Policy Rules", body)
                    self.assertIn("Validation Expectations", body)
                    self.assertNotIn("API endpoints", body)
                    self.assertNotIn("schemas", body)
                    self.assertNotIn("dashboard or query", body)

                if template_name == "metrics-brief":
                    self.assertIn("measurement source", body)
                    self.assertIn("observation window", body)
                    self.assertIn("decision rule", body)
                    self.assertNotIn("event name", body)
                    self.assertNotIn("trigger point", body)
                    self.assertNotIn("instrumentation owner", body)

                if template_name == "qa-scenario":
                    self.assertIn(
                        "Use `not run`, `pass`, `fail`, or `blocked`.",
                        body,
                    )

    def test_shared_quality_assets_exist(self) -> None:
        expected_files = [
            "schemas/doc-header.schema.json",
            "schemas/section-map.yaml",
            "snippets/decision-table.md",
            "snippets/risk-table.md",
            "snippets/source-assumption-confidence.md",
            "docs/style-guide.md",
            "docs/quality-rubric.md",
            "docs/examples.md",
            "docs/privacy-policy.md",
            "docs/terms-of-service.md",
        ]

        for relative_path in expected_files:
            with self.subTest(path=relative_path):
                self.assertTrue((PLUGIN_ROOT / relative_path).exists())

    def test_generated_core_suite_fixture_matches_contract(self) -> None:
        header_schema = json.loads(
            (PLUGIN_ROOT / "schemas" / "doc-header.schema.json").read_text()
        )
        section_map = parse_simple_yaml(
            (PLUGIN_ROOT / "schemas" / "section-map.yaml").read_text()
        )
        expected_doc_types = {
            "00-index.md": "index",
            "01-planning-brief.md": "planning-brief",
            "02-requirements.md": "requirements",
            "03-behavior-spec.md": "behavior-spec",
        }

        self.assertEqual(
            sorted(path.name for path in GENERATED_SUITE_FIXTURE_ROOT.glob("*.md")),
            CORE_GENERATED_FILES,
        )

        for file_name, doc_type in expected_doc_types.items():
            with self.subTest(file=file_name):
                header, body = parse_front_matter(
                    (GENERATED_SUITE_FIXTURE_ROOT / file_name).read_text()
                )
                self.assertEqual(header["doc_type"], doc_type)

                for required_key in header_schema["required"]:
                    self.assertIn(required_key, header)

                for key, property_schema in header_schema["properties"].items():
                    if key in header and "enum" in property_schema:
                        self.assertIn(header[key], property_schema["enum"])

                self.assertEqual(header["mode"], "standard")
                self.assertIn(header["approval_state"], {"draft", "needs_review"})
                self.assertEqual(extract_headings(body), section_map[doc_type]["required"])

        index_text = (GENERATED_SUITE_FIXTURE_ROOT / "00-index.md").read_text()
        for file_name in CORE_GENERATED_FILES[1:]:
            self.assertIn(f"]({file_name})", index_text)

    def test_plugin_is_registered_in_workspace_docs_and_marketplace(self) -> None:
        claude_manifest = json.loads(
            (PLUGIN_ROOT / ".claude-plugin" / "plugin.json").read_text()
        )
        codex_manifest = json.loads(
            (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text()
        )
        marketplace = json.loads(
            (WORKSPACE_ROOT / ".claude-plugin" / "marketplace.json").read_text()
        )
        codex_marketplace = json.loads(
            (WORKSPACE_ROOT / ".agents" / "plugins" / "marketplace.json").read_text()
        )
        plugin_entry = next(
            plugin
            for plugin in marketplace["plugins"]
            if plugin["name"] == "planning-team-kit"
        )
        codex_plugin_entry = next(
            plugin
            for plugin in codex_marketplace["plugins"]
            if plugin["name"] == "planning-team-kit"
        )

        self.assertEqual(plugin_entry["source"], "./planning-team-kit")
        self.assertEqual(plugin_entry["version"], claude_manifest["version"])
        self.assertEqual(plugin_entry["license"], claude_manifest["license"])
        self.assertEqual(plugin_entry["description"], claude_manifest["description"])
        self.assertEqual(plugin_entry["description"], codex_manifest["description"])

        claude_keywords = set(claude_manifest["keywords"]) - PLATFORM_KEYWORDS
        codex_keywords = set(codex_manifest["keywords"]) - PLATFORM_KEYWORDS
        self.assertTrue(set(plugin_entry["tags"]).issubset(claude_keywords))
        self.assertTrue(set(plugin_entry["tags"]).issubset(codex_keywords))

        self.assertEqual(codex_marketplace["name"], "inkwonjung-colosseum")
        self.assertEqual(
            codex_marketplace["interface"]["displayName"],
            "inkwonjung-colosseum plugins",
        )
        self.assertEqual(
            codex_plugin_entry["source"],
            {"source": "local", "path": "./planning-team-kit"},
        )
        self.assertEqual(
            codex_plugin_entry["policy"],
            {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        )
        self.assertEqual(
            codex_plugin_entry["category"],
            codex_manifest["interface"]["category"],
        )

        interface = codex_manifest["interface"]
        self.assertNotEqual(interface["privacyPolicyURL"], codex_manifest["repository"])
        self.assertNotEqual(interface["termsOfServiceURL"], codex_manifest["repository"])
        self.assertIn("privacy-policy.md", interface["privacyPolicyURL"])
        self.assertIn("terms-of-service.md", interface["termsOfServiceURL"])

        readme = (WORKSPACE_ROOT / "README.md").read_text()
        self.assertIn("planning-team-kit", readme)
        self.assertIn("기획 문서", readme)
        self.assertIn(".claude-plugin/marketplace.json", readme)
        self.assertIn(".agents/plugins/marketplace.json", readme)
        self.assertIn("├── snippets/", readme)
        self.assertIn("https://github.com/inkwonjung-colosseum/plugins", readme)
        self.assertIn(
            "claude plugin marketplace add https://github.com/inkwonjung-colosseum/plugins",
            readme,
        )
        self.assertIn(
            "codex marketplace add https://github.com/inkwonjung-colosseum/plugins",
            readme,
        )
        self.assertIn("claude plugin install planning-team-kit@inkwonjung-colosseum", readme)
        self.assertIn("claude plugin marketplace add", readme)
        self.assertNotIn("claude plugin add ./planning-team-kit", readme)
        self.assertNotIn("claude plugin marketplace add /absolute/path/to/colo-plugins", readme)
        self.assertNotIn("codex marketplace add /absolute/path/to/colo-plugins", readme)
        self.assertIn("Codex", readme)
        self.assertIn(".codex-plugin/plugin.json", readme)
        self.assertIn("policy.installation", readme)
        self.assertIn("policy.authentication", readme)

    def test_package_readme_exposes_start_here_and_full_workflow(self) -> None:
        readme = (PLUGIN_ROOT / "README.md").read_text()

        self.assertIn("## Start Here", readme)
        self.assertIn("/planning-team-kit:help", readme)
        self.assertIn("$help", readme)
        self.assertIn("00-index.md", readme)
        self.assertIn("01-planning-brief.md", readme)
        self.assertIn("02-requirements.md", readme)
        self.assertIn("03-behavior-spec.md", readme)
        self.assertNotIn("00-suite-index.md", readme)
        self.assertNotIn("00-planning-context.md", readme)
        self.assertNotIn("03-user-stories.md", readme)
        self.assertNotIn("04-feature-spec.md", readme)
        self.assertNotIn("05-metrics-brief.md", readme)
        self.assertNotIn("00-planning-context.yaml", readme)
        self.assertNotIn("03-metrics-brief.md", readme)
        self.assertNotIn("04-engineering-brief.md", readme)
        self.assertNotIn("03-qa-scenario.md", readme)
        self.assertNotIn("05-handoff-summary.md", readme)
        self.assertNotIn("/planning-team-kit:planning-coach", readme)
        self.assertNotIn("$planning-coach", readme)
        self.assertNotIn("/planning-team-kit:handoff-summary", readme)
        self.assertNotIn("$handoff-summary", readme)

    def test_package_readme_explains_multi_agent_quality_review(self) -> None:
        readme = (PLUGIN_ROOT / "README.md").read_text()
        help_text = (PLUGIN_ROOT / "skills" / "help" / "SKILL.md").read_text()

        self.assertIn("multi-agent review gate", readme)
        self.assertIn("Product Context Reviewer", readme)
        self.assertIn("Cross-Artifact Consistency Reviewer", readme)
        self.assertIn("Handoff Governance Reviewer", readme)
        self.assertIn("Product Context Reviewer", help_text)
        self.assertIn("Cross-Artifact Consistency Reviewer", help_text)
        self.assertIn("Handoff Governance Reviewer", help_text)

    def test_workflow_diagram_ends_at_quality_review(self) -> None:
        diagram = (WORKSPACE_ROOT / "docs" / "diagrams" / "planning-team-kit-workflow.html").read_text()

        self.assertIn("quality-review", diagram)
        self.assertIn("multi-agent review gate", diagram)
        self.assertNotIn("handoff-summary", diagram)
        self.assertNotIn("Handoff Summary", diagram)

    def test_header_schema_is_strict_enough_for_template_contract(self) -> None:
        header_schema = json.loads(
            (PLUGIN_ROOT / "schemas" / "doc-header.schema.json").read_text()
        )

        self.assertEqual(header_schema["additionalProperties"], False)
        self.assertEqual(
            header_schema["properties"]["last_updated"]["pattern"],
            r"^(YYYY-MM-DD|\d{4}-\d{2}-\d{2})$",
        )

        last_updated_pattern = re.compile(
            header_schema["properties"]["last_updated"]["pattern"]
        )
        self.assertTrue(last_updated_pattern.fullmatch("YYYY-MM-DD"))
        self.assertTrue(last_updated_pattern.fullmatch("2026-04-25"))
        self.assertFalse(last_updated_pattern.fullmatch(r"\d{4}-\d{2}-\d{2}"))


if __name__ == "__main__":
    unittest.main()
