---
description: Export a Confluence page and all descendants with Confluence Export Kit.
---

# Export Page Tree

Export one Confluence page and every descendant page beneath it with `cme pages-with-descendants`.

## Usage

```text
/confluence-export-kit:export-page-tree <page-url> [output-path]
```

- `<page-url>` — required Confluence page URL
- `[output-path]` — optional one-off output override
- `--skip-unchanged` — skip pages matching the lockfile (incremental)
- `--cleanup-stale` — remove local files for deleted/moved pages
- `--jira-enrichment` — include Jira issue summaries in exported Markdown
- `--dry-run` — validate auth and config without running the export

Auth must already be configured for the site extracted from the page URL.

See `skills/export-page-tree/SKILL.md` for runtime rules and response format.
