# Self-Review Rules

Use after draft generation unless `--no-self-review`.

Self-review is a feedback gate, not an auto-rewrite pass. Mechanical fixes may be applied. Meaning changes require user approval and go to `## 체크해야 할 항목`.

## Passes

F1 section completeness:

- Each policy section 1-10 has content.
- Each feature section 1-8 has content.
- Auxiliary tables/cards have data.
- `[TBD]` ratio is not dominant.

F2 layer bleed:

- Policy core rules avoid UI words such as button, click, input form, banner.
- Feature behavior avoids acting as the policy source for allowed/forbidden/approval rules.

F3 term consistency:

- One label per role, state, permission, and domain stem inside each layer.
- Feature UI label may pair Korean label with system term in parentheses.

F4 policy-feature mapping:

- Policy rules/states/permissions map to feature actions, exceptions, or access sections.
- Forbidden policy actions do not appear as normal feature flow.

F5 missing source facts:

- Explicit roles, states, feature names, thresholds, and authority facts appear in documents or exclusions.
- Fetch failures, scope exclusions, and source-definition gaps are cross-referenced.

F6 Markdown syntax:

- Fence pairs balanced.
- Header levels sane.
- No legacy auxiliary-table backlink suffix.
- No reserved wrapper headings inside generated bodies.
- No wide default feedback table.

## Classification

- Mechanical stabilization: may update body.
- Display-only transformation: may update screen rendering.
- Suggested fix: checklist first, body unchanged.
- User/external decision: checklist first, body unchanged.

When there are no findings, keep `## 체크해야 할 항목` and write `없음`.
