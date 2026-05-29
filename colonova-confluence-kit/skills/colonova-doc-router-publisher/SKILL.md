---
name: colonova-doc-router-publisher
description: Use when ColoNova 8.8 문서를 Confluence 트리에 게시·관리할 때 — 새 초안의 위치 추천·유형별 템플릿 변환·문서 분리·생성/업데이트·readback 검증. 기존 기준 문서(living standards) 최신화·갱신(변경 이력 기록), 최신화 후보 큐 일괄 갱신(batch refresh), discussion→decision 종결(논의사항 RESOLVED 처리), supersession(구 페이지 SUPERSEDED 처리)에도 발동. colonova-folder-audit이 최신화 후보로 식별한 page ID를 받아 실제 갱신을 수행하는 진입점(예: "감사 결과 page ID 12345 갱신해줘"). broad cleanup·트리 전체 감사는 colonova-folder-audit을 먼저 사용.
---

# ColoNova Doc Router Publisher

Use this skill for a single draft or a small package of related documents that should be routed into the ColoNova Engineering Confluence tree, or to refresh/update an existing standard. If the user already provides a specific page ID (or URL) with a clear update intent, enter the update path directly — no prior audit is needed. When no page ID is given and the request is a broad cleanup, defer to `colonova-folder-audit` first.

Fixed target:

- URL: `https://colosseum.atlassian.net/wiki/spaces/COLO/pages/933068815/8.8+ColoNova`
- root page ID: `933068815`
- space key: `COLO`
- space name: `[팀]Engineering`

For broad tree audits, bulk movement, archive recommendation, or folder-wide mismatch reports, stop and use `colonova-folder-audit`.

## Scope

This skill can recommend location, rewrite a draft with the right template, split mixed documents into a small package, and publish only after explicit user approval. Every create or update must be followed by readback verification.

### Refresh use case

This skill is also the refresh/update path for keeping living standards (`05. 기술문서`, `08. 결정사항`, `12. 운영 가이드`) current. When the user says a standard is stale or needs 최신화/갱신 and provides an existing page ID or URL, enter the update path: read the current page, apply the new content, and run the supersession check before finishing. `colonova-folder-audit` surfaces which pages are stale; this skill performs the actual refresh.

When the user hands more than one page ID at once — for example the whole `## 최신화 후보` queue from an audit report, or a pasted list/table of page IDs — run the Batch Refresh Flow below instead of forcing one single-page call per ID.

## Inputs

Use what the user provides:

- source draft, URL, file, or pasted text
- desired title
- purpose or audience
- draft-only, publish, or update intent
- known parent folder or candidate folder
- existing page ID or URL for updates (a single ID, or a list/queue/audit-report path of IDs for the Batch Refresh Flow)
- related pages or titles that may cause duplicates

Ask only when a missing value blocks safe routing or publishing.

## Workflow

1. Identify document purpose, audience, state, decisions, open issues, action items, repeatable procedures, solution/vendor content, incident content, and monitoring content.
2. Decide whether the source is a single-role document or a mixed document.
3. Read live root `933068815` and any linked classification guide. If unavailable, do not publish; create a draft-only result or mark location as `확인 필요`. Note live folder titles carry a ` - ColoNova` suffix.
4. Recommend one parent folder, or compare two to three candidates when ambiguous. Resolve the parent to a live page ID via `getConfluencePageDescendants(933068815)` (match on the `NN.` prefix, not exact title; `folder-id-map.md` lists folder titles, the top-level folder pageIds resolved live on 2026-05-29 as a speed cache, and known subfolders — always trust live if the cached ID no longer resolves to the expected folder). If the recommended folder does not exist in live (notably `06. 장애 / Incident`), follow Missing Folder Handling in `publish-safety.md`: tell the user and get approval to create the folder first or publish under root. The 13 top-level folders and 5 known subfolders already carry confirmed numeric pageIds in `references/folder-id-map.md` (resolved live 2026-05-29). If you ever resolve a folder/subfolder whose cached ID no longer matches live (the tree is actively maintained), you may optionally overwrite that row with the corrected numeric ID so later runs skip the lookup. This write-back is optional and best-effort: only do it when the runtime supports persistent local file writes and the file survives between sessions; if a write is unsupported or fails, skip it silently and continue (never error out).
5. Check the recommended parent's immediate children (including subfolders) for title patterns before proposing a final title, and route into a subfolder when it matches (`references/routing-rules.md` → Subfolder Routing). Note `getConfluencePageDescendants` returns 404 when called directly on a `type: "folder"` entity ID; enumerate folder/subfolder children by calling it on the root `933068815` with sufficient `depth` and reading the `parentId`/`type` fields, not by calling it on the folder ID. The five known subfolder pageIds are already in `references/folder-id-map.md` → Known Subfolders (resolved live 2026-05-29).
6. Select a local template from `templates/` first. The canonical doc-type → template list is the `Local template` column of `references/routing-rules.md` → Fallback Templates (single source of truth). For types still marked `(fallback only)` there (장애/Incident, 모니터링, 회고), use that table's fallback section map and tell the user a fallback section map is being used. Examples of local templates (the full canonical list is in routing-rules.md): ADR uses `templates/adr.md`; a `02` Design Review uses `templates/design-review.md`; 논의사항 uses `templates/discussion.md`; 결정사항 uses `templates/decision.md`; 솔루션 uses `templates/solution.md`; 스케쥴링 uses `templates/scheduling.md`.
7. Rewrite without inventing facts. Use `미정` or `확인 필요` for missing owners, dates, numbers, or decisions.
8. Show publish confirmation before writing to Confluence.
9. When updating any page whose template carries a `## 변경 이력` table — living standards (`doc_role = living_standard`: `05`, `08`, `12`), an ADR, a `02. 시스템 디자인` non-Design-Review page (`system-design.md`), or a `01. 시스템 분석` page (`system-analysis.md`) — append a 변경 이력 row (날짜 = today, 변경 내용 = brief summary, 작성자 = 미정 if unknown) before sending the body for approval, so the audit trail keeps current vs. historical separated (SSOT #3). For a Design Review page, follow the Design Review Update Rule (개정 이력) instead.
10. After user approval, create or update the page. For an update, first fetch the live `version.number` via `getConfluencePage(pageId)` and include the next version number in the update call (see `publish-safety.md` → Update Rules; an omitted/guessed version triggers a 409 conflict). Then read it back and verify title, parent, main sections, and non-empty body.
11. Post-update supersession check: if this update/new page supersedes a prior standard or ADR, run the Supersession Flow below and the Supersession Rules in `publish-safety.md` before finishing. If a discussion is being closed into a decision, run the Discussion Closure Flow.

## Supersession Flow

Trigger when a new document replaces an existing page, or an update fully replaces a standard/ADR.

1. Confirm and read back the old page ID.
2. Add a `## 대체 문서 링크` (`supersedes: <old URL>`) section to the new page draft; link, do not copy.
3. After approval, create/update the new page.
4. Update the old page status to `SUPERSEDED BY <new page link>` and add a top banner; keep it in place unless the user approves moving it to `99. Archive`.
5. For ADRs and `08. 결정사항` non-ADR decision pages (`templates/decision.md`), set the `## 상태` table status cell to `SUPERSEDED`, populate the `대체 문서` column with the new page URL, then append a `변경 이력` row. For ADRs, additionally confirm via CQL that the prior version exists. This keeps the structured `## 상태` field consistent with the SUPERSEDED banner (SSOT principles #1 and #3); do not leave the status table on `ACTIVE` after superseding. For a `12. 운영 가이드` runbook (`templates/operating-guide.md`, no status table) being replaced by a new runbook, keep the top SUPERSEDED banner from step 4 and append a `변경 이력` row recording the supersession — so the old runbook stays a current-vs-historical separated record (this is the state `colonova-folder-audit` step 6 detects as `Pending supersession` if left incomplete).
6. Read back both pages; report the backlink/reference count to the old page in the readback. If the count is greater than 0, list up to 5 inbound page titles/IDs and ask the user whether to update those cross-references to point to the new page, or leave them with the SUPERSEDED banner as sufficient. Do not edit inbound pages without approval.

## Discussion Closure Flow

Trigger when a `04. 논의사항` discussion reaches a settled conclusion and should become a decision (`08. 결정사항`). This keeps current vs. historical separated (SSOT principle #3) and uses links, not copies (principle #2).

1. Confirm the discussion page ID and read it back.
2. Create the decision page in `08` with `templates/decision.md`, linking back to the discussion page under `## 관련 문서`. Do not copy the discussion body.
3. After approval and readback of the decision page, update the discussion page: add a top-line status `RESOLVED — 결정: <new decision page link>` and set `결정 필요 사항` to the decision page URL.
4. Read back both pages and report each verification separately.

## Batch Refresh Flow

Trigger when the user hands several page IDs to refresh in one request — typically the `## 최신화 후보` queue from a `colonova-folder-audit` report, an audit report path, or a pasted list/table of page IDs. This is the most common continuous-maintenance operation (a sprint-close audit usually yields 5–10 refresh candidates), so process the queue as one tracked batch rather than repeated single calls.

1. Input: accept a page ID list, an audit report path (parse the `## 최신화 후보` table for page IDs), or a pasted table. Normalize to an ordered list of page IDs. Confirm the count back to the user.
2. For each page ID in order: fetch the live page (`getConfluencePage`, capturing the current body for the diff; record the `version.number` only for the diff display, not as the value to write), classify its doc type, and prepare the proposed change — including a `변경 이력` row (or `개정 이력` for a Design Review) per step 9. Do not write yet.
3. Present one batched approval gate, not N separate ones: show a per-page summary table (page ID, 제목, 폴더/유형, 제안 변경 요약, 추가될 변경 이력 row). State: "아래 N개 페이지를 순서대로 갱신합니다. 각 페이지 본문을 확인 후 전체 승인하거나 개별 건너뛸 수 있습니다." Let the user approve all, approve a subset, or skip specific IDs.
4. Apply approved updates in order. For each page, immediately before calling `updateConfluencePage`, re-fetch `version.number` via `getConfluencePage(pageId)` — do not reuse the `version.number` captured in step 2. The batched approval review of 5–10 pages can take minutes; if another user edited a page during the approval window, the step-2 version is stale and the write would 409-conflict. Reuse the pre-approved body diff, but always write with a fresh version number. If the fresh re-fetch shows the body changed since step 2 (someone else edited it during the approval window), surface that page's new diff to the user and get a per-page re-confirmation before writing it; do not silently overwrite the other edit. Then `updateConfluencePage`, then readback. Accumulate the readback result per page. On a per-page failure, record it and continue to the next page (a batch refresh is independent pages, unlike a split package which stops on first failure — see `publish-safety.md` → Batch Refresh Failure Handling). On HTTP 429, apply the 429 retry sub-clause before recording a failure.
5. After the batch, report a summary: `N개 갱신 완료, M개 실패 (page ID + 사유), K개 건너뜀`, with each page's Confluence link and readback result. List failures separately for manual follow-up.
6. Offer to re-run `colonova-folder-audit` (freshness mode) to confirm the refreshed pages cleared the `## 최신화 후보` queue and to pick up the next cadence date.

If any page in the batch needs supersession (it replaces another standard) or is actually a draft, pull it out of the batch and handle it individually via the Supersession Flow or Draft Page Handling — do not silently fold a supersession or draft transition into the batch approval.

## ADR Number and Status Transition Rule

When creating a new ADR, determine the number, do not guess. The ADR subfolder is a `type: "folder"` entity, so a direct `getConfluencePageDescendants(<ADR-subfolder-id>)` returns 404 (see step 5 and `folder-id-map.md` API note); enumerate the ADR subfolder children via the same root-depth pattern instead: call `getConfluencePageDescendants(933068815, depth=3)` and filter the results to `parentId = 1778810882` (the ADR subfolder, `05. 기술문서 / ADR`). Exhaust all cursor pages (same cursor-exhaustion loop as `colonova-folder-audit` in `references/confluence-tree-audit.md` → Pagination) before computing `max(N)` — the root tree exceeds ~100 descendants, so a single truncated response would miss higher-numbered ADRs and risk proposing a duplicate. Extract the `ADR-NNN` pattern from the filtered ADR titles, find the max N, and propose `ADR-(N+1)`. If the fully-paginated result has no ADR pages under that parent, start at `ADR-001`. If pagination fails partway (a cursor page errors out), do not propose a number; report the partial fetch and ask the user to confirm the ADR number manually. Include the proposed (or user-confirmed) number in the pre-approval diff so the user confirms it.

If the root-depth fetch fails (permission error, persistent 5xx/timeout, or the ADR subfolder ID `1778810882` no longer resolves to the ADR subfolder in live), do not propose a number and do not default to `ADR-001` — higher-numbered ADRs may exist but be unreachable, and guessing risks a duplicate number. Report the fetch failure and ask the user to confirm the ADR number manually before continuing. Include the user-supplied number in the pre-approval diff. (This mirrors the confidence-low / Manual review safety pattern used elsewhere.)

ADR status transitions:

- `PROPOSED → ACCEPTED` (the most common transition): update the 상태 table row and append a 변경 이력 row noting the transition. If a related `04. 논의사항` discussion exists, ask whether to apply the Discussion Closure Flow to it. Show the status change explicitly in the pre-approval diff.
- `ACCEPTED → DEPRECATED / SUPERSEDED`: route through the Supersession Flow (set the 상태 table to `SUPERSEDED` with the 대체 문서 link, add a 변경 이력 row, complete the two-page cycle).

## Design Review Update Rule

When updating a `02. 시스템 디자인` Design Review page, always increment the `## 개정 이력` table: add a new row with 버전 (prior max +0.1), 날짜 (today), 변경 내용 (brief), 작성자 (미정 if unknown). Show this row in the pre-approval diff. Run the Duplicate Check before creating any new Design Review page (see Update vs New Page).

### Design Review Deprecated 전환 규칙

When a new Design Review supersedes an existing one, complete the same two-page atomic cycle as Supersession Flow, reflecting Design Review's status field (`상태` row, not a status table):

1. Add a `## 대체 문서 링크` section to the new DR draft linking the old DR URL (link, do not copy).
2. After approval and readback of the new DR, set the old DR's `상태` to `Deprecated` and add a top banner `DEPRECATED — 대체 문서: <new DR link>`.
3. Append a `## 개정 이력` row to the old DR (버전 +0.1, 날짜 today, 변경 내용 = deprecated/superseded note).
4. Read back both pages and report each verification separately.
5. Report the inbound backlink/reference count to the old DR; if greater than 0, list up to 5 inbound titles/IDs and ask whether to repoint them. Do not edit inbound pages without approval.

If the old DR status update fails after the new DR is created, follow Partial Supersession Recovery in `publish-safety.md` (the old DR is `Pending supersession` until completed).

## Update vs New Page

Before creating a new page for a topic that may already exist, decide:

- If a page on the same design/standard topic already exists, default to updating it (SSOT principle #1, one source). For Design Review and living standards this is the norm.
- Create a new page only when the scope is fundamentally different from the existing one.
- Always run the Duplicate Check in `publish-safety.md` before creating a new Design Review page or living standard (`05`, `08`, `12`), even when the proposed title looks novel.
- For other types, run the Duplicate Check when unsure and ask the user.

## Mixed Documents

If one source mixes analysis, design, decision, technical reference, or operating procedure, do not force it into one folder without warning.

Use these split actions:

- `Extract decision`
- `Extract design`
- `Convert to technical reference`
- `Convert to operating guide`

Before publishing a mixed source, present:

1. single compressed page
2. split document package

Do not create or update pages until the user chooses and approves.

## Output

Before publishing:

1. recommended folder and reason
2. alternative folders when relevant
3. selected template
4. transformed document
5. publish approval request

After publishing:

1. Confluence link
2. saved location
3. template used
4. readback verification result
5. remaining checks
6. for split packages, list successes and failures separately; on partial failure, show created page IDs, failed documents, and the keep/delete decision pending from the user
7. for supersession, the old page's new status and the backlink/reference count to the new page
8. for a Batch Refresh Flow, the `N개 갱신 완료, M개 실패, K개 건너뜀` summary with per-page links/readback, failures listed separately, and an offer to re-run `colonova-folder-audit` freshness mode

## References

Load only what the current step needs:

- `references/routing-rules.md`: folder routing, subfolder routing, and fallback templates
- `references/folder-id-map.md`: top-level folder titles + pageIds and the five known-subfolder pageIds, all resolved live on 2026-05-29 (speed cache; live is SSOT — re-resolve if a cached ID no longer matches). Also documents the inconsistent subfolder suffix and the `getConfluencePageDescendants` 404-on-folder-ID constraint
- `references/split-document-rules.md`: mixed document and ADR split rules
- `references/publish-safety.md`: approval, create/update (incl. version pre-fetch and 429 retry), duplicate, missing folder, supersession (incl. inbound-link limit cap), split-package partial failure, batch-refresh failure, draft, and readback rules

## Safety

- Never publish before explicit approval.
- Never overwrite an existing page unless the user explicitly requested update and provided page ID or URL.
- Do not route to Archive for a new document unless the user clearly wants historical preservation.
- Resolve the parent to a live page ID; if the recommended folder is missing (for example `06`), do not auto-create — get approval first.
- For secrets, tokens, passwords, or credentials: mask matching lines and re-confirm before publishing the raw value, not just warn. This applies to both create and update paths — scan the newly supplied draft on updates too (see `publish-safety.md` → Sensitive Content).
- When updating a draft page, tell the user it stays a draft after the update. A draft → published transition changes visibility; re-show the Required Confirmation checklist and get separate approval (see `publish-safety.md` → Draft Page Handling).
- If a whiteboard URL/ID is given as the source, do not try to read or publish it directly; follow Whiteboard Source Handling in `publish-safety.md`.
- When superseding an existing standard or ADR, update the old page's status and link, and keep current vs. historical separated.
- Do not add arbitrary dates to meeting, incident, or retrospective titles.
- If live criteria cannot be verified, do not publish.
