# chain-of-custody 도메인 참조

## 활용 시점

- 자문: seal·서명·이중통제 정책 수립, 면허·수량 통제, 고가품 호송 설계
- 코드·정책 리뷰: `seal`, `chain_of_custody`, `controlled_substance`, `narcotic`, `alcohol_license`, `tobacco_license`, `tamper_evident`, `transfer_signature`, `dual_control` 식별자/문서 등장 시
- 운영·인시던트: seal 손상·위변조, 마약류 수량 불일치, 면허 위반 출하, 고가품 분실
- 사용자 발화 예: "봉인 번호", "controlled substance", "주류 면허", "마약류", "고가품 호송"

## 점검 포인트

1. **seal 발행·확인** — 일련번호 unique, 발행자·시각 기록, 도착지 무결성 확인 절차, 위변조 의심 시 격리?
2. **이양 서명·witness** — 인계자/인수자 식별·서명·시각, 단계별(창고→차량→DC→가맹점) 시계열, 디지털 서명 무결성?
3. **dual control(이중 인원)** — 입출고·이송 시 2인 동시 확인 의무(주류·마약류·고가품), 권한 분리?
4. **이중 잠금** — 마약류·향정신성: 2개 lock(다른 키 보유자), 보관 위치 격리·CCTV·출입 기록?
5. **수량 ledger** — controlled substance의 입고/출고/조정 ledger immutable, 감사기관 정기 보고(KFDA·DEA-like)?
6. **면허 검증** — 주류 면허·담배 판매업·마약류 취급자 — 발급 기관·만료·자동 검증?
7. **위반 보고 시한** — 분실·도난·이상 즉시 경찰·식약처 신고 시한, 보고서 양식?
8. **고가품 호송** — 보험 한도·armoured vehicle·라우팅 비공개·복수 호송원·GPS 실시간?
9. **CCTV·access log** — 보관 위치 CCTV 30일+, 접근 권한 RBAC, 출입 로그 immutability?
10. **재포장·분할** — controlled substance 재포장 시 새로운 seal·서명, 분할 시 모(母) lot ↔ 자(子) lot 연결?
11. **반품·폐기** — 미사용·기한경과 폐기 절차, 감독자 입회, 폐기 인증서?
12. **국가 간 이동** — 마약류·전구체 수출입 license, INCB·KFDA 보고, 정부 인증 운송업자?

## 응답 형식

- 질문 → 표준 seal·서명·이중통제·근거 법령
- 리뷰 → 위반·형사 노출·면허 취소 위험
- 형사 책임·면허 영향 별도 강조

## Hand-off

- 의약품·serialization → `pharma-gdp-serialization`
- 일반 콜드체인 → `cold-chain-monitor`
- 통관·면허 → `logistics-compliance`
- 회수·destruction → `recall-traceability`
- 분실·도난 보험 → `cargo-claims-insurance`
- 보안·접근 권한 → `data-privacy-logistics`/`logistics-observability`
