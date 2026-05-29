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

- BOTH a DBML artifact AND a spec document are present (file paths, pasted content, URLs).
- DBML 탐지: `Table X { ... }` 블록 + 관계 표기(`Ref:`/`[ref:`/`Ref name { }`) 중 하나.
- 사용자가 "기획서랑 다른 부분", "스펙대로 됐는지", "PRD와 스키마 비교", "does the DB cover spec X".

- DBML만 있으면 → 기획서도 공유해 달라고 안내 후 [[dbml-explain]]로 라우팅.
- 기획서만 있으면 → 개발자에게 해당 기능의 `.dbml`을 요청하라고 안내. **DBML을 임의로 지어내지 않는다.**

## 절차

1. **입력 검증.** DBML 쪽이 SQL DDL(`CREATE TABLE`, `FOREIGN KEY ... REFERENCES`, 끝 `;` 등)이거나 불완전하면 **추정 진행 금지**, 멈춘다. (상세: `references/axes.md`)
2. **Input handshake** — 각 측이 무엇인지 한 줄 명시. 모호하면 확인 후 진행.
3. **`references/axes.md`를 읽는다** — 7개 섹션의 형식·예시·추정 가드가 거기 있다.
4. 아래 7개 섹션을 순서대로 출력.

## 출력 섹션 (순서 고정)

1. **커버리지 매트릭스** — 기획서 개념 → DBML 테이블, 상태 `OK`/`부분`/`누락`/`초과`.
2. **누락** — 기획서엔 있으나 DBML에 없음. 출처 인용 + 추가 위치 + 의존. 영향순.
3. **초과** — DBML엔 있으나 기획서 미언급. 시스템 컬럼은 무시, 각 항목에 "왜 있나" 질문. *PM이 먼저 보는 섹션.*
4. **의미 불일치** — 같은 이름 다른 의미 / 다른 이름 같은 의미. SoT 어디인지.
5. **관계(cardinality) 충돌** — 기획서 암시 vs DBML `Ref`. 명시 안 된 건 추정 가드 적용.
6. **위험도 분류 (Top 3)** — P0(출시 차단)/P1(마이그레이션 영향)/P2(문서). 추정 항목은 P0 금지.
7. **개발자 합의용 질문 묶음** — §3~§5 질문을 복붙 체크리스트로(P0→P1→P2). 많으면 [[dbml-questions]]로 위임.

각 섹션의 예시·세부 규칙은 `references/axes.md`를 따른다.

## 핵심 스타일 (상세는 reference)

- 비난 톤 금지 — "빠졌다" 대신 "기획서엔 있는데 DBML에서 못 찾음, 의도된 분리인지 확인".
- 원문에 없는 사실은 추정 표기. 결론 먼저, 근거 뒤.
- 개발자 용어(FK/index 등)는 항상 풀어쓴다 — `../dbml-explain/references/glossary.md` 기준. 약어 단독 금지.

## Related

- [[dbml-explain]] — DBML 자체 설명만 필요할 때.
- [[dbml-questions]] — 도출된 갭을 개발자 합의용 질문 묶음으로.
- [[dbml-to-mermaid]] — 같은 그림(ERD)으로 화면 공유.
- 공통 용어집 `../dbml-explain/references/glossary.md`.
