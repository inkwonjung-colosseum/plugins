---
name: dbml-to-mermaid
description: Use when a .dbml file or DBML block needs a Mermaid erDiagram for Confluence, README, or planning docs.
allowed-tools:
  - Read
  - Grep
  - Glob
disable-model-invocation: false
user-invocable: true
---
# dbml-to-mermaid

Convert a DBML schema into a Mermaid `erDiagram` block ready to embed in Confluence, README, dbdocs, or a planning-kit deliverable.

## When to use

- A `.dbml` file or DBML block (`Table`, `Ref:`, `Enum`, `TableGroup`) is in the conversation.
- User asks: "ERD 만들어줘", "mermaid로 그려줘", "Confluence에 붙일 다이어그램", "render this DBML".
- A planning-kit doc needs a schema diagram before `planning-publish-confluence`.

Do NOT use for plain SQL DDL — only DBML syntax. For non-ER diagrams (flow/sequence/state), hand off to `diagram-design`.

## Input handshake

State in one line what is being converted, then proceed:

> DBML: `schemas/order.dbml` (6 tables, 4 refs, 2 enums)
> Target: Mermaid `erDiagram` (single block / grouped by TableGroup)

If grouping is ambiguous, confirm before rendering.

## Output

Produce in order:

1. **Mermaid block** — fenced `mermaid` code block(s). One per `TableGroup` if present, else single block.
2. **Korean caption** (1~2 lines) — PM-readable, business tone matching [[dbml-explain]].
3. **Embed guide** (3 lines max) — Confluence / README / dbdocs targets. Detail in `references/example.md`.
4. **Loss notes** — short bullets: what DBML expresses but Mermaid cannot. Each item: 1 line, reason + alternative.

## Rules

- Table/column names verbatim, preserve `snake_case`.
- Columns → `type name PK|FK|UK` form. Drop system columns (`created_at`, `updated_at`, `deleted_at`, `version`) unless requested.
- Cardinality: `>` → `}o--||`, `<` → `||--o{`, `-` → `||--||`, `<>` → preserve join table.
- Label relations with FK column name in quotes.
- Quote identifiers with characters Mermaid rejects.
- More than 12 tables → suggest split by `TableGroup` or FK cluster.
- Inferred cardinality (no explicit `Ref`) → mark "(추정)" in caption.
- No `classDef` styling unless user requests.
- Korean caption default; English if input is English.
- Mermaid block always fenced, never inline.

## Reference

For a worked example, cardinality mapping table, embed targets detail, and full loss-item list, read `references/example.md`.

## Related

- [[dbml-explain]] — narrative without diagram.
- [[dbml-spec-diff]] — PRD gap diagnosis.
- `planning-publish-confluence` — publish step downstream.
- `diagram-design` — non-ER diagrams.
