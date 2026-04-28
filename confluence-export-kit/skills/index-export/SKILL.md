---
name: index-export
description: "Background workflow for indexing local Markdown files that were already exported from Confluence; export skills run it automatically after successful cme export."
argument-hint: "<export-path> [--source-id <id>] [--index-root <path>] [--no-agent-rules] [--agent-files <file> ...]"
---

# Index Export

Index local Markdown files that were already exported from Confluence. This skill creates a local `.confluence-index/` and can install Reading Rule blocks into `AGENTS.md` and `CLAUDE.md`.

It does not fetch, create, or update remote Confluence or Jira content.

## Invocation

Claude Code:

This skill does not declare a visibility override in its front matter. Treat it as a background workflow: export skills run this helper automatically after successful `cme` export, and Claude can still load the skill when local export indexing guidance is relevant.

Codex:

Keep `agents/openai.yaml` set to `policy.allow_implicit_invocation: false` so this skill is not auto-injected for ordinary user requests. Export scripts still invoke the helper script automatically after successful `cme` export.

## Rules

1. Treat `<export-path>` as a local folder containing Markdown files already exported from Confluence.
2. Do not run `cme`, call Confluence, call Jira, or mutate the exported source files.
3. Create or update `.confluence-index/sources/<source-id>/source-index.jsonl`, `tree.md`, `stats.md`, and `log.md`.
4. Create or update root `.confluence-index/registry.json`, `tree.md`, `stats.md`, and `log.md`.
5. Default `<source-id>` to the export folder basename in kebab-case.
6. Support repeated indexing of multiple export folders by keeping each source under `.confluence-index/sources/<source-id>/`.
7. If a `<source-id>` already points to a different export path, stop and tell the user to pass a different `--source-id`.
8. Prefer scalar front matter metadata for `title`, `status`, and `source_type` / `type`; use headings and path-based fallback when metadata is absent.
9. Append to `.confluence-index/**/log.md`; do not rewrite existing logs just to add a new entry.
10. Unless `--no-agent-rules` is passed, add or update managed Reading Rule blocks in `AGENTS.md` and `CLAUDE.md`.
11. If `--agent-files <file> [<file> ...]` is passed, install Reading Rule blocks into those files instead of the default `AGENTS.md` and `CLAUDE.md`.
12. Only replace content between `confluence-export-kit:reading-rule:start` and `confluence-export-kit:reading-rule:end`; preserve all other file content.
13. The Reading Rule must state that Confluence is the source of truth and local exported Markdown is a read-only snapshot.
14. The Reading Rule must prohibit derived wiki, entity, concept, summary, and product-context pages unless a user explicitly asks for a draft-only artifact.
15. The Reading Rule must treat planning outputs as draft-only until a human reflects them back into Confluence.
16. Do not add a Claude-specific front matter visibility override; keep the background-workflow intent in the description and invocation guidance.
17. For Codex, keep `agents/openai.yaml` set to `policy.allow_implicit_invocation: false`; export skills should be the normal path that runs this helper.

## Execution

Run the matching helper script under this skill's `scripts/` directory with the user-supplied arguments. No extra setup is performed.

## Response Format

After the script finishes:

- report the source ID
- report the number of Markdown files indexed
- report the index root and source index path
- report whether Reading Rule installation was completed or skipped
- if the command failed because of a source ID conflict, tell the user which `--source-id` to change
