---
name: ssot-audit
description: Use when SSOT-marked Markdown folders need structure, content, or backlog audit.
---

# ssot-audit

Audit the current project's declared SSOT Markdown corpus. This skill does not review a new planning artifact and does not edit files.

## Inputs

- Options: `--ssot-include`, `--exclude`, `--axes <structure,content>`, `--no-follow-links`, `--no-image`.
- SSOT candidates must live under folder path segments with an independent `SSOT` token.
- Never fall back to all project Markdown when no SSOT token folder exists.
- Always exclude `planning/**`, `.planning-kit/**`, dependency/build/cache output, and internal plugin/skill docs from corpus evidence.

## Workflow

Parse options, collect only SSOT-token Markdown, classify roles/placeholders, follow links/images unless disabled, build an in-memory SSOT map, run selected structure/content rules, merge duplicates, then output a report-first audit with findings and backlog.

## Output Contract

- Start with `# ssot-audit`; do not print scan logs first.
- Use no scores or health grades.
- If there are no findings or recommendations, print `없음`.
- Include exclusion summary and backlog even when audit cannot run.

## References

Read `references/runtime-contract.md` for edge cases. Load `structure-rules`, `content-rules`, `output-contract`, and shared connector routing only when needed.
