# Routing Rules

## Source of Truth

The live `8.8 ColoNova` root page and linked classification guide are the routing SSOT. Use these fallback rules only when live criteria are missing or incomplete, and mark the result as inferred.

## Role-Based Routing

| Folder | Use when the document is mainly |
| --- | --- |
| `01. 시스템 분석` | problem, requirements, AS-IS, current-state discovery |
| `02. 시스템 디자인` | architecture, API, ERD, TO-BE, domain model, design review |
| `03. 회의록` | dated meeting, attendees, discussion flow, action items |
| `04. 논의사항` | unresolved RFC, options, tradeoffs, open questions |
| `05. 기술문서` | living implementation standard, code structure, ADR, interface rules |
| `06. 장애 / Incident` | real incident, cause, impact, response, RCA |
| `07. 모니터링` | SLI/SLO, alerts, dashboard, threshold, normal/abnormal criteria |
| `08. 결정사항` | settled policy, final direction, reversal criteria |
| `09. 스케쥴링` | roadmap, milestone, release order, dependency timing |
| `10. 솔루션` | vendor, SaaS, OSS, PoC, adoption review |
| `11. 회고 / Retrospective` | KPT, lessons, improvement actions after execution |
| `12. 운영 가이드` | runbook, SOP, onboarding, setup procedure, checklist |
| `99. Archive` | replaced, obsolete, retired, or preserved historical material |

## Boundary Rules

| Boundary | Rule |
| --- | --- |
| Analysis vs Design | Problem and current state go to analysis. Future structure goes to design. |
| Meeting vs Discussion | Date, attendees, and conversation flow go to meeting notes. Durable issue analysis goes to discussion. |
| Discussion vs Decision | Open choices go to discussion. Settled conclusions go to decisions. |
| Technical Doc vs Operating Guide | System understanding and implementation standards go to technical docs. Human procedures go to operating guides. |
| Monitoring vs Operating Guide | Normal/abnormal judgment vs setup or response steps. |
| Solution vs Technical Doc | Adoption review vs adopted team standard. |

## Fallback Templates

Use these section maps only when no local template file matches.

| Type | Sections |
| --- | --- |
| 시스템 분석 | 요약, 배경, 현재 상태, 문제 정의, 요구사항, 영향 범위, 열린 질문, 다음 단계 |
| 시스템 디자인 | 요약, 배경, 목표, 설계 범위, 제안 구조, 주요 흐름, 대안, 리스크, 다음 단계 |
| 논의사항 | 요약, 배경, 쟁점, 선택지, 트레이드오프, 현재 의견, 결정 필요 사항, 다음 단계 |
| 기술문서 | 요약, 적용 범위, 현재 기준, 구조/동작, 구현 규칙, 관련 문서, 변경 이력 |
| 장애 / Incident | 요약, 발생 정보, 현상, 원인, 대응, 재발 방지, 후속 액션 |
| 모니터링 | 요약, 관찰 대상, 정상/이상 기준, 알림, 대시보드, 대응 문서 |
| 스케쥴링 | 요약, 범위, 마일스톤, 의존성, 리스크, 변경 이력 |
| 솔루션 | 요약, 검토 배경, 후보, 평가 기준, 비교, PoC, 도입 판단 |
| 회고 / Retrospective | 회고 정보, 잘된 점, 아쉬운 점, 배운 점, 개선 액션 |
| 운영 가이드 | 요약, 독자, 사전 조건, 절차, 확인 방법, 실패 대응, 관련 문서 |
