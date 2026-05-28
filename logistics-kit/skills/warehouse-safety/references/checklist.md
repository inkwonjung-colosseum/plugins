# warehouse-safety 도메인 참조

## 활용 시점

- 설계 자문: 안전 SOP, PIT 인증·점검 정책, LOTO 절차, near-miss 신고, 인체공학 표준 수립
- 코드·정책 리뷰: `safety`, `pit_certification`, `forklift`, `loto`, `near_miss`, `incident`, `osha`, `kosha`, `ppe`, `msds`, `lift_limit`, `evacuation` 식별자/SOP 등장 시
- 운영·인시던트: 사고 발생, near-miss 패턴, 인증 만료, MSDS 접근성 미흡, 비상 훈련 누락
- 사용자 발화 예: "지게차 안전", "LOTO 절차", "near-miss", "사고조사", "인체공학", "산업안전보건법"

## 점검 포인트

1. **PIT(지게차·전동 carry) 인증** — 운전자 자격(국가기술자격·사내 교육), 갱신 주기(3년·연1회), 일일 시업 전 점검(체크리스트·hour meter)?
2. **LOTO 절차** — 컨베이어·소터·전기 차단 lockout/tagout SOP, 다중 작업자 lock, 권한·교육, 비상 해제 절차?
3. **near-miss 신고 체계** — 익명 채널, 24h 내 분석, 패턴 추적, CAPA 적용, 보복 금지 정책?
4. **사고분류·기록** — 무재해/응급/기록가능(recordable·OSHA 300)/lost-time/사망, 신고 의무 시한(KOSHA·산업안전보건공단)?
5. **인체공학(ergonomics)** — 1인 리프트 한계(25kg 가이드·반복 시 더 낮춤), 골든존 픽 비율, 반복동작·소음(85dB) 노출 모니터링?
6. **PPE** — 안전화·헬멧·고시도성 조끼·장갑 표준, hazmat 영역 SCBA·고글, 공급·교체 주기?
7. **MSDS/SDS 접근성** — hazmat 보관 위치 인접 게시, 다국어, 작업자 교육 기록?
8. **비상 대피·소화** — 대피 경로·집결지 지도, 소화기 종류(ABC·D·금속) 매칭, 스프링클러 점검, 비상조명?
9. **사고조사** — 5why·fishbone·TapRoot, root cause 분류, CAPA, 재발 방지 검증 시한?
10. **안전 KPI** — LTIR(lost-time injury rate), TRIR(total recordable), near-miss 비율, 인증 만료 알림? 경영 보고 주기?
11. **고소작업·확장 사다리·MEWP** — 추락 방지(harness·anchor), 인증, 결박 SOP?
12. **하청·임시 인력 안전 적용** — 동일 SOP·교육 의무, 외주 안전 평가(공정 안전·KOSHA 외주관리)?

## 응답 형식

- 질문 → 규정 근거(산업안전보건법·OSHA 1910)·표준 SOP·CAPA 패턴
- 리뷰 → 위반·위험 별도 강조 (생명·법적 의무)
- 인시던트 분석 → 5why·CAPA·재발 방지 검증

## Hand-off

- hazmat·MSDS 분류 → `dangerous-goods`
- 자동화 인터록(emergency stop, light curtain) → `wcs-mhe`
- 인사·노무·교육 기록 → `labor-mgmt`
- 산재보험·보상 분개 → `logistics-settlement`
- 사고로 인한 화물 파손 → `cargo-claims-insurance`
