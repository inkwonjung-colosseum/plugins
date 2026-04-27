# Confluence Retrieval

Use this reference before `plan-draft` makes factual claims from local Confluence exports.

## Source Selection

1. Open `.confluence-index/registry.json`.
2. Choose the relevant source by `source_id`, `display_path`, `file_count`, and `updated_at`.
3. Open `.confluence-index/sources/<source-id>/source-index.jsonl`.
4. Use `.confluence-index/sources/<source-id>/tree.md` to understand hierarchy.
5. Select the smallest relevant source files. Do not load a whole exported space.
6. Read raw exported Markdown before making claims.

`.confluence-index/` is retrieval metadata only. Treat local exported Markdown as a read-only snapshot of Confluence.

## Filtering Rules

- Prefer `status: current` over `draft`; use `archive` only as historical context.
- Prefer source types in this order when topic relevance is similar: `policy`, `feature-spec`, `prd`, `meeting-note`.
- For recent decisions, inspect Daily Sync or Weekly Sync only after the domain policy/design files are identified.
- If index metadata and raw Markdown disagree, trust the raw exported Markdown and mention the mismatch only when it affects the draft.

## Draft Evidence Rules

- Cite or name the source documents used in the draft's related-documents section.
- Do not invent page IDs from file names. Use `confluence/confluence-lock.json` when a page ID is needed.
- If a needed fact is absent from the selected files, ask the user one focused question or mark it `[미정]`.
- If a claim is useful but not confirmed by selected source files, prefix it with `[가정]`.
