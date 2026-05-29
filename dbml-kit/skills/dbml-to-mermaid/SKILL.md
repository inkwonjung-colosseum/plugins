---
name: dbml-to-mermaid
description: Use when a .dbml file or DBML block needs a Mermaid erDiagram for Confluence, README, or planning docs.
allowed-tools:
  - Read
  - Grep
  - Glob
disable-model-invocation: false
user-invocable: true
---
# dbml-to-mermaid

Convert a DBML schema into a Mermaid `erDiagram` block ready to embed in Confluence, README, dbdocs, or a planning-kit deliverable.

## When to use

- A `.dbml` file or DBML block (`Table`, `Ref:`, `Enum`, `TableGroup`) is in the conversation.
- 사용자가 "ERD 만들어줘", "mermaid로 그려줘", "Confluence에 붙일 다이어그램", "render this DBML".
- A planning-kit doc needs a schema diagram before `planning-publish-confluence`.

비-ER 다이어그램(flow/sequence/state)은 `diagram-design`으로 핸드오프.

## 절차

1. **입력 검증.** SQL DDL(`CREATE TABLE`, `FOREIGN KEY ... REFERENCES`, 끝 `;` 등)이거나 불완전하면 **추정 진행 금지**, 멈춘다. (상세: `references/example.md`)
2. **Input handshake** — 변환 대상을 한 줄 명시. grouping 모호하면 확인.
3. **`references/example.md`를 읽는다** — worked example, 변환 규칙, cardinality 매핑표, alias/self-ref 처리, embed 타깃, loss-item 전체가 거기 있다.
4. 아래 출력을 순서대로 생성.

## 출력 (순서 고정)

1. **Mermaid block** — fenced `mermaid` 블록. `TableGroup`이 있으면 그룹당 1개, 없으면 단일.
2. **한국어 캡션** (1~2줄) — PM 가독, [[dbml-explain]]과 같은 비즈니스 톤. 추정 cardinality는 "(추정)".
3. **범례(legend)** — Mermaid 블록 직후 **항상**: "PK=각 행을 구분하는 고유값, FK=다른 표를 가리키는 연결, UK=중복 불가". (PM이 개발자 옆에서 마커를 해독하게.)
4. **Embed guide** (3줄 max) — Confluence / README / dbdocs.
5. **Loss notes** — DBML이 표현하나 Mermaid가 못 하는 것. 각 1줄, 사유+대안.

## 핵심 규칙 (상세는 reference)

- Table/column명 verbatim, `snake_case` 유지. 시스템 컬럼은 생략.
- **Cardinality 방향**: 항상 부모(1쪽) 먼저 + `||--o{`로 통일 → 까마귀발 역전 방지 (가장 치명적 오류). 예: `users ||--o{ orders : "user_id"`.
- alias는 실제 테이블명으로 환원, self-ref는 같은 엔티티 양끝. 12개 초과면 분할 제안.
- 약어 풀이는 `../dbml-explain/references/glossary.md` 기준. Mermaid 블록은 항상 fenced.

## Related

- [[dbml-explain]] — 다이어그램 없는 서술.
- [[dbml-spec-diff]] — PRD 갭 진단.
- [[dbml-questions]] — 개발자 확인 질문 묶음.
- 공통 용어집 `../dbml-explain/references/glossary.md`.
- `planning-publish-confluence` — 다운스트림 publish. `diagram-design` — 비-ER 다이어그램.
