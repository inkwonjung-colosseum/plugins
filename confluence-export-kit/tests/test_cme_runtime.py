from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import unittest
from unittest import mock


RUNTIME_PATH = Path(__file__).resolve().parents[1] / "scripts" / "cme_runtime.py"


def load_runtime_module():
    spec = importlib.util.spec_from_file_location("cme_runtime", RUNTIME_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {RUNTIME_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CmeRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_runtime_module()

    def test_export_env_propagates_resolved_config_path_and_effective_defaults(self) -> None:
        args = argparse.Namespace(
            config_path="/tmp/custom-config.json",
            output_path=None,
            skip_unchanged=False,
            cleanup_stale=False,
            jira_enrichment=False,
            max_workers=None,
        )

        env = self.module.build_export_env(
            args,
            config_path=Path("/tmp/custom-config.json"),
            output_path="confluence",
        )

        self.assertEqual(env["CME_CONFIG_PATH"], "/tmp/custom-config.json")
        self.assertEqual(env["CME_EXPORT__OUTPUT_PATH"], "confluence")
        self.assertEqual(env["CME_EXPORT__SKIP_UNCHANGED"], "false")
        self.assertEqual(env["CME_EXPORT__CLEANUP_STALE"], "false")
        self.assertEqual(env["CME_EXPORT__ENABLE_JIRA_ENRICHMENT"], "false")

    def test_export_env_propagates_enabled_flags_as_true(self) -> None:
        args = argparse.Namespace(
            config_path=None,
            output_path="./docs/confluence",
            skip_unchanged=True,
            cleanup_stale=True,
            jira_enrichment=True,
            max_workers=3,
        )

        env = self.module.build_export_env(
            args,
            config_path=Path("/tmp/app-data.json"),
            output_path="./docs/confluence",
        )

        self.assertEqual(env["CME_CONFIG_PATH"], "/tmp/app-data.json")
        self.assertEqual(env["CME_EXPORT__OUTPUT_PATH"], "./docs/confluence")
        self.assertEqual(env["CME_EXPORT__SKIP_UNCHANGED"], "true")
        self.assertEqual(env["CME_EXPORT__CLEANUP_STALE"], "true")
        self.assertEqual(env["CME_EXPORT__ENABLE_JIRA_ENRICHMENT"], "true")
        self.assertEqual(env["CME_CONNECTION_CONFIG__MAX_WORKERS"], "3")

    def test_python_preflight_rejects_python_below_310(self) -> None:
        with mock.patch.object(self.module.sys, "version_info", (3, 9, 6)):
            with self.assertRaisesRegex(RuntimeError, "Python 3.10\\+"):
                self.module.ensure_python_preflight()

    def test_cme_preflight_does_not_bootstrap_pipx_when_cme_already_exists(self) -> None:
        with (
            mock.patch.object(self.module, "find_named_executable", return_value="/usr/local/bin/cme"),
            mock.patch.object(self.module, "validate_cme") as validate_mock,
            mock.patch.object(self.module, "ensure_pipx_available") as pipx_mock,
        ):
            cme_path, cme_status, installer_status = self.module.ensure_cme_available()

        self.assertEqual(cme_path, "/usr/local/bin/cme")
        self.assertEqual(cme_status, "already available")
        self.assertEqual(installer_status, "not needed (cme already available)")
        validate_mock.assert_called_once_with("/usr/local/bin/cme")
        pipx_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
