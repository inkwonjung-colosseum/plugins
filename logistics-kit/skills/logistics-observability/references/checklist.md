# logistics-observability 도메인 참조

## 활용 시점

- 자문: SLO/SLI/error budget 정의, structured log 필드 표준, trace 전파, alert 디자인 수립
- 코드·정책 리뷰: `slo`, `sli`, `error_budget`, `otel`, `opentelemetry`, `trace`, `span`, `structured_log`, `correlation_id`, `causation_id`, `red`, `use`, `runbook` 식별자/문서 등장 시
- 운영·인시던트: alert 폭주, root cause 추적 실패, 비즈니스 일탈 미감지, on-call burnout
- 사용자 발화 예: "SLO", "error budget", "trace 전파", "alert 임계", "runbook"

## 점검 포인트

1. **SLI 후보** — 가용성(2xx 비율) / 지연(p99) / 정확도(주문→출고 OTIF) / 일관성(이벤트 lag) / 콜드체인 일탈률 — 비즈니스 vs 기술 균형?
2. **SLO 임계·기간** — 28d rolling, 99.9% / 99.95% 매트릭스, 카테고리별 차등?
3. **error budget** — `1 - SLO`, 소진 시 deploy 동결·feature 차단 정책?
4. **trace 표준** — W3C traceparent, correlation_id(요청 단위) + causation_id(직전 이벤트) + tenant_id + business_id(order/shipment) 전파?
5. **structured log 필드** — timestamp(UTC ISO8601)·level·service·trace_id·span_id·tenant_id·user_id(마스킹)·event_type·payload(PII 제외)?
6. **PII 분리** — 로그·trace에 raw PII 금지, 토큰화·필드 마스킹·별도 vault?
7. **RED 방법(서비스 단위)** — Rate(req/s) / Errors(rate) / Duration(p50·p95·p99)?
8. **USE 방법(자원 단위)** — Utilization / Saturation / Errors — DB·Kafka·캐시 매트릭스?
9. **business metric** — OTIF·picking accuracy·콜드체인 break·shrinkage — alert + dashboard?
10. **alert 분류** — page(즉시 호출) / ticket(영업시간) / log(추적) 분류, alert fatigue 방지(deduplication·flapping suppression)?
11. **runbook** — 각 alert별 진단 단계·완화·escalation, 30분 내 1차 조치 가이드?
12. **on-call 운영** — rotation·handoff·post-incident review(PIR·blameless), SLI 회귀 추적?
13. **변경 추적** — deploy·feature flag·config 변경을 trace + alert와 결합, 변경 후 회귀 자동 감지?
14. **multi-tenant 모니터링** — 테넌트별 SLO·error budget, noisy neighbor 식별?

## 응답 형식

- 질문 → SLO/SLI 매트릭스·trace 표준·alert 임계
- 리뷰 → 약점·alert fatigue·PII 위험
- 비즈니스 일탈 미감지 위험 별도 강조

## Hand-off

- 이벤트 envelope·DLQ → `logistics-event-schema`
- 감사 로그 모델 → `logistics-data-model`
- 멱등성·dedup → `logistics-idempotency`
- 복원·DR → `logistics-dr`/`resilience-patterns`
- 비즈니스 KPI 정의 → `logistics-kpi`
- 보안·접근 로그 → `data-privacy-logistics`
