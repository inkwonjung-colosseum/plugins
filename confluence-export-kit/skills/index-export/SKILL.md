---
name: index-export
description: "Index local Markdown files that were already exported from Confluence. Usage: /confluence-export-kit:index-export <export-path> [--source-id <id>] [--index-root <path>] [--no-agent-rules] [--dry-run]"
argument-hint: "<export-path> [--source-id <id>] [--index-root <path>] [--no-agent-rules] [--dry-run]"
---

# Index Export

Index local Markdown files that were already exported from Confluence. This skill creates a local `.confluence-index/` and can install Reading Rule blocks into `AGENTS.md` and `CLAUDE.md`.

It does not fetch, create, or update remote Confluence or Jira content.

## Invocation

Claude Code:

```text
/confluence-export-kit:index-export <export-path>
/confluence-export-kit:index-export <export-path> --source-id <id>
/confluence-export-kit:index-export <export-path> --no-agent-rules
/confluence-export-kit:index-export <export-path> --dry-run
```

Codex:

```text
$index-export <export-path>
$index-export <export-path> --source-id <id>
$index-export <export-path> --no-agent-rules
$index-export <export-path> --dry-run
```

## Rules

1. Treat `<export-path>` as a local folder containing Markdown files already exported from Confluence.
2. Do not run `cme`, call Confluence, call Jira, or mutate the exported source files.
3. Create or update `.confluence-index/sources/<source-id>/source-index.jsonl`, `tree.md`, `stats.md`, and `log.md`.
4. Create or update root `.confluence-index/registry.json`, `tree.md`, `stats.md`, and `log.md`.
5. Default `<source-id>` to the export folder basename in kebab-case.
6. Support repeated indexing of multiple export folders by keeping each source under `.confluence-index/sources/<source-id>/`.
7. If a `<source-id>` already points to a different export path, stop and tell the user to pass a different `--source-id`.
8. Unless `--no-agent-rules` is passed, add or update managed Reading Rule blocks in `AGENTS.md` and `CLAUDE.md`.
9. Only replace content between `confluence-export-kit:reading-rule:start` and `confluence-export-kit:reading-rule:end`; preserve all other file content.
10. `--dry-run` prints planned writes without creating or modifying files.

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

If no Python 3.10+ interpreter is found, stop and tell the user to install Python 3.10+.

### Step 2 — Run the helper script

If no export path argument was provided, stop and tell the user to run one of:

```text
# Claude Code
/confluence-export-kit:index-export <export-path>

# Codex
$index-export <export-path>
```

Otherwise run the helper script in this skill directory.

macOS / Linux Bash:

```bash
SKILL_DIR="${CLAUDE_SKILL_DIR:-${CODEX_SKILL_DIR:-}}"
if [ ! -f "$SKILL_DIR/scripts/index_export.py" ]; then
  for c in \
    "$HOME/.codex/plugins/cache/"*"/confluence-export-kit/"*"/skills/index-export" \
    "./skills/index-export" \
    "./index-export" \
    "."; do
    if [ -f "$c/scripts/index_export.py" ]; then
      SKILL_DIR="$c"
      break
    fi
  done
fi

"$PYTHON_BIN" "$SKILL_DIR/scripts/index_export.py" "<export-path>" [--source-id "<id>"] [--index-root ".confluence-index"] [--no-agent-rules] [--dry-run]
```

Windows PowerShell:

```powershell
$SkillDir = $env:CLAUDE_SKILL_DIR
if (-not $SkillDir) { $SkillDir = $env:CODEX_SKILL_DIR }

$ScriptRelativePath = "scripts/index_export.py".Replace('/', [System.IO.Path]::DirectorySeparatorChar)
$SkillCandidates = @()
if ($SkillDir) { $SkillCandidates += $SkillDir }
$SkillCandidates += @(
  "$HOME/.codex/plugins/cache/*/confluence-export-kit/*/skills/index-export",
  "./skills/index-export",
  "./index-export",
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
  Write-Error "Could not locate scripts/index_export.py for confluence-export-kit index-export."
  exit 1
}

& $PythonCommand @PythonArgs (Join-Path $ResolvedSkillDir $ScriptRelativePath) "<export-path>" [--source-id "<id>"] [--index-root ".confluence-index"] [--no-agent-rules] [--dry-run]
```

## Response Format

After the script finishes:

- report the source ID
- report the number of Markdown files indexed
- report the index root and source index path
- report whether Reading Rule installation was completed or skipped
- if the command failed because of a source ID conflict, tell the user which `--source-id` to change
