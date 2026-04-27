# planning-team-kit Privacy Policy

`planning-team-kit` reads local Confluence exports and can publish confirmed drafts back to Confluence through the host MCP tools.

## Data Read

The plugin instructions guide the host agent to read:

- Local Confluence Markdown exports under the configured workspace.
- `.confluence-index/` retrieval metadata.
- `confluence/confluence-lock.json` page IDs, versions, titles, and export paths.
- User-provided planning intent and answers in the current conversation.

## Data Written

The plugin does not directly include network code. When `plan-publish` is used, the host agent may call available Confluence MCP write tools after explicit user confirmation.

Expected write operations:

- Create a new Confluence page.
- Update an existing Confluence page.

The plugin instructions prohibit modifying local exported Markdown and `confluence/confluence-lock.json` after publish.

## Confirmation Requirements

Before Confluence write operations, `plan-publish` requires:

- Stale export check.
- Review gate check for `[미정]`, `[가정]`, and conflict warnings.
- Final user confirmation with `yes`.

## User Responsibility

Users should review drafts before publishing, avoid including unnecessary sensitive data, and re-run Confluence export/index after publishing when local snapshots need to reflect the latest source of truth.

## Contact

Repository: https://github.com/inkwonjung-colosseum/plugins
