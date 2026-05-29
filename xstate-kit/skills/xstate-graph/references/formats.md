# 14 output formats (Step 2 detail)

All writers consume the `{nodes, edges}` shape from `references/extract.md`.

| Format | Shape / how to emit | Best for |
|--------|--------------------|----------|
| **Mermaid** | `stateDiagram-v2\n` + `s1 --> s2 : EVENT` lines | docs, Confluence, README, GitHub |
| **DOT** | `digraph { s1 -> s2 [label="EVENT"] }` | Graphviz render, print/PDF |
| **d2** | `s1 -> s2: EVENT` (d2lang) | modern auto-layout diagrams |
| **Cytoscape** | `{ elements: { nodes:[{data:{id,label}}], edges:[{data:{source,target,label}}] } }` | interactive web graph (cytoscape.js) |
| **xyflow** | `{ nodes:[{id,data:{label},position}], edges:[{id,source,target,label}] }` | React Flow editors |
| **ELK** | `{ id:'root', children:[{id,...}], edges:[{id,sources,targets}] }` | layered auto-layout engine |
| **D3** | `{ nodes:[{id}], links:[{source,target}] }` | force / custom d3 viz |
| **GraphML** | XML `<graph>` w/ `<node id>` `<edge source target>` | yEd, Gephi import |
| **GEXF** | XML `<gexf><graph>` nodes/edges | Gephi (rich attrs / time) |
| **GML** | `graph [ node [ id .. ] edge [ source .. ] ]` | yEd, igraph |
| **JGF** | JSON Graph Format `{graph:{nodes:{...},edges:[...]}}` | tool-agnostic JSON interchange |
| **Adjacency List** | `s1: [s2, s3]` per line | quick human scan, BFS/DFS input |
| **Edge List** | `s1 s2` per line (+ optional weight/label) | networkx, minimal interchange |
| **TGF** | id-label lines, `#`, then `src tgt label` lines | yEd Trivial Graph Format |

## Snippets

Mermaid:
```ts
const mermaid = 'stateDiagram-v2\n' +
  edges.map((e) => `  ${e.source} --> ${e.target}: ${e.label}`).join('\n');
```

DOT:
```ts
const dot = `digraph G {\n` +
  edges.map((e) => `  "${e.source}" -> "${e.target}" [label="${e.label}"];`).join('\n') + '\n}';
```

d2:
```ts
const d2 = edges.map((e) => `${e.source} -> ${e.target}: ${e.label}`).join('\n');
```

TGF:
```ts
const tgf = nodes.map((n) => `${n.id} ${n.label}`).join('\n') +
  '\n#\n' +
  edges.map((e) => `${e.source} ${e.target} ${e.label}`).join('\n');
```

Edge List:
```ts
const edgeList = edges.map((e) => `${e.source} ${e.target}`).join('\n');
```

GraphML (escape `& < >` in labels):
```ts
const gml = `<?xml version="1.0"?>\n<graphml><graph edgedefault="directed">\n` +
  nodes.map((n) => `  <node id="${n.id}"/>`).join('\n') + '\n' +
  edges.map((e) => `  <edge source="${e.source}" target="${e.target}"/>`).join('\n') +
  '\n</graph></graphml>';
```

## Choosing a default

No target given → **Mermaid** (inline render in Markdown/Confluence/GitHub, zero tooling). Recommend **DOT** for print-quality static layout, **Cytoscape/xyflow** for an interactive in-app graph, **GraphML/GEXF** for handoff to Gephi/yEd analysis.

## Escaping & scale

- Escape labels per target: quotes for DOT/GraphML, no raw newlines in Mermaid labels.
- Large machines: flat formats (Edge/Adjacency List) lose hierarchy — prefer Mermaid composite states or feed ELK for layout.
