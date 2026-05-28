# logistics-kit Backlog

v0.2.0 (50 Skills) 출시 후 추가 후보. 우선순위·근거·hand-off 명시.

v0.1 12 skills → v0.2 50 skills: 운영(slotting/wave/WCS/yard/IRA/labor/cross-dock/safety) + 운송(carrier-edi/last-mile/track/VRP-rating/forwarding) + 계획(forecast/inventory-planning/SOP/PO/network) + 규제(DGR/sanctions/pharma/recall/CoC/claims/sustainability/FTA/HACCP/privacy) + 플랫폼(saga/observability/multitenancy/channel/DR/bulk/locale/MDM/resilience/API) 38개 신설. 4 계층 균형 확보.

---

## P0 — 즉시 후보 (다음 minor)

### labeling-format-printer

- **범위**: 라벨 인쇄 farm·DPI·heat·재인쇄·라벨 농축 회수
- **공백 이유**: `carrier-edi`는 발급 / 보존 / void 표준에 한정. 실제 인쇄 farm·재인쇄·라벨 농축에 대한 운영 깊이 부족.
- **핵심 주제**: ZPL 표준 vs 캐리어 변형, 농축(consolidation)·관리 라벨, 재인쇄 권한·중복 차단, 인쇄 farm 부하 분산
- **Hand-off**: `carrier-edi`, `wave-pick-strategy`, `wms-inventory`

### voice-pick-rf-device

- **범위**: 디바이스 운영(연결·배터리·음성 trainset·voice tuning)
- **공백 이유**: `wave-pick-strategy`에서 디바이스 *선택* 매칭만 다룸. 실제 운영(헤드셋 위생·교체·노이즈·voice training·BLE·관리 콘솔)에 대한 깊이 부족.
- **Hand-off**: `wave-pick-strategy`, `labor-mgmt`, `warehouse-safety`

### supplier-portal

- **범위**: 공급사 self-service portal·ASN 입력·invoice 업로드·dispute
- **Hand-off**: `procurement-po`, `logistics-settlement`, `data-privacy-logistics`

---

## P1 — 중기 후보

### tax-engine
- **범위**: 부가세·관세·도착지세(VAT)·환급(drawback) 자동화 엔진
- **Hand-off**: `logistics-settlement`, `logistics-compliance`, `fta-origin`

### damage-claim-cv
- **범위**: 화물 파손 CV(이미지·AI 등급) 자동 판정
- **Hand-off**: `cargo-claims-insurance`, `returns-rma`

### returns-grading-cv
- **범위**: 반품 검수 CV·grading·refurb 자동화
- **Hand-off**: `returns-rma`, `wms-inventory`

### simulation-digital-twin
- **범위**: 창고·라우팅 digital twin·what-if 시뮬레이션
- **Hand-off**: `network-design`, `wcs-mhe`, `vrp-rating-engine`

### marketplace-arbitrage
- **범위**: 채널별 가격·재고 차익·이동 결정
- **Hand-off**: `channel-sync`, `inventory-planning`, `logistics-settlement`

---

## P2 — 장기·틈새

### blockchain-traceability
- **범위**: 식품·의약품 traceability 블록체인 통합 (GS1 EPCIS over chain)
- **Hand-off**: `recall-traceability`, `pharma-gdp-serialization`, `haccp-food-safety`

### autonomous-truck
- **범위**: 자율주행 트럭·last-mile robot·drone delivery 운영 모델
- **Hand-off**: `tms-routing`, `last-mile-delivery`, `warehouse-safety`

### iot-device-fleet
- **범위**: IoT sensor fleet 관리·OTA·firmware·battery
- **Hand-off**: `cold-chain-monitor`, `track-trace`, `wcs-mhe`

### customs-broker-handoff
- **범위**: 통관사·CHB(custom house broker) 연동, e-PCC 시스템
- **Hand-off**: `logistics-compliance`, `freight-forwarding`, `trade-sanctions`

### finance-audit-soc1
- **범위**: SOC 1·SOC 2 감사·내부통제, ERP 분개·tenant 격리 증명
- **Hand-off**: `logistics-settlement`, `logistics-observability`, `logistics-multitenancy`

---

## 비고

- v0.2.0 50 Skills로 운영·계획·규제·플랫폼 4 계층 균형 확보. 우선순위 변경 가능. 실 프로젝트 요구·고객 도메인 따라 P1↔P0 이동.
- 신규 스킬 추가 시 기존 hand-off 갱신 필요 (특히 `wms-inventory`, `tms-routing`, `oms-fulfillment`, `logistics-compliance`, `logistics-kpi`).
- 모든 신규 스킬은 frontmatter description에 `Use when [한국어 키워드] 설계/리뷰/운영` 패턴 강제 (trigger 토큰 절약).
- 모든 신규 스킬은 본문 6 라인 이하 유지, 깊이는 `references/checklist.md`에 위치 (deferred bucket).
