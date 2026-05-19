---
name: planning-publish-confluence
description: Use when current context or a planning output folder must publish v0.7 Confluence candidate pages.
---

# planning-publish-confluence

Publish one policy document and one feature design document to Confluence as `v0.7` candidate pages.

## Inputs

- No arguments: find the two publishable bodies in current context memory.
- One folder: accept only `planning/[safe-feature-name]--YYYY-MM-DD-HHMMSS/` with canonical policy and feature design files directly inside it.
- Reject URLs, arbitrary Markdown files, multiple folders, nested planning paths, options, and any path outside `planning/`.
- Forbidden inputs stop before local file reads, URL fetches, connector fallback, Confluence lookup, or parent questions.
- Compatibility marker: argument-hint: "(인자 없음 | [planning/[안전기능명]--YYYY-MM-DD-HHMMSS/])"; 현재 context memory; 지원 입력; 명시적 저장 폴더 입력; canonical 정책서·기능설계서 두 파일만; URL; 임의 `.md`.

## Workflow

Gate input before Confluence lookup. Ask parent choice, preflight the parent and update targets, prepare the `v0.7` container and two child pages, ask final confirmation, then write container -> policy -> feature design with readback after each step. Never move pages, batch publish, blind overwrite, append update, or auto-rollback.

Step markers: Step 1: 입력 dispatch와 금지 입력 확인; Confluence page create/update; Step 7: write 실행과 readback.

## Output Contract

- Start with `# planning-publish-confluence`.
- Distinguish success, partial completion, no change, and cancellation.
- Include page ids, URLs, versions, operation id, and readback status.

## References

Read `references/runtime-contract.md` for edge cases. Load `context-gate`, `confluence-page-contract`, and `output-contract` only when needed.
