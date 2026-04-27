# Inventory

재고 분석은 수량 하나만 보지 않습니다. on-hand, available, reserved, allocated, damaged, in-transit, returned stock을 구분해야 합니다. 수량 정의가 다르면 같은 현상을 서로 다르게 해석합니다.

## Common Concepts

- **On-hand**: 물리적으로 보유한 재고.
- **Available**: 주문 할당 가능한 재고. 보류, 손상, 예약 수량은 제외될 수 있습니다.
- **Allocation**: 주문 또는 채널에 재고를 배정하는 단계.
- **Safety stock**: 수요 변동과 공급 변동에 대비한 완충 재고.
- **Reorder point**: 보충 주문을 시작하는 기준.
- **Inventory accuracy**: 시스템 수량과 실제 수량의 일치 정도.
- **Cycle count**: 전체 재고실사 대신 구간별 반복 실사로 정확도를 유지하는 방식.

## Diagnosis Signals

- stockout과 overstock이 동시에 발생
- 주문 가능 수량과 실제 피킹 가능 수량이 다름
- 특정 SKU, lot, location에서 adjustment 반복
- 입고 처리 지연으로 available 전환이 늦음
- 반품 재고 disposition이 늦어 판매 가능 재고가 줄어듦

## Review Focus

재고 이슈는 수요, 공급, 운영 처리 속도, 시스템 예약 정책이 함께 작동합니다. 지표를 설계할 때는 분모와 측정 시점을 명확히 하고, 공식 KPI나 정산 기준은 회사별 확인 필요로 둡니다.
