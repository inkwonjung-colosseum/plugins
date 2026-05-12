import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "planning-kit"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path):
    return json.loads(read(path))


def section(content: str, start: str, end: str | None = None) -> str:
    start_index = content.index(start)
    if end is None:
        return content[start_index:]
    return content[start_index : content.index(end, start_index)]


class PlanningKit0214ContractTest(unittest.TestCase):
    def test_fixture_and_prd_index_cover_0_2_14_release_contract(self):
        fixture_path = PLUGIN / "docs" / "prd" / "fixtures" / "prd-0.2.14-fixtures.yml"
        self.assertTrue(fixture_path.exists())
        fixture = read(fixture_path)

        required_ids = [
            "planning_format_default_save_success",
            "planning_format_save_failure_fallback",
            "planning_format_no_save_screen_only",
            "planning_review_saved_files_handoff",
            "planning_review_save_failure_context_body",
            "planning_publish_storage_folder_input",
            "parser_boundaries_0_2_14",
        ]
        for fixture_id in required_ids:
            self.assertIn(f"id: {fixture_id}", fixture)

        prd_index = read(PLUGIN / "docs" / "prd" / "README.md")
        self.assertIn("fixtures/prd-0.2.14-fixtures.yml", prd_index)
        self.assertIn("저장 실패 fallback", prd_index)
        self.assertIn("저장 결과 handoff", prd_index)

    def test_planning_format_default_save_and_fallback_contract(self):
        skill = read(PLUGIN / "skills" / "planning-format" / "SKILL.md")
        output_contract = read(PLUGIN / "skills" / "planning-format" / "references" / "output-contract.md")

        self.assertIn("[--no-save]", skill)
        self.assertIn("옵션이 없으면 저장", skill)
        self.assertIn("`--save`", skill)
        self.assertIn("0.2.x 호환용 no-op alias", skill)

        output_order = section(output_contract, "## 1. 출력 블록 순서", "## 2. 출력 아티팩트 레이어")
        self.assertIn("0.2.14 기본 저장 성공 출력", output_order)
        self.assertIn("## 저장 파일", output_order)
        self.assertIn("## 체크해야 할 항목", output_order)
        self.assertIn("0.2.14 저장 실패 fallback 출력", output_order)
        self.assertIn("## 저장 실패 상세", output_order)
        self.assertIn("0.2.14 --no-save 화면 only 출력", output_order)
        self.assertNotIn("## 생성 결과 요약", output_order)
        self.assertNotIn("## 결정 보드", output_order)

        save_contract = section(output_contract, "## 8. 저장 처리", "## 9. Readable Projection Parser")
        self.assertIn("default-on", save_contract)
        self.assertIn("저장 실패 fallback", save_contract)
        self.assertIn("저장 파일에는 `## 체크해야 할 항목`", save_contract)
        self.assertIn("`## 저장 실패 상세`를 쓰지 않는다", save_contract)

    def test_planning_review_saved_file_handoff_and_result_first_output(self):
        skill = read(PLUGIN / "skills" / "planning-review" / "SKILL.md")

        self.assertIn("Step 1.1.3 planning-format 기본 저장 출력 handoff (0.2.14)", skill)
        self.assertIn("## 저장 파일", skill)
        self.assertIn("정확히 1개 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/`", skill)
        self.assertIn("- 정책서: <path>", skill)
        self.assertIn("- [기능설계서](<path>)", skill)
        self.assertIn("직전 출력의 `## 체크해야 할 항목`, `## 출처/누락 요약`, `## 상세 추적`, `## 저장 실패 상세`는 review 대상 본문에 합류하지 않는다", skill)
        self.assertIn("`planning/**`은 계속 기준 문서 묶음 근거에서 제외", skill)

        output_format = section(skill, "## 출력 포맷", "### 최종 clean-display 정규화")
        self.assertIn("# [기능명] 검토 결과", output_format)
        self.assertIn("## 결론", output_format)
        self.assertIn("## 검토 결과", output_format)
        self.assertIn("## 체크해야 할 항목", output_format)
        self.assertNotIn("## 결정 보드", output_format)
        self.assertNotIn("## 최우선 수정 항목", output_format)
        self.assertNotIn("## 작업 백로그", output_format)

    def test_planning_publish_confluence_accepts_only_explicit_storage_folder_or_context_body(self):
        skill = read(PLUGIN / "skills" / "planning-publish-confluence" / "SKILL.md")
        context_gate = read(PLUGIN / "skills" / "planning-publish-confluence" / "references" / "context-gate.md")

        self.assertIn("[planning/[안전기능명]--YYYY-MM-DD-HHMMSS/]", skill)
        self.assertIn("명시적 저장 폴더 입력", skill)
        self.assertIn("canonical 정책서·기능설계서 두 파일만", skill)
        self.assertIn("URL", skill)
        self.assertIn("임의 `.md`", skill)

        self.assertIn("0.2.14 저장 폴더 입력", context_gate)
        self.assertIn("repo root 기준 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` direct child", context_gate)
        self.assertIn("`planning/foo/`, `planning/drafts/...`, `planning/여러/중첩/...`는 인정하지 않는다", context_gate)
        self.assertIn("정책서 파일 1개와 기능설계서 파일 1개", context_gate)
        self.assertIn("`## 저장 파일`", context_gate)
        self.assertIn("`## 저장 실패 상세`", context_gate)

    def test_public_surfaces_are_versioned_for_0_2_14(self):
        claude = load_json(PLUGIN / ".claude-plugin" / "plugin.json")
        codex = load_json(PLUGIN / ".codex-plugin" / "plugin.json")
        claude_market = load_json(ROOT / ".claude-plugin" / "marketplace.json")
        codex_market = load_json(ROOT / ".agents" / "plugins" / "marketplace.json")

        self.assertEqual(claude["version"], "0.2.14")
        self.assertEqual(codex["version"], "0.2.14")
        self.assertNotIn("결정 보드 중심", claude["description"])
        self.assertNotIn("결정 보드", codex["interface"]["shortDescription"])
        self.assertIn("저장 파일", codex["description"])
        self.assertIn("결과 우선", codex["interface"]["longDescription"])

        planning_claude_entry = next(item for item in claude_market["plugins"] if item["name"] == "planning-kit")
        planning_codex_entry = next(item for item in codex_market["plugins"] if item["name"] == "planning-kit")
        self.assertEqual(planning_claude_entry["version"], "0.2.14")
        self.assertEqual(planning_codex_entry["version"], "0.2.14")
        self.assertIn("저장 파일", planning_claude_entry["description"])
        self.assertIn("결과 우선", planning_codex_entry["description"])

        docs = [
            read(ROOT / "README.md"),
            read(PLUGIN / "README.md"),
            read(PLUGIN / "docs" / "planning-kit-workflow-guide.md"),
            read(PLUGIN / "docs" / "planning-format-workflow.md"),
            read(PLUGIN / "docs" / "planning-review-workflow.md"),
            read(PLUGIN / "docs" / "planning-kit-install-guide-windows.md"),
            read(PLUGIN / "docs" / "claude-code-obsidian-claudian-install-guide-windows.md"),
        ]
        for content in docs:
            self.assertIn("0.2.14", content)
            self.assertIn("저장 파일", content)
            self.assertIn("--no-save", content)


if __name__ == "__main__":
    unittest.main()
