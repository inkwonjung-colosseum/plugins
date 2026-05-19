# logistics-kit Backlog

추가 후보 스킬 정리. 우선순위·근거·hand-off 명시.

현재 12개 스킬은 *내부 모델·산식 중심* 편향. 외부 통신·계획·소비자 레이어 공백 큼.

---

## P0 — 즉시 후보

### demand-forecast

- **범위**: 수요예측, 안전재고, 재주문점(ROP), S&OP
- **공백 이유**: `wms-inventory` ATP는 *현재 상태* 중심. 미래 수요·보충 계획 레이어 없음
- **핵심 주제**: 예측 정확도(MAPE/WMAPE/bias), bullwhip, 신제품 cold-start, 프로모션 lift, 시즈널리티, 이벤트 캘린더
- **Hand-off**: 재고 차감/ATP `wms-inventory`, 발주 트리거 `procurement-po`(신규), KPI 산식 `logistics-kpi`

### carrier-edi

- **범위**: 캐리어 연동·EDI·라벨·tracking webhook
- **공백 이유**: `tms-routing`은 산식·배차 휴리스틱. 외부 시스템 통신 프로토콜 공백
- **핵심 주제**: EDI 204/214/990, ASN 856, ZPL/EPL 라벨, AS2/SFTP, webhook idempotency, status mapping
- **Hand-off**: 멱등성 `logistics-idempotency`, 이벤트 envelope `logistics-event-schema`, 운임 정산 `logistics-settlement`

### last-mile-delivery

- **범위**: 라스트마일·시간대 슬롯·POD·부재 처리
- **공백 이유**: `tms-routing`은 간선·VRP 중심. 소비자 접점·CEP 패턴 공백
- **핵심 주제**: 시간대 슬롯 booking, POD(서명·사진·OTP), 부재 재시도 SLA, 도서산간 분기, 합포장, 픽업 포인트, 새벽배송
- **Hand-off**: 추적 노출 `track-trace`(신규), KPI(OTD) `logistics-kpi`, 클레임 `cargo-claims`(신규)

### slotting-putaway

- **범위**: 창고 슬로팅·putaway 전략·replenishment
- **공백 이유**: `wms-inventory`는 차감/이력. 위치 최적화 레이어 분리
- **핵심 주제**: ABC 분류, 회전율 기반 위치, golden zone, putaway 규칙(혼적 금지, lot 격리), forward/reserve pick, replenishment 트리거
- **Hand-off**: 재고 트랜잭션 `wms-inventory`, 회전율 KPI `logistics-kpi`, 자동화 `wcs-mhe`(신규)

---

## P1 — 중기 후보

### procurement-po

- **범위**: 발주·공급사·입고 예정(ASN)
- **핵심 주제**: PO 상태기계, 3-way match(PO/GR/Invoice), ASN 수신·매칭, 분할 입고, 검수 불합격 처리
- **Hand-off**: 입고 트랜잭션 `wms-inventory`, 수요 트리거 `demand-forecast`, 결제·매입 `logistics-settlement`

### yard-dock

- **범위**: YMS·도크 어포인트먼트·차량 게이트
- **핵심 주제**: 도크 슬롯 예약, gate in/out, 대기시간 KPI(detention), 트레일러 풀, 도크-오더 매칭
- **Hand-off**: 배차 `tms-routing`, 입출고 트리거 `wms-inventory`/`oms-fulfillment`, KPI `logistics-kpi`

### cargo-claims

- **범위**: 화물 클레임·보험·파손·분실
- **공백 이유**: `returns-rma`는 소비자 반품. B2B 운송 클레임 별개
- **핵심 주제**: 사유 코드, 사진 증빙, 보험사 정산 워크플로, 면책 한도, 차주 과실 분배
- **Hand-off**: 차주 분배 `tms-routing`, 정산 분개 `logistics-settlement`, 콜드체인 일탈 `cold-chain-monitor`

### track-trace

- **범위**: 화주·고객용 추적·이벤트 집약·ETA
- **공백 이유**: `logistics-event-schema`는 생산자 측. 소비 레이어·UI 노출 정책 없음
- **핵심 주제**: 마일스톤 정의, 이벤트 집약·중복 제거, ETA 재계산, 알림 채널(앱/SMS/카카오), 권한·PII 마스킹
- **Hand-off**: 원천 이벤트 `logistics-event-schema`, 멱등성 `logistics-idempotency`, 라스트마일 `last-mile-delivery`

---

## P2 — 장기·틈새

### wcs-mhe

- **범위**: WCS·AGV/AMR·컨베이어·소터
- **핵심 주제**: 작업 큐, 충돌 회피, hand-off 프로토콜, MES 연동, 장애 fallback
- **Hand-off**: 작업 지시 `wms-inventory`, 슬로팅 `slotting-putaway`

### inventory-accuracy

- **범위**: Cycle count 감사·차이 분석·shrinkage
- **공백 이유**: `wms-inventory` checklist에 포함 가능하나 감사·통계는 분리 가치 있음
- **핵심 주제**: ABC 빈도, blind count, 차이 사유 코드, IRA(Inventory Record Accuracy), shrinkage 분개
- **Hand-off**: 재고 트랜잭션 `wms-inventory`, 분개 `logistics-settlement`, KPI `logistics-kpi`

### chain-of-custody

- **범위**: 고가품·주류·담배 봉인 이력
- **핵심 주제**: 봉인(seal) 번호, 이양 서명, 분실 추적, 규제(주류 면허) 매핑
- **Hand-off**: 콜드체인 패턴 응용 `cold-chain-monitor`, 규제 `logistics-compliance`

### sustainability-carbon

- **범위**: 탄소배출(GLEC)·Scope 3·회수율
- **핵심 주제**: tkm 산정, 모드별 배출계수, 적재율 영향, 회수 포장재, CBAM 보고
- **Hand-off**: 적재율 `logistics-kpi`, 통관 보고 `logistics-compliance`

---

## 비고

- P0 4개 추가 시 총 16개. 도메인 균형(운영4 / 횡단4 / 플랫폼4 / 계획·외부4) 성립
- 신규 스킬 추가 시 기존 hand-off 갱신 필요 (특히 `wms-inventory`, `tms-routing`, `oms-fulfillment`)
- 우선순위 변경 가능. 실 프로젝트 요구·고객 도메인 따라 P1↔P0 이동
