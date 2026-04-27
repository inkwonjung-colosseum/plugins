<!-- confluence-export-kit:reading-rule:start -->
## Reading Rule

When working with exported Confluence documents:

1. Treat Confluence as the source of truth.
2. Treat local exported Markdown as a read-only snapshot of that source.
3. Start from `.confluence-index/registry.json` to choose the relevant export source.
4. Then read `.confluence-index/sources/<source-id>/source-index.jsonl`.
5. Use `.confluence-index/sources/<source-id>/tree.md` to understand that source hierarchy.
6. Select the smallest relevant source files.
7. Read raw exported Markdown before making claims.
8. Do not load a whole exported space into context.
9. Treat archive/draft/current documents differently when metadata is available.
10. Do not create or maintain derived wiki, entity, concept, summary, or product-context pages.
11. Treat `.confluence-index/` as retrieval metadata only, not as a source of truth.
12. Treat planning outputs as draft-only until a human reflects them back into Confluence.
<!-- confluence-export-kit:reading-rule:end -->
