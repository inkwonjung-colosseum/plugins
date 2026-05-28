---
name: grill-with-docs
description: Use when grilling plans against CONTEXT.md and ADRs.
license: MIT
---

# Grill With Docs

Interview the user about a plan until shared understanding emerges. Ask one question at a time and include your recommended answer.

## Process

1. Read `CONTEXT.md`, `CONTEXT-MAP.md`, and relevant ADRs.
2. Explore code instead of asking when code can answer.
3. Challenge glossary conflicts and sharpen vague terms.
4. Stress-test domain relationships with edge cases.
5. Update `CONTEXT.md` when a term is resolved.
6. Offer ADRs only for hard-to-reverse, surprising tradeoffs.

Create files lazily. If no `CONTEXT.md` exists, create it only when the first term is resolved; if no `docs/adr/` exists, create it only when the first ADR is accepted.
