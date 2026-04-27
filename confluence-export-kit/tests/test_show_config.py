from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest
from unittest import mock


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "show-config"
    / "scripts"
    / "show_config.py"
)


def load_show_config_module():
    spec = importlib.util.spec_from_file_location("show_config", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ShowConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_show_config_module()

    def test_main_runs_cme_config_list(self) -> None:
        completed = mock.Mock(stdout="export.output_path = confluence\n", stderr="")
        with (
            mock.patch.object(sys, "argv", ["show_config.py"]),
            mock.patch.object(self.module, "run_command", return_value=completed) as run_command,
            mock.patch("builtins.print"),
        ):
            exit_code = self.module.main()

        self.assertEqual(exit_code, 0)
        run_command.assert_called_once_with(["cme", "config", "list"])

    def test_main_runs_cme_config_list_json(self) -> None:
        completed = mock.Mock(stdout='{"export": {}}\n', stderr="")
        with (
            mock.patch.object(sys, "argv", ["show_config.py", "--json"]),
            mock.patch.object(self.module, "run_command", return_value=completed) as run_command,
            mock.patch("builtins.print"),
        ):
            exit_code = self.module.main()

        self.assertEqual(exit_code, 0)
        run_command.assert_called_once_with(
            ["cme", "config", "list", "-o", "json"]
        )


if __name__ == "__main__":
    unittest.main()
