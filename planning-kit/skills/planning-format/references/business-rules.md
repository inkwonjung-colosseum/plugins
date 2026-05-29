# Business Rules

Load when filling policy sections 1 (purpose / problem statement), 10 (business case), 11 (stakeholder), 12 (prioritization), 13 (risk), 14 (roadmap).

## Problem statement (section 1)

- Use the three-part form: 명제 (who has what problem), 신호 (observed evidence — data, interviews, tickets), 성공 정의 (quantitative + qualitative).
- 명제 is one sentence and names a specific user segment, not "users in general".
- 신호 cites at least one source artifact (URL, doc, ticket ID, interview note). When sources are missing, mark `[TBD]` and add a checklist item.
- 성공 정의 maps to at least one BIZ KPI in section 10.

## KPI / OKR (section 10.1)

- Objective is qualitative and ambitious; Key Results are quantitative and time-bounded.
- Each KPI has: name, baseline value (with measurement date and source), target value, measurement cadence, owner.
- Measurement instrument must exist or be planned in feature observability section 16.
- Cost / ROI: include numeric range or 소·중·대 band so trade-offs in section 12 have a real denominator. Bare `[TBD]` without band is an F11 finding.

## Hypothesis (section 10.2)

- Form: "We believe [change] will cause [outcome] because [reasoning]."
- Pair with a falsification condition: what observed value would prove the hypothesis wrong.
- Measurement event names match a business event log entry in feature section 16.
- Learning loop entry is mandatory: review cadence (e.g., D+14 / D+30), decision authority, and where the learning is reflected (POL / FUNC / BIZ ID).
- A hypothesis without measurement is a self-review F9 finding.

## Stakeholder (section 11)

- Section 11 must render three sub-blocks in order: (a) Power × Interest 2×2 table (HH/HL/LH/LL) with stakeholder names assigned to cells; (b) RACI matrix where each activity row has exactly 1 Accountable; (c) per-stakeholder card. Missing any of the three is an F11 finding.
- Each stakeholder card lists communication cadence and channel.
- Approver / decision-maker rows include 사인오프 상태: 미요청 / 요청 / 승인 / 보류 / 거부.
- Conflict between stakeholders becomes a DEC entry in section 12 or a RSK entry in section 13.

## Prioritization (section 12)

- Always include the "do nothing" baseline as an option for comparison.
- Frame choice depends on inputs:
  - RICE (Reach × Impact × Confidence / Effort) when quantitative signals exist.
  - MoSCoW for scope cuts inside a release.
  - Value vs. Risk 2×2 for early discovery.
- Document the score, the inputs that produced it, and the chosen frame.
- Trade-off line is mandatory; "no trade-off" is an F11 finding.
- Re-evaluation trigger is mandatory: time-based (absolute date or quarter) or signal-based (KPI metric + threshold). Missing trigger is an F11 finding.

## Risk register (section 13)

- Each `RSK-XXX` carries likelihood (저 / 중 / 고), impact (저 / 중 / 고), and derived risk score (P0 / P1 / P2).
- Strategy is one of avoid / mitigate / transfer / accept.
- Trigger / early warning is observable (metric threshold, market event, calendar date).
- Owner is a named role or person.
- Residual risk states what remains after mitigation.
- Risks reference the policy or feature IDs they affect.

## Roadmap (section 14)

- Each phase has explicit entry (DoR) and exit (DoD) conditions; ≥1 verifiable item per condition. Empty is an F12 finding.
- Phase 1 = MVP defines the minimum scope to validate hypotheses in section 10.2 and must name ≥1 `BIZ-002` ID; orphan MVP is an F12 finding.
- Subsequent phases reference the learning (BIZ-002 outcome) that triggers them.
- Milestones include hard dates or relative dates (T0 + N weeks); `[TBD]` on milestone alone with no checklist mirror is an F12 finding.
- Rollback condition for each phase names the 지표 and 임계값 (e.g., `p99 latency > 800ms 5분 윈도우`); 정성 표현만 ("문제 발생 시", "성능 저하 시")은 F12 finding.

## Cross-checks

- Every BIZ KPI ties to at least one FUNC and at least one observability event.
- Every RSK references at least one POL or FUNC, or is documented as portfolio-level.
- Every DEC names the option chosen and the option rejected.
- Roadmap phases align with feature section 2 scope statements.
