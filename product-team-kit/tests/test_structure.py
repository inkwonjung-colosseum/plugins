"""
product-team-kit v0.4.7 구조 테스트
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
CLAUDE_MARKETPLACE = os.path.join(WORKSPACE_ROOT, ".claude-plugin", "marketplace.json")
CODEX_MARKETPLACE = os.path.join(WORKSPACE_ROOT, ".agents", "plugins", "marketplace.json")
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

    REQUIRED_SKILLS = ["plan-format", "plan-review"]

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

    SKILLS_WITH_AGENT_CONFIG = ["plan-format", "plan-review"]

    def test_skills_with_agent_config_have_openai_yaml(self):
        for skill in self.SKILLS_WITH_AGENT_CONFIG:
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
            "/product-team-kit:plan ",
            "/product-team-kit:plan\n",
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
                self.assertIn("/product-team-kit:plan-format", content)
                self.assertIn("$plan-format", content)
                self.assertNotIn("/product-team-kit:plan-draft", content)
                self.assertNotIn("$plan-draft", content)
                self.assertNotIn("/product-team-kit:plan-publish", content)
                self.assertNotIn("$plan-publish", content)

    def test_public_docs_do_not_hardcode_workspace_confluence_values(self):
        public_paths = [
            os.path.join(BASE, "README.md"),
            os.path.join(BASE, ".codex-plugin", "plugin.json"),
            os.path.join(BASE, "docs", "examples.md"),
            skill_path("plan-format", "SKILL.md"),
        ]
        forbidden_phrases = [
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

    def test_version_is_0_4_7(self):
        self.assertEqual(self._claude()["version"], "0.4.7")
        self.assertEqual(self._codex()["version"], "0.4.7")

    def test_name_is_product_team_kit(self):
        self.assertEqual(self._claude()["name"], "product-team-kit")
        self.assertEqual(self._codex()["name"], "product-team-kit")

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

    def test_claude_marketplace_does_not_claim_confluence_publish(self):
        content = read_text(CLAUDE_MARKETPLACE)
        self.assertNotIn("publishes confirmed updates to Confluence", content)

    def test_marketplaces_point_to_product_team_kit(self):
        claude_plugins = load_json(CLAUDE_MARKETPLACE)["plugins"]
        claude_entry = next(p for p in claude_plugins if p["name"] == "product-team-kit")
        self.assertEqual(claude_entry["source"], "./product-team-kit")
        self.assertEqual(claude_entry["version"], "0.4.7")

        codex_plugins = load_json(CODEX_MARKETPLACE)["plugins"]
        codex_entry = next(p for p in codex_plugins if p["name"] == "product-team-kit")
        self.assertEqual(codex_entry["source"]["path"], "./product-team-kit")


# ---------------------------------------------------------------------------
# packaging
# ---------------------------------------------------------------------------

class TestPackageHygiene(unittest.TestCase):

    FORBIDDEN_PACKAGE_SUFFIXES = (".DS_Store", ".pyc", ".pyo", ".tmp", ".swp")
    FORBIDDEN_PACKAGE_PARTS = {"__pycache__"}

    def test_package_tree_has_no_local_artifacts(self):
        for root, dirs, files in os.walk(BASE):
            rel_root = os.path.relpath(root, BASE)
            if rel_root == os.path.join("tests", "__pycache__"):
                continue
            for part in rel_root.split(os.sep):
                with self.subTest(path=rel_root, part=part):
                    self.assertNotIn(part, self.FORBIDDEN_PACKAGE_PARTS)
            for filename in files:
                rel_path = os.path.relpath(os.path.join(root, filename), BASE)
                with self.subTest(path=rel_path):
                    self.assertFalse(
                        filename.endswith(self.FORBIDDEN_PACKAGE_SUFFIXES),
                        f"패키지에 로컬 산출물 포함: {rel_path}",
                    )


# ---------------------------------------------------------------------------
# 템플릿
# ---------------------------------------------------------------------------

class TestTemplates(unittest.TestCase):

    REQUIRED_TEMPLATES = ["기능설계서.md", "정책서.md"]

    def _feature_content(self):
        return read_text(skill_path("plan-format", "templates", "기능설계서.md"))

    def _feature_acceptance_section(self):
        content = self._feature_content()
        return content.split("## 9. 확인 기준", 1)[1].split("## 10.", 1)[0]

    def test_templates_exist(self):
        for tmpl in self.REQUIRED_TEMPLATES:
            with self.subTest(template=tmpl):
                p = skill_path("plan-format", "templates", tmpl)
                self.assertTrue(os.path.isfile(p), f"템플릿 {p} 없음")

    def test_templates_not_empty(self):
        for tmpl in self.REQUIRED_TEMPLATES:
            with self.subTest(template=tmpl):
                p = skill_path("plan-format", "templates", tmpl)
                content = read_text(p)
                self.assertGreater(len(content.strip()), 100, f"템플릿 {tmpl} 내용 너무 짧음")

    def test_기능설계서_has_required_sections(self):
        content = read_text(skill_path("plan-format", "templates", "기능설계서.md"))
        for section in [
            "개요",
            "범위",
            "진입점과 사용자 흐름",
            "화면과 입력 항목",
            "기능 동작",
            "권한과 데이터 접근",
            "예외와 메시지",
            "영향 범위와 충돌 방지",
            "확인 기준",
            "확인 필요 사항",
        ]:
            self.assertIn(section, content, f"기능설계서 템플릿에 '{section}' 없음")

    def test_기능설계서_has_formatter_contract_sections(self):
        content = self._feature_content()
        for phrase in [
            "확인 기준",
            "수정 가능 조건",
            "조건",
            "사용자 행동 / 트리거",
            "기대 결과",
            "실패 / 부분 성공 기준",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_기능설계서_uses_single_confirmation_section(self):
        content = self._feature_content()
        self.assertIn("## 9. 확인 기준", content)
        for old_section in ["### 11.1", "### 11.2", "### 11.3", "### 11.4", "### 11.5"]:
            with self.subTest(old_section=old_section):
                self.assertNotIn(old_section, content)

    def test_기능설계서_acceptance_section_is_planner_owned(self):
        acceptance_section = self._feature_acceptance_section()
        for phrase in ["조건", "사용자 행동", "기대 결과"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, acceptance_section)
        for phrase in ["테스트 데이터", "절차", "우선순위", "Case ID", "TC-", "케이스", "검수"]:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, acceptance_section)

    def test_optional_visual_artifacts_are_not_baked_into_templates(self):
        feature = self._feature_content()
        policy = read_text(skill_path("plan-format", "templates", "정책서.md"))
        self.assertNotIn("Flow Chart:", feature)
        self.assertNotIn("다이어그램:", policy)
        self.assertNotIn("```mermaid", feature)
        self.assertNotIn("```mermaid", policy)

    def test_audit_retention_is_not_forced_into_every_feature_doc(self):
        content = self._feature_content()
        self.assertNotIn("감사 로그", content)
        self.assertNotIn("보존 기간", content)

    def test_기능설계서_does_not_include_generation_meta_sections(self):
        content = read_text(skill_path("plan-format", "templates", "기능설계서.md"))
        for phrase in [
            "입력 반영 요약",
            "초안 생성 가능성",
            "섹션 적용 체크리스트",
            "Draftability gate",
            "원본 입력",
            "원문",
        ]:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, content)

    def test_기능설계서_does_not_include_review_status_columns(self):
        content = read_text(skill_path("plan-format", "templates", "기능설계서.md"))
        self.assertNotIn("검토 상태", content)

    def test_기능설계서_excludes_developer_owned_contract_details(self):
        content = self._feature_content()
        forbidden = [
            "API 계약",
            "API 필드명",
            "API 엔드포인트",
            "endpoint",
            "method",
            "auth / permission",
            "request schema",
            "response schema",
            "status code",
            "error code",
            "idempotency",
            "retry / timeout",
            "시스템 디테일",
            "락/타임아웃/이벤트",
            "자동화 여부",
        ]
        for phrase in forbidden:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, content)

    def test_기능설계서_exception_section_is_concise(self):
        content = self._feature_content()
        for phrase in [
            "예외와 메시지",
            "처리 등급",
            "사용자 메시지 / 결과",
            "운영 조치",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)
        for phrase in ["예외 ID", "관련 정책 ID", "EX-001"]:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, content)

    def test_기능설계서_message_sections_have_clear_ownership(self):
        content = self._feature_content()
        self.assertIn("사용자 메시지 / 결과", content)
        self.assertIn("운영 조치", content)
        self.assertNotIn("검증 실패 차단 메시지는 §10", content)

    def test_templates_do_not_document_trace_id_rules(self):
        for template in ["기능설계서.md", "정책서.md"]:
            content = read_text(skill_path("plan-format", "templates", template))
            for phrase in [
                "ID 작성 규칙",
                "P-###",
                "R-###",
                "ST-###",
                "EX-###",
                "AC-###",
                "초안에서는 연결 ID를 `[미정]`으로 둘 수 있으나",
                "발행 전 plan-review에서 trace 연결 누락을 확인한다",
            ]:
                with self.subTest(template=template, phrase=phrase):
                    self.assertNotIn(phrase, content)

    def test_templates_do_not_force_unknown_markers(self):
        for template in ["기능설계서.md", "정책서.md"]:
            content = read_text(skill_path("plan-format", "templates", template))
            with self.subTest(template=template):
                self.assertNotIn("[미정]", content)

    def test_정책서_has_required_sections(self):
        content = read_text(skill_path("plan-format", "templates", "정책서.md"))
        for section in [
            "정책 목적",
            "적용 범위",
            "용어 정의",
            "정책 원칙",
            "세부 규칙",
            "상태 및 처리 기준",
            "역할과 권한",
            "예외 및 승인 기준",
            "외부 / 타시스템 연동 정책",
            "확인 필요 사항",
        ]:
            self.assertIn(section, content, f"정책서 템플릿에 '{section}' 없음")

    def test_정책서_does_not_reference_developer_owned_feature_details(self):
        content = read_text(skill_path("plan-format", "templates", "정책서.md"))
        forbidden = [
            "기능설계서 §10 예외 처리",
            "시스템 구현 디테일",
            "타임아웃·락·이벤트",
            "운영 가이드 문서로 분리",
            "전체 코드 시트",
            "외부 권한 관리 시트",
            "별첨/시트 링크 권장",
            "시스템 구현 기능설계서",
        ]
        for phrase in forbidden:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, content)
        self.assertIn("실패 시 업무 대응", content)
        self.assertIn("정책이 보장해야 하는 결과", content)

    def test_정책서_does_not_include_evidence_or_trace_fields(self):
        content = read_text(skill_path("plan-format", "templates", "정책서.md"))
        for phrase in ["관련 문서", "결정 필요 이유", "영향"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)
        for phrase in ["근거", "R-001", "ST-001", "EX-001", "검토 상태", "규칙 ID", "관련 규칙 ID"]:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, content)


# ---------------------------------------------------------------------------
# schemas
# ---------------------------------------------------------------------------

class TestSchemas(unittest.TestCase):

    def test_doc_types_yaml_exists(self):
        p = os.path.join(SCHEMAS, "doc-types.yaml")
        self.assertTrue(os.path.isfile(p))

    def test_doc_types_has_plan_format_types(self):
        content = read_text(os.path.join(SCHEMAS, "doc-types.yaml"))
        for doc_type in ["기능설계서", "정책서"]:
            self.assertIn(doc_type, content, f"doc-types.yaml에 '{doc_type}' 없음")
        self.assertNotIn("상위설계서", content)

    def test_doc_types_uses_plan_format_templates(self):
        content = read_text(os.path.join(SCHEMAS, "doc-types.yaml"))
        self.assertIn("skills/plan-format/templates/", content)
        self.assertNotIn("skills/plan-draft/templates/", content)
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

    def test_docs_reflect_plan_format_review_gate(self):
        for doc in ["examples.md", "quality-rubric.md", "style-guide.md", "terms-of-service.md"]:
            with self.subTest(doc=doc):
                content = read_text(os.path.join(DOCS, doc))
                self.assertIn("plan", content)
        quality = read_text(os.path.join(DOCS, "quality-rubric.md"))
        self.assertIn("[미정]", quality)
        self.assertIn("[가정]", quality)
        self.assertIn("Review Gate", quality)
        self.assertNotIn("Publish Gate", quality)
        self.assertNotIn("Publish gate", quality)

    def test_docs_reflect_draftability_gate(self):
        for doc in ["examples.md", "quality-rubric.md", "style-guide.md"]:
            with self.subTest(doc=doc):
                content = read_text(os.path.join(DOCS, doc))
                self.assertIn("초안 생성 가능성", content)
                self.assertIn("저장 보류", content)
        style = read_text(os.path.join(DOCS, "style-guide.md"))
        self.assertIn("생성 전", style)
        self.assertIn("발행 전", style)
        combined = "\n".join(
            read_text(os.path.join(DOCS, doc))
            for doc in ["examples.md", "quality-rubric.md", "style-guide.md"]
        )
        self.assertNotIn("Draftability gate", combined)
        self.assertNotIn("planning brief", combined)
        self.assertNotIn("fresh-context", combined)
        self.assertNotIn("verdict", combined)
        self.assertNotIn("Completeness gate", combined)

    def test_policy_docs_reflect_draft_folder_path(self):
        privacy = read_text(os.path.join(DOCS, "privacy-policy.md"))
        self.assertIn("planning/[안전기능명]--YYYY-MM-DD-HHMMSS/", privacy)
        self.assertNotIn("planning/drafts/[안전기능명]--YYYY-MM-DD-HHMMSS/", privacy)
        self.assertNotIn("planning/[기능명]/", privacy)

    def test_root_readme_reflects_pair_review_contract(self):
        root_readme = read_text(os.path.join(WORKSPACE_ROOT, "README.md"))
        self.assertIn("기능설계서와 정책서를 함께 검토", root_readme)
        self.assertIn("초안 폴더", root_readme)
        for phrase in ["fresh-context", "verdict", "Draftability gate"]:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, root_readme)

    def test_diagrams_do_not_use_old_internal_terms(self):
        diagram_dir = os.path.join(WORKSPACE_ROOT, "docs", "diagrams")
        for name in sorted(name for name in os.listdir(diagram_dir) if name.endswith(".html")):
            content = read_text(os.path.join(diagram_dir, name))
            for phrase in ["Draftability gate", "fresh-context", "parallel reviewers", "verdict", "plan-review (선택)"]:
                with self.subTest(name=name, phrase=phrase):
                    self.assertNotIn(phrase, content)

    def test_docs_use_planner_acceptance_wording(self):
        for doc in ["examples.md", "quality-rubric.md", "style-guide.md"]:
            with self.subTest(doc=doc):
                content = read_text(os.path.join(DOCS, doc))
                self.assertIn("확인 기준", content)
                self.assertNotIn("QA 시드", content)
                self.assertNotIn("QA 매트릭스", content)
                self.assertNotIn("검수 기준", content)

    def test_style_guide_keeps_department_owned_outputs_as_references(self):
        content = read_text(os.path.join(DOCS, "style-guide.md"))
        for phrase in [
            "Confluence 발행 문서는 정책/기능 판단 계약을 소유한다",
            "부서별 상세 산출물은 본문에 완성본처럼 생성하지 않는다",
            "관련 문서 또는 확인 필요 사항으로만 남긴다",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)


# ---------------------------------------------------------------------------
# plan-format SKILL.md 핵심 내용 검증
# ---------------------------------------------------------------------------

class TestPlanFormatSkill(unittest.TestCase):

    def _content(self):
        return read_text(skill_path("plan-format", "SKILL.md"))

    def test_single_pass_documented(self):
        content = self._content()
        for phrase in ["질문 루프 없음", "단일 패스"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_assumption_tag_documented(self):
        self.assertIn("[가정]", self._content())

    def test_plan_format_does_not_make_publish_gate_judgment(self):
        content = self._content()
        self.assertIn("초안 생성 가능성 검증", content)
        self.assertIn("생성 전 판단", content)
        self.assertIn("plan-review 권장 신호", content)
        self.assertIn("초안 생성 가능성", content)
        self.assertNotIn("Completeness gate", content)
        self.assertNotIn("Publish gate", content)
        self.assertNotIn("review-required", content)
        self.assertNotIn("발행 전 검토 상태", content)

    def test_doc_type_generation_documented(self):
        content = self._content()
        for doc_type in ["기능설계서", "정책서"]:
            self.assertIn(doc_type, content, f"plan-format SKILL.md에 문서 타입 '{doc_type}' 생성 없음")
        self.assertIn("초안 생성 가능성 검증 통과 시 두 문서를 모두 생성", content)
        self.assertIn("상위설계서는 지원하지 않는다", content)

    def test_parallel_body_generation_contract_documented(self):
        content = self._content()
        for phrase in [
            "공통 분석은 순차 실행",
            "문서 본문 작성만 병렬 실행",
            "공통 정리 기준",
            "기능설계서 작성 worker",
            "정책서 작성 worker",
            "최종 조정은 단일 실행",
            "역할명 불일치",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_proactive_mermaid_visualization_contract_documented(self):
        content = self._content()
        for phrase in [
            "적극적 보조 시각화",
            "Mermaid",
            "표시 가능한 흐름, 상태 전이, 승인/차단/예외 분기, 관계 구조가 있으면 Mermaid를 기본적으로 추가",
            "새 사실을 만들지 않는다",
            "표나 본문과 1:1로 대응",
            "기능설계서 `3. 진입점과 사용자 흐름`",
            "정책서 `6. 상태 및 처리 기준`",
            "문서당 Mermaid 개수는 1개로 제한하지 않는다",
            "Mermaid와 표/본문 불일치 여부",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_original_document_feedback_is_reported(self):
        content = self._content()
        for phrase in [
            "원본 문서 피드백",
            "중복 내용",
            "상충/모순",
            "용어 불일치",
            "범위 혼입",
            "구조 문제",
            "근거 부족",
            "최종 화면 출력",
            "입력 원문에서 관찰 가능한 문제만",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_template_meta_markers_are_removed_from_outputs(self):
        content = self._content()
        for phrase in [
            "템플릿 메타 표식",
            "[필수]",
            "[선택]",
            "[필수 — 발행 전]",
            "결과물에서 제거",
            "최종 문서에서 제거",
            "[미정]`, `[가정]`은 판단 보류 표식",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_eight_step_formatter_flow_documented(self):
        content = self._content()
        for phrase in [
            "1. 입력 받기",
            "2. 기능명 추출",
            "3. 초안 생성 가능성 검증",
            "4. 부족하면 저장하지 않고 피드백 반환",
            "5. 충분하면 입력 내용을 기능설계서/정책서로 분류",
            "6. 템플릿에 맞춰 채우기",
            "7. 일부 미확정은 `[미정]` / `[가정]` / 확인 필요 질문으로 남기기",
            "8. 파일 저장",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_draftability_gate_contract_documented(self):
        content = self._content()
        for phrase in [
            "초안 생성 가능성 검증",
            "저장 보류",
            "초안 생성 가능: 아니오",
            "초안 생성 가능: 예",
            "입력 보완 질문",
            "기능 목적/기능명",
            "적용 대상 또는 업무 범위",
            "핵심 사용자 행동과 기대 결과",
            "주요 조건/정책/제약",
            "예외/권한/상태/근거/알림",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_plan_format_does_not_retrieve_confluence(self):
        content = self._content()
        forbidden = [
            "references/confluence-retrieval.md",
            ".confluence-index",
            "registry.json",
            "source-index.jsonl",
            "관련 문서 후보 수집",
            "fallback search",
            "Confluence index missing",
        ]
        for phrase in forbidden:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, content)

    def test_plan_format_excludes_developer_owned_implementation_contract(self):
        content = self._content()
        self.assertIn("기능 동작 명세", content)
        self.assertIn("개발자 소유 API 계약·내부 구현 결정은 기능설계서에 생성하지 않는다", content)
        self.assertNotIn("구현 명세", content)

    def test_plan_format_excludes_department_owned_detailed_deliverables(self):
        content = self._content()
        for phrase in [
            "Confluence 업로드용 기능설계서와 정책서 본문만 생성한다",
            "부서 소유 상세 산출물은 본문에 완성본처럼 생성하지 않는다",
            "관련 문서 또는 확인 필요 사항으로 남긴다",
            "디자인 상세",
            "QA 상세 테스트 케이스",
            "API 명세",
            "운영 런북",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_formatter_scope_documented(self):
        content = self._content()
        for phrase in [
            "formatting 중심",
            "초안 생성 가능성 검증",
            "Confluence 근거 검증은 plan-review",
            "확인 필요 질문",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_style_guide_documents_proactive_mermaid_boundary(self):
        content = read_text(os.path.join(DOCS, "style-guide.md"))
        for phrase in [
            "Mermaid",
            "표시 가능한 흐름, 상태, 분기, 관계 구조가 있으면 기본적으로 추가",
            "새 사실을 만들지 않는다",
            "표나 본문과 불일치하면 제거하거나 수정한다",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_invocation_does_not_require_feature_name_argument(self):
        content = self._content()
        self.assertIn("argument-hint: \"<기획 입력 또는 파일경로>\"", content)
        self.assertIn("$plan-format <기획 입력 또는 파일경로>", content)
        self.assertIn("입력 내용에서 기능명을 추출", content)
        self.assertNotIn("$plan-format <기능명>", content)
        self.assertNotIn("/product-team-kit:plan-format <기능명>", content)

    def test_public_examples_do_not_pass_feature_name_separately(self):
        readme = read_text(os.path.join(BASE, "README.md"))
        examples = read_text(os.path.join(DOCS, "examples.md"))
        for content in [readme, examples]:
            with self.subTest():
                self.assertIn("기능명을 입력하지 않는다", content)
                self.assertNotIn("plan-format 주문취소 \"", content)
                self.assertNotIn("plan-format 입고등록 /path", content)
                self.assertNotIn("plan-format 반품접수 \"", content)

    def test_plan_format_review_next_step_targets_draft_folder(self):
        content = self._content()
        self.assertIn("planning/[안전기능명]--YYYY-MM-DD-HHMMSS/", content)
        self.assertIn("다음 단계: /product-team-kit:plan-review planning/[안전기능명]--YYYY-MM-DD-HHMMSS/", content)
        self.assertIn("기능설계서와 정책서를 함께 검토", content)
        self.assertNotIn("planning/drafts/[안전기능명]--YYYY-MM-DD-HHMMSS/", content)
        self.assertNotIn("다음 단계: /product-team-kit:plan-review planning/[추출기능명]/[추출기능명]_기능설계서.md", content)

    def test_plan_format_slug_contract_documented(self):
        content = self._content()
        for phrase in [
            "안전기능명",
            "경로 구분자",
            "`..`",
            "줄바꿈",
            "50자",
            "중복 저장을 피하기 위해 timestamp",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)


# ---------------------------------------------------------------------------
# plan-review SKILL.md 핵심 내용 검증
# ---------------------------------------------------------------------------

class TestPlanReviewSkill(unittest.TestCase):

    def _content(self):
        return read_text(skill_path("plan-review", "SKILL.md"))

    def test_three_perspectives_documented(self):
        content = self._content()
        for perspective in ["근거", "결정·범위", "실행·검증 가능성"]:
            self.assertIn(perspective, content, f"plan-review SKILL.md에 관점 '{perspective}' 없음")

    def test_external_publish_review_required(self):
        content = self._content()
        self.assertIn("외부 발행 전에는 필수", content)
        self.assertNotIn("선택 스킬", content)
        self.assertNotIn("건너뛸 수 있다", content)

    def test_pass_result_documented(self):
        self.assertIn("pass", self._content().lower())

    def test_conditional_pass_documented(self):
        self.assertIn("conditional pass", self._content())

    def test_review_gate_reference_documented(self):
        self.assertIn("references/review-gate.md", self._content())

    def test_agent_description_matches_three_perspectives(self):
        content = read_text(skill_path("plan-review", "agents", "openai.yaml"))
        self.assertIn("3개 관점", content)
        self.assertIn("근거 / 결정·범위 / 실행·검증 가능성", content)
        self.assertNotIn("템플릿 준수", content)

    def test_review_gate_uses_canonical_role_names(self):
        content = read_text(skill_path("plan-review", "references", "review-gate.md"))
        for role in ["근거 검토자", "결정·범위 검토자", "실행·검증 가능성 검토자"]:
            with self.subTest(role=role):
                self.assertIn(role, content)

    def test_independent_review_is_required(self):
        content = self._content()
        for phrase in [
            "독립 검토자",
            "새 검증 에이전트",
            "현재 대화 컨텍스트를 근거로 사용하지 않는다",
            "더 보수적인 검토 결과",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_parallel_reviewers_are_documented(self):
        content = self._content()
        for phrase in [
            "독립 검토 3개 관점",
            "근거 검토자",
            "결정·범위 검토자",
            "실행·검증 가능성 검토자",
            "공통 입력 패키지",
            "최종 검토 결과",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_plan_review_skill_uses_korean_business_terms_for_user_surface(self):
        content = self._content()
        for phrase in ["fresh-context", "verdict", "reviewer"]:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, content)

    def test_plan_review_accepts_draft_folder_or_pair(self):
        content = self._content()
        self.assertIn("argument-hint: \"<초안 폴더 또는 기능설계서/정책서 파일경로>\"", content)
        self.assertIn("초안 폴더를 받으면 기능설계서와 정책서를 함께 검토한다", content)
        self.assertIn("역할명·범위·정책 기준이 두 문서에서 충돌하지 않는지", content)

    def test_pass_output_does_not_allow_unknown_evidence_metadata(self):
        content = self._content()
        pass_section = content.split("### pass", 1)[1].split("### 조건부 pass", 1)[0]
        self.assertNotIn("metadata unavailable", pass_section)
        self.assertIn("status: current", pass_section)
        self.assertIn("stale: no", pass_section)

    def test_plan_review_does_not_include_template_reviewer(self):
        content = "\n".join(
            [
                self._content(),
                read_text(skill_path("plan-review", "references", "review-gate.md")),
                read_text(os.path.join(DOCS, "quality-rubric.md")),
                read_text(os.path.join(BASE, "README.md")),
                read_text(os.path.join(DOCS, "examples.md")),
                read_text(skill_path("plan-review", "agents", "openai.yaml")),
            ]
        )
        for phrase in [
            "템플릿 reviewer",
            "템플릿 준수",
            "Template completeness reviewer",
            "template completeness",
            "required sections",
            "conditional required sections",
        ]:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, content)

    def test_plan_review_contract_excludes_api_spec_review(self):
        content = "\n".join(
            [
                self._content(),
                read_text(skill_path("plan-review", "references", "review-gate.md")),
                read_text(os.path.join(DOCS, "quality-rubric.md")),
            ]
        )
        self.assertNotIn("API 누락", content)
        self.assertNotIn("APIs, data fields", content)
        for phrase in ["업무 연동 경계", "업무 데이터", "외부 채널", "실패 대응", "운영 영향"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_plan_review_flags_department_owned_deliverables_mixed_into_body(self):
        content = "\n".join(
            [
                read_text(skill_path("plan-review", "references", "review-gate.md")),
                read_text(os.path.join(DOCS, "quality-rubric.md")),
            ]
        )
        for phrase in [
            "부서 소유 상세 산출물",
            "본문에 완성본처럼 섞였는지",
            "관련 문서 또는 확인 필요 사항으로 분리",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_confluence_evidence_expansion_is_owned_by_evidence_reviewer(self):
        content = "\n".join(
            [
                self._content(),
                read_text(skill_path("plan-review", "references", "review-gate.md")),
            ]
        )
        for phrase in [
            "근거 검토자가 관련 Confluence 근거 확장 탐색을 주도한다",
            "근거 패키지",
            "결정·범위 검토자와 실행·검증 가능성 검토자는 근거 패키지를 사용한다",
            "추가 근거 후보를 발견하면 읽지 않은 관련 후보 또는 검증 한계로 남긴다",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_plan_review_requires_structured_findings(self):
        content = "\n".join(
            [
                self._content(),
                read_text(skill_path("plan-review", "references", "review-gate.md")),
                read_text(os.path.join(DOCS, "quality-rubric.md")),
            ]
        )
        for phrase in [
            "구조화된 발견 사항",
            "관점",
            "제목",
            "위치",
            "발견 유형",
            "신뢰도 앵커",
            "근거 인용",
            "영향",
            "최소 수정 포인트 또는 확인 조건",
            "출력 버킷",
            "오류",
            "누락",
            "신뢰도 앵커: 50 / 75 / 100",
            "출력 버킷: 수정 포인트 / 확인 조건 / 참고 관찰",
            "참고 관찰은 최종 검토 결과를 낮추지 않는다",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_plan_review_does_not_adopt_ce_auto_workflow_terms(self):
        content = "\n".join(
            [
                self._content(),
                read_text(skill_path("plan-review", "references", "review-gate.md")),
                read_text(os.path.join(DOCS, "quality-rubric.md")),
            ]
        )
        for phrase in [
            "safe_auto",
            "gated_auto",
            "Open Questions",
            "Auto-resolve",
            "headless mode",
        ]:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, content)

    def test_agent_description_mentions_parallel_reviewers(self):
        content = read_text(skill_path("plan-review", "agents", "openai.yaml"))
        for phrase in [
            "병렬",
            "독립 검토",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)


# ---------------------------------------------------------------------------
# references
# ---------------------------------------------------------------------------

class TestReferences(unittest.TestCase):

    def test_plan_format_has_no_references_directory(self):
        self.assertFalse(
            os.path.isdir(skill_path("plan-format", "references")),
            "plan-format은 입력값 기반 formatter라 references 디렉토리를 갖지 않는다",
        )

    def test_plan_review_gate_reference_exists(self):
        p = skill_path("plan-review", "references", "review-gate.md")
        self.assertTrue(os.path.isfile(p), f"{p} 없음")
        content = read_text(p)
        for phrase in [
            "[미정]",
            "[가정]",
            "충돌 경고",
            "pass",
            "conditional pass",
            "독립 검토자",
            "더 보수적인 검토 결과",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_plan_review_gate_confluence_evidence_contract(self):
        content = read_text(skill_path("plan-review", "references", "review-gate.md"))
        for phrase in [
            ".confluence-index/registry.json",
            "source-index.jsonl",
            "tree.md",
            "충돌 가능성이 있는 관련 문서를 충분히 확장",
            "직접 관련 문서",
            "상위/하위 문서",
            "참조 문서",
            "sibling 문서",
            "전체 export 공간을 한 번에 읽지 않는다",
            "읽지 않은 관련 후보",
            "검증 한계",
            "raw exported Markdown path",
            "source-id",
            "current/draft/archive",
            "stale",
            "metadata unavailable",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_plan_review_gate_disallows_pass_with_unknown_evidence(self):
        content = read_text(skill_path("plan-review", "references", "review-gate.md"))
        for phrase in [
            "metadata unavailable이면 pass 금지",
            "stale 값을 확인할 수 없으면 pass 금지",
            "raw exported Markdown을 읽지 못했으면 pass 금지",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_plan_review_gate_parallel_aggregation_exists(self):
        content = read_text(skill_path("plan-review", "references", "review-gate.md"))
        for phrase in [
            "독립 검토자",
            "관점별 검토 결과",
            "최종 검토 결과",
            "수정 필요 > conditional pass > pass",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_plan_review_gate_structured_synthesis_contract(self):
        content = read_text(skill_path("plan-review", "references", "review-gate.md"))
        for phrase in [
            "필수 필드가 빠진 발견 사항은 최종 판단에 사용하지 않고 검증 한계에 기록한다",
            "위치 + 제목 + 근거 인용",
            "중복 발견을 병합",
            "더 높은 심각도",
            "더 높은 신뢰도",
            "더 보수적인 출력 버킷",
            "수정 포인트가 하나라도 있으면 최종 결과는 수정 필요",
            "수정 포인트가 없고 확인 조건만 있으면 conditional pass",
            "참고 관찰만 있으면 최종 검토 결과를 낮추지 않는다",
            "구조화 출력이 실패한 검토자가 있으면 pass 금지",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_plan_review_gate_uses_korean_business_terms(self):
        content = read_text(skill_path("plan-review", "references", "review-gate.md"))
        for phrase in ["fresh-context", "verdict", "reviewer"]:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, content)


if __name__ == "__main__":
    unittest.main()
