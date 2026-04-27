# Transportation

운송 분석은 mode, carrier, route, pickup, delivery promise, cost, claim을 분리해서 봅니다. 동일한 배송 지연이라도 창고 출고 지연, carrier pickup miss, hub delay, 라우팅 문제, 주소 오류의 대응은 다릅니다.

## Common Concepts

- **Mode**: parcel, LTL, FTL, ocean, air, rail, intermodal.
- **Carrier**: 운송 수행자. SLA, pickup window, surcharge, claim rule은 계약별로 다릅니다.
- **Cutoff**: 주문 또는 출고가 당일 처리 대상에 들어가기 위한 기준 시점.
- **Lead time**: order to ship, ship to deliver, end-to-end 등 측정 구간을 명확히 해야 합니다.
- **Status visibility**: pickup, in transit, out for delivery, delivered, exception, returned.

## Diagnosis Signals

- pickup scan 누락, manifest mismatch, carrier capacity limit
- zone별 lead time 증가, 특정 route 지연, 특정 carrier claim 증가
- surcharge 증가, re-delivery 증가, address correction 증가
- promised date와 actual delivery date의 정의 불일치

## Review Focus

운송 관련 결론은 계약, carrier SLA, 지역, 물량, 품목, 요율표에 민감합니다. 일반 물류 원칙은 원인 후보와 확인 데이터까지 제시하고, 정산이나 귀책은 회사별 확인 필요로 남깁니다.
