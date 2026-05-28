# tms-routing 도메인 참조

## 활용 시점

- 설계 자문: 운임표·권역·할증 정책 수립, VRP/TSP 알고리즘 선정
- 코드·스키마 리뷰: `routing`, `dispatch`, `tariff`, `zone`, `freight`, `vehicle`, `driver`, `vrp`, `tsp`, `fuel_surcharge` 식별자가 보일 때
- 운영·디버깅: 운임 차이, 도서산간 미적용, 차량 capacity 초과
- 사용자 발화 예: "배차 로직", "운임 계산", "최적 경로", "권역 분리", "할증 적용"

## 점검 포인트

1. **운임 산식** — base + 거리 + 중량/부피 + 할증 순서가 명시되어 있나? 반올림 위치(km 단위, 원 단위) 일관?
2. **권역(zone) 매핑** — 도서산간/오지/제주 special zone이 우편번호/좌표 기반으로 분기? 새 zone 추가 시 fallback 정의?
3. **유류할증/할증료** — 유가 연동 테이블 vs 고정값, 효력 기간(effective date) 적용 방식이 코드와 일치?
4. **적재율/공차율** — 차량 capacity(kg, m³, pallet) 제약이 솔버에 전달? overflow 시 분할/거절 정책?
5. **VRP/TSP 알고리즘** — 휴리스틱(greedy nearest, savings) 사용 시 time window·depot 제약 반영?
6. **driver 정산 베이스** — 운임 중 차주 분배 portion? 부대비용(통행료, 대기료) 처리?
7. **detention/demurrage 시계** — 도크 도착 후 자유시간(free time), 일시정지 사유, 차주 보상 vs 화주 부과 (→ `yard-dock`)
8. **위험물 차량 제약·터널 코드** — ADR 터널 B/C/D/E, 도시 화물차 통행 제한, hazmat 자격 차량 (→ `dangerous-goods`)
9. **운임 산식 깊이** — dim weight·accessorial stack·fuel index·zone-skip·contract vs spot은 `vrp-rating-engine`으로 위임
10. **HOS·ELD·tachograph** — 운전·휴게 규제(미 ELD·EU tachograph·한국 화물자동차법) 위반 시 운행 정지?
11. **last-mile vs line-haul 구분** — 간선·간이·라스트마일 라우팅 분리(→ `last-mile-delivery`), 라스트 mile capacity 모델 별도?
12. **국제 운송 leg** — 항만/공항 inland trucking·드레이지 (→ `freight-forwarding`)
13. **mode/carrier 선택 로직** — parcel/LTL/FTL/postal/자가 비교 룰(→ `vrp-rating-engine`)

## 응답 형식

- 질문 → 표준 산식·정책 분기·트레이드오프
- 리뷰 → 약점·위험·수정 제안 (필요 시 `file:line`)
- 운임표/zone 정책 외부화 권고는 별도 섹션

## Hand-off

- 운임 정산·회계 분개 → `logistics-settlement`
- 통관/HS코드/위험물 운송 제약 → `logistics-compliance`/`dangerous-goods`
- OTIF·적재율 KPI 정의 → `logistics-kpi`
- VRP solver·운임 stack → `vrp-rating-engine`
- 캐리어 EDI·라벨·webhook → `carrier-edi`
- 라스트마일·POD·슬롯 → `last-mile-delivery`
- 야드·디텐션 → `yard-dock`
- 추적·ETA → `track-trace`
- 국제 운송·B/L·AWB → `freight-forwarding`
- 클레임·보험 → `cargo-claims-insurance`
- 탄소·GLEC → `sustainability-carbon`
