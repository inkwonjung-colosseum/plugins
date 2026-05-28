# resilience-patterns 도메인 참조

## 활용 시점

- 자문: circuit breaker·bulkhead·timeout·retry budget·degradation 패턴 정책 수립
- 코드·정책 리뷰: `circuit_breaker`, `bulkhead`, `timeout`, `retry`, `backoff`, `jitter`, `hedged_request`, `fallback`, `degradation`, `chaos`, `retry_budget` 식별자/문서 등장 시
- 운영·인시던트: retry-storm, 외부 의존성 cascading failure, 부분 장애 확산, latency 증가
- 사용자 발화 예: "circuit breaker", "bulkhead", "retry storm", "hedged request", "chaos engineering"

## 점검 포인트

1. **timeout 매트릭스** — 호출 별 RPC·DB·외부 API timeout 명시, 부모 timeout < 자식 합산 보장(timeout budget)?
2. **circuit breaker** — failure rate·slow rate 임계, open · half-open · close 상태 전이, per-host vs per-route 단위?
3. **bulkhead** — thread pool/semaphore 격리, 의존성별 분리, full pool에서 fail-fast?
4. **hedged request** — p99 단축 위한 중복 호출, idempotent endpoint에만 적용, 한쪽 응답 시 다른 쪽 cancel?
5. **exponential backoff + jitter** — base × 2^attempt + jitter, max 캡, retry-after header 존중?
6. **retry budget** — 전체 호출 대비 retry 비율(10%) 한도, 초과 시 차단?
7. **idempotency 결합** — 부작용 API는 멱등성 키 없이 retry 금지(→ `logistics-idempotency`)?
8. **degradation·fallback** — 외부 의존 장애 시 cache · stale · default · 부분 기능 disable 정책?
9. **load shedding** — 큐 깊이·CPU·메모리 임계 시 4xx (429) 빠른 거절, priority 큐?
10. **chaos engineering** — 정기 game day, 의존성 차단·지연·실패 주입, 결과 KPI?
11. **DNS·DR routing** — health-check failover, multi-region routing, anycast?
12. **rate-limit 클라이언트 측** — 외부 service rate-limit 준수, token bucket·leaky bucket?
13. **graceful shutdown** — SIGTERM → drain → close, in-flight req 완료 보장?

## 패턴 결정 트리

```
외부 의존성 호출?
├─ idempotent → retry + backoff + jitter (retry budget 적용)
└─ non-idempotent → idempotency-key + 최대 1회 retry only
실패 임계 도달?
├─ circuit-open → fallback (cache/stale/default)
└─ half-open → 시험 호출 (1건) → 결과 따라 close 또는 open
의존성 그룹 격리 필요?
└─ bulkhead (별도 thread pool / semaphore)
지연 단축 필요?
└─ hedged request (idempotent + cancel)
```

## 응답 형식

- 질문 → 패턴 결정 트리·타임아웃·예산
- 리뷰 → 약점·retry-storm·cascading failure 위험
- 부적절한 retry·timeout 누락 별도 강조

## Hand-off

- 멱등성·dedup → `logistics-idempotency`
- bulk·chunking → `bulk-operations`
- 관측성·SLO → `logistics-observability`
- DR·region failover → `logistics-dr`
- 외부 API rate-limit → `channel-sync`/`carrier-edi`
- saga 보상 → `logistics-saga`
