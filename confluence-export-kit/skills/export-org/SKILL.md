---
name: export-org
description: "Export all spaces/pages under one or more Confluence orgs. Usage: /confluence-export-kit:export-org <org-url> [<org-url> ...] [output-path]"
argument-hint: "<org-url> [<org-url> ...] [output-path]"
---

# Export Org

Export every space and page under one or more Confluence instances with `cme orgs`.

## Invocation

Claude Code:

```text
/confluence-export-kit:export-org <org-url>
/confluence-export-kit:export-org <org-url> <output-path>
/confluence-export-kit:export-org <org-url> <org-url2> [output-path]
```

Codex:

```text
$export-org <org-url>
$export-org <org-url> <output-path>
$export-org <org-url> <org-url2> [output-path]
```

## Rules

1. Treat the arguments as one or more Confluence instance root URLs (e.g. `https://company.atlassian.net`).
2. If the final argument is not URL-like, treat it as an optional export output path override.
3. Assume `cme`, config, and auth are already available.
4. Do not print the stored API token.
5. Run `cme orgs <org-url> [<org-url2> ...]`.
6. If an output path was supplied, apply it only for this export via environment override. Do not persistently rewrite the user's `cme` config.
7. After `cme orgs` completes, index the effective output path with `index-export`.
8. `--skip-unchanged` / `--no-skip-unchanged` — skips pages whose version matches the lockfile (incremental export). **Default: on.**
9. `--cleanup-stale` / `--no-cleanup-stale` — removes local files for pages deleted or moved in Confluence. **Default: on.**
10. `--jira-enrichment` fetches Jira issue summaries and includes them in the exported Markdown.
11. `--max-workers N` overrides the upstream export worker count for this run.

## Execution

Run the matching helper script under this skill's `scripts/` directory with the user-supplied arguments. No extra setup is performed.

## Response Format

After the script finishes:

- state that config/auth were assumed to be configured
- report the org URL(s) being exported
- report the effective export output path
- confirm that the org export command completed
- confirm that the output path was indexed
