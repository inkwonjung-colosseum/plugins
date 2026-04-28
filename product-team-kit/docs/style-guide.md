# product-team-kit Style Guide

## 문서 원칙

- Confluence 원본을 source of truth로 둔다.
- 로컬 Markdown export는 읽기 전용 snapshot으로 취급한다.
- 확인된 사실, 가정, 미정 항목을 섞지 않는다.
- `plan-format`은 생성 전 `Draftability gate`로 초안 생성 가능성을 점검하고, 통과한 입력만 템플릿에 맞게 formatting한다.
- `plan-format`은 입력 해석과 공통 planning brief 확정은 순차로 처리하고, 기능설계서/정책서 본문 작성만 병렬화한다.
- `plan-format`은 Confluence 검색이나 index 조회를 수행하지 않는다.
- Confluence 검증과 발행 전 판단은 `plan-review`에서 수행한다.
- 기획자가 결정해야 하는 기능 동작, 조건, 예외를 표로 정리한다.

## 표현

- 확인되지 않은 내용은 `[가정]`으로 시작한다.
- 결정되지 않은 내용은 `[미정]`으로 표시한다.
- 검증이 필요한 내용은 확인 필요 질문으로 남긴다.
- 기존 문서와의 충돌 판정은 `plan-review`에서 수행한다.
- 정책 조건은 "조건 → 처리 방식 → 비고" 순서로 쓴다.

## 문서 타입

| 타입 | 사용 기준 |
|---|---|
| 기능설계서 | 화면, 플로우, 권한, 입력 유효성, 예외, 인수 조건 / 확인 기준을 정리한다 |
| 정책서 | 비즈니스 규칙, 조건, 상태 전이, 예외, 입력에 포함된 관련 문서와 근거를 정리한다 |

## 초안 출력 문구

초안 출력에는 생성 전 판단인 `Draftability gate`만 포함한다. 발행 전 판단은 `plan-review`에서 수행한다.

입력이 부족하면 파일을 만들지 않고 저장 보류를 출력한다.

```text
저장 보류
Draftability gate: blocked
```

입력이 충분해 파일을 만들면 다음처럼 출력한다.

```text
Draftability gate: passed
```

또는:

```text
Draftability gate: passed
plan-review 권장 신호: [미정], [가정], 확인 필요 질문
```
