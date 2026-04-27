#!/usr/bin/env python3
"""Export all pages in a Confluence space with cme."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.parse import urlparse

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))

from scripts.cme_runtime import (
    add_export_args,
    build_export_env,
    effective_output_path,
    ensure_cme_available,
    ensure_python_preflight,
    extract_base_url,
    load_json,
    print_export_flags,
    require_auth,
    resolve_config_path,
    run_cme_and_report,
)


def is_url_like(value: str) -> bool:
    parsed = urlparse(value)
    return bool(parsed.scheme or parsed.netloc)


def split_space_targets(targets: list[str]) -> tuple[list[str], str | None]:
    if len(targets) > 1 and not is_url_like(targets[-1]):
        return targets[:-1], targets[-1]
    return targets, None


def unique_preserving_order(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export all pages in a Confluence space with confluence-markdown-exporter."
    )
    parser.add_argument(
        "space_targets",
        nargs="+",
        help=(
            "One or more Confluence space URLs to export "
            "(e.g. https://company.atlassian.net/wiki/spaces/SPACEKEY), optionally followed by an output path."
        ),
    )
    add_export_args(parser)
    args = parser.parse_args(argv)
    args.space_urls, args.output_path = split_space_targets(args.space_targets)
    return args


def main() -> int:
    args = parse_args()
    python_path = ensure_python_preflight()
    cme_path, cme_status, installer_status = ensure_cme_available()
    config_path = resolve_config_path(args.config_path, cme_path)
    config_data = load_json(config_path)

    base_urls = unique_preserving_order(
        [extract_base_url(space_url) for space_url in args.space_urls]
    )
    for base_url in base_urls:
        require_auth(config_data, base_url)
    output_path = effective_output_path(config_data, args.output_path)

    print(f"Python executable: {python_path}")
    print(f"Installer status: {installer_status}")
    print(f"CME status: {cme_status}")
    print(f"CME executable: {cme_path}")
    print(f"Config path: {config_path}")
    print(f"Matched sites: {', '.join(base_urls)}")
    print("Auth status: configured")
    print(f"Space URLs: {', '.join(args.space_urls)}")
    print(f"Effective output path: {output_path}")
    print_export_flags(args)
    if args.dry_run:
        print("Export command: skipped (dry-run mode)")
        return 0

    run_cme_and_report(
        cme_path,
        ["spaces", *args.space_urls],
        build_export_env(args, config_path=config_path, output_path=output_path),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
