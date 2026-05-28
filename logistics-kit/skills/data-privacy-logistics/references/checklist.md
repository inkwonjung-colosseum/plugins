# data-privacy-logistics 도메인 참조

## 활용 시점

- 자문: PII 수집 근거, 보관기간, 위탁·재위탁 동의, cross-border 이전, 정보주체 권리 절차 수립
- 코드·정책 리뷰: `pii`, `pipa`, `gdpr`, `consent`, `retention`, `masking`, `processor`, `dpa`, `scc`, `bcr`, `data_subject_request`, `dsr` 식별자/문서 등장 시
- 운영·인시던트: 침해 의심·통지 시한 임박·DSR 처리·과도 수집·민감정보 노출
- 사용자 발화 예: "수하인 정보", "PII 보관기간", "PIPA", "GDPR", "위탁 동의", "DSR"

## 점검 포인트

1. **수집 근거** — 동의 / 계약 이행 / 법령 의무 / 정당한 이익 — 항목별 매트릭스, 필수 vs 선택?
2. **수집 항목 최소화** — 수하인 이름·주소·연락처 외 과도 수집(생년월일·성별 등) 여부?
3. **보관기간** — 거래 완료 후 PIPA 5년 마스킹·삭제, 결제 5년(전자상거래법), 통관 5년 — 매트릭스?
4. **마스킹 표준** — 이름 `홍**`, 주소 `서울시 강남구 ***`, 연락처 `010-****-1234` — UI/로그/검색 차등?
5. **위탁(processor) 동의** — 3PL·캐리어·CS 위탁 시 위탁 사실 고지·동의, 위탁 계약 의무 사항(DPA)?
6. **재위탁(sub-processor)** — 재위탁 동의 절차, 재위탁자 변경 통지?
7. **cross-border 이전** — EU → 한국 SCC·adequacy, 한국 → 해외 동의·계약·법령 근거, 처리 위치 표기?
8. **정보주체 권리(DSR)** — 열람·정정·삭제·처리정지·이동권 요청 채널, SLA(GDPR 30일·PIPA 10일), 거부 사유?
9. **민감정보 별도 처리** — 생체(지문·얼굴)·CCTV·건강·결제 카드 — 별도 동의·암호화·접근 통제?
10. **암호화·접근통제** — 저장·전송 암호화, RBAC, 키 rotation, MFA, 접근 audit log?
11. **침해·notification** — 침해 발생 시 정보주체 / 기관(개인정보위·KISA·GDPR DPA) 통지 시한 (72h GDPR / 즉시 PIPA)?
12. **이벤트·로그 PII** — 이벤트 envelope·로그에 raw PII 실리지 않게 토큰화·별도 vault·필드 마스킹?
13. **마케팅 동의·고지** — 마케팅 활용 별도 동의·철회 채널, 14세 미만 법정대리인 동의?
14. **개인통관고유부호(PCC)** — 형식·검증·재사용 금지, 입력 시 보관 정책?

## 응답 형식

- 질문 → 근거 법령·보관·마스킹·DSR 절차
- 리뷰 → 위반·과징금·통지 의무 위험
- 침해 통지 시한·과징금 별도 강조

## Hand-off

- tenant 격리·RLS → `logistics-multitenancy`
- 감사 로그 모델 → `logistics-data-model`/`logistics-observability`
- 통관 PII(PCC) → `logistics-compliance`
- 고객 노출 정책 → `track-trace`
- 결제·환불 PII → `logistics-settlement`/`logistics-idempotency`
- 직원 PII·인사 → `labor-mgmt`
