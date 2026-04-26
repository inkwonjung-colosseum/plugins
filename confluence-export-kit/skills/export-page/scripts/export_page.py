#!/usr/bin/env python3
"""Export one or more Confluence pages by URL with cme."""

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
    canonicalize_base_url,
    effective_output_path,
    ensure_cme_available,
    ensure_python_preflight,
    load_json,
    print_export_flags,
    print_preflight,
    require_auth,
    resolve_config_path,
    run_cme_and_report,
)


def is_url_like(value: str) -> bool:
    parsed = urlparse(value)
    return bool(parsed.scheme or parsed.netloc)


def split_page_targets(targets: list[str]) -> tuple[list[str], str | None]:
    if len(targets) > 1 and not is_url_like(targets[-1]):
        return targets[:-1], targets[-1]
    return targets, None


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export one or more Confluence pages by URL with confluence-markdown-exporter."
    )
    parser.add_argument(
        "page_targets",
        nargs="+",
        help="One or more Confluence page URLs to export, optionally followed by an output path.",
    )
    parser.add_argument(
        "--output-path",
        help="Optional one-off export output path override. Does not persist to cme config.",
    )
    add_export_args(parser)
    args = parser.parse_args(argv)
    args.page_urls, positional_output_path = split_page_targets(args.page_targets)
    if positional_output_path:
        if args.output_path:
            parser.error("Use either a trailing output path or --output-path, not both.")
        args.output_path = positional_output_path
    return args


def validate_same_site(urls: list[str]) -> str:
    """Ensure all URLs belong to the same site and return the common base URL."""
    base_urls = {canonicalize_base_url(u) for u in urls}
    if len(base_urls) > 1:
        raise RuntimeError(
            f"All page URLs must belong to the same Confluence site. "
            f"Found multiple sites: {', '.join(sorted(base_urls))}"
        )
    return base_urls.pop()


def main() -> int:
    args = parse_args()
    python_path = ensure_python_preflight()
    cme_path, cme_status, pipx_status = ensure_cme_available()
    config_path = resolve_config_path(args.config_path, cme_path)
    config_data = load_json(config_path)

    base_url = validate_same_site(args.page_urls)
    require_auth(config_data, base_url)
    output_path = effective_output_path(config_data, args.output_path)

    print_preflight(python_path, pipx_status, cme_status, cme_path, config_path, base_url)
    print(f"Page count: {len(args.page_urls)}")
    for url in args.page_urls:
        print(f"  {url}")
    print(f"Effective output path: {output_path}")
    print_export_flags(args)
    if args.dry_run:
        print("Export command: skipped (dry-run mode)")
        return 0

    run_cme_and_report(
        cme_path,
        ["pages", *args.page_urls],
        build_export_env(args, config_path=config_path, output_path=output_path),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
