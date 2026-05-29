---
name: dbml-questions
description: Use when a non-developer needs prioritized confirmation questions about a DBML schema to send a developer. DBML syntax only.
allowed-tools:
  - Read
  - Grep
  - Glob
disable-model-invocation: false
user-invocable: true
---
# dbml-questions

DBML 스키마(+선택적 기획서/explain·diff 결과)를 보고 **개발자에게 그대로 붙여넣어 보낼 확인 질문 묶음**을 만든다. 비개발자가 "무엇을 모르는지" 알고 올바른 질문으로 합의를 끌어내는 단계의 산출물.

## When to use

- DBML이 있고 사용자가 "개발자에게 뭘 물어봐야 해?", "확인 질문 정리", "질문 리스트", "슬랙에 보낼 질문" 요청.
- [[dbml-explain]] §6 질문이 5개를 넘어 라우팅된 경우.
- [[dbml-spec-diff]]에서 도출된 P0/P1 항목을 합의용 질문으로 묶을 때.

## 절차

1. **입력 검증.** SQL DDL(`CREATE TABLE`, `FOREIGN KEY ... REFERENCES` 등)이거나 불완전하면 "DBML 전용입니다, 변환해 드릴까요?"로 응답하고 **추정 진행 금지**.
2. **`references/format.md`를 읽는다** — 4요소 질문 형식·예시·질문 카테고리·채널 톤·스타일 규칙이 거기 있다.
3. 복붙용 질문 묶음을 P0→P1→P2 순으로 출력.

## 출력 핵심

- 복사 가능한 질문 블록(코드블록 아님). **각 질문 4요소**: `[근거 식별자]` `[질문(Yes/No·객관식)]` `[내 추정 답]` `[P0/P1/P2]`.
- 6개 카테고리(의미 모호·SoT 충돌·cardinality 의도·누락 흐름·soft-delete·nullable/참조 액션)를 빠짐없이 점검 — 상세·예시는 `references/format.md`.
- 단정 금지(추정은 질문으로), 추정 항목은 P0 금지, 약어는 `../dbml-explain/references/glossary.md` 기준 풀이.

## Related

- [[dbml-explain]] — 먼저 스키마 이해 (질문의 근거).
- [[dbml-spec-diff]] — 기획서 갭에서 합의용 질문 도출.
- [[dbml-to-mermaid]] — 질문 정리 후 ERD로 같은 그림 공유.
- 공통 용어집 `../dbml-explain/references/glossary.md`.
