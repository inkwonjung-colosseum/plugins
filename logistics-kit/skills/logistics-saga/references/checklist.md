# logistics-saga 도메인 참조

## 활용 시점

- 자문: orchestration vs choreography 결정, 보상 트랜잭션 설계, saga state 영속화, retry/timeout 정책
- 코드·정책 리뷰: `saga`, `orchestration`, `choreography`, `tcc`, `compensation`, `compensate`, `saga_state`, `state_machine`, `process_manager` 식별자가 보일 때
- 운영·인시던트: 보상 실패 누적, saga state 불일치, 분기 중복 발화, 영구 hang
- 사용자 발화 예: "saga", "보상 트랜잭션", "TCC", "분산 트랜잭션", "process manager"

## 점검 포인트

1. **orchestration vs choreography 결정** — 중앙 통제자(orchestrator) 명시적 vs 이벤트 전파(choreography), 단계 수·가시성·결합도 트레이드오프?
2. **TCC 패턴** — try(자원 예약) → confirm(확정) / cancel(취소) 3단계, 외부 서비스 멱등성 보장 시 활용?
3. **보상 트랜잭션 매트릭스** — 각 forward 단계마다 reverse 정의, semantic compensation(원복 ≠ 역연산) 차이?
4. **state 영속화** — saga state DB(외래키·optimistic lock·event sourcing), checkpoint·재시작?
5. **timeout·dead-letter** — 단계별 SLA timeout, 만료 시 자동 취소 vs 알람·수동 개입?
6. **멱등성 결합** — saga 단계마다 idempotency key, 컨슈머 dedup, 재실행 안전?
7. **이벤트 vs 명령 기반** — 명령(command·SAGA → 서비스) vs 이벤트(서비스 발행 → 처리), 결합도 영향?
8. **잠금 회피** — 장기 saga는 DB lock 보유 금지, 낙관적 동시성(version) 사용?
9. **부분 실패 격리** — 일부 단계 실패 시 다른 saga 영향 격리(thread/queue 분리), retry storm 방지?
10. **observability** — saga ID·correlation·causation, 단계별 상태 dashboard, stuck saga alert?
11. **재실행 가능성(replay)** — 이벤트 로그 기반 재구성, 실패한 saga 수동 재시작 도구?
12. **트랜잭션 경계 설계** — 핵심 saga 예: 주문 → 결제·재고 차감·출고 지시·라벨 발급 — 각 경계 ACID vs eventual?
13. **process manager 패턴** — 다수 동시 saga 관리, 상태 분리, lifecycle 시각화?

## Saga 예시 (주문 fulfillment)

```
forward: 결제 → 재고 차감 → 출고 지시 → 라벨 발급 → 카운터 update
compensate: 환불 ← 재고 복원 ← 출고 취소 ← 라벨 void ← 카운터 rollback
```

## 응답 형식

- 질문 → 결정 트리·보상 매트릭스·state 모델
- 리뷰 → 약점·위험·수정 제안 (필요 시 `file:line`)
- 분산 동시성·partial failure 위험 별도 강조

## Hand-off

- 멱등성/dedup → `logistics-idempotency`
- 이벤트 envelope → `logistics-event-schema`
- ERD·이벤트 소싱 → `logistics-data-model`
- 관측성·trace/causation → `logistics-observability`
- 외부 시스템 멱등성 미지원 → `logistics-idempotency` (reconciliation 패턴)
- bulk saga·재실행 → `bulk-operations`
