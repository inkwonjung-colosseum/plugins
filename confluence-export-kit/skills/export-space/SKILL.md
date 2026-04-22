---
description: Export all pages in a Confluence space with confluence-markdown-exporter. Invoke manually as /confluence-export-kit:export-space <space-url> [output-path].
disable-model-invocation: true
---

# Export Space

Export every page in a Confluence space with `cme spaces`.

## Invocation

Primary usage:

```text
/confluence-export-kit:export-space <space-url>
```

Optional output override:

```text
/confluence-export-kit:export-space <space-url> <output-path>
```

## Rules

1. Treat `$ARGUMENTS[0]` as the Confluence space URL (e.g. `https://company.atlassian.net/wiki/spaces/SPACEKEY`).
2. Treat `$ARGUMENTS[1]` as an optional export output path override.
3. Before export, validate that Python, `pip`, `pipx`, and `cme` are usable.
4. Extract the base site from the space URL (`scheme://netloc`) and verify that a configured `auth.confluence` entry with both `username` and `api_token` exists for that site.
5. If auth is missing or incomplete, stop and tell the user to run:

```text
/confluence-export-kit:set-api-key <api-key> <email>
```

6. Do not print the stored API token.
7. Run `cme spaces <space-url>` once auth is confirmed.
8. If an output path was supplied, apply it only for this export via environment override. Do not persistently rewrite the user's `cme` config.
9. `--skip-unchanged` skips pages whose version matches the lockfile (incremental export).
10. `--cleanup-stale` removes local files for pages deleted or moved in Confluence.
11. `--jira-enrichment` fetches Jira issue summaries and includes them in the exported Markdown.
12. `--dry-run` validates auth and config without running the export; prints "skipped" and returns.

## Execution

If no space URL argument was provided, stop and tell the user to run:

```text
/confluence-export-kit:export-space <space-url> [output-path]
```

Otherwise run the helper script in this skill directory:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/export_space.py" "<space-url>" ["<output-path>"]
```

## Response Format

After the script finishes:

- report Python/pipx/cme preflight status
- report which Confluence site was matched
- confirm that auth was already configured
- report the space URL being exported
- report the effective export output path
- confirm that the space export command completed
