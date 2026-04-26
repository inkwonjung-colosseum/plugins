---
name: planning-intake
description: "Run structured brainstorming and planning alignment before generating artifacts."
argument-hint: "[idea, note, meeting summary, or rough requirement]"
---

# Planning Intake

Use this skill before generating planning documents. It turns rough input into a structured planning context.

## Invocation

Claude Code:

```text
/planning-team-kit:planning-intake <idea or notes>
```

Codex:

```text
$planning-intake <idea or notes>
```

## Purpose

Run the front-of-funnel planning brainstorm without jumping straight to a PRD. The output is draft-only planning context that downstream skills can use.

## Process

1. Identify the current input type: idea, meeting note, rough requirement, existing draft, or decision request.
2. Extract what is already known.
3. Build a draft `planning_context` from the known information.
4. Check whether the context is ready for artifact generation.
5. Ask one high-leverage question at a time only when the answer changes the plan.
6. Update the `planning_context` after each answer.
7. Repeat the readiness check and question loop until the context is clear enough for artifact generation, the user asks to stop, or the user cannot provide more information.
8. Compare 2-3 viable directions when there is a meaningful choice.
9. Produce a concise planning context.
10. Stop before artifact generation if the context is still too ambiguous.

## Clarification Loop

The skill must clarify rough input iteratively. Ask one question per turn, but ask as many turns as needed to reach a usable planning context.

Required readiness criteria:

- The problem can be stated in one clear sentence.
- The affected users, stakeholders, or decision makers are identified.
- The intended outcome is explicit.
- Non-goals or excluded scope are identified.
- Success or failure criteria are present.
- Important constraints, dependencies, risks, and assumptions are separated from confirmed facts.

If any readiness criterion is missing, ask the single highest-impact missing question before recommending `planning-drafts`.

If the user cannot answer or asks to proceed anyway, keep the unresolved item in `open_questions`, mark related claims as assumptions, set `approval_state` to `needs_review`, and only then recommend the next skill.

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

The recommended next skill is usually `/planning-team-kit:planning-drafts` or `$planning-drafts`.
