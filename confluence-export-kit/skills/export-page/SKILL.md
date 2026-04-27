---
name: export-page
description: "Export one or more Confluence pages by URL. Usage: /confluence-export-kit:export-page <page-url> [<page-url> ...] [output-path]"
argument-hint: "<page-url> [<page-url> ...] [output-path]"
---

# Export Page

Export one or more Confluence pages by URL with `cme pages`.

## Invocation

Claude Code:

```text
/confluence-export-kit:export-page <page-url>
/confluence-export-kit:export-page <page-url> <page-url2> ...
/confluence-export-kit:export-page <page-url> [<page-url2> ...] <output-path>
/confluence-export-kit:export-page <page-url> [<page-url2> ...] --output-path <path>
```

Codex:

```text
$export-page <page-url>
$export-page <page-url> <page-url2> ...
$export-page <page-url> [<page-url2> ...] <output-path>
$export-page <page-url> [<page-url2> ...] --output-path <path>
```

## Rules

1. Positional URL-like arguments are treated as page URLs.
2. If the final positional argument is not URL-like, treat it as an optional export output path override for this run only.
3. `--output-path <path>` is still supported as an explicit output path override. Do not combine it with a trailing positional output path.
4. At least one page URL is required.
5. Assume `cme`, config, and auth are already available.
6. Do not print the stored API token.
7. Run `cme pages <url1> [url2 ...]` with all supplied URLs in a single call.
8. If an output path was supplied, apply it only for this export via environment override. Do not persistently rewrite the user's `cme` config.
9. After `cme pages` completes, index the effective output path with `index-export`.
10. `--skip-unchanged` / `--no-skip-unchanged` — skips pages whose version matches the lockfile (incremental export). **Default: on.**
11. `--cleanup-stale` / `--no-cleanup-stale` — removes local files for pages deleted or moved in Confluence. **Default: on.**
12. `--jira-enrichment` fetches Jira issue summaries and includes them in the exported Markdown.
13. `--max-workers N` overrides the upstream export worker count for this run.

## Execution

Run the matching helper script under this skill's `scripts/` directory with the user-supplied arguments. No extra setup is performed.

## Response Format

After the script finishes:

- state that config/auth were assumed to be configured
- report how many pages are being exported and list their URLs
- report the effective export output path
- confirm that the page export command completed
- confirm that the output path was indexed
