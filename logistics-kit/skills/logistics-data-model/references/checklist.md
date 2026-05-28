# logistics-data-model 도메인 참조

## 활용 시점

- 설계 자문: 마스터 vs 트랜잭션 분리, 재고 이력 표현, SCD type, 이벤트 소싱, 파티셔닝, 감사 로그
- 코드·스키마 리뷰: `*.dbml`, `*.sql`, `*migration*`, `*.prisma`, `*entity*`, `*schema*` 파일이 등장할 때
- 운영·디버깅: 재고 차이 조사, 마이그레이션 백필 영향, soft delete 누수
- 사용자 발화 예: "ERD 검토", "재고 이력 테이블", "SCD 적용", "이벤트 소싱", "감사 로그", "파티셔닝"

## 점검 포인트

1. **마스터 vs 트랜잭션** — SKU/Location/Carrier 마스터(소량/저변경) vs 재고/주문/배송 트랜잭션(대량/고변경) 분리?
2. **재고 이력 표현** — 스냅샷(매일) vs 트랜잭션 로그(in/out) vs 둘 다? 재고 차이 조사 가능?
3. **SCD type** — 마스터 변경(예: 운임표 갱신)이 SCD type 2(이력 보존) vs type 1(덮어쓰기)? Effective date 컬럼?
4. **이벤트 소싱 후보** — 주문/배송/재고 트랜잭션처럼 상태 전이가 핵심인 도메인은 이벤트 로그 + projection 패턴 고려.
5. **감사 로그** — `created_at/updated_at/created_by/updated_by`만으로 부족. 조정·삭제·승인 시 별도 audit table 필요.
6. **파티셔닝 키** — 재고 트랜잭션은 시간 또는 location 기반. 쿼리 패턴과 일치?
7. **soft delete** — 주문/재고는 hard delete 금지. `deleted_at` + 모든 쿼리 필터 일관성?
8. **tenant_id 컬럼 정책** — 모든 tenant-scoped 테이블에 `tenant_id` not-null + composite PK, FK 일관성, RLS 적용 (→ `logistics-multitenancy`)
9. **파티셔닝 by tenant + time** — `(tenant_id, occurred_at)` 복합 파티션, noisy neighbor 격리
10. **inventory snapshot 테이블** — 일·시간 단위 snapshot + event log replay로 임의 시점 복구 (→ `logistics-dr`)
11. **CDC source-of-truth markers** — outbox·debezium용 CDC 컬럼(`_lsn`, `_op_type`, `_committed_at`), retention 정책
12. **audit log immutability** — append-only, hash chain·trusted timestamping, hard delete 금지 검증
13. **PII column tagging** — 컬럼 단위 PII tag·마스킹 정책·복호화 권한 (→ `data-privacy-logistics`)
14. **MDM 마스터 lifecycle** — effective_date·end_date·current_flag, supersession (→ `mdm-reference-data`)
15. **이벤트 소싱 + projection** — 명시적 이벤트 모델 vs 트랜잭션 로그 + projection, snapshot+replay 패턴

## 응답 형식

- 질문 → 표준 모델 패턴·트레이드오프·예시 DDL/ERD
- 리뷰 → 모델 약점·권장 패턴·예시 DDL 또는 ERD 패치
- 마이그레이션 영향(데이터 백필 필요 여부) 평가 포함

## Hand-off

- 도메인 비즈니스 규칙 → `wms-inventory`/`oms-fulfillment`
- 이벤트 스키마·outbox → `logistics-event-schema`
- 컨슈머 멱등성 → `logistics-idempotency`
- tenant 격리·RLS → `logistics-multitenancy`
- 마스터·MDM lifecycle → `mdm-reference-data`
- DR·snapshot → `logistics-dr`
- PII·마스킹 → `data-privacy-logistics`
- 관측성·CDC 메타 → `logistics-observability`
