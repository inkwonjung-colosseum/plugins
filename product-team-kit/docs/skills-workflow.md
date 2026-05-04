# product-team-kit 스킬 워크플로

`product-team-kit`은 기획을 바로 문서화하는 도구가 아니라, 기획 입력을 만들고(`plan-draft`), 로컬 초안 두 문서로 정리하고(`plan-format`), 외부 반영 전에 검토하는(`plan-review`) 3단계 제품팀 워크플로다.

이 문서는 README의 빠른 시작보다 한 단계 자세히, 어떤 스킬을 언제 선택하고 어떤 산출물로 이어지는지 설명한다.

## 전체 스킬 맵

| 스킬 | 역할 | 주요 입력 | 주요 산출물 | 다음 단계 |
|---|---|---|---|---|
| `plan-draft` | 질문으로 핵심 모호함을 줄여 `plan-format` 입력용 기획초안을 만든다 | 기획 의도, 주제, 파일 경로, 로컬 프로젝트 경로 | `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/[안전기능명]_기획초안.md` | `plan-format` |
| `plan-format` | 충분한 기획 입력을 기능설계서와 정책서 로컬 초안으로 나눈다 | 기획초안, 기획 노트, 회의록, AI 대화 결과물, 문서 스크랩 | `[안전기능명]_기능설계서.md`, `[안전기능명]_정책서.md` | `plan-review` |
| `plan-review` | 기능설계서/정책서 초안을 발행 전 gate로 검토한다 | 초안 폴더 또는 기능설계서/정책서 파일 | `pass`, `conditional pass`, `수정 필요` 판단과 근거/수정 블록 | 사람의 반영 또는 초안 수정 |

## 호출 방식

| 환경 | plan-draft | plan-format | plan-review |
|---|---|---|---|
| Claude Code | `/product-team-kit:plan-draft` | `/product-team-kit:plan-format` | `/product-team-kit:plan-review` |
| Codex | `$plan-draft` | `$plan-format` | `$plan-review` |

## 전체 흐름

```mermaid
flowchart TD
    A[기획 의도, 주제, 메모, 파일 경로] --> B{기획 입력이 충분한가?}
    B -- 아니오 또는 질문 필요 --> C[plan-draft]
    C --> D{기획초안 저장 가능?}
    D -- 질문 필요 --> E[사용자에게 1~3개 질문]
    E --> C
    D -- 저장 보류 --> F[부족 항목과 재실행 입력 블록 출력]
    D -- 저장 완료 --> G[기획초안 저장]
    B -- 예 --> H[plan-format]
    G --> H
    H --> I{기능설계서/정책서 생성 가능?}
    I -- 정보 부족 --> J[저장하지 않고 plan-draft 보완 안내]
    I -- draft artifact도 부족 --> K[사용자 결정 필요]
    I -- 가능 --> L[기능설계서와 정책서 저장]
    L --> M[plan-review]
    M --> N{발행 전 gate 결과}
    N -- pass --> O[발행 준비 증적 출력]
    N -- conditional pass --> P[확인 조건과 발행 준비 증적 출력]
    N -- 수정 필요 --> Q[수정 작업 블록 출력]
    Q --> R[사람 또는 후속 작업이 초안 수정]
    R --> M
```

## Skill 1. plan-draft

### 설명

`plan-draft`는 사용자가 아직 기획을 정리하는 단계에서 사용한다. 기능 목적, 사용자, 범위, 정책 조건, 화면 흐름, 예외, 권한, 상태, 확인 기준을 질문으로 좁히고 `plan-format`에 넘길 수 있는 기획초안을 저장한다.

직접 기능설계서나 정책서를 만들지 않고, 발행 전 근거 검증도 하지 않는다.

### 선택 기준

`plan-draft`를 선택한다:

- 질문하면서 기획 방향을 잡아야 한다.
- 문제, 사용자, 범위, 정책 조건이 아직 모호하다.
- `plan-format`이 정보 부족으로 저장 보류했다.
- 기능설계서/정책서 생성 전에 입력을 정리해야 한다.

`plan-draft`를 선택하지 않는다:

- 이미 충분한 기획 입력을 문서 2개로 정리하려는 경우: `plan-format`
- 이미 생성된 초안을 발행 전 검토하려는 경우: `plan-review`

### Workflow

```mermaid
flowchart TD
    A[입력 확인: 기획 의도, 주제, 파일, 프로젝트 경로] --> B[입력 디스패치]
    B --> C{로컬 프로젝트 맥락 확인이 필요한가?}
    C -- 예 --> D[관련 Markdown 후보를 좁게 탐색]
    C -- 아니오 --> E[질문 필요 항목 판단]
    D --> E
    E --> F{저장 가능 조건 충족?}
    F -- 아니오, 대화 가능 --> G[일반 대화 또는 질문 도구로 1~3개 질문]
    G --> H[사용자 답변 수집]
    H --> E
    F -- 아니오, 대화 불가 --> I[질문 필요로 저장 보류]
    F -- 질문 후에도 부족 --> J[초안 부족으로 저장 보류]
    F -- 예 --> K[기획초안 작성]
    K --> L{저장 성공?}
    L -- 예 --> M[기획초안 저장 완료]
    L -- 아니오 --> N[초안 충분하지만 저장 실패]
    M --> O[다음 단계: plan-format]
```

### 저장 가능 조건

모두 충족해야 한다:

- 기능명이 있다.
- 문제 또는 목적을 한 문장으로 설명할 수 있다.
- 주요 사용자 또는 업무 범위를 설명할 수 있다.
- 핵심 사용자 행동과 기대 결과가 1개 이상 있다.
- 정책, 조건, 제약 중 최소 1개 이상 있다.

### 산출물

```text
planning/[안전기능명]--YYYY-MM-DD-HHMMSS/[안전기능명]_기획초안.md
```

기획초안에는 문제와 목적, 사용자와 업무 범위, 포함/제외 범위, 사용자 흐름, 정책과 조건, 상태/권한/예외, 화면 또는 입력 정보, 확인 기준, 로컬 출처, 미정/가정/확인 필요 질문이 포함된다.

## Skill 2. plan-format

### 설명

`plan-format`은 기획 입력을 기능설계서와 정책서 초안으로 정리하는 formatting 스킬이다. 입력이 충분한지 먼저 판단하고, 충분하면 두 문서를 하나의 저장 단위로 생성한다.

Project Docs SSOT 근거 검증은 하지 않는다. 검증은 `plan-review` 책임이다.

### 선택 기준

`plan-format`을 선택한다:

- 기획 노트, 회의록, AI 대화 결과물, 초안 문서 스크랩을 기능설계서와 정책서로 정리해야 한다.
- `plan-draft` 산출 `_기획초안.md`를 문서 2개로 변환해야 한다.
- 입력에 기능 목적, 대상, 핵심 행동, 주요 조건이 충분히 있다.

`plan-format`을 선택하지 않는다:

- 질문하면서 기획 방향을 잡아야 하는 경우: `plan-draft`
- 이미 생성된 기능설계서/정책서 초안을 검토해야 하는 경우: `plan-review`

### Workflow

```mermaid
flowchart TD
    A[기획 입력 또는 파일 경로] --> B[입력 확인과 디스패치]
    B --> C[기능명과 안전기능명 추출]
    C --> D{초안 생성 가능 조건 충족?}
    D -- 일반 입력 부족 --> E[저장 보류: plan-draft 보완 안내]
    D -- draft artifact 입력 부족 --> F[사용자 결정 필요]
    D -- 디자인/개발 상세만 많음 --> G[저장 보류: 제품·업무 판단 정보 요청]
    D -- 기존 산출물 존재 --> H[저장 보류: 덮어쓰기 금지]
    D -- 충족 --> I[공통 정리 기준 확정]
    I --> J{분리 컨텍스트 사용 가능?}
    J -- 예 --> K[기능설계서 worker]
    J -- 예 --> L[정책서 worker]
    J -- 아니오 --> M[동일 세션에서 기능설계서 후 정책서 순차 작성]
    K --> N[최종 조정]
    L --> N
    M --> N
    N --> O{two-file 저장 성공?}
    O -- 예 --> P[기능설계서와 정책서 저장 완료]
    O -- 아니오 --> Q[저장 실패와 partial artifact 안내]
    P --> R[다음 단계: plan-review]
```

### 생성 가능 조건

각 항목을 1개 이상 충족해야 한다:

- 기능 목적 또는 기능명: 기능명, 문제, 목적 중 한 문장 요약 가능
- 적용 대상 또는 업무 범위: 사용자, 역할, 조직, 업무 대상, 포함 범위 중 확인 가능
- 핵심 사용자 행동과 기대 결과: 행동 1개와 결과 1개
- 주요 조건/정책/제약: 허용, 금지, 조건, 예외, 제한, 판단 기준 중 확인 가능

### 산출물

일반 입력은 새 timestamp 폴더에 저장한다:

```text
planning/[안전기능명]--YYYY-MM-DD-HHMMSS/[안전기능명]_기능설계서.md
planning/[안전기능명]--YYYY-MM-DD-HHMMSS/[안전기능명]_정책서.md
```

`plan-draft` 산출 `_기획초안.md`를 입력으로 받으면 같은 기획초안 폴더를 재사용한다.

## Skill 3. plan-review

### 설명

`plan-review`는 `plan-format`으로 저장한 기능설계서/정책서 초안을 외부 반영 전에 검토하는 gate다. 템플릿 모양만 보는 검사가 아니라, Project Docs SSOT 근거, 결정·범위, 실행·검증 가능성을 확인한다.

검토 대상은 `planning/` 아래 초안일 수 있지만, `planning/` 파일은 SSOT 근거로 사용하지 않는다.

### 선택 기준

`plan-review`를 선택한다:

- 기존 초안 폴더나 기능설계서/정책서 파일을 검토해야 한다.
- 외부 공유 또는 팀 문서 반영 전에 pass 여부를 판단해야 한다.
- Project Docs SSOT와 초안 사이의 충돌, 누락, 실행 가능성을 확인해야 한다.

`plan-review`를 선택하지 않는다:

- 기획 입력 자체가 아직 부족한 경우: `plan-draft`
- 기능설계서/정책서 초안을 아직 만들지 않은 경우: `plan-format`

### Workflow

```mermaid
flowchart TD
    A[초안 폴더 또는 기능설계서/정책서 파일] --> B[검토 대상 확정]
    B --> C{지원 문서 타입인가?}
    C -- 아니오 --> D[P0 입력 오류로 종료]
    C -- 예 --> E[짝문서 확인]
    E --> F[검토 대상 본문 직접 읽기]
    F --> G[Project Docs SSOT 후보 탐색]
    G --> H[관련 Markdown과 linked local resource 선택]
    H --> I{근거 패키지 상태}
    I -- failed --> J[수정 필요로 취합]
    I -- completed 또는 limited --> K[근거 관점 검토]
    I -- completed 또는 limited --> L[결정·범위 관점 검토]
    I -- completed 또는 limited --> M[실행·검증 가능성 관점 검토]
    K --> N[발견 사항 병합]
    L --> N
    M --> N
    N --> O{가장 보수적인 결과}
    O -- pass --> P[publish_readiness 출력]
    O -- conditional pass --> Q[확인 조건과 publish_readiness 출력]
    O -- 수정 필요 --> R[수정 작업 블록 출력]
```

### 결과 기준

| 결과 | 의미 |
|---|---|
| `pass` | 중요한 가정, 충돌, 수정 포인트, 확인 조건, 검증 한계가 없고 근거가 충분하다 |
| `conditional pass` | 남은 문제가 명시적이고 기획자가 발행 전에 확인하거나 수용할 수 있다 |
| `수정 필요` | 누락된 결정, 충돌, 불명확한 규칙, 근거 없는 가정 때문에 구현 또는 운영 판단이 달라질 수 있다 |

최종 취합은 `수정 필요 > conditional pass > pass` 순서로 보수적으로 결정한다.

## Routing Decision Tree

```mermaid
flowchart TD
    A[사용자 요청] --> B{기능설계서/정책서 초안 경로가 있는가?}
    B -- 예, 검토 요청 --> C[plan-review]
    B -- 아니오 --> D{기획 입력이 충분한가?}
    D -- 아니오 또는 질문 요청 --> E[plan-draft]
    D -- 예 --> F{문서 2개 생성/저장 요청인가?}
    F -- 예 --> G[plan-format]
    F -- 아니오 --> H[요청 범위를 확인하거나 일반 답변]
    G --> I{바로 검토까지 명시했는가?}
    I -- 예, 저장 성공 --> C
    I -- 아니오 --> J[plan-review 다음 단계 안내]
```

## 산출물 경계

- `planning/` 아래 산출물은 로컬 초안 템플릿이며 공식 팀 문서가 아니다.
- `plan-draft`와 `plan-format`은 외부 시스템에 직접 게시하지 않는다.
- `plan-format`은 Project Docs SSOT 근거 검증을 수행하지 않는다.
- `plan-review`는 초안을 직접 수정하지 않고, 수정 포인트 또는 발행 준비 증적을 출력한다.
- Project Docs SSOT는 현재 프로젝트의 Markdown과 그 Markdown이 상대경로로 참조한 로컬 resource다.
- 코드, 테스트, 설정, 빌드 산출물, dependency/vendor, 외부 URL, `planning/` 산출물은 SSOT 근거에서 제외한다.

## Reference Map

| 주제 | 기준 파일 |
|---|---|
| 스킬 개요 | [`../README.md`](../README.md) |
| `plan-draft` 계약 | [`../skills/plan-draft/SKILL.md`](../skills/plan-draft/SKILL.md) |
| `plan-format` 계약 | [`../skills/plan-format/SKILL.md`](../skills/plan-format/SKILL.md) |
| `plan-review` 계약 | [`../skills/plan-review/SKILL.md`](../skills/plan-review/SKILL.md) |
| 저장 위치와 atomic write | [`../references/storage-contract.md`](../references/storage-contract.md) |
| 사용자 출력 형식 | [`../references/output-contract.md`](../references/output-contract.md) |
| `plan-format` worker 계약 | [`../skills/plan-format/references/worker-contract.md`](../skills/plan-format/references/worker-contract.md) |
| `plan-review` gate 기준 | [`../skills/plan-review/references/review-gate.md`](../skills/plan-review/references/review-gate.md) |
