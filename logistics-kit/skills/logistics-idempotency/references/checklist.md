# logistics-idempotency 도메인 참조

## 활용 시점

- 설계 자문: Idempotency-Key 키 종류·저장·TTL, 컨슈머 dedup, exactly-once 트레이드오프
- 코드·API 리뷰: `idempotency`, `retry`, `dedup`, `exactly_once`, `Idempotency-Key`, `consumer_offset` 등장 시
- 운영·인시던트: 이중 차감, 결제 중복, 컨슈머 리밸런싱 후 재처리
- 사용자 발화 예: "중복 호출", "재시도 정책", "이벤트 두 번 처리", "이중 차감", "Kafka 컨슈머 dedup"

## 점검 포인트

1. **API 멱등성 키** — POST/PUT 부작용 API에 `Idempotency-Key` 헤더 받음? 동일 키 N회 호출 = 1회 효과?
2. **키 저장/만료** — 멱등성 키 + 응답을 DB/Redis 저장. TTL 정책(24h ~ 7d) 명시?
3. **이벤트 컨슈머 dedup** — `event_id` 기반 처리 이력 + 중복 차단. partition 재처리/리밸런싱 안전?
4. **재고 차감 멱등성** — 같은 주문 차감 두 번 실행 = -1 보장? `order_id` unique constraint?
5. **결제/환불 호출** — PG trace_id를 멱등성 키로? PG가 멱등성 미지원이면 어떻게 보호?
6. **at-least-once vs exactly-once** — Kafka exactly-once는 transactional producer + consumer commit 결합. 부분 채택 시 한쪽이 깨짐.
7. **타임아웃·부분 실패** — HTTP 504 후 재시도 vs 백오프 + jitter. 외부 시스템 멱등성 미지원 시 reconciliation 배치?
8. **dedup 윈도우** — 무한 보존 불가. 윈도우 안에서만 보장한다는 점이 컨슈머에 문서화?
9. **distributed lock vs idempotency-key 트레이드오프** — pessimistic lock(`SELECT FOR UPDATE`·advisory lock) vs idempotency-key, 동시성 vs throughput 매트릭스
10. **retry-storm + circuit-breaker 결합** — retry budget·exponential backoff + circuit breaker open 시 retry 차단 (→ `resilience-patterns`)
11. **reconciliation 패턴 확장** — 정기 batch reconcile + 실시간 diff, 결과 차이 alert·자동 보정 trigger, 외부 시스템 멱등성 미지원 시 fallback
12. **saga 단계별 멱등성** — 보상 트랜잭션도 멱등 보장, 부분 보상 후 재실행 안전 (→ `logistics-saga`)
13. **bulk 작업 멱등성** — `bulk_job_id + item_id` 키, 일부 성공 후 재실행 누락/중복 방지 (→ `bulk-operations`)
14. **webhook receiver 멱등성** — 캐리어·채널 webhook의 `event_id`·`transaction_id` 기반 dedup (→ `carrier-edi`/`channel-sync`)

## 응답 형식

- 질문 → 표준 멱등성 패턴(키 종류·저장·TTL)·트레이드오프
- 리뷰 → 멱등성 누락 지점·권장 패턴
- 부작용 API 매트릭스(키 있음/없음) 제안은 별도 표기

## Hand-off

- 이벤트 스키마·outbox → `logistics-event-schema`
- 도메인 비즈니스 규칙 → `wms-inventory`/`oms-fulfillment`/`logistics-settlement`
- 복원 패턴(circuit breaker·bulkhead) → `resilience-patterns`
- saga·보상 → `logistics-saga`
- bulk·partial failure → `bulk-operations`
- webhook receiver (캐리어·채널) → `carrier-edi`/`channel-sync`
- DR·event replay → `logistics-dr`
