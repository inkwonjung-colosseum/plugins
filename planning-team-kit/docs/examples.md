# planning-team-kit Examples

## First Run Prompt

```text
이 회의 메모를 기반으로 먼저 문제, 대상, 목표, 비목표, 성공 기준을 정리하고 필요한 기획 문서 묶음을 추천해줘.
```

## Improvement Prompt

```text
이 PRD 초안에서 개발자가 해석해야 하는 모호한 요구사항과 빠진 엣지 케이스를 찾아줘.
```

## Handoff Prompt

```text
검토된 기획 산출물을 바탕으로 결정사항, 미결정사항, 리스크, 다음 액션, 소유자를 정리해줘.
```

## Saved Planning Drafts

`planning-drafts` always saves the generated standard draft suite under a timestamped local workspace path.

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

## Weak Output Recovery

If the output is too generic, run `quality-review` and ask for the highest-impact question first.

Claude Code:

```text
/planning-team-kit:quality-review <draft>
```

Codex:

```text
$quality-review <draft>
```
