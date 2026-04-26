---
name: show-config
description: Show the current confluence-markdown-exporter configuration by running cme config list. Add --json to output JSON format.
---

# Show Config

Display the current `confluence-markdown-exporter` configuration with `cme config list`.

## Invocation

Claude Code:

```text
/confluence-export-kit:show-config
/confluence-export-kit:show-config --json
```

Codex:

```text
$show-config
$show-config --json
```

## Rules

1. Before running, validate that Python, `pipx`, and `cme` are usable.
2. Run `cme config list` and capture its full output.
3. If `--json` is passed, run `cme config list -o json` instead.
4. Print the output verbatim — do not summarize or truncate it.
5. Do not infer, modify, or interpret the config values shown.

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

### Step 2 — Run the helper script

Run the helper script in this skill directory. The resolver handles both Claude Code (`CLAUDE_SKILL_DIR` injected) and Codex (falls back to the documented install cache `~/.codex/plugins/cache/*/confluence-export-kit/*/skills/show-config`, since Codex does not inject a skill-dir env var per its official plugin spec):

macOS / Linux Bash:

```bash
SKILL_DIR="${CLAUDE_SKILL_DIR:-${CODEX_SKILL_DIR:-}}"
if [ ! -f "$SKILL_DIR/scripts/show_config.py" ]; then
  for c in \
    "$HOME/.codex/plugins/cache/"*"/confluence-export-kit/"*"/skills/show-config" \
    "./skills/show-config" \
    "./show-config" \
    "."; do
    if [ -f "$c/scripts/show_config.py" ]; then
      SKILL_DIR="$c"
      break
    fi
  done
fi

"$PYTHON_BIN" "$SKILL_DIR/scripts/show_config.py" [--json]
```

Windows PowerShell:

```powershell
$SkillDir = $env:CLAUDE_SKILL_DIR
if (-not $SkillDir) { $SkillDir = $env:CODEX_SKILL_DIR }

$ScriptRelativePath = "scripts/show_config.py".Replace('/', [System.IO.Path]::DirectorySeparatorChar)
$SkillCandidates = @()
if ($SkillDir) { $SkillCandidates += $SkillDir }
$SkillCandidates += @(
  "$HOME/.codex/plugins/cache/*/confluence-export-kit/*/skills/show-config",
  "./skills/show-config",
  "./show-config",
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
  Write-Error "Could not locate scripts/show_config.py for confluence-export-kit show-config."
  exit 1
}

& $PythonCommand @PythonArgs (Join-Path $ResolvedSkillDir $ScriptRelativePath) [--json]
```

## Response Format

After the script finishes:

- report Python/pipx/cme preflight status
- print the full `cme config list` output

## Screen Feedback

When showing results to the user, explain terminal rendering behavior for both platforms:

- **macOS / Linux**: Terminal, Claude Code desktop, and Codex render ANSI output directly. `cme config list` output appears as-is.
- **Windows**: Terminal treats paths with backslashes and may wrap long lines differently. If output appears truncated, suggest running with `--json` flag for structured output or increasing terminal width (`mode con cols=120` in CMD, `$Host.UI.RawUI.BufferSize.Width = 120` in PowerShell).
