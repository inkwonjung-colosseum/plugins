"""
planning-team-kit v0.3.0 구조 테스트
"""

import json
import os
import unittest

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_ROOT = os.path.dirname(BASE)
SKILLS = os.path.join(BASE, "skills")
SCHEMAS = os.path.join(BASE, "schemas")
DOCS = os.path.join(BASE, "docs")
CLAUDE_PLUGIN = os.path.join(BASE, ".claude-plugin", "plugin.json")
CODEX_PLUGIN = os.path.join(BASE, ".codex-plugin", "plugin.json")
PUBLIC_DOCS = [
    os.path.join(BASE, "README.md"),
    os.path.join(WORKSPACE_ROOT, "README.md"),
]


# ---------------------------------------------------------------------------
# 헬퍼
# ---------------------------------------------------------------------------

def skill_path(skill_name, *parts):
    return os.path.join(SKILLS, skill_name, *parts)


def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_json(path):
    return json.loads(read_text(path))


# ---------------------------------------------------------------------------
# 스킬 존재
# ---------------------------------------------------------------------------

class TestSkillsExist(unittest.TestCase):

    REQUIRED_SKILLS = ["plan-draft", "plan-review", "plan-publish"]

    def test_required_skills_exist(self):
        for skill in self.REQUIRED_SKILLS:
            with self.subTest(skill=skill):
                self.assertTrue(
                    os.path.isdir(skill_path(skill)),
                    f"skills/{skill}/ 디렉토리 없음",
                )

    def test_each_skill_has_skill_md(self):
        for skill in self.REQUIRED_SKILLS:
            with self.subTest(skill=skill):
                p = skill_path(skill, "SKILL.md")
                self.assertTrue(os.path.isfile(p), f"{p} 없음")

    def test_each_skill_has_openai_yaml(self):
        for skill in self.REQUIRED_SKILLS:
            with self.subTest(skill=skill):
                p = skill_path(skill, "agents", "openai.yaml")
                self.assertTrue(os.path.isfile(p), f"{p} 없음")

    def test_each_skill_has_frontmatter_metadata(self):
        for skill in self.REQUIRED_SKILLS:
            with self.subTest(skill=skill):
                content = read_text(skill_path(skill, "SKILL.md"))
                self.assertTrue(content.startswith("---\n"), f"{skill} frontmatter 없음")
                self.assertIn(f"name: {skill}", content)
                self.assertIn("description:", content)


# ---------------------------------------------------------------------------
# 구버전 스킬 노출 안 됨
# ---------------------------------------------------------------------------

class TestOldSkillsRemoved(unittest.TestCase):

    OLD_SKILLS = [
        "plan",
        "planning-start",
        "planning-check",
        "planning-draft",
        "planning-review",
        "confluence-update-plan",
    ]

    def test_old_skill_dirs_removed(self):
        for skill in self.OLD_SKILLS:
            with self.subTest(skill=skill):
                self.assertFalse(
                    os.path.isdir(skill_path(skill)),
                    f"구버전 skills/{skill}/ 아직 존재함",
                )

    LEGACY_PUBLIC_PHRASES = OLD_SKILLS[1:] + [
        "v0.2.1",
        "draft-only",
    ]

    def test_old_skill_names_not_in_public_docs(self):
        for doc in PUBLIC_DOCS:
            content = read_text(doc)
            for phrase in self.LEGACY_PUBLIC_PHRASES:
                with self.subTest(doc=doc, phrase=phrase):
                    self.assertNotIn(
                        phrase,
                        content,
                        f"{doc}에 구버전 표현 '{phrase}' 노출됨",
                    )

    def test_plain_plan_command_not_in_public_docs(self):
        forbidden_commands = [
            "/planning-team-kit:plan ",
            "/planning-team-kit:plan\n",
            "$plan ",
            "$plan\n",
        ]
        for doc in PUBLIC_DOCS:
            content = read_text(doc)
            for command in forbidden_commands:
                with self.subTest(doc=doc, command=command):
                    self.assertNotIn(command, content)

    def test_current_plan_draft_command_is_documented(self):
        workspace_readme = read_text(os.path.join(WORKSPACE_ROOT, "README.md"))
        package_readme = read_text(os.path.join(BASE, "README.md"))
        for content in [workspace_readme, package_readme]:
            with self.subTest():
                self.assertIn("/planning-team-kit:plan-draft", content)
                self.assertIn("$plan-draft", content)

    def test_public_docs_do_not_hardcode_workspace_confluence_values(self):
        public_paths = [
            os.path.join(BASE, "README.md"),
            os.path.join(BASE, ".codex-plugin", "plugin.json"),
            os.path.join(BASE, "docs", "examples.md"),
            skill_path("plan-draft", "SKILL.md"),
            skill_path("plan-draft", "agents", "openai.yaml"),
            skill_path("plan-publish", "SKILL.md"),
            skill_path("plan-publish", "references", "publish-runbook.md"),
        ]
        forbidden_phrases = [
            "OMS",
            "WMS",
            "Platform Admin",
            "Colonova Product",
            "Product Team Space",
            "Product Department",
            "colosseum.atlassian.net",
            "PROD",
            'spaceId: "PROD"',
        ]

        for path in public_paths:
            content = read_text(path)
            for phrase in forbidden_phrases:
                with self.subTest(path=path, phrase=phrase):
                    self.assertNotIn(phrase, content)


# ---------------------------------------------------------------------------
# 매니페스트 동기화
# ---------------------------------------------------------------------------

class TestManifests(unittest.TestCase):

    def _claude(self):
        return load_json(CLAUDE_PLUGIN)

    def _codex(self):
        return load_json(CODEX_PLUGIN)

    def test_version_is_0_3_0(self):
        self.assertEqual(self._claude()["version"], "0.3.0")
        self.assertEqual(self._codex()["version"], "0.3.0")

    def test_name_synced(self):
        self.assertEqual(self._claude()["name"], self._codex()["name"])

    def test_version_synced(self):
        self.assertEqual(self._claude()["version"], self._codex()["version"])

    def test_skills_path_set(self):
        self.assertEqual(self._claude()["skills"], "./skills/")
        self.assertEqual(self._codex()["skills"], "./skills/")

    def test_codex_has_default_prompts(self):
        prompts = self._codex()["interface"]["defaultPrompt"]
        self.assertIsInstance(prompts, list)
        self.assertGreaterEqual(len(prompts), 1)

    def test_codex_links_policy_docs(self):
        interface = self._codex()["interface"]
        self.assertIn("privacy-policy.md", interface["privacyPolicyURL"])
        self.assertIn("terms-of-service.md", interface["termsOfServiceURL"])


# ---------------------------------------------------------------------------
# 템플릿
# ---------------------------------------------------------------------------

class TestTemplates(unittest.TestCase):

    REQUIRED_TEMPLATES = ["상위설계서.md", "기능설계서.md", "정책서.md"]

    def test_templates_exist(self):
        for tmpl in self.REQUIRED_TEMPLATES:
            with self.subTest(template=tmpl):
                p = skill_path("plan-draft", "templates", tmpl)
                self.assertTrue(os.path.isfile(p), f"템플릿 {p} 없음")

    def test_templates_not_empty(self):
        for tmpl in self.REQUIRED_TEMPLATES:
            with self.subTest(template=tmpl):
                p = skill_path("plan-draft", "templates", tmpl)
                content = read_text(p)
                self.assertGreater(len(content.strip()), 100, f"템플릿 {tmpl} 내용 너무 짧음")

    def test_상위설계서_has_required_sections(self):
        content = read_text(skill_path("plan-draft", "templates", "상위설계서.md"))
        for section in ["배경 및 문제", "목표", "비목표", "핵심 요구사항", "제약사항 및 가정", "관련 문서"]:
            self.assertIn(section, content, f"상위설계서 템플릿에 '{section}' 없음")

    def test_기능설계서_has_required_sections(self):
        content = read_text(skill_path("plan-draft", "templates", "기능설계서.md"))
        for section in ["기능 설명", "전체 흐름", "권한 정책", "기능 상세 설계", "예외 처리", "QA 체크리스트"]:
            self.assertIn(section, content, f"기능설계서 템플릿에 '{section}' 없음")

    def test_정책서_has_required_sections(self):
        content = read_text(skill_path("plan-draft", "templates", "정책서.md"))
        for section in ["정책 개요", "적용 범위", "정책 규칙", "예외 케이스", "상태 전이", "미결 사항"]:
            self.assertIn(section, content, f"정책서 템플릿에 '{section}' 없음")


# ---------------------------------------------------------------------------
# schemas
# ---------------------------------------------------------------------------

class TestSchemas(unittest.TestCase):

    def test_doc_types_yaml_exists(self):
        p = os.path.join(SCHEMAS, "doc-types.yaml")
        self.assertTrue(os.path.isfile(p))

    def test_doc_types_has_three_types(self):
        content = read_text(os.path.join(SCHEMAS, "doc-types.yaml"))
        for doc_type in ["상위설계서", "기능설계서", "정책서"]:
            self.assertIn(doc_type, content, f"doc-types.yaml에 '{doc_type}' 없음")

    def test_doc_types_uses_plan_draft_templates(self):
        content = read_text(os.path.join(SCHEMAS, "doc-types.yaml"))
        self.assertIn("skills/plan-draft/templates/", content)
        self.assertNotIn("skills/plan/templates/", content)

    def test_old_schemas_removed(self):
        self.assertFalse(
            os.path.isfile(os.path.join(SCHEMAS, "doc-header.schema.json")),
            "구버전 doc-header.schema.json 아직 존재함",
        )
        self.assertFalse(
            os.path.isfile(os.path.join(SCHEMAS, "section-map.yaml")),
            "구버전 section-map.yaml 아직 존재함",
        )


# ---------------------------------------------------------------------------
# docs
# ---------------------------------------------------------------------------

class TestDocs(unittest.TestCase):

    REQUIRED_DOCS = [
        "examples.md",
        "privacy-policy.md",
        "quality-rubric.md",
        "style-guide.md",
        "terms-of-service.md",
    ]

    def test_required_docs_exist(self):
        for doc in self.REQUIRED_DOCS:
            with self.subTest(doc=doc):
                self.assertTrue(os.path.isfile(os.path.join(DOCS, doc)))

    def test_docs_reflect_v0_3_publish_gate(self):
        for doc in ["examples.md", "quality-rubric.md", "style-guide.md", "terms-of-service.md"]:
            with self.subTest(doc=doc):
                content = read_text(os.path.join(DOCS, doc))
                self.assertIn("plan", content)
                self.assertIn("publish", content.lower())
        quality = read_text(os.path.join(DOCS, "quality-rubric.md"))
        self.assertIn("[미정]", quality)
        self.assertIn("[가정]", quality)
        self.assertIn("Publish Gate", quality)


# ---------------------------------------------------------------------------
# plan-publish SKILL.md 핵심 내용 검증
# ---------------------------------------------------------------------------

class TestPlanPublishSkill(unittest.TestCase):

    def _content(self):
        return read_text(skill_path("plan-publish", "SKILL.md"))

    def test_stale_check_documented(self):
        self.assertIn("stale", self._content().lower(), "plan-publish SKILL.md에 stale 체크 없음")

    def test_lock_json_path_documented(self):
        self.assertIn("confluence-lock.json", self._content())

    def test_mcp_tool_discovery_documented(self):
        content = self._content()
        self.assertNotIn("mcp__", content, "plan-publish SKILL.md에 고정 MCP 서버 ID가 남아 있음")
        self.assertIn("MCP tool discovery", content)

    def test_create_page_documented(self):
        self.assertIn("createConfluencePage", self._content())

    def test_update_page_documented(self):
        self.assertIn("updateConfluencePage", self._content())

    def test_user_confirmation_required(self):
        self.assertIn("yes", self._content(), "plan-publish SKILL.md에 사용자 확인 절차 없음")

    def test_direct_local_sync_not_documented(self):
        content = self._content()
        forbidden = [
            "로컬 파일 동기화",
            "로컬 마크다운 파일 생성",
            "기존 로컬 파일 내용 업데이트",
            "confluence-lock.json 업데이트",
        ]
        for phrase in forbidden:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, content)

    def test_parent_lookup_documented(self):
        content = self._content()
        for phrase in ["parent 후보", "중복", "없음", "page_id 또는 URL"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_review_gate_documented(self):
        content = self._content()
        for phrase in ["Review gate", "[미정]", "[가정]", "충돌 경고", "review 없이 publish 진행"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_schema_aware_mcp_mapping_documented(self):
        content = self._content()
        self.assertIn("references/publish-runbook.md", content)
        self.assertNotIn("spaceKey", content)
        self.assertNotIn("version: N+1", content)


# ---------------------------------------------------------------------------
# plan-draft SKILL.md 핵심 내용 검증
# ---------------------------------------------------------------------------

class TestPlanDraftSkill(unittest.TestCase):

    def _content(self):
        return read_text(skill_path("plan-draft", "SKILL.md"))

    def test_question_loop_documented(self):
        self.assertIn("질문", self._content())

    def test_assumption_tag_documented(self):
        self.assertIn("[가정]", self._content())

    def test_diff_output_documented(self):
        content = self._content()
        self.assertTrue(
            "[기존]" in content or "diff" in content.lower(),
            "plan-draft SKILL.md에 diff/변경 출력 형식 없음",
        )

    def test_publish_gate_output_documented(self):
        content = self._content()
        self.assertIn("Publish gate", content)
        self.assertIn("review-required", content)

    def test_doc_type_detection_documented(self):
        content = self._content()
        for doc_type in ["상위설계서", "기능설계서", "정책서"]:
            self.assertIn(doc_type, content, f"plan-draft SKILL.md에 문서 타입 '{doc_type}' 판별 없음")

    def test_no_question_limit_implied(self):
        content = self._content()
        self.assertNotIn("최대 3번", content, "질문 제한 있음")
        self.assertNotIn("최대 5번", content, "질문 제한 있음")

    def test_retrieval_reference_documented(self):
        content = self._content()
        self.assertIn("references/confluence-retrieval.md", content)


# ---------------------------------------------------------------------------
# plan-review SKILL.md 핵심 내용 검증
# ---------------------------------------------------------------------------

class TestPlanReviewSkill(unittest.TestCase):

    def _content(self):
        return read_text(skill_path("plan-review", "SKILL.md"))

    def test_three_perspectives_documented(self):
        content = self._content()
        for perspective in ["근거", "범위", "실행"]:
            self.assertIn(perspective, content, f"plan-review SKILL.md에 관점 '{perspective}' 없음")

    def test_optional_documented(self):
        self.assertIn("선택", self._content(), "plan-review가 선택 스킬임이 명시되지 않음")

    def test_pass_verdict_documented(self):
        self.assertIn("pass", self._content().lower())

    def test_conditional_pass_documented(self):
        self.assertIn("conditional pass", self._content())

    def test_review_gate_reference_documented(self):
        self.assertIn("references/review-gate.md", self._content())


# ---------------------------------------------------------------------------
# references
# ---------------------------------------------------------------------------

class TestReferences(unittest.TestCase):

    def test_plan_draft_retrieval_reference_exists_and_uses_index_rule(self):
        p = skill_path("plan-draft", "references", "confluence-retrieval.md")
        self.assertTrue(os.path.isfile(p), f"{p} 없음")
        content = read_text(p)
        for phrase in [
            ".confluence-index/registry.json",
            "source-index.jsonl",
            "tree.md",
            "smallest relevant",
            "raw exported Markdown",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_plan_publish_runbook_exists_and_uses_schema_aware_mcp_terms(self):
        p = skill_path("plan-publish", "references", "publish-runbook.md")
        self.assertTrue(os.path.isfile(p), f"{p} 없음")
        content = read_text(p)
        for phrase in [
            "MCP tool discovery",
            "cloudId",
            "spaceId",
            "body",
            "contentFormat",
            "parent lookup",
            "normalize",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_plan_review_gate_reference_exists(self):
        p = skill_path("plan-review", "references", "review-gate.md")
        self.assertTrue(os.path.isfile(p), f"{p} 없음")
        content = read_text(p)
        for phrase in ["[미정]", "[가정]", "충돌 경고", "pass", "conditional pass"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)


if __name__ == "__main__":
    unittest.main()
