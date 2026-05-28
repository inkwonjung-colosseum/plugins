# localization-audit 도메인 참조

## 활용 시점

- 자문: 타임존 cutoff, 통화·환율, 단위, locale, 휴일 캘린더, 다국어 라벨 표준 수립
- 코드·정책 리뷰: `timezone`, `tz`, `kst`, `utc`, `currency`, `exchange_rate`, `metric_unit`, `imperial_unit`, `locale`, `holiday_calendar`, `i18n` 식별자/문서 등장 시
- 운영·디버깅: 동일 KPI 리포트 간 차이, 환율 스냅샷 불일치, 단위 혼재(g/kg/lb), 휴일 미반영 배차
- 사용자 발화 예: "KST cutoff", "환율 스냅샷", "단위 변환", "로케일", "휴일 캘린더"

## 점검 포인트

1. **시스템 표준 timezone** — 저장은 UTC, 표시·집계는 tenant 또는 사용자 timezone, 변환 단일 진입점?
2. **cutoff 정책** — 일·월 마감 cutoff 시점(KST 23:59 vs UTC 14:59), 리포트 차이 회피, calendar 경계 처리?
3. **DST 처리** — DST 적용 국가(미·EU)의 transition 시 중복/공백 timestamp 처리?
4. **통화·환율 매트릭스** — base currency, 환율 source(한국은행·ECB·OANDA), 스냅샷(주문일 vs 출고일 vs 정산일) 명시?
5. **통화 변환 정밀도** — 환산 시 자릿수, 반올림 정책, 누적 차이 추적?
6. **단위 metric vs imperial** — kg/lb, m/ft, m³/ft³, ℃/℉, 변환 시 라운드 정책, 외부 캐리어 단위와 매핑?
7. **locale 포맷** — 숫자(1,234.56 vs 1.234,56)·날짜(YYYY-MM-DD vs DD/MM/YYYY)·통화 기호 표시 - tenant/사용자별?
8. **휴일·이벤트 캘린더** — 한국(설/추석/임시공휴일)·중국(춘절·국경일·광군제)·미국(추수감사절·블프)·EU(EU 휴일)·이슬람(라마단)?
9. **휴일 영향 매트릭스** — cutoff 변경·배차 가능/불가·세관 휴무·은행 휴무 - 운영 캘린더에 반영?
10. **다국어 라벨·문서** — 인보이스·라벨·이메일 다국어 템플릿, 번역 quality·검증?
11. **언어 fallback** — 누락 키 fallback, ICU MessageFormat 활용?
12. **PII 표시 locale** — 이름·주소 포맷 차이(한국 LastName first vs 영문), 마스킹 규칙도 locale별?
13. **이벤트 envelope timestamp** — `occurred_at` UTC + tz 메타, downstream consumer 변환 일관성?
14. **번역 거버넌스** — terminology(→ `logistics-glossary`) 단일 source, 번역 갱신 cycle?

## 응답 형식

- 질문 → 타임존/통화/단위/휴일 매트릭스·표준
- 리뷰 → 약점·KPI 차이·이벤트 timestamp 위험
- 마감 차이·환율 스냅샷 위험 별도 강조

## Hand-off

- KPI 산식·formulas → `logistics-kpi`
- 용어·i18n 키 → `logistics-glossary`
- tenant residency·휴일 캘린더 → `logistics-multitenancy`
- 이벤트·로그 timestamp → `logistics-observability`/`logistics-event-schema`
- 통관 환율 → `logistics-compliance`/`logistics-settlement`
- 라벨 다국어 → `carrier-edi`/`oms-fulfillment`
