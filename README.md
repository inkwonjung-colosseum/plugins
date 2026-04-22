# Plugins Workspace

English | [한국어](./README.ko.md)

This repository is a marketplace-ready workspace for Claude Code plugins. Each plugin directory is self-contained with its own manifest, skills, hooks, scripts, and documentation. The repository root holds a `marketplace.json` catalog for distribution.

## Quick Start

### Add this marketplace

```bash
# From a cloned copy
claude plugin marketplace add /path/to/plugins

# Or from a hosted URL
claude plugin marketplace add https://raw.githubusercontent.com/inkwonjung-colosseum/plugins/main/.claude-plugin/marketplace.json
```

### Install a plugin

```bash
# List available plugins
claude plugin marketplace list

# Install a specific plugin
claude plugin install confluence-export-kit
```

### Alternative: local plugin add

```bash
claude plugin add ./confluence-export-kit
```

## Plugin Directories

| Plugin | Purpose | Docs |
|---|---|---|
| `confluence-export-kit` | Confluence export-only plugin: auth setup, page-tree/keyword/label export, `confluence-markdown-exporter` bootstrap | [EN](./confluence-export-kit/README.en.md) / [KR](./confluence-export-kit/README.md) |
| `skeleton-plugin` | Starter template for building plugins that support both Codex and Claude Code | [EN](./skeleton-plugin/README.en.md) / [KR](./skeleton-plugin/README.md) |

## Repository Layout

```text
plugins/
├── .claude-plugin/
│   └── marketplace.json     # Marketplace catalog
├── confluence-export-kit/
│   ├── .claude-plugin/
│   │   └── plugin.json      # Plugin manifest
│   ├── commands/            # Slash commands (.md)
│   ├── skills/              # Skills (SKILL.md per folder)
│   ├── scripts/             # Helper scripts
│   └── docs/                # Plugin docs
├── skeleton-plugin/
│   ├── .claude-plugin/
│   │   └── plugin.json      # Plugin manifest
│   ├── .codex-plugin/       # Codex manifest (optional)
│   ├── commands/
│   ├── skills/
│   ├── hooks/
│   ├── scripts/
│   └── assets/
├── README.md
└── README.ko.md
```

## Marketplace Structure

The root `.claude-plugin/marketplace.json` catalogs all available plugins. Each entry maps a plugin name to its source directory and metadata.

```json
{
  "owner": "inkwonjung-colosseum",
  "plugins": [
    {
      "name": "confluence-export-kit",
      "source": "./confluence-export-kit",
      "description": "...",
      "version": "0.1.0"
    }
  ]
}
```

### Adding a new plugin to the marketplace

1. Create the plugin directory with `.claude-plugin/plugin.json`.
2. Add an entry to `.claude-plugin/marketplace.json`.
3. Run `claude plugin marketplace update inkwonjung-colosseum` to refresh.

## Working In This Repo

1. Open the plugin directory you want to work on.
2. Read that plugin's README before editing manifests, hooks, skills, or scripts.
3. Keep plugin-specific state inside the plugin directory.
4. After changes, test with `claude plugin add ./<plugin-dir>` before publishing.

## Notes

- The repository root is not an installable plugin — it is a marketplace catalog.
- `marketplace.json` can be hosted on any static URL for remote distribution.
- Plugins without a `.claude-plugin/plugin.json` are not recognized by the marketplace.

## Language Notes

- Root: `README.md` (English), `README.ko.md` (Korean).
- `confluence-export-kit`: `README.en.md` (English), `README.md` (Korean).
- `skeleton-plugin`: `README.en.md` (English), `README.md` (Korean).
