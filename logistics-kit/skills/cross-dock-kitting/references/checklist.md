# cross-dock-kitting 도메인 참조

## 활용 시점

- 설계 자문: cross-dock 매칭 규칙, kit BOM 구조, VAS 워크플로, 자재 reserve 정책 수립
- 코드·스키마 리뷰: `cross_dock`, `flow_through`, `kit`, `bom`, `kit_parent`, `kit_child`, `vas`, `assembly`, `kitting_order`, `giftwrap`, `bundle` 식별자가 보일 때
- 운영·디버깅: cross-dock 미매칭 화물 적치, BOM 폭발 누락, kit 결품, VAS 처리 지연
- 사용자 발화 예: "cross-dock 매칭", "kit BOM", "VAS 작업", "사전조립", "번들 SKU"

## 점검 포인트

1. **cross-dock 매칭 규칙** — ASN/PO와 대기 주문의 매칭 윈도우(시간·SKU·수량), opportunistic(우연 매칭) vs planned(사전 지정) 분기?
2. **flow-through 미매칭 처리** — 매칭 실패 시 putaway 회귀 정책, 임시 holding 위치, escalation 시한?
3. **kit BOM 구조** — 부모-자식 다단계 vs 단층, 자식 SKU 재고 차감 시 부모 재고 자동 산출 vs 명시적 production order?
4. **사전조립(pre-kit) vs 주문조립(make-to-order)** — 결정 기준(수요 안정성·자재 회전·VAS 시간), 사전조립분 재고 회전 모니터링?
5. **kit production order 멱등성** — 동일 주문에 대한 kit 생성 N회 호출 = 1회 효과? `production_order_id` unique?
6. **VAS 작업 유형 매트릭스** — giftwrap, insert(전단·쿠폰), 라벨링(price tag·country-of-origin), 번들 포장, 펌웨어 업데이트 등 각각 SOP·시간 표준?
7. **자재 reserve** — VAS 부자재(박스·리본·insert) 재고 차감 시점, ATP 영향, 부족 시 분기?
8. **lot/expiry 결합** — kit에 포함된 각 자식 SKU의 lot·expiry 추적 정책, kit 단위 expiry 결정(최단)?
9. **VAS 매출/원가 분개** — VAS 단가가 매출에 가산되나 vs 원가 흡수? 화주별 정산 매트릭스?
10. **재작업(rework)·해체(disassemble)** — kit 해체 시 부품 재고 복원 정책, 손실(소모품) 처리?

## 응답 형식

- 질문 → cross-dock 매칭 규칙·BOM 정합성·VAS 워크플로
- 리뷰 → 약점·위험·수정 제안 (필요 시 `file:line`)
- 자재 부족·해체 손실 위험 별도 강조

## Hand-off

- 재고 트랜잭션 자체 → `wms-inventory`
- 출고 sequencing → `oms-fulfillment`
- 작업 큐(컨베이어·소터) → `wcs-mhe`
- VAS 매출/원가 분개 → `logistics-settlement`
- 식약처/원산지 라벨링 → `logistics-compliance`/`haccp-food-safety`
