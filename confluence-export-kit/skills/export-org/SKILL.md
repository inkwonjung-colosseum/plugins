---
name: export-org
description: "Export all spaces/pages under one or more Confluence orgs. Usage: /confluence-export-kit:export-org <org-url> [<org-url> ...]"
argument-hint: "<org-url> [<org-url> ...]"
---

# Export Org

Export every space and page under one or more Confluence instances with `cme orgs`.

## Invocation

Claude Code:

```text
/confluence-export-kit:export-org <org-url>
/confluence-export-kit:export-org <org-url> <org-url2>
```

Codex:

```text
$export-org <org-url>
$export-org <org-url> <org-url2>
```

## Rules

1. Treat positional arguments as Confluence instance root targets and forward them to `cme orgs` unchanged.
2. Do not perform wrapper-side URL validation; malformed or unsupported targets must fail in `cme`.
3. Assume `cme`, config, and auth are already available.
4. Do not print the stored API token.
5. Run `cme orgs <org-url> [<org-url2> ...]`.
6. Force the fixed output path with `CME_EXPORT__OUTPUT_PATH=./confluence`; do not expose per-export output path overrides.
7. After `cme orgs` completes, index the fixed output path with `index-export`.
8. Export behavior defaults are configured by `set-config`: `export.skip_unchanged=true`, `export.cleanup_stale=true`, and `export.enable_jira_enrichment=false`.
9. Do not expose per-export flags for skip unchanged, cleanup stale, or Jira enrichment.

## Execution

Run the matching helper script under this skill's `scripts/` directory with the user-supplied arguments. No extra setup is performed.

## Response Format

After the script finishes:

- state that config/auth were assumed to be configured
- report the org URL(s) being exported
- report the fixed export output path
- confirm that the org export command completed
- confirm that the output path was indexed
