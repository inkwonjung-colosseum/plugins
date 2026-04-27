<!-- confluence-export-kit:reading-rule:start -->
## Reading Rule

When working with exported Confluence documents:

1. Start from `.confluence-index/registry.json` to choose the relevant export source.
2. Then read `.confluence-index/sources/<source-id>/source-index.jsonl`.
3. Use `.confluence-index/sources/<source-id>/tree.md` to understand that source hierarchy.
4. Select the smallest relevant source files.
5. Read raw exported Markdown only when evidence is needed.
6. Do not load a whole exported space into context.
7. Treat archive/draft/current documents differently when metadata is available.
<!-- confluence-export-kit:reading-rule:end -->
