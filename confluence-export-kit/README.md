# confluence-export-kit

confluence-export-kit은 `Claude Code`와 `Codex` 양쪽에서 동작하는 Confluence export 및 local export-index 플러그인입니다 (v0.1.2). `confluence-markdown-exporter` 기반으로 auth 설정, 다양한 export 범위, export된 로컬 Markdown 색인을 다룹니다.

두 에이전트의 플러그인 매니페스트(`.claude-plugin/`, `.codex-plugin/`)가 하나의 `skills/` 디렉터리와 `scripts/` 런타임을 공유합니다. 스킬 호출 문법은 에이전트별로 다릅니다 — Claude Code는 `/confluence-export-kit:<skill>` 콜론 네임스페이스, Codex는 공식 플러그인 스펙에 따라 `$<skill>` 형태를 사용합니다.

이 플러그인은 범용 Atlassian 도구 모음이 아닙니다. 지원 범위는 다음으로 제한됩니다.

- Confluence auth 설정
- `set-config` 실행 시 `pip` 기준 `confluence-markdown-exporter` 설치 확인
- org / space / page-with-descendants / page 단건/다건 export
- export 성공 후 같은 output path를 자동 색인
- 이미 export된 로컬 Markdown 폴더의 `.confluence-index/` 생성
- 현재 작업 폴더의 `AGENTS.md` / `CLAUDE.md` Reading Rule 관리 블록 설치
- `cme` config의 기본 출력 경로 영구 저장

지원하지 않는 범위는 다음과 같습니다.

- remote Confluence/Jira write 작업
- planning brief 작성
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
- `skills/index-export/SKILL.md` — 이미 export된 로컬 Markdown 색인 및 Reading Rule 설치
- `skills/show-config/SKILL.md` — 현재 cme 설정 출력
- `scripts/cme_runtime.py` — export/config helper 공통 처리

## Export 워크플로우

아래 워크플로우는 Claude Code 문법으로 표기했습니다. Codex에서는 각 `/confluence-export-kit:<skill>` 를 `$<skill>` 로 바꿔 호출하세요 (예: `/confluence-export-kit:export-page-with-descendant` → `$export-page-with-descendant`).

```text
/confluence-export-kit:set-config --api-key <api-key> --email <email> --output-path <path>
                                                            (최초 1회 auth + 기본 출력 경로 설정)
    │
    ├─► /confluence-export-kit:export-org <org-url> [<org-url> ...] [output-path]
    │       하나 이상의 Confluence instance 전체 export 후 output path 자동 색인
    │
    ├─► /confluence-export-kit:export-space <space-url> [<space-url> ...] [output-path]
    │       하나 이상의 space 전체 export 후 output path 자동 색인
    │
    ├─► /confluence-export-kit:export-page-with-descendant <page-url> [<page-url> ...] [output-path]
    │       하나 이상의 page URL과 하위 전체 문서 export 후 output path 자동 색인
    │
    ├─► /confluence-export-kit:export-page <page-url> [<page-url> ...] [output-path]
    │       특정 page URL 단건/다건 export 후 output path 자동 색인
    │
    └─► /confluence-export-kit:index-export <export-path>
            이미 export된 로컬 Markdown 폴더를 수동으로 다시 색인
```

## 공통 export 플래그

모든 export 명령에서 사용 가능:

| 플래그 | 설명 |
|---|---|
| `--skip-unchanged` / `--no-skip-unchanged` | lockfile 기반 증분 export 제어. 기본값은 on |
| `--cleanup-stale` / `--no-cleanup-stale` | Confluence에서 삭제/이동된 page의 로컬 파일 cleanup 제어. 기본값은 on |
| `--jira-enrichment` | Jira issue summary를 export된 Markdown에 포함 |
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

> Codex 는 설치한 플러그인을 `~/.codex/plugins/cache/<marketplace>/confluence-export-kit/local/` 로 복사해 실제 로드 경로로 사용합니다.

### 양쪽 에이전트 공통

설치 후 `confluence-export-kit` 은 동일한 `skills/` 와 `scripts/` 를 공유합니다. 각 스킬의 상세 실행 규칙은 해당 `skills/*/SKILL.md` 에 있습니다.

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

```text
# Claude Code
/confluence-export-kit:index-export ./Product\ Team\ Space
# Codex
$index-export ./Product\ Team\ Space
```

## 환경변수

| 환경변수 | 기본값 | 설명 |
|---|---|---|
| `CONFLUENCE_EXPORT_KIT_BASE_URL` | `https://colosseum.atlassian.net` | `set-config`의 기본 Confluence 사이트 |

## 동작 메모

- `set-config`
  - 기본 URL은 `https://colosseum.atlassian.net` 입니다.
  - `CONFLUENCE_EXPORT_KIT_BASE_URL` 또는 `--url` 로 site를 바꿀 수 있습니다.
  - 토큰 probe는 수행하지 않고 전달된 credential을 저장합니다.
  - `confluence-markdown-exporter` 설치 여부는 `pip` 로 확인하고, 없으면 설치합니다.
  - `auth.confluence` 와 `auth.jira` 를 같은 URL로 동시에 설정합니다. `--skip-jira` 로 Jira mirror를 생략할 수 있습니다.
  - `export.output_path` 를 cme config에 영구 저장합니다. 이 값은 `cme` 직접 실행과 `show-config`에서 확인되는 기본 설정입니다.
- export 명령 공통
  - `cme` 와 config/auth가 이미 준비되어 있다고 가정하고 `cme` 명령을 실행합니다.
  - `[output-path]` 또는 `--output-path` 는 env override로만 적용하고 config를 영구 수정하지 않습니다.
  - 현재 helper의 기본 output path는 명시적 override가 없을 때 `confluence` 입니다.
  - `cme` export가 성공하면 같은 output path를 `index-export` 로 자동 색인합니다. 이때 `index-export` 기본 동작에 따라 `AGENTS.md` / `CLAUDE.md` Reading Rule도 설치 또는 갱신됩니다.
- `index-export`
  - Confluence/Jira remote write를 하지 않고, 이미 export된 로컬 Markdown만 읽습니다.
  - 기본 출력은 현재 작업 폴더의 `.confluence-index/` 입니다.
  - 여러 export 폴더를 반복 색인할 수 있도록 `.confluence-index/sources/<source-id>/` namespace를 사용합니다.
  - 기본적으로 `AGENTS.md` 와 `CLAUDE.md` 에 Reading Rule 관리 블록을 설치합니다. `--no-agent-rules` 로 생략할 수 있습니다.
  - `--agent-files <file> [<file> ...]` 로 Reading Rule을 설치할 guidance 파일을 직접 지정할 수 있습니다.
