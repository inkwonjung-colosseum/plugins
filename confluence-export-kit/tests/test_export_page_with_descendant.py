from __future__ import annotations

import importlib.util
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

    def test_single_page_url_keeps_optional_output_path(self) -> None:
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
        self.assertIsNone(args.output_path)

    def test_multiple_page_urls_keep_trailing_output_path(self) -> None:
        args = self.module.parse_args(
            [
                "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
                "https://beta.atlassian.net/wiki/spaces/OPS/pages/2/Other",
                "./docs/confluence",
            ]
        )

        self.assertEqual(
            args.page_urls,
            [
                "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
                "https://beta.atlassian.net/wiki/spaces/OPS/pages/2/Other",
            ],
        )
        self.assertEqual(args.output_path, "./docs/confluence")

    def test_main_passes_all_page_urls_to_cme_pages_with_descendants(self) -> None:
        config_data = {
            "auth": {
                "confluence": {
                    "https://alpha.atlassian.net": {
                        "username": "user@example.com",
                        "api_token": "alpha-token",
                    },
                    "https://beta.atlassian.net": {
                        "username": "user@example.com",
                        "api_token": "beta-token",
                    },
                }
            }
        }
        argv = [
            "export_page_with_descendant.py",
            "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
            "https://beta.atlassian.net/wiki/spaces/OPS/pages/2/Other",
            "./docs/confluence",
        ]

        with (
            mock.patch.object(sys, "argv", argv),
            mock.patch.object(self.module, "ensure_python_preflight", return_value="/python"),
            mock.patch.object(
                self.module,
                "ensure_cme_available",
                return_value=("/usr/local/bin/cme", "already available", "already available"),
            ),
            mock.patch.object(
                self.module, "resolve_config_path", return_value=Path("/tmp/cme-config.json")
            ),
            mock.patch.object(self.module, "load_json", return_value=config_data),
            mock.patch.object(self.module, "run_cme_and_report") as run_cme,
            mock.patch("builtins.print"),
        ):
            exit_code = self.module.main()

        self.assertEqual(exit_code, 0)
        run_cme.assert_called_once()
        self.assertEqual(
            run_cme.call_args.args[1],
            [
                "pages-with-descendants",
                "https://alpha.atlassian.net/wiki/spaces/ENG/pages/1/Page",
                "https://beta.atlassian.net/wiki/spaces/OPS/pages/2/Other",
            ],
        )
        self.assertEqual(
            run_cme.call_args.args[2]["CME_EXPORT__OUTPUT_PATH"],
            "./docs/confluence",
        )


if __name__ == "__main__":
    unittest.main()
