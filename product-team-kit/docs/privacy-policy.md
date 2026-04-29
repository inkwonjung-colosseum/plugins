# product-team-kit Privacy Policy

`product-team-kit` formats user-provided planning input into local 기능설계서 and 정책서 drafts for review.

## Data Read

The plugin instructions guide the host agent to read:

- User-provided planning intent and answers in the current conversation.
- Optional local files explicitly provided as the planning input.

## Data Written

The plugin does not directly include network code or Confluence write instructions in the current `plan-format` workflow. `plan-format` does not validate Confluence conflicts; `plan-review` reviews evidence, decision scope, and execution readiness before external publishing.

Expected write operations:

- Create or update local draft files under `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/`.

The plugin instructions prohibit modifying local exported Markdown.

## Confirmation Requirements

Before using generated drafts as publish-ready material, users should check:

- Review gate status for `[가정]`, confirmation questions, and decision-scope or execution-readiness gaps.
- Source freshness of the local Confluence export.
- Team approval requirements outside this plugin.

## User Responsibility

Users should review drafts before publishing them through any external process, avoid including unnecessary sensitive data, and re-run Confluence export/index when local snapshots need to reflect the latest source of truth.

## Contact

Repository: https://github.com/inkwonjung-colosseum/plugins
