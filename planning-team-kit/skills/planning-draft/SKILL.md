---
name: planning-draft
description: "Generate and save the core draft planning artifact suite from aligned planning context."
argument-hint: "[planning context or source notes]"
---

# Planning Draft

Use this skill after planning context exists. It drafts and saves the core standard planning artifact suite.

## Invocation

Claude Code:

```text
/planning-team-kit:planning-draft <planning-context>
```

Codex:

```text
$planning-draft <planning-context>
```

## Purpose

Generate and locally save a slim draft-only planning artifact suite from structured context. The suite is optimized for planning-team review and manual Confluence update planning.

## Readiness Check

Before generating documents, check whether the input has a usable `planning_context`.

Do not generate draft artifacts when the core planning context is missing or too ambiguous.

If there is no usable context, route to `planning-start` first. Missing core context includes:

- unclear problem statement
- missing users, stakeholders, or decision makers
- missing intended outcome
- missing non-goals or excluded scope
- missing success or failure criteria
- mixed confirmed facts, assumptions, risks, and constraints

If the context exists but a specific document-quality gap remains, route back to `planning-start` before generating artifacts. Examples include:

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

The bundled reserved and legacy templates are reference resources. Do not generate them from `planning-draft` unless a later skill explicitly asks for a conditional add-on.

## Draft Generation Orchestration

Act as the suite orchestrator.

After the readiness check passes, generate `01-planning-brief.md` first as the canonical planning context and decision brief.

Before generating dependent artifacts, derive a trace contract from `01-planning-brief.md`, including requirement ID registry, scope boundaries, non-goals, source map, evidence sources, source confidence, assumptions, sensitivity, owner, and approval state.

When the execution environment supports subagents or parallel task execution, generate `02-requirements.md` and `03-behavior-spec.md` in parallel from `01-planning-brief.md` and the trace contract.

If subagents or parallel task execution are not available, do not skip the lane split. Run the same lanes sequentially and label the generation mode as `sequential fallback`.

Before saving files, run a reconciliation gate to align requirement IDs, cross-links, assumptions, open questions, non-goal boundaries, and behavior without matching requirements.

Generate `00-index.md` last from the final artifact map.

## Local Draft Persistence

Always save generated artifacts to the current workspace. Do not ask whether to save, and do not provide response-only output after artifacts are generated.

Use this directory format:

```text
planning/drafts/topic-slug--YYYY-MM-DD-HHMMSS/
```

Example:

```text
planning/drafts/login-onboarding--2026-04-24-143205/
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

`01-planning-brief.md` is the canonical planning context and decision brief. It must preserve the planning-start fields that matter for downstream review, including `evidence_sources`, `confirmed_facts`, `source_conflicts`, `excluded_sources`, and source confidence.

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
- Always save generated artifacts to `planning/drafts/topic-slug--YYYY-MM-DD-HHMMSS/`.
- Save the canonical planning context inside `01-planning-brief.md`, not as a separate YAML file.
- Do not generate draft artifacts from unclear rough input unless the user explicitly asks to proceed with `approval_state: needs_review`.
- Use templates from this skill's local `templates/` directory.
- Preserve source, source confidence, assumption, sensitivity, owner, and approval state metadata.
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
- `Generation Execution Mode`
- `Traceability Notes`
- `Assumptions and Open Questions`
- `Recommended Next Skill`

Use `parallel` or `sequential fallback` for `Generation Execution Mode`.

The recommended next skill is usually `/planning-team-kit:planning-review` or `$planning-review`.
