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

DEFAULT_OUTPUT_PATH = "./confluence"
DEFAULT_LOCKFILE_NAME = "confluence-lock.json"
DEFAULT_SITE: str = os.environ.get(
    "CONFLUENCE_EXPORT_KIT_BASE_URL",
    "https://colosseum.atlassian.net",
).rstrip("/")


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
) -> bool:
    confluence_entry = get_service_entry(data, "confluence", base_url)
    confluence_entry["username"] = username
    confluence_entry["api_token"] = api_token
    confluence_entry["pat"] = ""

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


def set_skip_unchanged(data: dict[str, Any], skip: bool) -> Any:
    export_section = ensure_dict(data, "export")
    previous = export_section.get("skip_unchanged", "(not set)")
    export_section["skip_unchanged"] = skip
    return previous


def set_cleanup_stale(data: dict[str, Any], cleanup: bool) -> Any:
    export_section = ensure_dict(data, "export")
    previous = export_section.get("cleanup_stale", "(not set)")
    export_section["cleanup_stale"] = cleanup
    return previous


def set_enable_jira_enrichment(data: dict[str, Any], enabled: bool) -> Any:
    export_section = ensure_dict(data, "export")
    previous = export_section.get("enable_jira_enrichment", "(not set)")
    export_section["enable_jira_enrichment"] = enabled
    return previous


def set_include_document_title(data: dict[str, Any], include: bool) -> Any:
    export_section = ensure_dict(data, "export")
    previous = export_section.get("include_document_title", "(not set)")
    export_section["include_document_title"] = include
    return previous


def set_page_breadcrumbs(data: dict[str, Any], include: bool) -> Any:
    export_section = ensure_dict(data, "export")
    previous = export_section.get("page_breadcrumbs", "(not set)")
    export_section["page_breadcrumbs"] = include
    return previous


def chmod_config_private(path: Path) -> None:
    if not IS_WINDOWS:
        os.chmod(path, 0o600)


def build_export_env(
    args: argparse.Namespace,
    *,
    config_path: Path | str | None = None,
) -> dict[str, str]:
    env = os.environ.copy()
    env["CME_EXPORT__OUTPUT_PATH"] = DEFAULT_OUTPUT_PATH
    if config_path:
        env["CME_CONFIG_PATH"] = str(config_path)
    return env


def _read_lockfile_export_paths(
    output_path: str | Path,
    *,
    lockfile_name: str = DEFAULT_LOCKFILE_NAME,
) -> dict[str, str]:
    lockfile_path = Path(output_path).expanduser() / lockfile_name
    if not lockfile_path.exists():
        return {}

    try:
        data = json.loads(lockfile_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}

    page_paths: dict[str, str] = {}
    orgs = data.get("orgs")
    if not isinstance(orgs, dict):
        return page_paths

    for org in orgs.values():
        if not isinstance(org, dict):
            continue
        spaces = org.get("spaces")
        if not isinstance(spaces, dict):
            continue
        for space in spaces.values():
            if not isinstance(space, dict):
                continue
            pages = space.get("pages")
            if not isinstance(pages, dict):
                continue
            for page_id, entry in pages.items():
                if not isinstance(entry, dict):
                    continue
                export_path = entry.get("export_path")
                if isinstance(page_id, str) and isinstance(export_path, str):
                    page_paths[page_id] = export_path
    return page_paths


def snapshot_lockfile_export_paths(output_path: str | Path) -> dict[str, str]:
    return _read_lockfile_export_paths(output_path)


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _prune_empty_parents(start: Path, stop: Path) -> None:
    current = start
    while current != stop and _is_within(current, stop):
        try:
            current.rmdir()
        except OSError:
            return
        current = current.parent


def cleanup_renamed_page_exports(
    output_path: str | Path,
    previous_export_paths: dict[str, str],
) -> int:
    if not previous_export_paths:
        return 0

    current_export_paths = _read_lockfile_export_paths(output_path)
    if not current_export_paths:
        return 0

    output_root = Path(output_path).expanduser().resolve()
    removed = 0
    for page_id, previous_path in previous_export_paths.items():
        current_path = current_export_paths.get(page_id)
        if not current_path or current_path == previous_path:
            continue

        previous_file = (output_root / previous_path).resolve()
        current_file = (output_root / current_path).resolve()
        if previous_file == current_file or not _is_within(previous_file, output_root):
            continue
        if previous_file.exists() and previous_file.is_file():
            previous_file.unlink()
            removed += 1
            _prune_empty_parents(previous_file.parent, output_root)
    return removed


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
