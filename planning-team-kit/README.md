# planning-team-kit

`planning-team-kit`은 Claude Code와 Codex 양쪽에서 쓰는 기획 문서 품질 플러그인입니다. v0.2.1은 `draft-only`로 동작하며, `planning-draft` 결과와 `confluence-update-plan` 결과를 로컬 workspace에 저장하지만 외부 시스템에 자동 반영하거나 쓰지 않습니다.

## 목적

이 플러그인은 PRD 하나를 빠르게 만드는 도구가 아니라, 아이디어를 `정리 -> 선택 점검 -> 작성 -> 검토 -> Confluence 반영 계획` 흐름으로 통과시켜 일관된 품질의 기획 산출물을 만들도록 돕습니다.

## 지원 범위

- 사용자 입력 분석과 `.confluence-index` 기반 관련 Confluence 문서 선별을 포함한 `planning-start`
- `planning-draft` 전 선택적으로 계획/결정안을 한 질문씩 점검하는 `planning-check`
- 모드 선택 없는 core standard 문서 묶음 생성 및 로컬 저장: index, planning brief, requirements, behavior spec
- Product Context Reviewer, Story & Testability Reviewer, Feature Behavior & Policy Reviewer, Metrics & Evidence Reviewer, Cross-Artifact Consistency Reviewer, Handoff Governance Reviewer 관점의 multi-agent review gate
- `planning-draft` 실행 전 부족한 맥락을 `planning-start`로 다시 보완하는 readiness 흐름
- 사람이 직접 Confluence에 추가/수정할 내용을 정리하는 `confluence-update-plan`
- Claude Code와 Codex 공통 `skills/` 기반 사용

## 비범위

- Jira, Confluence, Slack, Google Drive, Notion 자동 반영 또는 원격 쓰기
- 최종 의사결정 대행
- 승인 워크플로우 자동화
- 프로젝트 관리 대시보드
- 도메인별 특화 기획 로직

## Start Here

처음 쓰는 경우 `help`로 들어오거나 바로 `planning-start`에서 시작하면 됩니다.

Claude Code:

```text
/planning-team-kit:help
/planning-team-kit:planning-start
```

Codex:

```text
$help
$planning-start
```

## 사용법

Claude Code:

```text
/planning-team-kit:help
/planning-team-kit:planning-start
/planning-team-kit:planning-check
/planning-team-kit:planning-draft
/planning-team-kit:planning-review
/planning-team-kit:confluence-update-plan
```

Codex:

```text
$help
$planning-start
$planning-check
$planning-draft
$planning-review
$confluence-update-plan
```

## 기본 워크플로우

1. `planning-start`로 사용자 입력과 관련 Confluence 근거 문서를 정리합니다.
2. 필요하면 `planning-check`로 계획/결정안을 한 번에 하나의 질문으로 점검합니다.
3. `planning-draft`로 core standard 문서 묶음 초안을 만들고 `planning/drafts/topic-slug--YYYY-MM-DD-HHMMSS/`에 저장합니다.
4. `planning-draft`가 맥락 부족을 발견하면 생성하지 않고 `planning-start`로 돌아가 보완합니다.
5. `planning-review`의 multi-agent review gate로 누락, 모호함, 근거 부족, 핸드오프 리스크를 검토하고 `04-planning-review.md`를 저장합니다.
6. `confluence-update-plan`으로 사람이 직접 Confluence에 추가/수정할 작업을 `99-confluence-update-plan.md`로 정리합니다.

## 안전 원칙

- 모든 산출물은 초안입니다.
- 출처 없는 주장은 가정으로 분리합니다.
- 민감도와 문서 소유자를 명시합니다.
- Confluence 반영 계획은 수동 작업 안내이며 원격 페이지를 변경하지 않습니다.

## 저장 위치

`planning-draft`는 생성된 core standard 문서 묶음을 항상 현재 workspace 아래에 저장합니다.

```text
planning/drafts/login-onboarding--2026-04-24-143205/
├── 00-index.md
├── 01-planning-brief.md
├── 02-requirements.md
└── 03-behavior-spec.md
```

후속 단계는 같은 draft directory에 추가 파일을 저장합니다.

```text
planning/drafts/login-onboarding--2026-04-24-143205/
├── 04-planning-review.md          # planning-review 결과
└── 99-confluence-update-plan.md   # confluence-update-plan 결과
```

동일한 경로가 이미 있으면 덮어쓰지 않고 `-2`, `-3` 같은 숫자 suffix를 붙입니다.

## 포함된 구성

- `.claude-plugin/plugin.json` — Claude Code 플러그인 매니페스트
- `.codex-plugin/plugin.json` — Codex 플러그인 매니페스트
- `skills/` — 기획 워크플로우 스킬
- `skills/planning-draft/templates/` — `planning-draft`가 사용하는 문서 타입별 Markdown 템플릿
- `schemas/` — 문서 헤더와 섹션 맵
- `snippets/` — 재사용 가능한 표와 메타데이터 블록
- `docs/` — 스타일 가이드, 품질 루브릭, 예시
- `tests/` — 구조/호환성 회귀 테스트
