---
name: set-config
description: "Set confluence-export-kit auth and export defaults. Usage: /confluence-export-kit:set-config [--api-key <api-key> --email <email>] [--output-path <path>] [--url <base-url>] [--skip-jira] [--config-path <path>]"
argument-hint: "[--api-key <api-key> --email <email>] [--output-path <path>] [--url <base-url>] [--skip-jira] [--config-path <path>]"
---

# Set Config

Configure `confluence-markdown-exporter` auth and default export settings in one command.

## Invocation

Claude Code:

```text
/confluence-export-kit:set-config --api-key <api-key> --email <email>
/confluence-export-kit:set-config --output-path <path>
/confluence-export-kit:set-config --api-key <api-key> --email <email> --output-path <path>
/confluence-export-kit:set-config --api-key <api-key> --email <email> --url <base-url> --skip-jira
/confluence-export-kit:set-config --output-path <path> --config-path <config-path>
```

Codex:

```text
$set-config --api-key <api-key> --email <email>
$set-config --output-path <path>
$set-config --api-key <api-key> --email <email> --output-path <path>
$set-config --api-key <api-key> --email <email> --url <base-url> --skip-jira
$set-config --output-path <path> --config-path <config-path>
```

## Rules

1. Require at least one setting: auth (`--api-key` and `--email`) or `--output-path`.
2. Treat `--api-key` and `--email` as a pair; do not accept only one.
3. Never print the API token back to the user.
4. Default target is `CONFLUENCE_EXPORT_KIT_BASE_URL`, then `https://colosseum.atlassian.net`. Override via `--url`.
5. When auth is supplied, update both `auth.confluence` and `auth.jira` for that URL unless `--skip-jira` is passed.
6. When `--output-path` is supplied, persist it to `export.output_path`.
7. Apply all requested config changes in one write.
8. Do not probe the token; assume the supplied credentials are intended to be stored.
9. Before writing config, check whether `confluence-markdown-exporter` is installed through `pip`; install it with `pip` only when missing.
10. Add `--config-path <path>` to target a specific `confluence-markdown-exporter` config file.

## Execution

Run the matching helper script under this skill's `scripts/` directory with the user-supplied arguments. No extra setup is performed.

## Response Format

After the script finishes:

- report detected platform
- report whether `confluence-markdown-exporter` was already installed or installed through `pip`
- report the config file path
- report whether auth was updated and which site was targeted
- do not echo the token
- report previous and new output path when `--output-path` was supplied
