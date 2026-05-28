# cargo-claims-insurance 도메인 참조

## 활용 시점

- 자문: 책임 협약 적용, 면책 한도, 증빙·survey 절차, subrogation 워크플로 수립
- 코드·정책 리뷰: `cargo_claim`, `insurance`, `cogsa`, `cmr`, `hague_visby`, `montreal`, `warsaw`, `subrogation`, `time_bar`, `package_limitation`, `sdr`, `all_risk` 식별자/문서 등장 시
- 운영·분쟁: 클레임 접수, 시한 임박, 면책 한도 분쟁, 차주 과실 분배
- 사용자 발화 예: "cargo claim", "COGSA", "CMR", "subrogation", "면책 한도", "time bar"

## 점검 포인트

1. **협약 적용 매트릭스** — 해상 COGSA(US)/Hague-Visby(국제) / 도로 CMR(EU) / 항공 Montreal(개정)·Warsaw(구) / 철도 CIM/SMGS, 노선·계약별 결정?
2. **면책 한도** — 해상 Hague-Visby 666.67 SDR/포장 or 2 SDR/kg(둘 중 큰 값), 항공 22 SDR/kg(Montreal), 도로 CMR 8.33 SDR/kg — 산정?
3. **B/L 조항** — Himalaya·Paramount·jurisdiction·arbitration·time bar(보통 1년) 조항?
4. **time bar(시한)** — 통지(보통 7일)·소송 시한(1~2년) — 협약별 매트릭스, 시한 임박 자동 알림?
5. **all-risk vs named-peril** — cargo all-risk vs ICC(A/B/C), war/strike clause, 적용 위험 매트릭스?
6. **증빙·survey** — 도착지 즉시 사진·survey 보고서·packing list·B/L·invoice, 보존 기간?
7. **subrogation 권리** — 보험사 → 운송인 구상권, 시한, 권리 이전 문서?
8. **차주·캐리어 과실 분배** — 다구간 사고 발생 위치 입증, 책임 협약·계약·과실 비율?
9. **부분 손/전손 산정** — actual cash value vs replacement, depreciation, 인양·운임 가산?
10. **deductible·SIR** — 자기부담금·self-insured retention, 정산 차감?
11. **콜드체인 일탈로 인한 손** — TTI·MKT 일탈 → 폐기 → 클레임 연결, 의약품 class별 가치 평가?
12. **위험물 사고** — 환경 정화 비용·3자 책임·정부 부과·CMR Annex?
13. **재발 방지·CAPA** — 패턴 분석, 캐리어 scorecard 반영, 계약 갱신 협상?

## 협약 면책 한도 요약

| 협약 | 모드 | 면책 한도 |
|---|---|---|
| Hague-Visby | 해상 | 666.67 SDR/포장 OR 2 SDR/kg (대) |
| COGSA(US 1936) | 해상 (US) | USD 500 / package |
| CMR | 도로 (EU+) | 8.33 SDR/kg |
| Montreal 1999 | 항공 | 22 SDR/kg (현 갱신: 26 SDR/kg) |
| Warsaw 1929 | 항공 (구) | 17 SDR/kg |

## 응답 형식

- 질문 → 협약·면책·시한·증빙
- 리뷰 → 시한 누락·증빙 미비·법적 위험
- 시한·면책 한도 영향 별도 강조

## Hand-off

- 운임·debit/credit note 분개 → `logistics-settlement`
- 운송 디테일·B/L → `tms-routing`/`freight-forwarding`
- 콜드체인·MKT 일탈 → `cold-chain-monitor`/`pharma-gdp-serialization`
- 회수·class 결정 → `recall-traceability`
- 위험물 사고 → `dangerous-goods`
- 분실·도난 → `chain-of-custody`
