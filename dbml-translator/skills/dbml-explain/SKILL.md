---
name: dbml-explain
description: Use when a .dbml file or DBML code block needs a non-developer narrative (tables, refs, enums). DBML syntax only, not SQL DDL.
allowed-tools:
  - Read
  - Grep
  - Glob
disable-model-invocation: false
user-invocable: true
---
# dbml-explain

Translate a DBML schema into business-readable narrative for non-developers.

## When to use

- A `.dbml` file is in the conversation or referenced by path.
- A DBML code block appears (look for `Table`, `Ref:`, `Enum`, `Project` keywords).
- The user asks: "explain this schema", "what does this table store", "translate for PM", "비개발자도 이해하게 설명".

Do NOT use for plain SQL DDL — only DBML syntax. If unsure, check for `Ref:` shorthand or `Table X { ... }` block style.

## Output structure

Produce these sections in order, in the user's language (default Korean if user wrote Korean):

### 1. 한 줄 요약
One sentence: what business domain does this schema model? (e.g., "전자상거래 주문/결제 도메인").

### 2. 핵심 엔티티 (Tables)
For each `Table`, write:
- **테이블 이름** (technical) — **비즈니스 의미** (business-friendly name)
- 한 줄로 "무엇을 저장하는가" 설명. 기술 용어 금지 (PK/FK/index 등 등장하면 풀어쓴다).
- 주요 컬럼 3–5개만 골라 자연어로 풀이. `created_at` 같은 시스템 컬럼은 생략.

Example:
> **orders** — 주문
> 고객이 결제한 주문 내역을 보관한다. 누가(`user_id`), 언제(`placed_at`), 얼마(`total_amount`), 어떤 상태(`status`)인지를 기록.

### 3. 엔티티 간 관계 (Refs)
Walk through each `Ref:` as a business sentence — never as "FK".

DBML: `Ref: orders.user_id > users.id`
→ "한 명의 **사용자**는 여러 개의 **주문**을 가질 수 있다. (1:N)"

Group by cardinality (1:1 / 1:N / N:M) and order from most central entity outward.

### 4. 상태/분류값 (Enums)
Each `Enum` becomes a bullet list of allowed states with what each means in business terms. If the DBML has no `Note`, infer from naming but flag as inferred.

### 5. 비즈니스 시나리오 예시
Write 1–2 short narrative scenarios using the actual table/column names, e.g.:
> 사용자가 회원가입(`users` 신규 row) → 상품을 장바구니에 담음(`cart_items` 추가) → 결제하면 `orders` 한 건과 `order_items` 다건 생성, `status=paid`.

This is the section non-developers will actually read.

### 6. 누락/모호한 지점
Last section, short bullets. Things that surprised you while reading:
- 컬럼명만 보고는 의미가 불명확한 것 (e.g., `status_v2` — 왜 v2인지?)
- `Note` 없는 enum
- 비대칭적 관계 (있어야 할 것 같은데 없는 ref)
- 명명 일관성 깨진 부분

Keep this short — it is not a code review, just "things a PM would want to ask".

## Style rules

- 기술 용어 풀어쓰기: PK → "고유 식별값", FK → "~를 가리키는 연결", index → 언급 안 함.
- `snake_case` 컬럼명은 표기는 그대로 두되 직후에 한국어/자연어로 의미 풀이.
- 추측한 부분은 "(추정)" 또는 "DBML 주석 없어 명시되지 않음" 명시.
- 길이: 테이블 10개 기준 1–2화면. 절대 마크다운 테이블에 컬럼 전부 나열하지 않는다 (PM이 안 읽는다).
- 코드블록 안 사용. 식별자만 백틱.

