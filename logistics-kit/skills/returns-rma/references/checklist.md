# returns-rma 도메인 참조

## 활용 시점

- 설계 자문: 반품 사유 코드·검수 판정·재입고·환불 트리거 정책 수립
- 코드·API 리뷰: `return`, `rma`, `refund`, `exchange`, `inspection`, `reverse_logistics`, `restock` 식별자가 보일 때
- 운영·디버깅: 환불-재고 복원 타이밍 충돌, 부분 반품 처리, 교환 흐름
- 사용자 발화 예: "반품 흐름", "환불 시점", "재입고 처리", "검수 후 폐기", "부분 반품"

## 점검 포인트

1. **반품 사유 코드** — 사유별 환불/교환/거절 분기가 정책표와 일치? 사유 추가 시 default fallback?
2. **검수 판정** — 양품(restock) / 불량(scrap/return-to-vendor) / 폐기(dispose) 3-way 분기가 inspection 워크플로에 반영?
3. **재고 복원 시점** — 반품 접수 vs 회수 완료 vs 검수 후 양품 판정 중 어디서 재고가 +되나? 가용재고 즉시 반영 정책?
4. **환불 트리거** — PG 환불 호출 시점이 검수 전/후/부분? 부분 환불 가능?
5. **교환(exchange)** — 신주문 발행 vs 동일 주문 SKU 교체? 차액·배송비·재고 처리?
6. **3PL 반품 핸드오프** — 외부 3PL 검수 결과 sync 주기/실패 보상?
7. **grading 매트릭스** — A/B/C/D/scrap 등급 결정 기준(외관·기능·박스·구성품), refurb·재유통 채널·polishing·재포장 비용 매트릭스?
8. **recall 연계** — 회수 명령 발동 시 RMA 흐름과 분리(→ `recall-traceability`), 강제 회수 vs 자율 반품, 환급 조건?
9. **B2B cargo claim 별도** — 소비자 RMA와 별도, 캐리어 과실 / 보험 / time bar (→ `cargo-claims-insurance`)
10. **reverse 운송 leg** — 픽업 스케줄(→ `last-mile-delivery`), retail drop-off 네트워크, RTS 사유 코드, locker 통한 반품?
11. **hazmat 반품 제약** — 위험물·약·식품·전기·배터리 반품 불가 SKU(→ `dangerous-goods`), 회수 운송 제약?
12. **개인정보** — 반품 화물의 수령 정보·환불 수단 PII 보관 (→ `data-privacy-logistics`)

## 응답 형식

- 질문 → 표준 정책 분기·타이밍 정의·트레이드오프
- 리뷰 → 정책 분기 누락·위험·권장
- 환불/재고 복원 *타이밍 충돌* 별도 강조

## Hand-off

- 순방향 주문 흐름 → `oms-fulfillment`
- 재고 트랜잭션 자체 → `wms-inventory`
- 환불 분개·SLA 보상 → `logistics-settlement`
- 회수·class 결정 → `recall-traceability`
- B2B cargo claim → `cargo-claims-insurance`
- 반품 운송 leg → `last-mile-delivery`/`carrier-edi`
- 위험물 반품 제약 → `dangerous-goods`
- 식약처/식품 회수 → `haccp-food-safety`/`pharma-gdp-serialization`
- 데이터 PII → `data-privacy-logistics`
