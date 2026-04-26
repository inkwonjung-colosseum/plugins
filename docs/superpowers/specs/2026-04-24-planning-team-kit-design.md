# planning-team-kit Design

Date: 2026-04-24
Status: Draft for user review
Owner: developjik
Scope: Claude Code and Codex compatible planning-team plugin

## Summary

`planning-team-kit` is a dual-platform plugin for planning teams that need consistent, high-quality planning documents. It should not behave as a generic document generator or as a project management automation platform. Its core job is to help a planner turn an early idea into aligned planning artifacts through a repeatable flow:

1. Define and align the planning context.
2. Generate the right planning artifacts.
3. Review and improve the output before human handoff.

Internally, the plugin may use a richer pipeline:

```text
brainstorming -> direction criteria -> planning-drafts -> quality gate
```

Externally, users should experience only three simple stages:

```text
define/align -> generate documents -> review/improve
```

This keeps quality control strong without forcing planning users to learn a heavy framework.

## Problem

Planning documents currently fail in predictable ways:

- The problem definition is weak or unclear.
- Requirements are ambiguous and require engineering interpretation.
- Edge cases, operating policies, and exception handling are missing.
- Success criteria are not measurable.
- Document structure and terminology vary by author.

These failures are not solved by a PRD template alone. The plugin needs to guide the planning process before document generation, then apply consistent review criteria after generation.

## Goals

- Create consistent planning artifacts for product and planning teams.
- Start every serious planning task with structured brainstorming and alignment.
- Support multiple final artifact types, not only PRDs.
- Enforce quality through lightweight readiness and review gates.
- Keep Claude Code and Codex support in one shared plugin directory.
- Default to draft-only behavior with clear human ownership and approval.
- Keep v0.1 small enough to ship and test with a planning team pilot.

## Non-Goals

- Do not publish or overwrite Jira, Confluence, Slack, Google Drive, or Notion content in v0.1.
- Do not automate final business decisions.
- Do not become a full project management platform.
- Do not build dashboards, analytics tracking, or approval workflow engines in v0.1.
- Do not include domain-specific planning logic such as payments, growth, or operations vertical templates in v0.1.
- Do not expose every internal pipeline step as a required user step.

## Design Principles

- Draft-first: generated artifacts are drafts until a human approves them.
- No source, no claim: unsupported factual claims must be marked as assumptions.
- Read-first integration: external systems are future input sources before they become write targets.
- Standard-first artifact suite: v0.1 always generates the same standard suite to keep the workflow predictable.
- One question at a time: planning-intake should reduce ambiguity without turning planning into a meeting.
- Decisions before documents: document generation should follow explicit alignment on problem, audience, goals, non-goals, and success criteria.
- Internal rigor, external simplicity: keep the user-facing workflow short even if the internal quality model is richer.

## User-Facing Workflow

### Stage 1: Define and Align

The user brings an idea, meeting note, rough requirement, or product problem. The plugin asks only the highest-leverage questions needed to create a stable planning context.

Primary outputs:

- One-line problem definition
- Target users or stakeholders
- Current state and constraints
- Goals and non-goals
- Success and failure criteria
- Key assumptions
- Candidate approaches and tradeoffs
- Selected direction or decision criteria
- Open questions

The plugin should not generate final planning documents until this context is sufficiently clear.

### Stage 2: Generate Documents

The plugin saves the canonical planning context plus the standard generated document suite to the local workspace.

Saved standard files:

- `planning-context`
- `brief`
- `prd`
- `user-stories`
- `feature-spec`
- `metrics-brief`

Generated planning document types:

- `brief`
- `prd`
- `user-stories`
- `feature-spec`
- `metrics-brief`

The plugin should not expose mode selection in v0.1. `qa-scenario`, `option-memo`, and `stakeholder-brief` remain bundled template resources, but `planning-drafts` does not generate them until the suite contract is expanded.

Saved output path:

```text
docs/planning/drafts/YYYY-MM-DD-HHMMSS-topic-slug/
```

Example:

```text
docs/planning/drafts/2026-04-24-143205-login-onboarding/
├── 00-suite-index.md
├── 00-planning-context.md
├── 01-brief.md
├── 02-prd.md
├── 03-user-stories.md
├── 04-feature-spec.md
└── 05-metrics-brief.md
```

### Stage 3: Review and Improve

The plugin reviews generated drafts with a common rubric and produces targeted improvement requests.

Review outputs:

- Pass, conditional pass, or needs revision
- Missing sections
- Ambiguous requirements
- Unsupported claims
- Unmeasurable success criteria
- Conflicting scope or decisions
- Highest-priority next question
- Suggested rewrite or patch section

If review finds core context gaps, the user should return to `planning-intake` for another focused clarification pass before regenerating or updating the suite.

## Skill Architecture

v0.1 should be skill-first. Commands, hooks, MCP servers, and apps should be omitted unless there is a clear need.

### Required Skills

#### `help`

Purpose:

- Explain what the plugin does and does not do.
- Show Claude Code and Codex invocation forms.
- Offer first-use scenarios.
- Route users to the right workflow.

Claude Code example:

```text
/planning-team-kit:help
```

Codex example:

```text
$help
```

#### `planning-intake`

Purpose:

- Run the front-of-funnel planning brainstorm.
- Turn rough input into structured planning context.
- Ask one high-leverage question at a time.
- Stop before document generation if alignment is insufficient.

Output schema:

```yaml
planning_context:
  topic: string
  one_line_problem: string
  intended_outcome: string
  users_or_stakeholders:
    - string
  current_state: string
  constraints:
    - string
  non_goals:
    - string
  success_criteria:
    - string
  failure_criteria:
    - string
  assumptions:
    - string
  risks:
    - string
  options:
    - name: string
      pros:
        - string
      cons:
        - string
  recommended_direction: string
  approval_state: draft | needs_review | aligned
  open_questions:
    - string
```

#### `planning-drafts`

Purpose:

- Save the canonical planning context.
- Generate and locally save the standard draft planning documents from `planning_context`.
- Maintain traceability across documents.

Responsibilities:

- Always save `planning-context` and generate `brief`, `prd`, `user-stories`, `feature-spec`, and `metrics-brief`.
- Save generated artifacts under `docs/planning/drafts/YYYY-MM-DD-HHMMSS-topic-slug/`.
- Generate drafts with shared metadata.
- Preserve assumptions, decisions, risks, and open questions.
- Mark incomplete sections instead of inventing missing facts.

#### `quality-review`

Purpose:

- Evaluate a document suite through a multi-agent review gate.
- Produce consolidated, actionable improvement guidance.

Required behavior:

- Orchestrate Product Reviewer, User Story Reviewer, Feature Spec Reviewer, Metrics Reviewer, and Handoff Readiness Reviewer perspectives.
- Check structure, clarity, consistency, evidence, and execution readiness.
- Return a small set of prioritized findings.
- Consolidate conflicts by prioritizing higher handoff risk.
- Include evidence or quoted document locations for each finding when possible.
- Mark unsupported claims as assumptions.

## Document Model

All generated documents should include common front matter.

```yaml
---
doc_type: planning-context | brief | option-memo | prd | user-stories | feature-spec | qa-scenario | metrics-brief | stakeholder-brief
title: ""
status: draft | review | approved | archived
owner: ""
audience: ""
last_updated: "YYYY-MM-DD"
version: "0.1"
mode: standard
source_of_truth: ""
related_docs: []
decision_required: true | false
sensitivity: public | internal | restricted | highly-restricted
---
```

Common content sections:

- Summary
- Problem
- Goal
- Non-goals
- Audience
- Decisions
- Requirements or expected behavior
- Risks
- Assumptions
- Evidence and sources
- Open questions
- Next actions

## Document Types

### `planning-context`

Purpose:

- Preserve the canonical planning context in a human-readable Markdown file.

Audience:

- Planning team, product owner, and downstream agents.

Required sections:

- One-line problem
- Intended outcome
- Users or stakeholders
- Goals
- Non-goals
- Success criteria
- Constraints
- Assumptions
- Risks
- Recommended direction
- Open questions
- Readiness status

### `brief`

Purpose:

- Align early planning direction.

Audience:

- Planning team, product leads, decision makers.

Required sections:

- Background
- Problem
- Goal
- Non-goals
- Key constraints
- Assumptions
- Recommended direction
- Open questions
- Next actions

### `option-memo`

Purpose:

- Compare alternatives and document a recommended direction.

Audience:

- Product leads, engineering leads, stakeholders.

Required sections:

- Decision summary
- Comparison criteria
- Alternatives
- Recommendation
- Risks and mitigations
- Reversal conditions
- Decision needed

### `prd`

Purpose:

- Define what should be built and why.

Audience:

- Product, engineering, design, QA.

Required sections:

- Problem definition
- Goals
- Non-goals
- Users and scenarios
- Requirements
- Scope
- Edge cases
- Metrics
- Dependencies
- Open issues

### `qa-scenario`

Purpose:

- Make expected behavior testable.

Audience:

- QA, engineering, product.

Required sections:

- Scenario summary
- Preconditions
- Test data
- Steps
- Expected result
- Negative cases
- Evidence criteria
- Verdict

### `metrics-brief`

Purpose:

- Define success and guardrails.

Audience:

- Product, data, leadership.

Required sections:

- Primary metric
- Guardrail metrics
- Measurement source
- Observation window
- Segment
- Decision rule
- Known limitations

### `user-stories`

Purpose:

- Capture user-centered stories and acceptance criteria outside the PRD.

Audience:

- Product, design, engineering, QA, and stakeholders.

Required sections:

- Summary
- Personas or user types
- Story map
- User stories
- Acceptance criteria
- Negative and edge cases
- Priority and release scope
- Assumptions
- Open questions
- Evidence and sources
- Next actions

### `feature-spec`

Purpose:

- Define feature behavior without forcing implementation choices such as API, data, or query design.

Audience:

- Product, design, engineering, QA, data, and operations.

Required sections:

- Summary
- Source artifacts
- Feature scope
- User flow
- Screen or surface behavior
- State and policy rules
- Permission rules
- Edge cases and error states
- Validation expectations
- Rollout expectations
- Open questions
- Owners and next actions

### `stakeholder-brief`

Purpose:

- Communicate the planning decision to a specific audience.

Audience:

- Leadership, partner teams, operations, go-to-market teams.

Required sections:

- Audience-specific summary
- Why now
- Decision or ask
- Impact
- Risks
- Timeline
- Support needed

## Quality Gates

The quality review should use a hybrid multi-agent checklist and scoring model. A document should not pass only because it has a high total score. It should pass only when required defects are absent and key quality thresholds are met.

### Review Orchestration

When subagents are available, `quality-review` should spawn independent reviewer agents and then consolidate their findings. When subagents are not available, it should run the same roles sequentially and label the result as fallback review.

Reviewer agents:

- Product Reviewer
- User Story Reviewer
- Feature Spec Reviewer
- Metrics Reviewer
- Handoff Readiness Reviewer

Reviewers should not require implementation design details such as API endpoint, DB schema, concrete query, or instrumentation event.

### Common Rubric

Evaluate each document on these axes:

- Problem clarity: can the problem be stated in one clear sentence?
- Audience clarity: is the reader or decision maker explicit?
- Requirement completeness: are required, optional, and out-of-scope items separated?
- Exception and policy coverage: are edge cases and rules covered?
- Metric verifiability: can success be measured?
- Evidence quality: are claims tied to sources, notes, or explicit assumptions?
- Structural consistency: does the document follow the expected section model?
- Execution readiness: can another team act on the document without guessing?

### Gate Levels

#### Gate 0: Scope Fit

Checks:

- Is this a planning artifact?
- Is the document type clear?
- Is the audience clear?
- Is the requested output too broad?

Fail examples:

- The user asks for a full operating platform.
- The document type mixes PRD, roadmap, and release note without separation.

#### Gate 1: Basic Completeness

Checks:

- Required sections exist.
- Problem, goal, non-goal, and audience are present.
- Open questions are separated from decisions.

Fail examples:

- Requirements exist but no problem statement.
- Metrics exist but no decision rule.

#### Gate 2: Consistency and Execution

Checks:

- Requirements match goals.
- Edge cases do not contradict the main policy.
- Metrics reflect the intended outcome.
- Owners and next actions are clear.

Fail examples:

- The PRD says the feature is internal-only, but stakeholder brief claims external launch.
- A QA scenario tests behavior not specified in the PRD.

#### Gate 3: Evidence and Governance

Checks:

- Important claims have sources or assumptions.
- Sensitive content is marked.
- Low-confidence claims do not drive final decisions.
- Human approval is required for final use.

Fail examples:

- A market claim appears with no source.
- A high-risk assumption is presented as a decision.

## Clarification Model

Clarification should be owned by `planning-intake`. `planning-drafts` should stop and route back to `planning-intake` when context is not ready.

Rules:

- Ask one question at a time.
- Prefer 2 to 3 clear choices when possible.
- Do not ask questions that do not change the document.
- Do not repeat questions already answered.
- If information is missing, mark an assumption rather than inventing a fact.
- Show the changed section after applying the answer.

Good clarification prompt:

```text
The PRD has a clear goal, but the success metric is not measurable. Which metric should be primary?

1. Activation rate
2. Completion rate
3. Retention or repeat usage
```

Bad clarification prompt:

```text
Please provide all missing details about users, metrics, risks, edge cases, launch plan, and policy decisions.
```

## Safety and Governance

v0.1 is draft-only.

Rules:

- Do not publish externally.
- Do not write to Jira, Confluence, Slack, Google Drive, or Notion.
- Do not imply approval.
- Do not hide assumptions.
- Do not turn low-confidence claims into decisions.
- Do not include sensitive raw data unless the user explicitly provides and approves its use.

Every generated document should support these fields or sections:

- `source`
- `assumption`
- `confidence`
- `sensitivity`
- `owner`
- `approval_state`

Policy:

- Claims without sources become assumptions.
- Assumptions that affect decisions must be visible.
- Human owner remains accountable for final content.
- External sharing requires explicit human approval.

## Cross-Platform Plugin Structure

The plugin should share skills across Claude Code and Codex while keeping platform manifests separate. Document generation templates are bundled under `planning-drafts` because that skill owns artifact generation.

```text
planning-team-kit/
  .claude-plugin/
    plugin.json
  .codex-plugin/
    plugin.json
  README.md
  skills/
    help/
      SKILL.md
      agents/
        openai.yaml
    planning-intake/
      SKILL.md
      agents/
        openai.yaml
    planning-drafts/
      SKILL.md
      agents/
        openai.yaml
      templates/
        planning-context.md
        brief.md
        option-memo.md
        prd.md
        user-stories.md
        feature-spec.md
        qa-scenario.md
        metrics-brief.md
        stakeholder-brief.md
    quality-review/
      SKILL.md
      agents/
        openai.yaml
  schemas/
    doc-header.schema.json
    section-map.yaml
  snippets/
    decision-table.md
    risk-table.md
    source-assumption-confidence.md
  docs/
    style-guide.md
    quality-rubric.md
    examples.md
  tests/
```

### Manifest Guidance

`.claude-plugin/plugin.json`:

- Include shared metadata.
- Point to `./skills/`.
- Add `commands` only if command files are introduced later.
- Do not include Codex-only interface metadata.

`.codex-plugin/plugin.json`:

- Include the same shared metadata.
- Point to `./skills/`.
- Include `interface` metadata for Codex UI.
- Include default prompts that route users into the 3-stage workflow.

### Invocation Guidance

Claude Code:

```text
/planning-team-kit:planning-intake
/planning-team-kit:planning-drafts
/planning-team-kit:quality-review
```

Codex:

```text
$planning-intake
$planning-drafts
$quality-review
```

Each `SKILL.md` must teach both forms to avoid platform confusion.

## User Onboarding

The first 10 minutes should produce one real artifact.

Recommended `help` flow:

1. Explain the plugin in one sentence.
2. Show three starting scenarios.
3. Offer one copy-paste sample prompt.
4. Explain output quality expectations.
5. Show how to ask for improvement.

Example default prompts:

```text
입력된 메모를 기획 산출물로 정리하되, 목표-문제-대상-결정사항-미결정사항-리스크 순으로 구조화해줘.
```

```text
이 아이디어를 먼저 정의/정렬한 뒤, 필요한 기획 문서 묶음을 추천하고 초안을 만들어줘.
```

```text
이 기획 문서를 품질 기준으로 검토하고, 가장 중요한 보완 질문 하나부터 물어봐줘.
```

## Testing Strategy

Testing should focus on structure, platform compatibility, and document quality invariants.

Automated checks:

- Manifest metadata is synchronized between Claude Code and Codex.
- Codex manifest includes `interface`; Claude manifest does not.
- Required skills exist.
- Each `SKILL.md` includes both Claude Code and Codex invocation guidance.
- Template files exist for required document types.
- Required front matter fields are present in templates.
- Forbidden phrases such as unsupported auto-publish claims do not appear.
- Golden samples preserve expected section structure.
- `planning-drafts` always saves generated standard drafts to the timestamped local workspace path.
- Codex manifest declares `Write` when local draft saving is enabled.

Human or LLM-assisted review:

- Is the output useful to a planning team?
- Are examples realistic?
- Is the workflow too heavy?
- Are assumptions clearly separated?
- Does review feedback reduce ambiguity?

Pilot success metrics:

- First artifact generated within 10 minutes.
- At least 60% of generated drafts are reusable after one revision.
- Users report reduced first-draft effort.
- Review finds fewer missing problem statements, edge cases, and success metrics.
- Users can find and review the saved standard draft suite without choosing a mode.

## Rollout Plan

### v0.1

Focus:

- Core plugin structure.
- Five required skills.
- Doc-suite-owned templates.
- Shared quality rubric.
- Draft-only safety rules.
- Standard-only planning-drafts contract.
- Automatic local draft persistence under `docs/planning/drafts/YYYY-MM-DD-HHMMSS-topic-slug/`.
- README and help experience.
- Basic structure tests.

No external integrations.

### v0.2

Focus:

- Team-specific style presets.
- Deeper document-type guidance.
- Revision comparison.
- Previous draft gap detection.
- More examples and golden samples.

### v0.3

Focus:

- Read-first external integrations.
- Confluence, Jira, Slack, and Drive input gathering.
- Draft-first write targets behind explicit approval.
- Team template library.
- Audit logs for generated artifacts.

## Key Decisions

- The plugin is named `planning-team-kit`.
- v0.1 is draft-only.
- User-facing workflow has three stages, not six.
- `planning-drafts` is standard-only in v0.1.
- `planning-drafts` always saves `00-suite-index.md`, `00-planning-context.md`, `01-brief.md`, `02-prd.md`, `03-user-stories.md`, `04-feature-spec.md`, and `05-metrics-brief.md` to a timestamped local workspace directory.
- Internal pipeline keeps stronger quality logic.
- PRD is one artifact type, not the center of the plugin.
- External integrations are postponed until after v0.1.
- `commands/`, `hooks/`, MCP, and apps are excluded from v0.1 unless a concrete need emerges.

## Open Questions for User Review

- Should the initial templates use Korean-only section names, or bilingual Korean/English names for cross-functional teams?

## References

- Local template reference: `skeleton-plugin`
- Local production plugin reference: `confluence-export-kit`
- Codex plugin reference: https://developers.openai.com/codex/plugins/build
- Codex skills reference: https://developers.openai.com/codex/skills
- Claude Code plugins reference: https://code.claude.com/docs/en/plugins-reference
