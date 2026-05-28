# 표준 KPI 산식

## 운영 (operations)

| KPI | 산식 | 주의 |
|---|---|---|
| OTIF | `on_time_and_in_full / total_orders` | On-Time과 In-Full을 *함께* 만족(AND). |
| Fill Rate | `lines_filled / lines_ordered` (line fill) 또는 `units_filled / units_ordered` (unit fill) | 라인/단위/주문 fill 3종 구분. |
| 재고 회전율 | `COGS / avg_inventory` (annualized) | 평균재고 = (기초+기말)/2 또는 일평균 중 명시. |
| 리드타임 | `시점B - 시점A` | A/B 정의(주문접수~출고 vs 출고~도착) 명시. |
| Picking Accuracy | `correct_lines / total_lines_picked` | 라인 vs 수량 단위 구분. |
| Perfect Order Rate | OTIF × Damage-Free × Correct Docs | 곱셈이라 작은 결함도 큰 영향. |
| 적재율 | `loaded_volume / capacity` (체적/중량/pallet) | 단위 일치 필수. |
| Order cycle time | `shipped_at - order_received_at` | 처리 속도 |
| Dock-to-stock time | `putaway_complete - dock_arrival` | 입고 효율 |
| Cube utilization | `used_volume / capacity_volume` | 창고·차량 |

## 노동·생산성 (labor)

| KPI | 산식 | 주의 |
|---|---|---|
| UPH | `units_handled / actual_work_hours` | 휴게·교육·미팅 제외 |
| Lines per hour | `lines_picked / actual_work_hours` | 라인 정의 일관 |
| Direct/Indirect ratio | `direct_labor_hours / total_labor_hours` | direct: pick/pack/loading |
| Engineered SAH | 목표 표준 시간 vs 실제 | MOST/MTM 분석 기반 |
| 결근율 | `no_show_days / scheduled_days` | shift별 분리 |
| 30/60/90일 이탈률 | `terminated / hired` | 신규 인력 retention |

## 정확도·shrinkage

| KPI | 산식 | 주의 |
|---|---|---|
| IRA (위치) | `correct_locations / counted_locations` | location 기준 |
| IRA (수량) | `correct_units / counted_units` | unit 기준 |
| Shrinkage % | `lost_value / total_inventory_value` | 분실/파손/조정 |
| Damage rate | `damaged_units / shipped_units` | 출고 시점 기준 |

## 운송·last-mile

| KPI | 산식 | 주의 |
|---|---|---|
| OTP (on-time pickup) | `on_time_pickups / total_pickups` | 캐리어 scorecard |
| OTD (on-time delivery) | `on_time_deliveries / total_deliveries` | 화주 SLA |
| First-attempt delivery | `delivered_first_attempt / total_attempts` | 라스트마일 효율 |
| Cost-per-stop | `total_cost / stops` | 비용 효율 |
| Stops-per-hour | `stops / driver_hours` | 노동 생산성 |
| Dwell time | `dock_departure - gate_in` | 야드 효율 |
| Route adherence | `actual_route_match_planned / total_routes` | 라우팅 충실도 |
| Empty mile % | `empty_distance / total_distance` | 적재 효율 |
| ETA accuracy | `|actual - ETA| ≤ threshold` 비율 | threshold 정의 |

## 수요예측·계획

| KPI | 산식 | 주의 |
|---|---|---|
| MAPE | `mean(|actual - forecast| / actual)` | zero·near-zero 폭주 |
| WMAPE | `sum(|a - f|) / sum(a)` | volume 가중, 권장 |
| sMAPE | `mean(|a-f| / ((|a|+|f|)/2))` | symmetric [0,2] |
| Bias | `mean(forecast - actual)` | + 과대, - 과소 |
| Tracking signal | `cumulative_bias / MAD` | ±4 초과 시 재검토 |
| FVA | `Δ(MAPE) by step` | naive→stat→human→consensus |
| Days of Supply | `current_inventory / daily_demand` | 안전재고 별도 |
| GMROI | `annual_gross_margin / avg_inventory_at_cost` | 카테고리 비교 |
| Carrying cost % | `(capital + storage + risk) / inventory_value` | 25~35% 표준 |
| Safety stock | `z × √(L × σ_D² + D̄² × σ_L²)` | 결합 변동성 |
| ROP | `D̄ × L + SS` | 발주점 |
| EOQ | `√(2 × D × S / H)` | 주문비 S·보유비 H |

## 안전·품질

| KPI | 산식 | 주의 |
|---|---|---|
| LTIR | `lost_time_injuries × 200,000 / employee_hours` | OSHA 기준 |
| TRIR | `total_recordable × 200,000 / employee_hours` | OSHA 기준 |
| Near-miss ratio | `near_miss / total_incidents` | 안전 문화 |
| PIT 인증 갱신율 | `certified / required` | 만료 알림 |

## ESG·탄소

| KPI | 산식 | 주의 |
|---|---|---|
| gCO₂e/tkm | `emission_g / (weight_t × distance_km)` | GLEC framework |
| Load factor | `actual_weight / max_capacity` | 적재율 |
| Empty mile CO₂ | empty distance × factor | scope 3 cat 4/9 |
| Recycled packaging % | `returned_packaging / total_packaging` | 회수 포장재 |

## 정산·3PL

| KPI | 산식 | 주의 |
|---|---|---|
| SLA penalty rate | `penalty / contract_value` | 계약별 차이 |
| 3PL true-up Δ | `actual - estimate` | 월간 차이 |
| Storage rate utilization | `chargeable_cube / contracted_cube` | cost-plus 계약 |
| Detention/demurrage cost | per day per trailer/container | 협상 지표 |

## 회수·traceability

| KPI | 산식 | 주의 |
|---|---|---|
| Mock recall completion time | start → all-units-located | ISO 22005 SLA |
| Recall completeness % | `recovered / shipped` | class별 차등 |
| Repeat recall rate | per category | CAPA 효과 |

## 관측성·플랫폼

| KPI | 산식 | 주의 |
|---|---|---|
| Availability (SLI) | `success_req / total_req` | 28d rolling |
| Latency p99 | 99th percentile | 단위 명시 |
| Error budget | `1 - SLO` | 소진 시 deploy 동결 |
| Event lag p95 | producer → consumer | 이벤트 streaming |
| Webhook delivery success | `delivered_2xx / total_sent` | 캐리어·채널 |
