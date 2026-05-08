# planning-kit PRD chain

planning-kit PRD 6건의 관계·읽는 순서·핵심 변경 1줄 요약을 한 문서로 가이드.

## 읽는 순서

- **신규 사용자**: 본 README → `prd-0.2.2.md` → (필요 시) 역방향으로 상위 PRD 참고. 각 PRD 본문에 베이스가 명시돼 있어 chain 추적 가능.
- **기존 사용자**: 신규 PRD만 읽으면 충분 — 각 PRD가 incremental 베이스를 명시한다.

## PRD 관계도

| PRD | 관계 | 베이스 | 핵심 변경 (1줄) |
|---|---|---|---|
| 0.1.0 | base | (없음) | formalize 단일 스킬 — 텍스트·파일·디렉터리 입력 → 정책서·기능설계서 변환 + 자동 리뷰 (A·B축) |
| 0.1.1 | incremental | 0.1.0 | URL 분기·재귀 fetch·이미지 multimodal·SSOT 검색 키워드 노출 |
| 0.1.2 | incremental | 0.1.1 | connector fallback (Atlassian·Figma·Slack·Notion) + 인증 게이트 휴리스틱 |
| 0.2.0 | **breaking** | 0.1.2 | formalize 분할 → planning-format + planning-review. F6 markdown lint 추가. `--save` 옵션. Google Workspace 자원별 tool 시퀀스 |
| 0.2.1 | incremental | 0.2.0 | 입력 제외 § 카테고리 5 → 10종 + 항상 출력 + 처리 줄 + 헤더 분포 + F5 cross-ref 3종 |
| 0.2.2 | incremental | 0.2.1 | R1 SSOT corpus link follow + planning-review 입력 제외 § 인지 + Codex desc 압축 + README 비교표 갱신 + PRD chain 안내 |

## 호환성 요약

- **0.1.x → 0.2.0**: **breaking** (스킬 이름 변경 + 분할). 호출자 마이그레이션 필요 — `formalize` → `planning-format` + 선택적 `planning-review`.
- **그 외**: incremental, 출력 markdown micro-breaking 가능 (다운스트림 파서 영향 시 각 PRD §호환성 절 참조).

## PRD 파일

- [`prd-0.1.0.md`](./prd-0.1.0.md) — 0.1.0 base.
- [`prd-0.1.1.md`](./prd-0.1.1.md) — URL/재귀/이미지.
- [`prd-0.1.2.md`](./prd-0.1.2.md) — connector fallback.
- [`prd-0.2.0.md`](./prd-0.2.0.md) — 스킬 분할 (breaking).
- [`prd-0.2.1.md`](./prd-0.2.1.md) — 입력 제외 § 10종 + F5 cross-ref.
- [`prd-0.2.2.md`](./prd-0.2.2.md) — R1 link follow + 입력 제외 § R3 보조 신호.
