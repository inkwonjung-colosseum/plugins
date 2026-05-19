---
name: dbml-spec-diff
description: Use when both a DBML schema and a PRD/기획서 are present to surface missing entities, drift, and cardinality conflicts.
allowed-tools:
  - Read
  - Grep
  - Glob
disable-model-invocation: false
user-invocable: true
---
# dbml-spec-diff

Find gaps between a DBML schema and the product spec it is supposed to implement.

## When to use

- BOTH a DBML artifact AND a spec document are present in the conversation (file paths, pasted content, URLs).
- User asks: "기획서랑 다른 부분", "스펙대로 됐는지", "PRD와 스키마 비교", "does the DB cover spec X".

If only DBML present → tell user to also share the spec, then route to [[dbml-explain]] instead.
If only spec present → tell user no DBML to compare, do not invent one.

## Input handshake

Before analysis, state in one line what you are using as each side:
> DBML: `schemas/order.dbml` (87 lines)
> 기획서: `docs/PRD-주문.md` (3 sections)

If either is ambiguous, ask the user to confirm before diffing. Do not silently pick.

## Analysis axes

Produce these sections in order:

### 1. 커버리지 매트릭스
A short table mapping each spec-level **business object** to a DBML table.

| 기획서 개념 | DBML 테이블 | 상태 |
|---|---|---|
| 회원 | `users` | OK |
| 주문 | `orders` | OK |
| 환불 | (없음) | **누락** |
| 적립금 | `point_ledger` | **부분** (충전 흐름만 있고 사용 흐름 없음) |

Statuses: `OK` / `부분` / `누락` / `초과` (DBML에만 있고 기획서 언급 없음).

### 2. 누락 (기획서에 있지만 DBML에 없는 것)
List each. For each entry:
- 기획서 출처 (섹션/문장 인용 1줄)
- 어디에 추가해야 할지 (테이블 신설 / 기존 테이블 컬럼 추가 / 새 enum 값)
- 의존 관계 (이 누락이 다른 누락의 원인인가)

순서: 비즈니스 영향 큰 것부터.

### 3. 초과 (DBML에 있지만 기획서가 언급 안 한 것)
중요. 시니어 PM은 이 섹션을 가장 먼저 본다.
- 정당한 시스템 컬럼인가 (created_at, updated_at, deleted_at, version) → 무시
- 미래 기능 대비 / 기술 부채 / 옛 기획 잔재 / 정말 빠진 기획?
각 항목에 "왜 있는지 묻는 질문" 1개를 같이 적는다.

### 4. 의미 불일치
Same name, different meaning OR different name, same meaning.
- 기획서: "주문 취소" / DBML: `orders.status = 'refunded'` → 취소와 환불은 다른 개념인가?
- 기획서: "적립금 잔액" / DBML: `users.point_balance` vs `point_ledger` 합계 → SoT 어디?

### 5. 관계(cardinality) 충돌
기획서가 암시하는 cardinality와 DBML `Ref`의 충돌만.
- 기획서: "한 주문에 하나의 결제 수단" / DBML: `orders` ↔ `payments` 가 1:N → 분할결제 의도된 것?

### 6. 위험도 분류 (Top 3)
마지막에 위 모든 항목을 P0/P1/P2로 분류해 상위 3개만:
- **P0**: 출시 차단. 핵심 비즈니스 흐름이 표현 불가.
- **P1**: 출시는 되지만 후속 마이그레이션 큰 영향.
- **P2**: 명명/주석/문서 차원.

## Style rules

- 비난 톤 금지. "~가 빠져 있다" 말고 "~가 기획서에는 있는데 DBML에서 찾지 못함. 의도된 분리인지 확인 필요".
- 기획서/DBML 원문에 없는 도메인 사실은 추정 표기.
- 결론을 먼저, 근거를 뒤에 (PM 가독성).
- "FK", "normalization", "index" 같은 개발자 용어 가능한 한 회피. 꼭 써야 하면 1줄 풀이.
- 출력 길이: 1 화면 ± 50%. 매트릭스 + 누락/초과 핵심만.

## Related

- [[dbml-explain]] — DBML 자체를 비개발자에게 설명만 필요할 때.

