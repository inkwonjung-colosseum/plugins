---
name: set-config
description: "Set confluence-export-kit auth and export defaults. Usage: /confluence-export-kit:set-config --api-key <api-key> --email <email> [--url <base-url>]"
argument-hint: "--api-key <api-key> --email <email> [--url <base-url>]"
---

# Set Config

Configure `confluence-markdown-exporter` auth and default export settings in one command.

## Invocation

Claude Code:

```text
/confluence-export-kit:set-config --api-key <api-key> --email <email>
/confluence-export-kit:set-config --api-key <api-key> --email <email> --url <base-url>
```

Codex:

```text
$set-config --api-key <api-key> --email <email>
$set-config --api-key <api-key> --email <email> --url <base-url>
```

## Rules

1. Require auth (`--api-key` and `--email`).
2. Treat `--api-key` and `--email` as a pair; do not accept only one.
3. Never print the API token back to the user.
4. Default target is `CONFLUENCE_EXPORT_KIT_BASE_URL`, then `https://colosseum.atlassian.net`. Override via `--url`.
5. When auth is supplied, always update both `auth.confluence` and `auth.jira` for that URL.
6. Always persist `export.output_path=./confluence`.
7. Always persist `export.skip_unchanged=true` so incremental export is the fixed default instead of a per-command flag.
8. Always persist `export.cleanup_stale=true` so stale cleanup is the fixed default instead of a per-command flag.
9. Always persist `export.enable_jira_enrichment=false` so Jira enrichment is disabled by default instead of a per-command flag.
10. Always persist `export.include_document_title=false` so exported Markdown does not duplicate the document title in the body.
11. Always persist `export.page_breadcrumbs=false` so exported Markdown does not include breadcrumb links at the top.
12. Apply all requested config changes in one write.
13. Do not probe the token; assume the supplied credentials are intended to be stored.
14. Before writing config, check whether `confluence-markdown-exporter` is installed through `pip`; install it with `pip` only when missing.

## Execution

Run the matching helper script under this skill's `scripts/` directory with the user-supplied arguments. No extra setup is performed.

## Response Format

After the script finishes:

- report detected platform
- report whether `confluence-markdown-exporter` was already installed or installed through `pip`
- report the config file path
- report whether auth was updated and which site was targeted
- do not echo the token
- report previous and new output path
- report that `export.skip_unchanged` is enabled
- report that `export.cleanup_stale` is enabled
- report that `export.enable_jira_enrichment` is disabled
- report that `export.include_document_title` is disabled
- report that `export.page_breadcrumbs` is disabled
