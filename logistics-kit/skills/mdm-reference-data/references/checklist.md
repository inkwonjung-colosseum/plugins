# mdm-reference-data 도메인 참조

## 활용 시점

- 자문: 마스터·참조 데이터 lifecycle, effective date, supersession, 외부 sync, 거버넌스 수립
- 코드·정책 리뷰: `mdm`, `master_data`, `reference_data`, `tariff`, `zone`, `hs_code`, `currency`, `holiday_calendar`, `carrier_master`, `effective_date`, `supersession`, `scd2` 식별자/문서 등장 시
- 운영·디버깅: 운임 갱신 적용 시점 차이, HS 코드 변경 누락, 환율 동기 지연, 캐싱 stale
- 사용자 발화 예: "MDM", "운임표 갱신", "HS 코드 sync", "effective date", "휴일 캘린더"

## 점검 포인트

1. **참조 도메인 catalog** — tariff·zone·HS·UN/DG·CN-code·incoterms·통화·환율·휴일·캐리어 마스터·SLA tier — 단일 source?
2. **lifecycle** — draft → reviewed → approved → effective → expired / superseded, 전이 권한 매트릭스?
3. **effective date 모델** — 시작일·종료일·tenant·scope, 시점 검색 함수, overlap 검출?
4. **SCD type 2** — 이력 보존, 현재(current_flag), 미래 예약(future), 과거 조회 일관성?
5. **외부 sync 매트릭스** — 관세청(HS·환율), KOTRA, 통계청, 한국은행(환율) — 빈도·인증·실패 fallback?
6. **거버넌스** — domain owner·승인자·검토 cycle, 4-eyes 원칙, 변경 audit log immutability?
7. **이벤트 전파** — 마스터 변경 시 이벤트 발행(예: `mdm.tariff.updated`), 소비자 캐시 invalidation?
8. **캐시 invalidation** — TTL vs event-driven invalidation, 부분 무효화(키 단위), stale 허용 윈도우?
9. **계약·tenant override** — 글로벌 마스터 + tenant·계약 별 override, precedence 룰?
10. **이력 비교·diff** — 변경 전후 diff 확인, rollback 절차?
11. **외부 source 변경 알림** — 관세청 발효일 사전 안내, 자동 import + 검수 워크플로?
12. **dependency map** — tariff 변경이 quote·정산·KPI에 미치는 영향 자동 추적?
13. **데이터 품질** — 결측·중복·이상치 검증 규칙, 발견 시 차단/경고?

## 응답 형식

- 질문 → 도메인 catalog·lifecycle·effective date·거버넌스
- 리뷰 → 약점·sync 지연·invalidation 누락 위험
- 운임·HS 변경 미반영으로 인한 회계·통관 위험 별도 강조

## Hand-off

- ERD·SCD 모델 → `logistics-data-model`
- HS·관세 외부 마스터 → `logistics-compliance`/`fta-origin`
- 이벤트 전파·outbox → `logistics-event-schema`
- 캐싱 invalidation·resilience → `resilience-patterns`
- 휴일·환율·로케일 → `localization-audit`
- 운임 quote·rating → `vrp-rating-engine`
- 정산 영향 → `logistics-settlement`
