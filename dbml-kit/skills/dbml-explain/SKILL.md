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
- A DBML code block appears. 탐지 신호: `Table X { ... }` 블록 + 관계 표기 중 하나 — `Ref:`(standalone), `[ref:`(inline), `Ref name { ... }`(block). `Enum`/`Project`/`TableGroup`도 신호.
- 사용자가 "이 스키마 설명", "이 표에 뭐가 저장돼?", "PM에게 설명", "비개발자도 이해하게 설명" 요청.

Do NOT use for plain SQL DDL — only DBML. 헷갈리면 `Ref:` 약어나 `Table X { ... }` 블록 스타일을 확인.

## 절차

1. **입력 검증 먼저.** SQL DDL(`CREATE TABLE`, `VARCHAR(n)`, `FOREIGN KEY ... REFERENCES`, 끝 `;` 등) 또는 불완전/잘린 입력이면 **추정으로 진행하지 말고** 멈춘다. 거부 스크립트와 malformed/dangling-ref 처리 규칙은 `references/output-spec.md`의 "Input validation 상세" 참고.
2. **`references/output-spec.md`를 읽는다** — 6개 출력 섹션의 정확한 형식·예시·엣지 규칙(alias, composite/self-ref, 참조 액션, 카디널리티 풀이, index, 대용량 처리)이 거기 있다.
3. 아래 6개 섹션을 사용자 언어(한국어 입력이면 한국어)로 순서대로 출력한다.

## 출력 섹션 (순서 고정)

1. **한 줄 요약** — 어떤 비즈니스 도메인인가. `Project` Note가 있으면 1차 근거.
2. **핵심 엔티티** — 각 `Table`을 기술명 — 비즈니스 의미 + 무엇을 저장하는지. 주요 컬럼 3–5개 + 연결(`_id`) 컬럼은 항상. Note/nullable 반영.
3. **엔티티 간 관계** — 각 ref를 비즈니스 문장으로(never "FK"). 카디널리티 약어는 첫 등장 시 괄호 풀이, `N:M`은 연결 테이블 문장 강제.
4. **상태/분류값 (Enums)** — 허용 값 + 비즈니스 의미. Note 없으면 (추정).
5. **비즈니스 시나리오** — 실제 식별자로 1–2개 서술. `default` 상태는 초기값으로 명시. *PM이 실제로 읽는 섹션.*
6. **누락/모호 → 개발자 질문** — 막힌 지점을 개발자에게 보낼 **질문 1줄씩**. 비대칭 관계는 단정 말고 질문. 5개 초과면 [[dbml-questions]]로 라우팅.

각 섹션의 예시·세부 규칙은 모두 `references/output-spec.md`를 따른다.

## 핵심 스타일 (상세는 reference)

- 기술 용어 풀어쓰기 — PK/FK/UK 등은 `references/glossary.md` 기준 통일.
- 추측은 "(추정)" 표기. 코드블록 미사용, 식별자만 백틱.
- 길이 1–2화면. 컬럼 전부 나열 금지. 대용량(20+ 테이블)은 핵심+요약, 무언급 누락 금지.

## Related

- [[dbml-spec-diff]] — 기획서/PRD와 스키마 갭 확인.
- [[dbml-to-mermaid]] — 같은 그림(ERD)으로 개발자와 화면 공유.
- [[dbml-questions]] — 개발자 확인 질문 묶음 생성.
- 설명 후 자연스러운 다음 단계 안내 (기획서 비교 → ERD 공유 → 질문 정리).
