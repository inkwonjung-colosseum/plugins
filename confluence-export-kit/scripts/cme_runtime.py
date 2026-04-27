#!/usr/bin/env python3
"""Shared runtime helpers for Confluence export skills bundled into Confluence Export Kit."""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


IS_WINDOWS = platform.system() == "Windows"
PACKAGE_NAME = "confluence-markdown-exporter"


def run_command(
    cmd: list[str],
    *,
    check: bool = True,
    capture_output: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        check=check,
        capture_output=capture_output,
        text=True,
        env=env or os.environ.copy(),
    )


def platform_label() -> str:
    return f"{platform.system()} {platform.release()}"


def ensure_exporter_installed_with_pip() -> str:
    try:
        run_command([sys.executable, "-m", "pip", "show", PACKAGE_NAME])
        return "already installed"
    except subprocess.CalledProcessError:
        run_command([sys.executable, "-m", "pip", "install", PACKAGE_NAME])
        return "installed via pip"


def resolve_config_path(explicit_path: str | None, cme_path: str) -> Path:
    if explicit_path:
        return Path(explicit_path).expanduser().resolve()

    result = run_command([cme_path, "config", "path"])
    path = result.stdout.strip()
    if not path:
        raise RuntimeError("`cme config path` returned an empty path.")
    return Path(path).expanduser().resolve()


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Config file is not valid JSON: {path}") from exc
    if not isinstance(data, dict):
        raise RuntimeError(f"Config file must contain a JSON object: {path}")
    return data


def ensure_dict(parent: dict[str, Any], key: str) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        value = {}
        parent[key] = value
    return value


def normalize_nonempty(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise RuntimeError(f"{field_name} must not be blank.")
    return normalized


def get_service_entry(data: dict[str, Any], service: str, url: str) -> dict[str, Any]:
    auth = ensure_dict(data, "auth")
    service_map = ensure_dict(auth, service)
    entry = service_map.get(url)
    if not isinstance(entry, dict):
        entry = {}
        service_map[url] = entry
    return entry


def canonicalize_base_url(url: str, *, error_label: str = "Confluence base URL") -> str:
    normalized = normalize_nonempty(url, error_label)
    parsed = urlparse(normalized)
    if parsed.scheme != "https" or not parsed.netloc:
        raise RuntimeError(
            f"Invalid {error_label}: {url} "
            "(only https:// URLs are allowed to protect credentials)."
        )
    return f"https://{parsed.netloc}"


# ---------------------------------------------------------------------------
# Shared export infrastructure
# ---------------------------------------------------------------------------

DEFAULT_OUTPUT_PATH = "confluence"
DEFAULT_SITE: str = os.environ.get(
    "CONFLUENCE_EXPORT_KIT_BASE_URL",
    "https://colosseum.atlassian.net",
).rstrip("/")


def effective_output_path(config_data: dict[str, Any], override: str | None) -> str:
    if override:
        return override
    export = config_data.get("export", {})
    if not isinstance(export, dict):
        return DEFAULT_OUTPUT_PATH
    current = export.get("output_path")
    return current if isinstance(current, str) and current.strip() else DEFAULT_OUTPUT_PATH


def write_json_atomic(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", delete=False, dir=path.parent,
        prefix=path.name + ".", suffix=".tmp",
    ) as tmp:
        json.dump(data, tmp, indent=2)
        tmp.write("\n")
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)


def set_auth_credentials(
    data: dict[str, Any],
    base_url: str,
    username: str,
    api_token: str,
    *,
    mirror_jira: bool = True,
) -> bool:
    confluence_entry = get_service_entry(data, "confluence", base_url)
    confluence_entry["username"] = username
    confluence_entry["api_token"] = api_token
    confluence_entry["pat"] = ""

    if not mirror_jira:
        return False

    jira_entry = get_service_entry(data, "jira", base_url)
    jira_entry["username"] = username
    jira_entry["api_token"] = api_token
    jira_entry["pat"] = ""
    return True


def set_default_output_path(data: dict[str, Any], output_path: str) -> Any:
    export_section = ensure_dict(data, "export")
    previous = export_section.get("output_path", "(not set)")
    export_section["output_path"] = output_path
    return previous


def chmod_config_private(path: Path) -> None:
    if not IS_WINDOWS:
        os.chmod(path, 0o600)


def add_export_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--skip-unchanged",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Skip pages whose version matches the lockfile (incremental export). Default: on.",
    )
    parser.add_argument(
        "--cleanup-stale",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Remove local files for pages deleted or moved in Confluence. Default: on.",
    )
    parser.add_argument(
        "--jira-enrichment",
        action="store_true",
        help="Fetch Jira issue summaries and include them in exported Markdown.",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        metavar="N",
        help="Override the number of parallel export workers.",
    )


def _bool_env(value: bool) -> str:
    return "true" if value else "false"


def build_export_env(
    args: argparse.Namespace,
    *,
    config_path: Path | str | None = None,
    output_path: str | None = None,
) -> dict[str, str]:
    env = os.environ.copy()
    if config_path:
        env["CME_CONFIG_PATH"] = str(config_path)

    effective_output_path = output_path or getattr(args, "output_path", None)
    if effective_output_path:
        env["CME_EXPORT__OUTPUT_PATH"] = effective_output_path

    env["CME_EXPORT__SKIP_UNCHANGED"] = _bool_env(args.skip_unchanged)
    env["CME_EXPORT__CLEANUP_STALE"] = _bool_env(args.cleanup_stale)
    env["CME_EXPORT__ENABLE_JIRA_ENRICHMENT"] = _bool_env(args.jira_enrichment)
    if args.max_workers is not None:
        env["CME_CONNECTION_CONFIG__MAX_WORKERS"] = str(args.max_workers)
    return env


def print_export_flags(args: argparse.Namespace) -> None:
    print(f"Skip unchanged: {'yes' if args.skip_unchanged else 'no'}")
    print(f"Cleanup stale: {'yes' if args.cleanup_stale else 'no'}")
    print(f"Jira enrichment: {'yes' if args.jira_enrichment else 'no'}")
    print(f"Max workers: {args.max_workers if args.max_workers is not None else '(default)'}")


def run_cme_and_report(cme_path: str, cmd_args: list[str], env: dict[str, str]) -> None:
    result = run_command([cme_path] + cmd_args, env=env)
    for label, text in [("cme stdout", result.stdout.strip()), ("cme stderr", result.stderr.strip())]:
        if text:
            print(f"--- {label} ---")
            print(text)
    print("Export command: completed")


def run_index_export_and_report(output_path: str) -> None:
    index_script = (
        Path(__file__).resolve().parents[1]
        / "skills"
        / "index-export"
        / "scripts"
        / "index_export.py"
    )
    result = run_command([sys.executable, str(index_script), output_path])
    for label, text in [("index stdout", result.stdout.strip()), ("index stderr", result.stderr.strip())]:
        if text:
            print(f"--- {label} ---")
            print(text)
    print("Index command: completed")
