# Self-Review Rules

Use after draft generation unless `--no-self-review`.

Self-review is a feedback gate, not an auto-rewrite pass. Mechanical fixes may be applied. Meaning changes require user approval and go to `## 체크해야 할 항목`.

## Passes

F1 section completeness:

- Each policy section 0-15 has content or an explicit `[TBD]` with checklist mirror.
- Each feature section 0-18 has content or an explicit `[TBD]` with checklist mirror.
- Auxiliary tables, journey map (feature 8.2), state transition (feature 10.2), and message catalog (feature 13.2) have data rows when the section is in scope.
- Journey map (feature 8.2) emotion column must be integer 1-5; non-numeric value (e.g., `좋음`, `중립`) is a finding.
- If a journey stage row is intentionally omitted, the row must carry `[scope-out: <reason>]`; bare empty row is a finding.
- `[TBD]` ratio is not dominant.

F2 layer bleed:

- Policy core rules avoid UI words such as button, click, input form, banner.
- Feature behavior avoids acting as the policy source for allowed/forbidden/approval rules.
- Strategic items (KPI, OKR, hypothesis, stakeholder, prioritization, risk, roadmap) live in the policy doc, not the feature doc.
- Specification items (AC, data model, API/event, NFR, test scenarios, observability, DoR/DoD, design system) live in the feature doc, not the policy doc.

F3 term consistency:

- One label per role, state, permission, persona, and domain stem inside each layer.
- Feature UI label may pair Korean label with system term in parentheses.

F4 policy-feature mapping (ID traceability):

- Policy rules/states/permissions/KPIs/risks map to feature actions, exceptions, ACs, or test scenarios using explicit IDs.
- Forbidden policy actions do not appear as normal feature flow.
- Every `FUNC-XXX` references at least one `POL-XXX` or `BIZ-XXX`. The operational-only escape requires an explicit `[OPERATIONAL-ONLY, 근거: <문장>]` marker inside the FUNC card; bare prose justification is a finding.
- Every `POL-XXX` rule card must have non-empty `관련 기능 동작:` listing ≥1 `FUNC-XXX`, OR carry `[POLICY-ONLY, 근거: <문장>]` marker. Empty `관련 기능 동작:` without marker is a finding.
- Every `AC-XXX` references the `FUNC-XXX` it validates and the `TEST-XXX` that exercises it, if a test scenario exists.
- Every `DATA-XXX` referenced in a state transition or in any `AC-XXX` Given/Then clause must be touched by ≥1 `API-XXX` and ≥1 `TEST-XXX`.
- Every `DATA-XXX` defined in section 10.1 must be either (a) referenced by ≥1 `API-XXX` or `AC-XXX`, or (b) carry an explicit `[REFERENCE-ONLY, 근거: <문장>]` marker. Orphan entity is a finding.
- Every `DEC-XXX` must have non-empty `재검토 시점:` (time-based date or signal-based metric + threshold) and be referenced from at least one POL/FUNC body that implements its 선택안.
- Risks (RSK-) reference the policy/feature ID they materially affect.
- IDs are unique within a `planning/[안전기능명]--…/` folder across both documents; corpus-level collisions are namespaced by 문서 ID (정책서·기능설계서 0절).

F5 missing source facts:

- Explicit roles, states, feature names, thresholds, authority facts, KPI baselines/targets, persona attributes, API fields, NFR numbers, and AC measurement methods appear in documents or exclusions.
- Fetch failures, scope exclusions, and source-definition gaps are cross-referenced.

F6 Markdown syntax:

- Fence pairs balanced.
- Header levels sane.
- No legacy auxiliary-table backlink suffix.
- No reserved wrapper headings inside generated bodies.
- No wide default feedback table.

F7 acceptance criteria shape:

- Each `AC-XXX` uses Given / When / Then form with an observable result and a measurement method.
- AC priority is P0, P1, or P2 (no other tier).
- AC without a matching FUNC is a finding.
- Every P0 AC must have a matching `TEST-XXX` of P0 priority; missing or weaker test is a finding.
- AC measurement method must reference an existing observability event (section 16) or call out a `[TBD]` event.

F8 data and contract shape:

- `DATA-XXX` entries list at least name, attributes with type and required flag, and a relationship or lifecycle note.
- `API-XXX` entries list kind, request schema, response schema, and error codes.
- State transition rows (feature 10.2) align with policy section 6 state names.

F9 NFR and risk completeness:

- At least one NFR sub-section (12.1-12.5) is populated when feature is user-facing; otherwise excluded with a note.
- Each `RSK-XXX` has likelihood, impact, mitigation, and owner.
- Accessibility WCAG level is set when feature has a UI surface.
- NFR numeric placeholders must resolve to concrete values or explicit `[TBD]` with a checklist item; "fast", "secure", "scalable" alone are findings.
- Every NFR with a numeric target must reference at least one `TEST-XXX` (perf / security / accessibility) or be marked `[검증 보류]` with a checklist item.
- Each `BIZ-002` hypothesis must close the loop: hypothesis -> measurement event in section 16 -> `TEST-XXX` that asserts the event fires. Missing link is a finding.
- Every `RSK-XXX` with risk score P0 must name a mitigation TEST or operational drill.

F10 release readiness:

- DoR (feature 17.1) and DoD (feature 17.2) have explicit pass/fail items, not `[TBD]` blanket entries, when the feature targets a release phase in policy section 14.
- DoD (feature 17.2) each gate must have a named 책임자 (역할 또는 인명). Missing 책임자 is a finding.
- Rollback drill DoD row must specify drill_date, restored_target, evidence_link; narrative-only ("롤백 점검 완료") is a finding.
- Roadmap phase reference matches between policy section 14 and feature section 2.
- Regression matrix (15.2) is filled when the change touches any pre-existing FUNC, DATA, or API. Each affected FUNC row must list at least one AC and at least one TEST (or a `[TBD]` with checklist item).
- Each regression row carries `blast radius` (single user / cohort / tenant / all). Missing blast radius is a finding.
- DoR includes the gates: regression matrix complete, hypothesis measurement event mapped, NFR numeric targets resolved, security and accessibility reviewed.

F11 policy strategic completeness:

- Every `BIZ-001` KPI card must have non-empty Owner, 기준선 측정일/출처, 목표값, 측정 주기. Missing field is a finding.
- Every `BIZ-002` hypothesis must have falsification condition, learning loop cadence, decision-maker, and reflection location (POL/FUNC/BIZ ID).
- Every `DEC-XXX` must include `Do nothing` baseline in 옵션 비교, non-blank 트레이드오프 line, and a re-evaluation trigger (time-based date or signal-based metric+threshold). Missing any of the three is a finding.
- Stakeholder section 11 must contain a populated Power × Interest grid (≥1 data cell with a stakeholder identifier — organization or person name; framework hints like `Manage closely`/`Keep satisfied`/`Keep informed`/`Monitor` do not count) AND a RACI matrix with ≥1 activity row, each row having exactly 1 Accountable. Empty matrix or Accountable count ≠ 1 is a finding.
- Every stakeholder card with 역할 = Approver must have 사인오프 상태 set to one of (미요청 / 요청 / 승인 / 보류 / 거부); blank is a finding.

F12 roadmap policy-side completeness:

- Each policy section 14.N phase must have:
  - Non-blank 진입 조건 (DoR) with ≥1 verifiable item;
  - Non-blank 종료 조건 (DoD) with ≥1 verifiable item;
  - Concrete 출시 목표일 (absolute date or T0 + N weeks); `[TBD]` is allowed only with a checklist mirror;
  - Concrete 롤백 기준 carrying both 지표명 and 임계값 (e.g., "p99 latency > 800ms" or "error rate ≥ 2% in 5분 윈도우"); 정성 표현만("문제 발생 시", "성능 저하 시") is a finding.
- Phase 1 = MVP must reference at least one `BIZ-002` hypothesis it intends to validate; orphan MVP without hypothesis link is a finding.

## Classification

- Mechanical stabilization: may update body.
- Display-only transformation: may update screen rendering.
- Suggested fix: checklist first, body unchanged.
- User/external decision: checklist first, body unchanged.

When there are no findings, keep `## 체크해야 할 항목` and write `없음`.
