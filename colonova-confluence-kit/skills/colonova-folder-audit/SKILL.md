---
name: colonova-folder-audit
description: Use when ColoNova Engineering Confluence 8.8 하위 문서의 Archive 후보, 위치 불일치, 추출/전환 후보, 실행 큐를 read-only로 감사해야 할 때.
---

# ColoNova Folder Audit

Use this skill only for the ColoNova Engineering Confluence tree rooted at `8.8 ColoNova`.

Fixed target:

- URL: `https://colosseum.atlassian.net/wiki/spaces/COLO/pages/933068815/8.8+ColoNova`
- root page ID: `933068815`
- space key: `COLO`
- space name: `[팀]Engineering`

## Scope

This skill audits the current tree and returns evidence-backed recommendations. It never moves, edits, archives, or creates Confluence pages.

Default mode is Archive recommendation. Placement review is included only when the user asks for folder movement, mismatch, page relocation, reclassification, extraction, conversion, or companion review.

## Inputs

Do not ask for the Confluence root or site. Ask only when the request does not reveal:

- audit scope: whole tree, one folder, or specific candidate pages
- output format: chat summary, Confluence-ready table, or local Markdown report
- optional local export path for body fallback
- whether placement review should be included

## Workflow

1. Read live root page `933068815` and any linked classification guide. If live criteria cannot be read, report the failure and keep confidence low.
2. Fetch descendants deeply enough to include nested pages. If folder descendants fail, reconstruct folder subtrees from root descendant `parentId`, `depth`, title, and ordering.
3. Build one folder packet per top-level folder: folder ID, criteria, descendant IDs, nested folder boundaries, and special items such as draft or whiteboard.
4. For each packet, read every accessible page body. Record unread, draft, whiteboard, title-only, and local-only items separately.
5. Classify pages into Archive candidate, Archive hold, Archive excluded, and optional placement review candidates.
6. Produce coverage per folder:

```text
대상 <n>개 / live body 확인 <n>개 / local 보강 <n>개 / 제한 읽기 <n>개 / 실패 <n>개
```

7. Output recommendations, not inventory. Do not list pages that fit their current folder except as coverage counts.

## Output

For broad audits, create a local Markdown report and return a short chat summary. For narrow audits, a concise chat table is enough.

Always include:

- 5-line conclusion
- Archive or mismatch Top 5, depending on requested mode
- coverage summary
- execution queues
- special and limited items
- link or path to the detailed report when one is created

Load `references/output-contract.md` before composing the final report.

## Decision Rules

Load only the reference needed for the current step:

- `references/confluence-tree-audit.md`: live/local source priority, fields, worker packet rules
- `references/action-taxonomy.md`: action definitions and confidence rules
- `references/output-contract.md`: report sections and final self-check

## Safety

- Keep the default read-only.
- Do not put `low` confidence items into immediate execution queues.
- Do not recommend Archive without a replacement document, current reference, or clear retirement evidence.
- If discussion, decision, design, and operating procedure are mixed, prefer Extract or Convert over moving the original page.
- Keep draft, whiteboard, unread, title-only, and local-only entries out of immediate execution candidates.
