---
name: set-output-path
description: "Set default export output directory. Usage: /confluence-export-kit:set-output-path <path>"
---

# Set Output Path

Permanently update `export.output_path` in the `confluence-markdown-exporter` config so all subsequent exports write to that directory by default.

## Invocation

Primary usage:

```text
/confluence-export-kit:set-output-path <path>
```

## Rules

1. Treat `$ARGUMENTS[0]` as the required output path.
2. If the argument is missing or blank, stop and tell the user to run:

```text
/confluence-export-kit:set-output-path <path>
```

3. Before updating config, validate that Python, `pipx`, and `cme` are usable.
4. Write the value to `export.output_path` in the CME config file.
5. Report the previous value and the new value; do not silently overwrite.
6. This setting is persistent — all future exports use this path unless overridden at runtime with `[output-path]`.

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
python3 "${CLAUDE_SKILL_DIR}/scripts/set_output_path.py" "<path>"
```

## Response Format

After the script finishes:

- report Python/pipx/cme preflight status
- report the config file path
- report the previous output path value
- confirm the new output path that was written
