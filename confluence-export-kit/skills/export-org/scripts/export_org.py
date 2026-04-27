#!/usr/bin/env python3
"""Export all spaces and pages under a Confluence org with cme."""

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
    DEFAULT_OUTPUT_PATH,
    effective_output_path,
    print_export_flags,
    run_cme_and_report,
    run_index_export_and_report,
)


def is_url_like(value: str) -> bool:
    parsed = urlparse(value)
    return bool(parsed.scheme or parsed.netloc)


def split_org_targets(targets: list[str]) -> tuple[list[str], str | None]:
    if len(targets) > 1 and not is_url_like(targets[-1]):
        return targets[:-1], targets[-1]
    return targets, None


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export all spaces and pages under a Confluence org with confluence-markdown-exporter."
    )
    parser.add_argument(
        "org_targets",
        nargs="+",
        help=(
            "One or more Confluence instance root URLs "
            "(e.g. https://company.atlassian.net), optionally followed by an output path."
        ),
    )
    add_export_args(parser)
    args = parser.parse_args(argv)
    args.org_urls, args.output_path = split_org_targets(args.org_targets)
    return args


def main() -> int:
    args = parse_args()
    output_path = effective_output_path({}, args.output_path or DEFAULT_OUTPUT_PATH)

    print("Config/auth status: assumed configured")
    print(f"Org count: {len(args.org_urls)}")
    print(f"Org URLs: {', '.join(args.org_urls)}")
    print(f"Effective output path: {output_path}")
    print_export_flags(args)

    run_cme_and_report(
        "cme",
        ["orgs", *args.org_urls],
        build_export_env(args, output_path=output_path),
    )
    run_index_export_and_report(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
