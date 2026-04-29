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

## Confluence Evidence Selection

When a reviewer needs local Confluence evidence, use the repo reading rule:

1. Start from `.confluence-index/registry.json` to choose the relevant export source.
2. Read `.confluence-index/sources/<source-id>/source-index.jsonl` to locate candidate pages and metadata.
3. Use `.confluence-index/sources/<source-id>/tree.md` to understand the source hierarchy.
4. Select the smallest relevant raw exported Markdown file for the concrete claim being checked.
5. Read the raw exported Markdown before making claims.

Do not load a whole exported space. Treat local exported Markdown as a read-only snapshot of Confluence. If the index or page metadata is missing, report `metadata unavailable` and do not infer status or freshness.

## Reviewer Roles

### 근거 reviewer (Evidence reviewer)

Checks source support, Confluence conflicts, unsupported assumptions, stale evidence, and `[가정]` items that affect publish readiness.

### 결정·범위 reviewer (Decision-scope reviewer)

Checks remaining `[미정]` items, missing decisions, decision owner or follow-up action, affected and excluded cases, unsupported document types, and related 정책서/기능설계서 trace links.

### 실행·검증 가능성 reviewer (Execution-readiness reviewer)

Checks whether development, operations, and QA can act on the draft without conversation memory, including conditions, states, exceptions, permissions, business integration boundaries, business data, external channels, failure handling, operational impact, and acceptance criteria / confirmation criteria when relevant.

## Required Reviewer Output

- Review method: `parallel fresh-context reviewer`.
- Reviewer role.
- Target file path.
- Evidence files read, including `source-id`, `raw exported Markdown path`, `current/draft/archive` status, and `stale` assessment for each local Confluence source.
- Use `metadata unavailable` when source metadata, document status, or freshness cannot be verified from the local export.
- Findings for the assigned role.
- Role verdict: `pass`, `conditional pass`, or `수정 필요`.
- Minimum required changes or confirmation condition, when applicable.

## Verdict Reconciliation

The main context may format and summarize reviewer output, but it may not relax any reviewer's verdict without file-based evidence.

The final verdict uses the most conservative Role verdict. Conservative order: `수정 필요 > conditional pass > pass`.

- If any reviewer returns `수정 필요`, final verdict is `수정 필요`.
- Otherwise, if any reviewer returns `conditional pass`, final verdict is `conditional pass`.
- Final verdict is `pass` only when all three reviewers return `pass`.

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
