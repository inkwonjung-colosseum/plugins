# logistics-dr 도메인 참조

## 활용 시점

- 자문: RPO/RTO 목표, snapshot cadence, region failover, event replay 복구 전략 수립
- 코드·정책 리뷰: `disaster_recovery`, `dr`, `rpo`, `rto`, `snapshot`, `pitr`, `region_failover`, `active_active`, `active_passive`, `replay`, `backup_test` 식별자/문서 등장 시
- 운영·인시던트: 1차 region 장애·DB 손상·DC 단절, DR 테스트 실패, 데이터 손실
- 사용자 발화 예: "RPO/RTO", "재해복구", "snapshot", "region failover", "PITR"

## 점검 포인트

1. **RPO·RTO 목표** — 도메인별 매트릭스 (재고 ledger·주문 RPO 1분/RTO 15분, 통계 RPO 1h/RTO 4h)?
2. **백업 cadence** — full / incremental / WAL streaming, PITR(point-in-time recovery) 범위?
3. **재고 ledger snapshot** — 정기 snapshot + event log replay로 임의 시점 재구성, 일관성 검증?
4. **region failover 토폴로지** — active-active(geo-aware routing) vs active-passive(warm standby) vs pilot-light, 데이터 sync(동기 vs 비동기) 트레이드오프?
5. **event log replay** — 컨슈머 offset reset 정책, 재처리 안전(멱등성), 외부 부작용(이메일·라벨 발급) 격리?
6. **외부 의존성 매트릭스** — PG·캐리어 API·식약처·세관 — 각각 가용성·복구 SLA·우회·대기 정책?
7. **DR 테스트** — 분기·반기 game day, 부분(서비스 단위) vs 전체 region 시뮬레이션, 결과 KPI?
8. **데이터 일관성 검증** — 복구 후 reconciliation 절차(재고·주문·정산), 외부 시스템 sync?
9. **백업 보관기간** — 일별 30일 / 주별 1년 / 월별 7년, 매트릭스 + 암호화·접근통제?
10. **runbook** — 단계별 명령·responsible role·escalation·예상 시간 — 30분 1차 대응 가능?
11. **부분 장애 격리** — single-AZ vs multi-AZ vs cross-region 매트릭스, bulkhead 패턴?
12. **데이터 destruction(영구 삭제)** — tenant off-boarding 시 백업·snapshot 포함 삭제 보증?
13. **외부 데이터 의존(MDM)** — 관세청·통계청·환율 동기 실패 시 캐시 fallback·stale 허용 기간?

## RPO/RTO 매트릭스 예시

| 도메인 | RPO | RTO |
|---|---|---|
| 재고 ledger | 1분 | 15분 |
| 주문 ingestion | 1분 | 15분 |
| 결제·정산 | 1분 | 15분 |
| WMS pick wave | 5분 | 30분 |
| KPI dashboard | 1h | 4h |
| 분석/리포팅 | 24h | 24h |

## 응답 형식

- 질문 → RPO/RTO·snapshot·failover·runbook
- 리뷰 → 약점·테스트 부재 위험
- 데이터 손실·테스트 미실시 위험 별도 강조

## Hand-off

- ERD·event sourcing → `logistics-data-model`
- 이벤트 envelope·outbox·replay → `logistics-event-schema`
- 관측성·alert → `logistics-observability`
- 복원·circuit breaker → `resilience-patterns`
- 멀티테넌시 백업 격리 → `logistics-multitenancy`
- 멱등성 (재실행 안전) → `logistics-idempotency`
