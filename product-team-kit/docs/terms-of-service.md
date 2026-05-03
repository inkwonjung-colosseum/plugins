# product-team-kit Terms of Service

`product-team-kit` is a local workflow plugin for interactive planning, formatting planning input into 기능설계서 and 정책서 drafts, and reviewing those drafts with an evidence package before external publishing.

## Intended Use

Use this plugin to:

- Draft 기능설계서 and 정책서 documents from user-provided planning input.
- Create a 기획초안 through guided user questions before formatting.
- Record `[미정]`, `[가정]`, and confirmation questions without treating them as verified facts.
- Review draft evidence, decision scope, and execution readiness with `plan-review` before publishing through a separate external process.
- Produce a publish-readiness checklist for human review when `plan-review` returns `pass` or `conditional pass`.

## Limitations

- The plugin does not replace human product, legal, security, or operational approval.
- Project Docs SSOT Markdown or linked local resources may be outdated. Users remain responsible for confirming source freshness.
- The plugin should not be used to bypass team review policies.
- Codex interactive `plan-draft` uses Plan mode user-question tools when available, falls back to normal conversation when the current thread can continue, and returns a hold only for non-interactive execution where user answers cannot be collected.

## Publishing Rules

This plugin does not publish directly to external systems. The `publish_readiness` output is a readiness checklist only. If a draft includes `[가정]`, confirmation questions, conflict warnings, decision-scope gaps, or execution-readiness gaps, users should run `plan-review`, review the evidence package and gate result, and resolve or explicitly accept those items before using the draft in a publishing process.

## No Warranty

The plugin is provided as-is. Users are responsible for reviewing generated content and confirming that published changes are accurate and appropriate for their workspace.
