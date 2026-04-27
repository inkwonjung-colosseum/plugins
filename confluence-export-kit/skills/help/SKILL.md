---
name: help
description: Show a concise help summary for confluence-export-kit.
---

# Help

Provide a concise operational help summary for `confluence-export-kit`.

## Purpose

Explain the plugin's current command surface without implying that every upstream `confluence-markdown-exporter` feature is directly exposed.

## Coverage

1. State that this is a Confluence export and local export-index plugin that works with both Claude Code and Codex. Clarify that `index-export` only indexes local Markdown files that were already exported from Confluence.
2. Show command invocation for both agents. Claude Code uses `/confluence-export-kit:<skill>`, Codex uses `$<skill>` (per Codex's official plugin spec, which does not support colon-namespaced slash commands). Group commands under these buckets:
   - Setup: `set-config`
   - Export: `export-org`, `export-space`, `export-page-with-descendant`, `export-page`
   - Local index: `index-export`
   - Config: `show-config`

   When listing examples, show both forms, e.g.:
   - Claude Code: `/confluence-export-kit:set-config --api-key <api-key> --email <email>`
   - Codex: `$set-config --api-key <api-key> --email <email>`
3. Mention these common export flags:
   - `--skip-unchanged`
   - `--cleanup-stale`
   - `--jira-enrichment`
   - `--dry-run`
   - `--max-workers N`
4. Include a short quick start sequence that begins with the agent-appropriate form:

```text
# Claude Code
/confluence-export-kit:set-config --api-key <api-key> --email <email> --output-path <path>

# Codex
$set-config --api-key <api-key> --email <email> --output-path <path>
```

5. Mention the explicit non-goals:
   - Jira write workflows
   - remote Confluence write workflows
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
