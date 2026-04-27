# planning-team-kit

로컬 Confluence 문서를 읽고 기획 초안을 만들어 Confluence에 직접 반영하는 기획팀 도구. Claude Code와 Codex 양쪽에서 동작한다.

## 핵심 원칙

- **Confluence = SSOT**: 기존 내용이 항상 우선이다
- **읽기**: 로컬 export 파일 사용 (빠르고 토큰 절약)
- **쓰기**: MCP로 Confluence 직접 반영 (확인받은 것만)
- **검토 게이트**: `[미정]`, `[가정]`, 기존 문서와의 충돌 경고가 남아 있으면 `plan-review` 확인 없이 publish하지 않는다

## 문서 타입

| 타입 | 용도 |
|:-----|:-----|
| 상위설계서 | WHY·방향·범위. 개발 시작 전 방향 정렬 |
| 기능설계서 | HOW·화면·플로우. 개발팀 구현 명세 |
| 정책서 | 규칙·조건·예외 정의 |

## Start Here

```
/planning-team-kit:plan-draft 주문 취소 정책 만들어줘
/planning-team-kit:plan-draft 입고 기능 설계서 업데이트해야 해
/planning-team-kit:plan-draft 새 기능 방향 잡아야 해
```

## 워크플로

```
/planning-team-kit:plan-draft "기획 의도"
    ↓ 로컬 Confluence 문서 읽기
    ↓ 질문 루프 (구체화 완료까지)
    ↓ 초안 생성
    ↓
(선택) /planning-team-kit:plan-review
    ↓ 3관점 검토 (근거·범위·실행)
    ↓
/planning-team-kit:plan-publish
    ↓ [미정]·[가정]·충돌 경고 review gate 확인
    ↓ 최종 확인
    ↓ MCP로 Confluence 반영
    ↓ 로컬 export 재최신화 안내
```

`plan-review`는 일반적으로 선택 단계다. 단, 초안에 `[미정]`, `[가정]`, "충돌" 경고가 남아 있으면 `plan-publish`가 review 결과 또는 명시적 사용자 확인을 먼저 요구한다.

## 스킬

Claude Code:

```
/planning-team-kit:plan-draft
/planning-team-kit:plan-review
/planning-team-kit:plan-publish
```

Codex:

```
$plan-draft
$plan-review
$plan-publish
```

## 포함 구성

- `.claude-plugin/plugin.json` — Claude Code 플러그인 매니페스트
- `.codex-plugin/plugin.json` — Codex 플러그인 매니페스트
- `skills/plan-draft/` — 기획 의도 입력 → 초안 생성
- `skills/plan-draft/templates/` — 상위설계서·기능설계서·정책서 템플릿
- `skills/plan-review/` — 초안 품질 검토
- `skills/plan-publish/` — Confluence 반영
- `schemas/doc-types.yaml` — 문서 타입 정의
- `docs/` — 예시, 품질 기준, 안전/정책 문서
- `tests/` — 구조 회귀 테스트
