# Review Gate

Use this reference to decide whether a `plan-draft` output can proceed to `plan-publish`.

## Required Review Inputs

- The full draft from the current conversation.
- Any source documents named by the draft.
- Additional local Confluence files only when needed to verify a concrete claim.

## Blocking Signals

The following signals require a clear verdict before publish:

- `[미정]`
- `[가정]`
- `충돌 경고`
- `Publish gate: review-required`

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
- Treat archive documents as historical context, not current policy.
- If local evidence is stale or insufficient, say which evidence is missing rather than filling the gap with assumptions.
