# recall-traceability 도메인 참조

## 활용 시점

- 자문: mock recall 절차, one-up-one-down 정책, lot genealogy 모델, 보고 시한·통신 체계 수립
- 코드·정책 리뷰: `recall`, `traceability`, `lot_genealogy`, `one_up_one_down`, `mock_recall`, `class_i`, `class_ii`, `class_iii`, `regulator_notification`, `disposition` 식별자/문서 등장 시
- 운영·인시던트: 회수 발동, 추적 끊김, 보고 시한 임박, 폐기 인증서 누락
- 사용자 발화 예: "회수", "mock recall", "lot 추적", "식약처 보고", "FDA recall class"

## 점검 포인트

1. **one-up-one-down 추적** — 직전 공급사 + 직후 고객 1단계씩 추적 가능? 모든 lot/batch에 입출입 기록?
2. **lot genealogy 데이터 모델** — 원재료 lot → 공정 lot → 완제품 lot → 출고 단위(case·pallet·tracking) 일대다·다대다 매핑?
3. **mock recall 빈도·기준** — 분기·반기 mock, 가상 lot 선정 후 N시간 이내 추적 완료 SLA(보통 4h ISO 22005·식약처)?
4. **recall class** — class I(심각한 건강 위험·의무 시한 24~72h) / II(일시적 위험) / III(라벨 오류 등 경미), 분류 결정 권한?
5. **regulator notification 시한** — 식약처(약사법·식품위생법), FDA 21 CFR 7, EU rapid alert system(RASFF/Safety Gate) 시한·매뉴얼?
6. **고객·소비자 통신** — 화주·재판매 채널·소비자 직접 알림 매트릭스, 매체(보도자료·웹·문자), 다국어?
7. **회수·격리(reverse 흐름)** — RMA 절차와 분리, 회수 운임 부담, 일자별 회수율 추적, 미회수 대책?
8. **disposition 결정** — 폐기 / 재작업(rework) / 등급 하향(downgrade) / 기증 결정 권한, audit trail?
9. **폐기 입증** — 소각 인증서·매립 인증서·destruction witness signature·사진?
10. **CAPA·재발 방지** — root cause·CAPA·effectiveness check, regulator 보고 후속?
11. **EPCIS / GS1 이벤트** — 표준 이벤트(commission·aggregation·shipping·decommission) 기록, 호환성?
12. **데이터 보존 의무** — 식품 2년+, 의약품 5~10년+, 의료기기 평생, 회수 기록 immutability?
13. **회수 KPI** — recall completeness %, time-to-completion, repeat recall rate, regulator letter 무이행률?

## 응답 형식

- 질문 → 표준 추적·보고·통신·CAPA
- 리뷰 → 위반·시한 위험·법적 노출
- 환자/소비자 안전 별도 강조

## Hand-off

- 일반 RMA(소비자 반품) → `returns-rma`
- 의약품 회수·class 결정 → `pharma-gdp-serialization`
- 식품 회수·CCP → `haccp-food-safety`
- 위험물 회수 → `dangerous-goods`
- 보험·청구 → `cargo-claims-insurance`
- 감사 로그 immutability → `logistics-data-model`/`logistics-observability`
