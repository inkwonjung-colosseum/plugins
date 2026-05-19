---
name: planning-review
description: Use when policy and feature design documents need SSOT, acceptance criteria, or dependency impact review.
---

# planning-review

Review `planning-format` output. This skill does not create or auto-fix documents.

## Inputs

- No arguments: use the previous `planning-format` output or its `## 저장 파일` handoff.
- One or more `https?://` URLs: fetch each as a root review source.
- One directory: find policy and feature design files in that directory.
- One file: same-folder companion read; scan sibling text files and supported images non-recursively to identify the pair.
- Two non-URL paths: identify policy and feature design by file name or heading.
- Otherwise: treat input as pasted Markdown text.
- Options: `--ssot-include`, `--no-input-fetch`, `--no-input-image`, `--no-ssot-fetch`, `--no-ssot-image`.
- Review axes run as one consolidated pass; axis-selection is not a public option.
- Handoff marker: Step 1.1.3 planning-format 기본 저장 출력 handoff (0.2.14); `## 저장 파일`; exactly one `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` folder.
- Exclusion marker: 직전 출력의 `## 체크해야 할 항목`, `## 출처/누락 요약`, `## 상세 추적`, `## 저장 실패 상세`는 review 대상 본문에 합류하지 않는다.
- SSOT marker: `planning/**`은 계속 기준 문서 묶음 근거에서 제외.

## Workflow

Identify exactly one policy body and one feature design body; stop if ambiguous. Keep review inputs separate from SSOT evidence. Use only SSOT-marked folders as evidence, never `planning/**` or `.planning-kit/**`. Run the three review axes in one main pass, merge duplicates by `R1 > R3 > R2`, then report verdict, confidence, conclusion, findings, checklist, evidence summary, and trace when needed.

## Output Contract

- Start with `# [feature-name] 검토 결과`; do not print progress logs first.
- Do not wrap the whole report in a code fence.
- Show `## 결론` before detailed findings.
- Put unresolved decisions and document work in `## 체크해야 할 항목`.
- Keep raw R* finding IDs in `## 상세 추적`, not the top summary.
- Use clean display labels; do not leak internal terms such as `SSOT corpus`, `fetch`, or `connector fallback`.

## 출력 포맷

Required visible order marker: `# [기능명] 검토 결과`, `## 결론`, `## 검토 결과`, `## 체크해야 할 항목`.

### 최종 clean-display 정규화

## References

Read `references/runtime-contract.md` for parser and output edge cases. Load `ssot-rules`, `ac-rules`, `deps-rules`, and shared planning-format fetch/image references only when needed.
