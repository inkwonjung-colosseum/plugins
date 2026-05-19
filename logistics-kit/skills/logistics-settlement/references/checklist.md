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

## 응답 형식

- 질문 → 표준 정산 산식·분개 매핑·계약별 effective date
- 리뷰 → 분개 매핑 누락·회계 감사 리스크
- 외부 ERP 연동 매핑표 권고는 별도 표기

## Hand-off

- 운임 산식·차주 분배 base → `tms-routing`
- OTIF·KPI 산식 → `logistics-kpi`
- 통관·관세 분개 → `logistics-compliance`
