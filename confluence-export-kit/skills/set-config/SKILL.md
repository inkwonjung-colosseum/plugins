---
name: set-config
description: "Set confluence-export-kit auth and export defaults. Usage: /confluence-export-kit:set-config [--api-key <api-key> --email <email>] [--output-path <path>] [--url <base-url>] [--skip-jira] [--skip-validate] [--config-path <path>]"
argument-hint: "[--api-key <api-key> --email <email>] [--output-path <path>] [--url <base-url>] [--skip-jira] [--skip-validate] [--config-path <path>]"
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
/confluence-export-kit:set-config --api-key <api-key> --email <email> --skip-validate
/confluence-export-kit:set-config --output-path <path> --config-path <config-path>
```

Codex:

```text
$set-config --api-key <api-key> --email <email>
$set-config --output-path <path>
$set-config --api-key <api-key> --email <email> --output-path <path>
$set-config --api-key <api-key> --email <email> --url <base-url> --skip-jira
$set-config --api-key <api-key> --email <email> --skip-validate
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
8. Token probe runs by default. Add `--skip-validate` to skip the `/rest/api/user/current` probe.
9. Add `--config-path <path>` to target a specific `confluence-markdown-exporter` config file.

## Execution

Use the snippet that matches the active shell. On Windows, use the Windows PowerShell snippets; do not run the Bash snippets in CMD or PowerShell.

### Step 1 — Python 3.10+ availability check

Before running any script, resolve a Python interpreter that is at least 3.10:

macOS / Linux Bash:

```bash
PYTHON_BIN=""
for candidate in python3 python3.13 python3.12 python3.11 python3.10 python; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys; raise SystemExit(sys.version_info < (3, 10))'; then
    PYTHON_BIN="$candidate"
    break
  fi
done

if [ -z "$PYTHON_BIN" ]; then
  echo "Python 3.10+ is required before continuing."
  exit 1
fi

"$PYTHON_BIN" --version
```

Windows PowerShell:

```powershell
$PythonCommand = $null
$PythonArgs = @()
$PythonCandidates = @(
  @{ Exe = "py"; Args = @("-3.13") },
  @{ Exe = "py"; Args = @("-3.12") },
  @{ Exe = "py"; Args = @("-3.11") },
  @{ Exe = "py"; Args = @("-3.10") },
  @{ Exe = "python"; Args = @() },
  @{ Exe = "python3"; Args = @() }
)

foreach ($Candidate in $PythonCandidates) {
  if (Get-Command $Candidate.Exe -ErrorAction SilentlyContinue) {
    $ProbeArgs = @($Candidate.Args) + @("-c", "import sys; raise SystemExit(sys.version_info < (3, 10))")
    & $Candidate.Exe @ProbeArgs
    if ($LASTEXITCODE -eq 0) {
      $PythonCommand = $Candidate.Exe
      $PythonArgs = $Candidate.Args
      break
    }
  }
}

if (-not $PythonCommand) {
  Write-Error "Python 3.10+ is required before continuing."
  exit 1
}

$VersionArgs = @($PythonArgs) + @("--version")
& $PythonCommand @VersionArgs
```

If no Python 3.10+ interpreter is found, stop and tell the user:

> **Python is not installed.** Install Python 3.10+ before continuing:
> - **macOS**: `brew install python` or download from https://www.python.org/downloads/
> - **Windows**: Download from https://www.python.org/downloads/ (check "Add to PATH" during install)
> - **Linux**: `sudo apt install python3` (Debian/Ubuntu) or `sudo dnf install python3` (Fedora)

Do not proceed to Step 2 until `PYTHON_BIN` (Bash) or `$PythonCommand` (PowerShell) is set.

### Step 2 — Run the helper script and ensure `cme`

The helper checks `cme` first. If `cme` is already available, it does not check or install `pipx`; if `cme` is missing, it prepares the installer path and installs `confluence-markdown-exporter`.

Run the helper script in this skill directory. The resolver handles both Claude Code (`CLAUDE_SKILL_DIR` injected) and Codex (falls back to the documented install cache `~/.codex/plugins/cache/*/confluence-export-kit/*/skills/set-config`, since Codex does not inject a skill-dir env var per its official plugin spec):

macOS / Linux Bash:

```bash
SKILL_DIR="${CLAUDE_SKILL_DIR:-${CODEX_SKILL_DIR:-}}"
if [ ! -f "$SKILL_DIR/scripts/set_config.py" ]; then
  for c in \
    "$HOME/.codex/plugins/cache/"*"/confluence-export-kit/"*"/skills/set-config" \
    "./skills/set-config" \
    "./set-config" \
    "."; do
    if [ -f "$c/scripts/set_config.py" ]; then
      SKILL_DIR="$c"
      break
    fi
  done
fi

"$PYTHON_BIN" "$SKILL_DIR/scripts/set_config.py" [--api-key "<api-key>" --email "<email>"] [--output-path "<path>"] [--url "<base-url>"] [--skip-jira] [--skip-validate] [--config-path "<path>"]
```

Windows PowerShell:

```powershell
$SkillDir = $env:CLAUDE_SKILL_DIR
if (-not $SkillDir) { $SkillDir = $env:CODEX_SKILL_DIR }

$ScriptRelativePath = "scripts/set_config.py".Replace('/', [System.IO.Path]::DirectorySeparatorChar)
$SkillCandidates = @()
if ($SkillDir) { $SkillCandidates += $SkillDir }
$SkillCandidates += @(
  "$HOME/.codex/plugins/cache/*/confluence-export-kit/*/skills/set-config",
  "./skills/set-config",
  "./set-config",
  "."
)

$ResolvedSkillDir = $null
foreach ($Candidate in $SkillCandidates) {
  foreach ($Match in Get-Item -Path $Candidate -ErrorAction SilentlyContinue) {
    $ScriptPath = Join-Path $Match.FullName $ScriptRelativePath
    if (Test-Path $ScriptPath) {
      $ResolvedSkillDir = $Match.FullName
      break
    }
  }
  if ($ResolvedSkillDir) { break }
}

if (-not $ResolvedSkillDir) {
  Write-Error "Could not locate scripts/set_config.py for confluence-export-kit set-config."
  exit 1
}

& $PythonCommand @PythonArgs (Join-Path $ResolvedSkillDir $ScriptRelativePath) [--api-key "<api-key>" --email "<email>"] [--output-path "<path>"] [--url "<base-url>"] [--skip-jira] [--skip-validate] [--config-path "<path>"]
```

## Response Format

After the script finishes:

- report detected platform
- report Python/cme preflight status and installer status when installation was needed
- report the config file path
- report whether auth was updated and which site was targeted
- report token probe status without echoing the token
- report previous and new output path when `--output-path` was supplied
