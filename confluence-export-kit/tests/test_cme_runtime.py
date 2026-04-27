from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
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

    def test_default_output_path_is_dot_confluence(self) -> None:
        self.assertEqual(self.module.DEFAULT_OUTPUT_PATH, "./confluence")

    def test_export_env_propagates_resolved_config_path_with_fixed_output_path(self) -> None:
        args = argparse.Namespace(
            config_path="/tmp/custom-config.json",
            output_path=None,
        )

        env = self.module.build_export_env(
            args,
            config_path=Path("/tmp/custom-config.json"),
        )

        self.assertEqual(env["CME_CONFIG_PATH"], "/tmp/custom-config.json")
        self.assertEqual(env["CME_EXPORT__OUTPUT_PATH"], "./confluence")
        self.assertNotIn("CME_EXPORT__SKIP_UNCHANGED", env)
        self.assertNotIn("CME_EXPORT__CLEANUP_STALE", env)
        self.assertNotIn("CME_EXPORT__ENABLE_JIRA_ENRICHMENT", env)

    def test_export_env_forces_fixed_output_path_over_namespace_attribute(self) -> None:
        args = argparse.Namespace(output_path="./docs/confluence")

        env = self.module.build_export_env(args)

        self.assertNotIn("CME_CONFIG_PATH", env)
        self.assertEqual(env["CME_EXPORT__OUTPUT_PATH"], "./confluence")
        self.assertNotIn("CME_EXPORT__SKIP_UNCHANGED", env)
        self.assertNotIn("CME_EXPORT__CLEANUP_STALE", env)
        self.assertNotIn("CME_EXPORT__ENABLE_JIRA_ENRICHMENT", env)

    def test_exporter_install_check_uses_pip_show_when_present(self) -> None:
        with mock.patch.object(self.module, "run_command") as run_command:
            status = self.module.ensure_exporter_installed_with_pip()

        self.assertEqual(status, "already installed")
        run_command.assert_called_once_with(
            [
                self.module.sys.executable,
                "-m",
                "pip",
                "show",
                "confluence-markdown-exporter",
            ]
        )

    def test_exporter_install_check_installs_with_pip_when_missing(self) -> None:
        with mock.patch.object(
            self.module,
            "run_command",
            side_effect=[
                subprocess.CalledProcessError(1, ["pip", "show"]),
                subprocess.CompletedProcess(["pip", "install"], 0, "", ""),
            ],
        ) as run_command:
            status = self.module.ensure_exporter_installed_with_pip()

        self.assertEqual(status, "installed via pip")
        self.assertEqual(run_command.call_count, 2)
        self.assertEqual(
            run_command.call_args_list[1].args[0],
            [
                self.module.sys.executable,
                "-m",
                "pip",
                "install",
                "confluence-markdown-exporter",
            ],
        )

    def test_cleanup_renamed_page_exports_removes_previous_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            old_file = root / "Space" / "Page 0.9.md"
            new_file = root / "Space" / "Page 0.91.md"
            old_file.parent.mkdir(parents=True)
            old_file.write_text("# Page 0.9\n", encoding="utf-8")

            lockfile_path = root / "confluence-lock.json"
            lockfile_path.write_text(
                json.dumps(
                    {
                        "lockfile_version": 2,
                        "orgs": {
                            "https://example.atlassian.net": {
                                "spaces": {
                                    "DOC": {
                                        "pages": {
                                            "123": {
                                                "title": "Page 0.9",
                                                "version": 1,
                                                "export_path": "Space/Page 0.9.md",
                                                "attachments": {},
                                            }
                                        }
                                    }
                                }
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            previous = self.module.snapshot_lockfile_export_paths(root)

            new_file.write_text("# Page 0.91\n", encoding="utf-8")
            lockfile_path.write_text(
                json.dumps(
                    {
                        "lockfile_version": 2,
                        "orgs": {
                            "https://example.atlassian.net": {
                                "spaces": {
                                    "DOC": {
                                        "pages": {
                                            "123": {
                                                "title": "Page 0.91",
                                                "version": 2,
                                                "export_path": "Space/Page 0.91.md",
                                                "attachments": {},
                                            }
                                        }
                                    }
                                }
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )

            removed = self.module.cleanup_renamed_page_exports(root, previous)

            self.assertEqual(removed, 1)
            self.assertFalse(old_file.exists())
            self.assertTrue(new_file.exists())


if __name__ == "__main__":
    unittest.main()
