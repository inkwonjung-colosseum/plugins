# product-team-kit

기획 입력을 현재 템플릿에 맞춰 기능설계서와 정책서 초안으로 정리하는 제품팀 도구. Claude Code와 Codex 양쪽에서 동작한다.

## 핵심 원칙

- **Formatter first**: `plan-format`은 입력값을 템플릿에 맞게 구조화한다
- **Confluence = SSOT**: 기존 내용 검증은 `plan-review`에서 수행한다
- **읽기**: `plan-format`은 사용자가 준 입력값 또는 파일만 읽는다
- **쓰기**: 입력에서 기능명을 추출해 로컬 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 아래에 초안 저장
- **발행 전 검토**: Confluence 반영이나 외부 공유 전에는 `plan-review`로 기능설계서와 정책서를 함께 검토한다

## 문서 타입

| 타입 | 용도 |
|:-----|:-----|
| 기능설계서 | HOW·화면·플로우. 기획자가 정하는 기능 동작 명세 |
| 정책서 | 규칙·조건·예외 정의 |

## Start Here

```
/product-team-kit:plan-format "주문 취소 기능: 주문 취소 정책과 화면 동작 정리..."
/product-team-kit:plan-format /path/to/planning-notes.md
$plan-format "반품 접수 기능 관련 AI 대화 결과물 또는 비구조 기획 노트"
```

`plan-format`에는 기능명을 입력하지 않는다. 스킬이 입력 본문 또는 파일명에서 기능명을 추출한다.

## 워크플로

```
/product-team-kit:plan-format "기획 입력 또는 파일경로"
    ↓ 입력에서 기능명 추출
    ↓ 초안 생성 가능성과 공통 정리 기준 확정
    ↓ 기능설계서/정책서 본문만 병렬 작성
    ↓ 단일 흐름에서 역할명·범위·미정 항목 최종 조정
    ↓ planning/[안전기능명]--YYYY-MM-DD-HHMMSS/ 에 초안 2개 저장
    ↓
/product-team-kit:plan-review <초안 폴더 또는 기능설계서/정책서 파일경로>
    ↓ 새 검토 관점 3개로 근거·결정/범위·실행/검증 가능성 확인
    ↓ 최종 결과는 수정 필요 > conditional pass > pass 순서로 보수적으로 취합
```

`plan-format`은 질문 루프 없이 단일 패스로 변환한다. 입력 해석과 공통 기준 확정은 순차로 처리하고, 기능설계서/정책서 본문 작성만 병렬화한다. 확인되지 않은 내용은 `[미정]`, `[가정]`, 확인 필요 질문으로 남긴다. Confluence 근거 검증과 발행 전 결정·실행 가능성 판단은 `plan-review`로 확인한다. `plan-review`는 템플릿 구조 검증 도구가 아니다.

## 스킬

Claude Code:

```
/product-team-kit:plan-format
/product-team-kit:plan-review
```

Codex:

```
$plan-format
$plan-review
```

## 포함 구성

- `.claude-plugin/plugin.json` — Claude Code 플러그인 매니페스트
- `.codex-plugin/plugin.json` — Codex 플러그인 매니페스트
- `skills/plan-format/` — 기획 입력 → 기능설계서·정책서 동시 생성
- `skills/plan-format/templates/` — 기능설계서·정책서 템플릿
- `skills/plan-review/` — 3개 검토 관점 기반 초안 품질 검토
- `schemas/doc-types.yaml` — 문서 타입 정의
- `docs/` — 예시, 품질 기준, 안전/정책 문서
- `tests/` — 구조 회귀 테스트
