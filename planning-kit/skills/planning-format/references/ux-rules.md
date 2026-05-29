# UX Rules

Load when filling feature design sections 8 (persona / journey), 13 (UX writing), 14 (design system).

## Persona (8.1)

- Each persona has a real-context role (department, seniority, daily tool stack).
- Goals are jobs-to-be-done phrased as "When [situation], I want to [motivation], so I can [outcome]".
- Pain points cite either a source artifact (interview note, support ticket, NPS comment) or `[TBD]` with a checklist item.
- Mark Primary vs. Secondary; Primary drives default flows, Secondary informs edge cases.
- Tie persona to one or more journey rows in 8.2 by name.

## Journey map (8.2)

- Cover at least Awareness, Entry, Use, Completion, Post (회귀) stages. If a stage is omitted, that row must carry `[scope-out: <사유>]`; bare empty stage row is an F1 finding.
- Each row includes user action, user thought (verbatim or paraphrased), emotion / satisfaction (integer 1-5), touchpoint (channel + system), pain point, opportunity, and the mapped FUNC ID. Non-numeric emotion is an F1 finding.
- Opportunity entries must be actionable, not aspirational.
- Negative-emotion rows (<= 2/5) cascade into a self-review F9 risk item or RSK entry.

## UX writing (13.1)

- Voice choice (정중 / 친근 / 단호) applies consistently across surfaces.
- Prefer active voice; passive only when the subject is unknown or sensitive.
- Length budgets:
  - Button label <= 4 words, ideally 1-2.
  - Toast / snackbar <= 2 sentences, auto-dismiss safe.
  - Inline error 1-2 sentences with cause + fix.
  - Modal title <= 8 words; modal body 1-3 short sentences.
- Order in error messages: what happened -> why -> what to do next.
- Banned-word list: vague apologies without action, jargon without translation, blame ("you did wrong"), techno-noise ("error code 0x42").
- Banned-word seed bank (확장 가능, project별 추가 허용):
  - Korean: `죄송합니다만`, `시스템 오류가 발생하였습니다`, `잘못된 요청입니다`, `알 수 없는 오류`, `다시 시도해주세요` (단독 사용), `처리 중 문제가 발생했습니다` (원인·후속 행동 없음).
  - English: `Oops`, `Something went wrong`, `Unknown error`, `Invalid input` (no detail), `Please try again` (no cause).
  - 사용 시 반드시 원인 + 다음 행동을 함께 제공해야 함.
- Honorific / pronoun rule documented per persona.

## Message catalog (13.2)

- For each row, provide Korean and English (or each supported locale) with character / line limits.
- Include CTA / next-action label so the message is action-complete.
- Destructive confirms must repeat the object name and consequence and require explicit action.
- Permission-denied messages explain who to contact, not what code was thrown.

## Design system (14)

- Component selection rules:
  - Single primary action per screen; secondary actions use Link or ghost button.
  - Toast for non-blocking confirmation (auto-dismiss). Banner for persistent advisory. Modal only when work must stop.
  - Skeleton over spinner when content shape is predictable.
  - Empty state always pairs illustration / icon + one-line explanation + primary action.
- Token discipline: never hardcode color, spacing, radius, or shadow; always reference design tokens.
- When overriding a token (e.g., brand accent), re-check contrast against NFR 12.4 baseline.
- Component code mapping: cite the Code Connect entry or repo path when available.

## Cross-checks

- Persona attributes referenced in 13 (writing tone) and 14 (component density) must trace back to 8.1.
- Journey opportunities should appear as FUNC, AC, or RSK entries; orphan opportunities are findings.
- Locale list in 13.2 matches NFR 12.4 supported locales.
