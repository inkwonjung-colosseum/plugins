---
name: set-api-key
description: Set the API token for confluence-markdown-exporter. Both arguments are required. Also validates Python, pip, pipx, and the cme CLI, and bootstraps missing dependencies when possible.
---

# Set Exporter API Key

Configure `confluence-markdown-exporter` for a Confluence site.

## Invocation

Primary usage:

```text
/confluence-export-kit:set-api-key <api-key> <email>
```

## Rules

1. Treat `$ARGUMENTS[0]` as the API token.
2. Treat `$ARGUMENTS[1]` as a required Atlassian email.
3. Never print the API token back to the user.
4. Default target is `CONFLUENCE_EXPORT_KIT_BASE_URL`, then `https://colosseum.atlassian.net`. Override via `--url`.
5. Update both `auth.confluence` and `auth.jira` for that URL so Jira enrichment stays aligned.
6. Do not reuse a stored username implicitly. Always write the email provided in the command.
7. Before updating config, validate that Python, `pip`, `pipx`, and `cme` are usable.
8. If `pipx` is missing but `pip` exists, bootstrap `pipx` with the current Python interpreter.
9. If `cme` is missing, install or upgrade `confluence-markdown-exporter` through `pipx`.

## Execution

If either required argument is missing, stop and tell the user to run:

```text
/confluence-export-kit:set-api-key <api-key> <email>
```

Otherwise run the helper script in this skill directory.

Command pattern:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/set_cme_api_key.py" "<api-key>" "<email>"
```

Token probe runs by default. Add `--skip-validate` to skip the `/rest/api/user/current` probe. Add `--url <base-url>` to override the target site for one invocation.

## Response Format

After the script finishes:

- report Python/pipx/cme preflight status
- confirm that the config was updated
- report the config file path
- say that the username was set from the required email argument
- report the token probe status (skipped or ok)
- do not echo the token
