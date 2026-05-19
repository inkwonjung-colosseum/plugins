---
name: logistics-kpi
description: Use when 물류 KPI·OTIF·fill rate·회전율·리드타임·picking accuracy·적재율 산식 설계/리뷰.
---

# logistics-kpi

물류 KPI·지표 산식 도메인 상시 전문가. OTIF, Fill Rate(라인/단위/주문), 재고 회전율, 리드타임, Picking Accuracy, Perfect Order Rate, 적재율 정의·분모·시점·단위·타임존에 대한 설계 자문, BI 쿼리·대시보드 리뷰, 지표 통일 질의 응답을 수행.

Workflow: 질의·맥락 파악(정의 / 리뷰 / 디버깅 / 신규 KPI 제안) → `references/formulas.md` 표준 산식 + `references/checklist.md` 점검 포인트 적용 → 산식 차이·표준 정의·SLA 타깃·근거 제시.

Hand-off: 보상·정산 적용은 `logistics-settlement`, 데이터 소스·집계 모델은 `logistics-data-model`, 타임존은 `localization-audit`.
