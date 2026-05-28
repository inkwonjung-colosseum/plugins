# logistics-settlement 도메인 참조

## 활용 시점

- 설계 자문: 차주·3PL 정산 산식, 부대비용 분류, debit/credit note, ERP 분개 매핑 수립
- 코드·정책 리뷰: `settlement`, `payout`, `invoice`, `debit_note`, `credit_note`, `sla_penalty`, `journal_entry`, `accounting` 식별자가 보일 때
- 운영·감사: 정산 차이, 분개 누락, SLA 위약금 미적용, 부가세 분리
- 사용자 발화 예: "차주 정산", "월말 정산서", "SLA 위약금", "부대비용 청구", "분개 매핑"

## 점검 포인트

1. **정산 베이스 산식** — 운임 중 차주 분배 portion? 부대비용 항목별 100%/분담 정책 명시?
2. **부대비용 분류** — 통행료/대기료/할증/유류대납 각각 매출원가 vs 매출 차감 vs pass-through?
3. **debit/credit note** — 사후 조정(추가 청구/환급) 발생 시 원전표 수정 vs 별도 전표? 회계 정책 일치?
4. **SLA 보상** — OTIF 미달·손/파손·분실 보상 산식이 계약별 테이블화? effective date?
5. **3PL/위탁사 정산** — 위탁 수수료 산식, 정산 cycle(주/월), 발생일 vs 정산일 기준?
6. **회계 매핑** — 운임/부대비용/보상 각각 차변/대변 계정 매핑이 ERP에 일치? 부가세 분리?
7. **세금계산서/현금영수증** — 발행 시점·대상·종류 자동화 로직?
8. **3PL 계약 유형별 정산** — cost-plus(원가+마진) / transactional(건별) / gain-share / open-book / per-pallet·per-cube — 매트릭스, KPI 인센티브·차감, true-up cycle?
9. **storage·handling·VAS rate card** — 보관(occupancy/pallet/cube)·핸들링(입출고 건수)·VAS(라벨·번들·giftwrap)·peak surcharge — 등급별 단가 매트릭스?
10. **CBAM·탄소 levy** — 분개 매핑·tenant·국가별, embedded emission 보고 (→ `sustainability-carbon`)
11. **detention/demurrage 회계** — 자유시간 초과 일별 부과, 차주 보상 vs 화주 부과 분개 (→ `yard-dock`)
12. **insurance subrogation** — 화물 클레임 보험 구상권 처리 분개 (→ `cargo-claims-insurance`)
13. **shrinkage·loss 충당금** — IRA·도난·파손 분개 (→ `inventory-accuracy`)
14. **채널 marketplace 수수료** — Shopify·Amazon·Coupang·네이버 수수료·반품 차감 (→ `channel-sync`)
15. **세무 외화 환산** — 환율 스냅샷·통화별 분개, BAF/CAF 부대비용 (→ `localization-audit`/`freight-forwarding`)

## 응답 형식

- 질문 → 표준 정산 산식·분개 매핑·계약별 effective date
- 리뷰 → 분개 매핑 누락·회계 감사 리스크
- 외부 ERP 연동 매핑표 권고는 별도 표기

## Hand-off

- 운임 산식·차주 분배 base → `tms-routing`/`vrp-rating-engine`
- OTIF·KPI 산식 → `logistics-kpi`
- 통관·관세 분개 → `logistics-compliance`/`fta-origin`
- 정산 분쟁·보험 구상 → `cargo-claims-insurance`
- CBAM·Scope 3 분개 → `sustainability-carbon`
- 채널 수수료 → `channel-sync`
- 디텐션/디머리지 → `yard-dock`/`freight-forwarding`
- 결제 PG 멱등성 → `logistics-idempotency`
- 외화 환산·tenant 통화 → `localization-audit`
