# Logistics Domain Map

이 문서는 범용 물류 이슈를 분류하기 위한 지도입니다. 특정 조직의 운영 방식이 아니라, 물류 대화를 빠르게 구조화하기 위한 공통 범주입니다.

## Core Domains

- **Warehouse operations**: receiving, putaway, replenishment, picking, packing, shipping, cycle count, location control.
- **Transportation**: mode, carrier, route, dispatch, pickup, delivery, lead time, cutoff, freight cost, claims.
- **Inventory**: on-hand quantity, available quantity, allocation, safety stock, reorder point, stockout, overstock, inventory accuracy.
- **Fulfillment**: order capture, release, wave/batch, split shipment, backorder, partial fulfillment, delivery promise.
- **Returns**: RMA, pickup, inspection, disposition, restock, refurbish, scrap, refund, exchange.
- **Cross-border / trade / customs**: import/export direction, origin, destination, Incoterms, HS code, dangerous goods, customs documents, sanctions review.
- **Metrics**: service level, reliability, speed, cost, productivity, quality, inventory health.
- **Risk**: bottleneck, exception handling, data integrity, customer impact, compliance review, cutover risk.

## Intake Questions

- 어떤 흐름인가: 입고, 보관, 주문, 피킹, 출고, 배송, 반품 중 어디인가?
- 어떤 증상인가: 지연, 오류, 비용 증가, 품절, 과재고, 클레임, 고객 불만 중 무엇인가?
- 어떤 시스템이 관련되는가: WMS, TMS, OMS, ERP, carrier portal, marketplace, spreadsheet 중 무엇인가?
- 국제운송인가: 출발국, 도착국, 수출입 방향, Incoterms, HS code, 위험물, 통관 서류가 관련되는가?
- 어떤 데이터가 있는가: order count, SKU count, inventory count, scan history, delivery status, cost, exception reason.
- 어떤 결정을 내려야 하는가: 원인 파악, KPI 정의, 정책 변경, 프로세스 개선, 전문 검토 필요 여부.

## Routing

- 범위가 흐리면 `logistics-scope`.
- 증상과 원인 후보가 필요하면 `logistics-diagnose`.
- 지표, 계산식, 해석 기준이 필요하면 `logistics-metrics`.
- 변경안, 정책, cutover, 고객 영향이 있으면 `logistics-risk`.
