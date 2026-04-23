---
name: export-by-label
description: "Export Confluence pages by label. Usage: /confluence-export-kit:export-by-label <label> [output-path] [--space-key <KEY>] [--dry-run]"
---

# Export By Label

Search Confluence pages by label and export only the matched pages with `cme pages`.

## Invocation

Primary usage:

```text
/confluence-export-kit:export-by-label <label>
```

Optional output override:

```text
/confluence-export-kit:export-by-label <label> <output-path>
```

Limit search to a specific space:

```text
/confluence-export-kit:export-by-label <label> --space-key <SPACEKEY>
```

Preview matched pages without exporting:

```text
/confluence-export-kit:export-by-label <label> --dry-run
```

## Rules

1. Treat `$ARGUMENTS[0]` as the Confluence label name to search.
2. Treat `$ARGUMENTS[1]` as an optional export output path override.
3. Default target is `CONFLUENCE_EXPORT_KIT_BASE_URL`, then `https://colosseum.atlassian.net`. Override via `--site`.
4. Before export, validate that Python, `pipx`, and `cme` are usable.
5. Read the `cme` config file and verify that the target site already has a configured `auth.confluence` entry with both `username` and `api_token`.
6. If auth is missing or incomplete, stop and tell the user to run:

```text
/confluence-export-kit:set-api-key <api-key> <email>
```

7. Search Confluence with CQL: `type = page and label = "<label>"`.
8. If `--space-key <SPACEKEY>` is provided, add `and space = "<SPACEKEY>"` to the CQL query.
9. If `--dry-run` is set, print the matched page URLs and stop without running the export.
10. Export only the matched pages. Do not export descendants.
11. If an output path was supplied, apply it only for this export via environment override. Do not persistently rewrite the user's `cme` config.
12. `--skip-unchanged` / `--no-skip-unchanged` — skips pages whose version matches the lockfile (incremental export). **Default: on.**
13. `--cleanup-stale` / `--no-cleanup-stale` — removes local files for pages deleted or moved in Confluence. **Default: on.**
14. `--jira-enrichment` fetches Jira issue summaries and includes them in the exported Markdown.
15. Do not print stored secrets.

## Execution

### Step 1 — Python availability check

Before running any script, verify Python is installed:

```bash
python3 --version
```

If this fails, stop and tell the user:

> **Python is not installed.** Install Python 3.10+ before continuing:
> - **macOS**: `brew install python` or download from https://www.python.org/downloads/
> - **Windows**: Download from https://www.python.org/downloads/ (check "Add to PATH" during install)
> - **Linux**: `sudo apt install python3` (Debian/Ubuntu) or `sudo dnf install python3` (Fedora)

Do not proceed to Step 2 until Python is available.

### Step 2 — Run the helper script

If no label argument was provided, stop and tell the user to run:

```text
/confluence-export-kit:export-by-label <label> [output-path] [--space-key <KEY>] [--dry-run]
```

Otherwise run the helper script in this skill directory:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/export_by_label.py" "<label>" ["<output-path>"] [--space-key "<SPACEKEY>"] [--dry-run] [--no-skip-unchanged] [--no-cleanup-stale] [--jira-enrichment]
```

## Response Format

After the script finishes:

- report Python/pipx/cme preflight status
- report the Confluence site used
- confirm that auth was already configured
- report the label searched and any space key filter applied
- report how many pages matched
- if dry-run: list all matched URLs and note that export was skipped
- if not dry-run: report the effective export output path and confirm export completed
