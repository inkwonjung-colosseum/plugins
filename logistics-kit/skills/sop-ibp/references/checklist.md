# sop-ibp 도메인 참조

## 활용 시점

- 설계 자문: S&OP/IBP 5-step cadence, consensus forecast 절차, scenario planning, KPI deck, 의사결정 권한 매트릭스
- 프로세스·툴 리뷰: `s_op`, `ibp`, `consensus`, `cadence`, `scenario`, `demand_review`, `supply_review`, `pre_sop`, `exec_review`, `balance_meeting` 식별자/문서 등장 시
- 운영·디버깅: 부서 사이로 어긋남(forecast ≠ commit), 월간 사이클 늦음, exec review 결정 미이행
- 사용자 발화 예: "S&OP", "IBP", "consensus", "scenario planning", "exec review"

## 점검 포인트

1. **5-step cadence** — Product review(NPI/EOL) → Demand review(consensus) → Supply review(capacity·재고) → Pre-S&OP(reconcile gap) → Exec S&OP(승인·결정) — 표준 일정·소요일?
2. **input·output 표준** — 각 단계 input(forecast·재고·capacity·재무 plan) / output(consensus number·gap list·decision log) 정의?
3. **consensus forecast** — sales/marketing/finance/ops 인풋 통합 절차, override 권한·근거 기록, FVA 측정(→ `demand-forecast`)?
4. **scenario planning** — base/upside/downside, 트리거(promo·신제품·외부 충격), 대응 플레이북?
5. **demand-supply balancing** — 결품 시(공급 부족) 우선순위(고객 SLA·이익·전략), 잉여 시(수요 약세) promo·할인·EOL 결정?
6. **결정 권한 매트릭스** — capacity 변경 / capex / 외주 / NPI 일정 — 누가 어느 수준에서 결정? exec→이사회 escalation?
7. **KPI deck 표준** — forecast accuracy(WMAPE·bias), service level, days of supply, capacity utilization, OTIF, P&L impact?
8. **bullwhip 완화** — 정보 공유(POS·재고), lot size 축소, CPFR, 가격 안정(EDLP), 리드타임 단축, ration 알고리즘?
9. **IBP vs S&OP 차이** — IBP는 재무 통합·전략 horizon(18-36개월), S&OP는 운영(3-18개월) — 매칭 가이드?
10. **digital integration** — 단일 SoR(SAP IBP·o9·Anaplan·Kinaxis)·in-house, 데이터 자동화, what-if 시뮬레이션?
11. **회의 운영** — 어젠다·필수 참석자·결정 vs 정보 공유 구분, decision log immutability?

## 응답 형식

- 질문 → 5-step input/output·결정 매트릭스·KPI deck
- 리뷰 → 약점·위험·수정 제안 (필요 시 `file:line`)
- 의사결정 미이행·부서 사일로 위험 별도 강조

## Hand-off

- 수요 모델·정확도 → `demand-forecast`
- 재고 정책·MEIO → `inventory-planning`
- 발주·supplier capacity → `procurement-po`
- 시설·네트워크 capacity → `network-design`
- 노동 capacity → `labor-mgmt`
- KPI deck → `logistics-kpi`
