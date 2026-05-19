# logistics-kpi 도메인 참조

## 활용 시점

- 설계 자문: KPI 정의·분모·시점·단위·타임존 결정, 신규 KPI 산식 제안
- 코드·쿼리 리뷰: `kpi`, `metric`, `otif`, `fill_rate`, `turnover`, `lead_time`, `picking_accuracy`, BI 쿼리/뷰 등장 시
- 운영·디버깅: 같은 KPI인데 리포트마다 값이 다른 경우, 월말 마감 차이
- 사용자 발화 예: "OTIF 계산", "회전율 산식", "리드타임 정의", "fill rate 분모", "지표 통일"

## 점검 포인트

1. **산식 단일 소스** — 같은 KPI를 BI 쿼리, 운영 대시보드, 리포트 PDF가 *다른 SQL*로 계산하지 않나? 공유 view/semantic layer?
2. **분모 정의** — 분모에 취소/반품 주문 포함? 테스트 주문 제외 필터?
3. **시점 기준** — 주문일 vs 출고일 vs 결제일 기준 집계. 월말 마감 시 차이.
4. **단위 일관성** — 라인 vs 단위 vs 주문이 한 리포트 안에 혼재되지 않나?
5. **타임존** — KST 마감 vs UTC 마감으로 일 단위 결과가 갈리지 않나? (→ `localization-audit`)
6. **벤치마크/타깃** — KPI에 목표치(SLA) 함께 노출되나?

## 응답 형식

- 질문 → 표준 산식(→ `formulas.md`)·분모·시점·단위 정의
- 리뷰 → KPI별 산식 일관성 매트릭스·차이 위치
- 추가 KPI 제안 시 표준 산식 함께 제시

## Hand-off

- 보상·정산 적용 → `logistics-settlement`
- 데이터 소스·집계 모델 → `logistics-data-model`
- 타임존·로케일 → `localization-audit`
