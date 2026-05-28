# channel-sync 도메인 참조

## 활용 시점

- 자문: connector 패턴, oversell guard, rate-limit 전략, SKU 매핑, 주문 ingestion 멱등성 수립
- 코드·API 리뷰: `channel`, `marketplace`, `shopify`, `amazon`, `coupang`, `naver`, `smartstore`, `gmarket`, `eleven_st`, `oversell`, `inventory_sync`, `listing_sync` 식별자가 보일 때
- 운영·디버깅: oversell 발생, 채널 listing 잠금, rate-limit hit, 주문 ingestion 누락
- 사용자 발화 예: "옴니채널 재고", "Shopify connector", "Coupang 연동", "oversell 방지", "marketplace sync"

## 점검 포인트

1. **재고 노출 모델** — 단일 풀(channel ↔ shared inventory) vs 채널별 quota·할당, 우선순위 매트릭스?
2. **oversell guard** — 채널 inventory level publish 시점 lag·jitter, reserve pattern, 결제 직전 재검증, soft fail 정책?
3. **push vs pull** — 채널 webhook(push, near real-time) vs polling(pull, 안정), hybrid 정책?
4. **rate-limit·backoff** — 채널 API rate (Shopify 2 req/s burst, Amazon SP-API throttle) 매트릭스, 토큰 버킷, 적응형 backoff?
5. **SKU 매핑** — 내부 SKU ↔ 채널 listing ID, 변형(옵션·번들) 매핑, 분실·중복 방지?
6. **주문 ingestion 멱등성** — 채널 order_id 기반 dedup, 재시도 안전, 부분 수정·취소 처리?
7. **status code 정규화** — 채널별 주문 status를 canonical로 매핑(→ `track-trace` 유사), unknown fallback?
8. **listing 변경 sync** — 가격·재고·이미지·옵션 변경 sync 우선순위, 부분 실패 retry, rollback?
9. **반품·refund sync** — 채널 PG와 내부 RMA·환불 동기화(→ `returns-rma`), 양방향 status 매트릭스?
10. **catalog 다중 채널 운영** — 채널별 카테고리 매핑·금지 SKU·VAT, country-of-origin 표기?
11. **분쟁(case·dispute) 워크플로** — 채널 dispute 발생 시 evidence·response, 시한, escalation?
12. **수수료·정산** — 채널별 수수료·정산 cycle·차감 항목(→ `logistics-settlement`)?
13. **인증·자격** — Amazon FBA·Coupang 로켓·네이버 도착보장 자격, 인증 만료 추적?

## 응답 형식

- 질문 → connector 패턴·oversell guard·rate-limit·매핑
- 리뷰 → 약점·oversell·rate-limit 위험
- oversell·rate-limit 위반·dispute 시한 별도 강조

## Hand-off

- 주문 수신 후 OMS → `oms-fulfillment`
- 재고 ATP·차감 → `wms-inventory`
- 멱등성/dedup → `logistics-idempotency`
- tenant 격리·quota → `logistics-multitenancy`
- 채널 정산·수수료 분개 → `logistics-settlement`
- 추적·고객 알림 → `track-trace`
- 데이터 보안·SCC → `data-privacy-logistics`
