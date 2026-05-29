---
name: planning-format
description: Use when a draft, file, folder, URL, or image must become Korean 정책서 and 기능설계서 with full PM, BA, UX, technical, and QA detail.
---

# planning-format

Convert one planning input into 정책서 + 기능설계서 covering strategy, traceability, UX, spec, and QA.

## Inputs

- Positional: text, file, directory, image, or `https?://` URLs.
- Options: `--save` (default), `--no-save`, `--no-fetch`, `--no-image`, `--no-self-review`.
- Mixed URL and non-URL tokens = text input. `file://`, `ftp://`, `mailto:`, scheme-less = not URL mode.

## Workflow

Dispatch → collect → fetch BFS unless disabled → merge → convert via templates → self-review unless disabled → save by default under `planning/[safe-feature-name]--YYYY-MM-DD-HHMMSS/`. Output starts with `# [feature-name]`.

## Output Contract

- Save success: header → `## 저장 파일` → `## 체크해야 할 항목`.
- `--no-save`: header → `## 정책서` → `## 기능설계서` → `## 체크해야 할 항목`.
- Save failure: both bodies + `## 저장 실패 상세`.
- `planning/**` is never SSOT evidence.

## References

Load on demand by step:

- `references/runtime-contract.md` — dispatch, save, output edges.
- `references/connector-routing.md` — URL fetch, connector fallback.
- `references/conversion-rules.md` — image, merge, mapping, template, requirement IDs.
- `references/exclusion-rules.md` — unmapped input, `[TBD]`, omission.
- `references/self-review-rules.md` — F1-F12 (F11 strategy, F12 roadmap).
- `references/output-contract.md` — save handoff, checklist, response shape.
- Section rules: `business-rules.md` (정책서 1, 10-14), `specification-rules.md` (기능설계서 10-11), `nfr-rules.md` (12), `ux-rules.md` (8, 13-14), `qa-rules.md` (9, 15-17).
- `templates/정책서.md`, `templates/기능설계서.md` — Step 6 generation.
