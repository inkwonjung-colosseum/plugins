---
name: show-config
description: Show the current confluence-markdown-exporter configuration by running cme config list. Add --json to output JSON format.
---

# Show Config

Display the current `confluence-markdown-exporter` configuration with `cme config list`.

## Invocation

Claude Code:

```text
/confluence-export-kit:show-config
/confluence-export-kit:show-config --json
```

Codex:

```text
$show-config
$show-config --json
```

## Rules

1. Assume `cme` is already available.
2. Run `cme config list` and capture its full output.
3. If `--json` is passed, run `cme config list -o json` instead.
4. Print the full output without summarizing or truncating it.
5. Do not infer, modify, or interpret the config values shown.

## Execution

Run the matching helper script under this skill's `scripts/` directory with the user-supplied arguments. No extra setup is performed.

## Response Format

After the script finishes:

- print the full helper output, including the `--- cme config list ---` header and any `--- cme stderr ---` section

## Screen Feedback

When showing results to the user, explain terminal rendering behavior for both platforms:

- **macOS / Linux**: Terminal, Claude Code desktop, and Codex render ANSI output directly. `cme config list` output appears as-is.
- **Windows**: Terminal treats paths with backslashes and may wrap long lines differently. If output appears truncated, suggest running with `--json` flag for structured output or increasing terminal width (`mode con cols=120` in CMD, `$Host.UI.RawUI.BufferSize.Width = 120` in PowerShell).
