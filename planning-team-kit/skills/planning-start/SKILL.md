---
name: planning-start
description: "Organize planning input and select relevant indexed Confluence evidence before generating artifacts."
argument-hint: "[idea, note, meeting summary, or rough requirement]"
---

# Planning Start

Use this skill before generating planning documents. It turns rough input into a structured planning context and, when a `.confluence-index/` exists in the workspace, selects the smallest relevant Confluence source set for evidence.

## Invocation

Claude Code:

```text
/planning-team-kit:planning-start <idea or notes>
```

Codex:

```text
$planning-start <idea or notes>
```

## Purpose

Run the front-of-funnel planning alignment without jumping straight to a PRD. The output is draft-only planning context that downstream skills can use.

## Process

1. Identify the current input type: idea, meeting note, rough requirement, existing draft, revision request, or decision request.
2. Extract topic, keywords, likely product area, desired outcome, scope hints, and whether this is new planning or revision planning.
3. If `.confluence-index/` exists, use the Evidence Selection process before asking the user for facts that may already be documented.
4. Extract what is already known from the user input and selected evidence.
5. Build a draft `planning_context` from the known information.
6. Check whether the context is ready for artifact generation.
7. Ask one high-leverage question at a time only when the answer changes the plan.
8. Update the `planning_context` after each answer.
9. Repeat the readiness check and question loop until the context is clear enough for artifact generation, the user asks to stop, or the user cannot provide more information.
10. Compare 2-3 viable directions when there is a meaningful choice.
11. Produce a concise planning context.
12. Stop before artifact generation if the context is still too ambiguous.

## Evidence Selection

When exported Confluence documents are indexed in the workspace, select evidence before asking broad source questions.

Read in this order:

1. `.confluence-index/registry.json` to choose the relevant source.
2. `.confluence-index/sources/<source-id>/source-index.jsonl` to rank candidate documents.
3. `.confluence-index/sources/<source-id>/tree.md` to understand hierarchy and neighboring pages.
4. Raw exported Markdown only for the smallest set of candidate files needed for evidence.

Selection rules:

- Use the user's topic, keywords, product area, feature name, policy terms, and revision target to rank candidates.
- Keep at most 12 indexed candidate records in the working source list.
- Read at most 6 raw Markdown source files by default.
- Prefer `current` documents over `draft` and `archive` documents when status metadata is available.
- Use `archive` and `draft` documents only as historical context, contradiction checks, or explicit user-requested sources.
- Do not load a whole exported space into context.
- If no relevant index exists, continue with user-provided context and record missing source evidence as an open question.
- If multiple source IDs are plausible, choose the narrowest source that contains likely evidence and list the selection as an assumption.

For each selected source, record:

- `title`
- `path`
- `source_id`
- `status`
- `source_type`
- `reason`
- `confidence`: high | medium | low

## Clarification Loop

The skill must clarify rough input iteratively. Ask one question per turn, but ask as many turns as needed to reach a usable planning context.

Required readiness criteria:

- The problem can be stated in one clear sentence.
- The affected users, stakeholders, or decision makers are identified.
- The intended outcome is explicit.
- Non-goals or excluded scope are identified.
- Success or failure criteria are present.
- Important constraints, dependencies, risks, and assumptions are separated from confirmed facts.

If any readiness criterion is missing, ask the single highest-impact missing question before recommending `planning-draft`.

If the user cannot answer or asks to proceed anyway, keep the unresolved item in `open_questions`, mark related claims as assumptions, set `approval_state` to `needs_review`, and only then recommend the next skill.

## Question Delivery

When asking a user-facing clarification question, prefer an interactive choice tool if the runtime provides one.

- In Codex Plan mode, use `request_user_input` when the question can be answered with 2-3 mutually exclusive choices.
- In Claude Code, use `askUserQuestion` when that tool is available and the question can be answered with 2-3 mutually exclusive choices.
- Put the recommended option first and mark it as recommended.
- If no interactive question tool is available, ask the same question in plain Markdown with a compact option table.
- Use plain Markdown for open-ended questions that cannot be reduced to useful choices.

## Question Order

Ask only what is missing:

1. What problem are we solving?
2. Who is affected or deciding?
3. What outcome should change?
4. What is explicitly out of scope?
5. How will success or failure be judged?
6. What constraints or dependencies matter?
7. What direction is recommended and why?

## Output Schema

```yaml
planning_context:
  topic: ""
  one_line_problem: ""
  intended_outcome: ""
  users_or_stakeholders: []
  current_state: ""
  constraints: []
  evidence_sources:
    - title: ""
      path: ""
      source_id: ""
      status: current | draft | archive | unknown
      source_type: ""
      reason: ""
      confidence: high | medium | low
  confirmed_facts: []
  source_conflicts: []
  excluded_sources:
    - title: ""
      reason: ""
  non_goals: []
  success_criteria: []
  failure_criteria: []
  assumptions: []
  risks: []
  options:
    - name: ""
      pros: []
      cons: []
  recommended_direction: ""
  approval_state: draft | needs_review | aligned
  open_questions: []
```

## Rules

- Keep the workflow draft-only.
- Do not generate final planning artifacts until context is sufficiently clear.
- Do not invent missing facts.
- Mark unsupported claims as assumptions.
- Preserve evidence sources, source confidence, excluded sources, and source conflicts in `planning_context`.
- Treat indexed Confluence content as evidence, not as final approval.
- Prefer one focused question over a broad questionnaire.
- Continue the one-question loop until the context is ready, the user stops, or remaining gaps are explicitly marked as open questions.
- If the user wants artifacts immediately, provide a minimal context summary first.

## Response Format

Return:

- `Planning Context`
- `Known Decisions`
- `Assumptions`
- `Open Questions`
- `Recommended Next Skill`

The recommended next skill is usually `/planning-team-kit:planning-draft` or `$planning-draft`.
