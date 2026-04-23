---
name: export-org
description: Export all spaces and pages under a Confluence organization with confluence-markdown-exporter.
---

# Export Org

Export every space and page under a Confluence instance with `cme orgs`.

## Invocation

Primary usage:

```text
/confluence-export-kit:export-org <org-url>
```

Optional output override:

```text
/confluence-export-kit:export-org <org-url> <output-path>
```

## Rules

1. Treat `$ARGUMENTS[0]` as the Confluence instance root URL (e.g. `https://company.atlassian.net`).
2. Treat `$ARGUMENTS[1]` as an optional export output path override.
3. Before export, validate that Python, `pip`, `pipx`, and `cme` are usable.
4. Extract the base site from the org URL (`scheme://netloc`) and verify that a configured `auth.confluence` entry with both `username` and `api_token` exists for that site.
5. If auth is missing or incomplete, stop and tell the user to run:

```text
/confluence-export-kit:set-api-key <api-key> <email>
```

6. Do not print the stored API token.
7. Run `cme orgs <org-url>` once auth is confirmed.
8. If an output path was supplied, apply it only for this export via environment override. Do not persistently rewrite the user's `cme` config.
9. `--skip-unchanged` / `--no-skip-unchanged` — skips pages whose version matches the lockfile (incremental export). **Default: on.**
10. `--cleanup-stale` / `--no-cleanup-stale` — removes local files for pages deleted or moved in Confluence. **Default: on.**
11. `--jira-enrichment` fetches Jira issue summaries and includes them in the exported Markdown.
12. `--dry-run` validates auth and config without running the export; prints "skipped" and returns.

## Execution

If no org URL argument was provided, stop and tell the user to run:

```text
/confluence-export-kit:export-org <org-url> [output-path]
```

Otherwise run the helper script in this skill directory:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/export_org.py" "<org-url>" ["<output-path>"]
```

## Response Format

After the script finishes:

- report Python/pipx/cme preflight status
- report which Confluence site was matched
- confirm that auth was already configured
- report the org URL being exported
- report the effective export output path
- confirm that the org export command completed
