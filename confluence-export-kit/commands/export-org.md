---
description: Export all spaces and pages under a Confluence organization with Confluence Export Kit.
---

# Export Org

Export every space and page under a Confluence instance with `cme orgs`.

## Usage

```text
/confluence-export-kit:export-org <org-url> [output-path]
```

- `<org-url>` — required Confluence instance root URL (e.g. `https://company.atlassian.net`)
- `[output-path]` — optional one-off output override
- `--skip-unchanged` — skip pages matching the lockfile (incremental)
- `--cleanup-stale` — remove local files for deleted/moved pages
- `--jira-enrichment` — include Jira issue summaries in exported Markdown
- `--dry-run` — validate auth and config without running the export

Auth must already be configured for the site extracted from the org URL.

See `skills/export-org/SKILL.md` for runtime rules and response format.
