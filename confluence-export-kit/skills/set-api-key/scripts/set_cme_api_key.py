#!/usr/bin/env python3
"""Bootstrap cme if needed, then update auth config without printing secrets."""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))

from scripts.cme_runtime import ensure_cme_available
from scripts.cme_runtime import canonicalize_base_url
from scripts.cme_runtime import ensure_dict
from scripts.cme_runtime import ensure_python_preflight
from scripts.cme_runtime import load_json
from scripts.cme_runtime import normalize_nonempty
from scripts.cme_runtime import resolve_config_path


DEFAULT_URL = os.environ.get(
    "CONFLUENCE_EXPORT_KIT_BASE_URL",
    "https://colosseum.atlassian.net",
).rstrip("/")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Set confluence-markdown-exporter API token for the Colosseum Atlassian site."
    )
    parser.add_argument("api_token", help="Atlassian API token to store")
    parser.add_argument("username", help="Required Atlassian email/username to store")
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help=f"Confluence base URL (default: {DEFAULT_URL})",
    )
    parser.add_argument(
        "--config-path",
        help="Optional explicit path to the confluence-markdown-exporter config file",
    )
    parser.add_argument(
        "--skip-jira",
        action="store_true",
        help="Do not mirror credentials into auth.jira for the same site",
    )
    parser.add_argument(
        "--skip-validate",
        action="store_true",
        help="Skip probing Atlassian /rest/api/user/current before writing config.",
    )
    return parser.parse_args()


def probe_token(url: str, username: str, api_token: str) -> str:
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


def get_service_entry(data: dict, service: str, url: str) -> dict:
    auth = ensure_dict(data, "auth")
    service_map = ensure_dict(auth, service)
    entry = service_map.get(url)
    if not isinstance(entry, dict):
        entry = {}
        service_map[url] = entry
    return entry


def write_json_atomic(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        delete=False,
        dir=path.parent,
        prefix=path.name + ".",
        suffix=".tmp",
    ) as tmp:
        json.dump(data, tmp, indent=2)
        tmp.write("\n")
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)


def main() -> int:
    args = parse_args()
    api_token = normalize_nonempty(args.api_token, "API token")
    username = normalize_nonempty(args.username, "Username")
    base_url = canonicalize_base_url(args.url)
    python_path = ensure_python_preflight()
    cme_path, cme_status, pipx_status = ensure_cme_available()
    config_path = resolve_config_path(args.config_path, cme_path)
    data = load_json(config_path)

    probe_status = "skipped"
    if not args.skip_validate:
        probe_identity = probe_token(base_url, username, api_token)
        probe_status = f"ok ({probe_identity})"

    confluence_entry = get_service_entry(data, "confluence", base_url)
    jira_entry = get_service_entry(data, "jira", base_url)

    confluence_entry["username"] = username
    confluence_entry["api_token"] = api_token
    confluence_entry["pat"] = ""

    jira_updated = False
    if not args.skip_jira:
        jira_entry["username"] = username
        jira_entry["api_token"] = api_token
        jira_entry["pat"] = ""
        jira_updated = True

    write_json_atomic(config_path, data)

    print(f"Python executable: {python_path}")
    print(f"Pipx status: {pipx_status}")
    print(f"CME status: {cme_status}")
    print(f"CME executable: {cme_path}")
    print(f"Updated config: {config_path}")
    print(f"Site: {base_url}")
    print("Username status: set from required argument")
    print(f"Jira mirror updated: {'yes' if jira_updated else 'no'}")
    print(f"Token probe: {probe_status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
