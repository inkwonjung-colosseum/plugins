---
name: ssot-audit
description: Use when SSOT-marked Markdown folders need structure, content, or backlog audit.
---

# ssot-audit

Audit the current project's declared SSOT Markdown corpus. Does not review a new planning artifact; never edits files.

## Inputs

- Options: `--ssot-include`, `--exclude`, `--axes <structure,content>`, `--no-follow-links`, `--no-image`.
- SSOT candidates: folder path segment must contain independent `SSOT` token.
- Filename version gate: `(?i)v(\d+)\.(\d+)` last match `>= (0, 8)` semantic, or no version match. `v0.7` 이하 = `버전 미달`, excluded.
- Never fall back to all project Markdown when no SSOT token folder exists. Never auto-relax version cutoff.
- Always exclude: `planning/**`, `.planning-kit/**`, dependency/build/cache, internal plugin/skill docs.

## Workflow

Parse options → collect SSOT-token Markdown → classify roles/placeholders → follow links/images unless disabled → build in-memory SSOT map → run selected structure/content rules → merge duplicates → emit report-first audit with findings + backlog.

## Output Contract

- Start with `# ssot-audit`; no scan logs first.
- No scores, no health grades.
- No findings or recommendations = `없음`.
- Include exclusion summary + backlog even when audit cannot run.

## References

Read `references/runtime-contract.md` for edges. Load `structure-rules`, `content-rules`, `output-contract`, shared connector routing only when needed.
