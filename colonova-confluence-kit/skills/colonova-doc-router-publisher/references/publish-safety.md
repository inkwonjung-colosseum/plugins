# Publish Safety

## Required Confirmation

Before any Confluence write, show:

- recommended folder
- recommended parent page ID
- title
- document type
- template
- create or update intent
- transformed document body

Proceed only after explicit approval.

## Create Rules

- Use the selected parent ID.
- Prefer Markdown content when the tool supports it.
- Record created page ID and URL.
- If the title may duplicate an existing page, ask before creating.

## Update Rules

- Update only when the user explicitly asked to update an existing page.
- Require page ID or URL.
- Do not silently overwrite pages found by title search.
- Preserve the existing page relationship unless the user approved a move or new parent.

## Readback Verification

After create or update, read the page by ID and verify:

- title is correct
- parent is correct
- main sections exist
- body is not empty or broken
- split packages have verification per page ID

Report successes and failures separately.

## Sensitive Content

Warn before publishing:

- passwords
- tokens
- API keys
- private credentials
- internal authentication values
- personal data not necessary for the document
