# Warehouse Operations

창고 운영은 물리 흐름과 데이터 흐름이 동시에 맞아야 합니다. 일반적인 분석에서는 입고, 검수, 적치, 보충, 피킹, 패킹, 출고, 재고실사를 별도 단계로 보고 각 단계의 병목과 오류 가능성을 나눕니다.

## Common Concepts

- **Receiving**: 입고 예정, 도착, 검수, 수량 확인, 품질 확인.
- **Putaway**: 입고품을 보관 위치에 배치하고 시스템 재고를 갱신하는 단계.
- **Replenishment**: 피킹 위치 재고를 보충하는 단계. 부족하면 picking delay가 발생합니다.
- **Picking**: 주문 또는 작업 단위로 상품을 집품하는 단계. 위치, SKU, 수량 오류가 자주 발생합니다.
- **Packing**: 포장, 송장, 중량, 출고 검수. carrier handoff 전 품질 게이트입니다.
- **Shipping**: 출고 확정, carrier 인계, 배송 상태 연동.
- **Cycle count**: 재고 정확도를 유지하기 위한 반복 실사.

## Diagnosis Signals

- scan 누락, location mismatch, SKU alias, UOM 불일치
- wave release 지연, picking queue backlog, packing station capacity 부족
- cutoff 직전 주문 집중, carrier pickup miss, 출고 확정과 실제 인계 시점 차이
- inventory adjustment 증가, negative stock, unavailable stock 증가

## Review Focus

창고 이슈는 사람, 설비, layout, 시스템 데이터, carrier handoff를 함께 봐야 합니다. 단일 원인을 바로 확정하지 말고 증상별 확인 순서를 제시합니다.
