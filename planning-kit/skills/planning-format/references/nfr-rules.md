# NFR Rules

Load when filling feature design section 12 (NFR). Every NFR must be measurable; "fast", "secure", "scalable" alone is a self-review F9 finding.

## Performance (12.1)

- State p50 / p95 / p99 latency targets in milliseconds with the measurement boundary (gateway, service, end-to-end).
- State throughput target with units (TPS / RPS / messages per second).
- State concurrent-user target for baseline and peak.
- Spike behavior: scale trigger metric, scale ceiling, queue-and-shed policy.
- Test method: load profile, ramp pattern, expected steady-state duration.

## Availability / reliability (12.2)

- Convert availability % to allowed downtime (99.9% = 43m/month, 99.95% = 21m/month, 99.99% = 4.3m/month).
- Define error budget consumption policy.
- RTO / RPO numeric values.
- Failure containment: per-call timeout, circuit-breaker thresholds, bulkhead boundaries, deadline propagation.
- Distributed transaction strategy: saga compensation, outbox pattern, or two-phase commit with cost note.

## Security / privacy (12.3)

- Apply STRIDE threat modeling and list at least one identified threat plus a mitigation for each applicable category. Each identified STRIDE threat must map to at least one `TEST-XXX` (security or chaos scenario) or a named operational drill; non-numeric mitigations are not exempt from the F9 traceability rule.
- Authentication: scheme (OAuth2 / OIDC / mTLS / API key), MFA requirement, session policy (idle timeout, absolute timeout, re-auth on sensitive ops).
- Authorization: cite the policy section 7 role; specify enforcement point (gateway / service / data layer).
- PII classification (identifier / quasi-identifier / sensitive). Encryption: TLS 1.2+ in transit, AES-256 at rest, key management (KMS, rotation cadence).
- Masking and anonymization rule per field, including log and analytics surfaces.
- Audit log: in-scope actions, retention period, who can read.
- Security testing: SAST / DAST cadence, dependency scanning, pen-test cadence.

## Accessibility / i18n (12.4)

- WCAG conformance level (A / AA / AAA) with these baseline numbers when AA is chosen:
  - Body text contrast ratio >= 4.5:1, large text (>= 18pt or >= 14pt bold) >= 3:1, UI components / graphical objects >= 3:1.
  - Minimum touch target 44x44 CSS px on mobile.
  - Keyboard reachable for every interactive element; visible focus indicator >= 3:1.
  - Tab order matches logical reading order.
- Screen reader: ARIA role / state / property contract per non-native widget; live region for async updates.
- Motion: respect `prefers-reduced-motion`; auto-playing content must have pause control.
- Internationalization: supported locales, translation key namespace, ICU plural / select rules, pseudo-localization test.
- Locale formatting: date, time, number, currency, address; timezone storage (UTC) and display rule.
- RTL: list mirrored components and assets; bidi-text handling in form fields.
- Validation tools: axe, Lighthouse, manual NVDA / VoiceOver script.

## Operations / scalability (12.5)

- Scaling: horizontal target instances, vertical limits, autoscale metric (CPU, RPS, queue depth) and cooldown.
- Deployment: canary or blue-green steps with traffic percentage and bake time at each step.
- Rollback: trigger metric thresholds, automatic vs. manual, recovery time target.
- Feature flag / kill switch: default state, kill condition, escalation owner.
- Data migration: online vs. offline, dual-write window, cutover trigger, backfill verification query, rollback-safe checkpoint.
- Environment parity: list dev / staging / prod differences (data scale, secrets, traffic shape).
