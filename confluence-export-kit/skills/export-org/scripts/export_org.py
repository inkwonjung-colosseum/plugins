#!/usr/bin/env python3
"""Export all spaces and pages under a Confluence org with cme."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))

from scripts.cme_runtime import auth_entry_is_complete
from scripts.cme_runtime import ensure_cme_available
from scripts.cme_runtime import ensure_python_preflight
from scripts.cme_runtime import extract_base_url
from scripts.cme_runtime import get_configured_auth_entry
from scripts.cme_runtime import load_json
from scripts.cme_runtime import resolve_config_path
from scripts.cme_runtime import run_command


DEFAULT_OUTPUT_PATH = "raw/articles"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export all spaces and pages under a Confluence org with confluence-markdown-exporter."
    )
    parser.add_argument(
        "org_url",
        help="Confluence instance root URL (e.g. https://company.atlassian.net)",
    )
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
    return parser.parse_args()


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
    python_path = ensure_python_preflight()
    cme_path, cme_status, pipx_status = ensure_cme_available()
    config_path = resolve_config_path(args.config_path, cme_path)
    config_data = load_json(config_path)

    base_url = extract_base_url(args.org_url)
    auth_entry = get_configured_auth_entry(config_data, base_url)
    if not auth_entry_is_complete(auth_entry):
        raise RuntimeError(
            "Confluence auth is not configured for this site. "
            "Run `/confluence-export-kit:set-api-key <api-key> <email>` first."
        )

    output_path = effective_output_path(config_data, args.output_path)
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

    print(f"Python executable: {python_path}")
    print(f"Pipx status: {pipx_status}")
    print(f"CME status: {cme_status}")
    print(f"CME executable: {cme_path}")
    print(f"Config path: {config_path}")
    print(f"Matched site: {base_url}")
    print("Auth status: configured")
    print(f"Org URL: {args.org_url}")
    print(f"Effective output path: {output_path}")
    print(f"Skip unchanged: {'yes' if args.skip_unchanged else 'no'}")
    print(f"Cleanup stale: {'yes' if args.cleanup_stale else 'no'}")
    print(f"Jira enrichment: {'yes' if args.jira_enrichment else 'no'}")
    print(f"Max workers: {args.max_workers if args.max_workers is not None else '(default)'}")
    if args.dry_run:
        print("Export command: skipped (dry-run mode)")
        return 0

    result = run_command([cme_path, "orgs", args.org_url], env=env)

    stdout = result.stdout.strip()
    if stdout:
        print("--- cme stdout ---")
        print(stdout)

    stderr = result.stderr.strip()
    if stderr:
        print("--- cme stderr ---")
        print(stderr)

    print("Export command: completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
