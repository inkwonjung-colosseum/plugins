---
description: Export all Confluence pages that have a specific label with Confluence Export Kit.
---

# Export By Label

Search Confluence pages by label and export only the matched pages with `cme pages`.

## Usage

```text
/confluence-export-kit:export-by-label <label> [output-path]
```

- `<label>` — required Confluence label name
- `[output-path]` — optional one-off output override
- `--space-key <SPACEKEY>` — limit search to a specific space
- `--dry-run` — preview matched URLs without exporting
- `--skip-unchanged` — skip pages matching the lockfile (incremental)
- `--cleanup-stale` — remove local files for deleted/moved pages
- `--jira-enrichment` — include Jira issue summaries in exported Markdown

Auth must already be configured for the target site.

See `skills/export-by-label/SKILL.md` for runtime rules and response format.
