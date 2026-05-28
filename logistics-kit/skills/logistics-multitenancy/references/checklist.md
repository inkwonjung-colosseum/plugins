# logistics-multitenancy 도메인 참조

## 활용 시점

- 자문: tenant 격리 모델, RLS 정책, quota·rate limit, 비용 attribution 수립
- 코드·정책 리뷰: `tenant_id`, `multitenancy`, `rls`, `row_level_security`, `tenant_key`, `noisy_neighbor`, `quota`, `rate_limit`, `tenant_isolation` 식별자가 보일 때
- 운영·디버깅: tenant 데이터 교차 누출, noisy neighbor으로 SLA 위반, 비용 추적 불일치
- 사용자 발화 예: "tenant 격리", "3PL 멀티테넌시", "RLS", "noisy neighbor", "quota"

## 점검 포인트

1. **격리 모델 결정 트리** — shared schema(row + tenant_id) / schema-per-tenant / DB-per-tenant — 보안·운영·성능·비용 트레이드오프?
2. **tenant_id 전파** — HTTP header / JWT claim / API path, 모든 쿼리·이벤트·로그에 tenant_id 자동 주입?
3. **RLS 정책** — Postgres RLS·필드 보안, 우회 불가 보장, super admin escape hatch 격리?
4. **암호화 키 분리** — tenant별 KMS 키(envelope encryption), rotation·revocation 절차?
5. **noisy neighbor 격리** — DB connection pool·CPU·메모리·queue 단위 quota, 격리 실패 시 fallback?
6. **quota·rate limit** — API req/s, 동시 작업·bulk 한도, 초과 시 4xx vs 큐잉, soft/hard limit 차이?
7. **비용 attribution** — tenant별 컴퓨트·스토리지·네트워크 비용 측정, billing 산정 매핑?
8. **schema 변경(migration)** — schema-per-tenant 시 N개 schema 일괄 마이그레이션, 부분 실패 대응?
9. **백업·복원 격리** — tenant 단위 PITR, 단일 tenant 복원 시 다른 tenant 영향 차단?
10. **데이터 internationalization** — tenant별 region·data residency(KR·EU·US) 선택, cross-border 정책(→ `data-privacy-logistics`)?
11. **tenant onboarding/offboarding** — 신규 tenant 프로비저닝 자동화, off-boarding 시 데이터 영구 삭제·인증서?
12. **tenant 메타데이터** — feature flag·SLA tier·시간대·통화·언어 등 별도 tenant config service?
13. **테스트 격리** — 통합·E2E 테스트 격리(이상 tenant 누출 방지), prod 데이터 노출 차단?

## 응답 형식

- 질문 → 격리 모델·RLS·quota·비용 attribution
- 리뷰 → 약점·교차 누출·과징금 위험
- 데이터 잔존·교차 누출 위험 별도 강조

## Hand-off

- ERD·tenant_id 컬럼 정책 → `logistics-data-model`
- PII·data residency → `data-privacy-logistics`
- 관측성·tenant 별 SLO → `logistics-observability`
- 채널·marketplace sync → `channel-sync`
- 백업·복원 → `logistics-dr`
- 한도 알림·DLQ → `resilience-patterns`/`bulk-operations`
