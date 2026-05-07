# product-team-kit Terms of Service

`product-team-kit` is a local workflow plugin for configuring product-document draft settings, formatting planning input into 기능설계서 and 정책서 drafts, and reviewing those drafts with Product Docs SSOT evidence before external publishing. The workflow reads config, input, templates, references, and SSOT corpus only in the branches where those files are needed.

## Intended Use

Use this plugin to:

- Draft 기능설계서 and 정책서 documents from user-provided planning input.
- Create or update local product-team-kit settings with `set-config`: `.product-team-kit/config.json`, then the product-team-kit managed block in project-root `CLAUDE.md` and `AGENTS.md`.
- Record `[미정]`, `[가정]`, and confirmation questions without treating them as verified facts.
- Return a save-hold with missing fields when the planning input is not enough to create both draft documents.
- Review SSOT conflict, clarity, and terminology consistency with `plan-review` before publishing through a separate external process. `plan-review` narrows Product Docs candidates with review-target keywords and reads only directly needed Markdown and linked local resources.
- Produce a planner-facing review summary and a publish-preparation checklist for human review when `plan-review` returns `통과` or `조건부 통과`.

## Limitations

- The plugin does not replace human product, legal, security, or operational approval.
- Product Docs SSOT Markdown or linked local resources may be outdated. Users remain responsible for confirming source freshness.
- The plugin should not be used to bypass team review policies.
- `plan-format` does not interview the user. If input is insufficient, it returns a save-hold with missing fields only.

## Publishing Rules

This plugin does not publish directly to external systems. The publish-preparation checklist and re-review checklist are screen-output guidance only. If a draft includes `[가정]`, confirmation questions, conflict warnings, or clarity/terminology gaps, users should run `plan-review`, review the planner-facing summary and evidence details, and resolve or explicitly accept those items before using the draft in a publishing process.

## No Warranty

The plugin is provided as-is. Users are responsible for reviewing generated content and confirming that published changes are accurate and appropriate for their workspace.
