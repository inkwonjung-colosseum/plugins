---
name: improve-codebase-architecture
description: Use when reviewing architecture or deepening modules.
license: MIT
---

# Improve Codebase Architecture

Find architectural friction and propose deepening opportunities: shallow modules becoming deep modules.

## Vocabulary

Use: module, interface, implementation, depth, deep, shallow, seam, adapter, leverage, locality. Avoid component, service, API, and boundary when these apply.

## Process

1. Read `CONTEXT.md`, `CONTEXT-MAP.md`, and relevant ADRs first when they exist.
2. Look for file-bouncing, shallow pass-throughs, low locality, leaky seams, and hard tests.
3. Apply the deletion test: if complexity vanishes, the module is shallow.
4. Classify dependencies: in-process, local-substitutable, owned remote, or external.
5. Write a short HTML report in the OS temp directory with candidates and before/after diagrams.
6. After the user picks a candidate, grill constraints, seam placement, adapters, and tests.

When domain terms are resolved during the conversation, update `CONTEXT.md` inline. Offer ADRs only for decisions that are hard to reverse, surprising without context, and based on a real tradeoff.

Keep report prose concise. The diagram should carry the architectural explanation.
