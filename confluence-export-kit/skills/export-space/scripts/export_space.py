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
    cleanup_renamed_page_exports,
    DEFAULT_OUTPUT_PATH,
    effective_output_path,
    print_export_flags,
    run_cme_and_report,
    run_index_export_and_report,
    snapshot_lockfile_export_paths,
)


def is_url_like(value: str) -> bool:
    parsed = urlparse(value)
    return bool(parsed.scheme or parsed.netloc)


def split_space_targets(targets: list[str]) -> tuple[list[str], str | None]:
    if len(targets) > 1 and not is_url_like(targets[-1]):
        return targets[:-1], targets[-1]
    return targets, None


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
    output_path = effective_output_path({}, args.output_path or DEFAULT_OUTPUT_PATH)

    print("Config/auth status: assumed configured")
    print(f"Space count: {len(args.space_urls)}")
    print(f"Space URLs: {', '.join(args.space_urls)}")
    print(f"Effective output path: {output_path}")
    print_export_flags(args)

    previous_export_paths = snapshot_lockfile_export_paths(output_path)
    run_cme_and_report(
        "cme",
        ["spaces", *args.space_urls],
        build_export_env(args, output_path=output_path),
    )
    removed_count = cleanup_renamed_page_exports(output_path, previous_export_paths)
    if removed_count:
        print(f"Renamed page cleanup: removed {removed_count} stale path(s)")
    run_index_export_and_report(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
