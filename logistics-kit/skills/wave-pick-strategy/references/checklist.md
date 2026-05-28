# wave-pick-strategy 도메인 참조

## 활용 시점

- 설계 자문: wave/batch/cluster 묶음 정책, pick path 라우팅, 디바이스 매칭, accuracy 목표 수립
- 코드·스키마 리뷰: `wave`, `batch_pick`, `cluster_pick`, `pick_path`, `pick_route`, `voice_pick`, `pick_to_light`, `rf_scan`, `cart`, `tote`, `pick_face` 식별자가 보일 때
- 운영·디버깅: wave 보류로 cutoff 미준수, multi-order shorts, 정확도 하락, cart capacity 초과
- 사용자 발화 예: "wave 묶음", "배치 픽", "보이스 픽", "pick path", "picking accuracy"

## 점검 포인트

1. **wave 구성 기준** — 출고 cutoff(택배 마감) + 캐리어 / SLA tier / 존 / SKU heat 중 어떤 조합? wave release 권한·승인 흐름?
2. **batch vs cluster vs zone 픽 매칭** — 단건 / 다건 묶음(batch) / 카트별 다주문(cluster) / 존 라우팅 — SKU velocity·라인 수·동선과 매칭 규칙?
3. **pick path 휴리스틱** — S자 / return / midpoint / largest gap 중 어느 것? 다층 랙·고소픽 적용?
4. **multi-order cart capacity** — totes/슬롯 수, 무게/부피 제약 솔버 반영? 초과 시 분할 wave?
5. **디바이스 매칭** — voice는 양손 자유·고빈도 라인, PTL은 다품종 소량 batch, RF는 범용·lot/serial 스캔 — SKU/존별 매칭 정책 명시?
6. **pick-pack-ship sequencing** — 단일 흐름(pick-and-pack) vs 분리(pick→pack station) vs put-wall 결정 기준?
7. **shorts 처리** — 픽 실패(재고 없음/위치 차이) 시 wave 보류 vs 부분 픽 + replenishment 트리거 정책?
8. **picking accuracy 산식** — 라인 단위(`correct_lines / picked_lines`) vs 수량 단위 정의 어디서? 측정 시점(QC/검수)?
9. **wave 종료 조건** — 모든 픽 완료 시 자동 close vs 수동 close? cutoff 후 잔여 픽 정책?
10. **fast/slow mover 분리 wave** — 슬로우 무버 전용 wave 시간대 vs 통합? cross-zone 동선 영향?

## 응답 형식

- 질문 → 표준 묶음 규칙·라우팅 휴리스틱·디바이스 매칭표
- 리뷰 → 약점·위험·수정 제안 (필요 시 `file:line`)
- accuracy 측정 시점 표준화 권고는 별도 강조

## Hand-off

- 위치/존 정의 → `slotting-putaway`
- 자동화 작업 큐·소터 hand-off → `wcs-mhe`
- 노동 생산성(UPH/lines per hour) → `labor-mgmt`
- 출고 sequencing·label 인쇄 → `oms-fulfillment`
- 정확도 KPI 정의 → `logistics-kpi`
