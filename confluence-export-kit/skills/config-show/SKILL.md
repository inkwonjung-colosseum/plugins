---
name: config-show
description: Show the current confluence-markdown-exporter configuration by running cme config list. Add --json to output JSON format.
---

# Config Show

Display the current `confluence-markdown-exporter` configuration with `cme config list`.

## Invocation

Primary usage:

```text
/confluence-export-kit:config-show
```

JSON output:

```text
/confluence-export-kit:config-show --json
```

## Rules

1. Before running, validate that Python, `pipx`, and `cme` are usable.
2. Run `cme config list` and capture its full output.
3. If `--json` is passed, run `cme config list -o json` instead.
4. Print the output verbatim — do not summarize or truncate it.
5. Do not infer, modify, or interpret the config values shown.

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

Run the helper script in this skill directory:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/config_show.py" [--json]
```

## Response Format

After the script finishes:

- report Python/pipx/cme preflight status
- print the full `cme config list` output

## Screen Feedback

When showing results to the user, explain terminal rendering behavior for both platforms:

- **macOS / Linux**: Terminal and Claude Code desktop render ANSI output directly. `cme config list` output appears as-is.
- **Windows**: Terminal treats paths with backslashes and may wrap long lines differently. If output appears truncated, suggest running with `--json` flag for structured output or increasing terminal width (`mode con cols=120` in CMD, `$Host.UI.RawUI.BufferSize.Width = 120` in PowerShell).
