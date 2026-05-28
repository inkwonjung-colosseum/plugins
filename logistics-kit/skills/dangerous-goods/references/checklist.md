# dangerous-goods 도메인 참조

## 활용 시점

- 분류·운송 자문: UN/class/PG 분류, 모드별 신고서, segregation, lithium PI, LQ/EQ
- 코드·정책 리뷰: `dangerous_goods`, `dgr`, `imdg`, `iata`, `adr`, `rid`, `un_number`, `class`, `packing_group`, `lq`, `eq`, `pi_965`, `pi_966`, `pi_967`, `marine_pollutant` 식별자/문서 등장 시
- 운영·디버깅: 선적 거부, 리튬 배터리 항공 발화, segregation 위반, 운송 사고
- 사용자 발화 예: "위험물 분류", "UN 번호", "IMDG", "IATA DGR", "리튬배터리", "marine pollutant"

## 점검 포인트

1. **분류** — UN 번호 + class(1~9, 분할 hazard) + packing group(I/II/III), proper shipping name 정확? 신규 SKU master에서 필수 항목?
2. **모드별 표준 매트릭스** — 해상 IMDG / 항공 IATA DGR / 도로 ADR / 철도 RID — 동일 화물 모드 전환 시 재분류 필수?
3. **segregation 매트릭스** — class 간 격리(예: class 5.1 산화제 ↔ class 3 가연성), 코드(X·A·B·C·D) 매핑, 창고·차량·컨테이너 적용?
4. **포장 종류·UN 인증** — UN 인증 포장(예: 4G/X/Y/Z), 표시·라벨·placard 의무?
5. **LQ/EQ** — limited quantity / excepted quantity 한도, exception 적용 시 라벨 차이?
6. **리튬 배터리 PI 965-970** — Section IA/IB/II 분류, watt-hour·% SoC, 동봉/포함 여부, 항공 cargo-only(CAO) vs PAX 제한, 2024-2026 갱신 사항?
7. **marine pollutant** — UN 3077/3082, 표시 추가 의무?
8. **shipper's declaration** — DGR 서식, 책임 서명, e-DGD 도입 여부, training 인증(IATA cat 1·6)?
9. **차량·터널 제약** — ADR 터널 코드(B/C/D/E), placard·orange plate 의무, 동승 제한, 도로별 통행 시간?
10. **창고 보관** — bunding(누출 차단), 분리 보관, MSDS 게시, 비상 대응 키트, 소방·환기?
11. **응급 대응** — Emergency Response Guide(ERG)·24h hotline, 누출·화재 시 대응 매뉴얼?
12. **항공 cool dry-ice** — UN 1845, NET·overpack 표시?
13. **regulatory 갱신** — IMDG amendments 2년 주기, IATA DGR annual, ADR 격년 — 발효일 추적?

## 응답 형식

- 질문 → 분류·segregation·신고서·근거 법령
- 리뷰 → 위반·위험·법적 노출
- 모드 전환·갱신·리튬 PI 변경 별도 강조

## Hand-off

- 통관·HS·식약처 → `logistics-compliance`
- 해상/항공 부킹 → `freight-forwarding`
- 차량 라우팅 제약 → `vrp-rating-engine`
- 창고 격리·MSDS → `wms-inventory`/`warehouse-safety`
- 식품·의약품 hazmat 결합 → `pharma-gdp-serialization`/`haccp-food-safety`
- 보험·청구 → `cargo-claims-insurance`
