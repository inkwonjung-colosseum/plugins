---
description: "Overview and getting-started guide for the skeleton-plugin template."
---

# Skeleton Plugin Help

This plugin is a starter template for building plugins that work in both Codex and Claude Code.

## Available Commands

- `/skeleton-plugin:help` — Show this help message.

## Available Skills

- `skeleton-plugin-starter` — Placeholder starter skill that shows the expected `SKILL.md` structure.

## Getting Started

1. Update the manifests under `.claude-plugin/` and `.codex-plugin/` with your plugin's real metadata.
2. Replace the starter skill in `skills/` with your first real workflow.
3. Add or replace commands in `commands/`.
4. Remove unused hooks, MCP definitions, and assets before publishing.
