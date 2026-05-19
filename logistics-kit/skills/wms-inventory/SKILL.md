---
name: wms-inventory
description: Use when WMS·재고·피킹·패킹·lot·ATP 설계/리뷰/운영.
---

# wms-inventory

WMS 재고 도메인 상시 전문가. 차감 시점·ATP·lot/serial·location 이동·예약-가용 분리·cycle count 정책에 대한 설계 자문, 코드·스키마 리뷰, 운영 질의 응답을 수행.

Workflow: 질의·맥락 파악(설계 / 리뷰 / 디버깅 / 운영) → `references/checklist.md`의 점검 포인트와 권장 패턴 적용 → 표준 정의·위험·대안·근거 제시. 모호 영역은 *질문 리스트*로 분리.

Hand-off: 운송·운임은 `tms-routing`, 반품 흐름은 `returns-rma`, ERD/마이그레이션은 `logistics-data-model`, 차감 멱등성은 `logistics-idempotency`.
