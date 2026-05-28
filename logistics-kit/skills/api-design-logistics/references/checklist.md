# api-design-logistics 도메인 참조

## 활용 시점

- 자문: 프로토콜 결정(REST/gRPC/GraphQL), async 패턴, pagination, versioning, webhook 표준
- 코드·인터페이스 리뷰: `openapi`, `swagger`, `rest`, `grpc`, `graphql`, `webhook`, `pagination`, `cursor`, `versioning`, `hmac`, `signature`, `error_envelope` 식별자/문서 등장 시
- 운영·디버깅: 호환성 깨짐, webhook 위변조 의심, pagination 누락·중복, partial 응답 불일치
- 사용자 발화 예: "REST vs gRPC", "webhook signing", "pagination", "API versioning", "OpenAPI"

## 점검 포인트

1. **프로토콜 결정** — REST(공개·범용·캐싱) / gRPC(내부 고성능·streaming) / GraphQL(다중 client·과수집 회피) 매칭?
2. **resource·verb·URI** — 명사 중심·복수형(`/orders/{id}`), 행위는 POST + sub-resource(`/orders/{id}/cancel`) 정책?
3. **pagination** — cursor(opaque) vs offset, 깊은 페이지 안전, `next`·`prev` 링크, count 별도 endpoint?
4. **filtering·sorting·partial response** — `?filter[]=...&sort=field&fields=a,b`, JSON:API 호환 옵션?
5. **versioning** — URI(`/v1/`) vs header(`Accept-Version`) vs media type, deprecation 정책·sunset header?
6. **async 패턴** — long-polling / callback / webhook / SSE / WebSocket / Server-Sent — 사용 사례 매칭?
7. **webhook signing** — HMAC-SHA256 over body + timestamp + replay window, secret rotation, 재시도 시 같은 signature?
8. **멱등성 키** — POST/PUT 부작용에 `Idempotency-Key` header, TTL·응답 캐싱(→ `logistics-idempotency`)?
9. **error envelope** — `{ code, message, details[], correlation_id }`, RFC 9457 problem detail 호환?
10. **rate limit·throttle** — `X-RateLimit-*` header, 429 + retry-after, tenant·user·IP·route 별 분기?
11. **인증·인가** — OAuth 2 / JWT (claims tenant·scope), API key per partner, mTLS 옵션?
12. **OpenAPI 거버넌스** — spec-first, lint(Spectral), 호환성 매트릭스(BACKWARD), client SDK 자동생성?
13. **content negotiation** — JSON 기본, CSV/XML 옵션, compression(gzip·brotli)?
14. **외부 webhook 수신** — 멱등성·서명 검증·delivery retry·DLQ 전파(→ `carrier-edi`)?

## 응답 형식

- 질문 → 결정 트리·표준·예시 spec
- 리뷰 → 약점·호환성·서명 누락 위험
- 호환성·서명 위변조 위험 별도 강조

## Hand-off

- 멱등성/dedup → `logistics-idempotency`
- 캐리어 EDI/webhook → `carrier-edi`
- 채널 marketplace API → `channel-sync`
- 멀티테넌시·tenant header → `logistics-multitenancy`
- 이벤트 envelope → `logistics-event-schema`
- 관측성·rate-limit alert → `logistics-observability`
- 보안·OAuth scope → `data-privacy-logistics`
