# Confluence Tree Audit

## Source Priority

1. Use live Confluence for current tree structure, parent, status, and page existence.
2. Use live body for current content.
3. Use local export only when live body fetch fails and the export is explicitly provided or clear from context.
4. If live and local body conflict, prefer live and mark local as an older snapshot.
5. If a page exists only in local export, classify as `Manual review`.
6. If a page exists only in live descendants, include it with no local evidence.

## Standard Fields

Record these fields for every candidate:

| Field | Values |
| --- | --- |
| `source` | `live`, `local export`, `both` |
| `body_status` | `read`, `unread`, `limited`, `local-fallback`, `title-only` |
| `failure_reason` | `folder-404`, `page-404`, `permission`, `draft`, `unsupported-type`, `unknown` |
| `classification_basis` | `body`, `title+parent`, `local body`, `linked context` |
| `confidence` | `high`, `medium`, `low` |

## Folder Packet

Each top-level folder packet should include:

- folder title and ID
- live criteria for the folder
- all descendant page IDs under that folder
- nested folder boundaries
- draft, whiteboard, and unsupported items

Do not send the entire tree to every worker. Give each worker only its packet plus shared classification rules.

## Worker Requirements

Each folder worker must:

1. Read all accessible page bodies in the packet.
2. Record unread pages with failure reason.
3. Separate Archive candidate, Archive hold, and Archive excluded.
4. List fitting pages only as coverage counts or exclusion aggregates.
5. For each candidate, include page ID, evidence, confidence, and recommended action.
6. Include placement review only when requested.

If parallel workers are unavailable, process the same packets sequentially and note the fallback briefly.
