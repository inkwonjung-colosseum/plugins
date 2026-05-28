# haccp-food-safety 도메인 참조

## 활용 시점

- 자문: HACCP 7원칙 적용, CCP 식별·모니터링, allergen 관리, 라벨 표시, 회수 분류 정책 수립
- 코드·정책 리뷰: `haccp`, `ccp`, `allergen`, `country_of_origin`, `coo`, `halal`, `kosher`, `expiry`, `best_before`, `use_by`, `traceability` 식별자/문서 등장 시
- 운영·인시던트: 식중독·이물·allergen 미표시·소비기한 위반·식약처 회수 명령
- 사용자 발화 예: "HACCP", "CCP", "allergen", "원산지 표시", "할랄", "kosher", "소비기한"

## 점검 포인트

1. **HACCP 7원칙·12절차** — 위해 분석 → CCP 결정 → 한계 기준 → 모니터링 → 시정조치 → 검증 → 기록, 식약처 HACCP 적용 매트릭스?
2. **CCP 식별·결정 트리** — 위해 가능성 + 제어 필수성, 의사결정 도구(Codex 4 questions)?
3. **한계 기준(critical limit) 매트릭스** — 온도·시간·pH·Aw, 측정 가능 indicator?
4. **모니터링·시정조치** — 빈도·책임자·기록, 한계 초과 시 격리/폐기/재가공 결정 트리?
5. **allergen 관리** — 한국 알레르기 유발 22종(식약처) / FDA 9 major, 라벨·교차오염 방지·청소 SOP?
6. **원산지 표시** — 식품·농수산물 원산지 표시법 적용, 가공·복합 제품 규칙, 잘못 표시 시 처벌?
7. **halal/kosher 인증** — 인증 기관(KMF·MUI·OU·OK), 인증 lot 격리·교차 오염 방지, 인증 만료?
8. **소비기한 vs 유통기한** — 2023.01부터 한국 소비기한 전환, 라벨·FEFO 정책, 경계 임박 SKU 처리?
9. **traceability one-up-one-down** — 식품위생법 의무, 2년+ 기록, 빠른 회수 가능성?
10. **회수 class** — 식약처 1·2·3등급 (1등급 즉시 보고·24h), 모의 회수 SLA?
11. **공급망 검증(audit)** — 1차·2차·3차 supplier audit, GFSI(BRC·SQF·FSSC 22000·IFS) 인증 요구?
12. **외식·HMR·온라인 식품 특수규칙** — 일반음식점·즉석조리·온라인 판매 식품 표시 규칙 차이?
13. **수입식품 특별법** — 수입식품 안전관리 특별법, 해외 제조업소 등록, 검사 등급제?

## 응답 형식

- 질문 → HACCP 7원칙·CCP·라벨 표준·근거 법령
- 리뷰 → 위반·식약처 처분 위험·소비자 안전
- 식약처 회수·교차오염 위험 별도 강조

## Hand-off

- 콜드체인·온도 일탈 → `cold-chain-monitor`
- 식약처 회수·식품위생법 → `recall-traceability`/`logistics-compliance`
- 원산지·FTA → `fta-origin`
- 식품 hazmat(살충제·세제 결합 보관) → `dangerous-goods`/`warehouse-safety`
- 라벨·VAS 작업 → `cross-dock-kitting`
- 일탈로 인한 클레임 → `cargo-claims-insurance`
