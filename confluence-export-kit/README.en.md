# Confluence Export Kit

Confluence Export Kit is a `Claude Code` plugin for Confluence export-only workflows (v0.1.0). It handles `confluence-markdown-exporter` auth setup, org/space/page-tree/page export, keyword and label search export, and the Python/pipx/`cme` bootstrap needed to run those exports.

This is not a general Atlassian toolkit. The supported surface is intentionally narrow:

- Confluence auth setup and token validation
- org / space / page-tree / individual page export
- keyword-matched or label-matched page export
- export runtime bootstrap (`python`, `pip`, `pipx`, `cme`)
- persistent default output path configuration

Explicit non-goals:

- planning briefs
- Jira write workflows
- general-purpose CQL console
- `cme config` interactive menu

See the Korean document in [README.md](./README.md).

## Included Pieces

- `.claude-plugin/plugin.json` — Claude Code plugin manifest
- `commands/help.md` — export workflow, install, and env-var guidance
- `commands/set-api-key.md` — auth setup command
- `commands/set-output-path.md` — default output path command
- `commands/export-org.md` — org export command
- `commands/export-space.md` — space export command
- `commands/export-page-tree.md` — page-tree export command
- `commands/export-page.md` — single/multi page export command
- `commands/export-by-keyword.md` — keyword search export command
- `commands/export-by-label.md` — label search export command
- `commands/config-show.md` — show current configuration command
- `skills/set-api-key/SKILL.md` — auth setup and token validation
- `skills/help/SKILL.md` — help response rules and quick-start guidance
- `skills/set-output-path/SKILL.md` — persist default output path
- `skills/export-org/SKILL.md` — export all spaces and pages under an org
- `skills/export-space/SKILL.md` — export all pages in a space
- `skills/export-page-tree/SKILL.md` — export one page and all descendants
- `skills/export-page/SKILL.md` — export one or more pages by URL
- `skills/export-by-keyword/SKILL.md` — export only keyword-matched pages
- `skills/export-by-label/SKILL.md` — export only label-matched pages
- `skills/config-show/SKILL.md` — display current cme configuration
- `scripts/cme_runtime.py` — shared preflight, bootstrap, and config/auth helpers

## Export Workflow

```text
/confluence-export-kit:set-api-key <api-key> <email>       (one-time auth)
/confluence-export-kit:set-output-path <path>              (optional: set default output dir)
    │
    ├─► /confluence-export-kit:export-org <org-url> [output-path]
    │       exports every space and page under a Confluence instance
    │
    ├─► /confluence-export-kit:export-space <space-url> [output-path]
    │       exports every page in a space
    │
    ├─► /confluence-export-kit:export-page-tree <page-url> [output-path]
    │       exports one page and all descendants
    │
    ├─► /confluence-export-kit:export-page <page-url> [<page-url2> ...] [--output-path <path>]
    │       exports one or more specific pages by URL
    │
    ├─► /confluence-export-kit:export-by-keyword <keyword> [output-path]
    │       searches title + text (CQL), exports only matched pages
    │
    └─► /confluence-export-kit:export-by-label <label> [output-path]
            searches by Confluence label (CQL), exports only matched pages
```

## Common Export Flags

Available on all export commands:

| Flag | Description |
|---|---|
| `--skip-unchanged` | Skip pages whose version matches the lockfile (incremental export) |
| `--cleanup-stale` | Remove local files for pages deleted or moved in Confluence |
| `--jira-enrichment` | Include Jira issue summaries in exported Markdown |
| `--dry-run` | Validate auth and config without running the export |
| `--max-workers N` | Override the number of parallel export workers |

## Installation

From this repository root in Claude Code:

```text
/plugin marketplace add https://raw.githubusercontent.com/inkwonjung-colosseum/plugins/main/.claude-plugin/marketplace.json
/plugin install confluence-export-kit@inkwonjung-colosseum-plugins
/reload-plugins
```

## Suggested Commands

```text
/confluence-export-kit:set-api-key <api-key> <email>
```

```text
/confluence-export-kit:export-page-tree https://colosseum.atlassian.net/wiki/spaces/KEY/pages/123456789/Root
```

```text
/confluence-export-kit:export-by-keyword "incident review" ./exports/confluence
```

```text
/confluence-export-kit:export-by-label "runbook" --space-key OPS --dry-run
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `CONFLUENCE_EXPORT_KIT_BASE_URL` | `https://colosseum.atlassian.net` | Target Confluence site for `set-api-key`, `export-by-keyword`, and `export-by-label` |

## Behavior Notes

- `set-api-key`
  - Default site is `https://colosseum.atlassian.net`.
  - Override via `CONFLUENCE_EXPORT_KIT_BASE_URL` or `--url`.
  - Token validation runs by default. Use `--skip-validate` to skip.
  - Updates both `auth.confluence` and `auth.jira` for the same URL.
- `set-output-path`
  - Persists `export.output_path` to the cme config file.
  - All subsequent exports use this path as the default.
- All export commands
  - Block when auth is missing and prompt to run `set-api-key`.
  - Apply `[output-path]` via env override only; never modify cme config persistently.
- `export-by-keyword` / `export-by-label`
  - Export matched pages only, not descendants.
  - Use `--space-key` to restrict search to a specific space.
