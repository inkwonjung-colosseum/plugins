from __future__ import annotations

import importlib.util
import io
from pathlib import Path
import sys
import unittest
from unittest import mock


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "export-page"
    / "scripts"
    / "export_page.py"
)


def load_export_page_module():
    spec = importlib.util.spec_from_file_location("export_page", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExportPageArgumentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_export_page_module()

    def test_multiple_page_urls_are_kept_as_targets(self) -> None:
        args = self.module.parse_args(
            [
                "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
                "https://alpha.atlassian.net/wiki/spaces/ENG/pages/2/Other",
            ]
        )

        self.assertEqual(
            args.page_urls,
            [
                "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
                "https://alpha.atlassian.net/wiki/spaces/ENG/pages/2/Other",
            ],
        )

    def test_path_like_target_is_forwarded_to_cme_validation(self) -> None:
        args = self.module.parse_args(
            [
                "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
                "./docs/confluence",
            ]
        )

        self.assertEqual(
            args.page_urls,
            [
                "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
                "./docs/confluence",
            ],
        )

    def test_rejects_output_path_flag(self) -> None:
        with mock.patch("sys.stderr", new_callable=io.StringIO), self.assertRaises(SystemExit):
            self.module.parse_args(
                [
                    "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
                    "--output-path",
                    "./docs/confluence",
                ]
            )

    def test_non_url_target_is_forwarded_to_cme_validation(self) -> None:
        args = self.module.parse_args(["not-a-url"])

        self.assertEqual(args.page_urls, ["not-a-url"])

    def test_main_passes_all_page_urls_to_cme_pages(self) -> None:
        argv = [
            "export_page.py",
            "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
            "https://alpha.atlassian.net/wiki/spaces/ENG/pages/2/Other",
        ]

        with (
            mock.patch.object(sys, "argv", argv),
            mock.patch.object(self.module, "run_cme_and_report") as run_cme,
            mock.patch.object(self.module, "run_index_export_and_report") as run_index,
            mock.patch("builtins.print"),
        ):
            exit_code = self.module.main()

        self.assertEqual(exit_code, 0)
        run_cme.assert_called_once()
        self.assertEqual(run_cme.call_args.args[0], "cme")
        self.assertEqual(
            run_cme.call_args.args[1],
            [
                "pages",
                "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
                "https://alpha.atlassian.net/wiki/spaces/ENG/pages/2/Other",
            ],
        )
        self.assertEqual(run_cme.call_args.args[2]["CME_EXPORT__OUTPUT_PATH"], "./confluence")
        run_index.assert_called_once_with("./confluence")

    def test_rejects_max_workers_flag(self) -> None:
        with mock.patch("sys.stderr", new_callable=io.StringIO), self.assertRaises(SystemExit):
            self.module.parse_args(
                [
                    "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
                    "--max-workers",
                    "3",
                ]
            )

    def test_rejects_skip_unchanged_flag(self) -> None:
        with mock.patch("sys.stderr", new_callable=io.StringIO), self.assertRaises(SystemExit):
            self.module.parse_args(
                [
                    "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
                    "--skip-unchanged",
                ]
            )

    def test_rejects_no_skip_unchanged_flag(self) -> None:
        with mock.patch("sys.stderr", new_callable=io.StringIO), self.assertRaises(SystemExit):
            self.module.parse_args(
                [
                    "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
                    "--no-skip-unchanged",
                ]
            )

    def test_rejects_cleanup_stale_flag(self) -> None:
        with mock.patch("sys.stderr", new_callable=io.StringIO), self.assertRaises(SystemExit):
            self.module.parse_args(
                [
                    "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
                    "--cleanup-stale",
                ]
            )

    def test_rejects_no_cleanup_stale_flag(self) -> None:
        with mock.patch("sys.stderr", new_callable=io.StringIO), self.assertRaises(SystemExit):
            self.module.parse_args(
                [
                    "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
                    "--no-cleanup-stale",
                ]
            )

    def test_rejects_jira_enrichment_flag(self) -> None:
        with mock.patch("sys.stderr", new_callable=io.StringIO), self.assertRaises(SystemExit):
            self.module.parse_args(
                [
                    "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
                    "--jira-enrichment",
                ]
            )


if __name__ == "__main__":
    unittest.main()
