# planning-team-kit Terms of Service

`planning-team-kit` is a local workflow plugin for drafting, reviewing, and publishing planning documents based on Confluence source material.

## Intended Use

Use this plugin to:

- Read local Confluence exports for product planning context.
- Draft 상위설계서, 기능설계서, and 정책서 documents.
- Review drafts before publishing.
- Publish explicitly confirmed changes to Confluence through available MCP tools.

## Limitations

- The plugin does not replace human product, legal, security, or operational approval.
- Local exported Markdown may be stale. `plan-publish` includes a stale check, but users remain responsible for confirming source freshness.
- Parent page lookup depends on `confluence/confluence-lock.json`. If the parent cannot be found exactly, the agent must ask for a page ID or URL.
- The plugin should not be used to bypass Confluence permissions or team review policies.

## Publishing Rules

Confluence writes require explicit confirmation. If a draft includes `[미정]`, `[가정]`, or conflict warnings, publish requires a `plan-review` pass/conditional pass or an explicit user override.

## No Warranty

The plugin is provided as-is. Users are responsible for reviewing generated content and confirming that published changes are accurate and appropriate for their workspace.
