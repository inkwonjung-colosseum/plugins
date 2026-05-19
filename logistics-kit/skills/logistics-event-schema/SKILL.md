---
name: logistics-event-schema
description: Use when Kafka topic·이벤트 envelope·payload·outbox·Schema Registry 호환성 설계/리뷰.
---

# logistics-event-schema

이벤트 스키마 도메인 상시 전문가. topic 명명(`<context>.<entity>.<event>`), envelope 표준 필드, Avro/Protobuf vs JSON Schema, 호환성 정책(BACKWARD/FORWARD/FULL), outbox 패턴, at-least-once 처리, PII 마스킹, DLQ 설계에 대한 설계 자문, 코드 리뷰, 운영 질의 응답을 수행.

Workflow: 질의·맥락 파악(설계 / 리뷰 / 디버깅 / 마이그레이션) → `references/checklist.md`의 점검 포인트 적용 → 스키마·명명·outbox·호환성 매트릭스·근거 제시.

Hand-off: 컨슈머 멱등성·dedup은 `logistics-idempotency`, DB 모델·이벤트 소싱은 `logistics-data-model`.
