# QA Rules

Load when filling feature design sections 9 (AC), 15 (test scenarios), 16 (observability), 17 (DoR/DoD).

## Acceptance criteria (section 9)

- Each `AC-XXX` uses Given / When / Then exactly. Multiple Givens or Thens are allowed as bullet lists.
- Each AC has an observable result and a measurement method (log event, UI state, API response, metric).
- Priority is P0, P1, or P2:
  - P0 blocks release; failure means feature cannot ship.
  - P1 must pass before release; failure means hotfix or known-issue note.
  - P2 polish; failure tracked but not blocking.
- Every AC names its mapped FUNC ID and (if a test exists) its TEST ID.
- AC with no clear measurement method must include a `[TBD]` measurement and a checklist item.

## Test scenarios (section 15.1)

- Categorize each scenario: happy / edge / negative / regression / performance / security / accessibility / chaos (fault-injection·failover) / data-migration (dry-run·backfill) / contract (consumer-driven, schema compatibility).
- Provide concrete test data (not "valid input" — give the value or fixture path).
- Steps are numbered, imperative, deterministic; no "verify it works" wording.
- Expected result is observable: response code, log line, UI text, persisted row, alarm fired.
- Automation tier: E2E / API / Contract / Unit / 수동만. Automation location is a file path or `[TBD]`.

## Regression matrix (section 15.2)

- Required when the change touches an existing FUNC, DATA, or API.
- Each row links: change ID -> affected FUNC IDs -> affected AC IDs -> affected TEST IDs -> blast radius -> affected entity count -> dependent service count -> risk priority -> automation flag.
- A change with affected ACs and no covering TEST is a self-review F10 finding.
- Risk priority follows AC priority of the most severe impacted AC.
- Row completeness rule: every affected FUNC must list at least one AC and at least one TEST (or `[TBD]` with a checklist item). Any blank in those columns is a finding.
- Blast radius is one of `single` (one user), `cohort` (defined segment), `tenant` (one organization), or `all`. Higher blast radius forces priority up by one tier unless explicitly justified.
- Quantitative impact: affected entity count and dependent service count populate the impact magnitude used in policy section 13 risk scoring.

## Test data and environment (section 15.3)

- Fixture location is a path or repo link, not "see staging DB".
- Test users / roles cite policy section 7 to inherit permission rules.
- External system mocks list the contract version they pin to.
- Cleanup procedure prevents cross-test contamination; for shared envs document tenant or namespace isolation.

## Defect classification

- Use severity P0 / P1 / P2 aligned with AC priority. Do not introduce parallel severity scales.
- Each defect references the failing AC ID, the TEST ID that reproduced it, and the mapping FUNC.
- Field for blast radius: single user / cohort / tenant / all.

## Observability for QA (section 16)

- Each AC with a measurement type "log event" or "metric" must list the exact event name and required fields in section 16.
- Alarm thresholds in 16.1 link to a P0 or P1 outcome so QA can trace alarm-to-customer-impact.
- Synthetic monitors / smoke tests live in 15 with the production schedule referenced in 16.

## DoR / DoD (section 17)

- DoR items are pre-implementation gates; each gate is a checkbox with a verifiable artifact.
- DoD items are pre-release gates; each gate has an owner column populated (역할 or 인명). Missing owner is an F10 finding.
- For features rolled out behind a feature flag, DoD includes a flag-on validation step and a rollback drill record with fields: `drill_date`, `restored_target`, `evidence_link` (runbook URL / 녹화 / report 경로). 책임자는 DoD 표 책임자 열에서 별도로 표기한다. Narrative-only ("rollback 검증 완료") is an F10 finding.
- DoD requires the regression matrix (15.2) to be filled and AC-mapped tests to be green.

## NFR ↔ TEST traceability

- Every NFR sub-section (12.1 perf, 12.2 avail, 12.3 sec, 12.4 a11y, 12.5 ops) that holds numeric targets must list a `매핑 TEST: TEST-XXX` row referencing a test in section 15.
- An NFR numeric target without a mapped TEST and without a `[검증 보류]` checklist item is a self-review F9 finding.
- TEST scenarios that validate NFR thresholds carry the same threshold values in their expected result; mismatch is a finding.

## Hypothesis loop closure (BIZ-002 → Event → TEST)

- Every `BIZ-002` hypothesis must name a measurement event (section 16) by event name.
- Every named measurement event must appear in section 16 with required fields and retention.
- Every named measurement event must have a `TEST-XXX` that asserts the event fires for the corresponding happy-path AC.
- DoR (17.1) blocks until the hypothesis-event-test loop is closed; DoD (17.2) verifies the events are actually emitted after deployment.

## Cross-checks

- Every P0 AC has at least one TEST entry whose priority is P0.
- Every API (synchronous or event) has at least one Contract or API-tier test.
- Every NFR with numeric targets has a performance, security, or accessibility test scenario, or an explicit exclusion note.
- Every BIZ-002 hypothesis closes the loop hypothesis -> event -> test.
- Every named measurement event in section 16 has a `TEST-XXX` that asserts emission, regardless of whether it backs a hypothesis or general telemetry.
- Every regression matrix row carries a blast radius value.
