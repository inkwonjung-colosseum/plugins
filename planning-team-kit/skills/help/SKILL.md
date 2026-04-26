---
name: help
description: Show concise help for planning-team-kit.
---

# planning-team-kit Help

Use this skill when the user asks what `planning-team-kit` can do, how to start, or which planning workflow to use.

## Invocation

Claude Code:

```text
/planning-team-kit:help
```

Codex:

```text
$help
```

## Scope

`planning-team-kit` is a draft-only planning document quality kit. It helps planning teams move through three user-facing stages:

1. Define and align the idea.
2. Generate the right planning artifacts.
3. Review and improve the draft before human handoff.

## Must Explain

- The plugin creates draft planning artifacts, not final decisions.
- `planning-drafts` always saves generated standard draft artifacts under `docs/planning/drafts/YYYY-MM-DD-HHMMSS-topic-slug/`.
- v0.1 does not write to Jira, Confluence, Slack, Google Drive, or Notion.
- Unsupported facts must be marked as assumptions.
- PRD is one artifact type, not the only output.
- `quality-review` is a multi-agent review gate with Product Context Reviewer, Story & Testability Reviewer, Feature Behavior & Policy Reviewer, Metrics & Evidence Reviewer, Cross-Artifact Consistency Reviewer, and Handoff Governance Reviewer perspectives.
- Claude Code uses `/planning-team-kit:<skill>`.
- Codex uses `$<skill>`.

## Core Skills

- `planning-intake`: structure the idea before writing documents.
- `planning-drafts`: generate and save the standard draft planning artifact suite.
- `quality-review`: inspect documents with the shared multi-agent review gate.

## Response Format

Start with one sentence explaining the plugin. Then include:

- `Start Here`: three short scenarios.
- `Core Skills`: flat bullets with Claude Code and Codex invocation examples.
- `Safety`: draft-only, no source no claim, no external writes.
- `If Context Is Weak`: tell the user to return to `planning-intake`.

Keep the answer concise and operational.
