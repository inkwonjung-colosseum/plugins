# Publish Safety

## Required Confirmation

Before any Confluence write, show:

- recommended folder
- recommended parent page ID
- title
- document type
- template
- create or update intent
- current page status (draft / published) and the expected status after this action
- transformed document body

Proceed only after explicit approval.

## Create Rules

- Use the selected parent ID.
- Prefer Markdown content when the tool supports it.
- Record created page ID and URL.
- If the title may duplicate an existing page, run the Duplicate Check below before creating.
- If `createConfluencePage` returns HTTP 429 (rate limit), pause briefly and retry the same call up to twice before treating it as a failure; a transient 429 must not trigger the uncertain-create CQL path or Partial Failure Handling until two retries have failed (see the 429 sub-clause in Update Rules, which applies equally to create and update).

### Duplicate Check

A title "may duplicate" when an existing page shares the same or a near-identical title or topic. Check explicitly, do not guess:

1. Run `searchConfluenceUsingCql` scoped under the recommended parent (title match, ancestor filter) for the proposed title.
2. If a same-title page exists under that parent, present the existing page ID and URL and stop the create. Offer update instead.
3. If a same-title page exists elsewhere in the space but not under the recommended parent: for living standards (`05`, `08`, `12`), warn that a duplicate elsewhere likely violates SSOT principle #1 (one source) and propose reviewing the update path first; for other types, tell the user and ask whether to proceed.

For Design Review and living standards (`05`, `08`, `12`), always run this check before creating a new page, regardless of title similarity — do not skip even when the proposed title appears novel.

### Missing Folder Handling

If the recommended parent folder does not exist in the live tree (notably `06. 장애 / Incident`, which is defined in the SSOT table but not yet created):

1. Tell the user the folder is missing; do not auto-create it.
2. Offer two options: (a) create the folder first under root `933068815` using the SSOT standard title (for example `06. 장애 / Incident - ColoNova`), then publish the document under it; or (b) publish directly under root `933068815`.
3. On approval of option (a), create the folder page first, read it back, then create the document under the new folder and read that back too.
4. Never publish under a guessed or nonexistent parent ID.

Folder-page readback criteria (the general Readback Verification "main sections exist / body not empty" checks do not apply to a structural folder page, which intentionally has no body sections). Readback for a folder verifies: (1) the title exactly matches the SSOT standard title including the ` - ColoNova` suffix (for example `06. 장애 / Incident - ColoNova`); (2) the parent is root `933068815`; (3) a page ID is returned. A naive empty-body check is not sufficient — a folder created with a missing suffix or wrong parent would otherwise pass.

### Partial Failure Handling

For a split package where some pages create successfully and a later one fails:

1. List the successfully created page IDs/URLs and the failed documents separately.
2. Stop further creation; do not continue the remaining package.
3. Ask the user whether to keep or delete the already-created pages, and wait for the decision before any more writes.

(A split package is one logical document; its pages cross-reference each other, so a mid-package failure stops the batch. A batch refresh is the opposite — independent pages — and uses the separate rule below.)

### Batch Refresh Failure Handling

For a Batch Refresh Flow (independent pages, see SKILL.md → Batch Refresh Flow), the pages are unrelated, so a single page's failure must not abort the rest:

1. On a per-page update failure (after the 429 retry sub-clause is exhausted, or a 5xx/timeout/permission error), record the page ID and cause and continue to the next page in the queue. Do not stop the batch.
2. For a 5xx/timeout where the write outcome is unknown, follow the Uncertain update rule in Readback Failure Action for that page only (version re-check, then decide), then continue.
3. At the end, report `N개 갱신 완료, M개 실패 (page ID + 사유), K개 건너뜀`. Keep successes and failures in separate lists so the user can manually follow up only on the failures.
4. Do not roll back already-refreshed pages — each refreshed page (with its appended 변경 이력 row) is a valid current state on its own.

## Update Rules

- Update only when the user explicitly asked to update an existing page.
- Require page ID or URL.
- Do not silently overwrite pages found by title search.
- Preserve the existing page relationship unless the user approved a move or new parent.
- Pre-fetch the version number (normal path, not just recovery): before calling `updateConfluencePage`, call `getConfluencePage(pageId)` and record the live `version.number`. Pass it in the update body as `version: { number: <fetched_number + 1> }` (Confluence optimistic locking expects the next version number). Never call `updateConfluencePage` with a guessed or omitted version — a stale or missing version produces a 409 conflict on every non-zero-version page. This live fetch also gives you the current body for the diff and supersession checks.
- If `createConfluencePage` or `updateConfluencePage` returns HTTP 429 (rate limit), pause briefly and retry the same call up to twice before treating it as a failure. A 429 is transient: it does not trigger the uncertain-create / uncertain-update CQL or version-re-check paths (those apply only to 5xx/timeout where the write outcome is unknown), and a mid-package 429 must not trigger Partial Failure Handling until two retries have failed. If the 429 persists after two retries, treat it as a failure and apply the relevant partial-failure handling. (Mirrors `confluence-tree-audit.md` → Pagination.)
- When updating any page whose template carries a `## 변경 이력` table — a living standard (`05`, `08`, `12`), an ADR, a `02. 시스템 디자인` non-Design-Review page (`system-design.md`), or a `01. 시스템 분석` page (`system-analysis.md`) — append a 변경 이력 row (날짜 = today, 변경 내용, 작성자 = 미정 if unknown) before approval. For a Design Review page, increment the 개정 이력 table instead (see SKILL.md → Design Review Update Rule).
- Closing a discussion into a decision is a two-page obligation: create the decision page in `08` and update the source discussion page to `RESOLVED` with the decision link. Do not create the decision page and leave the discussion unchanged (see SKILL.md → Discussion Closure Flow).

#### Discussion Closure 부분 실패 처리

If the decision page is created successfully but the discussion page `RESOLVED` update then fails (permission, draft, or API error):

1. Immediately report the decision page ID + URL and the discussion page ID that was not updated.
2. Provide the exact text the user must add to the discussion page by hand: the top-line status `RESOLVED — 결정: <decision page URL>` and the `결정 필요 사항 = <decision page URL>` value.
3. State the closure as `Discussion closure incomplete` and do not report it as completed.
4. This state is detectable by `colonova-folder-audit` as a `Discussion closure incomplete` Manual review sub-case (see action-taxonomy.md), so the next audit cycle can surface it.

### Draft Page Handling

If the target page is in draft state:

1. Tell the user the page is a draft before updating.
2. Note that after the update it remains a draft and is not published/visible.
3. If the user wants to publish (draft → published): this is a visibility-changing write. Re-show the Required Confirmation checklist (including current status `draft`, expected status `published`, and the resulting visible audience) and get a separate, explicit approval before the transition. Do not bundle it into an ordinary update approval.

### Supersession Rules

When an update or a new page supersedes an existing standard or ADR, complete the cycle as a two-page atomic action:

1. Confirm the old page ID and read it back.
2. In the new page draft, add a `## 대체 문서 링크` section linking the old page Confluence URL (`supersedes: <old URL>`). Do not copy the old body; link it (SSOT principle #2).
3. After approval, create/update the new page.
4. Update the old page: set its status to `SUPERSEDED BY <new page link>` and add a banner at the top of its body pointing to the new page. Keep the old page in place (principle #3, current vs. historical separation); if the user wants it retired, move to `99. Archive` only on explicit approval.
5. Read back both pages and report each verification separately. Report the inbound backlink/reference count to the old page (see Inbound Link Check below); if greater than 0, list up to 5 inbound page titles/IDs and ask whether to repoint them to the new page or leave them with the SUPERSEDED banner. Do not edit inbound pages without approval.

For ADRs and `08. 결정사항` non-ADR decision pages (`templates/decision.md`), set the `## 상태` table's status cell to `SUPERSEDED`, fill the `대체 문서` column with the new page URL, and add a 변경 이력 row. Do not leave the structured `## 상태` field on `ACTIVE` after applying the SUPERSEDED banner — the banner and the status table must agree (SSOT #1/#3). For ADRs, additionally confirm the prior version via CQL. For a `12. 운영 가이드` runbook (`templates/operating-guide.md`, which has no status table) replaced by a new runbook, keep the step-4 SUPERSEDED banner and append a 변경 이력 row recording the supersession. `colonova-folder-audit` sweeps `05`, `08`, `12`, and ADR pages for half-completed supersession, so leaving a `12` old runbook without the banner surfaces it as `Pending supersession`.

#### Inbound Link Check

`getConfluencePage` does not return inbound links, so find them with CQL:

1. Run `searchConfluenceUsingCql(query: 'space = "COLO" AND text ~ "<old-page-url>" AND ancestor = 933068815', limit: 50)`.
2. If that returns nothing (some link macros store the ID, not the URL), retry with the old page title: `searchConfluenceUsingCql(query: 'space = "COLO" AND text ~ "<old-page-title>" AND ancestor = 933068815', limit: 50)`.
3. If the title pass also returns nothing, run a third pass on the bare page ID, since Confluence Smart Links / link macros may store only the page ID (neither the URL nor the title appears in the searchable body text): `searchConfluenceUsingCql(query: 'space = "COLO" AND text ~ "<old-page-id>" AND ancestor = 933068815', limit: 50)`.
3b. Result-count cap warning: if any pass returns a result count equal to its `limit`, the true inbound count may be higher than reported — do not report it as exact. Add the note `검색 결과가 limit에 도달했습니다 — 실제 inbound 링크 수는 표시된 수보다 많을 수 있습니다. 이 페이지가 광범위하게 참조되었다면 Confluence 페이지 내 링크 UI(페이지 정보 → "이 페이지를 링크한 항목")로 전체 수를 직접 확인하세요.` This matters most when superseding a widely-referenced living standard in `05`, where underreporting blast radius could lead the user to approve a repoint that misses many pages.
4. Report the result count (mark it non-exact if step 3b applies). If 0, mark "inbound 없음 (CQL text 검색 기준)" and note that CQL text search cannot guarantee complete inbound-link detection, so recommend a manual spot-check when the old page was widely referenced. If ≥1, list up to 5 titles/IDs and ask the user whether to repoint them to the new page or leave them with the SUPERSEDED banner (banner alone is acceptable). Never edit inbound pages without approval.

#### Inbound Link 수정 부분 실패 처리

When the user approves repointing several inbound pages and some succeed while others fail (for example permission error on one of three):

1. On each failure, record the page ID and error cause and continue to the remaining pages in the approved list. Do not stop on the first failure. Inbound-link repointing operates on independent pages — like Batch Refresh, not like a split package — so stopping early would needlessly abandon pages that would have succeeded and leave more links pointing at the SUPERSEDED page than necessary. Combined with the result-count cap warning (true inbound count may exceed the reported limit), stopping early makes it harder for the user to know which links were missed.
2. At the end, report the succeeded and failed inbound pages as two separate lists (page ID + cause for each failure), so the user has a complete residual list to follow up manually and does not have to re-run the entire inbound check.
3. Do not roll back the succeeded pages — pointing each link to the new (current) page is the safer state for that link on its own.
4. List the failed inbound page IDs and instruct the user to update them manually.
5. Report the supersession cycle as `부분 완료` (not 완료), and include the count of inbound links still pointing at the old page in the readback result.

### Partial Supersession Recovery

Confluence has no real transaction, so the new page can be created while the old page status update fails — leaving both pages active. If that happens:

1. Immediately show the new page ID and URL.
2. Provide the exact text the user must add to the old page to retire it manually: a top banner like `SUPERSEDED BY <new page URL>` and, for ADRs, the 상태 table value `SUPERSEDED` with the 대체 문서 link.
3. Treat the cycle as incomplete until the old page is updated. While it is incomplete, the old page is `Pending supersession`, not `Refresh required`, for `colonova-folder-audit` (see action-taxonomy.md).

## Readback Verification

After create or update, read the page by ID and verify:

- title is correct
- parent is correct
- main sections exist
- body is not empty or broken
- split packages have verification per page ID

Report successes and failures separately.

### Readback Failure Action

- Title mismatch or empty/broken body: report to the user immediately and stop any further writes.
- Parent mismatch: present the page ID and the actual parent ID and ask for manual confirmation; do not silently move.
- Readback API itself fails (404, permission): record the page as `unverified` and ask the user to confirm manually.
- Uncertain single create (the create call fails with a 5xx, timeout, or network error and the response carries no page ID): do not retry blindly — Confluence create is not idempotent and a retry can produce a duplicate. Immediately run a CQL duplicate check under the recommended parent for the proposed title to see whether the page was actually created, report the result, and wait for the user's decision before any retry.
- Uncertain update (the update call fails with a 5xx, timeout, or network error): Confluence update is not idempotent either — it uses optimistic locking on `version.number`, so a blind retry can hit a 409 version conflict or double-apply a change. Do not retry blindly. Instead: (1) re-fetch the page via `getConfluencePage(pageId)` and read its current `version.number` and body; (2) check whether the intended change (including the 변경 이력 row) is already present, to avoid a duplicate row; (3) if the change is not present, present the current live content and the intended diff and ask the user whether to retry; (4) follow this `version-check-then-decide` flow rather than unconditionally stopping or unconditionally retrying.
- For supersession, if either page fails readback, report which one and do not consider the cycle complete; follow Partial Supersession Recovery.

## Whiteboard Source Handling

A Confluence whiteboard is not a normal page; its body cannot be read with `getConfluencePage`. If a whiteboard URL/ID is given as the source draft:

1. Tell the user the whiteboard body cannot be read through the API.
2. Ask the user to paste or export the content as text so it can be routed and templated into a normal page.
3. Do not treat the whiteboard itself as an update/publish target; create a separate page for the converted content.

## Sensitive Content

Warn before publishing:

- passwords
- tokens
- API keys
- private credentials
- internal authentication values
- personal data not necessary for the document

### Block Condition

Do not stop at a warning when the body contains a value matching a credential pattern (for example `Bearer`, `token`, `password`, `secret`, `api[_-]?key`, private key blocks):

1. Mask each matching line as `---REDACTED---` and show the user a masked preview.
2. Warn the user that publishing a credential (token, API key, password, secret) to Confluence is a security risk — it becomes visible in the page, in search results, and in version history. Recommend the safer path first: replace the value with a placeholder (for example `<TOKEN_REDACTED>` or `$ENV_VAR_NAME`) or store it in a secrets manager instead of in the page. Then, only if the user still wants the raw value, ask explicitly: "이 값을 그대로 게시하시겠습니까? 보안 위험을 인지하고 원문 그대로 게시하려면 명시적으로 확인해 주세요." Frame redaction as the default and raw publishing as the exception, so the user does not approve a credential by reflex while approving the document.
3. Do not publish the raw value without that explicit second confirmation.
4. Apply the same pattern scan to the proposed page title, not only the body. A title can carry a credential (for example `API Key: sk-live-xxxx 갱신 절차`), and the title is written to Confluence and visible in search results and breadcrumbs. If a credential pattern matches in the title, mask the matching substring in the pre-approval display and require the same explicit re-confirmation before publishing.

### Scope: create and update

The Block Condition applies to both create and update paths. On an update, scan only the newly supplied draft / changed content — do not re-scan the entire existing body fetched during readback. A credential pattern already present in the live page (not introduced by this change) is treated as already-published information and is not re-masked; apply the Block Condition only when the new content introduces a new credential value. Examples in living standards (`05. 기술문서`) and runbooks (`12. 운영 가이드`) often contain command snippets, so this scoping prevents false re-masking of pre-existing examples while still catching newly added secrets.
