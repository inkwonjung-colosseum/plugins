---
name: export-page
description: "Export one or more Confluence pages by URL. Usage: /confluence-export-kit:export-page <page-url> [<page-url> ...] [output-path]"
argument-hint: "<page-url> [<page-url> ...] [output-path]"
---

# Export Page

Export one or more Confluence pages by URL with `cme pages`.

## Invocation

Claude Code:

```text
/confluence-export-kit:export-page <page-url>
/confluence-export-kit:export-page <page-url> <page-url2> ...
/confluence-export-kit:export-page <page-url> [<page-url2> ...] <output-path>
/confluence-export-kit:export-page <page-url> [<page-url2> ...] --output-path <path>
```

Codex:

```text
$export-page <page-url>
$export-page <page-url> <page-url2> ...
$export-page <page-url> [<page-url2> ...] <output-path>
$export-page <page-url> [<page-url2> ...] --output-path <path>
```

## Rules

1. Positional URL-like arguments are treated as page URLs.
2. If the final positional argument is not URL-like, treat it as an optional export output path override for this run only.
3. `--output-path <path>` is still supported as an explicit output path override. Do not combine it with a trailing positional output path.
4. At least one page URL is required.
5. All supplied URLs must belong to the same Confluence site (`scheme://netloc`). Mixed-site exports are not supported.
6. Before export, validate that Python and `cme` are usable; install `confluence-markdown-exporter` only when `cme` is missing.
7. Resolve config through `cme config path`, read it through `cme config list -o json`, then extract the base site from the first page URL and verify that a configured `auth.confluence` entry with both `username` and `api_token` exists for that site. Do not hardcode `~/.cme/config.yaml`.
8. If auth is missing or incomplete, stop and tell the user to run one of:

```text
# Claude Code
/confluence-export-kit:set-config --api-key <api-key> --email <email>

# Codex
$set-config --api-key <api-key> --email <email>
```

9. Do not print the stored API token.
10. Run `cme pages <url1> [url2 ...]` with all supplied URLs in a single call.
11. If an output path was supplied, apply it only for this export via environment override. Do not persistently rewrite the user's `cme` config.
12. `--skip-unchanged` / `--no-skip-unchanged` — skips pages whose version matches the lockfile (incremental export). **Default: on.**
13. `--cleanup-stale` / `--no-cleanup-stale` — removes local files for pages deleted or moved in Confluence. **Default: on.**
14. `--jira-enrichment` fetches Jira issue summaries and includes them in the exported Markdown.
15. `--dry-run` validates auth and config without running the export; prints "skipped" and returns.

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

If no page URL argument was provided, stop and tell the user to run one of:

```text
# Claude Code
/confluence-export-kit:export-page <page-url> [<page-url2> ...] [output-path]

# Codex
$export-page <page-url> [<page-url2> ...] [output-path]
```

Otherwise run the helper script in this skill directory. The resolver handles both Claude Code (`CLAUDE_SKILL_DIR` injected) and Codex (falls back to the documented install cache `~/.codex/plugins/cache/*/confluence-export-kit/*/skills/export-page`, since Codex does not inject a skill-dir env var per its official plugin spec):

macOS / Linux Bash:

```bash
SKILL_DIR="${CLAUDE_SKILL_DIR:-${CODEX_SKILL_DIR:-}}"
if [ ! -f "$SKILL_DIR/scripts/export_page.py" ]; then
  for c in \
    "$HOME/.codex/plugins/cache/"*"/confluence-export-kit/"*"/skills/export-page" \
    "./skills/export-page" \
    "./export-page" \
    "."; do
    if [ -f "$c/scripts/export_page.py" ]; then
      SKILL_DIR="$c"
      break
    fi
  done
fi

"$PYTHON_BIN" "$SKILL_DIR/scripts/export_page.py" "<url1>" ["<url2>" ...] ["<output-path>"]
```

Windows PowerShell:

```powershell
$SkillDir = $env:CLAUDE_SKILL_DIR
if (-not $SkillDir) { $SkillDir = $env:CODEX_SKILL_DIR }

$ScriptRelativePath = "scripts/export_page.py".Replace('/', [System.IO.Path]::DirectorySeparatorChar)
$SkillCandidates = @()
if ($SkillDir) { $SkillCandidates += $SkillDir }
$SkillCandidates += @(
  "$HOME/.codex/plugins/cache/*/confluence-export-kit/*/skills/export-page",
  "./skills/export-page",
  "./export-page",
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
  Write-Error "Could not locate scripts/export_page.py for confluence-export-kit export-page."
  exit 1
}

& $PythonCommand @PythonArgs (Join-Path $ResolvedSkillDir $ScriptRelativePath) "<url1>" ["<url2>" ...] ["<output-path>"]
```

## Response Format

After the script finishes:

- report Python/cme preflight status and installer status when installation was needed
- report which Confluence site was matched
- confirm that auth was already configured
- report how many pages are being exported and list their URLs
- report the effective export output path
- confirm that the page export command completed
