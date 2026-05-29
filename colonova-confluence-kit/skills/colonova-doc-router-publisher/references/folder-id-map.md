# Folder ID Map (cache)

This is a cache of live top-level folder titles and page IDs under root `933068815`. It is **not** the SSOT. Live `getConfluencePageDescendants(933068815)` is authoritative. If a row is unknown or disagrees with live, resolve from live and update this row.

The top-level pageIds below were resolved from a live `getConfluencePageDescendants(933068815)` run on 2026-05-29. The tree is actively maintained, so a folder could in principle be re-created with a new ID; if a cached ID does not resolve to the expected folder in live, discard it and re-resolve. Always trust live over this cache when they disagree.

Re-resolving and writing pageIds back is optional and best-effort. It only helps when the runtime supports persistent local file writes and the file survives between sessions (true in Claude Code project context; not guaranteed in every Codex/Cursor environment). If a write is unsupported or fails, skip it silently and always fall back to live resolution — never treat a failed cache write as an error, and never block routing on it.

| Classification name | Live full title | Live pageId (resolved 2026-05-29) |
| --- | --- | --- |
| `01. 시스템 분석` | `01. 시스템 분석 - ColoNova` | `932642831` |
| `02. 시스템 디자인` | `02. 시스템 디자인 - ColoNova` | `932806686` |
| `03. 회의록` | `03. 회의록 - ColoNova` | `932675630` |
| `04. 논의사항` | `04. 논의사항 - ColoNova` | `932773920` |
| `05. 기술문서` | `05. 기술문서 - ColoNova` | `933036056` |
| `06. 장애 / Incident` | (not created) | 미생성 — create under 933068815 only after user approval |
| `07. 모니터링` | `07. 모니터링 - ColoNova` | `932642832` |
| `08. 결정사항` | `08. 결정사항 - ColoNova` | `1178240081` |
| `09. 스케쥴링` | `09. 스케쥴링 - ColoNova` | `1221033989` |
| `10. 솔루션` | `10. 솔루션 - ColoNova` | `1371602946` |
| `11. 회고 / Retrospective` | `11. 회고 / Retrospective - ColoNova` | `1445560321` |
| `12. 운영 가이드` | `12. 운영 가이드 - ColoNova` | `1534591019` |
| `99. Archive` | `99. Archive - ColoNova` | `1774223491` |

## Known Subfolders

These subfolders are documented in `routing-rules.md` → Subfolder Routing. The pageIds below were resolved from a live `getConfluencePageDescendants(933068815, depth=2)` run on 2026-05-29 (a `confirmed ID` row, not a `fill-on-first-resolution` placeholder). Listing them here lets routing recognize a known subfolder and use its ID directly without re-fetching, and lets `colonova-folder-audit` step 3b skip confirmed rows and flag only genuinely new subfolders. Subfolders evolve, so live children remain authoritative — if a cached ID no longer resolves to the expected subfolder, discard it and re-resolve.

| Parent (classification) | Subfolder classification name | Live full title | Live pageId (resolved 2026-05-29) |
| --- | --- | --- | --- |
| `03. 회의록` | `위클리` | `위클리 - ColoNova` | `1778581670` |
| `03. 회의록` | `프로젝트 Status 공유` | `프로젝트 Status 공유 - ColoNova` | `1778286687` |
| `04. 논의사항` | `ColoNova 데이터모델링 ERD 설계` | `ColoNova 데이터모델링 ERD 설계` | `1665597710` |
| `05. 기술문서` | `ADR` | `ADR - ColoNova` | `1778810882` |
| `05. 기술문서` | `인증 인가 계정 권한` | `인증 인가 계정 권한` | `1443627012` |

The ` - ColoNova` suffix is **inconsistent** on subfolders (confirmed 2026-05-29): `위클리`, `프로젝트 Status 공유`, and `ADR` carry it (`위클리 - ColoNova`), while `ColoNova 데이터모델링 ERD 설계` and `인증 인가 계정 권한` do not. Do not assume a suffix either way — match a subfolder by its resolved `Live pageId` (preferred) or by the role-name portion of the title, and trust live children if a title differs from this table.

API note: `getConfluencePageDescendants` returns 404 when called directly on a `type: "folder"` entity ID. Enumerate a folder's children by calling it on the root `933068815` with sufficient `depth` and reading the `parentId`/`type` fields, not by calling it on the folder ID. This is why the subfolder IDs above were resolved via a depth=2 root descendants traversal.

## Resolution Rule

1. Match the live folder by `NN.` number prefix plus role name, ignoring the ` - ColoNova` suffix.
2. Use the resolved pageId as the create/update parent.
3. If a known subfolder applies, use its confirmed `Live pageId` from the Known Subfolders table directly; otherwise resolve it under the matched parent's live children before finalizing the parent.
3a. For subfolders, the ` - ColoNova` suffix is inconsistent (see Known Subfolders), so do not match on an assumed suffix. Prefer the confirmed `Live pageId`; if matching by title, match on the role-name portion. The live children of the resolved parent are authoritative if the title differs from the table.
4. If `06. 장애 / Incident` is the target, follow `publish-safety.md` → Missing Folder Handling before publishing.
5. The top-level and known-subfolder pageIds above were resolved live on 2026-05-29; use them as a speed cache, but if one does not resolve to the expected folder/subfolder in live, discard it and re-resolve. Never invent a numeric ID.
