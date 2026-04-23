#!/usr/bin/env python3
"""Search Confluence pages by label, then export matched pages with cme."""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))

from scripts.cme_runtime import auth_entry_is_complete
from scripts.cme_runtime import canonicalize_base_url
from scripts.cme_runtime import ensure_cme_available
from scripts.cme_runtime import ensure_python_preflight
from scripts.cme_runtime import get_configured_auth_entry
from scripts.cme_runtime import load_json
from scripts.cme_runtime import normalize_nonempty
from scripts.cme_runtime import resolve_config_path
from scripts.cme_runtime import run_command


DEFAULT_SITE = os.environ.get(
    "CONFLUENCE_EXPORT_KIT_BASE_URL",
    "https://colosseum.atlassian.net",
).rstrip("/")
DEFAULT_OUTPUT_PATH = "confluence"
SEARCH_LIMIT = 100
EXPORT_BATCH_SIZE = 25


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search Confluence pages by label and export matched pages with cme."
    )
    parser.add_argument("label", help="Confluence label name to search for")
    parser.add_argument(
        "output_path",
        nargs="?",
        help="Optional one-off export output path override. Does not persist to cme config.",
    )
    parser.add_argument(
        "--config-path",
        help="Optional explicit path to the confluence-markdown-exporter config file",
    )
    parser.add_argument(
        "--site",
        default=DEFAULT_SITE,
        help=(
            "Confluence base URL. Defaults to CONFLUENCE_EXPORT_KIT_BASE_URL, "
            "then https://colosseum.atlassian.net."
        ),
    )
    parser.add_argument(
        "--space-key",
        help="Limit search to a specific Confluence space key (e.g. ENG, DOCS).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Search only; print matched page URLs without running the export.",
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
        "--max-workers",
        type=int,
        metavar="N",
        help="Override the number of parallel export workers.",
    )
    return parser.parse_args()


def build_cql(label: str, space_key: str | None = None) -> str:
    label_escaped = label.strip().replace("\\", "\\\\").replace('"', '\\"')
    cql = f'type = page and label = "{label_escaped}"'
    if space_key:
        space_escaped = space_key.strip().replace('"', '\\"')
        cql += f' and space = "{space_escaped}"'
    cql += " order by lastmodified desc"
    return cql


def build_auth_header(auth_entry: dict) -> str:
    username = auth_entry["username"]
    api_token = auth_entry["api_token"]
    raw = f"{username}:{api_token}".encode()
    return "Basic " + base64.b64encode(raw).decode()


def request_json(url: str, auth_header: str) -> dict:
    request = urllib.request.Request(url)
    request.add_header("Authorization", auth_header)
    request.add_header("Accept", "application/json")
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if not isinstance(payload, dict):
        raise RuntimeError(f"Expected JSON object from Confluence search, got: {type(payload)}")
    return payload


def search_page_urls(
    site: str, auth_entry: dict, label: str, space_key: str | None = None
) -> list[str]:
    cql = build_cql(label, space_key)
    auth_header = build_auth_header(auth_entry)
    query = urllib.parse.urlencode({"cql": cql, "limit": SEARCH_LIMIT, "start": 0})
    next_url = f"{site}/wiki/rest/api/content/search?{query}"
    collected: list[str] = []
    seen: set[str] = set()
    api_base = f"{site}/wiki"

    while next_url:
        payload = request_json(next_url, auth_header)
        links = payload.get("_links", {})
        if isinstance(links, dict):
            api_base = str(links.get("base") or api_base)

        for item in payload.get("results", []):
            if not isinstance(item, dict):
                continue
            item_links = item.get("_links", {})
            if not isinstance(item_links, dict):
                continue
            webui = item_links.get("webui")
            if not isinstance(webui, str) or not webui:
                continue
            page_url = api_base.rstrip("/") + webui
            if page_url not in seen:
                seen.add(page_url)
                collected.append(page_url)

        next_path = links.get("next") if isinstance(links, dict) else None
        if isinstance(next_path, str) and next_path:
            if next_path.startswith("http://") or next_path.startswith("https://"):
                next_url = next_path
            else:
                next_url = api_base.rstrip("/") + next_path
        else:
            next_url = ""

    return collected


def chunked(values: list[str], size: int) -> list[list[str]]:
    return [values[index : index + size] for index in range(0, len(values), size)]


def effective_output_path(config_data: dict, override: str | None) -> str:
    if override:
        return override

    export = config_data.get("export", {})
    if not isinstance(export, dict):
        return DEFAULT_OUTPUT_PATH

    current = export.get("output_path")
    return current if isinstance(current, str) and current.strip() else DEFAULT_OUTPUT_PATH


def main() -> int:
    args = parse_args()
    label = normalize_nonempty(args.label, "Label")
    site = canonicalize_base_url(args.site)
    python_path = ensure_python_preflight()
    cme_path, cme_status, pipx_status = ensure_cme_available()
    config_path = resolve_config_path(args.config_path, cme_path)
    config_data = load_json(config_path)

    auth_entry = get_configured_auth_entry(config_data, site)
    if not auth_entry_is_complete(auth_entry):
        raise RuntimeError(
            "Confluence auth is not configured for this site. "
            "Run `/confluence-export-kit:set-api-key <api-key> <email>` first."
        )

    matched_urls = search_page_urls(site, auth_entry, label, args.space_key)
    output_path = effective_output_path(config_data, args.output_path)

    print(f"Python executable: {python_path}")
    print(f"Pipx status: {pipx_status}")
    print(f"CME status: {cme_status}")
    print(f"CME executable: {cme_path}")
    print(f"Config path: {config_path}")
    print(f"Matched site: {site}")
    print("Auth status: configured")
    print(f"Label: {label}")
    print(f"Space key filter: {args.space_key or '(none)'}")
    print(f"Dry run: {'yes' if args.dry_run else 'no'}")
    print(f"Skip unchanged: {'yes' if args.skip_unchanged else 'no'}")
    print(f"Cleanup stale: {'yes' if args.cleanup_stale else 'no'}")
    print(f"Jira enrichment: {'yes' if args.jira_enrichment else 'no'}")
    print(f"Max workers: {args.max_workers if args.max_workers is not None else '(default)'}")
    print(f"Matched pages: {len(matched_urls)}")
    print(f"Effective output path: {output_path}")

    if args.dry_run:
        print("Export command: skipped (dry-run mode)")
        if matched_urls:
            print("\n--- Matched page URLs ---")
            for url in matched_urls:
                print(url)
        return 0

    if not matched_urls:
        print("Export command: skipped (no matches)")
        return 0

    env = os.environ.copy()
    if args.output_path:
        env["CME_EXPORT__OUTPUT_PATH"] = args.output_path
    if args.skip_unchanged:
        env["CME_EXPORT__SKIP_UNCHANGED"] = "true"
    if args.cleanup_stale:
        env["CME_EXPORT__CLEANUP_STALE"] = "true"
    if args.jira_enrichment:
        env["CME_EXPORT__ENABLE_JIRA_ENRICHMENT"] = "true"
    if args.max_workers is not None:
        env["CME_CONNECTION_CONFIG__MAX_WORKERS"] = str(args.max_workers)

    batches = chunked(matched_urls, EXPORT_BATCH_SIZE)
    for batch in batches:
        run_command([cme_path, "pages", *batch], env=env)

    print(f"Export batches: {len(batches)}")
    print("Export command: completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
