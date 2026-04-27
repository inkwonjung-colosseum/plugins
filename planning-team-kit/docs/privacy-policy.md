# planning-team-kit Privacy Policy

`planning-team-kit` is a local-first, draft-only planning plugin.

## What this plugin stores

- Draft planning artifacts created in the local workspace
- Timestamped `planning-draft` drafts saved under `planning/drafts/topic-slug--YYYY-MM-DD-HHMMSS/`
- Manual `confluence-update-plan` instructions saved inside reviewed draft directories
- Plugin manifests, templates, schemas, and examples stored in the repository
- User-provided planning inputs that are included in generated drafts

## What this plugin does not do in v0.2.1

- It does not automatically reflect content in Jira, Confluence, Slack, Google Drive, Notion, or other third-party services.
- It does not call Confluence write APIs or change Confluence pages.
- It does not include built-in telemetry or analytics collection inside the plugin bundle.
- It does not make final business decisions on behalf of users.

## User responsibility

- Review generated drafts before sharing them.
- Remove or redact sensitive information before moving artifacts into external systems.
- Confirm whether the local workspace path is synced by the host operating system or cloud storage provider.
- Confirm the privacy and retention rules of the host AI platform being used.

## Contact

Repository: https://github.com/inkwonjung-colosseum/plugins
