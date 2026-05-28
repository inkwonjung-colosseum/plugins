# procurement-po 도메인 참조

## 활용 시점

- 설계 자문: PO 상태기계, ASN 매칭, 3-way match 규칙, supplier scorecard, dual sourcing 정책 수립
- 코드·API 리뷰: `purchase_order`, `po`, `asn`, `goods_receipt`, `gr`, `three_way_match`, `supplier_scorecard`, `moq`, `mov`, `dual_source`, `lead_time` 식별자가 보일 때
- 운영·디버깅: 분할 입고 매칭 실패, 3-way match 자동화율 저조, 검수 불합격 처리 지연, supplier OTD 저조
- 사용자 발화 예: "PO 상태", "ASN 매칭", "3-way match", "supplier scorecard", "MOQ"

## 점검 포인트

1. **PO 상태기계** — draft → submitted → acknowledged → in-production → shipped(ASN) → received(GR) → invoiced → matched → paid → closed (역행·취소·partial 정책)?
2. **ASN 856 수신·매칭** — ASN 수신 시 PO 매칭(라인·수량·lot), 미매칭 시 hold, ASN 수정 처리?
3. **3-way match 룰** — PO vs GR vs Invoice 수량·단가·세금 허용 오차(tolerance), 자동 승인 vs 예외 워크플로?
4. **분할 입고** — partial shipment 처리(잔여 backorder), 분할 GR 단위 처리, ASN 다중 vs 통합?
5. **검수 불합격** — 입고 검수에서 불량 발견 시 returns to vendor(RTV) 워크플로, debit note 발행, 대체 보충 트리거?
6. **supplier scorecard** — OTD(on-time delivery), 품질(defect rate·DPPM), 가격·결제 준수, 응답성·CAPA — 가중 점수, 분기 평가?
7. **MOQ/MOV** — 최소 발주 수량/금액, EOQ와 충돌 시 정책(다음 주기로 이월·multi-PO 합산)?
8. **dual/multi sourcing** — primary·secondary 비율 할당, 재해·품질 이슈 시 자동 전환?
9. **lead-time variability** — supplier별 lead-time 평균·표준편차 추적, 안전재고 σ_L 반영(→ `inventory-planning`)?
10. **입고 예정 ATP** — open PO + ASN 수량을 ATP 계산에 반영?
11. **계약·가격 marker** — 계약 단가·effective date·MOQ tier, 가격 시뮬레이션·승인?
12. **공급사 onboarding** — 인증(ISO·KC·식약처), 결제 조건(net 30/60), 위탁 동의(개인정보·MSA)?
13. **분쟁·CAPA** — supplier 품질 이슈 → CAPA, evidence, time bar(시한)?

## 응답 형식

- 질문 → PO 상태 매트릭스·match 규칙·scorecard 산식
- 리뷰 → 약점·위험·수정 제안 (필요 시 `file:line`)
- 미매칭·OTD 저조·계약 위반 위험 별도 강조

## Hand-off

- 입고 트랜잭션 → `wms-inventory`
- 수요·안전재고 → `demand-forecast`/`inventory-planning`
- 결제·매입 분개 → `logistics-settlement`
- 국제 운송·관세 → `freight-forwarding`/`logistics-compliance`
- 통관 사전신고·이동 → `freight-forwarding`
- supplier OTD·품질 KPI → `logistics-kpi`
