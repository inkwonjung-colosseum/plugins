---
name: planning-drafts
description: "Generate and save the core draft planning artifact suite from aligned planning context."
argument-hint: "[planning context or source notes]"
---

# Planning Drafts

Use this skill after planning context exists. It drafts and saves the core standard planning artifact suite.

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

Generate and locally save a slim draft-only planning artifact suite from structured context. The suite is optimized for planning-team review before deeper handoff artifacts are split out.

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

Always generate the core standard suite:

- `index`
- `planning-brief`
- `requirements`
- `behavior-spec`

The bundled reserved and legacy templates are reference resources. Do not generate them from `planning-drafts` unless a later skill explicitly asks for a conditional add-on.

## Local Draft Persistence

Always save generated artifacts to the current workspace. Do not ask whether to save, and do not provide response-only output after artifacts are generated.

Use this directory format:

```text
planning/topic-slug--YYYY-MM-DD-HHMMSS/
```

Example:

```text
planning/login-onboarding--2026-04-24-143205/
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
00-index.md
01-planning-brief.md
02-requirements.md
03-behavior-spec.md
```

`01-planning-brief.md` is the canonical planning context and decision brief. It must preserve the planning-intake fields that matter for downstream review.

`00-index.md` must list reading order, generated artifacts, source map, traceability notes, assumptions, open questions, and recommended next skill.

## Generated Artifact Types

- `index`
- `planning-brief`
- `requirements`
- `behavior-spec`

## Template Map

Use the core templates bundled with this skill:

- `index` -> `templates/index.md`
- `planning-brief` -> `templates/planning-brief.md`
- `requirements` -> `templates/requirements.md`
- `behavior-spec` -> `templates/behavior-spec.md`

Reserved and legacy templates remain available for compatibility and future conditional skills:

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
- Always generate the core standard suite after the readiness check passes.
- Always save generated artifacts to `planning/topic-slug--YYYY-MM-DD-HHMMSS/`.
- Save the canonical planning context inside `01-planning-brief.md`, not as a separate YAML file.
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
