---
name: quality-review
description: "Review draft planning documents against the shared quality rubric."
argument-hint: "<planning document or document suite>"
---

# Quality Review

Use this skill to inspect a draft planning document suite before handoff.

## Invocation

Claude Code:

```text
/planning-team-kit:quality-review <document>
```

Codex:

```text
$quality-review <document>
```

## Purpose

Apply a draft-only multi-agent review gate. The goal is not copyediting. The goal is to find ambiguity, missing decisions, unsupported claims, and handoff risks through independent reviewer perspectives.

## Input Contract

Accept these input shapes:

- `full standard suite`: the generated suite directory or all standard files are available.
- `partial suite`: two or more generated planning documents are available, but one or more standard files are missing.
- `single document`: one planning document or pasted draft is available.

The standard suite files are:

- `00-planning-context.md`
- `01-brief.md`
- `02-prd.md`
- `03-user-stories.md`
- `04-feature-spec.md`
- `05-metrics-brief.md`

Rules:

- Always state `Input Type`, `Documents Reviewed`, and `Documents Missing`.
- Prefer full-suite review when the user provides a saved `planning-drafts` directory.
- For `partial suite` or `single document`, disclose coverage limits and do not invent findings for documents that were not provided.
- If the missing context prevents a useful review, return `needs revision` and recommend `planning-intake`.
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
- Gate 2: consistency and execution. Check that PRD requirements, user stories, feature behavior, metrics, non-goals, owners, and next actions do not conflict and can support handoff without guessing.
- Gate 3: evidence and governance. Check that unsupported claims are marked as assumptions, metrics are measurable, sensitivity and approval state are explicit, and the draft does not imply final approval.

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

Do not use average score alone to determine the verdict. A critical failure, final-approval implication, missing core planning context, unsupported decision-driving claim, or unmeasurable primary success metric forces `needs revision` even when most scores are high.

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

- Product Context Reviewer: review `00-planning-context.md`, `01-brief.md`, and `02-prd.md` for problem clarity, audience clarity, goal/non-goal separation, requirement completeness, and decision traceability.
- Story & Testability Reviewer: review `02-prd.md` and `03-user-stories.md` for requirement testability, story clarity, acceptance criteria quality, and edge or negative case coverage.
- Feature Behavior & Policy Reviewer: review `02-prd.md` and `04-feature-spec.md` for user flow, screen or surface behavior, state and policy rules, permission rules, rollout expectations, reversibility, and error states.
- Metrics & Evidence Reviewer: review `00-planning-context.md`, `02-prd.md`, and `05-metrics-brief.md` for metric verifiability, guardrails, observation window, segment, decision rule, evidence quality, and assumption separation.
- Cross-Artifact Consistency Reviewer: review the full suite for PRD requirement to user story to feature spec to metrics traceability, non-goal leakage, conflicting scope, and contradictory decisions.
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
- If core planning context is missing, recommend `planning-intake`.
- If any critical failure is present, return `needs revision` regardless of score totals.
- If the suite is usable with named conditions, use `conditional pass` and recommend the smallest fix.
- If the suite is ready for downstream handoff as a draft, state that no next skill is required and the reviewed draft can be shared by the human owner.

## Fallback Mode

If the execution environment cannot create subagents, do not skip the role split. Run the same six reviewer roles sequentially as a checklist and set `Review Execution Mode` to `sequential fallback`.

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

The recommended next skill is usually `/planning-team-kit:planning-intake` or `$planning-intake` when core context needs more clarification. When the reviewed draft is ready for human handoff, return `No next skill required`.
