# Routing Rules

## Source of Truth

The live `8.8 ColoNova` root page and linked classification guide are the routing SSOT. Use these fallback rules only when live criteria are missing or incomplete, and mark the result as inferred.

## Folder Title and ID Resolution

The short folder names in the routing table below are classification references only. They are not the live page titles.

- Live top-level folder titles carry a ` - ColoNova` suffix, for example `01. 시스템 분석 - ColoNova`, `02. 시스템 디자인 - ColoNova`.
- Never match a parent by short name alone. Resolve the actual parent by `getConfluencePageDescendants(933068815)` and match on the `NN.` number prefix plus role name, or use the page ID directly.
- The cached `folder-id-map.md` (in this references folder) may be used to speed up resolution, but live descendants are the SSOT; if the map and live disagree, trust live.
- For folders with a slash in the name (`06. 장애 / Incident`, `11. 회고 / Retrospective`), the live title uses spaces on both sides of the slash (` / `): the live `11` folder is `11. 회고 / Retrospective - ColoNova` (confirmed 2026-05-29). Use `folder-id-map.md` → `Live full title` for the exact string when a human needs to copy a title to search; do not reconstruct it from the classification name.

## Role-Based Routing

Folder column shows the classification name; the live title adds the ` - ColoNova` suffix.

| Folder (classification name) | Use when the document is mainly |
| --- | --- |
| `01. 시스템 분석` | problem, requirements, AS-IS, current-state discovery |
| `02. 시스템 디자인` | architecture, API, ERD, TO-BE, domain model, design review |
| `03. 회의록` | dated meeting, attendees, discussion flow, action items |
| `04. 논의사항` | unresolved RFC, options, tradeoffs, open questions |
| `05. 기술문서` | living implementation standard, code structure, ADR, interface rules |
| `06. 장애 / Incident` | real incident, cause, impact, response, RCA — **live 폴더 미생성. 게시 전 폴더 존재 확인 및 생성 승인 필요 (see publish-safety.md Missing Folder Handling)** |
| `07. 모니터링` | SLI/SLO, alerts, dashboard, threshold, normal/abnormal criteria |
| `08. 결정사항` | settled policy, final direction, reversal criteria |
| `09. 스케쥴링` | roadmap, milestone, release order, dependency timing |
| `10. 솔루션` | vendor, SaaS, OSS, PoC, adoption review |
| `11. 회고 / Retrospective` | KPT, lessons, improvement actions after execution |
| `12. 운영 가이드` | runbook, SOP, onboarding, setup procedure, checklist |
| `99. Archive` | replaced, obsolete, retired, or preserved historical material |

## Subfolder Routing

Some top-level folders have live subfolders. Route into the subfolder when it matches; otherwise place directly under the top-level folder. Confirm by reading the recommended parent's immediate children before finalizing the parent.

| Top-level | Live subfolders | Use the subfolder when |
| --- | --- | --- |
| `03. 회의록` | `위클리`, `프로젝트 Status 공유` | recurring weekly notes → `위클리`; project-level status sharing → `프로젝트 Status 공유`; one-off topic meetings → directly under `03` |
| `04. 논의사항` | `ColoNova 데이터모델링 ERD 설계` | ERD 설계 방향이 아직 미결인 논의·선택지·RFC → that subfolder; 확정 ERD 산출물은 `02. 시스템 디자인`으로; other discussions → directly under `04` |
| `05. 기술문서` | `ADR`, `인증 인가 계정 권한` | ADR-format decisions → `ADR`; auth/authorization/account/permission domain docs → `인증 인가 계정 권한`; other living standards → directly under `05` |

Only `03`, `04`, and `05` carry live subfolders today (confirmed 2026-05-29). `01`, `02`, `07`, `08`, `09`, `10`, `11`, `12`, `99` have none yet — place documents directly under those top-level folders.

Subfolders evolve. Always reconcile against live children; if a listed subfolder is gone or a new one appears, trust the live tree. If a new subfolder appears in the live children that is not listed here, place the document into it when it matches, and record it for `colonova-engineering-docs-audit` to surface on its next run as a 신규 subfolder so this table (and `folder-id-map.md` → Known Subfolders) can be updated. This closes the drift loop between the routing taxonomy and the live tree.

## Boundary Rules

| Boundary | Rule |
| --- | --- |
| Analysis vs Design | Problem and current state go to analysis. Future structure goes to design. |
| Meeting vs Discussion | Date, attendees, and conversation flow go to meeting notes. Durable issue analysis goes to discussion. |
| Discussion vs Decision | Open choices go to discussion. Settled conclusions go to decisions. |
| Technical Doc vs Operating Guide | System understanding and implementation standards go to technical docs. Human procedures go to operating guides. |
| Monitoring vs Operating Guide | Normal/abnormal judgment vs setup or response steps. |
| Solution vs Technical Doc | Adoption review vs adopted team standard. |
| Design (ERD artifact) vs Discussion (ERD subfolder) | 확정된 ERD 산출물, TO-BE 데이터 모델, 인터페이스 계약은 `02. 시스템 디자인`으로. 미결 ERD 선택지, 트레이드오프, 열린 질문은 `04. 논의사항 / ColoNova 데이터모델링 ERD 설계`로. |

## Fallback Templates

This table's `Local template` column is the single source of truth for the doc-type → template mapping; SKILL.md step 6 defers to it. When adding a template, update this column only. Types with a local template file must use that file first; the section maps here are fallback only for the remaining `(fallback only)` types with no local file. SKILL.md step 6 enforces local-first selection.

Every doc type that can be revised as a current reference includes a `변경 이력` section (in its local template or its fallback section map): 시스템 분석, 시스템 디자인, 기술문서, 결정사항, 운영 가이드, 스케쥴링, 솔루션, and 장애/Incident (for RCA pages re-analyzed or amended with prevention actions after the fact). This lets `publish-safety.md` → Update Rules append a 변경 이력 row on every update, keeping current vs. historical separated (SSOT #3) even for fallback-only types. 회의록 and one-off 모니터링 dashboard pages are point-in-time and do not carry 변경 이력.

| Type | Local template | Sections |
| --- | --- | --- |
| 시스템 분석 | `templates/system-analysis.md` | 요약, 배경, 현재 상태, 문제 정의, 요구사항, 영향 범위, 열린 질문, 다음 단계, 변경 이력 |
| 시스템 디자인 | `templates/system-design.md` (Design Review: `templates/design-review.md`) | 요약, 배경, 목표, 설계 범위, 제안 구조, 주요 흐름, 대안, 리스크, 다음 단계 |
| 회의록 | `templates/meeting-notes.md` | 회의 유형, 날짜, 참여자, 장소, 회의 목표, 회의 내용, 결정 사항, 액션 아이템 |
| 논의사항 | `templates/discussion.md` | 요약, 배경, 쟁점, 선택지, 트레이드오프, 현재 의견, 결정 필요 사항, 다음 단계 |
| 기술문서 | `templates/technical-reference.md` (ADR: `templates/adr.md`) | 요약, 적용 범위, 현재 기준, 구조/동작, 구현 규칙, 관련 문서, 변경 이력 |
| 장애 / Incident | (fallback only) | 요약, 발생 정보, 현상, 원인, 대응, 재발 방지, 후속 액션, 변경 이력 |
| 모니터링 | (fallback only) | 요약, 관찰 대상, 정상/이상 기준, 알림, 대시보드, 대응 문서 |
| 결정사항 | `templates/decision.md` | 상태, 요약, 배경, 결정, 근거, 영향 범위, 역전/재검토 기준, 관련 문서, 변경 이력 |
| 스케쥴링 | `templates/scheduling.md` | 요약, 범위, 마일스톤, 의존성, 리스크, 변경 이력 |
| 솔루션 | `templates/solution.md` | 요약, 검토 배경, 후보, 평가 기준, 비교, PoC, 도입 판단, 관련 문서, 변경 이력 |
| 회고 / Retrospective | (fallback only) | 회고 정보, 잘된 점, 아쉬운 점, 배운 점, 개선 액션 |
| 운영 가이드 | `templates/operating-guide.md` | 요약, 독자, 사전 조건, 절차, 확인 방법, 실패 대응, 관련 문서, 변경 이력 |
