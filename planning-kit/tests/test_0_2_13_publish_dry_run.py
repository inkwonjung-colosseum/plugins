import unittest
from dataclasses import dataclass, field
from pathlib import Path


PLUGIN = Path(__file__).resolve().parents[1]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


@dataclass
class PublishDryRun:
    final_confirmed: bool = True
    version_conflict: bool = False
    fail_readback: str | None = None
    events: list[str] = field(default_factory=list)

    def run(self) -> str:
        self.events.extend(
            [
                "context_gate",
                "ask_parent",
                "read_parent",
                "check_create_child_permission",
                "duplicate_lookup",
                "render_bodies_and_fingerprints",
                "ask_final_confirm",
            ]
        )

        if not self.final_confirmed:
            return "발행 취소"

        self.events.extend(["read_parent_again", "read_update_versions_again"])

        if self.version_conflict:
            self.events.append("version_conflict_cancel")
            return "발행 취소"

        for role in ["container", "policy", "feature"]:
            self.events.append(f"confluence_create_page:{role}")
            self.events.append(f"readback:{role}")
            if self.fail_readback == role:
                self.events.append("남은 write: 실행하지 않음")
                return "부분 완료"

        return "Confluence 발행 완료"


class PublishDryRunTest(unittest.TestCase):
    def test_no_write_occurs_before_final_confirmation(self):
        dry_run = PublishDryRun(final_confirmed=False)

        self.assertEqual(dry_run.run(), "발행 취소")
        self.assertIn("ask_final_confirm", dry_run.events)
        self.assertNotIn("confluence_create_page:container", dry_run.events)
        self.assertNotIn("confluence_update_page:container", dry_run.events)

    def test_version_conflict_cancels_before_any_write(self):
        dry_run = PublishDryRun(version_conflict=True)

        self.assertEqual(dry_run.run(), "발행 취소")
        self.assertIn("read_update_versions_again", dry_run.events)
        self.assertIn("version_conflict_cancel", dry_run.events)
        self.assertFalse(any(event.startswith("confluence_create_page") for event in dry_run.events))
        self.assertFalse(any(event.startswith("confluence_update_page") for event in dry_run.events))

    def test_policy_readback_failure_stops_feature_write_as_partial_completion(self):
        dry_run = PublishDryRun(fail_readback="policy")

        self.assertEqual(dry_run.run(), "부분 완료")
        self.assertEqual(
            dry_run.events,
            [
                "context_gate",
                "ask_parent",
                "read_parent",
                "check_create_child_permission",
                "duplicate_lookup",
                "render_bodies_and_fingerprints",
                "ask_final_confirm",
                "read_parent_again",
                "read_update_versions_again",
                "confluence_create_page:container",
                "readback:container",
                "confluence_create_page:policy",
                "readback:policy",
                "남은 write: 실행하지 않음",
            ],
        )
        self.assertNotIn("confluence_create_page:feature", dry_run.events)

    def test_output_contract_puts_urls_and_failures_before_publish_metadata(self):
        output_contract = read(
            PLUGIN
            / "skills"
            / "planning-publish-confluence"
            / "references"
            / "output-contract.md"
        )
        completed = output_contract.index("## 4. 완료 출력")
        pages = output_contract.index("## 생성/수정 페이지", completed)
        skipped = output_contract.index("## 실패/스킵", completed)
        publish_info = output_contract.index("## 발행 정보", completed)

        self.assertLess(pages, publish_info)
        self.assertLess(skipped, publish_info)
        self.assertIn("URL 또는 실패/스킵 사유를 먼저", output_contract)


if __name__ == "__main__":
    unittest.main()
