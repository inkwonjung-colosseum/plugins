# Publish Runbook

Use this reference when `plan-publish` prepares a Confluence write.

## MCP tool discovery

Discover the current Confluence MCP tools and their argument schemas before writing.

Common schema terms in Atlassian connectors:

- `cloudId`: Atlassian cloud resource ID or site URL, usually discovered with an accessible-resources tool.
- `spaceId`: Confluence space identifier. Use the value confirmed from `confluence-lock.json`, parent lookup, or the discovered MCP tool context.
- `parentId`: parent page ID for new pages.
- `pageId`: existing page ID for updates.
- `title`: page title.
- `body`: Markdown or ADF content.
- `contentFormat`: use `markdown` when the tool supports it.

Do not send arguments that are not in the discovered schema. In particular, do not assume `spaceKey`, `content`, or explicit version arguments unless the current tool schema requires them.

## Stale and Review Gates

1. Read `confluence/confluence-lock.json`.
2. Check `last_export`; warn when it is 7 or more days old.
3. If the draft contains `[미정]`, `[가정]`, `충돌 경고`, or `Publish gate: review-required`, require a `plan-review` pass/conditional pass or explicit user override.
4. Require final user `yes` before any MCP write call.

## parent lookup

For new pages, derive the parent from the draft location and verify it with lock data.

1. Build the expected parent `export_path` from the draft location and selected export source root.
2. Normalize both expected and lock paths before comparison:
   - Unicode normalize to NFC.
   - Normalize path separators to `/`.
   - Strip leading `confluence/`.
   - Collapse duplicate whitespace.
3. Match against all `confluence/confluence-lock.json` org/space pages by normalized `export_path`.
4. If exactly one candidate matches, use its `site_url`, `space_id`, `page_id`, `title`, and `export_path`.
5. If no candidate matches, try a title-based fallback only when the parent title and parent path context both match.
6. If there are zero or multiple credible candidates, stop and ask for the parent page ID or URL.

Never guess a parent page from a folder name alone.

## Update Safety

- For existing pages, use the `page_id` and current `export_path` from `confluence/confluence-lock.json`.
- If the MCP update tool exposes its own version handling, let the tool handle it.
- If the tool requires a version field, compute it from lock version only after showing the current version in the final confirmation.
- Do not modify exported Markdown or `confluence/confluence-lock.json` after publish.
