"""
planning-team-kit v0.3.1 구조 테스트
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

    SKILLS_WITH_AGENT_CONFIG = ["plan-review"]

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
                self.assertIn("/planning-team-kit:plan-format", content)
                self.assertIn("$plan-format", content)
                self.assertNotIn("/planning-team-kit:plan-draft", content)
                self.assertNotIn("$plan-draft", content)
                self.assertNotIn("/planning-team-kit:plan-publish", content)
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

    def test_version_is_0_3_1(self):
        self.assertEqual(self._claude()["version"], "0.3.1")
        self.assertEqual(self._codex()["version"], "0.3.1")

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


# ---------------------------------------------------------------------------
# 템플릿
# ---------------------------------------------------------------------------

class TestTemplates(unittest.TestCase):

    REQUIRED_TEMPLATES = ["기능설계서.md", "정책서.md"]

    def _feature_content(self):
        return read_text(skill_path("plan-format", "templates", "기능설계서.md"))

    def _feature_acceptance_section(self):
        content = self._feature_content()
        return content.split("## 11. 인수 조건 / 확인 기준 [필수]", 1)[1].split("## 12.", 1)[0]

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
        for section in ["기능 설명", "전체 흐름", "권한 정책", "기능 상세 설계", "예외 처리", "인수 조건"]:
            self.assertIn(section, content, f"기능설계서 템플릿에 '{section}' 없음")

    def test_기능설계서_has_formatter_contract_sections(self):
        content = self._feature_content()
        for phrase in [
            "입력 반영 요약",
            "초안 생성 가능성",
            "섹션 적용 체크리스트",
            "확인 기준",
            "관련 정책 ID",
            "값/코드 출처",
            "상태별 수정 가능",
            "권한별 수정 가능",
            "기준 ID",
            "조건",
            "사용자 행동",
            "기대 결과",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_기능설계서_qa_section_numbering_is_consistent(self):
        content = self._feature_content()
        for section in ["### 11.1", "### 11.2", "### 11.3", "### 11.4", "### 11.5"]:
            with self.subTest(section=section):
                self.assertIn(section, content)
        for old_section in ["### 12.1", "### 12.2", "### 12.3", "### 12.4", "### 12.5"]:
            with self.subTest(old_section=old_section):
                self.assertNotIn(old_section, content)

    def test_기능설계서_acceptance_section_is_planner_owned(self):
        acceptance_section = self._feature_acceptance_section()
        for phrase in ["조건", "사용자 행동", "기대 결과", "검토 상태"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, acceptance_section)
        for phrase in ["테스트 데이터", "절차", "우선순위", "Case ID", "TC-", "케이스", "검수"]:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, acceptance_section)

    def test_optional_visual_artifacts_are_not_required(self):
        feature = self._feature_content()
        policy = read_text(skill_path("plan-format", "templates", "정책서.md"))
        self.assertIn("Flow Chart: <!-- 있으면 링크 또는 이미지. 없으면 위 흐름 표만으로 충분 -->", feature)
        self.assertIn("다이어그램: <!-- 있으면 링크 또는 이미지. 없으면 위 상태 전이 표만으로 충분 -->", policy)

    def test_audit_retention_can_reference_common_policy(self):
        content = self._feature_content()
        self.assertIn("보존 기간은 공통 보존 정책 참조 가능", content)
        self.assertIn("기능별 예외가 있으면 별도 명시", content)
        self.assertIn("공통 보존 정책 참조 / [미정]", content)

    def test_기능설계서_has_section_applicability_checklist(self):
        content = read_text(skill_path("plan-format", "templates", "기능설계서.md"))
        for phrase in [
            "0.1 섹션 적용 체크리스트",
            "적용 여부",
            "남길 섹션",
            "권한 분리",
            "상태 전이",
            "시간/SLA",
            "엑셀 입력",
            "외부 채널",
            "예 / 아니오 / [미정]",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_기능설계서_core_tables_have_review_status(self):
        content = read_text(skill_path("plan-format", "templates", "기능설계서.md"))
        required_review_status_count = 15
        self.assertGreaterEqual(
            content.count("검토 상태"),
            required_review_status_count,
            "기능설계서 주요 표는 [미정]/[가정]을 명시할 검토 상태 컬럼을 가져야 함",
        )

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

    def test_기능설계서_exception_rows_have_ids_and_unknown_policy_links(self):
        content = self._feature_content()
        for phrase in [
            "| EX-001      | 필수값 누락",
            "| EX-002      | 중복 데이터",
            "| EX-003      | 권한 부족",
            "| EX-004      | 상태 조건 불충족",
            "차단 메시지 노출",
            "| [미정]",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_기능설계서_message_sections_have_clear_ownership(self):
        content = self._feature_content()
        self.assertIn("차단성 예외의 사용자 노출 결과", content)
        self.assertIn("비차단 안내 메시지", content)
        self.assertIn("기획 의도와 초안 문구", content)
        self.assertIn("최종 UX copy·디자인 명세가 아니다", content)
        self.assertIn("차단성 예외 메시지는 §9에 적는다", content)
        self.assertNotIn("검증 실패 차단 메시지는 §10", content)

    def test_templates_document_id_rules(self):
        for template in ["기능설계서.md", "정책서.md"]:
            content = read_text(skill_path("plan-format", "templates", template))
            for phrase in [
                "ID 작성 규칙",
                "P-###",
                "R-###",
                "ST-###",
                "EX-###",
                "AC-###",
                "[미정]",
                "초안에서는 연결 ID를 `[미정]`으로 둘 수 있으나",
                "발행 전 plan-review에서 trace 연결 누락을 확인한다",
            ]:
                with self.subTest(template=template, phrase=phrase):
                    self.assertIn(phrase, content)

    def test_templates_document_detail_unknowns_after_draftability_gate(self):
        for template in ["기능설계서.md", "정책서.md"]:
            content = read_text(skill_path("plan-format", "templates", template))
            with self.subTest(template=template):
                self.assertIn("Draftability gate 통과 후에도", content)
                self.assertIn("세부 미정", content)
                self.assertIn("[미정]", content)

    def test_정책서_has_required_sections(self):
        content = read_text(skill_path("plan-format", "templates", "정책서.md"))
        for section in ["문서 목적", "적용 범위", "정책 원칙", "세부 규칙", "예외 시나리오", "상태 전이", "미확정 항목"]:
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
        self.assertIn("기능설계서 §9 예외 처리", content)
        self.assertIn("기능설계서 §6.1.2는 정책서 §6 상태 전이를 사용자 동작 관점으로 참조한다", content)
        self.assertIn("비즈니스 연동 정책만 작성", content)
        self.assertIn("API 계약·schema·technical design은 작성하지 않는다", content)
        self.assertIn("재시도 횟수·timeout·queue 같은 구현 방식은 작성하지 않는다", content)
        self.assertIn("업무상 실패 대응", content)
        self.assertIn("본 정책과 연결된 기능설계서", content)

    def test_정책서_has_trace_and_evidence_fields(self):
        content = read_text(skill_path("plan-format", "templates", "정책서.md"))
        for phrase in [
            "R-001",
            "ST-001",
            "EX-001",
            "근거",
            "검토 상태",
            "관련 문서 및 근거",
            "결정 필요 이유",
            "영향 범위",
            "확인 질문",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)


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
                self.assertIn("Draftability gate", content)
                self.assertIn("저장 보류", content)
        style = read_text(os.path.join(DOCS, "style-guide.md"))
        self.assertIn("생성 전", style)
        self.assertIn("발행 전", style)
        combined = "\n".join(
            read_text(os.path.join(DOCS, doc))
            for doc in ["examples.md", "quality-rubric.md", "style-guide.md"]
        )
        self.assertNotIn("Completeness gate", combined)

    def test_docs_use_planner_acceptance_wording(self):
        for doc in ["examples.md", "quality-rubric.md", "style-guide.md"]:
            with self.subTest(doc=doc):
                content = read_text(os.path.join(DOCS, doc))
                self.assertIn("인수 조건", content)
                self.assertIn("확인 기준", content)
                self.assertNotIn("QA 시드", content)
                self.assertNotIn("QA 매트릭스", content)
                self.assertNotIn("검수 기준", content)


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
        self.assertIn("Draftability gate", content)
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
        self.assertIn("Draftability gate 통과 시 두 문서를 모두 생성", content)
        self.assertIn("상위설계서는 지원하지 않는다", content)

    def test_parallel_body_generation_contract_documented(self):
        content = self._content()
        for phrase in [
            "공통 분석은 순차 실행",
            "문서 본문 작성만 병렬 실행",
            "공통 planning brief",
            "기능설계서 작성 worker",
            "정책서 작성 worker",
            "최종 조정은 단일 실행",
            "역할명 불일치",
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
            "Draftability gate",
            "저장 보류",
            "blocked",
            "passed",
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

    def test_formatter_scope_documented(self):
        content = self._content()
        for phrase in [
            "formatting 중심",
            "초안 생성 가능성 검증",
            "Confluence 검증은 plan-review",
            "확인 필요 질문",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_invocation_does_not_require_feature_name_argument(self):
        content = self._content()
        self.assertIn("argument-hint: \"<기획 입력 또는 파일경로>\"", content)
        self.assertIn("$plan-format <기획 입력 또는 파일경로>", content)
        self.assertIn("입력 내용에서 기능명을 추출", content)
        self.assertNotIn("$plan-format <기능명>", content)
        self.assertNotIn("/planning-team-kit:plan-format <기능명>", content)

    def test_public_examples_do_not_pass_feature_name_separately(self):
        readme = read_text(os.path.join(BASE, "README.md"))
        examples = read_text(os.path.join(DOCS, "examples.md"))
        for content in [readme, examples]:
            with self.subTest():
                self.assertIn("기능명을 입력하지 않는다", content)
                self.assertNotIn("plan-format 주문취소 \"", content)
                self.assertNotIn("plan-format 입고등록 /path", content)
                self.assertNotIn("plan-format 반품접수 \"", content)


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

    def test_agent_description_matches_four_perspectives(self):
        content = read_text(skill_path("plan-review", "agents", "openai.yaml"))
        self.assertIn("4개 관점", content)
        self.assertIn("템플릿 준수", content)

    def test_fresh_context_reviewer_is_required(self):
        content = self._content()
        for phrase in [
            "fresh-context reviewer",
            "새 검증 에이전트",
            "현재 대화 컨텍스트를 근거로 사용하지 않는다",
            "더 보수적인 verdict",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_parallel_reviewers_are_documented(self):
        content = self._content()
        for phrase in [
            "parallel fresh-context reviewers",
            "근거 reviewer",
            "범위 reviewer",
            "실행 reviewer",
            "템플릿 reviewer",
            "공통 입력 패키지",
            "최종 verdict",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_agent_description_mentions_parallel_reviewers(self):
        content = read_text(skill_path("plan-review", "agents", "openai.yaml"))
        for phrase in [
            "병렬",
            "fresh-context reviewer",
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
            "fresh-context reviewer",
            "more conservative verdict",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_plan_review_gate_parallel_aggregation_exists(self):
        content = read_text(skill_path("plan-review", "references", "review-gate.md"))
        for phrase in [
            "parallel fresh-context reviewer",
            "Role verdict",
            "final verdict",
            "수정 필요 > conditional pass > pass",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)


if __name__ == "__main__":
    unittest.main()
