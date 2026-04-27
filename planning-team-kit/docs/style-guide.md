# planning-team-kit Style Guide

## 문서 원칙

- Confluence 원본을 source of truth로 둔다.
- 로컬 Markdown export는 읽기 전용 snapshot으로 취급한다.
- 확인된 사실, 가정, 미정 항목을 섞지 않는다.
- 개발팀이 구현 판단에 필요한 조건을 표로 정리한다.

## 표현

- 확인되지 않은 내용은 `[가정]`으로 시작한다.
- 결정되지 않은 내용은 `[미정]`으로 표시한다.
- 기존 문서와 충돌하면 "충돌 경고"를 먼저 적고 초안에 무리하게 병합하지 않는다.
- 정책 조건은 "조건 → 처리 방식 → 비고" 순서로 쓴다.

## 문서 타입

| 타입 | 사용 기준 |
|---|---|
| 상위설계서 | WHY, 방향, 범위, 비목표, 성공 기준을 정리한다 |
| 기능설계서 | 화면, 플로우, 권한, 입력 유효성, 예외 처리를 정리한다 |
| 정책서 | 비즈니스 규칙, 조건, 상태 전이, 예외를 정리한다 |

## Publish 문구

초안 출력에는 publish 상태를 포함한다.

```text
Publish gate: clean
Review required reason: 없음
```

또는:

```text
Publish gate: review-required
Review required reason: [미정], [가정]
```
