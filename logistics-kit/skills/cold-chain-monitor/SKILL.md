---
name: cold-chain-monitor
description: Use when 콜드체인·온도 이력·TTI·reefer·백신/의약품 운송 설계/리뷰/운영.
---

# cold-chain-monitor

콜드체인(시간×온도) 도메인 상시 전문가. SKU별 온도 범위, TTI(time-temperature integration), 센서 결측 정책, 단절(break) 감지, reefer 차량 vs 화물 측정, 폐기 판정 워크플로, GDP/HACCP 감사 로그에 대한 설계 자문, 코드 리뷰, 운영 질의 응답을 수행.

Workflow: 질의·맥락 파악(설계 / 리뷰 / 디버깅 / 규제 검토) → `references/checklist.md`의 점검 포인트 적용 → 일탈 검출 로직·권장 패턴·약사법/식품위생법/GDP 가이드 근거 제시.

Hand-off: 일반 재고는 `wms-inventory`, 운송·reefer 차량 배차는 `tms-routing`, 의약품 통관은 `logistics-compliance`.
