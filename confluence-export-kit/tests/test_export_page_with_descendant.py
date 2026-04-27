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
    / "export-page-with-descendant"
    / "scripts"
    / "export_page_with_descendant.py"
)


def load_export_page_with_descendant_module():
    spec = importlib.util.spec_from_file_location(
        "export_page_with_descendant", SCRIPT_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExportPageWithDescendantArgumentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_export_page_with_descendant_module()

    def test_multiple_page_urls_are_kept_as_targets(self) -> None:
        args = self.module.parse_args(
            [
                "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
                "https://beta.atlassian.net/wiki/spaces/OPS/pages/2/Other",
            ]
        )

        self.assertEqual(
            args.page_urls,
            [
                "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
                "https://beta.atlassian.net/wiki/spaces/OPS/pages/2/Other",
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

    def test_non_url_target_is_forwarded_to_cme_validation(self) -> None:
        args = self.module.parse_args(["not-a-url"])

        self.assertEqual(args.page_urls, ["not-a-url"])

    def test_main_passes_all_page_urls_to_cme_pages_with_descendants(self) -> None:
        argv = [
            "export_page_with_descendant.py",
            "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
            "https://beta.atlassian.net/wiki/spaces/OPS/pages/2/Other",
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
                "pages-with-descendants",
                "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
                "https://beta.atlassian.net/wiki/spaces/OPS/pages/2/Other",
            ],
        )
        self.assertEqual(run_cme.call_args.args[2]["CME_EXPORT__OUTPUT_PATH"], "./confluence")
        run_index.assert_called_once_with("./confluence")


if __name__ == "__main__":
    unittest.main()
