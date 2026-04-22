#!/usr/bin/env python3
"""Shared runtime helpers for Confluence export skills bundled into Plan Kit."""

from __future__ import annotations

import json
import os
import shutil
import site
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


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


def ensure_python_preflight() -> str:
    python_path = Path(sys.executable).resolve()
    if not python_path.exists():
        raise RuntimeError(f"Python executable not found: {python_path}")
    return str(python_path)


def ensure_pip_preflight() -> None:
    try:
        run_command([sys.executable, "-m", "pip", "--version"])
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            "Python is available, but `pip` is not. Install pip for this Python interpreter first."
        ) from exc


def candidate_bin_dirs() -> list[Path]:
    candidates = []

    pipx_bin_dir = os.environ.get("PIPX_BIN_DIR")
    if pipx_bin_dir:
        candidates.append(Path(pipx_bin_dir).expanduser())

    user_base = Path(site.getuserbase()).expanduser()
    candidates.append(user_base / "bin")
    candidates.append(Path.home() / ".local" / "bin")

    seen: set[Path] = set()
    unique: list[Path] = []
    for candidate in candidates:
        resolved = candidate.expanduser()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(resolved)
    return unique


def find_named_executable(name: str) -> str | None:
    direct = shutil.which(name)
    if direct:
        return direct

    for bin_dir in candidate_bin_dirs():
        candidate = bin_dir / name
        if candidate.exists() and os.access(candidate, os.X_OK):
            return str(candidate)

    return None


def pipx_command_from_environment() -> list[str] | None:
    pipx_path = find_named_executable("pipx")
    if pipx_path:
        return [pipx_path]

    try:
        run_command([sys.executable, "-m", "pipx", "--version"])
    except subprocess.CalledProcessError:
        return None
    return [sys.executable, "-m", "pipx"]


def install_pipx() -> list[str]:
    ensure_pip_preflight()
    install_cmd = [sys.executable, "-m", "pip", "install", "--user", "pipx"]
    try:
        run_command(install_cmd, capture_output=True)
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr or ""
        if "externally-managed-environment" not in stderr:
            raise RuntimeError(f"Failed to install pipx: {stderr.strip() or exc}") from exc
        retry_cmd = install_cmd + ["--break-system-packages"]
        try:
            run_command(retry_cmd, capture_output=True)
        except subprocess.CalledProcessError as retry_exc:
            retry_stderr = retry_exc.stderr or ""
            raise RuntimeError(
                f"Failed to install pipx after PEP 668 retry: {retry_stderr.strip() or retry_exc}"
            ) from retry_exc

    module_cmd = [sys.executable, "-m", "pipx"]
    try:
        run_command(module_cmd + ["--version"])
        return module_cmd
    except subprocess.CalledProcessError:
        pipx_cmd = pipx_command_from_environment()
        if pipx_cmd:
            return pipx_cmd
        raise RuntimeError("Installed `pipx`, but could not resolve a usable pipx command.")


def ensure_pipx_available() -> tuple[list[str], str]:
    pipx_cmd = pipx_command_from_environment()
    if pipx_cmd:
        return pipx_cmd, "already available"
    return install_pipx(), "installed via pip --user"


def pipx_list_json(pipx_cmd: list[str]) -> dict[str, Any]:
    result = run_command(pipx_cmd + ["list", "--json"])
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("`pipx list --json` returned invalid JSON.") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("`pipx list --json` returned an unexpected payload.")
    return payload


def pipx_has_package(pipx_cmd: list[str], package_name: str) -> bool:
    payload = pipx_list_json(pipx_cmd)
    venvs = payload.get("venvs", {})
    return isinstance(venvs, dict) and package_name in venvs


def cme_path_from_pipx_metadata(pipx_cmd: list[str]) -> str | None:
    payload = pipx_list_json(pipx_cmd)
    venvs = payload.get("venvs", {})
    if not isinstance(venvs, dict):
        return None

    package_data = venvs.get(PACKAGE_NAME, {})
    metadata = package_data.get("metadata", {})
    main_package = metadata.get("main_package", {})
    app_paths = main_package.get("app_paths", [])
    if not isinstance(app_paths, list):
        return None

    for app_path in app_paths:
        if not isinstance(app_path, dict):
            continue
        raw_path = app_path.get("__Path__")
        if not isinstance(raw_path, str):
            continue
        path = Path(raw_path)
        if path.name == "cme" and path.exists() and os.access(path, os.X_OK):
            return str(path)
    return None


def validate_cme(cme_path: str) -> None:
    run_command([cme_path, "version"])


def install_or_upgrade_cme(pipx_cmd: list[str]) -> str:
    if pipx_has_package(pipx_cmd, PACKAGE_NAME):
        run_command(pipx_cmd + ["upgrade", PACKAGE_NAME])
    else:
        run_command(pipx_cmd + ["install", PACKAGE_NAME])

    cme_path = find_named_executable("cme") or cme_path_from_pipx_metadata(pipx_cmd)
    if not cme_path:
        raise RuntimeError(
            "Installed confluence-markdown-exporter, but could not find the `cme` app."
        )
    validate_cme(cme_path)
    return cme_path


def ensure_cme_available() -> tuple[str, str, str]:
    cme_path = find_named_executable("cme")
    if cme_path:
        validate_cme(cme_path)
        pipx_cmd, pipx_status = ensure_pipx_available()
        return cme_path, "already available", pipx_status

    pipx_cmd, pipx_status = ensure_pipx_available()
    cme_path = cme_path_from_pipx_metadata(pipx_cmd)
    if cme_path:
        validate_cme(cme_path)
        return cme_path, "resolved from existing pipx installation", pipx_status

    installed_path = install_or_upgrade_cme(pipx_cmd)
    return installed_path, "installed via pipx", pipx_status


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


def extract_base_url(url: str) -> str:
    return canonicalize_base_url(url, error_label="Confluence page URL")


def canonicalize_base_url(url: str, *, error_label: str = "Confluence base URL") -> str:
    normalized = normalize_nonempty(url, error_label)
    parsed = urlparse(normalized)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise RuntimeError(f"Invalid {error_label}: {url}")
    return f"{parsed.scheme}://{parsed.netloc}"


def get_configured_auth_entry(config_data: dict[str, Any], base_url: str) -> dict[str, Any] | None:
    auth = config_data.get("auth", {})
    if not isinstance(auth, dict):
        return None
    confluence = auth.get("confluence", {})
    if not isinstance(confluence, dict):
        return None
    entry = confluence.get(base_url)
    return entry if isinstance(entry, dict) else None


def auth_entry_is_complete(entry: dict[str, Any] | None) -> bool:
    if not isinstance(entry, dict):
        return False
    username = entry.get("username")
    api_token = entry.get("api_token")
    return isinstance(username, str) and bool(username.strip()) and isinstance(
        api_token, str
    ) and bool(api_token.strip())
