# confluence-export-kit

confluence-export-kit은 `Claude Code`와 `Codex` 양쪽에서 동작하는 Confluence export-only 플러그인입니다 (v0.1.0). `confluence-markdown-exporter` 기반으로 auth 설정, 다양한 export 범위, Python/`cme` bootstrap을 다룹니다.

두 에이전트의 플러그인 매니페스트(`.claude-plugin/`, `.codex-plugin/`)가 하나의 `skills/` 디렉터리와 `scripts/` 런타임을 공유합니다. 스킬 호출 문법은 에이전트별로 다릅니다 — Claude Code는 `/confluence-export-kit:<skill>` 콜론 네임스페이스, Codex는 공식 플러그인 스펙에 따라 `$<skill>` 형태를 사용합니다. helper 스크립트 경로는 각 SKILL.md 안에서 직접 해결합니다: Claude Code가 주입하는 `CLAUDE_SKILL_DIR` 을 우선 시도하고, Codex에는 해당하는 env 주입이 공식 문서에 없으므로 Codex 설치 캐시(`~/.codex/plugins/cache/*/confluence-export-kit/*/skills/<skill>`)와 로컬 개발 경로를 순서대로 탐지합니다.

이 플러그인은 범용 Atlassian 도구 모음이 아닙니다. 지원 범위는 다음으로 제한됩니다.

- Confluence auth 설정 및 token 검증
- org / space / page-with-descendants / page 단건/다건 export
- export runtime bootstrap (`python`, `cme`; `cme`가 없을 때만 installer 사용)
- 기본 출력 경로 영구 설정

지원하지 않는 범위는 다음과 같습니다.

- planning brief 작성
- Jira write 작업
- 범용 CQL 콘솔
- `cme config` interactive menu

## 포함된 구성

- `.claude-plugin/plugin.json` — Claude Code 플러그인 매니페스트
- `.codex-plugin/plugin.json` — Codex 플러그인 매니페스트 (Codex registry용 `interface` 메타 포함)
- `skills/set-config/SKILL.md` — auth와 기본 출력 경로 통합 설정
- `skills/help/SKILL.md` — help 응답 규칙과 quick start 안내
- `skills/export-org/SKILL.md` — org 전체 export
- `skills/export-space/SKILL.md` — space 전체 export
- `skills/export-page-with-descendant/SKILL.md` — page with descendants export
- `skills/export-page/SKILL.md` — 단건/다건 page export
- `skills/show-config/SKILL.md` — 현재 cme 설정 출력
- `scripts/cme_runtime.py` — preflight, bootstrap, config/auth helper 공통 처리

## Export 워크플로우

아래 워크플로우는 Claude Code 문법으로 표기했습니다. Codex에서는 각 `/confluence-export-kit:<skill>` 를 `$<skill>` 로 바꿔 호출하세요 (예: `/confluence-export-kit:export-page-with-descendant` → `$export-page-with-descendant`).

```text
/confluence-export-kit:set-config --api-key <api-key> --email <email> --output-path <path>
                                                            (최초 1회 auth + 기본 출력 경로 설정)
    │
    ├─► /confluence-export-kit:export-org <org-url> [<org-url> ...] [output-path]
    │       하나 이상의 Confluence instance 전체 export
    │
    ├─► /confluence-export-kit:export-space <space-url> [<space-url> ...] [output-path]
    │       하나 이상의 space 전체 export
    │
    ├─► /confluence-export-kit:export-page-with-descendant <page-url> [<page-url> ...] [output-path]
    │       하나 이상의 page URL과 하위 전체 문서 export
    │
    └─► /confluence-export-kit:export-page <page-url> [<page-url> ...] [output-path]
            특정 page URL 단건/다건 export
```

## 공통 export 플래그

모든 export 명령에서 사용 가능:

| 플래그 | 설명 |
|---|---|
| `--skip-unchanged` | lockfile 기반 증분 export — 변경 없는 page skip |
| `--cleanup-stale` | Confluence에서 삭제/이동된 page의 로컬 파일 cleanup |
| `--jira-enrichment` | Jira issue summary를 export된 Markdown에 포함 |
| `--dry-run` | auth/config 검증만 수행, cme 실행 생략 |
| `--max-workers N` | 병렬 export worker 수 제어 |

## 설치

### Claude Code

```bash
claude plugin marketplace add inkwonjung-colosseum/plugins
claude plugin install confluence-export-kit@inkwonjung-colosseum
```

### Codex

Codex 공식 플러그인 스펙은 로컬 marketplace 파일 기반 설치를 사용합니다 ([Build plugins 문서 참고](https://developers.openai.com/codex/plugins/build)). repo 범위 또는 개인 범위 중 하나를 선택합니다.

**Repo 범위 (팀 공유)**

1. confluence-export-kit 폴더를 repo 의 `plugins/` 아래로 복사합니다.

   ```bash
   mkdir -p ./plugins
   cp -R /absolute/path/to/confluence-export-kit ./plugins/confluence-export-kit
   ```

   Windows PowerShell:

   ```powershell
   New-Item -ItemType Directory -Force -Path .\plugins | Out-Null
   Copy-Item -Recurse -Force C:\absolute\path\to\confluence-export-kit .\plugins\confluence-export-kit
   ```

2. `$REPO_ROOT/.agents/plugins/marketplace.json` 을 만들거나 갱신합니다.

   ```json
   {
     "name": "inkwonjung-colosseum",
     "interface": { "displayName": "inkwonjung-colosseum" },
     "plugins": [
       {
         "name": "confluence-export-kit",
         "source": { "source": "local", "path": "./plugins/confluence-export-kit" },
         "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
         "category": "Productivity"
       }
     ]
   }
   ```

3. Codex 를 재시작하고 `/plugins` 를 열어 `inkwonjung-colosseum` marketplace 에서 confluence-export-kit 을 설치합니다.

**개인 범위**

1. confluence-export-kit 폴더를 `~/.codex/plugins/confluence-export-kit` 으로 복사합니다.

   ```bash
   mkdir -p ~/.codex/plugins
   cp -R /absolute/path/to/confluence-export-kit ~/.codex/plugins/confluence-export-kit
   ```

   Windows PowerShell:

   ```powershell
   New-Item -ItemType Directory -Force -Path "$HOME\.codex\plugins" | Out-Null
   Copy-Item -Recurse -Force C:\absolute\path\to\confluence-export-kit "$HOME\.codex\plugins\confluence-export-kit"
   ```

2. `~/.agents/plugins/marketplace.json` 에 동일한 구조의 marketplace 파일을 만들되 `source.path` 를 `./confluence-export-kit` 로 지정합니다 (marketplace 파일 루트 기준).

3. Codex 를 재시작하고 `/plugins` 에서 confluence-export-kit 을 설치합니다.

> Codex 는 설치한 플러그인을 `~/.codex/plugins/cache/<marketplace>/confluence-export-kit/local/` 로 복사해 실제 로드 경로로 사용합니다. confluence-export-kit 의 각 SKILL.md 는 이 캐시 경로를 자동 탐지하도록 작성돼 있어 별도 설정이 필요 없습니다.

### 양쪽 에이전트 공통

설치 후 `confluence-export-kit` 은 동일한 `skills/` 와 `scripts/` 를 공유합니다. 각 SKILL.md 의 helper 호출은 다음 순서로 스킬 디렉터리를 해결합니다.

1. `$CLAUDE_SKILL_DIR` (Claude Code 가 주입)
2. `$CODEX_SKILL_DIR` (Codex 공식 문서에는 없지만 향후 대비)
3. `~/.codex/plugins/cache/*/confluence-export-kit/*/skills/<skill>` (Codex 설치 캐시)
4. `./skills/<skill>` 및 현재 디렉터리 (로컬 개발용)

덕분에 Claude Code 에서는 `CLAUDE_SKILL_DIR` 경로가 그대로 쓰이고, Codex 에서는 env 주입 없이도 캐시 경로가 매칭되어 helper 스크립트가 실행됩니다.

## 추천 사용 예

Claude Code 와 Codex 각각에서 동일한 작업을 하는 문법 쌍입니다.

```text
# Claude Code
/confluence-export-kit:set-config --api-key <api-key> --email <email> --output-path ./docs/confluence
# Codex
$set-config --api-key <api-key> --email <email> --output-path ./docs/confluence
```

```text
# Claude Code
/confluence-export-kit:export-page-with-descendant https://colosseum.atlassian.net/wiki/spaces/KEY/pages/123456789/Root
# Codex
$export-page-with-descendant https://colosseum.atlassian.net/wiki/spaces/KEY/pages/123456789/Root
```

## 환경변수

| 환경변수 | 기본값 | 설명 |
|---|---|---|
| `CONFLUENCE_EXPORT_KIT_BASE_URL` | `https://colosseum.atlassian.net` | `set-config`의 기본 Confluence 사이트 |

## 동작 메모

- `set-config`
  - 기본 URL은 `https://colosseum.atlassian.net` 입니다.
  - `CONFLUENCE_EXPORT_KIT_BASE_URL` 또는 `--url` 로 site를 바꿀 수 있습니다.
  - 토큰 검증은 기본 동작입니다. `--skip-validate` 로 생략할 수 있습니다.
  - `auth.confluence` 와 `auth.jira` 를 같은 URL로 동시에 설정합니다. `--skip-jira` 로 Jira mirror를 생략할 수 있습니다.
  - `export.output_path` 를 cme config에 영구 저장합니다.
  - 이후 모든 export는 이 경로를 기본값으로 사용합니다.
- export 명령 공통
  - auth가 없으면 export를 막고 `set-config` 실행을 안내합니다.
  - `[output-path]` 는 env override로만 적용하고 config를 영구 수정하지 않습니다.
