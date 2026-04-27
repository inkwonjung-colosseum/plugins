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

`planning-team-kit` is a draft-only planning document quality kit. It helps planning teams move through five user-facing stages:

1. Organize planning input and relevant Confluence evidence.
2. Optionally check weak decisions with one question at a time.
3. Generate the right planning artifacts.
4. Review and improve the draft.
5. Prepare a manual Confluence add/update plan.

## Must Explain

- The plugin creates draft planning artifacts, not final decisions.
- `planning-draft` always saves generated core standard draft artifacts under `planning/drafts/topic-slug--YYYY-MM-DD-HHMMSS/`.
- v0.2.1 does not write to Jira, Confluence, Slack, Google Drive, or Notion.
- `confluence-update-plan` creates manual Confluence add/update instructions only and does not change Confluence pages.
- Unsupported facts must be marked as assumptions.
- Requirements are one artifact type, not the only output.
- `planning-check` is optional. It checks a plan or decision with one question at a time before draft generation or handoff.
- `planning-review` is a multi-agent review gate with Product Context Reviewer, Story & Testability Reviewer, Feature Behavior & Policy Reviewer, Metrics & Evidence Reviewer, Cross-Artifact Consistency Reviewer, and Handoff Governance Reviewer perspectives.
- Claude Code uses `/planning-team-kit:<skill>`.
- Codex uses `$<skill>`.

## Core Skills

- `planning-start`: organize input and select relevant indexed Confluence evidence before writing documents.
- `planning-check`: check a plan, planning context, or decision before writing or handoff.
- `planning-draft`: generate and save the core draft planning artifact suite.
- `planning-review`: inspect documents with the shared multi-agent review gate.
- `confluence-update-plan`: create a manual Confluence add/update plan without external writes.

## Response Format

Start with one sentence explaining the plugin. Then include:

- `Start Here`: three short scenarios.
- `Core Skills`: flat bullets with Claude Code and Codex invocation examples.
- `Safety`: draft-only, no source no claim, no external writes.
- `If Context Is Weak`: tell the user to return to `planning-start`.

Keep the answer concise and operational.
