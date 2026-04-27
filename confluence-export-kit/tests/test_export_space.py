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
            "export_space.py",
            "https://alpha.atlassian.net/wiki/spaces/ENG",
            "https://beta.atlassian.net/wiki/spaces/OPS",
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
            mock.patch.object(self.module, "load_cme_config", return_value=config_data) as load_cme_config,
            mock.patch.object(self.module, "run_cme_and_report") as run_cme,
            mock.patch("builtins.print"),
        ):
            exit_code = self.module.main()

        self.assertEqual(exit_code, 0)
        load_cme_config.assert_called_once_with(
            "/usr/local/bin/cme", Path("/tmp/cme-config.json")
        )
        run_cme.assert_called_once()
        self.assertEqual(
            run_cme.call_args.args[1],
            [
                "spaces",
                "https://alpha.atlassian.net/wiki/spaces/ENG",
                "https://beta.atlassian.net/wiki/spaces/OPS",
            ],
        )
        self.assertEqual(
            run_cme.call_args.args[2]["CME_EXPORT__OUTPUT_PATH"],
            "./docs/confluence",
        )


if __name__ == "__main__":
    unittest.main()
