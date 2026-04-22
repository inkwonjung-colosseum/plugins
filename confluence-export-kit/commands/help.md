---
description: Show usage guidance for Confluence Export Kit.
---

# Confluence Export Kit Help

Confluence Export Kit is an export-only plugin for Confluence auth setup and document export.

## Export Workflow

```text
/confluence-export-kit:set-api-key <api-key> <email>       (one-time auth)
/confluence-export-kit:set-output-path <path>              (optional: set default output dir)
    │
    ├─► /confluence-export-kit:export-org <org-url> [output-path]
    │       exports every space and page under a Confluence instance
    │
    ├─► /confluence-export-kit:export-space <space-url> [output-path]
    │       exports every page in a space
    │
    ├─► /confluence-export-kit:export-page-tree <page-url> [output-path]
    │       exports one page and all descendants
    │
    ├─► /confluence-export-kit:export-page <page-url> [<page-url2> ...] [--output-path <path>]
    │       exports one or more specific pages by URL
    │
    ├─► /confluence-export-kit:export-by-keyword <keyword> [output-path]
    │       searches title + text (CQL), exports only matched pages
    │       options: --space-key <KEY>  limit search to one space
    │                --dry-run          preview matches without exporting
    │
    └─► /confluence-export-kit:export-by-label <label> [output-path]
            searches by Confluence label (CQL), exports only matched pages
            options: --space-key <KEY>  limit search to one space
                     --dry-run          preview matches without exporting
```

## Common Export Flags

All export commands accept these flags:

- `--skip-unchanged` — skip pages whose version matches the lockfile (incremental export)
- `--cleanup-stale` — remove local files for pages deleted or moved in Confluence
- `--jira-enrichment` — include Jira issue summaries in exported Markdown
- `--dry-run` — validate auth and config without running the export
- `--max-workers N` — override the number of parallel export workers

## Commands

- `/confluence-export-kit:help` — show this help message
- `/confluence-export-kit:set-api-key <api-key> <email>` — configure `confluence-markdown-exporter` auth (token validated by default; `--skip-validate` to skip)
- `/confluence-export-kit:set-output-path <path>` — persist the default export output directory to cme config
- `/confluence-export-kit:export-org <org-url> [output-path]` — export all spaces and pages under a Confluence instance
- `/confluence-export-kit:export-space <space-url> [output-path]` — export all pages in a space
- `/confluence-export-kit:export-page-tree <page-url> [output-path]` — export one page and all descendants
- `/confluence-export-kit:export-page <page-url> [<page-url2> ...] [--output-path <path>]` — export specific pages by URL
- `/confluence-export-kit:export-by-keyword <keyword> [output-path] [--space-key <KEY>] [--dry-run]` — search title + text and export matched pages
- `/confluence-export-kit:export-by-label <label> [output-path] [--space-key <KEY>] [--dry-run]` — search by label and export matched pages
- `/confluence-export-kit:config-show [--json]` — display current cme configuration

Detailed runtime behavior lives in `skills/*/SKILL.md`.
