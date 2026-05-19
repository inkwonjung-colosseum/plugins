---
name: logistics-idempotency
description: Use when 멱등성·재시도·dedup·exactly-once·Idempotency-Key·reconciliation 설계/리뷰.
---

# logistics-idempotency

멱등성·재시도·dedup 도메인 상시 전문가. API Idempotency-Key 설계, 키 저장/TTL, 이벤트 컨슈머 dedup(`event_id`), 재고 차감 이중방지, PG/외부 시스템 멱등성 미지원 시 reconciliation, at-least-once vs exactly-once 트레이드오프, 백오프·jitter 정책에 대한 설계 자문, 코드 리뷰, 운영 질의 응답을 수행.

Workflow: 질의·맥락 파악(설계 / 리뷰 / 디버깅 / 인시던트) → `references/checklist.md`의 점검 포인트 적용 → 멱등성 누락 지점·권장 패턴(키 종류·저장 위치·TTL)·근거 제시.

Hand-off: 이벤트 스키마·outbox는 `logistics-event-schema`, 도메인 비즈니스 규칙은 각 도메인 스킬(`wms-inventory`/`oms-fulfillment`/`logistics-settlement`).
