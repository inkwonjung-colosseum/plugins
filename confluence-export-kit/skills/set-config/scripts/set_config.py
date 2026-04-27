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
    DEFAULT_SITE,
    canonicalize_base_url,
    chmod_config_private,
    ensure_exporter_installed_with_pip,
    load_json,
    normalize_nonempty,
    platform_label,
    resolve_config_path,
    set_auth_credentials,
    set_default_output_path,
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
    parser.add_argument(
        "--output-path",
        help="Default export output directory to persist in cme config.",
    )
    parser.add_argument(
        "--config-path",
        help="Optional explicit path to the confluence-markdown-exporter config file",
    )
    parser.add_argument(
        "--skip-jira",
        action="store_true",
        help="Do not mirror credentials into auth.jira for the same site.",
    )
    args = parser.parse_args(argv)

    wants_auth = bool(args.api_key or args.email)
    wants_output_path = bool(args.output_path)
    if not wants_auth and not wants_output_path:
        parser.error("Set at least one of --api-key/--email or --output-path.")
    if wants_auth and not (args.api_key and args.email):
        parser.error("--api-key and --email must be provided together.")
    return args


def main() -> int:
    args = parse_args()
    exporter_status = ensure_exporter_installed_with_pip()
    config_path = resolve_config_path(args.config_path, "cme")
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
            mirror_jira=not args.skip_jira,
        )
        auth_updated = True

    output_previous = None
    output_updated = False
    if args.output_path:
        output_path = normalize_nonempty(args.output_path, "Output path")
        output_previous = set_default_output_path(data, output_path)
        output_updated = True

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
    print(f"Output path updated: {'yes' if output_updated else 'no'}")
    if output_updated:
        print(f"Previous output path: {output_previous}")
        print(f"New output path: {args.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
