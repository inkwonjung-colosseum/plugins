# Conversion Rules

Use during image handling, body merge, and policy/feature document generation.

## Source merge

- Text/file/directory input is source 0.
- URL and discovered child URLs follow BFS source order.
- Images can come from input files, directories, markdown/HTML references, image content-type responses, or inline `data:image`.
- For images, transcribe visible text and describe screen/flow/diagram meaning. Prefix uncertain inference with `추정:`.

## Feature name

Prefer explicit user topic, then URL title/H1, file stem, directory name, repeated heading, then first core noun phrase. Keep one feature name; track other candidates as excluded input.

## Template generation

Read both templates in the same turn:

- `templates/정책서.md`: 15-section policy document with business case, stakeholders, prioritization, risk register, and roadmap.
- `templates/기능설계서.md`: 18-section feature design document with personas/journey, acceptance criteria, data model, API/event, NFR, UX writing, design system, test scenarios, observability, and DoR/DoD.

Templates use field lists and `### item` cards by default. Add Markdown tables only for short 2-4 column comparisons, journey maps, state transitions, message catalogs, or other inherently tabular content. Do not leave empty placeholder rows. Use `[TBD]` for missing evidence and mirror it in unresolved items.

## Requirement ID convention

Policy doc prefixes: `POL-` (rules), `BIZ-` (business case/KPI/hypothesis), `RSK-` (risk), `DEC-` (decision).
Feature doc prefixes: `FUNC-` (function), `AC-` (acceptance criteria), `DATA-` (data entity), `API-` (API/event), `NFR-` (non-functional), `TEST-` (test scenario).

Assign IDs sequentially within each prefix (POL-001, POL-002, ...). Cross-document links use the explicit ID (e.g., `FUNC-001 ↔ POL-003`). If draft does not surface an entity for a section, leave the section with `[TBD]` and a checklist item — do not invent IDs without source evidence.

`NFR-` uses categorical suffixes (`NFR-PERF`, `NFR-AVAIL`, `NFR-SEC`, `NFR-A11Y`, `NFR-OPS`) corresponding to feature sections 12.1-12.5; all other prefixes use sequential numbering. When a section has multiple NFR cards, append `-001`, `-002` etc. to the suffix (e.g., `NFR-PERF-001`, `NFR-PERF-002`).

## Mapping

Business / strategic layer (policy doc):

- Rules, limits, allowed/forbidden criteria, terms, scope, principles -> policy core (sections 1-9).
- KPI, OKR, success metric, baseline, target, ROI, cost/benefit, hypothesis, experiment plan -> policy section 10 (business case).
- Decision-maker, approver, RACI, stakeholder concern, communication cadence, sign-off -> policy section 11 (stakeholder).
- Option comparison, RICE / MoSCoW / Value-Risk frame, trade-off, do-nothing baseline -> policy section 12 (prioritization).
- Risk, likelihood, impact, mitigation, early warning, residual risk -> policy section 13 (risk register).
- Release phase, MVP / v1 / v2 scope, entry/exit gate, milestone, rollback -> policy section 14 (roadmap).
- State transitions, processing criteria, exceptions, approvals, external integration -> policy sections 6/8/9.

UX layer (feature doc 1-7, 8, 13-14):

- UI, fields, buttons, messages, visible behavior, user flow, trigger, action sequence -> feature sections 3-5.
- Permission/data visibility -> both documents, split by policy intent vs screen/action access.
- Persona attributes (role, goal, pain, tool familiarity), end-to-end journey, emotion curve, touchpoint -> feature section 8.
- Tone, voice, banned words, message catalog (success/warning/error/empty/loading) -> feature section 13.
- Design system, component, design token, Figma link, Code Connect -> feature section 14.

Specification layer (feature doc 9-12, 15-17):

- Given-When-Then conditions, observable result, measurement method, priority P0/P1/P2 -> feature section 9 (acceptance criteria).
- Entity, attribute, type, constraint, relationship, lifecycle, retention -> feature section 10 (data model).
- API endpoint, request/response schema, error code, idempotency, event topic/payload, webhook, integration contract -> feature section 11 (API/event).
- Latency, throughput, SLA/SLO, RTO/RPO, threat model, WCAG accessibility, i18n locale, deploy/rollback -> feature section 12 (NFR).
- Happy / edge / negative / regression scenario, test data, automation tier (E2E/API/Unit) -> feature section 15 (test scenarios).
- Business event log, KPI dashboard, system metric, alarm threshold, trace id -> feature section 16 (observability).
- Pre-implementation readiness check, pre-release done check, rollback plan, release notes -> feature section 17 (DoR/DoD).

- Anything unmapped -> exclusion tracking.

## Cross-document anchors

Policy rules, states, permissions, exceptions, integrations, KPIs, hypotheses, risks, and roadmap phases should name related feature behavior (`FUNC-XXX`, `AC-XXX`). Feature actions, ACs, data entities, APIs, NFRs, and test scenarios should name related policy IDs (`POL-XXX`, `BIZ-XXX`, `RSK-XXX`). Missing back-link is a self-review F4 finding.

## Terms

Policy prefers domain/system terms. Feature UI fields prefer Korean label first with system term in parentheses, such as `존 코드 (Zone Code)`.

## Auxiliary tables

Use `### N.M [purpose] 보조 표` only when a list is too heterogeneous for one field. Number sequentially. No legacy backlink suffix. Max nested depth is 3; deeper detail stays summarized with an exclusion note. The journey map (8.2), state transition (10.2), and message catalog (13.2) are first-class tables and are not counted as auxiliary tables.
