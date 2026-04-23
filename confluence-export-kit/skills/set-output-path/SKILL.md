---
name: set-output-path
description: Persist the default export output path in the confluence-markdown-exporter config. Permanently changes the output directory without passing [output-path] on every export command.
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

3. Before updating config, validate that Python, `pip`, `pipx`, and `cme` are usable.
4. Write the value to `export.output_path` in the CME config file.
5. Report the previous value and the new value; do not silently overwrite.
6. This setting is persistent — all future exports use this path unless overridden at runtime with `[output-path]`.

## Execution

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
