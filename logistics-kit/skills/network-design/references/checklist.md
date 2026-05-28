# network-design 도메인 참조

## 활용 시점

- 설계 자문: 시설 위치·sourcing·postponement·DRP·modal mix·시나리오 평가 수립
- 모델·정책 리뷰: `facility_location`, `p_median`, `mip`, `sourcing`, `postponement`, `drp`, `network_optimization`, `scenario`, `flow` 모델/문서 등장 시
- 운영·시뮬레이션: 신규 DC 검토, M&A 통합, capacity 확장 ROI, 외주 vs 자가 결정
- 사용자 발화 예: "네트워크 최적화", "DC 위치", "sourcing 의사결정", "postponement", "what-if"

## 점검 포인트

1. **문제 유형** — 단일 시설 위치(p-median·p-center) / 다중 시설(MILP·set covering) / 흐름 최적화(transshipment·max-flow·min-cost-flow) — 매칭?
2. **input 데이터** — 수요(예측 vs 실적), 시설 후보·고정비·변동비, lane 운임, capacity, lead-time, 세금·incentive?
3. **목적함수** — 총 비용(시설+운송+재고+세금) vs 서비스 수준(N% 인구 24h 이내) vs 다목표(가중)?
4. **제약** — capacity / 단일 sourcing / max distance / SLA / hazmat·온도 호환·정치(노동·법규)?
5. **postponement 전략** — 완제품 vs 반제품 보유, 후가공(라벨·번들) 위치, customization 시점 결정?
6. **sourcing 의사결정** — single vs dual·multi, supplier capacity·risk·lead-time, near-shore vs offshore 트레이드오프?
7. **DRP(distribution requirements planning)** — central DC → regional → store 다단계 push, BOM 폭발 유사 흐름·재계산 주기?
8. **mode/modal mix** — air·ocean·rail·truck 선택 룰(가치/무게·SLA·CO₂), CO₂ shadow price 반영?
9. **scenario·what-if** — base / upside / downside / disruption(사이트 닫힘·캐리어 파업·관세 인상) — 평가 매트릭스?
10. **재고-운송 트레이드오프** — 시설↑·재고↑·운송↓ vs 시설↓·재고↓·운송↑, EOQ-frequency 연계?
11. **세금·관세·incentive** — 자유무역지역·보세창고·세금 우대 zone, 효과 시뮬레이션?
12. **solver·tool** — Gurobi·CPLEX·OR-Tools·SCIP·Anaplan·Llamasoft, 규모별 매칭?
13. **민감도 분석** — 주요 input 변동 시 솔루션 안정성, scenario weighted optimal?

## 응답 형식

- 질문 → 문제 유형 분류·목적함수·제약·KPI
- 리뷰 → 모델 가정·input 품질·결과 해석 위험
- 정치/사회적 제약·세금 변경 위험 별도 강조

## Hand-off

- 재고 정책·MEIO → `inventory-planning`
- 수요 입력 → `demand-forecast`
- S&OP·전략 통합 → `sop-ibp`
- 운임 모델 → `vrp-rating-engine`
- 운임 정산·세금 → `logistics-settlement`
- 탄소 회계 (Scope3·GLEC) → `sustainability-carbon`
