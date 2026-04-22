# Confluence Export Kit

Confluence Export Kit은 `Claude Code` 전용 Confluence export-only 플러그인입니다 (v0.1.0). `confluence-markdown-exporter` 기반으로 auth 설정, 다양한 export 범위, keyword/label 검색 export, Python/pipx/`cme` bootstrap을 다룹니다.

이 플러그인은 범용 Atlassian 도구 모음이 아닙니다. 지원 범위는 다음으로 제한됩니다.

- Confluence auth 설정 및 token 검증
- org / space / page tree / 단건 page export
- keyword 또는 label로 매칭된 page만 export
- export runtime bootstrap (`python`, `pip`, `pipx`, `cme`)
- 기본 출력 경로 영구 설정

지원하지 않는 범위는 다음과 같습니다.

- planning brief 작성
- Jira write 작업
- 범용 CQL 콘솔
- `cme config` interactive menu

영문 문서는 [README.en.md](./README.en.md)를 참고하세요.

## 포함된 구성

- `.claude-plugin/plugin.json` — Claude Code 플러그인 매니페스트
- `commands/help.md` — export 워크플로우, 설치, 환경변수 안내
- `commands/set-api-key.md` — auth 설정 커맨드
- `commands/set-output-path.md` — 기본 출력 경로 설정 커맨드
- `commands/export-org.md` — org 전체 export 커맨드
- `commands/export-space.md` — space 전체 export 커맨드
- `commands/export-page-tree.md` — page tree export 커맨드
- `commands/export-page.md` — 단건/다건 page export 커맨드
- `commands/export-by-keyword.md` — keyword 검색 export 커맨드
- `commands/export-by-label.md` — label 검색 export 커맨드
- `commands/config-show.md` — 현재 설정 확인 커맨드
- `skills/set-api-key/SKILL.md` — auth 설정 및 token 검증
- `skills/set-output-path/SKILL.md` — 기본 출력 경로 영구 설정
- `skills/export-org/SKILL.md` — org 전체 export
- `skills/export-space/SKILL.md` — space 전체 export
- `skills/export-page-tree/SKILL.md` — page tree export
- `skills/export-page/SKILL.md` — 단건/다건 page export
- `skills/export-by-keyword/SKILL.md` — keyword 검색 후 매칭 page export
- `skills/export-by-label/SKILL.md` — label 검색 후 매칭 page export
- `skills/config-show/SKILL.md` — 현재 cme 설정 출력
- `scripts/cme_runtime.py` — preflight, bootstrap, config/auth helper 공통 처리

## Export 워크플로우

```text
/confluence-export-kit:set-api-key <api-key> <email>       (최초 1회 auth 설정)
/confluence-export-kit:set-output-path <path>              (선택: 기본 출력 경로 설정)
    │
    ├─► /confluence-export-kit:export-org <org-url> [output-path]
    │       Confluence instance 전체 export
    │
    ├─► /confluence-export-kit:export-space <space-url> [output-path]
    │       space 전체 export
    │
    ├─► /confluence-export-kit:export-page-tree <page-url> [output-path]
    │       page URL 하위 전체 문서 export
    │
    ├─► /confluence-export-kit:export-page <page-url> [<page-url2> ...] [--output-path <path>]
    │       특정 page URL 단건/다건 export
    │
    ├─► /confluence-export-kit:export-by-keyword <keyword> [output-path]
    │       CQL title + text 검색 후 매칭 page만 export
    │
    └─► /confluence-export-kit:export-by-label <label> [output-path]
            CQL label 검색 후 매칭 page만 export
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

이 저장소 루트에서 Claude Code 기준:

```text
/plugin marketplace add https://raw.githubusercontent.com/inkwonjung-colosseum/plugins/main/.claude-plugin/marketplace.json
/plugin install confluence-export-kit@inkwonjung-colosseum-plugins
/reload-plugins
```

## 추천 사용 예

```text
/confluence-export-kit:set-api-key <api-key> <email>
```

```text
/confluence-export-kit:export-page-tree https://colosseum.atlassian.net/wiki/spaces/KEY/pages/123456789/Root
```

```text
/confluence-export-kit:export-by-keyword "incident review" ./exports/confluence
```

```text
/confluence-export-kit:export-by-label "runbook" --space-key OPS --dry-run
```

## 환경변수

| 환경변수 | 기본값 | 설명 |
|---|---|---|
| `CONFLUENCE_EXPORT_KIT_BASE_URL` | `https://colosseum.atlassian.net` | `set-api-key`, `export-by-keyword`, `export-by-label`의 대상 Confluence 사이트 |

## 동작 메모

- `set-api-key`
  - 기본 URL은 `https://colosseum.atlassian.net` 입니다.
  - `CONFLUENCE_EXPORT_KIT_BASE_URL` 또는 `--url` 로 site를 바꿀 수 있습니다.
  - 토큰 검증은 기본 동작입니다. `--skip-validate` 로 생략할 수 있습니다.
  - `auth.confluence` 와 `auth.jira` 를 같은 URL로 동시에 설정합니다.
- `set-output-path`
  - `export.output_path` 를 cme config에 영구 저장합니다.
  - 이후 모든 export는 이 경로를 기본값으로 사용합니다.
- export 명령 공통
  - auth가 없으면 export를 막고 `set-api-key` 실행을 안내합니다.
  - `[output-path]` 는 env override로만 적용하고 config를 영구 수정하지 않습니다.
- `export-by-keyword` / `export-by-label`
  - descendants는 따라가지 않고, 매칭된 page만 export합니다.
  - `--space-key` 로 검색 범위를 특정 space로 제한할 수 있습니다.
