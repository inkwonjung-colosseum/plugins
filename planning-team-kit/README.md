# planning-team-kit

`planning-team-kit`은 Claude Code와 Codex 양쪽에서 쓰는 기획 문서 품질 플러그인입니다. v0.1은 `draft-only`로 동작하며, `planning-drafts` 결과를 로컬 workspace에 저장하지만 외부 시스템에 자동 게시하거나 쓰지 않습니다.

## 목적

이 플러그인은 PRD 하나를 빠르게 만드는 도구가 아니라, 아이디어를 `정의/정렬 -> 문서 생성 -> 검수/개선` 흐름으로 통과시켜 일관된 품질의 기획 산출물을 만들도록 돕습니다.

## 지원 범위

- 구조화된 brainstorming과 planning intake
- 모드 선택 없는 standard 문서 묶음 생성 및 로컬 저장: planning context, 기획 브리프, PRD, user stories, feature spec, 지표 브리프
- Product Context Reviewer, Story & Testability Reviewer, Feature Behavior & Policy Reviewer, Metrics & Evidence Reviewer, Cross-Artifact Consistency Reviewer, Handoff Governance Reviewer 관점의 multi-agent review gate
- `planning-drafts` 실행 전 부족한 맥락을 `planning-intake`로 다시 보완하는 readiness 흐름
- Claude Code와 Codex 공통 `skills/` 기반 사용

## 비범위

- Jira, Confluence, Slack, Google Drive, Notion 자동 쓰기
- 최종 의사결정 대행
- 승인 워크플로우 자동화
- 프로젝트 관리 대시보드
- 도메인별 특화 기획 로직

## Start Here

처음 쓰는 경우 `help`로 들어오거나 바로 `planning-intake`에서 시작하면 됩니다.

Claude Code:

```text
/planning-team-kit:help
/planning-team-kit:planning-intake
```

Codex:

```text
$help
$planning-intake
```

## 사용법

Claude Code:

```text
/planning-team-kit:help
/planning-team-kit:planning-intake
/planning-team-kit:planning-drafts
/planning-team-kit:quality-review
```

Codex:

```text
$help
$planning-intake
$planning-drafts
$quality-review
```

## 기본 워크플로우

1. `planning-intake`로 아이디어의 문제, 대상, 목표, 비목표, 성공 기준, 제약을 정리합니다.
2. `planning-drafts`로 standard 문서 묶음 초안을 만들고 `docs/planning/drafts/YYYY-MM-DD-HHMMSS-topic-slug/`에 저장합니다.
3. `planning-drafts`가 맥락 부족을 발견하면 생성하지 않고 `planning-intake`로 돌아가 보완합니다.
4. `quality-review`의 multi-agent review gate로 누락, 모호함, 근거 부족, 핸드오프 리스크를 검토합니다.

## 안전 원칙

- 모든 산출물은 초안입니다.
- 출처 없는 주장은 가정으로 분리합니다.
- 민감도와 문서 소유자를 명시합니다.
- 사람이 최종 승인하기 전에는 외부 시스템에 쓰지 않습니다.

## 저장 위치

`planning-drafts`는 생성된 standard 문서 묶음을 항상 현재 workspace 아래에 저장합니다.

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

동일한 경로가 이미 있으면 덮어쓰지 않고 `-2`, `-3` 같은 숫자 suffix를 붙입니다.

## 포함된 구성

- `.claude-plugin/plugin.json` — Claude Code 플러그인 매니페스트
- `.codex-plugin/plugin.json` — Codex 플러그인 매니페스트
- `skills/` — 기획 워크플로우 스킬
- `skills/planning-drafts/templates/` — `planning-drafts`가 사용하는 문서 타입별 Markdown 템플릿
- `schemas/` — 문서 헤더와 섹션 맵
- `snippets/` — 재사용 가능한 표와 메타데이터 블록
- `docs/` — 스타일 가이드, 품질 루브릭, 예시
- `tests/` — 구조/호환성 회귀 테스트
