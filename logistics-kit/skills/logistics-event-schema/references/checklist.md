# logistics-event-schema 도메인 참조

## 활용 시점

- 설계 자문: topic 명명, envelope 표준, payload 스키마 형식 결정, 호환성 정책, outbox·DLQ 설계
- 코드·스키마 리뷰: `kafka`, `topic`, `outbox`, `cdc`, `event_store`, `*.avsc`, `*.proto`, `schema_registry` 등장 시
- 운영·디버깅: 호환성 깨짐, 컨슈머 처리 실패, PII 유출, 이중 쓰기 문제
- 사용자 발화 예: "topic 이름", "이벤트 발행", "outbox 테이블", "스키마 버전", "컨슈머 호환성"

## 점검 포인트

1. **topic 명명 규칙** — `<bounded-context>.<entity>.<event>` 패턴 일관? 예: `wms.inventory.adjusted`. ad-hoc 이름 금지.
2. **envelope 필드** — `event_id`(UUID), `event_type`, `event_version`, `occurred_at`, `producer`, `correlation_id`, `causation_id`, `payload` 표준 구조?
3. **payload 스키마 관리** — Avro/Protobuf + Schema Registry vs JSON Schema. 호환성(BACKWARD/FORWARD/FULL) 정책 설정?
4. **버전 관리** — `event_version` 변경 시 컨슈머 마이그레이션 윈도우? deprecated 이벤트 sunset 정책?
5. **Outbox 패턴** — DB 트랜잭션과 이벤트 발행을 한 트랜잭션 단위? 단순 producer.send()는 *이중 쓰기* 문제.
6. **at-least-once vs exactly-once** — Kafka 기본은 at-least-once. 컨슈머 멱등성(→ `logistics-idempotency`) 보장 필수.
7. **PII/민감 정보** — 수하인 정보가 이벤트에 raw로 실리지 않나? 마스킹/별도 topic 분리?
8. **DLQ(dead letter queue)** — 파싱·처리 실패 메시지 격리 + 재처리 도구?
9. **DLQ replay tooling** — replay GUI/CLI, target offset 지정·기간·필터, replay 시 부작용 격리·멱등성 보장
10. **Schema Registry 호환성 매트릭스** — BACKWARD / FORWARD / FULL / BACKWARD_TRANSITIVE — 도메인별 정책 표(예: 주문/inventory FULL, 추적 BACKWARD)
11. **Outbox → Debezium 레퍼런스** — outbox table 구조(`id`, `aggregate_type`, `aggregate_id`, `type`, `payload`, `published_at`), Debezium SMT 변환 표준
12. **retention·compaction 정책** — log 보존(7~30일), compacted topic(latest 보존), tiered storage·archive
13. **partitioning key 전략** — entity ID 기반(예: `order_id`), tenant_id 결합, 순서 보장 vs 부하 분산 트레이드오프
14. **key rotation·PII 토큰화** — payload 내 PII 토큰화 + 별도 vault, encryption key rotation, key versioning
15. **contract testing** — producer/consumer pact, Schema Registry CI 검증, breaking change 자동 감지

## 응답 형식

- 질문 → 표준 envelope·명명·호환성 정책·outbox 패턴
- 리뷰 → 스키마/명명/outbox 위반 항목·권장
- Schema Registry 호환성 매트릭스 확인 권고는 별도 표기

## Hand-off

- 컨슈머 멱등성·dedup → `logistics-idempotency`
- DB 모델·이벤트 소싱 → `logistics-data-model`
- 관측성·trace 전파 → `logistics-observability`
- saga·보상 → `logistics-saga`
- DR·replay 복구 → `logistics-dr`
- bulk 작업·DLQ replay → `bulk-operations`
- 다중 채널 fan-out (webhook) → `api-design-logistics`/`channel-sync`
- PII 토큰화 → `data-privacy-logistics`
