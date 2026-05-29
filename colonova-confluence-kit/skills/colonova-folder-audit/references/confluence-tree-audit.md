# Confluence Tree Audit

## Source Priority

1. Use live Confluence for current tree structure, parent, status, and page existence.
2. Use live body for current content.
3. Use local export only when live body fetch fails and the export is explicitly provided or clear from context.
4. If live and local body conflict, prefer live and mark local as an older snapshot.
5. If a page exists only in local export, classify as `Manual review`.
6. If a page exists only in live descendants, include it with no local evidence.

## Pagination

`getConfluencePageDescendants` returns a cursor when a parent has more than ~100 descendants. The live `8.8 ColoNova` tree exceeds this.

1. If the response includes a `cursor` (or `_links.next`) field, call again with that cursor and accumulate results until no cursor remains.
2. Never treat a single truncated page of descendants as the complete tree.
3. If pagination fails partway, split handling by status code:
   - HTTP 429 (rate limit) is transient and safe to retry: pause briefly and retry the same cursor position up to two times before giving up. A large, actively growing tree like `8.8 ColoNova` can throttle mid-audit; a brief pause usually recovers full coverage, so do not downgrade confidence on a recoverable 429.
   - If the error is 4xx other than 429 (for example 403 permission, 404 not found), or 5xx/timeout that persists after retries, mark that folder `partial-fetch`, record the HTTP status and the cursor range collected, and flag the affected coverage counts with `partial-fetch`.
4. Apply the same cursor loop to any per-folder descendants fetch, not only the root. The same cursor-exhaustion loop also applies to any `getConfluencePageDescendants` call in the `colonova-doc-router-publisher` skill (notably ADR-NNN numbering and root-level folder-ID resolution), not only audit root fetches. Note that ADR subfolder enumeration cannot call `getConfluencePageDescendants` directly on the ADR subfolder ID (a `type: "folder"` entity returns 404 — see `folder-id-map.md` API note); it enumerates via a root-depth fetch (`getConfluencePageDescendants(933068815, depth=3)`) filtered by `parentId`, and a truncated root fetch there would miscompute `max(N)` and risk a duplicate ADR number — hence the cursor loop.
5. A `partial-fetch` folder must not contribute to Archive 후보 or `Refresh required` queues — its evidence is incomplete. List it only under `## 특수 항목과 제한 사항`.
6. Confidence downgrade: if 30% or more of the folders are `partial-fetch`, state audit confidence as `저 (partial coverage)` in `## 결론` and recommend re-running the audit. Do not present a partial tree as a complete audit.

## Standard Fields

Record these fields for every candidate:

| Field | Values |
| --- | --- |
| `source` | `live`, `local export`, `both` |
| `body_status` | `read`, `unread`, `limited`, `local-fallback`, `title-only` |
| `failure_reason` | `folder-404`, `page-404`, `permission`, `draft`, `unsupported-type`, `unknown` |
| `classification_basis` | `body`, `title+parent`, `local body`, `linked context` |
| `last_modified` | ISO 8601 date string, taken from Confluence `version.when` |
| `staleness_days` | integer, `today - last_modified` in days |
| `doc_role` | `living_standard`, `design_standard`, `meeting_record`, `incident`, `archive_candidate`, `other` |
| `confidence` | `high`, `medium`, `low` |

`last_modified` comes from `version.when` on the page returned by `getConfluencePage` or in descendant metadata. `today` is the run date. Set `doc_role` from the folder and body:

- `living_standard` for `05. 기술문서`, `08. 결정사항 (settled policy / 결정사항)`, `12. 운영 가이드` (current reference docs).
- `design_standard` for pages in `02. 시스템 디자인` whose body contains the Design Review `## 디자인 리뷰 정보` table with `상태 = Approved`. Draft / Under Review / Deprecated Design Reviews are `other` (freshness-exempt).
- `monitoring_standard` for `07. 모니터링` pages whose body actually states SLI/SLO targets, alert thresholds, or normal/abnormal criteria (the operational baseline). Plain dashboard-link or index pages with no thresholds in the body are `other` (freshness-exempt) — judge by body, not folder alone.
- `meeting_record` for `03. 회의록` and other dated point-in-time records.
- `incident` for `06. 장애 / Incident`.
- `archive_candidate` when retirement evidence already exists.
- `other` for everything else, including `01. 시스템 분석` (point-in-time AS-IS snapshot) and `09. 스케쥴링` (roadmap/milestone). Exception: if a `01` or `09` page's body carries a `## 변경 이력` table with two or more rows, it is being used as a repeatedly-updated living reference (a living roadmap for `09`) — flag it as a `Manual review` freshness candidate (see Freshness Thresholds) rather than leaving it a freshness blind spot.

## Freshness Thresholds

Use these default staleness thresholds when surfacing refresh candidates. They are guidance, not hard rules; confirm with the owner before acting.

| doc_role / folder | Expected refresh window | Stale when staleness_days > |
| --- | --- | --- |
| `05. 기술문서` (living standard) | quarterly | 90 |
| `12. 운영 가이드` (runbook/SOP) | half-yearly | 180 |
| `02. 시스템 디자인` (design_standard — Approved Design Review only) | half-yearly | 180 |
| `07. 모니터링` (`monitoring_standard` — body states SLI/SLO or alert thresholds) | half-yearly | 180 → `Refresh required` |
| `08. 결정사항 / settled policy` (living standard) | yearly | 365 |
| `02. 시스템 디자인` Under Review DR (stale workflow) | review should resolve within ~90 days | 90 → `Manual review (workflow stale)`, not `Refresh required` |
| `01. 시스템 분석` with 2+ `변경 이력` rows (used as living reference) | judgment | 365 → `Manual review` |
| `09. 스케쥴링` with 2+ `변경 이력` rows (living roadmap/milestone) | judgment | 365 → `Manual review` |
| other living references | judgment call | flag for `Manual review` |

`02. 시스템 디자인` content freshness (`Refresh required`) applies only to pages with `상태 = Approved` in the `## 디자인 리뷰 정보` table. Draft and Deprecated Design Reviews are exempt (`doc_role = other`). An `Under Review` Design Review past 90 days is a stalled review *workflow*, not a stale document: surface it as `Manual review (workflow stale)` so the owner restarts the review or transitions it to `Deprecated`. Do not classify it as `Refresh required` (no content edit is the fix) or `Archive`.

`07. 모니터링` freshness (`Refresh required`, 180-day window) applies only to `monitoring_standard` pages — pages whose body states SLI/SLO targets, alert thresholds, or normal/abnormal criteria that operators rely on. A stale monitoring baseline can drive wrong operational judgments, so it is freshness-tracked like a living standard. Dashboard-link, index, or pointer pages with no thresholds in the body are `other` and exempt; judge by body content, not by the folder alone.

`01. 시스템 분석` is normally a point-in-time AS-IS snapshot (`other`, no freshness flag). The exception: a `01` page whose body has accumulated a `## 변경 이력` table with two or more rows is being maintained as a living reference (the publisher appends a 변경 이력 row on every `01` update). Flag such a page as a `Manual review` freshness candidate when `staleness_days > 365`, so the publisher's update path and the audit's freshness path agree on which `01` pages are repeatedly revised.

`09. 스케쥴링` follows the same pattern. A one-off schedule note is `other` (no freshness flag), but a roadmap / milestone / release-order page whose body carries a `## 변경 이력` table with two or more rows is a repeatedly-revised living roadmap. Flag it as a `Manual review` freshness candidate when `staleness_days > 365` (the yearly window matches `08`), so a long-abandoned roadmap surfaces for owner review rather than staying a blind spot. The publisher's `templates/scheduling.md` carries a `## 변경 이력` table, so this keeps the publisher update path and audit freshness path aligned for `09`.

A page over threshold with no retirement evidence is a `Refresh required` candidate, not an `Archive` candidate. Meeting records, incidents, and historical pages are exempt from freshness flags; old age is expected for them.

## Folder Packet

Each top-level folder packet should include:

- folder title and ID
- live criteria for the folder
- all descendant page IDs under that folder
- nested folder boundaries
- draft, whiteboard, and unsupported items
- oldest and newest page `last_modified` in the folder, as packet metadata

Do not send the entire tree to every worker. Give each worker only its packet plus shared classification rules.

## Tree Gap Detection

The root SSOT classification table defines 13 folders. Compare it against the live top-level folders and report any defined folder that is missing in the live tree as a `정의됨-미생성` (defined, not yet created) gap.

Current known gap: `06. 장애 / Incident` is defined in the SSOT table but has no live folder yet.

Live folder titles carry a ` - ColoNova` suffix (for example `01. 시스템 분석 - ColoNova`). Match folders by normalized prefix (`NN.` number plus role name), not by exact string, so the suffix does not cause false gaps.

## Worker Requirements

Each folder worker must:

1. Read all accessible page bodies in the packet.
2. Record unread pages with failure reason.
3. Separate Archive candidate, Archive hold, and Archive excluded.
4. List fitting pages only as coverage counts or exclusion aggregates.
5. For each candidate, include page ID, evidence, confidence, and recommended action.
6. Include placement review only when requested.

If parallel workers are unavailable, process the same packets sequentially and note the fallback briefly.
