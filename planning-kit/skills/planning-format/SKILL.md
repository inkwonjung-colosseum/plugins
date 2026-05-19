---
name: planning-format
description: Use when a draft, file, folder, URL, or image must become Korean policy and feature design documents.
---

# planning-format

Turn one planning input into a policy document and a feature design document.

## Inputs

- Required positional input: draft text, file path, directory path, image path, or one or more `https?://` URLs.
- Options: `--save` (default/no-op alias), `--no-save`, `--no-fetch`, `--no-image`, `--no-self-review`.
- Mixed URL and non-URL tokens are treated as text input. `file://`, `ftp://`, `mailto:`, and scheme-less strings are not URL mode.
- Compatibility marker: `[--no-save]`, `--save`, 옵션이 없으면 저장, 0.2.x 호환용 no-op alias.

## Workflow

Dispatch input, collect linked sources, fetch breadth-first unless disabled, merge bodies, convert through templates, self-review unless disabled, then save by default under `planning/[safe-feature-name]--YYYY-MM-DD-HHMMSS/`. `--no-save` prints both documents. Output starts with `# [feature-name]`.

## Output Contract

- Save success: header summary -> `## 저장 파일` -> `## 체크해야 할 항목`.
- `--no-save`: header summary -> `## 정책서` -> `## 기능설계서` -> `## 체크해야 할 항목`.
- Save failure: print both full documents and `## 저장 실패 상세`.
- `planning/**` output may be reviewed or published later, but it is never SSOT evidence.
- Use clean display labels such as `정책서 5.1`, not legacy section symbols.

## References

Read `references/runtime-contract.md` for edge cases. Load `connector-routing`, `conversion-rules`, `exclusion-rules`, `self-review-rules`, `output-contract`, and the two templates only when that detail is needed.
