---
name: export-page
description: "Export one or more Confluence pages by URL. Usage: /confluence-export-kit:export-page <page-url> [<page-url2> ...] [--output-path <path>]"
argument-hint: "<page-url> [<page-url2> ...] [--output-path <path>]"
---

# Export Page

Export one or more Confluence pages by URL with `cme pages`.

## Invocation

Single page:

```text
/confluence-export-kit:export-page <page-url>
```

Multiple pages:

```text
/confluence-export-kit:export-page <page-url> <page-url2> ...
```

Optional output override:

```text
/confluence-export-kit:export-page <page-url> [<page-url2> ...] --output-path <path>
```

## Rules

1. All positional arguments that start with `http://` or `https://` are treated as page URLs.
2. Use `--output-path <path>` to override the export output directory for this run only.
3. At least one page URL is required.
4. All supplied URLs must belong to the same Confluence site (`scheme://netloc`). Mixed-site exports are not supported.
5. Before export, validate that Python, `pipx`, and `cme` are usable.
6. Extract the base site from the first page URL and verify that a configured `auth.confluence` entry with both `username` and `api_token` exists for that site.
7. If auth is missing or incomplete, stop and tell the user to run:

```text
/confluence-export-kit:set-api-key <api-key> <email>
```

8. Do not print the stored API token.
9. Run `cme pages <url1> [url2 ...]` with all supplied URLs in a single call.
10. If `--output-path` was supplied, apply it only for this export via environment override. Do not persistently rewrite the user's `cme` config.
11. `--skip-unchanged` / `--no-skip-unchanged` — skips pages whose version matches the lockfile (incremental export). **Default: on.**
12. `--cleanup-stale` / `--no-cleanup-stale` — removes local files for pages deleted or moved in Confluence. **Default: on.**
13. `--jira-enrichment` fetches Jira issue summaries and includes them in the exported Markdown.
14. `--dry-run` validates auth and config without running the export; prints "skipped" and returns.

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
/confluence-export-kit:export-page <page-url> [<page-url2> ...] [--output-path <path>]
```

Otherwise run the helper script in this skill directory:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/export_page.py" "<url1>" ["<url2>" ...] [--output-path "<path>"]
```

## Response Format

After the script finishes:

- report Python/pipx/cme preflight status
- report which Confluence site was matched
- confirm that auth was already configured
- report how many pages are being exported and list their URLs
- report the effective export output path
- confirm that the page export command completed
