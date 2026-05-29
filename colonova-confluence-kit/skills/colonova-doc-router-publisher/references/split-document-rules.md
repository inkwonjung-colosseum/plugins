# Split Document Rules

## Mixed Document Detection

Treat a source as mixed when it contains two or more durable roles:

- analysis: current state, problem, requirements, AS-IS
- design: target architecture, API, ERD, domain model
- decision: final choice, rationale, reversal criteria
- technical reference: implementation standard, code/interface rule
- operating guide: repeatable human procedure, checklist, runbook
- monitoring: SLO, alert, dashboard, threshold

If mixed, identify the primary nature and propose companion or extracted documents for the rest.

## Split Actions

| Action | Output | Template |
| --- | --- | --- |
| `Extract decision` | Concise decision page with background, decision, rationale, impact, reversal criteria. | `templates/decision.md` |
| `Extract design` | Design page or design review update with target structure and tradeoffs. | `templates/system-design.md`, or `templates/design-review.md` for a Design Review page |
| `Convert to technical reference` | Living implementation reference or interface rule. | `templates/technical-reference.md` |
| `Convert to operating guide` | Step-by-step procedure, setup, checklist, or runbook. | `templates/operating-guide.md` |

## ADR Rules

ADR pages should prioritize:

- status (structured table: 상태, 대체 문서 link, 날짜, 메모)
- background
- options
- decision
- rationale
- impact
- non-goals when relevant
- open questions when relevant
- reversal or supersession criteria
- 관련 문서 (linked, not copied)
- 변경 이력 (날짜, 변경 내용, 작성자)

Use `templates/adr.md`, which already carries these sections. When an ADR is superseded, set the status table to `SUPERSEDED` with the 대체 문서 link and add a 변경 이력 row; follow `publish-safety.md` → Supersession Rules.

## Operating Guide Rules

`Convert to operating guide` outputs use `templates/operating-guide.md`. It carries 요약, 독자, 사전 조건, 절차(번호 목록), 확인 방법, 실패 대응, 관련 문서, and 변경 이력. `12. 운영 가이드` is a living standard (180-day freshness window); on every refresh append a 변경 이력 row.

## Technical Reference Rules

`Convert to technical reference` outputs use `templates/technical-reference.md`. It carries 요약, 적용 범위, 현재 기준, 구조/동작, 구현 규칙, 비목표(선택), 관련 문서, and 변경 이력. `05. 기술문서` is a living standard (90-day freshness window); on every refresh append a 변경 이력 row.

Move repeatable procedures, setup checklists, incident response, retry/resume policy, verification plans, and detailed logging/observability steps into operating guide or technical reference companions.

## Change History on Updatable Pages

`templates/system-analysis.md` (`01. 시스템 분석`), `templates/system-design.md` (`02. 시스템 디자인` non-Design-Review), `templates/solution.md` (`10. 솔루션` — PoC results, adoption decisions revised over time), and `templates/scheduling.md` (`09. 스케쥴링` — roadmaps/milestones revised over time) all carry a `## 변경 이력` table. When extracting/converting content into any of these, or when updating an existing one, append a 변경 이력 row (날짜 = today, 변경 내용, 작성자 = 미정 if unknown) so current vs. historical stays separated (SSOT #3). For `장애 / Incident` (fallback section map, no local file), append a 변경 이력 row to the fallback 변경 이력 section when an RCA page is re-analyzed or amended with prevention actions after the fact. This matches `publish-safety.md` → Update Rules and SKILL.md step 9.

## Package Confirmation

For split packages, show this table before publishing:

| 문서 | 문서 유형 | 추천 parent | 제목 | 템플릿 | 분리 이유 | 게시 여부 |
| --- | --- | --- | --- | --- | --- | --- |

Create only the documents the user explicitly approves.
