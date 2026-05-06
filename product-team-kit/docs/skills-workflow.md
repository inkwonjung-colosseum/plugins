# product-team-kit 스킬 워크플로

`product-team-kit`은 기획 입력을 로컬 초안 두 문서로 정리하고(`plan-format`), 외부 반영 전에 검토하는(`plan-review`) 2단계 제품팀 워크플로다.

이 문서는 README의 빠른 시작보다 한 단계 자세히, 어떤 스킬을 언제 선택하고 어떤 산출물로 이어지는지 설명한다.

## 전체 스킬 맵

| 스킬 | 역할 | 주요 입력 | 주요 산출물 | 다음 단계 |
|---|---|---|---|---|
| `plan-format` | 충분한 기획 입력을 기능설계서와 정책서 로컬 초안으로 나눈다 | 기획 노트, 회의록, AI 대화 결과물, 문서 스크랩, 파일 경로, 디렉터리 경로 | `[안전기능명]_기능설계서.md`, `[안전기능명]_정책서.md` | `plan-review` |
| `plan-review` | 기능설계서/정책서 초안을 발행 전 gate로 검토한다 | 초안 폴더 또는 기능설계서/정책서 파일 | `통과`, `조건부 통과`, `수정 필요` 판단과 기획팀용 리포트 | 사람의 반영 또는 초안 수정 |

## 호출 방식

| 환경 | plan-format | plan-review |
|---|---|---|
| Claude Code | `/product-team-kit:plan-format` | `/product-team-kit:plan-review` |
| Codex | `$plan-format` | `$plan-review` |

## 전체 흐름

```mermaid
flowchart TD
    A[기획 노트, 회의록, 파일, 디렉터리] --> B[plan-format]
    B --> C{기능설계서/정책서 생성 가능?}
    C -- 정보 부족 --> D[저장 보류: 부족 항목만 출력]
    C -- 디자인/개발 상세만 많음 --> E[저장 보류: 제품·업무 판단 정보 부족 항목 출력]
    C -- 가능 --> F[기능설계서와 정책서 저장]
    F --> G[plan-review]
    G --> H{발행 전 gate 결과}
    H -- 통과 --> I[발행 준비 상세 출력]
    H -- 조건부 통과 --> J[확인 항목과 발행 준비 상세 출력]
    H -- 수정 필요 --> K[먼저 고칠 항목과 재검토용 상세 정보 출력]
    K --> L[사람 또는 후속 작업이 초안 수정]
    L --> G
```

## Skill 1. plan-format

### 설명

`plan-format`은 기획 입력을 기능설계서와 정책서 초안으로 정리하는 formatting 스킬이다. 입력이 충분한지 먼저 판단하고, 충분하면 두 문서를 하나의 저장 단위로 생성한다.

입력이 부족하면 질문하지 않고 저장 보류를 반환한다. 보류 출력에는 부족 항목만 포함하고 보강용 입력 템플릿은 만들지 않는다.

Product Docs SSOT 근거 검증은 하지 않는다. 검증은 `plan-review` 책임이다.

### 선택 기준

`plan-format`을 선택한다:

- 기획 노트, 회의록, AI 대화 결과물, 초안 문서 스크랩, 기획자료 디렉터리를 기능설계서와 정책서로 정리해야 한다.
- 기획 입력을 기능설계서와 정책서 로컬 초안으로 생성하려는 의도가 있다. 저장 가능 여부는 Gate First가 판정한다.
- 저장 보류가 나온 뒤 부족 항목을 보강해 다시 문서 생성을 시도한다.

`plan-format`을 선택하지 않는다:

- 이미 생성된 기능설계서/정책서 초안을 검토해야 하는 경우: `plan-review`
- 단순 질의응답, 아이디어 탐색, 문서 생성 없는 일반 상담이 목적인 경우: 일반 답변

### Workflow

```mermaid
flowchart TD
    A[기획 입력 또는 파일/디렉터리 경로] --> B[입력 확인과 디스패치]
    B --> B1[없는 path-like 입력은 직접 텍스트로 처리]
    B --> B2[디렉터리는 읽을 수 있는 텍스트 파일을 상대경로 오름차순으로 통합]
    B1 --> C[기능명과 안전기능명 추출]
    B2 --> C
    C --> D{초안 생성 가능 조건 충족?}
    D -- 정보 부족 --> E[저장 보류: 부족 항목만 출력]
    D -- 디자인/개발 상세만 많음 --> F[저장 보류: 제품·업무 판단 정보 부족 항목 출력]
    D -- 충족 --> H[공통 정리 기준 확정]
    H --> I{분리 컨텍스트 사용 가능?}
    I -- 예 --> J[기능설계서 worker]
    I -- 예 --> K[정책서 worker]
    I -- 아니오 --> L[동일 세션에서 기능설계서 후 정책서 순차 작성]
    J --> M[최종 조정]
    K --> M
    L --> M
    M --> N{two-file 저장 성공?}
    N -- 예 --> O[기능설계서와 정책서 저장 완료]
    N -- 아니오 --> P[저장 실패와 precheck/partial artifact 안내]
    O --> Q[다음 단계 안내: plan-review]
```

### 생성 가능 조건

각 항목을 1개 이상 충족해야 한다:

- 기능 목적 또는 기능명: 기능명, 문제, 목적 중 한 문장 요약 가능
- 적용 대상 또는 업무 범위: 사용자, 역할, 조직, 업무 대상, 포함 범위 중 확인 가능
- 핵심 사용자 행동과 기대 결과: 행동 1개와 결과 1개
- 주요 조건/정책/제약: 허용, 금지, 조건, 예외, 제한, 판단 기준 중 확인 가능

기능설계서와 정책서 중 한쪽에 실질 내용이 거의 없으면 저장 보류한다. 디렉터리 입력은 입력 dispatch 계약에 따라 기본 제외 경로와 파일 100개, 파일당 512KB, 총 2MB 상한을 적용해 통합한다. 읽을 수 없는 파일과 상한 초과 파일은 저장 보류 사유가 아니라 출력의 `[입력 제외 항목]`에 남긴다. Python, Node.js, 별도 CLI helper 설치는 전제하지 않는다.

### 산출물

일반 입력, 존재하지 않는 path-like 입력, 파일 입력, 디렉터리 입력은 새 timestamp 폴더에 저장한다:

```text
planning/[안전기능명]--YYYY-MM-DD-HHMMSS/[안전기능명]_기능설계서.md
planning/[안전기능명]--YYYY-MM-DD-HHMMSS/[안전기능명]_정책서.md
```

## Skill 2. plan-review

### 설명

`plan-review`는 `plan-format`으로 저장한 기능설계서/정책서 초안을 외부 반영 전에 검토하는 gate다. 템플릿 모양만 보는 검사가 아니라, Product Docs SSOT 충돌 여부와 디자인·개발·QA·운영 착수 가능성을 확인한다.

검토 대상은 `planning/` 아래 초안일 수 있지만, `planning/` 파일은 SSOT 근거로 사용하지 않는다.

### 선택 기준

`plan-review`를 선택한다:

- 기존 초안 폴더나 기능설계서/정책서 파일을 검토해야 한다.
- 외부 공유 또는 팀 문서 반영 전에 통과 여부를 판단해야 한다.
- Product Docs SSOT와 초안 사이의 충돌, 누락, 착수 가능성을 확인해야 한다.

`plan-review`를 선택하지 않는다:

- 기능설계서/정책서 초안을 아직 만들지 않은 경우: `plan-format`
- 초안 검토가 아니라 새 문서 생성이 목적인 경우: `plan-format`

### Workflow

```mermaid
flowchart TD
    A[초안 폴더 또는 기능설계서/정책서 파일] --> B[검토 대상 확정]
    B --> C{지원 문서 타입인가?}
    C -- 아니오 --> D[올바른 검토 대상이 아님 안내]
    C -- 예 --> E[짝문서 확인]
    E --> F[검토 대상 본문 직접 읽기]
    F --> G[Product Docs SSOT 후보 탐색]
    G --> H[관련 Markdown과 linked local resource 선택]
    H --> I{근거 패키지 상태}
    I -- failed --> J[수정 필요로 취합]
    I -- completed 또는 limited --> K[근거 관점 검토]
    I -- completed 또는 limited --> M[착수 가능성 관점 검토]
    K --> N[발견 사항 병합]
    M --> N
    N --> O{가장 보수적인 결과}
    O -- 통과 --> P[기획팀용 리포트와 publish_readiness 출력]
    O -- 조건부 통과 --> Q[확인 항목과 publish_readiness 출력]
    O -- 수정 필요 --> R[먼저 고칠 항목과 review_repair 출력]
```

### 결과 기준

| 결과 | 의미 |
|---|---|
| `통과` | 중요한 가정, 충돌, 필수 수정, 발행 전 확인, 검증 한계가 없고 근거가 충분하다 |
| `조건부 통과` | 남은 문제가 명시적이고 기획자가 발행 전에 확인하거나 수용할 수 있다 |
| `수정 필요` | 충돌, 불명확한 규칙, 근거 없는 가정 때문에 디자인·개발·QA·운영 판단이 달라질 수 있다 |
| `올바른 검토 대상이 아님` | 기능/화면설계서 또는 정책서 초안이 아닌 입력이라 검토를 수행하지 않는다 |

최종 취합은 `수정 필요 > 조건부 통과 > 통과` 순서로 보수적으로 결정한다. `blocked` 역할이 있으면 `수정 필요`이며, `blocked`는 발행 준비 상세에 포함하지 않는다.

## Routing Decision Tree

```mermaid
flowchart TD
    A[사용자 요청] --> B{기능설계서/정책서 초안 경로가 있는가?}
    B -- 예, 검토 요청 --> C[plan-review]
    B -- 아니오 --> D{문서 2개 생성/저장 요청인가?}
    D -- 예 --> E[plan-format]
    D -- 아니오 --> F[요청 범위를 확인하거나 일반 답변]
    E --> G{바로 검토까지 명시했는가?}
    G -- 예, 저장 성공 --> C
    G -- 아니오 --> H[plan-review 다음 단계 안내]
```

## 산출물 경계

- `planning/` 아래 산출물은 로컬 초안 템플릿이며 공식 팀 문서가 아니다.
- `plan-format`은 외부 시스템에 직접 게시하지 않는다.
- `plan-format`은 Product Docs SSOT 근거 검증을 수행하지 않는다.
- `plan-review`는 초안을 직접 수정하지 않고, 기획팀용 리포트와 발행 준비 상세 또는 재검토용 상세 정보를 출력한다.
- Product Docs SSOT는 현재 프로젝트의 Markdown과 그 Markdown이 상대경로로 참조한 로컬 resource다.
- 코드, 테스트, 설정, 빌드 산출물, dependency/vendor, 외부 URL, `planning/` 산출물은 SSOT 근거에서 제외한다.

## Reference Map

| 주제 | 기준 파일 |
|---|---|
| 스킬 개요 | [`../README.md`](../README.md) |
| `plan-format` 계약 | [`../skills/plan-format/SKILL.md`](../skills/plan-format/SKILL.md) |
| `plan-review` 계약 | [`../skills/plan-review/SKILL.md`](../skills/plan-review/SKILL.md) |
| 저장 위치와 atomic write | [`../skills/plan-format/references/storage-contract.md`](../skills/plan-format/references/storage-contract.md) |
| 사용자 출력 형식 | [`../skills/plan-format/references/output-contract.md`](../skills/plan-format/references/output-contract.md) |
| `plan-format` worker 계약 | [`../skills/plan-format/references/worker-contract.md`](../skills/plan-format/references/worker-contract.md) |
| `plan-review` gate 기준 | [`../skills/plan-review/references/review-gate.md`](../skills/plan-review/references/review-gate.md) |
