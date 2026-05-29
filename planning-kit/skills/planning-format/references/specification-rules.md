# Specification Rules

Load when filling feature design sections 10 (data), 11 (API/event), or producing ERD / API contracts. Goal: make output implementable without follow-up questions to the planner.

## Data model (section 10)

- Each `DATA-XXX` lists attribute name, type (with size where applicable: `varchar(64)`, `decimal(18,4)`), required flag, default, and constraints (`NOT NULL`, `UNIQUE`, `CHECK`, `FK -> Entity.field`).
- Identify PK and candidate keys explicitly. FK must name target entity.
- Relationship must include cardinality (`1:1`, `1:N`, `M:N`) and optionality (`mandatory` / `optional`).
- Lifecycle row required: created-by trigger, update events, terminal state (delete vs. soft delete vs. archive).
- Retention row required when PII or compliance applies; cite the policy authority.
- Migration note: when entity replaces or extends a prior schema, list source schema, backfill method (script / dual-write / online migration), and rollback safety.
- Index / query pattern: list expected predicates and sort orders; flag high-cardinality columns and range scans.
- Partition / sharding key: required when projected row count > 100M, hot-key risk is documented, OR multi-tenant data isolation is in scope (Day-1 decision for tenant-isolated SaaS).

## ERD (section 10.3)

- Prefer Mermaid `erDiagram` inline fenced block for portability. Use DBML when DB-engine specific syntax is required.
- Include only entities introduced in section 10. Auxiliary entities go to a separate fenced block.
- Notation: `PK` for primary key, `FK` for foreign key, `*` for required, relationship lines indicate cardinality. Document any non-standard notation in 10.3 preamble.
- When ERD exceeds 12 entities, split into core + sub-graph(s) and link with cross-reference text.

## Synchronous API (section 11.1)

- Each `API-XXX` for HTTP/gRPC documents: method, path, auth scheme (and policy section 7 role), request schema with examples, response schemas for success and error, error code table (HTTP + domain code + user message + retryability), idempotency contract, retry policy (where, interval, max attempts, backoff, jitter), rate limit / quota, pagination & filter contract, version & deprecation (sunset header + supported window).
- Idempotency: if endpoint is non-GET and may be retried, state the idempotency key header, dedup window, and storage scope (per-tenant, per-user).
- Backward compatibility: state breaking-change rules (semver), deprecation grace period, and consumer notification channel.

## Asynchronous event (section 11.2)

- Each `API-XXX` for event/webhook documents: transport (Kafka / SQS / SNS / Webhook), topic or queue name (with naming convention), producer service, consumer services, envelope schema (`event_id`, `type`, `version`, `occurred_at`, `body`), partition / ordering key, delivery semantics (at-least-once is default unless justified), consumer-side idempotency strategy, retry & DLQ policy with alert wiring, schema registry compatibility mode (backward / forward / full).
- Sequence guarantees: state whether order is per-key, per-partition, or none. Cross-topic ordering requires saga or correlation contract — document it.
- Failure propagation: define poison-pill handling, DLQ retention, and replay procedure.
- Field-level schema evolution rule: additive-only, optional-with-default, no-remove-within-deprecation-window. Any breaking field change is a new event version (semver `type@major.minor`).

## Cross-section coherence

- API request/response field names align with the data model attribute names where they refer to the same concept.
- State transitions cited in API responses match feature 10.2 and policy section 6.
- Event payloads carry enough fields for consumer projections defined in feature 16 (observability).
- When the same business entity drives both data partition (section 10.1) and event partition key (section 11.2), the key derivation must be identical or explicitly mapped (cite the source field).
