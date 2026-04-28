# Privacy Policy

`confluence-export-kit` is a local workflow plugin for exporting Confluence content to Markdown and indexing those local exports for agent-friendly reading.

The plugin uses the active Claude Code or Codex session to configure Confluence credentials, call `confluence-markdown-exporter`, write exported Markdown files, and create local `.confluence-index/` metadata. It does not include a background service, telemetry collector, or separate hosted database.

Users should only provide Confluence URLs, email addresses, API keys, and exported content when their runtime environment and organization policy allow that use. Credentials are handled by the local `cme` configuration flow and should be managed according to the user's own security policy.

The plugin treats Confluence as the source of truth and local Markdown as a read-only snapshot. Local exports may contain confidential workspace content, so users remain responsible for storage, sharing, retention, and deletion of generated files.
