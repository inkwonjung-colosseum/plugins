---
name: export-page-tree
description: Export a Confluence page and all descendant pages with confluence-markdown-exporter after verifying that auth is already configured.
---

# Export Page Tree

Export one Confluence page and every child page beneath it with `cme pages-with-descendants`.

## Invocation

Primary usage:

```text
/confluence-export-kit:export-page-tree <page-url>
```

Optional output override:

```text
/confluence-export-kit:export-page-tree <page-url> <output-path>
```

## Rules

1. Treat `$ARGUMENTS[0]` as the Confluence page URL.
2. Treat `$ARGUMENTS[1]` as an optional export output path override.
3. Before export, validate that Python, `pip`, `pipx`, and `cme` are usable.
4. Read the `cme` config file and verify that the page URL's base site already has a configured `auth.confluence` entry with both `username` and `api_token`.
5. If auth is missing or incomplete, stop and tell the user to run:

```text
/confluence-export-kit:set-api-key <api-key> <email>
```

6. Do not print the stored API token.
7. Run `cme pages-with-descendants <page-url>` once auth is confirmed.
8. If an output path was supplied, apply it only for this export via environment override. Do not persistently rewrite the user's `cme` config.
9. `--skip-unchanged` skips pages whose version matches the lockfile (incremental export).
10. `--cleanup-stale` removes local files for pages deleted or moved in Confluence.
11. `--jira-enrichment` fetches Jira issue summaries and includes them in the exported Markdown.
12. `--dry-run` validates auth and config without running the export; prints "skipped" and returns.

## Execution

If no page URL argument was provided, stop and tell the user to run:

```text
/confluence-export-kit:export-page-tree <page-url> [output-path]
```

Otherwise run the helper script in this skill directory:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/export_page_tree.py" "<page-url>" ["<output-path>"]
```

## Response Format

After the script finishes:

- report Python/pipx/cme preflight status
- report which Confluence site was matched
- confirm that auth was already configured
- report the effective export output path
- confirm that the page tree export command completed
