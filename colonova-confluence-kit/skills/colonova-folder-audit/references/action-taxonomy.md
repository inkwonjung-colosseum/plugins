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
| `Archive` | The page is replaced, obsolete, duplicated, a retired PoC, or no longer current, and evidence exists. |
| `Manual review` | Evidence is weak, ownership/link impact is high, or the item is draft, whiteboard, unread, title-only, or local-only. |

## Decision Order

1. If the page fits the folder, classify as `Keep`.
2. If it is a natural child or support document, classify as `Keep as companion`.
3. If several document natures are mixed, prefer `Extract` or `Convert` over moving the original.
4. Use `Move` only when the body clearly belongs elsewhere and context dependency is low.
5. Use `Archive` only with replacement, current reference, or retirement evidence.
6. Use `Manual review` when confidence or execution safety is insufficient.

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
| `Archive 후보` | Replacement/current reference/retirement evidence exists. |
| `Manual review 후보` | Draft, whiteboard, body read failure, strong mixed nature, owner check, or link impact. |
| `건드리면 위험한 항목` | Meeting companions, historical decision evidence, currentness unclear, or high owner/link impact. |
