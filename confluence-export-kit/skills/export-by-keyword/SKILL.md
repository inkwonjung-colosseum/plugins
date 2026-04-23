---
name: export-by-keyword
description: Export all Confluence pages that match a keyword by searching title and text, then passing the matched page URLs to cme pages.
---

# Export By Keyword

Search Confluence pages by keyword and export only the matched pages with `cme pages`.

## Invocation

Primary usage:

```text
/confluence-export-kit:export-by-keyword <keyword>
```

Optional output override:

```text
/confluence-export-kit:export-by-keyword <keyword> <output-path>
```

Limit search to a specific space:

```text
/confluence-export-kit:export-by-keyword <keyword> --space-key <SPACEKEY>
```

Preview matched pages without exporting:

```text
/confluence-export-kit:export-by-keyword <keyword> --dry-run
```

## Rules

1. Treat `$ARGUMENTS[0]` as the keyword or phrase to search.
2. Treat `$ARGUMENTS[1]` as an optional export output path override.
3. Default target is `CONFLUENCE_EXPORT_KIT_BASE_URL`, then `https://colosseum.atlassian.net`. Override via `--site`.
4. Before export, validate that Python, `pip`, `pipx`, and `cme` are usable.
5. Read the `cme` config file and verify that the fixed site already has a configured `auth.confluence` entry with both `username` and `api_token`.
6. If auth is missing or incomplete, stop and tell the user to run:

```text
/confluence-export-kit:set-api-key <api-key> <email>
```

7. Search Confluence with CQL against both `title` and `text`.
8. If `--space-key <SPACEKEY>` is provided, add `and space = "<SPACEKEY>"` to the CQL query to restrict search to that space.
9. If `--dry-run` is set, print the matched page URLs and stop without running the export.
10. Export only the matched pages. Do not export descendants.
11. If an output path was supplied, apply it only for this export via environment override. Do not persistently rewrite the user's `cme` config.
12. `--skip-unchanged` skips pages whose version matches the lockfile (incremental export).
13. `--cleanup-stale` removes local files for pages deleted or moved in Confluence.
14. `--jira-enrichment` fetches Jira issue summaries and includes them in the exported Markdown.
15. Do not print stored secrets.

## Execution

If no keyword argument was provided, stop and tell the user to run:

```text
/confluence-export-kit:export-by-keyword <keyword> [output-path] [--space-key <KEY>] [--dry-run]
```

Otherwise run the helper script in this skill directory:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/export_by_keyword.py" "<keyword>" ["<output-path>"] [--space-key "<SPACEKEY>"] [--dry-run]
```

## Response Format

After the script finishes:

- report Python/pipx/cme preflight status
- report the Confluence site used
- confirm that auth was already configured
- report the keyword searched and any space key filter applied
- report how many pages matched
- if dry-run: list all matched URLs and note that export was skipped
- if not dry-run: report the effective export output path and confirm export completed
