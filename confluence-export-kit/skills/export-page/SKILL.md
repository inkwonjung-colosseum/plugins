---
name: export-page
description: "Export one or more Confluence pages by URL. Usage: /confluence-export-kit:export-page <page-url> [<page-url> ...]"
argument-hint: "<page-url> [<page-url> ...]"
---

# Export Page

Export one or more Confluence pages by URL with `cme pages`.

## Invocation

Claude Code:

```text
/confluence-export-kit:export-page <page-url>
/confluence-export-kit:export-page <page-url> <page-url2> ...
```

Codex:

```text
$export-page <page-url>
$export-page <page-url> <page-url2> ...
```

## Rules

1. Treat positional arguments as page targets and forward them to `cme pages` unchanged.
2. Do not perform wrapper-side URL validation; malformed or unsupported targets must fail in `cme`.
3. Force the fixed output path with `CME_EXPORT__OUTPUT_PATH=./confluence`; do not expose per-export output path overrides.
4. At least one page URL is required.
5. Assume `cme`, config, and auth are already available.
6. Do not print the stored API token.
7. Run `cme pages <url1> [url2 ...]` with all supplied URLs in a single call.
8. Set `CME_EXPORT__OUTPUT_PATH=./confluence` for this run so cleanup and indexing target the same fixed path.
9. After `cme pages` completes, index the fixed output path with `index-export`.
10. Export behavior defaults are configured by `set-config`: `export.skip_unchanged=true`, `export.cleanup_stale=true`, and `export.enable_jira_enrichment=false`.
11. Do not expose per-export flags for skip unchanged, cleanup stale, or Jira enrichment.

## Execution

Run the matching helper script under this skill's `scripts/` directory with the user-supplied arguments. No extra setup is performed.

## Response Format

After the script finishes:

- state that config/auth were assumed to be configured
- report how many pages are being exported and list their URLs
- report the fixed export output path
- confirm that the page export command completed
- confirm that the output path was indexed
