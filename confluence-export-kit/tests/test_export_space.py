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

    def test_multiple_space_urls_are_kept_as_targets(self) -> None:
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

    def test_path_like_target_is_forwarded_to_cme_validation(self) -> None:
        args = self.module.parse_args(
            ["https://alpha.atlassian.net/wiki/spaces/ENG", "./docs/confluence"]
        )

        self.assertEqual(
            args.space_urls,
            ["https://alpha.atlassian.net/wiki/spaces/ENG", "./docs/confluence"],
        )

    def test_non_url_target_is_forwarded_to_cme_validation(self) -> None:
        args = self.module.parse_args(["not-a-url"])

        self.assertEqual(args.space_urls, ["not-a-url"])

    def test_main_passes_all_space_urls_to_cme_spaces(self) -> None:
        argv = [
            "export_space.py",
            "https://alpha.atlassian.net/wiki/spaces/ENG",
            "https://beta.atlassian.net/wiki/spaces/OPS",
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
                "https://alpha.atlassian.net/wiki/spaces/ENG",
                "https://beta.atlassian.net/wiki/spaces/OPS",
            ],
        )
        self.assertEqual(run_cme.call_args.args[2]["CME_EXPORT__OUTPUT_PATH"], "./confluence")
        run_index.assert_called_once_with("./confluence")


if __name__ == "__main__":
    unittest.main()
