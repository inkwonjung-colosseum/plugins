import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "planning-kit"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path):
    return json.loads(read(path))


class PublishContractTest(unittest.TestCase):
    def test_publish_skill_and_references_exist_with_safety_contracts(self):
        skill_dir = PLUGIN / "skills" / "planning-publish-confluence"
        skill = read(skill_dir / "SKILL.md")

        self.assertIn("name: planning-publish-confluence", skill)
        self.assertIn("argument-hint: \"(인자 없음", skill)
        self.assertIn("현재 context memory", skill)
        self.assertIn("위치 인자와 옵션", skill)
        self.assertIn("Confluence page create/update", skill)
        self.assertIn("Step 1: 금지 입력 확인", skill)
        self.assertIn("Step 7: write 실행과 readback", skill)

        context_gate = read(skill_dir / "references" / "context-gate.md")
        self.assertIn("금지 입력", context_gate)
        self.assertIn("로컬 파일 read", context_gate)
        self.assertIn("URL fetch", context_gate)
        self.assertIn("readable projection boundary ambiguous", context_gate)
        self.assertIn("candidate가 2개 이상", context_gate)

        page_contract = read(skill_dir / "references" / "confluence-page-contract.md")
        self.assertIn("[기능명] v0.7", page_contract)
        self.assertIn("[기능명] 정책서 v0.7", page_contract)
        self.assertIn("[기능명] 기능 설계서 v0.7", page_contract)
        self.assertIn("page move는 0.2.13 범위 밖", page_contract)
        self.assertIn("version conflict", page_contract)
        self.assertIn("readback", page_contract)
        self.assertIn("발행 label: `v0.7`", page_contract)

        output_contract = read(skill_dir / "references" / "output-contract.md")
        self.assertIn("# planning-publish-confluence", output_contract)
        self.assertIn("부분 완료", output_contract)
        self.assertIn("변경 없음", output_contract)
        self.assertIn("Confluence 변경: 없음", output_contract)

    def test_0_2_13_fixture_covers_publish_release_gates(self):
        fixture = read(PLUGIN / "docs" / "prd" / "fixtures" / "prd-0.2.13-fixtures.yml")

        required_ids = [
            "forbidden_path_input_no_io",
            "context_memory_two_bodies_publishable",
            "context_memory_duplicate_candidates_cancel",
            "default_parent_permission_preflight",
            "duplicate_unversioned_title_no_update",
            "no_write_before_final_confirm",
            "readback_fingerprint_mismatch_partial",
            "v07_title_label_required",
        ]
        for fixture_id in required_ids:
            self.assertIn(f"id: {fixture_id}", fixture)

        self.assertIn("expected_no_tool_calls", fixture)
        self.assertIn("local_file_read", fixture)
        self.assertIn("url_fetch", fixture)
        self.assertIn("confluence_create_page", fixture)
        self.assertIn("v0.7", fixture)

    def test_public_surfaces_are_versioned_and_list_publish_skill(self):
        claude = load_json(PLUGIN / ".claude-plugin" / "plugin.json")
        codex = load_json(PLUGIN / ".codex-plugin" / "plugin.json")
        claude_market = load_json(ROOT / ".claude-plugin" / "marketplace.json")
        codex_market = load_json(ROOT / ".agents" / "plugins" / "marketplace.json")

        self.assertEqual(claude["version"], "0.2.13")
        self.assertEqual(codex["version"], "0.2.13")
        self.assertIn("planning-publish-confluence", claude["description"])
        self.assertIn("planning-publish-confluence", codex["description"])
        self.assertIn("Write", codex["interface"]["capabilities"])
        self.assertTrue(any("planning-publish-confluence" in prompt for prompt in codex["interface"]["defaultPrompt"]))

        planning_claude_entry = next(item for item in claude_market["plugins"] if item["name"] == "planning-kit")
        planning_codex_entry = next(item for item in codex_market["plugins"] if item["name"] == "planning-kit")
        self.assertEqual(planning_claude_entry["version"], "0.2.13")
        self.assertEqual(planning_codex_entry["version"], "0.2.13")
        self.assertIn("planning-publish-confluence", planning_claude_entry["description"])
        self.assertIn("planning-publish-confluence", planning_codex_entry["description"])

        root_readme = read(ROOT / "README.md")
        plugin_readme = read(PLUGIN / "README.md")
        workflow = read(PLUGIN / "docs" / "planning-kit-workflow-guide.md")
        install = read(PLUGIN / "docs" / "planning-kit-install-guide-windows.md")

        for content in [root_readme, plugin_readme, workflow, install]:
            self.assertIn("planning-publish-confluence", content)
            self.assertIn("v0.7", content)


if __name__ == "__main__":
    unittest.main()
