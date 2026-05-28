# slotting-putaway 도메인 참조

## 활용 시점

- 설계 자문: 슬로팅 점수 산식, putaway 규칙, forward/reserve 비율, 보충 트리거 정책 수립
- 코드·스키마 리뷰: `slotting`, `putaway`, `replenishment`, `golden_zone`, `forward_pick`, `reserve_pick`, `abc_class`, `velocity_class`, `min_max`, `kanban` 식별자가 보일 때
- 운영·디버깅: pick 시간 증가, replenishment 누락으로 forward 결품, 혼적 위반, lot 격리 위반
- 사용자 발화 예: "슬로팅", "putaway 규칙", "재슬롯팅", "forward pick 보충", "ABC 존"

## 점검 포인트

1. **슬로팅 점수 산식** — 회전율(velocity) + 무게/부피 + 동시 픽 빈도(affinity) + 황금존 가산이 명시되어 있나? 가중치 변경 정책?
2. **ABC/velocity class** — 매출/픽 빈도 어느 쪽 기준? 분류 갱신 주기(주/월/분기)? 신제품 cold-start fallback?
3. **golden zone** — 인체공학 높이(허리~어깨, 약 0.7~1.5m) 픽 비율 목표? 부피·무게 제약과 충돌 해소 규칙?
4. **forward vs reserve pick** — forward 보유량 산식(lead time × peak demand × safety factor)? overflow 시 reserve 잔여?
5. **putaway 규칙 매트릭스** — 혼적 금지 SKU(위험물·식약처·콜드체인 분리), lot 단위 격리(`quarantine`/`hold`), expiry 우선 위치, 무거운 SKU 바닥 위치 규칙?
6. **replenishment 트리거** — min/max vs ROP vs kanban(2-bin)? 트리거 발화 후 작업지시까지 leadtime SLA?
7. **wave에서 replenishment 동기화** — wave release 전 forward 잔량 검증? 부족 시 wave 보류 정책?
8. **re-slotting 주기·트리거** — 분기/반기 정기 + ad-hoc 트리거(velocity 변동 N% 이상)? 이동 비용 vs 픽 절감 ROI 평가?
9. **mixed lot 위치 운영** — 동일 SKU 다른 lot이 같은 bin에 들어가나? FEFO 보장 위해 분리?
10. **위치 capacity 제약** — bin 용량(kg/m³/units) 마스터 정확? 초과 시 알림?

## 응답 형식

- 질문 → 표준 산식·정책 매트릭스·트레이드오프
- 리뷰 → 약점·위험·수정 제안 (필요 시 `file:line`)
- 재슬롯팅 ROI 평가는 별도 표기 (이동 비용·재교육 비용 vs 픽 절감)

## Hand-off

- 재고 트랜잭션 자체 → `wms-inventory`
- 자동화 작업 큐·소터 매핑 → `wcs-mhe`
- 회전율/픽 처리량 KPI → `logistics-kpi`
- ABC-XYZ 세그먼테이션 + safety stock → `inventory-planning`
