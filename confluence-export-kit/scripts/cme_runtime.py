#!/usr/bin/env python3
"""Shared runtime helpers for Confluence export skills bundled into Confluence Export Kit."""

from __future__ import annotations

import argparse
import base64
import json
import os
import platform
import shutil
import site
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


PACKAGE_NAME = "confluence-markdown-exporter"
IS_WINDOWS = platform.system() == "Windows"
MIN_PYTHON_VERSION = (3, 10)


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


def ensure_python_preflight() -> str:
    python_path = Path(sys.executable).resolve()
    if not python_path.exists():
        raise RuntimeError(
            f"Python executable not found at {python_path}. "
            f"Install Python 3.10+ from https://www.python.org/downloads/ "
            f"(detected platform: {platform_label()})."
        )
    if sys.version_info < MIN_PYTHON_VERSION:
        actual_version = ".".join(str(part) for part in sys.version_info[:3])
        raise RuntimeError(
            f"Python 3.10+ is required to install and run {PACKAGE_NAME}. "
            f"Detected Python {actual_version} at {python_path} "
            f"(platform: {platform_label()})."
        )
    return str(python_path)


def ensure_pip_preflight() -> None:
    try:
        run_command([sys.executable, "-m", "pip", "--version"])
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            "Python is available, but `pip` is not. "
            f"Install pip for this Python interpreter first "
            f"(detected platform: {platform_label()})."
        ) from exc


def candidate_bin_dirs() -> list[Path]:
    candidates: list[Path] = []

    pipx_bin_dir = os.environ.get("PIPX_BIN_DIR")
    if pipx_bin_dir:
        candidates.append(Path(pipx_bin_dir).expanduser())

    user_base = Path(site.getuserbase()).expanduser()

    if IS_WINDOWS:
        candidates.append(user_base / "Scripts")
        appdata = os.environ.get("APPDATA")
        if appdata:
            candidates.append(Path(appdata) / "Python" / "Scripts")
    else:
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


def _executable_names(base: str) -> list[str]:
    names = [base]
    if IS_WINDOWS:
        names.append(base + ".exe")
    return names


def find_named_executable(name: str) -> str | None:
    direct = shutil.which(name)
    if direct:
        return direct

    for bin_dir in candidate_bin_dirs():
        for variant in _executable_names(name):
            candidate = bin_dir / variant
            if candidate.exists():
                if IS_WINDOWS or os.access(candidate, os.X_OK):
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
            raise RuntimeError(
                f"Failed to install pipx: {stderr.strip() or exc} "
                f"(detected platform: {platform_label()})."
            ) from exc
        retry_cmd = install_cmd + ["--break-system-packages"]
        try:
            run_command(retry_cmd, capture_output=True)
        except subprocess.CalledProcessError as retry_exc:
            retry_stderr = retry_exc.stderr or ""
            raise RuntimeError(
                f"Failed to install pipx after PEP 668 retry: {retry_stderr.strip() or retry_exc} "
                f"(detected platform: {platform_label()})."
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
        if path.name not in _executable_names("cme"):
            continue
        if path.exists() and (IS_WINDOWS or os.access(path, os.X_OK)):
            return str(path)
    return None


def validate_cme(cme_path: str) -> None:
    run_command([cme_path, "--help"])


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
    if parsed.scheme != "https" or not parsed.netloc:
        raise RuntimeError(
            f"Invalid {error_label}: {url} "
            "(only https:// URLs are allowed to protect credentials)."
        )
    return f"https://{parsed.netloc}"


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


# ---------------------------------------------------------------------------
# Shared config mutation infrastructure
# ---------------------------------------------------------------------------

def probe_atlassian_token(url: str, username: str, api_token: str) -> str:
    raw = f"{username}:{api_token}".encode()
    auth_header = "Basic " + base64.b64encode(raw).decode()
    probe_url = f"{url.rstrip('/')}/wiki/rest/api/user/current"
    request = urllib.request.Request(probe_url)
    request.add_header("Authorization", auth_header)
    request.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            if response.status != 200:
                raise RuntimeError(
                    f"Token probe returned HTTP {response.status} for {probe_url}"
                )
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(
            f"Token probe failed: HTTP {exc.code} {exc.reason} for {probe_url}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Token probe network error: {exc.reason}") from exc

    if not isinstance(payload, dict):
        raise RuntimeError("Token probe returned unexpected payload type.")
    return str(payload.get("displayName") or payload.get("accountId") or "ok")


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
        "--config-path",
        help="Optional explicit path to the confluence-markdown-exporter config file",
    )
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
        "--dry-run",
        action="store_true",
        help="Validate auth and config without running the export.",
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


def require_auth(config_data: dict[str, Any], base_url: str) -> dict[str, Any]:
    entry = get_configured_auth_entry(config_data, base_url)
    if not auth_entry_is_complete(entry):
        raise RuntimeError(
            "Confluence auth is not configured for this site. "
            "Run `/confluence-export-kit:set-config --api-key <api-key> --email <email>` first."
        )
    return entry


def print_preflight(
    python_path: str, pipx_status: str, cme_status: str,
    cme_path: str, config_path: Path, base_url: str,
) -> None:
    print(f"Python executable: {python_path}")
    print(f"Pipx status: {pipx_status}")
    print(f"CME status: {cme_status}")
    print(f"CME executable: {cme_path}")
    print(f"Config path: {config_path}")
    print(f"Matched site: {base_url}")
    print("Auth status: configured")


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
