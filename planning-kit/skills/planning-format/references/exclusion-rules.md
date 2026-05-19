# Exclusion Rules

Use after conversion to track every input fragment that did not enter the policy or feature document.

## Categories

- duplicate
- out of scope
- structural conversion
- fetch failed
- source definition missing
- ambiguous term
- conflict candidate
- other feature candidate
- unsupported media
- detail summarized
- unmapped label

## Record shape

Each meaningful exclusion keeps five fields:

- source:
- location:
- category:
- handling:
- reason:

## Rules

- Catch-all: every non-empty input fragment is either in a document or in exclusions.
- Use only `[TBD]` as the uncertainty marker. Do not use `[미정]`, `[가정]`, `[확인 필요]`, or `해당 없음`.
- Empty rows and empty sections may be removed.
- If a fetch failure affects user flow, screen evidence, integration behavior, or policy authority, surface it in `체크해야 할 항목 > 출처·누락 참고`.
- If a source says something is excluded from scope, mirror it in document scope and exclusion tracking.
- If a document field says source definition is missing, add a matching `source definition missing` exclusion.
