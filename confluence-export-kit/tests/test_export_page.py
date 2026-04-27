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

    def test_single_page_url_keeps_positional_output_path(self) -> None:
        args = self.module.parse_args(
            [
                "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
                "./docs/confluence",
            ]
        )

        self.assertEqual(
            args.page_urls,
            ["https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page"],
        )
        self.assertEqual(args.output_path, "./docs/confluence")

    def test_multiple_page_urls_are_not_treated_as_output_path(self) -> None:
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
        self.assertIsNone(args.output_path)

    def test_multiple_page_urls_keep_trailing_output_path(self) -> None:
        args = self.module.parse_args(
            [
                "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
                "https://alpha.atlassian.net/wiki/spaces/ENG/pages/2/Other",
                "./docs/confluence",
            ]
        )

        self.assertEqual(
            args.page_urls,
            [
                "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
                "https://alpha.atlassian.net/wiki/spaces/ENG/pages/2/Other",
            ],
        )
        self.assertEqual(args.output_path, "./docs/confluence")

    def test_output_path_flag_still_works(self) -> None:
        args = self.module.parse_args(
            [
                "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
                "--output-path",
                "./docs/confluence",
            ]
        )

        self.assertEqual(
            args.page_urls,
            ["https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page"],
        )
        self.assertEqual(args.output_path, "./docs/confluence")

    def test_rejects_positional_and_flag_output_paths_together(self) -> None:
        with mock.patch("sys.stderr", new_callable=io.StringIO), self.assertRaises(SystemExit):
            self.module.parse_args(
                [
                    "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
                    "./positional",
                    "--output-path",
                    "./flag",
                ]
            )

    def test_main_passes_all_page_urls_to_cme_pages(self) -> None:
        argv = [
            "export_page.py",
            "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
            "https://alpha.atlassian.net/wiki/spaces/ENG/pages/2/Other",
            "./docs/confluence",
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
        self.assertEqual(
            run_cme.call_args.args[2]["CME_EXPORT__OUTPUT_PATH"],
            "./docs/confluence",
        )
        run_index.assert_called_once_with("./docs/confluence")


if __name__ == "__main__":
    unittest.main()
