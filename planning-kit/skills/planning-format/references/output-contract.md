# Output Contract

Final output is the artifact handoff, not an execution log. Start with `# [기능명]`.

## Header

- 입력: human-readable source summary
- 산출물: 정책서, 기능설계서
- 검증: 확인 필요 N건, 문서 보강 M건, 출처 누락 K건 / 확인 필요 없음 / 생략 (--no-self-review)
- 저장: `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/`, `없음 (--no-save)`, or `실패 - reason`

## Save success

Show only:

1. header
2. `## 저장 파일`
3. `## 체크해야 할 항목`

Do not print full policy or feature bodies on save success.

## No-save

Show:

1. header
2. `## 정책서`
3. `## 기능설계서`
4. `## 체크해야 할 항목`

## Save failure

Print the same body as no-save, then `## 저장 실패 상세` with failed step, target path, and remaining files/folders if known.

## Checklist

Use these subsections in order:

1. `### 결정 필요`
2. `### 문서 보강 필요`
3. `### 출처/누락 참고`

Empty subsection value is `없음`. Checklist items use:

- 확인할 것:
- 이유:
- 반영 위치:

No raw F* dump, connector stack trace, wide table, or full URL table in the default checklist.

## Trace

`## 출처/누락 요약` and `## 상세 추적` are allowed only for no-save or save-failure output, or when trace materially changes trust. Keep save-success output compact.

## Save path

Default is save-on. `--save` is a compatibility no-op. Only `--no-save` disables writing. Resolve collisions with `--2`, `--3`, etc.

Use clean display labels such as `정책서 5.1`, `기능설계서 7`, `입력 제외 섹션`, `보조 표`, `여정 표`, `상태 전이 표`, `메시지 표`. Reference requirement IDs with their prefix (e.g., `POL-001`, `FUNC-002`, `AC-003`, `DATA-004`, `API-005`, `NFR-PERF`, `TEST-006`, `RSK-007`, `BIZ-008`, `DEC-009`).

## Requirement ID surfacing

When the checklist references a missing or unresolved item that already has an ID, include the ID in the item's `반영 위치` field. When the body assigns an ID but evidence is missing, mention the ID in `## 출처/누락 요약` (no-save/save-failure outputs only).
