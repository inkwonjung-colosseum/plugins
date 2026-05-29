---
name: colonova-engineering-docs-audit
description: Use when read-only로 ColoNova Engineering Confluence 8.8 ColoNova 트리를 감사할 때 — Archive 후보, 위치 불일치, 추출/전환 후보, 실행 큐, stale 기준 문서·최신화(freshness) 후보 식별. 특정 page ID 없이 "유지보수 해줘"·"최신화 해줘"·"트리 정리해줘"·"스프린트 끝났어 ColoNova 정리"·"문서 상태 점검" 같은 broad cleanup·정기 점검 진입어에 발동. delta(이전 감사 대비 변화), Pending supersession(구 페이지 SUPERSEDED 미완료), Discussion closure incomplete(논의사항 RESOLVED 미처리), Under Review 디자인 리뷰 정체 탐지도 포함.
---

# ColoNova Engineering Docs Audit

Use this skill only for the ColoNova Engineering Confluence tree rooted at `8.8 ColoNova`.

Fixed target:

- URL: `https://colosseum.atlassian.net/wiki/spaces/COLO/pages/933068815/8.8+ColoNova`
- root page ID: `933068815`
- space key: `COLO`
- space name: `[팀]Engineering`

## Scope

This skill audits the current tree and returns evidence-backed recommendations. It never moves, edits, archives, or creates Confluence pages.

Modes:

- Archive recommendation (default): Archive candidates and execution queue.
- Placement review: included when the user asks for folder movement, mismatch, relocation, reclassification, extraction, conversion, or companion review.
- Freshness audit: triggered when the user mentions 최신화, freshness, stale, 오래된 문서, 갱신 필요, `07 SLO 기준`, `design review 최신화`, or `DR 갱신`. Surfaces living standards (`05`, `08`, `12`), Approved Design Reviews in `02` (`design_standard`, 180-day window), and `07. 모니터링` pages stating SLI/SLO or alert thresholds (`monitoring_standard`, 180-day window) past their freshness threshold as `Refresh required` candidates rather than Archive.

This skill is the recurring maintenance entry point for the tree. It identifies what to act on; `colonova-engineering-docs-publish` performs the actual refresh/update with the page ID.

### Combined intent (audit + 갱신)

When the user asks for both auditing and updating in one request (for example "유지보수 해줘", "최신화 해줘", "트리 정리하고 오래된 문서도 갱신해줘"), enter this skill first: run the audit, build the execution queues, then ask whether to hand the `최신화 후보`/`바로 실행 후보` page IDs to `colonova-engineering-docs-publish`. Do not jump straight to publishing. The user goes directly to `colonova-engineering-docs-publish` only when they already have a specific page ID and a clear update intent (no audit needed).

## Maintenance Cadence

This is a continuous-maintenance tool, not a one-off utility. Recommended recurring use:

- Every sprint close (about 2 weeks): full-tree audit for Archive, placement, and tree gaps.
- Monthly: freshness-only audit of living standards (`05`, `08`, `12`), `07. 모니터링` SLO/threshold pages, and Approved `02` Design Reviews for stale documents.
- Ad hoc: single-folder spot-check when one folder grew quickly or a specific document is suspected stale.

Execution modes the user can request:

| Mode | What it does | Typical trigger |
| --- | --- | --- |
| full-tree audit | whole tree, all queues | sprint close, broad cleanup |
| freshness-only | staleness of living standards | monthly refresh review |
| single-folder spot-check | one folder, fast | a folder grew or looks stale |

For delta-aware runs, the user may provide a prior report path; compare against it and summarize changes (see Inputs and Output).

To turn the recommended cadence from advisory into a working loop, do two things:

1. Save the broad-audit local report with the convention `colonova-audit-YYYY-MM-DD.md` (date = audit_date) in the export directory. On the next run, if no prior report path is given, auto-select the most recent `colonova-audit-*.md` in the same directory as the prior report for delta mode (state which file was picked). Also compare its `next_recommended_run` against today: if today is on or after that date, add an `오버듀: 지난 권장 감사일(<date>)을 경과했습니다` note in `## 감사 메타`; if the prior file's date is far older than its own recommended cadence, flag the gap.
2. After completing the report, append a one-line prompt offering to register the cadence: `다음 감사 권장일 <next_recommended_run>을 /schedule로 등록하시겠습니까? (예: "매 스프린트 종료마다 colonova-engineering-docs-audit 전체 트리 감사")`. If the user agrees, point them to Claude Code's `/schedule` skill — for example "매 스프린트 종료마다 colonova-engineering-docs-audit 전체 트리 감사 실행" or "매월 1일 freshness 모드 점검". The skill itself never registers the cron; it only proposes the prompt.

## Inputs

Do not ask for the Confluence root or site. Ask only when the request does not reveal:

- audit scope: whole tree, one folder, or specific candidate pages
- audit mode: archive (default), placement review, or freshness
- output format: chat summary, Confluence-ready table, or local Markdown report
- optional local export path for body fallback
- whether placement review should be included
- prior report path (optional, for delta mode comparison). If not given, auto-select the most recent `colonova-audit-*.md` in the export directory as the prior report and state which file was picked.

## Workflow

1. Read live root page `933068815` and any linked classification guide. If live criteria cannot be read, report the failure and keep confidence low.
2. Fetch descendants deeply enough to include nested pages. Repeat the fetch until cursor pagination is exhausted (descendants beyond ~100 are paginated). If folder descendants fail, reconstruct folder subtrees from root descendant `parentId`, `depth`, title, and ordering. If a mid-stream cursor fetch fails: on HTTP 429 (rate limit) pause briefly and retry the same cursor up to twice before giving up; on a persistent 4xx (non-429) / 5xx / timeout, mark that folder `partial-fetch`, record the range collected and HTTP status, and do not include its pages in Archive 후보 or `Refresh required` queues (insufficient basis). If 30% or more of folders are `partial-fetch`, set audit confidence to `저 (partial coverage)` in `## 결론` and recommend re-running (see `references/confluence-tree-audit.md` Pagination).
3. Compare the SSOT classification table (13 folders) against live top-level folders. Report any defined-but-missing folder (currently `06. 장애 / Incident`) under `## Tree Gap`. Match folders by `NN.` number prefix; live titles carry a ` - ColoNova` suffix. Optional cache refresh: `colonova-engineering-docs-publish/references/folder-id-map.md` already carries the 13 top-level folder pageIds and the 5 known-subfolder pageIds, all resolved live on 2026-05-29. If a cached ID no longer resolves to the expected folder/subfolder (the tree is actively maintained), you may overwrite that row with the corrected numeric ID. This is optional and best-effort — only when the runtime supports persistent local file writes and the file survives between sessions; if a write is unsupported or fails, skip it silently and continue (never error out, never block the audit).
3b. New subfolder drift detection (produces `## 신규 Subfolder 탐지`, output-contract.md section 4b): for each top-level folder, compare its live immediate child subfolders against the known-subfolder list (`colonova-engineering-docs-publish/references/folder-id-map.md` → Known Subfolders, and `routing-rules.md` → Subfolder Routing — only `03`, `04`, `05` carry subfolders as of 2026-05-29, with their pageIds now confirmed in folder-id-map). A row with a confirmed numeric pageId is already cached and known; only flag subfolders absent from this list. If a live subfolder is present that is not on the known list, surface it under `## 신규 Subfolder 탐지` (folder, subfolder title, pageId, page count). This closes the drift loop: `colonova-engineering-docs-publish` delegates new-subfolder discovery to this audit, so the routing taxonomy (Subfolder Routing table + folder-id-map Known Subfolders) can be updated on the next routing run. If the known list is unreadable, note it and skip silently — do not block the audit.
4. Build one folder packet per top-level folder: folder ID, criteria, descendant IDs, nested folder boundaries, special items such as draft or whiteboard, and each page's `last_modified` (from `version.when`).
5. For each packet, read every accessible page body. Record unread, draft, whiteboard, title-only, and local-only items separately.
6. Pending supersession sweep (run in full-tree and freshness modes): for each `05`, `08`, `12`, and ADR page whose body contains a `## 대체 문서 링크` (supersedes) header, fetch the referenced old page and check whether the old page carries a `SUPERSEDED` banner / status. (`12. 운영 가이드` runbooks are living standards whose template carries `## 대체 문서 링크` / `## 변경 이력`, so a new runbook replacing an old one can leave the old one un-superseded.) If the old page has no SUPERSEDED marker, classify the old page as `Pending supersession` (`confidence = medium`) and list it under `## Pending supersession 후보` for manual completion by `colonova-engineering-docs-publish`. This enforces the current-vs-historical SSOT principle for half-completed supersession cycles. Apply the same check to a `02` Design Review whose body links a successor DR while the old DR status is not `Deprecated`.
6b. Discussion closure sweep (run in full-tree mode; symmetric to step 6): for each `04. 논의사항` page whose body links an `08. 결정사항` decision page (a Confluence URL in the `결정 필요 사항` field or in the body) but whose top of page has no `RESOLVED` status marker, classify it as `Discussion closure incomplete` (`confidence = medium`) and add it to `## Manual review 후보`. This is a half-finished discussion→decision closure: the decision page was created but the source discussion was never set to `RESOLVED` (SSOT principle #3, current vs. historical). Route it to `colonova-engineering-docs-publish` to finish the Discussion Closure Flow. Do not mark such a discussion page `Refresh required` or `Archive`.
7. Classify pages into Archive candidate, Archive hold, Archive excluded, optional placement review candidates, and `Refresh required` candidates. In freshness mode, compute `staleness_days` for `doc_role = living_standard` pages (`05`, `08`, `12`) and flag those past their threshold (see `references/confluence-tree-audit.md` Freshness Thresholds) as `Refresh required`, never Archive. Also compute `staleness_days` for `doc_role = design_standard` pages — `02. 시스템 디자인` Design Reviews whose `상태` is `Approved` — and flag those over 180 days as `Refresh required`. Treat Draft / Deprecated Design Reviews as `other` (exempt from freshness flags). Also compute `staleness_days` for `doc_role = monitoring_standard` pages — `07. 모니터링` pages whose body states SLI/SLO or alert thresholds — and flag those over 180 days as `Refresh required`; treat threshold-free dashboard/index pages as `other`. For a `01. 시스템 분석` page whose body carries a `## 변경 이력` table with 2+ rows (a living reference), flag it as `Manual review` when `staleness_days > 365` instead of leaving it freshness-blind. Apply the same 365-day `Manual review` rule to a `09. 스케쥴링` roadmap/milestone page whose body carries a `## 변경 이력` table with 2+ rows (a repeatedly-revised living roadmap), so a long-abandoned roadmap is not a freshness blind spot. For an `Under Review` Design Review with `staleness_days > 90`, this is a stale *workflow* (the review process itself stalled), not a stale document: classify it as `Manual review (workflow stale)`, not `Refresh required` — it needs the review restarted or a `Deprecated` transition, not a content refresh (see `references/confluence-tree-audit.md` Freshness Thresholds). Keep `Refresh required` queues limited to published pages; route any draft to Manual review instead.
8. Produce coverage per folder:

```text
대상 <n>개 / live body 확인 <n>개 / local 보강 <n>개 / 제한 읽기 <n>개 / 실패 <n>개
```

9. Output recommendations, not inventory. Do not list pages that fit their current folder except as coverage counts.

## Output

For broad audits, create a local Markdown report and return a short chat summary. For narrow audits, a concise chat table is enough.

Always include:

- 5-line conclusion, ending with a `다음 감사 권장: YYYY-MM-DD` line (sprint-close = today + 14 days; freshness-only = today + 30 days; single-folder = judgment)
- `## 감사 메타`: audit_date (today, ISO 8601), audit_mode, scope, next_recommended_run, and (when a prior report was found) an `오버듀` note if today is on or after the prior report's next_recommended_run
- Archive, mismatch, or refresh Top 5, depending on requested mode
- coverage summary
- tree gap (when an SSOT-defined folder is missing in live)
- `## 신규 Subfolder 탐지` when a live subfolder exists that is not on the known-subfolder list (step 3b)
- execution queues (including `최신화 후보` when stale living standards are found)
- `## Pending supersession 후보` whenever the sweep finds at least one half-completed supersession cycle
- `Discussion closure incomplete` items inside `## Manual review 후보` whenever the discussion closure sweep finds a `04` page that links a decision page but is not marked `RESOLVED`
- special and limited items
- link or path to the detailed report when one is created

In freshness mode, always emit the `## 최신화 후보` section. When zero candidates are found, do not omit it; output the all-clear line: `모든 living standard가 freshness 임계값 이내입니다 (감사 기준일: <today>). 다음 freshness 점검 권장일: <today+30d>.`

When a prior report path is provided or auto-selected (delta mode), include an optional `## 이전 감사 대비 변화` section in the local report: 신규 항목, 해소 항목, 재등장 항목, 악화 항목. Save the broad-audit local report as `colonova-audit-YYYY-MM-DD.md` (date = audit_date) so it doubles as the prior report for the next run and is auto-discoverable by the most-recent-file lookup.

Load `references/output-contract.md` before composing the final report.

## Decision Rules

Load only the reference needed for the current step:

- `references/confluence-tree-audit.md`: live/local source priority, fields, worker packet rules
- `references/action-taxonomy.md`: action definitions and confidence rules
- `references/output-contract.md`: report sections and final self-check

## Safety

- Keep the default read-only.
- Do not put `low` confidence items into immediate execution queues.
- Do not recommend Archive without a replacement document, current reference, or clear retirement evidence.
- Classify stale-but-current living standards as `Refresh required`, not Archive.
- If discussion, decision, design, and operating procedure are mixed, prefer Extract or Convert over moving the original page.
- Keep draft, whiteboard, unread, title-only, and local-only entries out of immediate execution candidates.
- Never put a draft page into the `최신화 후보` (Refresh required) queue; the publisher handoff hands a raw page ID and the receiver cannot tell it is a draft. Classify draft pages as `Manual review` only. The `최신화 후보` queue contains published pages only.
- Surface half-completed supersession cycles (across `05`, `08`, `12`, and ADR pages) as `Pending supersession` (medium confidence) for manual completion by the publisher; do not mark such old pages `Refresh required` or `Archive`.
- Surface half-completed discussion→decision closures (a `04` page that links a decision page but has no `RESOLVED` marker) as `Discussion closure incomplete` under `Manual review 후보`; do not mark them `Refresh required` or `Archive`.
- Surface `02` Design Reviews stuck in `Under Review` for too long as `Manual review (workflow stale)`, separate from `Refresh required` (these need review restart or Deprecated transition, not content refresh).
