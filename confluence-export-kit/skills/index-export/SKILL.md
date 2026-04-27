---
name: index-export
description: "Index local Markdown files that were already exported from Confluence. Usage: /confluence-export-kit:index-export <export-path> [--source-id <id>] [--index-root <path>] [--no-agent-rules] [--agent-files <file> ...]"
argument-hint: "<export-path> [--source-id <id>] [--index-root <path>] [--no-agent-rules] [--agent-files <file> ...]"
---

# Index Export

Index local Markdown files that were already exported from Confluence. This skill creates a local `.confluence-index/` and can install Reading Rule blocks into `AGENTS.md` and `CLAUDE.md`.

It does not fetch, create, or update remote Confluence or Jira content.

## Invocation

Claude Code:

```text
/confluence-export-kit:index-export <export-path>
/confluence-export-kit:index-export <export-path> --source-id <id>
/confluence-export-kit:index-export <export-path> --no-agent-rules
/confluence-export-kit:index-export <export-path> --agent-files AGENTS.md CLAUDE.md
```

Codex:

```text
$index-export <export-path>
$index-export <export-path> --source-id <id>
$index-export <export-path> --no-agent-rules
$index-export <export-path> --agent-files AGENTS.md CLAUDE.md
```

## Rules

1. Treat `<export-path>` as a local folder containing Markdown files already exported from Confluence.
2. Do not run `cme`, call Confluence, call Jira, or mutate the exported source files.
3. Create or update `.confluence-index/sources/<source-id>/source-index.jsonl`, `tree.md`, `stats.md`, and `log.md`.
4. Create or update root `.confluence-index/registry.json`, `tree.md`, `stats.md`, and `log.md`.
5. Default `<source-id>` to the export folder basename in kebab-case.
6. Support repeated indexing of multiple export folders by keeping each source under `.confluence-index/sources/<source-id>/`.
7. If a `<source-id>` already points to a different export path, stop and tell the user to pass a different `--source-id`.
8. Unless `--no-agent-rules` is passed, add or update managed Reading Rule blocks in `AGENTS.md` and `CLAUDE.md`.
9. If `--agent-files <file> [<file> ...]` is passed, install Reading Rule blocks into those files instead of the default `AGENTS.md` and `CLAUDE.md`.
10. Only replace content between `confluence-export-kit:reading-rule:start` and `confluence-export-kit:reading-rule:end`; preserve all other file content.

## Execution

Run the matching helper script under this skill's `scripts/` directory with the user-supplied arguments. No extra setup is performed.

## Response Format

After the script finishes:

- report the source ID
- report the number of Markdown files indexed
- report the index root and source index path
- report whether Reading Rule installation was completed or skipped
- if the command failed because of a source ID conflict, tell the user which `--source-id` to change
