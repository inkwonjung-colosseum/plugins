# wms-inventory 도메인 참조

## 활용 시점

- 설계 자문: 재고 모델·차감 정책·ATP 정의 수립
- 코드·스키마 리뷰: `inventory`, `stock`, `picking`, `packing`, `putaway`, `lot`, `serial`, `bin`, `location`, `cycle_count`, `safety_stock`, `atp`, `reserved` 식별자가 보일 때
- 운영·디버깅: 음수 재고, 이중 차감, lot 추적, 차이 조사
- 사용자 발화 예: "재고 차감 시점", "음수 재고 방지", "lot 추적", "안전재고 식", "출고 시점"

## 점검 포인트

1. **재고 차감 시점** — 주문 접수 vs 피킹 완료 vs 출고 확정 중 어디서 감소하는지 명시되어 있나? 시점 변경 시 ATP 계산도 같이 바뀌어야 한다.
2. **음수 재고 방지** — DB 레벨 제약(check constraint) 또는 application 레벨 락(SELECT FOR UPDATE) 중 어느 쪽으로 보호되나?
3. **lot/serial 추적** — FIFO/LIFO/FEFO 정책이 코드와 일치하나? expiry date 우선순위가 lot 단위로 잠겨있나?
4. **location 이동** — 출발/도착 location 둘 다 트랜잭션 한 단위로 처리되나? 부분 실패 시 보상 트랜잭션 정의?
5. **예약(reserved) vs 가용(available)** — `available = on_hand - reserved - allocated` 식이 모든 호출자에서 동일하게 쓰이나?
6. **cycle count** — 실재고 차이 발생 시 조정 분개(adjustment) 이력이 audit log에 남나?

## 응답 형식

- 질문 → 표준 정의·트레이드오프·권장 패턴
- 리뷰 → 약점·위험·수정 방향 (필요 시 `file:line`)
- 회색 영역은 *추가 질문 리스트*로 분리

## Hand-off

- TMS 라우팅/운임 → `tms-routing`
- 반품 흐름 → `returns-rma`
- ERD 설계·마이그레이션 → `logistics-data-model`
- 차감 멱등성 → `logistics-idempotency`
