---
name: help
description: Show a concise help summary for Confluence Export Kit.
---

# Help

Provide a concise operational help summary for `confluence-export-kit`.

## Purpose

Explain the plugin's current command surface without implying that every upstream `confluence-markdown-exporter` feature is directly exposed.

## Coverage

1. State that this is an export-only Confluence plugin.
2. Group commands under these buckets:
   - Setup: `/confluence-export-kit:set-api-key`, `/confluence-export-kit:set-output-path`
   - Export: `/confluence-export-kit:export-org`, `/confluence-export-kit:export-space`, `/confluence-export-kit:export-page-tree`, `/confluence-export-kit:export-page`
   - Search export: `/confluence-export-kit:export-by-keyword`, `/confluence-export-kit:export-by-label`
   - Config: `/confluence-export-kit:config-show`
3. Mention these common export flags:
   - `--skip-unchanged`
   - `--cleanup-stale`
   - `--jira-enrichment`
   - `--dry-run`
   - `--max-workers N`
4. Include a short quick start sequence that begins with:

```text
/confluence-export-kit:set-api-key <api-key> <email>
```

5. Mention the explicit non-goals:
   - Jira write workflows
   - planning briefs
   - general-purpose CQL console
   - interactive `cme config` menu
6. If helpful, note that each command's detailed runtime rules live in its matching `skills/*/SKILL.md`.

## Response Format

- Start with one sentence describing the plugin scope.
- Add a `Quick Start` section with 3 numbered steps.
- Add a `Commands` section with flat bullets.
- Add a `Common Flags` section with flat bullets.
- Add a `Non-goals` section with flat bullets.
- Keep the answer concise and operational.
