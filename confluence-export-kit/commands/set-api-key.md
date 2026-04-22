---
description: Configure confluence-markdown-exporter auth for Confluence Export Kit.
---

# Set API Key

Configure `confluence-markdown-exporter` auth for a Confluence site.

## Usage

```text
/confluence-export-kit:set-api-key <api-key> <email>
```

- `<api-key>` — required Atlassian API token
- `<email>` — required Atlassian email
- `--skip-validate` — skip token probe (probe runs by default)
- `--url <base-url>` — optional site override

See `skills/set-api-key/SKILL.md` for runtime rules and response format.
