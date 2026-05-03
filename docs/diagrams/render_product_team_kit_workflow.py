#!/usr/bin/env python3
"""Render product-team-kit workflow diagrams from a shared JSON source."""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
SOURCE_PATH = ROOT / "product-team-kit-workflow.source.json"
GENERATED_NOTICE = (
    "Generated from product-team-kit-workflow.source.json by "
    "render_product_team_kit_workflow.py. Do not edit directly."
)


def escape(value: str) -> str:
    return html.escape(value, quote=True)


def load_source() -> dict[str, Any]:
    return json.loads(SOURCE_PATH.read_text(encoding="utf-8"))


def text_block(
    lines: list[str],
    x: float,
    y: float,
    *,
    title_class: str = "title",
    line_class: str = "sub",
    anchor: str = "middle",
) -> list[str]:
    output = [
        f'<text class="{title_class}" x="{x:g}" y="{y:g}" text-anchor="{anchor}">{escape(lines[0])}</text>'
    ]
    for index, line in enumerate(lines[1:], start=1):
        output.append(
            f'<text class="{line_class}" x="{x:g}" y="{y + (index * 17):g}" text-anchor="{anchor}">{escape(line)}</text>'
        )
    return output


def render_node(node: dict[str, Any], definitions: dict[str, Any]) -> list[str]:
    definition = definitions[node["ref"]]
    kind = node["kind"]
    cls = node["class"]
    x = node["x"]
    y = node["y"]
    w = node["w"]
    h = node["h"]
    cx = x + (w / 2)
    cy = y + (h / 2)
    lines = [definition["title"], *definition["lines"]]
    start_y = cy - ((len(lines) - 1) * 8) + 5

    if kind == "decision":
        points = f"{cx:g},{y:g} {x + w:g},{cy:g} {cx:g},{y + h:g} {x:g},{cy:g}"
        output = [f'<polygon class="{cls}" points="{points}"/>']
    else:
        rx = h / 2 if kind == "pill" else 8
        output = [f'<rect class="{cls}" x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx:g}"/>']
    output.extend(text_block(lines, cx, start_y))
    return output


def render_label(edge: dict[str, Any]) -> str:
    label = edge["label"]
    width = edge.get("label_w", max(46, len(label) * 7))
    x = edge["label_x"]
    y = edge["label_y"]
    return "\n".join(
        [
            f'<rect class="edge-label-bg" x="{x - (width / 2):g}" y="{y - 12:g}" width="{width:g}" height="18" rx="3"/>',
            f'<text class="edge-label" x="{x:g}" y="{y:g}" text-anchor="middle">{escape(label)}</text>',
        ]
    )


def render_edge(edge: dict[str, Any]) -> list[str]:
    cls = "line-accent" if edge.get("accent") else "line"
    if edge.get("dash"):
        cls = "line-dash"
    output = [f'<path class="{cls}" d="{escape(edge["d"])}"/>']
    if "label" in edge:
        output.append(render_label(edge))
    return output


def render_notes(notes: list[dict[str, Any]]) -> list[str]:
    output: list[str] = []
    for note in notes:
        for index, line in enumerate(note["lines"]):
            output.append(
                f'<text class="note" x="{note["x"]:g}" y="{note["y"] + (index * 20):g}">{escape(line)}</text>'
            )
    return output


def render_lanes(lanes: list[dict[str, Any]]) -> list[str]:
    output: list[str] = []
    for lane in lanes:
        output.append(
            f'<rect class="lane" x="{lane["x"]:g}" y="{lane["y"]:g}" width="{lane["w"]:g}" height="{lane["h"]:g}" rx="10"/>'
        )
        output.append(
            f'<text class="lane-label" x="{lane["x"] + 22:g}" y="{lane["y"] + 28:g}">{escape(lane["label"])}</text>'
        )
    return output


def render_svg(view: dict[str, Any], definitions: dict[str, Any]) -> str:
    svg = view["svg"]
    width = svg["width"]
    height = svg["height"]
    parts = [
        f'<svg viewBox="0 0 {width:g} {height:g}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">',
        f'  <title id="title">{escape(svg["title"])}</title>',
        f'  <desc id="desc">{escape(svg["desc"])}</desc>',
        "  <defs>",
        '    <marker id="arrow" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">',
        '      <polygon points="0 0, 9 3.5, 0 7" fill="#4f5d75"/>',
        "    </marker>",
        '    <marker id="arrow-accent" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">',
        '      <polygon points="0 0, 9 3.5, 0 7" fill="#eb6c36"/>',
        "    </marker>",
        "  </defs>",
        f'  <rect width="{width:g}" height="{height:g}" fill="#f5f5f5"/>',
    ]
    for item in render_lanes(view.get("lanes", [])):
        parts.append(f"  {item}")
    for edge in view["edges"]:
        for item in render_edge(edge):
            parts.append(f"  {item}")
    for node in view["nodes"]:
        for item in render_node(node, definitions):
            parts.append(f"  {item}")
    for item in render_notes(view.get("notes", [])):
        parts.append(f"  {item}")
    parts.append("</svg>")
    return "\n".join(parts)


def render_html(view: dict[str, Any], definitions: dict[str, Any]) -> str:
    svg = view["svg"]
    summary = f'\n    <p class="summary">{escape(view["summary"])}</p>' if view.get("summary") else ""
    return f"""<!DOCTYPE html>
<!-- {GENERATED_NOTICE} -->
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(view["document_title"])}</title>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --paper: #f5f5f5;
      --ink: #2d3142;
      --muted: #4f5d75;
      --soft: #7a8399;
      --rule: rgba(45,49,66,0.13);
      --accent: #eb6c36;
      --warn: #b84a2b;
      --accent-tint: rgba(235,108,54,0.08);
      --warn-tint: rgba(184,74,43,0.08);
      --sans: 'Geist', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
      --serif: 'Instrument Serif', Georgia, serif;
      --mono: 'Geist Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
    }}

    body {{
      min-height: 100vh;
      background: var(--paper);
      color: var(--ink);
      font-family: var(--sans);
      padding: 44px 28px;
    }}

    main {{
      width: min(100%, 1260px);
      margin: 0 auto;
      overflow-x: auto;
    }}

    .eyebrow {{
      color: var(--muted);
      font-family: var(--mono);
      font-size: 12px;
      font-weight: 500;
      letter-spacing: 0;
      margin-bottom: 8px;
      text-transform: uppercase;
    }}

    h1 {{
      color: var(--ink);
      font-family: var(--serif);
      font-size: clamp(30px, 3vw, 38px);
      font-weight: 400;
      letter-spacing: 0;
      line-height: 1.12;
      margin-bottom: 10px;
    }}

    .summary {{
      color: var(--muted);
      font-size: 14px;
      line-height: 1.55;
      margin-bottom: 24px;
      max-width: 960px;
    }}

    svg {{
      display: block;
      min-width: {svg["min_width"]:g}px;
      width: 100%;
      height: auto;
    }}

    .lane {{ fill: rgba(45,49,66,0.025); stroke: rgba(45,49,66,0.10); stroke-width: 1; }}
    .lane-label {{ fill: var(--soft); font-family: var(--mono); font-size: 10px; font-weight: 500; text-transform: uppercase; }}
    .node {{ fill: #ffffff; stroke: var(--ink); stroke-width: 1; }}
    .node-soft {{ fill: rgba(45,49,66,0.02); stroke: rgba(45,49,66,0.25); stroke-width: 1; stroke-dasharray: 4 3; }}
    .node-accent {{ fill: var(--accent-tint); stroke: var(--accent); stroke-width: 1.2; }}
    .node-store {{ fill: rgba(45,49,66,0.05); stroke: var(--muted); stroke-width: 1; }}
    .node-warn {{ fill: var(--warn-tint); stroke: var(--warn); stroke-width: 1.15; stroke-dasharray: 5 3; }}
    .title {{ fill: var(--ink); font-family: var(--sans); font-size: 13px; font-weight: 600; }}
    .sub {{ fill: var(--muted); font-family: var(--mono); font-size: 8.5px; }}
    .note {{ fill: var(--muted); font-family: var(--sans); font-size: 11px; }}
    .line {{ fill: none; stroke: var(--muted); stroke-width: 1.25; marker-end: url(#arrow); }}
    .line-accent {{ fill: none; stroke: var(--accent); stroke-width: 1.35; marker-end: url(#arrow-accent); }}
    .line-dash {{ fill: none; stroke: var(--muted); stroke-width: 1.2; stroke-dasharray: 5 4; marker-end: url(#arrow); }}
    .edge-label-bg {{ fill: var(--paper); }}
    .edge-label {{ fill: var(--muted); font-family: var(--mono); font-size: 8px; font-weight: 500; }}
  </style>
</head>
<body>
  <main>
    <p class="eyebrow">{escape(view["eyebrow"])}</p>
    <h1>{escape(view["heading"])}</h1>{summary}

{render_svg(view, definitions)}
  </main>
</body>
</html>
"""


def render_all(source: dict[str, Any]) -> dict[Path, str]:
    definitions = source["workflow"]["nodes"]
    return {
        ROOT / view["output"]: render_html(view, definitions)
        for view in source["views"].values()
    }


def write_outputs(outputs: dict[Path, str]) -> None:
    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT.parent.parent)}")


def check_outputs(outputs: dict[Path, str]) -> int:
    failures: list[str] = []
    for path, expected in outputs.items():
        actual = path.read_text(encoding="utf-8") if path.exists() else None
        if actual != expected:
            failures.append(str(path.relative_to(ROOT.parent.parent)))
        else:
            print(f"OK {path.relative_to(ROOT.parent.parent)}")
    if failures:
        print("Out of date generated diagram(s):", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        print("Run: python3 docs/diagrams/render_product_team_kit_workflow.py --write", file=sys.stderr)
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="Regenerate HTML diagrams")
    mode.add_argument("--check", action="store_true", help="Verify HTML diagrams are current")
    args = parser.parse_args()

    source = load_source()
    outputs = render_all(source)
    if args.write:
        write_outputs(outputs)
        return 0
    return check_outputs(outputs)


if __name__ == "__main__":
    raise SystemExit(main())
