# cold-chain-monitor 도메인 참조

## 활용 시점

- 설계 자문: SKU별 온도 범위·TTI·단절 감지·결측 정책·폐기 워크플로 수립
- 코드·스키마 리뷰: `temperature_log`, `cold_chain`, `reefer`, `tti`, `frozen`, `chilled`, `vaccine`, `gdp`, `humidity` 식별자가 보일 때
- 운영·디버깅: 일탈 알림 미발생, 폐기 판정 오작동, 감사 로그 누락
- 사용자 발화 예: "온도 일탈", "콜드체인 단절", "백신 운송", "냉장 차량", "센서 결측"

## 점검 포인트

1. **온도 범위 정의** — 상품/SKU 단위로 허용 범위(min, max) + 누적 일탈 시간 한계가 마스터에 있나?
2. **TTI 적합성** — 단순 범위 검사 vs 누적 노출(time-temperature) 곡선 평가? 약제는 보통 후자 필수.
3. **센서 결측 처리** — 결손 구간을 conservative 판정(폐기) vs interpolate vs 보류 중 어떤 정책?
4. **단절(break) 감지** — 연속 N분 이상 범위 이탈 = break. N 값이 product별로 다른가?
5. **reefer 차량 데이터** — 차량 vs 화물(pallet) 단위 측정? 차량 데이터로 화물 적합성 판정 가능(공간 분포)?
6. **폐기 판정 → 후속 처리** — 자동 폐기 vs 사람 검토? 손해배상/보험 청구 트리거?
7. **GDP/HACCP 감사 로그** — 일탈·판정·승인자가 audit log에 시계열로 남나?
8. **MKT(mean kinetic temperature)** — `MKT = -ΔH/R / ln(Σ exp(-ΔH/RT_i)/n)` (ΔH=83.144 kJ/mol), 누적 일탈 통합 평가 (→ `pharma-gdp-serialization`)
9. **qualification IQ/OQ/PQ** — 시설·장비·시스템 IQ(설치)·OQ(작동)·PQ(성능) 프로토콜, 갱신 주기
10. **온도 mapping study** — 창고·트럭·컨테이너 사계절 매핑, hot/cold spot 식별, sensor 배치 표준
11. **excursion review board 워크플로** — 일탈 → quarantine → MKT/안정성 평가 → 사용/폐기 결정, SLA time bar
12. **GDP CAPA loop** — root cause → CAPA → effectiveness check, audit trail immutability, regulator 보고
13. **pre-conditioning·dry-ice** — reefer 사전 냉각 SOP, dry-ice 보충, gel-pack 검증, packaging 인증
14. **excursion 보험 청구** — 폐기 결정 후 보험 청구 트리거 (→ `cargo-claims-insurance`)

## 응답 형식

- 질문 → 표준 정의·trade-off·약사법/식품위생법/GDP 가이드 근거
- 리뷰 → 일탈 검출 로직 누락·권장 패턴
- 규제 인용 시 법령·가이드 명시

## Hand-off

- 일반 재고 트랜잭션 → `wms-inventory`
- reefer 차량 배차·라우팅 → `tms-routing`
- 의약품 통관·GDP 적용 → `logistics-compliance`/`pharma-gdp-serialization`
- 식품 HACCP·CCP → `haccp-food-safety`
- 회수 (recall class) → `recall-traceability`
- chain of custody (high-value pharma) → `chain-of-custody`
- 클레임·보험 → `cargo-claims-insurance`
- 콜드체인 alert·observability → `logistics-observability`
