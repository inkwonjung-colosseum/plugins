# demand-forecast 도메인 참조

## 활용 시점

- 설계 자문: 모델 선택, 계층 reconciliation, promo lift, ensemble, 정확도 측정 체계 수립
- 코드·모델 리뷰: `forecast`, `croston`, `holt_winters`, `arima`, `ets`, `prophet`, `lightgbm`, `mape`, `wmape`, `bias`, `fva`, `cold_start`, `cannibalization`, `promo_lift` 식별자가 보일 때
- 운영·디버깅: 예측 정확도 하락, bias 누적, promo 미반영, 신제품 cold-start fail, hierarchical 불일치
- 사용자 발화 예: "수요예측", "Croston", "MAPE", "promo lift", "FVA", "신제품 예측"

## 점검 포인트

1. **모델 매칭 (수요 패턴별)** — 안정·계절(Holt-Winters/ETS) / 추세+계절(ARIMA·SARIMA) / 간헐·lumpy(Croston·SBA·TSB) / 외생변수(Prophet/LightGBM) — 분류 자동화?
2. **간헐 수요(intermittent) 판정** — ADI(평균 inter-arrival) ≥ 1.32 + CV² ≥ 0.49 = lumpy. 분류 후 Croston 계열 적용?
3. **신제품 cold-start** — analog product 매칭(속성·카테고리·가격), 도입곡선(Bass·Gompertz), 1차 launch 후 단계적 전환?
4. **promotion lift/cannibalization/halo** — base + lift 분해(인과·DID/regression), 카니발(다른 SKU 잠식)·halo(보완재 견인) 계수 추정?
5. **계층적 reconciliation** — top-down(총 → 분해) / bottom-up(SKU → 집계) / middle-out / MinT(분산 최적), 일관성 보장?
6. **ensemble** — 단순 평균 / 가중(역MAPE) / stacking, 모델 다양성·robustness 트레이드오프?
7. **정확도 지표** — MAPE / WMAPE(=weighted by volume, 권장) / sMAPE(zero 안정) / bias / tracking signal(누적 bias / MAD) — 리포트 단일 소스?
8. **FVA(Forecast Value Add)** — 단계(naive → stat → human → consensus) 별 정확도 ΔMAPE 측정, 음(-) 가산 시 단계 제거?
9. **백테스트·교차검증** — rolling origin, blocked time-series CV, train/test 분할, holdout 정책?
10. **외생변수** — 날씨·이벤트(설/추석/블프)·가격·재고 가용성·경쟁사 가격 — feature pipeline·data leakage 방지?
11. **계절성 처리** — 다중 계절(주간 + 연간), 이벤트 캘린더(설/추석/블프/광군제), 휴일 효과 분리?
12. **bias 모니터링** — SKU·카테고리별 bias 누적 시 alert, 자동 재학습 트리거?

## 산식 요약

| 지표 | 산식 | 주의 |
|---|---|---|
| MAPE | mean(|actual - forecast| / actual) | zero·near-zero에서 폭주 |
| WMAPE | sum(|actual - forecast|) / sum(actual) | volume 가중, 권장 |
| sMAPE | mean(|a-f| / ((|a|+|f|)/2)) | symmetric, [0,2] |
| bias | mean(forecast - actual) | + 과대, - 과소 |
| tracking signal | cumulative bias / MAD | ±4 초과 시 모델 재검토 |
| Croston | 별도 demand size·interval 두 시리즈 SES | intermittent 표준 |

## 응답 형식

- 질문 → 표준 모델·산식·정확도 매트릭스
- 리뷰 → 약점·위험·수정 제안 (필요 시 `file:line`)
- 데이터 누수·spec drift 위험 별도 강조

## Hand-off

- 안전재고·ROP·EOQ 적용 → `inventory-planning`
- S&OP 월간 cadence → `sop-ibp`
- 발주 트리거 → `procurement-po`
- 정확도 KPI 노출 → `logistics-kpi`
- 시즈널리티·이벤트 캘린더(타임존) → `localization-audit`
