---
name: export-page-with-descendant
description: "Export one or more Confluence pages with descendants. Usage: /confluence-export-kit:export-page-with-descendant <page-url> [<page-url> ...]"
argument-hint: "<page-url> [<page-url> ...]"
---

# Export Page With Descendant

Export one or more Confluence root pages and every descendant beneath each root with `cme pages-with-descendants`.

## Invocation

Claude Code:

```text
/confluence-export-kit:export-page-with-descendant <page-url>
/confluence-export-kit:export-page-with-descendant <page-url> <page-url2>
```

Codex:

```text
$export-page-with-descendant <page-url>
$export-page-with-descendant <page-url> <page-url2>
```

## Rules

1. Treat positional arguments as Confluence root page targets and forward them to `cme pages-with-descendants` unchanged.
2. Do not perform wrapper-side URL validation; malformed or unsupported targets must fail in `cme`.
3. Assume `cme`, config, and auth are already available.
4. Do not print the stored API token.
5. Run `cme pages-with-descendants <page-url> [<page-url2> ...]`.
6. Force the fixed output path with `CME_EXPORT__OUTPUT_PATH=./confluence`; do not expose per-export output path overrides.
7. After `cme pages-with-descendants` completes, index the fixed output path with `index-export`.
8. Export behavior defaults are configured by `set-config`: `export.skip_unchanged=true`, `export.cleanup_stale=true`, and `export.enable_jira_enrichment=false`.
9. Do not expose per-export flags for skip unchanged, cleanup stale, or Jira enrichment.

## Execution

Run the matching helper script under this skill's `scripts/` directory with the user-supplied arguments. No extra setup is performed.

## Response Format

After the script finishes:

- state that config/auth were assumed to be configured
- report how many root pages are being exported and list their URLs
- report the fixed export output path
- confirm that the page-with-descendants export command completed
- confirm that the output path was indexed
