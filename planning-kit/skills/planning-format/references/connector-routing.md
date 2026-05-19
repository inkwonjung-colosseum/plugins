# Connector Routing

Use only during URL collection.

## Rules

- Try the plain URL fetch first for every dequeued `https?://` URL unless `--no-fetch`.
- Never skip a fetch attempt because a page looks private. Attempt, then record the failure.
- Traverse breadth-first. Same-depth order follows discovery order: markdown link, HTML href/src, plain URL.
- Normalize before enqueue. Use a visited set to prevent cycles. No depth, page, or body-size cap.
- Ignore `mailto:`, `tel:`, `javascript:`, `blob:`, self anchors, and scheme-less strings.

## Connector fallback

Use a connector only after direct fetch is blocked, empty, or clearly auth-gated.

- Atlassian: Confluence/Jira URLs.
- Google Drive: Docs, Sheets, Slides, Drive file URLs.
- Gmail, Slack, Calendar: only when the URL host and task clearly match.
- Browser/Chrome: only when logged-in rendering is required and connector text is unavailable.

## Source row

Every dequeued URL gets one source row:

- URL:
- status: success / auth required / timeout / 4xx / 5xx / unsupported / empty
- body used: yes / no
- note:

Google Sheets source notes include `gid` and range when known.
