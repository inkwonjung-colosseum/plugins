# Review Gate

Use this reference to decide whether a `plan-format` output is ready for external publishing.

`plan-review` must use parallel fresh-context reviewers for every review. Each reviewer starts from the target file and local evidence, not from the conversation that produced the draft.

## Required Review Inputs

- The target draft file path.
- The full draft read directly from disk by each fresh-context reviewer.
- Any source documents named by the draft.
- Additional local Confluence files only when needed to verify a concrete claim.
- The reviewer role and perspective-specific scope.

The current conversation is not evidence. If a fact is only known from conversation context and is absent from the draft or selected source files, treat it as missing evidence.

## Reviewer Roles

### Evidence reviewer

Checks source support, Confluence conflicts, unsupported assumptions, stale evidence, and `[가정]` items that affect publish readiness.

### Scope reviewer

Checks remaining `[미정]` items, missing decisions, missing sections, affected cases, and unsupported document types.

### Implementation readiness reviewer

Checks whether development or operations can act on the draft without conversation memory, including conditions, states, exceptions, permissions, APIs, data fields, and QA specificity when relevant.

### Template completeness reviewer

Checks required sections for the document type and whether source intent is preserved when the source input is named. If the source input is not available, source-intent claims remain unsupported.

## Required Reviewer Output

- Review method: `parallel fresh-context reviewer`.
- Reviewer role.
- Target file path.
- Evidence files read.
- Findings for the assigned role.
- Role verdict: `pass`, `conditional pass`, or `수정 필요`.
- Minimum required changes or confirmation condition, when applicable.

## Verdict Reconciliation

The main context may format and summarize reviewer output, but it may not relax any reviewer's verdict without file-based evidence.

The final verdict uses the most conservative Role verdict. Conservative order: `수정 필요 > conditional pass > pass`.

- If any reviewer returns `수정 필요`, final verdict is `수정 필요`.
- Otherwise, if any reviewer returns `conditional pass`, final verdict is `conditional pass`.
- Final verdict is `pass` only when all four reviewers return `pass`.

If the main context and fresh-context reviewers disagree, use the more conservative verdict:

1. `수정 필요`
2. `conditional pass`
3. `pass`

## Blocking Signals

The following signals require a clear verdict before publish:

- `[미정]`
- `[가정]`
- `충돌 경고`

## Verdicts

### pass

Use `pass` when there are no material `[미정]`, `[가정]`, or conflict issues left, and the draft is specific enough for development or operations to act on.

### conditional pass

Use `conditional pass` when remaining issues are explicit and acceptable for the planner to acknowledge before publish. State the exact condition in one sentence.

### 수정 필요

Use `수정 필요` when a missing decision, conflict, unclear rule, or unsupported assumption would cause implementation or operational ambiguity.

## Review Boundaries

- Do not rewrite the draft directly.
- Point to the minimum set of changes needed.
- Do not use conversation memory as evidence.
- Treat archive documents as historical context, not current policy.
- If local evidence is stale or insufficient, say which evidence is missing rather than filling the gap with assumptions.
