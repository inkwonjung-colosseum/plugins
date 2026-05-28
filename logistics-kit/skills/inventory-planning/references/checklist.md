# inventory-planning 도메인 참조

## 활용 시점

- 설계 자문: 안전재고 산식, ROP·EOQ·(s,S)·base-stock·min-max·kanban 정책, ABC-XYZ 세그먼테이션, MEIO 전략 수립
- 코드·정책 리뷰: `safety_stock`, `rop`, `eoq`, `min_max`, `base_stock`, `s_s_policy`, `kanban`, `abc_xyz`, `meio`, `days_of_supply`, `gmroi`, `carrying_cost` 식별자가 보일 때
- 운영·디버깅: 결품·잉여재고 동시 발생, 서비스 수준 미달, lead-time 변동성 미반영
- 사용자 발화 예: "안전재고 식", "ROP", "EOQ", "ABC-XYZ", "보충 정책", "MEIO"

## 점검 포인트

1. **세그먼테이션** — ABC(매출·이익·픽 빈도) × XYZ(수요 변동성), 9 셀별 정책 매트릭스 (AX: tight base-stock / CZ: review on demand)?
2. **서비스 수준 z** — 목표 sl(95/97/99/99.5%)별 z(1.645/1.881/2.326/2.576), 카테고리별 매트릭스?
3. **안전재고 σ** — `SS = z × √(L × σ_D² + D̄² × σ_L²)` (수요·리드타임 변동 결합), 수요 안정 시 `z × σ_D × √L` 단순화?
4. **ROP** — `ROP = D̄ × L + SS`, lead time 분포(평균·표준편차) 데이터 품질?
5. **EOQ** — `EOQ = √(2 × D × S / H)` (주문비 S, 보유비 H), 가격 할인·MOQ 제약 시 LCM 검토?
6. **lot sizing(다기간)** — Wagner-Whitin(최적) / Silver-Meal / POQ / FOQ / LFL — 수요·셋업비·보유비 매칭?
7. **(s,S) 정책** — s 이하 시 S로 보충, 주기적 vs 연속 review, calc 갱신 주기?
8. **base-stock / min-max / kanban** — A·고가 SKU base-stock, B/C min-max, kanban 2-bin 단순 — 매칭 가이드?
9. **MEIO(다단계)** — central DC + regional + store 단계별 push/pull 결정, postponement(완제품 → 반제품 보유) 전략?
10. **carrying cost** — 자본비(WACC)·창고·보험·진부화·shrinkage 합산, 연 25~35% 표준?
11. **days of supply / GMROI** — `DOS = inventory / daily_demand`, `GMROI = gross_margin / avg_inventory_cost` — 카테고리 비교?
12. **constraint-aware planning** — capacity(창고·운송·예산) constraint 하 allocation, 우선순위(SLA tier·이익·전략)?
13. **obsolescence reserve** — slow/dead stock 식별(N개월 무이동), 충당금 정책?

## 산식 요약

| 지표 | 산식 |
|---|---|
| 안전재고 (결합) | `z × √(L × σ_D² + D̄² × σ_L²)` |
| ROP | `D̄ × L + SS` |
| EOQ | `√(2 × D × S / H)` |
| DOS | `current_inventory / daily_demand` |
| GMROI | `annual_gross_margin / avg_inventory_at_cost` |
| Carrying cost % | (capital + storage + risk) / inventory_value |

## 응답 형식

- 질문 → 표준 산식·세그먼테이션·정책 매트릭스
- 리뷰 → 약점·위험·수정 제안 (필요 시 `file:line`)
- 결품 vs 잉여 트레이드오프 별도 강조

## Hand-off

- 수요 입력 (forecast / FVA / 정확도) → `demand-forecast`
- 발주 트리거·MOQ·supplier lead-time → `procurement-po`
- 멀티에셜론·시설 배치 → `network-design`
- 회전율·GMROI·DOS KPI → `logistics-kpi`
- 안전재고 슬로팅 위치 반영 → `slotting-putaway`
