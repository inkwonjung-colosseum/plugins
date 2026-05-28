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

| Action | Output |
| --- | --- |
| `Extract decision` | Concise decision page with background, decision, rationale, impact, reversal criteria. |
| `Extract design` | Design page or design review update with target structure and tradeoffs. |
| `Convert to technical reference` | Living implementation reference or interface rule. |
| `Convert to operating guide` | Step-by-step procedure, setup, checklist, or runbook. |

## ADR Rules

ADR pages should prioritize:

- status
- background
- options
- decision
- rationale
- impact
- non-goals when relevant
- open questions when relevant
- reversal or supersession criteria

Move repeatable procedures, setup checklists, incident response, retry/resume policy, verification plans, and detailed logging/observability steps into operating guide or technical reference companions.

## Package Confirmation

For split packages, show this table before publishing:

| 문서 | 문서 유형 | 추천 parent | 제목 | 템플릿 | 분리 이유 | 게시 여부 |
| --- | --- | --- | --- | --- | --- | --- |

Create only the documents the user explicitly approves.
