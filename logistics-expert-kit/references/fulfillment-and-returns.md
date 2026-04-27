# Fulfillment and Returns

풀필먼트는 주문이 접수되어 고객에게 전달되기까지의 end-to-end 흐름입니다. 반품은 reverse logistics로 별도 흐름을 갖지만, 재고 가용성, 고객 경험, 비용에 직접 영향을 줍니다.

## Fulfillment Flow

- order capture: 주문 접수와 결제 또는 승인 상태 확인
- order release: 창고 작업 대상으로 주문을 넘기는 단계
- allocation: 주문에 재고를 배정
- pick/pack/ship: 창고 작업과 carrier 인계
- delivery confirmation: 배송 완료 또는 예외 상태 확인
- exception handling: backorder, split shipment, partial fulfillment, cancel, address issue

## Returns Flow

- RMA or return request: 반품 요청과 사유 수집
- pickup or drop-off: 회수 방식 결정
- inspection: 상품 상태와 수량 확인
- disposition: 재입고, 재포장, 수리, 폐기, 공급사 반송
- refund or exchange: 고객 처리와 정산

## Diagnosis Signals

- 주문 release 지연, allocation 실패, backorder 증가
- split shipment 증가로 배송비와 고객 문의 증가
- 반품 사유가 품질, 오배송, 주소, 단순 변심 중 어디에 집중되는지 불명확
- 반품 검수 지연으로 재판매 가능 재고 전환이 늦음

## Review Focus

풀필먼트와 반품은 고객 약속, 재고 정확도, 창고 capacity, carrier handoff가 만나는 영역입니다. 정책 변경 전에는 고객 영향, 비용 영향, 예외 처리, 데이터 정합성을 함께 검토해야 합니다.
