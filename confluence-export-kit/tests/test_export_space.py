from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest
from unittest import mock


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "export-space"
    / "scripts"
    / "export_space.py"
)


def load_export_space_module():
    spec = importlib.util.spec_from_file_location("export_space", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExportSpaceArgumentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_export_space_module()

    def test_single_space_url_keeps_optional_output_path(self) -> None:
        args = self.module.parse_args(
            ["https://alpha.atlassian.net/wiki/spaces/ENG", "./docs/confluence"]
        )

        self.assertEqual(args.space_urls, ["https://alpha.atlassian.net/wiki/spaces/ENG"])
        self.assertEqual(args.output_path, "./docs/confluence")

    def test_multiple_space_urls_are_not_treated_as_output_path(self) -> None:
        args = self.module.parse_args(
            [
                "https://alpha.atlassian.net/wiki/spaces/ENG",
                "https://beta.atlassian.net/wiki/spaces/OPS",
            ]
        )

        self.assertEqual(
            args.space_urls,
            [
                "https://alpha.atlassian.net/wiki/spaces/ENG",
                "https://beta.atlassian.net/wiki/spaces/OPS",
            ],
        )
        self.assertIsNone(args.output_path)

    def test_multiple_space_urls_keep_trailing_output_path(self) -> None:
        args = self.module.parse_args(
            [
                "https://alpha.atlassian.net/wiki/spaces/ENG",
                "https://beta.atlassian.net/wiki/spaces/OPS",
                "./docs/confluence",
            ]
        )

        self.assertEqual(
            args.space_urls,
            [
                "https://alpha.atlassian.net/wiki/spaces/ENG",
                "https://beta.atlassian.net/wiki/spaces/OPS",
            ],
        )
        self.assertEqual(args.output_path, "./docs/confluence")

    def test_main_passes_all_space_urls_to_cme_spaces(self) -> None:
        argv = [
            "export_space.py",
            "not-a-url",
            "still-not-a-url",
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
                "spaces",
                "not-a-url",
                "still-not-a-url",
            ],
        )
        self.assertEqual(
            run_cme.call_args.args[2]["CME_EXPORT__OUTPUT_PATH"],
            "./docs/confluence",
        )
        run_index.assert_called_once_with("./docs/confluence")


if __name__ == "__main__":
    unittest.main()
