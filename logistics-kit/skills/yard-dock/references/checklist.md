# yard-dock 도메인 참조

## 활용 시점

- 설계 자문: 도크 슬롯·어포인트먼트 모델, gate 절차, detention/demurrage 정책, 야드 동선·트레일러 풀 운영 수립
- 코드·스키마 리뷰: `yms`, `dock`, `appointment`, `gate`, `trailer`, `yard_move`, `detention`, `demurrage`, `dock_door`, `inbound_window`, `outbound_window` 식별자가 보일 때
- 운영·디버깅: 도크 대기 폭주, no-show, dock-to-stock 지연, 디텐션 청구 분쟁
- 사용자 발화 예: "도크 예약", "디텐션", "트레일러 풀", "야드 셔틀", "gate in/out"

## 점검 포인트

1. **도크 슬롯 모델** — 도크/시간(15·30·60분 슬롯)·작업 유형(LL/UL/cross-dock) 분리? 동시 사용 제약(인접 도크 충돌)?
2. **어포인트먼트 예약 절차** — 캐리어 셀프 예약 vs 화주 예약 vs WMS 자동? 변경/취소 SLA, no-show 페널티?
3. **gate in/out 검증** — 차량 번호·운전기사·트레일러 매칭, 통합 ID로 입출 시각 캡처, 위변조 방지(사진/봉인)?
4. **detention/demurrage 시계** — 자유시간(free time) 시작 시점(도착 vs 도크 도착 vs 게이트 in), 일시정지 사유(우리측 지연·서류 누락) 정책?
5. **트레일러 풀(drop trailer)** — 풀 트레일러 ownership, lot 점유 시간 SLA, idle 트레일러 정리?
6. **도크-오더 매칭** — 어포인트먼트와 ASN/PO/order의 매칭 키, 미매칭 도착 처리(보류·임시 도크)?
7. **wave 동기화** — 인바운드 도착 시 putaway wave 자동 트리거 / 아웃바운드 출고 wave 종료와 도크 슬롯 매칭?
8. **셔틀·spotter 운영** — 야드 내 트레일러 이동 작업 큐, spotter 인력 배정?
9. **비상 슬롯·드롭** — 우선 화물(콜드체인·위험물·SLA tier A) 우회 정책?
10. **dwell time KPI** — gate in → dock arrival → unload start → unload end → gate out 시계 캡처, 단계별 KPI 노출?

## 응답 형식

- 질문 → 표준 어포인트먼트 정책·디텐션 산식·매칭 규칙
- 리뷰 → 약점·위험·수정 제안 (필요 시 `file:line`)
- detention 분쟁 위험 별도 강조 (계약 조항 vs 운영 실제 불일치)

## Hand-off

- 배차·캐리어 운임 → `tms-routing`
- 입출고 트리거 → `wms-inventory`/`oms-fulfillment`
- 디텐션/디머리지 정산 분개 → `logistics-settlement`
- dwell time / dock-to-stock KPI → `logistics-kpi`
- 통관 보세창고 대기 → `logistics-compliance`
