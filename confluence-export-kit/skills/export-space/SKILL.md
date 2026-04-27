---
name: export-space
description: "Export all pages in one or more Confluence spaces. Usage: /confluence-export-kit:export-space <space-url> [<space-url> ...]"
argument-hint: "<space-url> [<space-url> ...]"
---

# Export Space

Export every page in one or more Confluence spaces with `cme spaces`.

## Invocation

Claude Code:

```text
/confluence-export-kit:export-space <space-url>
/confluence-export-kit:export-space <space-url> <space-url2>
```

Codex:

```text
$export-space <space-url>
$export-space <space-url> <space-url2>
```

## Rules

1. Treat positional arguments as Confluence space targets and forward them to `cme spaces` unchanged.
2. Do not perform wrapper-side URL validation; malformed or unsupported targets must fail in `cme`.
3. Assume `cme`, config, and auth are already available.
4. Do not print the stored API token.
5. Run `cme spaces <space-url> [<space-url2> ...]`.
6. Force the fixed output path with `CME_EXPORT__OUTPUT_PATH=./confluence`; do not expose per-export output path overrides.
7. After `cme spaces` completes, index the fixed output path with `index-export`.
8. Export behavior defaults are configured by `set-config`: `export.skip_unchanged=true`, `export.cleanup_stale=true`, and `export.enable_jira_enrichment=false`.
9. Do not expose per-export flags for skip unchanged, cleanup stale, or Jira enrichment.

## Execution

Run the matching helper script under this skill's `scripts/` directory with the user-supplied arguments. No extra setup is performed.

## Response Format

After the script finishes:

- state that config/auth were assumed to be configured
- report the space URL(s) being exported
- report the fixed export output path
- confirm that the space export command completed
- confirm that the output path was indexed
