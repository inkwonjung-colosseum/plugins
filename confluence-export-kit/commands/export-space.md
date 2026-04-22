---
description: Export all pages in a Confluence space with Confluence Export Kit.
---

# Export Space

Export every page in a Confluence space with `cme spaces`.

## Usage

```text
/confluence-export-kit:export-space <space-url> [output-path]
```

- `<space-url>` — required Confluence space URL (e.g. `https://company.atlassian.net/wiki/spaces/SPACEKEY`)
- `[output-path]` — optional one-off output override
- `--skip-unchanged` — skip pages matching the lockfile (incremental)
- `--cleanup-stale` — remove local files for deleted/moved pages
- `--jira-enrichment` — include Jira issue summaries in exported Markdown
- `--dry-run` — validate auth and config without running the export

Auth must already be configured for the site extracted from the space URL.

See `skills/export-space/SKILL.md` for runtime rules and response format.
