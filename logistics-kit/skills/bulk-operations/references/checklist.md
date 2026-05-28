# bulk-operations 도메인 참조

## 활용 시점

- 자문: chunking 단위, throttling, partial-failure 의미론, progress 추적, retry-storm 방지 정책 수립
- 코드·API 리뷰: `bulk`, `batch`, `mass`, `chunk`, `throttle`, `partial_failure`, `progress`, `bulk_job`, `csv_import`, `csv_export` 식별자/엔드포인트가 보일 때
- 운영·인시던트: bulk 작업 partial 실패 처리 불일치, retry-storm, 진행률 비표시, 데이터 불일치
- 사용자 발화 예: "대량 라벨", "대량 반품", "bulk 재고 조정", "CSV import", "partial failure"

## 점검 포인트

1. **API 디자인** — async job 생성 → polling/webhook progress → 결과 download (단일 sync vs job-based), idempotency-key 적용?
2. **chunk 단위** — N건 단위 chunk(예: 1000), DB transaction batch size, 외부 API rate-limit 매칭?
3. **partial-failure 의미론** — all-or-nothing(트랜잭션) vs best-effort(개별 성공/실패) — 사용자 의도 명시? 결과 매트릭스(`success`/`failed_with_reason`)?
4. **progress 캡처** — `total / processed / success / failed` 시계열, ETA 계산, UI 표시?
5. **재실행 안전** — bulk_job_id + item_id 키 dedup, 일부 성공 후 재실행 시 누락/중복 방지?
6. **throttling·retry-storm 방지** — 외부 의존(라벨 API·캐리어·PG) rate-limit, adaptive backoff, circuit breaker 결합?
7. **데이터 검증·dry-run** — bulk 적용 전 dry-run 모드(영향 미리보기), 위험 작업(삭제·조정) 의무?
8. **승인 절차** — 일정 규모 이상 bulk(예: 1만 건+) 별도 승인, 감사 로그 작성?
9. **결과 보관·archive** — 결과 파일 보관기간, PII 마스킹, 다운로드 만료?
10. **취소·일시중단** — 진행 중 작업 cancel·pause 가능? 부분 완료 상태 처리?
11. **백프레셔** — queue 깊이·worker 수 vs DB·외부 cap, 깊이 초과 시 enqueue 거절(429)?
12. **bulk reconciliation** — 종료 후 결과 ↔ 외부 system 상태 reconcile, 차이 알람?
13. **재시도 정책** — failed-only 재시도, max retries, dead-letter 격리?

## 응답 형식

- 질문 → chunk 모델·partial 의미론·progress·재실행
- 리뷰 → 약점·partial 실패 위험·retry-storm 위험
- 부분 적용·외부 rate-limit 위반 별도 강조

## Hand-off

- 멱등성/dedup → `logistics-idempotency`
- 복원·circuit breaker → `resilience-patterns`
- 관측성·progress dashboard → `logistics-observability`
- 채널 sync rate-limit → `channel-sync`
- 라벨 발행·voiding → `carrier-edi`
- 재고 트랜잭션 영향 → `wms-inventory`/`inventory-accuracy`
- 분개 게시(승인 한도) → `logistics-settlement`
