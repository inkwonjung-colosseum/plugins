---
name: planning-publish-confluence
description: Use when current context or a planning output folder must publish v0.7 Confluence candidate pages.
---

# planning-publish-confluence

Publish one 정책서 + one 기능설계서 to Confluence as `v0.7` candidate pages.

## Inputs

- No arguments: find the two publishable bodies in current context memory.
- One folder: only `planning/[safe-feature-name]--YYYY-MM-DD-HHMMSS/` with canonical 정책서·기능설계서 files directly inside.
- Reject: URLs, arbitrary `.md`, multiple folders, nested paths, options, anything outside `planning/`.
- Forbidden inputs stop before local file reads, URL fetches, connector fallback, Confluence lookup, parent questions.
- argument-hint: `(인자 없음 | [planning/[안전기능명]--YYYY-MM-DD-HHMMSS/])`.

## Workflow

Gate input before Confluence lookup. Ask parent choice → preflight parent + update targets → prepare `v0.7` container + two child pages → ask final confirmation → write container → 정책서 → 기능설계서, readback after each. Never move pages, batch publish, blind overwrite, append update, or auto-rollback.

Step markers: Step 1 입력 dispatch + 금지 입력 확인; Confluence page create/update; Step 7 write 실행 + readback.

## Output Contract

- Start with `# planning-publish-confluence`.
- Distinguish success, partial completion, no change, cancellation.
- Include page ids, URLs, versions, operation id, readback status.

## References

Read `references/runtime-contract.md` for edges. Load `context-gate`, `confluence-page-contract`, `output-contract` only when needed.
