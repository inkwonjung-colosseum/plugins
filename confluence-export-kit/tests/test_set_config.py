from __future__ import annotations

import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "set-config"
    / "scripts"
    / "set_config.py"
)


def load_set_config_module():
    spec = importlib.util.spec_from_file_location("set_config", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SetConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_set_config_module()

    def test_parse_requires_at_least_one_setting(self) -> None:
        with mock.patch("sys.stderr", new_callable=io.StringIO), self.assertRaises(SystemExit):
            self.module.parse_args([])

    def test_main_sets_auth_and_output_path_together(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = Path(tmp_dir) / "app_data.json"
            argv = [
                "set_config.py",
                "--api-key",
                "secret-token",
                "--email",
                "user@example.com",
                "--url",
                "https://alpha.atlassian.net/wiki/spaces/ENG",
                "--output-path",
                "./docs/confluence",
            ]

            with (
                mock.patch.object(sys, "argv", argv),
                mock.patch.object(
                    self.module,
                    "ensure_exporter_installed_with_pip",
                    return_value="already installed",
                ) as ensure_exporter,
                mock.patch.object(self.module, "resolve_config_path", return_value=config_path),
                mock.patch("builtins.print") as print_mock,
            ):
                exit_code = self.module.main()

            self.assertEqual(exit_code, 0)
            ensure_exporter.assert_called_once_with()
            self.assertFalse(hasattr(self.module, "probe_atlassian_token"))
            config_data = json.loads(config_path.read_text())
            self.assertEqual(
                config_data["auth"]["confluence"]["https://alpha.atlassian.net"]["username"],
                "user@example.com",
            )
            self.assertEqual(
                config_data["auth"]["confluence"]["https://alpha.atlassian.net"]["api_token"],
                "secret-token",
            )
            self.assertEqual(
                config_data["auth"]["jira"]["https://alpha.atlassian.net"]["api_token"],
                "secret-token",
            )
            self.assertEqual(config_data["export"]["output_path"], "./docs/confluence")
            printed = "\n".join(str(call.args[0]) for call in print_mock.call_args_list)
            self.assertNotIn("secret-token", printed)


if __name__ == "__main__":
    unittest.main()
