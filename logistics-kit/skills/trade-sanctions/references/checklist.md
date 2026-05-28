# trade-sanctions 도메인 참조

## 활용 시점

- 자문: denied party 스크리닝 정책, 전략물자 분류, license/exception 결정, 위반 보고 절차
- 코드·정책 리뷰: `sanctions`, `denied_party`, `ofac`, `sdn`, `entity_list`, `eccn`, `ear`, `itar`, `dual_use`, `end_use`, `embargo`, `strategic_items` 식별자/문서 등장 시
- 운영·인시던트: 매칭 false positive 폭주, hit 처리 지연, dual-use 의심 화물, 위반 자가 보고
- 사용자 발화 예: "OFAC 스크리닝", "전략물자", "EAR", "ITAR", "dual-use", "denied party"

## 점검 포인트

1. **스크리닝 트리거** — 주문 접수 / 출고 전 / 부킹 / 결제 — 어느 시점에 자동 스크리닝? 미통과 시 hold?
2. **대상 리스트 동기화** — OFAC SDN·non-SDN·sectoral, EU consolidated·UK OFSI·UN, 한국 전략물자(KOSTI)·테러자금 — sync 주기(일/주), 변경 알림?
3. **매칭 알고리즘** — exact + fuzzy(Levenshtein·phonetic·Soundex), 임계치 튜닝, false positive 율 관리?
4. **hit handling 워크플로** — 검토자 풀, 평가 기록(누가·언제·결정), 4-eyes 원칙, escalation·license 신청?
5. **전략물자 분류** — ECCN·CCL·USML·전략물자 ID 자가 분류 vs 외부 결정, 분류 기록·근거?
6. **end-use/end-user 검증** — red flag 인디케이터(이상 결제·우회 국가·민감 산업), CHEC/EUC 문서 요구?
7. **embargo·sanctioned 국가** — 운송 거부·결제 차단, OFAC 50% rule(소유 비율 추정), 우회 거래 차단?
8. **license·exception** — TSR·EAR99 등급 분류, license 신청·기한·연장, 일반·특정 exception?
9. **위반 자가 보고(voluntary self-disclosure)** — 시점·문서·법적 보호 효과, 외부 변호인 협업?
10. **연결 거래 위험** — 보험·금융·통신 등 동반 제공 시 위반 위험?
11. **공급사·고객 KYC** — 신규 onboarding 시 UBO(실소유주) 확인, 정기 재스크리닝?
12. **audit log immutability** — 스크리닝 결정·근거·매칭 ID 영구 보존(7년+), tampering 방지?
13. **rate limit·SLA** — 외부 스크리닝 API 호출 비용·캐싱, 부분 장애 시 fail-closed(차단) 정책?

## 응답 형식

- 질문 → 표준 스크리닝 절차·결정 기준·근거 법령
- 리뷰 → 위반·위험·자가 보고 권고
- 위반 형사·민사 노출 별도 강조

## Hand-off

- HS·통관 → `logistics-compliance`
- FTA 원산지 결정 → `fta-origin`
- 국제 운송 부킹 → `freight-forwarding`
- PII 처리·data minimization → `data-privacy-logistics`
- 감사 로그 모델 → `logistics-data-model`/`logistics-observability`
