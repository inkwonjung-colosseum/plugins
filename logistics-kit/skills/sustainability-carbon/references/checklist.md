# sustainability-carbon 도메인 참조

## 활용 시점

- 자문: GLEC 산정 방법, Scope 3 cat 4/9 구분, CBAM 보고, science-based target 설정
- 코드·모델 리뷰: `co2`, `emission`, `glec`, `tkm`, `scope_3`, `cat_4`, `cat_9`, `cbam`, `eu_ets`, `wtw`, `ttw`, `empty_mile`, `load_factor` 식별자/문서 등장 시
- 운영·감사: ESG 보고 데이터 품질, 모드 별 계수 변경, well-to-wheel vs tank-to-wheel 차이, 회수 포장 회수율
- 사용자 발화 예: "탄소 배출", "GLEC", "tkm", "Scope 3", "CBAM", "science-based target"

## 점검 포인트

1. **GLEC framework** — well-to-wheel(WTW) 표준, 모드별(truck·rail·ocean·air·inland barge) 기본 계수, 1차 데이터 우선·기본값 보조?
2. **tkm 산정** — `weight_t × distance_km × emission_factor (gCO₂e/tkm)` 계산, 적재율·우회 거리 반영?
3. **Scope 3 cat 4 vs 9** — cat 4(upstream: 회사가 비용 부담) vs cat 9(downstream: 고객이 비용 부담) — 분류 매트릭스?
4. **데이터 hierarchy** — 1차(실측 연료 소비) > 2차(차종·평균 mileage) > 3차(distance × 기본계수) — 측정 수준 표기?
5. **empty mile·detour** — empty mile 포함 의무, payload 비율(load factor) 차감 반영?
6. **air freight 별도 처리** — RFI(radiative forcing index) 2~3 배수 적용 정책(GLEC는 미적용 권장하나 GHG Protocol 옵션)?
7. **CBAM(EU)** — CN-code 매핑, 제품군 매트릭스(철강·시멘트·알루미늄 등), embedded emission 보고·verify, 분기 보고서?
8. **EU ETS shipping** — 2024 단계적 도입(40%→70%→100%), 항해 데이터·EU 항만 50% 의무?
9. **회수 포장재** — 반복 사용 회수율, 회수 운임 emission, deposit-refund 모델?
10. **science-based target(SBTi)** — 1.5°C 정렬 절대 감축률, near-term(2030)·long-term(2050)·net-zero?
11. **third-party assurance** — ISO 14064 / 14083 verification, audit trail immutability?
12. **모드 전환 시뮬레이션** — road→rail/ocean 절감 시나리오, 비용·CO₂·SLA 트레이드오프 평가?
13. **공급사·캐리어 ESG scorecard** — 캐리어별 CO₂/tkm 비교, 입찰·계약 기준 반영?

## 산식 요약

| 모드 | 기본 emission factor (참고) |
|---|---|
| Diesel truck | ~80 gCO₂e/tkm (적재율 평균) |
| Rail freight | ~25 gCO₂e/tkm |
| Sea container | ~10–15 gCO₂e/tkm (vessel/route) |
| Air freight | ~600–1000 gCO₂e/tkm (RFI 미적용) |
| Inland barge | ~30 gCO₂e/tkm |

(실제 보고는 GLEC v3+ / ISO 14083 갱신 계수 사용)

## 응답 형식

- 질문 → 산정 방법·Scope 분류·근거 표준
- 리뷰 → 데이터 hierarchy·verify 위험·보고 시한
- CBAM·SBTi 위반·assurance 부족 위험 별도 강조

## Hand-off

- 적재율·empty mile KPI → `logistics-kpi`
- HS·CN-code → `logistics-compliance`/`fta-origin`
- 모드 mix·네트워크 의사결정 → `network-design`/`vrp-rating-engine`
- 정산 충당금·CBAM levy → `logistics-settlement`
- 보고 PII·tenant 분리 → `data-privacy-logistics`/`logistics-multitenancy`
