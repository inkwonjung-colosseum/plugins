---
name: xstate-graph
description: "Convert an XState v5 machine to a diagram in any of 14 graph formats (Mermaid, DOT, GraphML, etc.). Use when visualizing, diagramming, or documenting a state machine."
---
# XState Graph (multi-format visualizer)

Convert an XState v5 machine to a graph and export to any of 14 formats. Use when the user wants to visualize, diagram, document, or feed a machine into a graph tool.

All emittable: Adjacency List · Cytoscape · d2 · D3 · DOT · Edge List · ELK · GEXF · GML · GraphML · JGF · Mermaid · TGF · xyflow.

## Step 0 — let the USER pick the format (do this first)

Unless the user already named a format, ask with `AskUserQuestion`. Show the **3 primary formats** as options; the auto "Other" slot carries the remaining 11 via free text. Never silently default.

Question "어떤 포맷으로 내보낼까요?" — options:

1. **Mermaid** — docs / Markdown / Confluence / GitHub. Zero-tooling inline render. (recommended default)
2. **xyflow** — interactive React Flow graph inside a web app.
3. **GraphML** — analysis / handoff to Gephi, yEd, networkx.

"Other" accepts: `DOT, d2, Cytoscape, ELK, D3, GEXF, GML, JGF, Adjacency List, Edge List, TGF` (case-insensitive → map to the matching writer). Unknown input → say so, offer the closest match.

Why these 3: each is the best pick of a distinct use-case lens (docs, interactive, analysis); the other 11 stay one keystroke away without crowding the menu.

## Step 1 — extract once

`toDirectedGraph(machine)` from `@xstate/graph`, walked into a portable `{nodes, edges}` shape. Path views use `getShortestPaths`/`getSimplePaths`. Extraction code: `references/extract.md`.

## Step 2 — serialize to the chosen format

Pick the writer for the format. All 14 format shapes, "best for" guidance, and code snippets: `references/formats.md`.

## Rules

- One extraction, many serializers — never re-walk the machine per format.
- Escape labels per target (quotes for DOT/GraphML; no raw newlines in Mermaid labels).
- Nested states: prefix child ids with the parent (`parent.child`) so ids stay unique across formats.
- Large machines: flat formats (Edge/Adjacency List) lose hierarchy — prefer Mermaid composite states or ELK for layout.
