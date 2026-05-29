# Output Contract

## Chat Summary

Keep the chat response short:

- conclusion in 5 lines or fewer
- Top 5 Archive or mismatch candidates
- folder with the most candidates
- holds and risk items
- detailed report path or link

## Report Sections

Use only sections relevant to the requested mode:

1. `## 결론` — end with a `다음 감사 권장: YYYY-MM-DD` line
2. `## 감사 메타` (mandatory, immediately after `## 결론`) — `audit_date` (today, ISO 8601), `audit_mode` (full-tree | freshness-only | single-folder), `scope`, `next_recommended_run` (full-tree/sprint-close = today + 14 days; freshness-only = today + 30 days; single-folder = judgment)
3. `## Coverage`
4. `## Tree Gap` when SSOT-defined folders are missing in the live tree (for example `06. 장애 / Incident`)
4b. `## 신규 Subfolder 탐지` (produced by SKILL.md workflow step 3b — same section, step number differs by skill convention only) when a live subfolder exists that is not on the known-subfolder list (folder, subfolder title, pageId, page count) — for `colonova-doc-router-publisher` to update its Subfolder Routing table and folder-id-map Known Subfolders
5. `## 최신화 후보` in freshness mode, or whenever stale living standards are found. In freshness mode this section is never omitted: if zero stale candidates are found, output a single all-clear line instead — `모든 living standard가 freshness 임계값 이내입니다 (감사 기준일: <today>). 다음 freshness 점검 권장일: <today+30d>.` The 최신화 후보 queue contains published pages only; route any draft to `Manual review` instead.
6. `## Pending supersession 후보` — list old pages from a started-but-incomplete supersession cycle (the new page links the old as superseded, but the old page has no SUPERSEDED banner/status); emit whenever at least one such candidate exists
6b. `## Manual review 후보` — include whenever a `Discussion closure incomplete` item or a `Manual review (workflow stale)` Design Review is found (workflow steps 6b and 7). Sub-cases: `Discussion closure incomplete` (a `04` page links an `08` decision page but the discussion was never marked `RESOLVED`) and `Manual review (workflow stale)` (an `02` Under Review Design Review past 90 days). Also list any draft routed here from a freshness queue. In freshness mode, when zero such items are found, output a single all-clear line instead — `Manual review 대상 항목 없음 (감사 기준일: <today>).` — so the section is never omitted silently; in archive/full-tree mode, omit the section when empty.
7. `## Archive 후보`
8. `## Archive 보류/제외`
9. `## Placement review` only when requested
10. `## 실행 큐`
11. `## Confluence 복붙용 실행 표`
12. `## 이전 감사 대비 변화` optional, only in delta mode when a prior report is provided
13. `## 특수 항목과 제한 사항` — list draft, whiteboard, unread, title-only, local-only, and any partial-fetch folders (folders whose descendants failed midway through cursor pagination)

Do not include a full folder-by-folder document type inventory unless the user explicitly asks for it.

## Candidate Tables

| 현재 폴더 | 페이지 | Archive 이유 | 대체/현재 기준 문서 | 확신도 | 근거 |
| --- | --- | --- | --- | --- | --- |

최신화 후보 표 (freshness mode):

| 현재 폴더 | 페이지(ID) | last_modified | staleness_days | 갱신 필요 이유 | 확신도 |
| --- | --- | --- | --- | --- | --- |

`doc_role`: `living_standard` (`05. 기술문서`, `08. 결정사항`, `12. 운영 가이드`), `design_standard` (`02. 시스템 디자인` Approved Design Reviews, 180-day window), and `monitoring_standard` (`07. 모니터링` pages stating SLI/SLO or alert thresholds, 180-day window) are the `Refresh required` freshness-tracked roles. A `01. 시스템 분석` page with 2+ `변경 이력` rows, or a `09. 스케쥴링` roadmap/milestone page with 2+ `변경 이력` rows, is a `Manual review` freshness candidate (365-day window), not `Refresh required`.

Pending supersession 후보 표:

| 구 페이지(ID) | 구 페이지 제목 | 대체 신규 페이지(ID) | 미완료 사유 | 확신도 |
| --- | --- | --- | --- | --- |

이전 감사 대비 변화 표 (delta mode):

| 변화 유형 | 페이지(ID) | 이전 상태 | 현재 상태 | 비고 |
| --- | --- | --- | --- | --- |

변화 유형: `신규`(this run only), `해소`(resolved since prior), `재등장`(reappeared), `악화`(worsened).

| 현재 폴더 | 페이지 | 현재 성격 | 추천 대상 | Action | 확신도 | 근거 |
| --- | --- | --- | --- | --- | --- | --- |

| 큐 | 페이지(ID) | Action | 필요한 확인 | 비고 |
| --- | --- | --- | --- | --- |

| 우선순위 | 현재 폴더 | 페이지(ID) | 현재 성격 | 추천 위치 | Action | 확신도 | 비고 |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Self-Check

Before final output, verify internally:

- fixed root `933068815` or access failure is stated
- coverage numbers exist
- matching pages are not listed as inventory
- each candidate has page ID, source, body status, classification basis, confidence
- each candidate has at least two evidence points unless marked low confidence
- Move, companion, Extract, Convert, Refresh required, and Archive are separated
- Refresh required is used for stale living standards, stale Approved Design Reviews (`design_standard`), and stale `07` monitoring-standard pages (`monitoring_standard`), not Archive
- Archive has replacement, current reference, or retirement evidence
- immediate, extraction, 최신화, Pending supersession, Archive, manual, and dangerous queues are separated
- SSOT-vs-live folder gaps are reported in `## Tree Gap` when any defined folder is missing
- any live subfolder not on the known-subfolder list is reported in `## 신규 Subfolder 탐지`
- draft, whiteboard, unread, local-only, and fetch failures are separated
- no draft page appears in the 최신화 후보 queue (drafts go to Manual review)
- any partial-fetch folder is named in `## 특수 항목과 제한 사항` and flagged with `partial-fetch` in coverage; if ≥30% of folders are partial-fetch, `## 결론` states confidence `저 (partial coverage)`
- `audit_date` and `next_recommended_run` are present in `## 감사 메타`, and `## 결론` ends with a `다음 감사 권장: YYYY-MM-DD` line
- when a prior report was provided or auto-selected, the picked file is named and an `오버듀` note is added in `## 감사 메타` if today is on or after that report's next_recommended_run
- in freshness mode, `## 최신화 후보` is always present — either with candidates or with the all-clear statement
- a `09. 스케쥴링` page with 2+ `변경 이력` rows (living roadmap) over 365 days is flagged as `Manual review`, not left freshness-blind
- `## Pending supersession 후보` is present whenever the sweep found at least one half-completed supersession cycle, and the sweep covered `05`, `08`, `12`, and ADR pages
- `## Manual review 후보` is listed in the Report Sections (item 6b) and is emitted whenever any `Discussion closure incomplete` or `Manual review (workflow stale)` item exists; in freshness mode it is never omitted silently (all-clear line when empty)
- any `Discussion closure incomplete` item (a `04` page linking a decision page but not marked `RESOLVED`) is included under `## Manual review 후보`
- any `Under Review` Design Review past 90 days is listed as `Manual review (workflow stale)`, separate from `Refresh required`
- read-only default is preserved
