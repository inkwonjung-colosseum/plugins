# planning-team-kit Examples

## First Run Prompt

```text
이 회의 메모를 기반으로 먼저 문제, 대상, 목표, 비목표, 성공 기준을 정리하고 필요한 기획 문서 묶음을 추천해줘.
```

## Improvement Prompt

```text
이 PRD 초안에서 개발자가 해석해야 하는 모호한 요구사항과 빠진 엣지 케이스를 찾아줘.
```

## Grill Prompt

```text
이 planning context를 문서화하기 전에 가장 위험한 결정부터 하나씩 질문하면서 검증해줘.
```

## Handoff Prompt

```text
검토된 기획 산출물을 바탕으로 결정사항, 미결정사항, 리스크, 다음 액션, 소유자를 정리해줘.
```

## Saved Planning Drafts

`planning-drafts` always saves the generated core standard draft suite under a timestamped local workspace path.

```text
docs/planning/drafts/login-onboarding--2026-04-24-143205/
├── 00-index.md
├── 01-planning-brief.md
├── 02-requirements.md
└── 03-behavior-spec.md
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

If the plan is still too soft before draft generation, run `planning-grill` and answer one decision question at a time.

Claude Code:

```text
/planning-team-kit:planning-grill <planning-context>
```

Codex:

```text
$planning-grill <planning-context>
```
