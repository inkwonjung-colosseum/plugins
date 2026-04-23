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

1. Before running, validate that Python, `pip`, `pipx`, and `cme` are usable.
2. Run `cme config list` and capture its full output.
3. If `--json` is passed, run `cme config list -o json` instead.
4. Print the output verbatim — do not summarize or truncate it.
5. Do not infer, modify, or interpret the config values shown.

## Execution

Run the helper script in this skill directory:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/config_show.py" [--json]
```

## Response Format

After the script finishes:

- report Python/pipx/cme preflight status
- print the full `cme config list` output
