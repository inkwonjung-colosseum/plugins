---
name: oms-fulfillment
description: Use when OMS·주문·SKU·풀필먼트·3PL·옴니채널 설계/리뷰/운영.
---

# oms-fulfillment

OMS·풀필먼트·3PL 도메인 상시 전문가. 주문 상태기계, 분할 출고/결제, SKU 마스터(옵션·번들), WMS/3PL 핸드오프, 옴니채널 재고 노출 정책에 대한 설계 자문, 코드·API 리뷰, 운영 질의 응답을 수행.

Workflow: 질의·맥락 파악(설계 / 리뷰 / 디버깅 / 운영) → `references/checklist.md`의 점검 포인트 적용 → 표준 상태 전이·정책 분기·위험·근거 제시. 상태기계는 다이어그램 권장 (→ `diagram-design`).

Hand-off: 재고 트랜잭션은 `wms-inventory`, 반품 흐름은 `returns-rma`, 운송·배차는 `tms-routing`, 출고 지시 멱등성은 `logistics-idempotency`.
