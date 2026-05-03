"""
product-team-kit plan-draft fallback contract tests.
"""

from pathlib import Path
import unittest


BASE = Path(__file__).resolve().parents[1]


def read_text(*parts):
    return (BASE.joinpath(*parts)).read_text(encoding="utf-8")


class PlanDraftFallbackContractTest(unittest.TestCase):

    def test_plan_draft_defines_plain_conversation_fallback(self):
        skill = read_text("skills", "plan-draft", "SKILL.md")

        self.assertIn("일반 대화 fallback", skill)
        self.assertIn("비대화형 실행", skill)
        self.assertIn("질문 도구가 없더라도 바로 저장 보류로 종료하지 않는다", skill)
        self.assertIn("현재 대화의 다음 사용자 답변을 같은 plan-draft 실행의 답변으로 이어받는다", skill)

    def test_output_contract_has_plain_conversation_question_template(self):
        output_contract = read_text("references", "output-contract.md")

        self.assertIn("일반 대화 질문 진행", output_contract)
        self.assertIn("파일 생성: 아니오", output_contract)
        self.assertIn("답변을 받으면 같은 plan-draft 흐름으로 이어서 판단한다", output_contract)

    def test_public_docs_describe_non_plan_mode_fallback(self):
        docs = "\n".join(
            [
                read_text("docs", "examples.md"),
                read_text("docs", "quality-rubric.md"),
                read_text("docs", "style-guide.md"),
            ]
        )

        self.assertIn("일반 대화 fallback", docs)
        self.assertIn("비대화형 실행", docs)


if __name__ == "__main__":
    unittest.main()
