#!/usr/bin/env python3
"""Persist the default export output path in the cme config."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))

from scripts.cme_runtime import ensure_cme_available
from scripts.cme_runtime import ensure_dict
from scripts.cme_runtime import ensure_python_preflight
from scripts.cme_runtime import load_json
from scripts.cme_runtime import normalize_nonempty
from scripts.cme_runtime import resolve_config_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Persist the default export output path in the confluence-markdown-exporter config."
    )
    parser.add_argument(
        "output_path",
        help="Directory path to set as the default export output location.",
    )
    parser.add_argument(
        "--config-path",
        help="Optional explicit path to the confluence-markdown-exporter config file",
    )
    return parser.parse_args()


def write_json_atomic(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        delete=False,
        dir=path.parent,
        prefix=path.name + ".",
        suffix=".tmp",
    ) as tmp:
        json.dump(data, tmp, indent=2)
        tmp.write("\n")
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)


def main() -> int:
    args = parse_args()
    output_path = normalize_nonempty(args.output_path, "Output path")
    python_path = ensure_python_preflight()
    cme_path, cme_status, pipx_status = ensure_cme_available()
    config_path = resolve_config_path(args.config_path, cme_path)
    data = load_json(config_path)

    export_section = ensure_dict(data, "export")
    previous = export_section.get("output_path", "(not set)")
    export_section["output_path"] = output_path

    write_json_atomic(config_path, data)

    print(f"Python executable: {python_path}")
    print(f"Pipx status: {pipx_status}")
    print(f"CME status: {cme_status}")
    print(f"CME executable: {cme_path}")
    print(f"Updated config: {config_path}")
    print(f"Previous output path: {previous}")
    print(f"New output path: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
