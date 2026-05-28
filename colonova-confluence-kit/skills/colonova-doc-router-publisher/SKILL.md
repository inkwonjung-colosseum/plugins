---
name: colonova-doc-router-publisher
description: Use when ColoNova 8.8 문서의 위치 추천, 템플릿 변환, 문서 분리, Confluence 생성/업데이트, readback 검증이 필요할 때.
---

# ColoNova Doc Router Publisher

Use this skill for a single draft or a small package of related documents that should be routed into the ColoNova Engineering Confluence tree.

Fixed target:

- URL: `https://colosseum.atlassian.net/wiki/spaces/COLO/pages/933068815/8.8+ColoNova`
- root page ID: `933068815`
- space key: `COLO`
- space name: `[팀]Engineering`

For broad tree audits, bulk movement, archive recommendation, or folder-wide mismatch reports, stop and use `colonova-folder-audit`.

## Scope

This skill can recommend location, rewrite a draft with the right template, split mixed documents into a small package, and publish only after explicit user approval. Every create or update must be followed by readback verification.

## Inputs

Use what the user provides:

- source draft, URL, file, or pasted text
- desired title
- purpose or audience
- draft-only, publish, or update intent
- known parent folder or candidate folder
- existing page ID or URL for updates
- related pages or titles that may cause duplicates

Ask only when a missing value blocks safe routing or publishing.

## Workflow

1. Identify document purpose, audience, state, decisions, open issues, action items, repeatable procedures, solution/vendor content, incident content, and monitoring content.
2. Decide whether the source is a single-role document or a mixed document.
3. Read live root `933068815` and any linked classification guide. If unavailable, do not publish; create a draft-only result or mark location as `확인 필요`.
4. Recommend one parent folder, or compare two to three candidates when ambiguous.
5. Check child page title patterns under the recommended parent before proposing a final title.
6. Select a local template from `templates/` first. Use `references/routing-rules.md` fallback templates only when no template file exists.
7. Rewrite without inventing facts. Use `미정` or `확인 필요` for missing owners, dates, numbers, or decisions.
8. Show publish confirmation before writing to Confluence.
9. After user approval, create or update the page, then read it back and verify title, parent, main sections, and non-empty body.

## Mixed Documents

If one source mixes analysis, design, decision, technical reference, or operating procedure, do not force it into one folder without warning.

Use these split actions:

- `Extract decision`
- `Extract design`
- `Convert to technical reference`
- `Convert to operating guide`

Before publishing a mixed source, present:

1. single compressed page
2. split document package

Do not create or update pages until the user chooses and approves.

## Output

Before publishing:

1. recommended folder and reason
2. alternative folders when relevant
3. selected template
4. transformed document
5. publish approval request

After publishing:

1. Confluence link
2. saved location
3. template used
4. readback verification result
5. remaining checks

## References

Load only what the current step needs:

- `references/routing-rules.md`: folder routing and fallback templates
- `references/split-document-rules.md`: mixed document and ADR split rules
- `references/publish-safety.md`: approval, create/update, duplicate, and readback rules

## Safety

- Never publish before explicit approval.
- Never overwrite an existing page unless the user explicitly requested update and provided page ID or URL.
- Do not route to Archive for a new document unless the user clearly wants historical preservation.
- Warn before publishing secrets, tokens, passwords, or internal credentials.
- Do not add arbitrary dates to meeting, incident, or retrospective titles.
- If live criteria cannot be verified, do not publish.
