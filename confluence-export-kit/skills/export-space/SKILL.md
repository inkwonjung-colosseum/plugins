---
name: export-space
description: "Export all pages in a Confluence space. Usage: /confluence-export-kit:export-space <space-url> [output-path]"
---

# Export Space

Export every page in a Confluence space with `cme spaces`.

## Invocation

Primary usage:

```text
/confluence-export-kit:export-space <space-url>
```

Optional output override:

```text
/confluence-export-kit:export-space <space-url> <output-path>
```

## Rules

1. Treat `$ARGUMENTS[0]` as the Confluence space URL (e.g. `https://company.atlassian.net/wiki/spaces/SPACEKEY`).
2. Treat `$ARGUMENTS[1]` as an optional export output path override.
3. Before export, validate that Python, `pipx`, and `cme` are usable.
4. Extract the base site from the space URL (`scheme://netloc`) and verify that a configured `auth.confluence` entry with both `username` and `api_token` exists for that site.
5. If auth is missing or incomplete, stop and tell the user to run:

```text
/confluence-export-kit:set-api-key <api-key> <email>
```

6. Do not print the stored API token.
7. Run `cme spaces <space-url>` once auth is confirmed.
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

If no space URL argument was provided, stop and tell the user to run:

```text
/confluence-export-kit:export-space <space-url> [output-path]
```

Otherwise run the helper script in this skill directory:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/export_space.py" "<space-url>" ["<output-path>"]
```

## Response Format

After the script finishes:

- report Python/pipx/cme preflight status
- report which Confluence site was matched
- confirm that auth was already configured
- report the space URL being exported
- report the effective export output path
- confirm that the space export command completed
