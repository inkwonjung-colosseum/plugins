---
name: planning-check
description: "Check a planning context, rough plan, decision, or draft with focused one-question-at-a-time questions."
argument-hint: "[planning context, rough plan, decision, PRD draft, or source notes]"
---

# Planning Check

Use this optional skill when the user wants to check a planning decision before draft generation, review, or Confluence handoff planning.

## Invocation

Claude Code:

```text
/planning-team-kit:planning-check <plan or decision>
```

Codex:

```text
$planning-check <plan or decision>
```

## Purpose

Run a draft-only check for a planning context, rough plan, decision, PRD draft, or source notes. The goal is to expose missing decisions, weak assumptions, hidden dependencies, and unclear tradeoffs before `planning-draft`, `planning-review`, or `confluence-update-plan`.

`planning-check` is not a required workflow gate. It is an optional pre-draft or pre-handoff question step.

## Input Contract

Accept these input shapes:

- `planning_context`: structured context from `planning-start`
- `rough plan`: early proposal, meeting note, or product idea
- `decision request`: an unresolved option or tradeoff
- `draft artifact`: planning brief, requirements, behavior spec, PRD, brief, or a saved draft suite
- `source notes`: pasted evidence, links, meeting notes, or raw requirements

Always state the inferred input type before asking the first question.

If the input points to local files or a draft directory, inspect the available files before asking questions. If a question can be answered by reading provided source material or local workspace files, answer it from the source instead of asking the user.

## Check Loop

Ask one question at a time. Each question must include:

- the question
- why the answer matters
- the recommended answer or recommended direction
- what would change if the answer is different

After each user answer, update the working state:

- `resolved_decisions`
- `assumptions`
- `open_questions`
- `risks`
- `recommended_next_step`

Continue until one of these stop conditions is met:

- the plan is clear enough to proceed to `planning-draft`
- the plan should return to `planning-start`
- the draft is ready for `planning-review`
- the reviewed draft is ready for `confluence-update-plan`
- the user asks to stop
- the next question would be lower value than summarizing the state

## Question Delivery

When asking a user-facing check question, prefer an interactive choice tool if the runtime provides one.

- In Codex Plan mode, use `request_user_input` when the question can be answered with 2-3 mutually exclusive choices.
- In Claude Code, use `askUserQuestion` when that tool is available and the question can be answered with 2-3 mutually exclusive choices.
- Put the recommended answer first and mark it as recommended.
- If no interactive question tool is available, ask the same question in plain Markdown with a compact option table.
- Use plain Markdown for open-ended questions that cannot be reduced to useful choices.

## Question Selection

Ask the highest-impact unresolved question first. Prefer questions in this order:

1. What decision is this plan actually asking people to make?
2. Who is affected, approving, or blocked by this decision?
3. What user or business outcome must change?
4. What is explicitly out of scope?
5. What constraint, dependency, policy, or deadline can invalidate the plan?
6. What edge case or failure path would make the plan unsafe to execute?
7. What metric or evidence would prove the decision worked?
8. What option was rejected, and why?
9. What must be true before draft generation or handoff?

Do not run a broad questionnaire. Ask only the next question that changes the plan.

## Source Handling

- Separate confirmed facts from assumptions.
- If source evidence is unavailable, label the claim as an assumption.
- If available sources contradict the plan, surface the contradiction before asking the next question.
- If the answer is discoverable from local source files, inspect those files instead of asking the user.
- Do not invent requirements, owners, metrics, dates, or approval status.

## Relationship To Other Skills

- Use `planning-start` when the core problem, audience, intended outcome, non-goals, or success criteria are missing.
- Use `planning-draft` when the plan has enough context to generate the core draft artifact suite.
- Use `planning-review` when draft artifacts already exist and need a review gate.
- Use `confluence-update-plan` when a reviewed draft needs manual Confluence add/update instructions.

`planning-check` may recommend any of those skills, but it must not generate the standard draft suite or Confluence update plan itself.

## Rules

- Keep the workflow draft-only.
- Ask one question per turn.
- Provide a recommended answer with every question.
- Prefer source inspection over asking when the answer is discoverable.
- Do not require implementation details such as API endpoint, DB schema, concrete query, or instrumentation event unless the user-provided plan is specifically about implementation.
- Do not approve final publication or final decision-making.
- Do not rewrite the full document unless asked.
- Preserve unresolved items as open questions instead of filling gaps with guesses.

## Response Format

For the first response, return:

- `Input Type`
- `Known Context`
- `Current Risk`
- `Question 1`
- `Why It Matters`
- `Recommended Answer`
- `If Different`

For follow-up turns, return:

- `Updated State`
- `Next Question`
- `Why It Matters`
- `Recommended Answer`
- `If Different`

When stopping, return:

- `Resolved Decisions`
- `Assumptions`
- `Open Questions`
- `Risks`
- `Recommended Next Skill`

The recommended next skill is usually `/planning-team-kit:planning-start`, `/planning-team-kit:planning-draft`, `/planning-team-kit:planning-review`, or the Codex equivalents `$planning-start`, `$planning-draft`, `$planning-review`.

## Attribution

This skill is inspired by Matt Pocock's MIT-licensed `grill-me` skill concept and adapts it for the `planning-team-kit` draft-only planning workflow.
