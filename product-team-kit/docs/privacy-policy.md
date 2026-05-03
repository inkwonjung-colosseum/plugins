# product-team-kit Privacy Policy

`product-team-kit` guides interactive planning, formats user-provided planning input into local 기능설계서 and 정책서 drafts, and reviews those drafts with an evidence package before external publishing.

## Data Read

The plugin instructions guide the host agent to read:

- User-provided planning intent and answers in the current conversation.
- Optional local files explicitly provided as the planning input.
- Relevant local project files when `plan-draft` needs project context for interactive planning.
- Project Markdown documents and local resources linked from those Markdown documents when `plan-review` builds an evidence package.

## Data Written

The plugin does not directly include network publishing instructions in the current planning workflow. `plan-draft` may inspect relevant local project context, `plan-format` does not validate Project Docs SSOT conflicts, and `plan-review` reads Project Markdown documents plus explicitly linked local resources to build an evidence package for evidence, decision scope, and execution-readiness review before external publishing.

Expected write operations:

- Create local planning drafts under `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/[안전기능명]_기획초안.md`.
- Create 기능설계서 and 정책서 drafts under `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/`; when formatting a `plan-draft` `_기획초안.md`, reuse that 기획초안 폴더.

The plugin instructions prohibit modifying Project Docs SSOT evidence sources during review. External URLs are not automatically read as evidence. `publish_readiness` is a screen-output checklist only and does not write to Confluence, Project Docs SSOT, linked local resources, or external systems.

## Confirmation Requirements

Before using generated drafts as publish-ready material, users should check:

- Review gate status for `[가정]`, confirmation questions, and decision-scope or execution-readiness gaps.
- Source freshness and authority of the Project Docs SSOT evidence.
- `publish_readiness` checklist items when `plan-review` returns `pass` or `conditional pass`.
- Team approval requirements outside this plugin.

## User Responsibility

Users should review drafts before publishing them through any external process, avoid including unnecessary sensitive data, and keep Project Docs SSOT Markdown and linked local resources current.

## Contact

Repository: https://github.com/inkwonjung-colosseum/plugins
