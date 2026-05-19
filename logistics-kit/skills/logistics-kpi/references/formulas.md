# 표준 KPI 산식

| KPI | 산식 | 주의 |
|---|---|---|
| OTIF | `on_time_and_in_full / total_orders` | On-Time과 In-Full을 *함께* 만족(AND). |
| Fill Rate | `lines_filled / lines_ordered` (line fill) 또는 `units_filled / units_ordered` (unit fill) | 라인/단위/주문 fill 3종 구분. |
| 재고 회전율 | `COGS / avg_inventory` (annualized) | 평균재고 = (기초+기말)/2 또는 일평균 중 명시. |
| 리드타임 | `시점B - 시점A` | A/B 정의(주문접수~출고 vs 출고~도착) 명시. |
| Picking Accuracy | `correct_lines / total_lines_picked` | 라인 vs 수량 단위 구분. |
| Perfect Order Rate | OTIF × Damage-Free × Correct Docs | 곱셈이라 작은 결함도 큰 영향. |
| 적재율 | `loaded_volume / capacity` (체적/중량/pallet) | 단위 일치 필수. |
