---
name: export-page-tree
description: "Export a Confluence page and all descendants. Usage: /confluence-export-kit:export-page-tree <page-url> [output-path]"
---

# Export Page Tree

Export one Confluence page and every child page beneath it with `cme pages-with-descendants`.

## Invocation

Primary usage:

```text
/confluence-export-kit:export-page-tree <page-url>
```

Optional output override:

```text
/confluence-export-kit:export-page-tree <page-url> <output-path>
```

## Rules

1. Treat `$ARGUMENTS[0]` as the Confluence page URL.
2. Treat `$ARGUMENTS[1]` as an optional export output path override.
3. Before export, validate that Python, `pipx`, and `cme` are usable.
4. Read the `cme` config file and verify that the page URL's base site already has a configured `auth.confluence` entry with both `username` and `api_token`.
5. If auth is missing or incomplete, stop and tell the user to run:

```text
/confluence-export-kit:set-api-key <api-key> <email>
```

6. Do not print the stored API token.
7. Run `cme pages-with-descendants <page-url>` once auth is confirmed.
8. If an output path was supplied, apply it only for this export via environment override. Do not persistently rewrite the user's `cme` config.
9. `--skip-unchanged` / `--no-skip-unchanged` — skips pages whose version matches the lockfile (incremental export). **Default: on.**
10. `--cleanup-stale` / `--no-cleanup-stale` — removes local files for pages deleted or moved in Confluence. **Default: on.**
11. `--jira-enrichment` fetches Jira issue summaries and includes them in the exported Markdown.
12. `--dry-run` validates auth and config without running the export; prints "skipped" and returns.

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

If no page URL argument was provided, stop and tell the user to run:

```text
/confluence-export-kit:export-page-tree <page-url> [output-path]
```

Otherwise run the helper script in this skill directory:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/export_page_tree.py" "<page-url>" ["<output-path>"]
```

## Response Format

After the script finishes:

- report Python/pipx/cme preflight status
- report which Confluence site was matched
- confirm that auth was already configured
- report the effective export output path
- confirm that the page tree export command completed
