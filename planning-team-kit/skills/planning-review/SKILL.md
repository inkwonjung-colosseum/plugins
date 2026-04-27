---
name: planning-review
description: "Review draft planning documents against the shared quality rubric."
argument-hint: "<planning document or document suite>"
---

# Planning Review

Use this skill to inspect a draft planning document suite before handoff.

## Invocation

Claude Code:

```text
/planning-team-kit:planning-review <document>
```

Codex:

```text
$planning-review <document>
```

## Purpose

Apply a draft-only multi-agent review gate. The goal is not copyediting. The goal is to find ambiguity, missing decisions, unsupported claims, and handoff risks through independent reviewer perspectives.

## Input Contract

Accept these input shapes:

- `full standard suite`: the generated suite directory or all standard files are available.
- `partial suite`: two or more generated planning documents are available, but one or more standard files are missing.
- `single document`: one planning document or pasted draft is available.

The standard suite files are:

- `00-index.md`
- `01-planning-brief.md`
- `02-requirements.md`
- `03-behavior-spec.md`

Rules:

- Always state `Input Type`, `Documents Reviewed`, and `Documents Missing`.
- Prefer full-suite review when the user provides a saved `planning-draft` directory.
- For `partial suite` or `single document`, disclose coverage limits and do not invent findings for documents that were not provided.
- If the missing context prevents a useful review, return `needs revision` and recommend `planning-start`.
- If a provided path points to a directory, read all standard files present before judging individual documents.

## Rubric

Check these axes:

- Problem clarity
- Audience clarity
- Requirement completeness
- Exception and policy coverage
- Metric verifiability
- Evidence quality
- Structural consistency
- Execution readiness

## Gate Results

Report Gate 0-3 as `pass`, `warn`, or `fail`. Use `warn` when the draft is reviewable but has named limits or non-blocking gaps.

- Gate 0: scope fit. Check that the input is a planning artifact, the input type is clear, required documents are present or explicitly missing, and draft-only status is preserved.
- Gate 1: basic completeness. Check for problem, audience, goals, non-goals, requirements, success criteria, and separated open questions.
- Gate 2: consistency and execution. Check that requirements, acceptance criteria, behavior rules, non-goals, owners, and next actions do not conflict and can support handoff without guessing.
- Gate 3: evidence and governance. Check that unsupported claims are marked as assumptions, validation expectations are reviewable, sensitivity and approval state are explicit, and the draft does not imply final approval.

Gate outcomes inform the final verdict:

- Any Gate 0 `fail` or critical failure returns `needs revision`.
- Any blocking Gate 1-3 issue returns `needs revision`.
- `warn` gates can return `conditional pass` when the suite is usable with named fixes.
- All gates must be `pass` for `pass`.

## Quality Scores

Score each rubric axis with the shared 0/1/2 model:

- `0`: missing, contradictory, unsupported, or not usable for draft handoff.
- `1`: present but vague, partial, weak, or requires interpretation.
- `2`: explicit, verifiable, aligned, and usable for draft handoff.

Do not use average score alone to determine the verdict. A critical failure, final-approval implication, missing core planning context, unsupported decision-driving claim, or unreviewable validation expectation forces `needs revision` even when most scores are high.

## Review Orchestration

Act as the review orchestrator.

1. Read the full document suite before judging individual files.
2. Split the review across the reviewer agents below when the environment supports subagents.
3. Ask each reviewer to inspect only its assigned scope and return prioritized findings.
4. If subagents are not available, run the same reviewer roles sequentially and label the mode as `sequential fallback`.
5. Consolidate reviewer outputs into one final verdict.
6. Keep the review draft-only and do not imply final approval.

## Reviewer Agents

Use these fixed reviewer roles:

- Product Context Reviewer: review `00-index.md` and `01-planning-brief.md` for problem clarity, audience clarity, goal/non-goal separation, decision traceability, and open question quality.
- Story & Testability Reviewer: review `02-requirements.md` for requirement testability, acceptance criteria quality, and edge or negative case coverage.
- Feature Behavior & Policy Reviewer: review `02-requirements.md` and `03-behavior-spec.md` for user flow, screen or surface behavior, state and policy rules, permission rules, reversibility, and error states.
- Metrics & Evidence Reviewer: review `00-index.md`, `01-planning-brief.md`, and `02-requirements.md` for evidence quality, validation expectations, source quality, and assumption separation.
- Cross-Artifact Consistency Reviewer: review the full suite for planning brief to requirements to behavior spec traceability, non-goal leakage, conflicting scope, and contradictory decisions.
- Handoff Governance Reviewer: review the full suite for owners, unresolved issues, dependencies, risks, next actions, sensitivity, approval state, decision-required consistency, and handoff blockers.

Each critical finding must use this shape:

- `reviewer`
- `severity`
- `document`
- `section`
- `location`
- `evidence`
- `issue`
- `why it matters`
- `suggested fix`

Use these severity values:

- `critical`: blocks draft handoff and forces `needs revision`.
- `major`: may allow `conditional pass` when the fix is clear and bounded.
- `minor`: non-blocking improvement.

## Consolidation Rules

- Use `pass`, `conditional pass`, or `needs revision`.
- Prefer the higher handoff risk when reviewer findings conflict.
- Record reviewer disagreement or tradeoffs under `Conflict Resolution`.
- Deduplicate repeated findings and keep only the highest-impact issues.
- If core planning context is missing, recommend `planning-start`.
- If any critical failure is present, return `needs revision` regardless of score totals.
- If the suite is usable with named conditions, use `conditional pass` and recommend the smallest fix.
- If the suite is ready for manual Confluence update planning, recommend `confluence-update-plan`.

## Local Review Persistence

When the input is a saved draft directory, save the consolidated review result into that directory as:

```text
04-planning-review.md
```

Rules:

- Do not overwrite unrelated files.
- Include the verdict, gate results, reviewer summary, critical findings, unsupported claims, highest-impact question, and suggested fixes.
- Use only these final verdict values: `pass`, `conditional pass`, `needs revision`.
- If the verdict is `needs revision`, do not recommend `confluence-update-plan`; recommend `planning-start`, `planning-check`, or `planning-draft` based on the smallest needed fix.
- If the input is not a local directory, return the review in the response and state that no review file was saved.

## Fallback Mode

If the execution environment cannot create subagents, do not skip the role split. Run the same six reviewer roles sequentially as a checklist and set `Review Execution Mode` to `sequential fallback`.

## Question Delivery

When asking the highest-impact follow-up question, prefer an interactive choice tool if the runtime provides one.

- In Codex Plan mode, use `request_user_input` when the question can be answered with 2-3 mutually exclusive choices.
- In Claude Code, use `askUserQuestion` when that tool is available and the question can be answered with 2-3 mutually exclusive choices.
- Put the recommended answer first and mark it as recommended.
- If no interactive question tool is available, ask the same question in plain Markdown with a compact option table.
- Use plain Markdown for open-ended questions that cannot be reduced to useful choices.

## Rules

- Do not approve final publication.
- Do not rewrite the full document unless asked.
- Mark unsupported claims as assumptions.
- Use `pass`, `conditional pass`, or `needs revision`.
- Use `multi-agent` or `sequential fallback` for `Review Execution Mode`.
- Include the strongest reason for each finding.
- Include document location and evidence for each critical finding when possible.
- Ask at most one highest-impact follow-up question.
- Do not ask reviewers to design outside their assigned scope.
- Do not require implementation design details such as API endpoint, DB schema, concrete query, or instrumentation event.
- Do not turn Feature Spec review into backend architecture review.
- Save `04-planning-review.md` when reviewing a local draft suite directory.
- Do not recommend `confluence-update-plan` when the verdict is `needs revision`.

## Response Format

Return:

- `Input Type`
- `Documents Reviewed`
- `Documents Missing`
- `Verdict`
- `Review Execution Mode`
- `Gate Results`
- `Agent Review Summary`
- `Critical Findings`
- `Conflict Resolution`
- `Quality Scores`
- `Unsupported Claims`
- `Highest-Impact Question`
- `Suggested Fixes`
- `Recommended Next Skill`

The recommended next skill is usually `/planning-team-kit:planning-start` or `$planning-start` when core context needs more clarification. When the reviewed draft is ready for manual Confluence update planning, recommend `/planning-team-kit:confluence-update-plan` or `$confluence-update-plan`.
