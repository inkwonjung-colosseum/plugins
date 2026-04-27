#!/usr/bin/env python3
"""Export one or more Confluence pages by URL with cme."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))

from scripts.cme_runtime import (
    build_export_env,
    cleanup_renamed_page_exports,
    DEFAULT_OUTPUT_PATH,
    run_cme_and_report,
    run_index_export_and_report,
    snapshot_lockfile_export_paths,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export one or more Confluence pages by URL with confluence-markdown-exporter."
    )
    parser.add_argument(
        "page_targets",
        nargs="+",
        help="One or more Confluence page URLs to export.",
    )
    args = parser.parse_args(argv)
    args.page_urls = args.page_targets
    return args


def main() -> int:
    args = parse_args()
    output_path = DEFAULT_OUTPUT_PATH

    print("Config/auth status: assumed configured")
    print(f"Page count: {len(args.page_urls)}")
    for url in args.page_urls:
        print(f"  {url}")
    print(f"Effective output path: {output_path}")

    previous_export_paths = snapshot_lockfile_export_paths(output_path)
    run_cme_and_report(
        "cme",
        ["pages", *args.page_urls],
        build_export_env(args),
    )
    removed_count = cleanup_renamed_page_exports(output_path, previous_export_paths)
    if removed_count:
        print(f"Renamed page cleanup: removed {removed_count} stale path(s)")
    run_index_export_and_report(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
