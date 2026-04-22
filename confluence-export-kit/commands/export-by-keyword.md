---
description: Search Confluence by keyword and export matched pages with Confluence Export Kit.
---

# Export By Keyword

Search Confluence with CQL against `title` and `text`, then export only the matched pages.

## Usage

```text
/confluence-export-kit:export-by-keyword <keyword> [output-path]
```

- `<keyword>` — required keyword or phrase
- `[output-path]` — optional one-off output override
- `--site <base-url>` — optional site override

See `skills/export-by-keyword/SKILL.md` for runtime rules and response format.
