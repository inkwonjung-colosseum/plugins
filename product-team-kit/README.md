# product-team-kit

핵심 모호함을 질문으로 해소하거나 명시해 기획초안을 만들고, 기획 입력을 현재 템플릿에 맞춰 기능설계서와 정책서 초안으로 정리하는 제품팀 도구. Claude Code와 Codex 양쪽에서 동작한다.

## 핵심 원칙

- **Interactive draft first**: `plan-draft`는 기획 인터뷰로 핵심 모호함을 줄이고 `plan-format`에 넘길 기획초안을 만든다
- **Formatter first**: `plan-format`은 입력값을 템플릿에 맞게 구조화한다
- **Project Docs SSOT**: 기존 내용 검증은 `planning/`을 제외한 현재 프로젝트의 Markdown 문서와 그 문서가 참조한 로컬 resource를 기준으로 `plan-review`에서 수행한다
- **읽기**: `plan-draft`는 필요한 로컬 프로젝트 맥락을 최소로 확인할 수 있고, `plan-format`은 사용자가 준 입력값 또는 파일만 읽는다
- **쓰기**: 입력에서 기능명을 추출해 `plan-draft` 기획초안 폴더를 재사용하거나, 그 외 입력은 로컬 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 아래에 초안 저장
- **발행 전 검토**: 외부 공유나 팀 문서 반영 전에는 `plan-review`로 기능설계서와 정책서를 함께 검토한다

## 로컬 초안 템플릿 경계

`planning/` 아래 생성되는 기획초안, 기능설계서, 정책서는 **로컬 초안 템플릿**이다. 이 산출물은 **공식 팀 문서가 아니다**. 팀 문서 필수 섹션과 1:1로 동기화된 원본이 아니라, 사람이 팀 문서에 반영하기 전 검토하는 작업 초안이다.

팀 문서 히스토리는 반영 이후 관리한다. 따라서 이 플러그인은 팀 문서 export snapshot, Project Docs SSOT Markdown, 팀 문서 이력을 자동 수정하지 않는다.

## Project Docs SSOT

Project Docs SSOT는 현재 프로젝트 안의 `*.md`, `*.markdown` 문서와, 그 문서가 상대경로로 명시 참조한 로컬 resource만 포함한다. `planning/` 하위 산출물은 검토 대상일 수 있지만 SSOT 근거로 사용하지 않는다.

SSOT 근거에서 제외하는 항목:

- `planning/`, `.git/`, dependency/vendor/build/cache/generated 경로
- 코드, 테스트, 설정 파일
- 외부 URL
- Markdown에서 참조하지 않은 독립 resource

외부 문서 시스템에서 export된 Markdown이 프로젝트에 있더라도 특별 취급하지 않고 일반 Project Docs Markdown으로만 취급한다.

## 문서 타입

| 타입 | 용도 |
|:-----|:-----|
| 기획초안 | 질문과 로컬 맥락 확인을 통해 `plan-format` 입력으로 정리한 초기 기획 문서 |
| 기능설계서 | HOW·화면·플로우. 기획자가 정하는 기능 동작 명세 |
| 정책서 | 규칙·조건·예외 정의 |

## 공통 계약

`plan-draft`와 `plan-format`의 입력 판정, 저장 규칙, 출력 형식, 미정/가정 marker 규칙, 재실행 제어는 `references/` 아래 공통 계약을 따른다. `plan-format`의 분류 기준, handoff artifact, worker 계약은 `skills/plan-format/references/` 아래 계약을 따른다. `plan-review`의 근거 패키지, 출력 템플릿, 발행 준비 증적, 재검토 입력 계약은 `skills/plan-review/references/` 아래 계약을 따른다.

## Start Here

```
/product-team-kit:plan-draft "주문 취소 기능을 기획하고 싶어"
/product-team-kit:plan-format "주문 취소 기능: 주문 취소 정책과 화면 동작 정리..."
/product-team-kit:plan-format /path/to/planning-notes.md
/product-team-kit:plan-review planning/주문취소--YYYY-MM-DD-HHMMSS/
$plan-draft "반품 접수 기능을 질문하면서 정리해줘"
$plan-format "반품 접수 기능 관련 AI 대화 결과물 또는 비구조 기획 노트"
$plan-review planning/반품접수--YYYY-MM-DD-HHMMSS/
```

`plan-format`에는 기능명을 입력하지 않는다. 스킬이 입력 본문 또는 파일명에서 기능명을 추출한다.

전체 스킬 설명과 각 스킬별 워크플로 다이어그램은 [`docs/skills-workflow.md`](docs/skills-workflow.md)를 참고한다.

## Implicit Invocation 라우팅

자연어 요청으로 스킬을 암묵 호출할 때는 아래 우선순위를 따른다.

| 사용자 의도 | 선택 스킬 | 기준 |
|:--|:--|:--|
| 질문하면서 기획을 잡기, 모호함 해소, 기능 방향 정리, 입력 보완 | `plan-draft` | 기획 판단에 필요한 답변을 더 받아야 함 |
| 기획 노트·회의록·AI 대화 결과를 기능설계서와 정책서로 정리 | `plan-format` | 기능설계서/정책서 초안 생성 또는 저장이 목적 |
| 기존 초안 평가, 발행 전 검토, pass/conditional pass/수정 필요 판단 | `plan-review` | 이미 생성된 기능설계서/정책서 초안 또는 초안 폴더가 대상 |

한 요청에 생성과 검토가 함께 있으면 `plan-format`으로 초안을 만든 뒤 `plan-review`를 다음 단계로 안내한다. 사용자가 명시적으로 “생성 후 바로 검토”를 요청하고 초안 저장이 성공한 경우에만 같은 흐름에서 `plan-review`를 이어서 수행한다.

## 워크플로

```
/product-team-kit:plan-draft "기획 의도, 주제, 파일경로, 또는 로컬 프로젝트 경로"
    ↓ 사용자 답변 수집
    ↓ 중요한 모호함이 남아 있으면 추가 질문하고, 확정 불가 항목은 [미정]/[가정]/[확인 필요]/[충돌 후보]로 분리
    ↓ 필요한 경우 현재 프로젝트의 관련 Markdown 문서와 linked local resource를 최소 확인
    ↓ planning/[안전기능명]--YYYY-MM-DD-HHMMSS/[안전기능명]_기획초안.md 에 기획초안 저장
    ↓
/product-team-kit:plan-format "기획 입력 또는 파일경로"
    ↓ 입력에서 기능명 추출
    ↓ 초안 생성 가능성과 공통 정리 기준 확정
    ↓ 일반 입력이 부족하면 파일을 만들지 않고 저장 보류 후 plan-draft 보완 안내
    ↓ plan-draft 산출 기획초안도 부족하면 사용자 결정 필요로 종료
    ↓ 기능설계서/정책서 본문만 병렬 작성
    ↓ 단일 흐름에서 역할명·범위·미정 항목 최종 조정
    ↓ 입력이 plan-draft 산출 _기획초안.md이면 기획초안 폴더를 재사용하고, 그 외 입력은 planning/[안전기능명]--YYYY-MM-DD-HHMMSS/ 에 초안 2개 저장
    ↓
/product-team-kit:plan-review <초안 폴더 또는 기능설계서/정책서 파일경로>
    ↓ Project Docs SSOT 근거 패키지 생성
    ↓ 근거·결정/범위·실행/검증 가능성 확인
    ↓ 최종 결과는 수정 필요 > conditional pass > pass 순서로 보수적으로 취합
```

`plan-draft`는 사용자가 아직 기획을 정리하는 단계에서 사용한다. 질문 우선순위는 문제/목적, 사용자/범위, 핵심 흐름, 정책/조건, 예외/권한/상태, 확인 기준 순서다. 질문은 최대 3라운드까지만 진행하고, 저장 가능 조건을 충족하면 세부 미확정은 확인 필요 항목으로 남긴다. Codex에서는 Plan mode의 사용자 질문 도구를 우선 사용하되, 질문 도구가 없어도 현재 대화를 이어갈 수 있으면 일반 대화 fallback으로 질문을 진행한다. 비대화형 실행처럼 사용자 답변을 이어받을 수 없는 경우에만 `질문 필요로 저장 보류`를 반환한다. 저장 가능하면 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/[안전기능명]_기획초안.md`에 저장하며 기존 폴더는 덮어쓰지 않는다.

`plan-format`은 단일 패스 변환 스킬이다. 일반 입력이 부족하면 파일을 만들지 않고 저장 보류를 반환하며, 부족 항목을 `plan-draft`로 보완하도록 안내한다. 자동 보완 왕복은 1회까지만 허용한다. 입력이 `plan-draft` 산출 `_기획초안.md`인데도 부족하면 다시 `plan-draft`로 보내지 않고 `사용자 결정 필요`로 종료한다. 입력이 `plan-draft` 산출 `_기획초안.md`이면 기획초안 폴더를 재사용해 기능설계서와 정책서를 같은 폴더에 저장한다. 직접 입력, 일반 파일 입력, AI 대화 결과물, 문서 스크랩 같은 일반 입력은 새 timestamp 폴더에 저장한다. 생성된 초안은 review target이지 Project Docs SSOT 근거가 아니다.

`plan-review`는 먼저 관련 Project Docs Markdown과 linked local resource를 읽어 근거 패키지를 만든다. 폴더에 `_기획초안.md`가 함께 있어도 검토 대상은 기존처럼 `_기능설계서.md`와 `_정책서.md` 쌍이다. `planning/` 하위 파일은 검토 대상으로 읽을 수 있지만 SSOT 근거로 사용하지 않는다. `plan-review` 결과가 `수정 필요`이면 수정 작업 블록을 출력하며, 초안을 수정한 뒤 같은 초안 폴더를 다시 검토한다. `pass` 또는 `conditional pass`이면 발행 준비 증적 `publish_readiness`를 출력한다. 이 증적은 외부 게시가 아니라 사람이 팀의 외부 반영 또는 공유 절차로 넘기기 전 확인할 체크리스트다.

플러그인 내부 생성·검토 흐름은 루트의 [`docs/diagrams/product-team-kit-workflow.html`](../docs/diagrams/product-team-kit-workflow.html)에서 확인한다. 상세 분석 흐름은 [`docs/diagrams/product-team-kit-workflow-analysis.html`](../docs/diagrams/product-team-kit-workflow-analysis.html)을 참고한다. 두 다이어그램은 [`docs/diagrams/product-team-kit-workflow.source.json`](../docs/diagrams/product-team-kit-workflow.source.json)을 단일 source로 사용해 생성되며, `format-after-draft-insufficient`, `review_repair`, `publish_readiness`, `planning/` SSOT 근거 제외 경계를 같은 정의에서 공유한다.

## 스킬

Claude Code:

```
/product-team-kit:plan-draft
/product-team-kit:plan-format
/product-team-kit:plan-review
```

Codex:

```
$plan-draft
$plan-format
$plan-review
```

## 포함 구성

- `.claude-plugin/plugin.json` — Claude Code 플러그인 매니페스트
- `.codex-plugin/plugin.json` — Codex 플러그인 매니페스트
- `skills/plan-draft/` — 대화형 질문 → `plan-format` 입력용 기획초안 생성
- `skills/*/agents/` — OpenAI/Codex agent metadata와 implicit invocation routing hint
- `skills/plan-format/` — 기획 입력 → 기능설계서·정책서 동시 생성
- `skills/plan-format/templates/` — 기능설계서·정책서 템플릿
- `skills/plan-format/references/` — `plan-format` 분류 기준, handoff artifact, worker 계약
- `skills/plan-review/` — Project Docs SSOT 근거 패키지 기반 발행 전 초안 품질 검토
- `skills/plan-review/references/` — review gate, evidence package, output template, publish readiness, rerun contract, portable reviewer prompt 기준
- `references/` — 입력 dispatch, 저장 atomicity, 출력 형식, marker, 재실행 제어 공통 계약
- `schemas/doc-types.yaml` — 기획초안·기능설계서·정책서 타입 정의
- `docs/` — 스킬 워크플로 설명, 예시, 품질 기준, 안전/정책 문서
- `tests/` — 로컬 초안 경계와 `plan-draft` fallback 계약 테스트
