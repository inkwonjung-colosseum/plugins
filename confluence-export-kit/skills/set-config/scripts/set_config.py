#!/usr/bin/env python3
"""Persist confluence-export-kit auth and export defaults in the cme config."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))

from scripts.cme_runtime import (
    DEFAULT_OUTPUT_PATH,
    DEFAULT_SITE,
    canonicalize_base_url,
    chmod_config_private,
    ensure_exporter_installed_with_pip,
    load_json,
    normalize_nonempty,
    platform_label,
    resolve_config_path,
    set_auth_credentials,
    set_cleanup_stale,
    set_default_output_path,
    set_enable_jira_enrichment,
    set_include_document_title,
    set_page_breadcrumbs,
    set_skip_unchanged,
    write_json_atomic,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Set confluence-markdown-exporter auth and export defaults."
    )
    parser.add_argument("--api-key", help="Atlassian API token to store")
    parser.add_argument("--email", help="Required Atlassian email/username to store")
    parser.add_argument(
        "--url",
        default=DEFAULT_SITE,
        help=f"Confluence base URL for auth updates (default: {DEFAULT_SITE})",
    )
    args = parser.parse_args(argv)

    wants_auth = bool(args.api_key or args.email)
    if not wants_auth:
        parser.error("--api-key and --email are required.")
    if wants_auth and not (args.api_key and args.email):
        parser.error("--api-key and --email must be provided together.")
    return args


def main() -> int:
    args = parse_args()
    exporter_status = ensure_exporter_installed_with_pip()
    config_path = resolve_config_path(None, "cme")
    data = load_json(config_path)

    auth_updated = False
    jira_updated = False
    site = "(not updated)"
    if args.api_key:
        api_token = normalize_nonempty(args.api_key, "API token")
        username = normalize_nonempty(args.email, "Email")
        site = canonicalize_base_url(args.url)
        jira_updated = set_auth_credentials(
            data,
            site,
            username,
            api_token,
        )
        auth_updated = True

    output_previous = set_default_output_path(data, DEFAULT_OUTPUT_PATH)
    skip_unchanged_previous = set_skip_unchanged(data, True)
    cleanup_stale_previous = set_cleanup_stale(data, True)
    jira_enrichment_previous = set_enable_jira_enrichment(data, False)
    include_title_previous = set_include_document_title(data, False)
    breadcrumbs_previous = set_page_breadcrumbs(data, False)

    write_json_atomic(config_path, data)
    if auth_updated:
        chmod_config_private(config_path)

    print(f"Platform: {platform_label()}")
    print(f"Exporter status: {exporter_status}")
    print(f"Updated config: {config_path}")
    print(f"Auth updated: {'yes' if auth_updated else 'no'}")
    if auth_updated:
        print(f"Site: {site}")
        print("Username status: set from required email argument")
        print(f"Jira mirror updated: {'yes' if jira_updated else 'no'}")
    print("Output path updated: yes")
    print(f"Previous output path: {output_previous}")
    print(f"New output path: {DEFAULT_OUTPUT_PATH}")
    print(f"Previous skip unchanged: {skip_unchanged_previous}")
    print("Skip unchanged: true")
    print(f"Previous cleanup stale: {cleanup_stale_previous}")
    print("Cleanup stale: true")
    print(f"Previous Jira enrichment: {jira_enrichment_previous}")
    print("Jira enrichment: false")
    print(f"Previous include document title: {include_title_previous}")
    print("Include document title: false")
    print(f"Previous page breadcrumbs: {breadcrumbs_previous}")
    print("Page breadcrumbs: false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
