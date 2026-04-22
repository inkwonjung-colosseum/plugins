---
description: Persist the default export output path in the confluence-markdown-exporter config.
---

# Set Output Path

Permanently set `export.output_path` in the `confluence-markdown-exporter` config.

## Usage

```text
/confluence-export-kit:set-output-path <path>
```

- `<path>` — required directory path to store exported Markdown files

All subsequent export commands use this path by default unless overridden with `[output-path]`.

See `skills/set-output-path/SKILL.md` for runtime rules and response format.
