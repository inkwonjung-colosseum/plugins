# vrp-rating-engine 도메인 참조

## 활용 시점

- 설계 자문: VRP 변형 선택, solver 매칭, 운임 산식 스택, dim weight·accessorial·fuel index 정책 수립
- 코드·정책 리뷰: `vrp`, `vrptw`, `vrppd`, `cvrp`, `mdvrp`, `or_tools`, `jsprit`, `dim_weight`, `accessorial`, `fuel_index`, `zone_skip`, `surcharge`, `quote`, `rate_engine` 식별자가 보일 때
- 운영·디버깅: 솔버 timeout, time window 위반, dim weight 분쟁, accessorial 누락, fuel index 갱신 지연
- 사용자 발화 예: "VRPTW", "OR-Tools", "dim weight", "유류할증", "accessorial", "rate quote"

## 점검 포인트

1. **VRP 변형 선택** — TW(시간창), PD(픽업·배송 쌍), 용량(C), 다중depot(MD), 분할(SD) 결합·우선순위? 시작 모델 선택 기준?
2. **목적함수** — 단일 비용 최소화 vs 다목표(비용+CO₂+drv 시간+SLA risk)? 가중치 정책?
3. **solver 선택** — OR-Tools(범용·GLS) / jsprit(EU 표준) / LKH(TSP 대형) / 자체 metaheuristic, 문제 규모(stops·차량)별 매칭?
4. **휴리스틱 초기해 + LS** — savings(C&W) / nearest neighbor + 2-opt/Or-opt/large-neighborhood-search 결합?
5. **실시간 re-route** — 트리거(부재·교통 지연·신규 주문 삽입), 부분 재계산(rolling horizon) 정책?
6. **모드/캐리어 선택 로직** — parcel / LTL / FTL / postal / 자가 차량 비용·SLA 비교 룰?
7. **dim weight 산식** — `L×W×H / divisor`, divisor 캐리어별(139·166·6000), 적용 시점·반올림, 최소 청구 단위?
8. **accessorial 분류 매트릭스** — 거주지·리프트게이트·인사이드·재배달·hazmat·detention·연료할증·중량초과·도서산간 — 각각 정액 vs 비율 vs 거리?
9. **surcharge 스택 순서** — base → 거리·중량 → zone 할증 → accessorial → fuel → 세금. 순서가 결과 영향 (compound vs additive)?
10. **fuel index 운영** — 외부 publication(EIA·KOFETRA)와 연동, 효력 시작일, 데이터 sync 지연 fallback?
11. **contract vs spot rating** — 계약 단가 우선·spot fallback, 동일 lane multiple rate priority(화주·계약·effective date)?
12. **zone-skip** — 다구간 운임 절감용 zone-skip(잘게 분할 vs 직송) 결정?

## 응답 형식

- 질문 → VRP 변형·solver 매칭·운임 산식 스택
- 리뷰 → 약점·위험·수정 제안 (필요 시 `file:line`)
- 운임 분쟁 위험 별도 강조 (dim weight·accessorial·effective date)

## Hand-off

- 외부 운임 정산·debit/credit note → `logistics-settlement`
- hazmat 차량 제약·터널 제한 → `dangerous-goods`
- 라스트마일 슬롯 booking → `last-mile-delivery`
- OTIF·적재율·cost-per-stop KPI → `logistics-kpi`
- 통관·HS 분기 → `logistics-compliance`
