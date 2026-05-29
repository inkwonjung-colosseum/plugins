# Action Taxonomy

## Actions

| Action | Use when |
| --- | --- |
| `Keep` | The page fits the current folder. Use only for internal classification, not final page listings. |
| `Keep as companion` | The page is valid as a supporting child of the current parent, but the relationship should be explicit. |
| `Move` | Most of the body belongs to another folder, parent context dependency is low, and owner/link review is still required before execution. |
| `Extract decision` | A discussion page contains a stable decision that should become a concise decision page. |
| `Extract design` | A mixed page contains reusable design content that should become or update a design page. |
| `Convert to technical reference` | A page should become a living implementation or interface reference. |
| `Convert to operating guide` | A page should become a repeatable runbook, SOP, onboarding guide, or checklist. |
| `Refresh required` | A living standard (`doc_role = living_standard`), an Approved Design Review (`design_standard`), or a `07` monitoring-standard page (`monitoring_standard`, body states SLI/SLO or alert thresholds) is past its freshness threshold and still referenced as current, with no retirement evidence. It must be updated, not archived. |
| `Pending supersession` | A supersession cycle was started (a newer page exists) but the old page's SUPERSEDED status update did not complete, so the old page is still active. Covers `05`, `08`, `12. 운영 가이드` (a new runbook replacing an old one), and ADR pages that carry a `## 대체 문서 링크` header. Surface for manual completion, not as `Refresh required` or `Archive`. |
| `Archive` | The page is replaced, obsolete, duplicated, a retired PoC, or no longer current, and evidence exists. |
| `Manual review` | Evidence is weak, ownership/link impact is high, or the item is draft, whiteboard, unread, title-only, or local-only. Sub-cases: `Discussion closure incomplete` (a `04` page links a decision page but the discussion was never set to `RESOLVED`); `Manual review (workflow stale)` (a `02` Design Review stuck in `Under Review` past 90 days — the review process stalled, so it needs a review restart or `Deprecated` transition, not a content refresh or archive). |

## Decision Order

1. If the page fits the folder, classify as `Keep`.
2. If it is a natural child or support document, classify as `Keep as companion`.
3. If several document natures are mixed, prefer `Extract` or `Convert` over moving the original.
4. Use `Move` only when the body clearly belongs elsewhere and context dependency is low.
5. If the page is a living standard past its freshness threshold with no retirement evidence, classify as `Refresh required`, never `Archive`.
6. Use `Archive` only with replacement, current reference, or retirement evidence.
7. Use `Manual review` when confidence or execution safety is insufficient.

`Refresh required` and `Archive` are mutually exclusive. A stale-but-still-current living standard is a refresh candidate; only retirement evidence moves it to `Archive`.

## Confidence

| Confidence | Criteria |
| --- | --- |
| `high` | Live body was read, two or more body/context evidence points exist, and the recommended target is clear. |
| `medium` | Body evidence exists, but the page has mixed nature or needs owner/replacement confirmation. |
| `low` | Classification depends on title/parent only, fetch failed, item is draft/whiteboard/local-only, or current status is unclear. |

## Execution Queues

| Queue | Criteria |
| --- | --- |
| `바로 실행 후보` | High-confidence, simple Move, Archive, or companion cleanup after execution confirmation. |
| `추출 먼저 후보` | Original should remain, but decision, design, technical reference, or operating guide should be extracted. |
| `최신화 후보` | Living standard (`05. 기술문서`, `08. 결정사항 / settled policy`, `12. 운영 가이드`), `design_standard` (Approved Design Reviews in `02. 시스템 디자인`), or `monitoring_standard` (`07. 모니터링` SLO/threshold pages) past its freshness threshold, still current, needs `Refresh required`. Published pages only — never include drafts. Route to `colonova-engineering-docs-publish` with the page ID for update. |
| `Pending supersession 후보` | Supersession cycle started but the old page's SUPERSEDED status update did not complete, leaving old and new pages both active (`05`, `08`, `12`, ADR). Route to `colonova-engineering-docs-publish` for manual completion. |
| `Archive 후보` | Replacement/current reference/retirement evidence exists. |
| `Manual review 후보` | Draft, whiteboard, body read failure, strong mixed nature, owner check, or link impact. Includes `Discussion closure incomplete`: a decision page was created but the source discussion page was never set to RESOLVED (route to `colonova-engineering-docs-publish` to finish the closure). Includes `Manual review (workflow stale)`: a `02` Design Review stuck in `Under Review` past 90 days, needing review restart or `Deprecated` transition, not a content refresh. |
| `건드리면 위험한 항목` | Meeting companions, historical decision evidence, currentness unclear, or high owner/link impact. |
