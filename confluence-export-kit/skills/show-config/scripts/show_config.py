#!/usr/bin/env python3
"""Show the current confluence-markdown-exporter config via cme config list."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))

from scripts.cme_runtime import run_command


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Show the current confluence-markdown-exporter configuration."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output config as JSON instead of the default human-readable format.",
    )
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args()

    cmd = ["cme", "config", "list"]
    if args.json:
        cmd += ["-o", "json"]

    result = run_command(cmd)

    print("--- cme config list ---")
    output = result.stdout.strip()
    if output:
        print(output)

    stderr = result.stderr.strip()
    if stderr:
        print("--- cme stderr ---")
        print(stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
