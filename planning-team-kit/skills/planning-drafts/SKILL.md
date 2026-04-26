---
name: planning-drafts
description: "Generate and save the standard draft planning artifact suite from aligned planning context."
argument-hint: "[planning context or source notes]"
---

# Planning Drafts

Use this skill after planning context exists. It drafts and saves the standard planning artifact suite.

## Invocation

Claude Code:

```text
/planning-team-kit:planning-drafts <planning-context>
```

Codex:

```text
$planning-drafts <planning-context>
```

## Purpose

Generate and locally save the standard draft-only planning artifact suite from structured context. PRD is only one output in the suite.

## Readiness Check

Before generating documents, check whether the input has a usable `planning_context`.

Do not generate draft artifacts when the core planning context is missing or too ambiguous.

If there is no usable context, route to `planning-intake` first. Missing core context includes:

- unclear problem statement
- missing users, stakeholders, or decision makers
- missing intended outcome
- missing non-goals or excluded scope
- missing success or failure criteria
- mixed confirmed facts, assumptions, risks, and constraints

If the context exists but a specific document-quality gap remains, route back to `planning-intake` before generating artifacts. Examples include:

- missing policy detail
- unclear edge case
- missing metric observation window
- missing owner, date, or validation detail
- unresolved requirement wording

If the user explicitly asks to proceed despite gaps, keep the output draft-only, set `approval_state: needs_review`, preserve unresolved items in open questions, and label unsupported claims as assumptions.

## Standard Suite

Always generate the standard suite:

- `brief`
- `prd`
- `user-stories`
- `feature-spec`
- `metrics-brief`

The bundled `qa-scenario`, `option-memo`, and `stakeholder-brief` templates are reserved resources. Do not generate them from `planning-drafts` until the suite contract is expanded later.

## Local Draft Persistence

Always save generated artifacts to the current workspace. Do not ask whether to save, and do not provide response-only output after artifacts are generated.

Use this directory format:

```text
docs/planning/drafts/YYYY-MM-DD-HHMMSS-topic-slug/
```

Example:

```text
docs/planning/drafts/2026-04-24-143205-login-onboarding/
```

Rules:

- Use the host environment's current local date and time for `YYYY-MM-DD-HHMMSS`.
- Build `topic-slug` from `planning_context.topic`, the document title, or the clearest available topic.
- Use lowercase kebab-case for `topic-slug`; remove unsafe path characters; use `planning-draft` if no topic is available.
- Do not overwrite existing suite directories. If the target path exists, append `-2`, `-3`, or the next available numeric suffix.
- Keep saved files inside the current workspace unless the user explicitly provides a different local workspace path.
- Do not write to Jira, Confluence, Slack, Google Drive, Notion, or other external systems.

Save this file set:

```text
00-suite-index.md
00-planning-context.md
01-brief.md
02-prd.md
03-user-stories.md
04-feature-spec.md
05-metrics-brief.md
```

`00-planning-context.md` is the canonical planning context. It must include YAML front matter plus human-readable Markdown sections.

`00-suite-index.md` must list the generated artifacts, traceability notes, assumptions, open questions, and recommended next skill.

## Generated Artifact Types

- `brief`
- `prd`
- `user-stories`
- `feature-spec`
- `metrics-brief`

## Template Map

Use the templates bundled with this skill:

- `planning-context` -> `templates/planning-context.md`
- `brief` -> `templates/brief.md`
- `option-memo` -> `templates/option-memo.md`
- `prd` -> `templates/prd.md`
- `user-stories` -> `templates/user-stories.md`
- `feature-spec` -> `templates/feature-spec.md`
- `qa-scenario` -> `templates/qa-scenario.md`
- `metrics-brief` -> `templates/metrics-brief.md`
- `stakeholder-brief` -> `templates/stakeholder-brief.md`

## Rules

- Keep all outputs draft-only.
- Run the readiness check before selecting or generating artifacts.
- Always generate the standard suite after the readiness check passes.
- Always save generated artifacts to `docs/planning/drafts/YYYY-MM-DD-HHMMSS-topic-slug/`.
- Save planning context as `00-planning-context.md`, not as a separate YAML file.
- Do not generate draft artifacts from unclear rough input unless the user explicitly asks to proceed with `approval_state: needs_review`.
- Use templates from this skill's local `templates/` directory.
- Preserve source, assumption, confidence, sensitivity, owner, and approval state metadata.
- Do not generate every bundled template.
- Do not invent missing requirements, metrics, owners, or dates.
- If source evidence is missing, label the statement as an assumption.
- Include open questions where the draft is incomplete.

## Response Format

Return:

- `Recommended Document Suite`
- `Saved Draft Directory`
- `Saved Files`
- `Generated Drafts`
- `Traceability Notes`
- `Assumptions and Open Questions`
- `Recommended Next Skill`

The recommended next skill is usually `/planning-team-kit:quality-review` or `$quality-review`.
