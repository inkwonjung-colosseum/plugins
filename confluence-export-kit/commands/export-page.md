---
description: Export one or more Confluence pages by URL with Confluence Export Kit.
---

# Export Page

Export one or more Confluence pages by URL with `cme pages`.

## Usage

```text
/confluence-export-kit:export-page <page-url> [<page-url2> ...] [--output-path <path>]
```

- `<page-url>` — one or more required Confluence page URLs (all must be same site)
- `--output-path <path>` — optional one-off output override
- `--skip-unchanged` — skip pages matching the lockfile (incremental)
- `--cleanup-stale` — remove local files for deleted/moved pages
- `--jira-enrichment` — include Jira issue summaries in exported Markdown
- `--dry-run` — validate auth and config without running the export

Auth must already be configured for the site extracted from the page URLs.

See `skills/export-page/SKILL.md` for runtime rules and response format.
