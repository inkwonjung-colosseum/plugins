# planning-team-kit Terms of Service

`planning-team-kit` is a local workflow plugin for formatting planning input into 기능설계서 and 정책서 drafts and reviewing those drafts before external publishing.

## Intended Use

Use this plugin to:

- Draft 기능설계서 and 정책서 documents from user-provided planning input.
- Record `[미정]`, `[가정]`, and confirmation questions without treating them as verified facts.
- Review drafts before publishing through a separate external process.

## Limitations

- The plugin does not replace human product, legal, security, or operational approval.
- Local exported Markdown may be stale. Users remain responsible for confirming source freshness.
- The plugin should not be used to bypass Confluence permissions or team review policies.

## Publishing Rules

This plugin does not publish directly to Confluence. If a draft includes `[미정]`, `[가정]`, confirmation questions, or conflict warnings, users should run `plan-review` and resolve or explicitly accept those items before using the draft in a publishing process.

## No Warranty

The plugin is provided as-is. Users are responsible for reviewing generated content and confirming that published changes are accurate and appropriate for their workspace.
