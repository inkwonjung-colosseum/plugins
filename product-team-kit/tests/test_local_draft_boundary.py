"""
product-team-kit local draft boundary contract tests.
"""

from pathlib import Path
import unittest


BASE = Path(__file__).resolve().parents[1]


def read_text(*parts):
    return (BASE.joinpath(*parts)).read_text(encoding="utf-8")


class LocalDraftBoundaryContractTest(unittest.TestCase):

    def test_readme_is_single_source_of_boundary(self):
        readme = read_text("README.md")

        self.assertIn("로컬 초안 템플릿", readme)
        self.assertIn("공식 팀 문서가 아니다", readme)
        self.assertIn("팀 문서 히스토리는 반영 이후 관리한다", readme)

    def test_plan_format_declares_local_draft_boundary(self):
        skill = read_text("skills", "plan-format", "SKILL.md")

        self.assertIn("로컬 초안 템플릿", skill)
        self.assertIn("공식 팀 문서가 아니다", skill)

    def test_public_docs_reference_boundary(self):
        docs = "\n".join(
            [
                read_text("docs", "style-guide.md"),
                read_text("docs", "quality-rubric.md"),
                read_text("docs", "examples.md"),
            ]
        )

        self.assertIn("로컬 초안 템플릿", docs)
        self.assertIn("공식 팀 문서가 아니다", docs)

    def test_templates_mark_outputs_as_local_drafts(self):
        feature_template = read_text("skills", "plan-format", "templates", "기능설계서.md")
        policy_template = read_text("skills", "plan-format", "templates", "정책서.md")

        for template in [feature_template, policy_template]:
            with self.subTest():
                self.assertIn("- 문서 상태: 로컬 초안", template)
                self.assertIn("- 팀 문서 반영 상태: 미반영", template)

    def test_no_confluence_brand_in_skill_files(self):
        """SKILL.md에 Confluence 브랜드명 없음 - vendor 중립 drift guard."""
        for skill_name in ["plan-draft", "plan-format", "plan-review"]:
            content = read_text("skills", skill_name, "SKILL.md")
            self.assertNotIn(
                "Confluence",
                content,
                msg=f"skills/{skill_name}/SKILL.md에 'Confluence' 브랜드명 있음. 팀 문서 등 중립 표현으로 교체 필요.",
            )

    def test_boundary_phrase_not_repeated_outside_readme(self):
        """Boundary 핵심 문구는 README 1곳만 - single source drift guard."""
        boundary_phrase = "팀 문서 히스토리는 반영 이후 관리한다"
        non_readme_files = [
            ("skills", "plan-format", "SKILL.md"),
            ("skills", "plan-review", "SKILL.md"),
            ("docs", "style-guide.md"),
            ("docs", "quality-rubric.md"),
            ("docs", "examples.md"),
        ]
        for parts in non_readme_files:
            content = read_text(*parts)
            self.assertNotIn(
                boundary_phrase,
                content,
                msg=f"{'/'.join(parts)}에 boundary 핵심 문구 중복. README 위임 참조로 교체 필요.",
            )


if __name__ == "__main__":
    unittest.main()
