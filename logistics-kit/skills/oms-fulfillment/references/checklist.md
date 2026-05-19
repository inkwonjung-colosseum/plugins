# oms-fulfillment 도메인 참조

## 활용 시점

- 설계 자문: 주문 상태기계·분할 출고·SKU 마스터·옴니채널 정책 수립
- 코드·API 리뷰: `order`, `fulfillment`, `sku`, `bundle`, `3pl`, `shipping_label`, `order_status`, `allocation` 식별자가 보일 때
- 운영·디버깅: 상태 역행, 3PL ack 누락, 옴니채널 재고 oversell
- 사용자 발화 예: "주문 상태", "분할 배송", "번들 SKU", "3PL 연동", "옴니채널 재고"

## 점검 포인트

1. **주문 상태기계** — 상태 전이(approved→picked→shipped→delivered) 단방향? 취소/홀드(hold) 처리 가능 단계? 불법 전이 차단 코드?
2. **분할 주문/배송** — 부분 출고 시 잔여 수량 어디에 보관? 결제/환불 분할 단위 처리?
3. **SKU master** — 옵션(색상/사이즈)/번들이 별도 SKU vs 부모-자식 관계? 자식 SKU 재고 차감 일관 전파?
4. **WMS↔OMS 연동** — 출고 지시 후 ack 누락 재시도 정책? 멱등성 키는? (→ `logistics-idempotency`)
5. **3PL 핸드오프** — 외부 3PL 시스템 sync 주기, 실패 시 reconciliation 배치?
6. **옴니채널 재고** — 채널별 노출 vs 단일 풀(common pool) 정책 명확?

## 응답 형식

- 질문 → 표준 상태 전이·정책 분기·트레이드오프
- 리뷰 → 누락/위험·수정 권장 (필요 시 `file:line`)
- 상태기계는 다이어그램 권고 (→ `diagram-design`)

## Hand-off

- 재고 트랜잭션 자체 → `wms-inventory`
- 반품 흐름 → `returns-rma`
- 배차·운송 → `tms-routing`
- 출고 지시 멱등성 → `logistics-idempotency`
