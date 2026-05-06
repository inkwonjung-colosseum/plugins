# product-team-kit Privacy Policy

`product-team-kit` formats user-provided planning input into local 기능설계서 and 정책서 drafts, configures local draft/review settings, and reviews those drafts with Product Docs SSOT evidence before external publishing.

## Data Read

The plugin instructions guide the host agent to read:

- User-provided planning input in the current conversation.
- Optional local files or directories explicitly provided as the planning input.
- Project Markdown documents and local resources linked from those Markdown documents when `plan-review` builds its evidence record.
- Existing `.product-team-kit/config.json` when `set-config`, `plan-format`, or `plan-review` needs local settings.

## Data Written

The plugin does not directly include network publishing instructions in the current planning workflow. `plan-format` does not validate Product Docs SSOT conflicts, and `plan-review` reads Product Docs Markdown documents plus explicitly linked local resources to build an evidence record for SSOT conflict, clarity, terminology consistency, and downstream-readiness review before external publishing.

Expected write operations:

- Create 기능설계서 and 정책서 drafts under `<outputRoot>/[안전기능명]--YYYY-MM-DD-HHMMSS/`; the default `<outputRoot>` is `planning`.
- Create or update `.product-team-kit/config.json` when the user invokes `set-config`.

The plugin instructions prohibit modifying Product Docs SSOT evidence sources during review. External URLs are not automatically read as evidence. `plan-review` returns one planner-facing markdown report with a verdict, role readiness, evidence details, and either a publish-preparation checklist or a re-review checklist. These outputs do not write to Confluence, Product Docs SSOT, linked local resources, or external systems.

## Confirmation Requirements

Before using generated drafts as publish-ready material, users should check:

- Review gate status for `[가정]`, confirmation questions, and role-based readiness gaps.
- Source freshness and authority of the Product Docs SSOT evidence.
- Publish-preparation checklist items when `plan-review` returns `통과` or `조건부 통과`.
- Required-fix and re-review checklist items when `plan-review` returns `수정 필요`.
- Team approval requirements outside this plugin.

## User Responsibility

Users should review drafts before publishing them through any external process, avoid including unnecessary sensitive data, and keep Product Docs SSOT Markdown and linked local resources current.

## Contact

Repository: https://github.com/inkwonjung-colosseum/plugins
