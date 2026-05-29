---
name: planning-review
description: Use when 정책서 and 기능설계서 need SSOT, acceptance criteria, or dependency impact review.
---

# planning-review

Review `planning-format` output. Never creates or auto-fixes docs.

## Inputs

- No arguments: prior `planning-format` output or `## 저장 파일` handoff (one `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/`).
- `https?://` URLs: each = root review source.
- One directory: find policy + feature design inside.
- One file: same-folder companion scan to identify the pair.
- Two non-URL paths: identify by filename or heading.
- Otherwise: pasted Markdown.
- Options: `--ssot-include`, `--no-input-fetch`, `--no-input-image`, `--no-ssot-fetch`, `--no-ssot-image`.
- SSOT marker: `planning/**` excluded. SSOT-tagged folders qualify only when filename version `>= v0.8` or no version.

## Workflow

Identify exactly one policy + one feature design body; stop if ambiguous. SSOT evidence = SSOT-marked folders only (never `planning/**` or `.planning-kit/**`). Run R1+R2+R3 in one pass; merge by `R1 > R3 > R2`.

Axes:
- R1: SSOT consistency.
- R2: each `AC-XXX` is Given-When-Then with measurement + mapped FUNC + TEST when present; NFR numeric; journey emotion 1-5; UX message rows include CTA + destructive-confirm object repetition.
- R3: policy↔feature ID cross-links resolve; data/API/event contracts close; risks/KPIs/roadmap trace to feature artifacts. Policy strategic completeness (mirrors F11/F12): BIZ-001 Owner+baseline+cadence; BIZ-002 falsification+learning loop; DEC-XXX do-nothing+trade-off+re-eval; section 11 Power×Interest+RACI+Approver 사인오프; section 14 phases DoR/DoD/milestone date/rollback metric+threshold.

## Output Contract

- Required order: `# [기능명] 검토 결과` → `## 결론` → `## 검토 결과` → `## 체크해야 할 항목`.
- No code fence wrapping; no progress logs first.
- Raw R* IDs only in `## 상세 추적`.
- Clean display labels; never leak `SSOT corpus`, `fetch`, `connector fallback`.

## References

Load `references/runtime-contract.md` for parser + output edges. Load `ssot-rules`, `ac-rules`, `deps-rules`, and shared planning-format fetch/image refs only when needed.
