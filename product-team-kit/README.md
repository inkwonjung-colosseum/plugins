# product-team-kit

기획 입력을 현재 템플릿에 맞춰 기능설계서와 정책서 초안으로 정리하고, 외부 공유나 팀 문서 반영 전에 Product Docs SSOT 근거 기반으로 검토하는 제품팀 도구. Claude Code와 Codex 양쪽에서 동작한다.

## 핵심 원칙

- **Gate First**: `plan-format`은 변환 가능성을 먼저 판정하고, 통과 전에는 파일 생성 금지다.
- **Formatter first**: `plan-format`은 통과한 입력값을 템플릿에 맞게 구조화한다.
- **No interview loop**: `plan-format`은 질문하지 않는다. 입력이 부족하면 파일을 만들지 않고 부족 항목만 출력한다.
- **Product Docs SSOT**: 기존 내용 검증은 `planning/`을 제외한 현재 프로젝트의 제품 정책, PRD/요구사항, 기능/화면 설계, 운영/QA 판단 Markdown과 그 문서가 참조한 로컬 resource를 기준으로 `plan-review`에서 수행한다.
- **읽기**: `plan-format`은 사용자가 준 입력값, 파일, 또는 기획자료 폴더를 읽는다.
- **쓰기**: 입력에서 기능명을 추출해 로컬 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 아래에 기능설계서와 정책서 초안을 저장한다.
- **발행 전 검토**: 외부 공유나 팀 문서 반영 전에는 `plan-review`로 기능설계서와 정책서를 함께 검토한다.

## 로컬 초안 템플릿 경계

`planning/` 아래 생성되는 기능설계서와 정책서는 **로컬 초안 템플릿**이다. 이 산출물은 **공식 팀 문서가 아니다**. 팀 문서 필수 섹션과 1:1로 동기화된 원본이 아니라, 사람이 팀 문서에 반영하기 전 검토하는 작업 초안이다.

팀 문서 히스토리는 반영 이후 관리한다. 따라서 이 플러그인은 팀 문서 export snapshot, Product Docs SSOT Markdown, 팀 문서 이력을 자동 수정하지 않는다.

## Product Docs SSOT

Product Docs SSOT는 현재 프로젝트 안의 제품 정책, PRD/요구사항, 기능/화면 설계, 운영/QA 판단 `*.md`, `*.markdown` 문서와, 그 문서가 상대경로로 명시 참조한 로컬 resource만 포함한다. `planning/` 하위 산출물은 검토 대상일 수 있지만 SSOT 근거로 사용하지 않는다.

SSOT 근거에서 제외하는 항목:

- `planning/`, `.git/`, dependency/vendor/build/cache/generated 경로
- 코드, 테스트, 설정 파일
- 외부 URL
- Markdown에서 참조하지 않은 독립 resource

외부 문서 시스템에서 export된 Markdown이 프로젝트에 있더라도 특별 취급하지 않고 일반 Product Docs 후보로만 취급한다.

## 문서 타입

| 타입 | 용도 |
|:-----|:-----|
| 기능설계서 | HOW·화면·플로우. 기획자가 정하는 기능 동작 명세 |
| 정책서 | 규칙·조건·예외 정의 |

## 스킬별 계약

`plan-format`의 입력 판정, 저장 규칙, 출력, 미정/가정 marker 규칙, 분류 기준, handoff artifact, worker 계약은 `skills/plan-format/references/` 아래 계약을 따른다. `plan-review`의 근거 패키지, 출력 템플릿, 발행 준비 상세, 재검토용 상세 정보 계약은 `skills/plan-review/references/` 아래 계약을 따른다.

## Start Here

```text
/product-team-kit:plan-format "주문 취소 기능: 주문 취소 정책과 화면 동작 정리..."
/product-team-kit:plan-format /path/to/planning-notes.md
/product-team-kit:plan-format /path/to/planning-folder/
/product-team-kit:plan-review planning/주문취소--YYYY-MM-DD-HHMMSS/
$plan-format "반품 접수 기능 관련 AI 대화 결과물 또는 비구조 기획 노트"
$plan-review planning/반품접수--YYYY-MM-DD-HHMMSS/
```

`plan-format`에는 기능명을 별도 인자로 입력하지 않는다. 스킬이 입력 본문, 파일명, 디렉터리명에서 기능명을 추출한다.

전체 스킬 설명과 각 스킬별 워크플로 다이어그램은 [`docs/skills-workflow.md`](docs/skills-workflow.md)를 참고한다.

## Implicit Invocation 라우팅

자연어 요청으로 스킬을 암묵 호출할 때는 아래 우선순위를 따른다.

| 사용자 의도 | 선택 스킬 | 기준 |
|:--|:--|:--|
| 기획 노트·회의록·AI 대화 결과·기획자료 디렉터리를 기능설계서와 정책서로 정리 | `plan-format` | 기능설계서/정책서 초안 생성 또는 저장이 목적 |
| 기존 초안 평가, 발행 전 검토, 통과/조건부 통과/수정 필요 판단 | `plan-review` | 이미 생성된 기능설계서/정책서 초안 또는 초안 폴더가 대상 |

한 요청에 생성과 검토가 함께 있으면 `plan-format`으로 초안을 만든 뒤 `plan-review`를 다음 단계로 안내한다. 사용자가 명시적으로 “생성 후 바로 검토”를 요청하고 초안 저장이 성공한 경우에만 같은 흐름에서 `plan-review`를 이어서 수행한다.

## 워크플로

```text
/product-team-kit:plan-format "기획 입력 또는 파일/디렉터리 경로"
    ↓ 입력에서 기능명 추출
    ↓ 입력 dispatch 계약으로 파일/디렉터리 입력을 읽고 제외 항목을 기록
    ↓ 존재하지 않는 path-like 입력이면 입력 문자열 자체를 기획 입력으로 처리
    ↓ Gate First로 변환 가능성 판정
    ↓ 입력이 부족하면 파일을 만들지 않고 부족 항목만 출력
    ↓ 기능설계서/정책서 본문만 병렬 작성
    ↓ 단일 흐름에서 역할명·범위·미정 항목 최종 조정
    ↓ storage 계약으로 planning/[안전기능명]--YYYY-MM-DD-HHMMSS/ 에 초안 2개 저장
    ↓
/product-team-kit:plan-review <초안 폴더 또는 기능설계서/정책서 파일경로>
    ↓ Product Docs SSOT 근거 패키지 생성
    ↓ Product Docs SSOT 충돌·착수 가능성 확인
    ↓ 기획팀용 리포트로 판정·먼저 할 일·역할별 착수 가능성 출력
    ↓ 최종 결과는 수정 필요 > 조건부 통과 > 통과 순서로 보수적으로 취합
```

`plan-format`은 단일 패스 변환 스킬이다. 입력이 부족하면 질문 루프를 만들지 않고 저장 보류를 반환한다. 이때 출력에는 부족 항목만 포함하고 보강용 입력 템플릿은 만들지 않는다. 디렉터리 입력은 기본 제외 경로와 파일 100개, 파일당 512KB, 총 2MB 상한을 적용해 읽는다. 기존 기능설계서/정책서도 참고 입력으로 포함할 수 있지만, 저장은 새 timestamp 폴더에만 수행한다. 읽을 수 없는 파일과 상한 초과 파일은 출력의 `[입력 제외 항목]`에 남긴다. 생성된 초안은 review target이지 Product Docs SSOT 근거가 아니다. `plan-format`은 Product Docs SSOT를 검색하거나 검증하지 않는다. Python, Node.js, 별도 CLI helper 설치는 전제하지 않는다.

`plan-review`는 먼저 관련 Product Docs Markdown과 linked local resource를 읽어 근거 패키지를 만든다. `planning/` 하위 파일은 검토 대상으로 읽을 수 있지만 SSOT 근거로 사용하지 않는다. 출력 상단에는 기획팀이 바로 볼 수 있도록 판정, 한 줄 결론, 먼저 할 일, 역할별 착수 가능성, 기준 문서 충돌을 보여준다. 결과가 `수정 필요`이면 하단에 재검토용 상세 정보를 출력하며, 초안을 수정한 뒤 같은 초안 폴더를 다시 검토한다. `통과` 또는 `조건부 통과`이면 role별 `downstream_readiness`를 포함한 발행 준비 상세 `publish_readiness`를 출력한다. 이 상세 정보는 외부 게시가 아니라 사람이 팀의 외부 반영 또는 공유 절차로 넘기기 전 확인할 체크리스트다. 기능/화면설계서 또는 정책서가 아닌 입력은 검토 결과가 아니라 `올바른 검토 대상이 아님` 안내로 종료한다.

플러그인 내부 생성·검토 흐름은 루트의 [`docs/diagrams/product-team-kit-workflow.html`](../docs/diagrams/product-team-kit-workflow.html)에서 확인한다. 상세 분석 흐름은 [`docs/diagrams/product-team-kit-workflow-analysis.html`](../docs/diagrams/product-team-kit-workflow-analysis.html)을 참고한다. 두 다이어그램은 [`docs/diagrams/product-team-kit-workflow.source.json`](../docs/diagrams/product-team-kit-workflow.source.json)을 단일 source로 사용해 생성된다.

## 스킬

Claude Code:

```text
/product-team-kit:plan-format
/product-team-kit:plan-review
```

Codex:

```text
$plan-format
$plan-review
```

## 포함 구성

- `.claude-plugin/plugin.json` — Claude Code 플러그인 매니페스트
- `.codex-plugin/plugin.json` — Codex 플러그인 매니페스트
- `skills/*/agents/` — OpenAI/Codex agent metadata와 implicit invocation routing hint
- `skills/plan-format/` — 기획 입력 → 기능설계서·정책서 동시 생성
- `skills/plan-format/templates/` — 기능설계서·정책서 템플릿
- `skills/plan-format/references/` — `plan-format` 입력 dispatch, 저장 atomicity, 출력, marker, 분류 기준, handoff artifact, worker 계약
- `skills/plan-review/` — Product Docs SSOT 근거 패키지 기반 발행 전 초안 품질 검토
- `skills/plan-review/references/` — review gate, evidence package, output template, publish readiness, rerun contract, portable reviewer prompt 기준
- `docs/` — 스킬 워크플로 설명, 안전/정책 문서
