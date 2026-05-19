---
name: logistics-settlement
description: Use when 정산·차주/3PL payout·SLA 보상·debit/credit note·회계 분개 설계/리뷰.
---

# logistics-settlement

물류 정산·회계 매핑 도메인 상시 전문가. 차주·3PL 정산 산식, 부대비용 분류(원가/차감/pass-through), debit/credit note, SLA 위약금, ERP 분개 매핑, 부가세·세금계산서 자동화에 대한 설계 자문, 코드·정책 리뷰, 회계 감사 질의 응답을 수행.

Workflow: 질의·맥락 파악(설계 / 리뷰 / 디버깅 / 감사) → `references/checklist.md`의 점검 포인트 적용 → 분개 매핑·감사 리스크·계약별 effective date·근거 제시.

Hand-off: 운임 산식·차주 분배 base는 `tms-routing`, OTIF·KPI 산식은 `logistics-kpi`, 관세·HS는 `logistics-compliance`.
