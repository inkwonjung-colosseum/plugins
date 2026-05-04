# confluence-export-kit 스킬 설명서

## 문서 목적

이 문서는 `confluence-export-kit`에 포함된 모든 스킬을 한 곳에서 설명합니다.

기준 소스는 각 `confluence-export-kit/skills/*/SKILL.md`이며, 이 문서는 사용자와 플러그인 관리자가 빠르게 스킬 목적, 호출법, 전제 조건, 산출물을 확인하기 위한 참조 문서입니다.

`confluence-export-kit`은 범용 Atlassian 작업 도구가 아니라 Confluence 문서를 로컬 Markdown으로 export하고, export 결과를 agent가 읽기 쉬운 local export-index로 정리하는 플러그인입니다.

## 전체 스킬 목록

| 스킬 | 사용자 호출 | 목적 | 주요 산출물 |
|---|---|---|---|
| `set-config` | 예 | Confluence 인증과 고정 export 기본값 설정 | `cme` config 업데이트 |
| `show-config` | 예 | 현재 `confluence-markdown-exporter` 설정 출력 | `cme config list` 출력 |
| `export-page` | 예 | 하나 이상의 개별 page export | `./confluence` Markdown export + `.confluence-index/` |
| `export-page-with-descendant` | 예 | root page와 모든 descendant page export | `./confluence` Markdown export + `.confluence-index/` |
| `export-space` | 예 | 하나 이상의 space 전체 export | `./confluence` Markdown export + `.confluence-index/` |
| `export-org` | 예 | 하나 이상의 Confluence instance 전체 export | `./confluence` Markdown export + `.confluence-index/` |
| `index-export` | 보통 직접 호출 안 함 | 이미 export된 Markdown 폴더 인덱싱 | `.confluence-index/`, Reading Rule block |

## 호출 문법

Claude Code에서는 플러그인 namespace가 붙은 slash command를 사용합니다.

```text
/confluence-export-kit:set-config --api-key <api-key> --email <email>
/confluence-export-kit:show-config
/confluence-export-kit:export-page <page-url> [<page-url> ...]
/confluence-export-kit:export-page-with-descendant <page-url> [<page-url> ...]
/confluence-export-kit:export-space <space-url> [<space-url> ...]
/confluence-export-kit:export-org <org-url> [<org-url> ...]
```

Codex에서는 설치된 플러그인의 skill invocation을 사용합니다.

```text
$set-config --api-key <api-key> --email <email>
$show-config
$export-page <page-url> [<page-url> ...]
$export-page-with-descendant <page-url> [<page-url> ...]
$export-space <space-url> [<space-url> ...]
$export-org <org-url> [<org-url> ...]
```

`index-export`는 export 스킬이 성공한 뒤 자동 실행하는 background workflow로 취급합니다. 일반 사용 요청에서 먼저 고르는 스킬은 아닙니다.

## 기본 사용 흐름

```text
set-config
  |
  +-- export-page
  +-- export-page-with-descendant
  +-- export-space
  +-- export-org
        |
        +-- index-export
              |
              +-- .confluence-index/
              +-- AGENTS.md / CLAUDE.md Reading Rule block
```

1. 최초 1회 `set-config`로 인증과 export 기본값을 저장합니다.
2. 필요한 export 범위에 따라 page, page-with-descendant, space, org 중 하나를 실행합니다.
3. export 결과는 고정 경로 `./confluence`에 생성됩니다.
4. export가 성공하면 `index-export`가 자동으로 실행되어 `.confluence-index/`를 갱신합니다.
5. agent guidance 파일에는 Confluence source-of-truth 읽기 규칙이 설치 또는 갱신됩니다.

## 공통 export 규칙

`export-page`, `export-page-with-descendant`, `export-space`, `export-org`는 공통으로 다음 규칙을 따릅니다.

| 항목 | 동작 |
|---|---|
| 인증 전제 | `cme`, config, auth가 이미 준비되어 있다고 가정 |
| target 검증 | wrapper에서 URL을 검증하지 않고 `cme`에 그대로 전달 |
| output path | 실행 환경에서 `CME_EXPORT__OUTPUT_PATH=./confluence` 강제 |
| output override | per-export output path 옵션 미노출 |
| API token 출력 | 저장된 token을 사용자에게 출력하지 않음 |
| 후처리 | `cme` export 성공 후 `index-export` 자동 실행 |
| export 기본값 | `set-config`가 저장한 config를 사용 |

`set-config`가 고정하는 주요 export 기본값은 다음과 같습니다.

| 설정 | 값 | 의미 |
|---|---|---|
| `export.output_path` | `./confluence` | 기본 export 저장 위치 |
| `export.skip_unchanged` | `true` | 변경 없는 page는 증분 export에서 skip |
| `export.cleanup_stale` | `true` | Confluence에서 삭제/이동된 page의 로컬 파일 정리 |
| `export.enable_jira_enrichment` | `false` | Jira issue summary enrichment 비활성화 |
| `export.include_document_title` | `false` | export 본문에 문서 제목 H1 중복 방지 |
| `export.page_breadcrumbs` | `false` | export 본문 상단 breadcrumb 제외 |

## 스킬별 설명

### `set-config`

Confluence 인증 정보와 export 기본값을 `confluence-markdown-exporter` config에 저장합니다.

| 항목 | 설명 |
|---|---|
| 입력 | `--api-key <api-key> --email <email> [--url <base-url>]` |
| 기본 URL | `CONFLUENCE_EXPORT_KIT_BASE_URL`, 없으면 `https://colosseum.atlassian.net` |
| 필수 조건 | `--api-key`와 `--email`은 반드시 함께 전달 |
| 내부 동작 | `confluence-markdown-exporter` 설치 여부를 `pip` 기준으로 확인하고, 없으면 설치 |
| config 범위 | `auth.confluence`, `auth.jira`, export 기본값을 한 번에 저장 |
| 보안 규칙 | API token을 사용자 응답에 다시 출력하지 않음 |

사용 예:

```text
/confluence-export-kit:set-config --api-key <api-key> --email <email>
$set-config --api-key <api-key> --email <email> --url https://example.atlassian.net
```

이 스킬은 token 유효성 probe를 하지 않습니다. 전달된 credential은 사용자가 저장 의도로 제공한 값으로 간주합니다.

### `show-config`

현재 `confluence-markdown-exporter` 설정을 그대로 보여줍니다.

| 항목 | 설명 |
|---|---|
| 입력 | 없음 또는 `--json` |
| 기본 동작 | `cme config list` 실행 |
| JSON 출력 | `--json` 전달 시 `cme config list -o json` 실행 |
| 응답 원칙 | 출력 전체를 요약하거나 해석하지 않고 표시 |
| 주의 | 설정을 조회만 하며 수정하지 않음 |

사용 예:

```text
/confluence-export-kit:show-config
/confluence-export-kit:show-config --json
$show-config --json
```

### `export-page`

하나 이상의 개별 Confluence page URL을 로컬 Markdown으로 export합니다.

| 항목 | 설명 |
|---|---|
| 입력 | `<page-url> [<page-url> ...]` |
| upstream 명령 | `cme pages <url1> [url2 ...]` |
| 대상 | 특정 page 단건 또는 다건 |
| output path | `./confluence` |
| 후처리 | export 성공 후 `index-export ./confluence` 자동 실행 |

사용 예:

```text
/confluence-export-kit:export-page https://example.atlassian.net/wiki/spaces/KEY/pages/123/Page
$export-page https://example.atlassian.net/wiki/spaces/KEY/pages/123/Page https://example.atlassian.net/wiki/spaces/KEY/pages/456/Page2
```

특정 문서 몇 개만 뽑아야 할 때 사용합니다. 하위 페이지는 자동 포함하지 않습니다.

### `export-page-with-descendant`

하나 이상의 root page와 그 아래 모든 descendant page를 함께 export합니다.

| 항목 | 설명 |
|---|---|
| 입력 | `<page-url> [<page-url> ...]` |
| upstream 명령 | `cme pages-with-descendants <page-url> [<page-url2> ...]` |
| 대상 | root page와 전체 하위 문서 |
| output path | `./confluence` |
| 후처리 | export 성공 후 `index-export ./confluence` 자동 실행 |

사용 예:

```text
/confluence-export-kit:export-page-with-descendant https://example.atlassian.net/wiki/spaces/KEY/pages/123/Root
$export-page-with-descendant https://example.atlassian.net/wiki/spaces/KEY/pages/123/Root
```

제품 문서 묶음, 기능 문서 트리, 특정 상위 page 아래의 하위 문서를 함께 가져올 때 가장 자주 쓰는 export 스킬입니다.

### `export-space`

하나 이상의 Confluence space 전체를 export합니다.

| 항목 | 설명 |
|---|---|
| 입력 | `<space-url> [<space-url> ...]` |
| upstream 명령 | `cme spaces <space-url> [<space-url2> ...]` |
| 대상 | space 안의 모든 page |
| output path | `./confluence` |
| 후처리 | export 성공 후 `index-export ./confluence` 자동 실행 |

사용 예:

```text
/confluence-export-kit:export-space https://example.atlassian.net/wiki/spaces/KEY
$export-space https://example.atlassian.net/wiki/spaces/KEY
```

space 단위로 전체 문서 snapshot을 만들 때 사용합니다. 문서 수와 첨부파일이 많으면 실행 시간이 길어질 수 있습니다.

### `export-org`

하나 이상의 Confluence instance root 아래 접근 가능한 모든 space와 page를 export합니다.

| 항목 | 설명 |
|---|---|
| 입력 | `<org-url> [<org-url> ...]` |
| upstream 명령 | `cme orgs <org-url> [<org-url2> ...]` |
| 대상 | Confluence instance 전체 |
| output path | `./confluence` |
| 후처리 | export 성공 후 `index-export ./confluence` 자동 실행 |

사용 예:

```text
/confluence-export-kit:export-org https://example.atlassian.net
$export-org https://example.atlassian.net
```

가장 넓은 범위의 export입니다. 필요한 범위가 page tree나 space로 충분하면 더 작은 스킬을 먼저 선택하는 것이 좋습니다.

### `index-export`

이미 Confluence에서 export된 로컬 Markdown 폴더를 agent가 탐색하기 쉬운 `.confluence-index/`로 인덱싱합니다.

| 항목 | 설명 |
|---|---|
| 입력 | `<export-path> [--source-id <id>] [--index-root <path>] [--no-agent-rules] [--agent-files <file> ...]` |
| remote 작업 | 없음. Confluence/Jira를 호출하지 않음 |
| source 수정 | 없음. export된 Markdown source 파일을 수정하지 않음 |
| 기본 source ID | export folder basename을 kebab-case로 변환 |
| 기본 index root | 현재 작업 폴더의 `.confluence-index/` |
| guidance 파일 | 기본적으로 `AGENTS.md`, `CLAUDE.md`에 Reading Rule block 설치 또는 갱신 |

생성 또는 갱신하는 주요 파일:

```text
.confluence-index/
├── registry.json
├── tree.md
├── stats.md
├── log.md
└── sources/
    └── <source-id>/
        ├── source-index.jsonl
        ├── tree.md
        ├── stats.md
        └── log.md
```

주요 규칙:

- `<source-id>`가 이미 다른 export path를 가리키면 중단합니다.
- `title`, `status`, `source_type` 또는 `type` scalar front matter를 우선 사용합니다.
- metadata가 없으면 heading과 path 기반 fallback을 사용합니다.
- `log.md`는 append-only로 누적하고, 기존 로그를 단순 재작성하지 않습니다.
- Reading Rule block은 관리 구간 안의 내용만 교체하고 나머지 파일 내용은 보존합니다.
- Reading Rule은 Confluence를 source of truth로, 로컬 Markdown을 read-only snapshot으로 취급하게 만듭니다.
- 파생 wiki, entity, concept, summary, product-context page를 source-of-truth처럼 유지하지 않도록 제한합니다.
- planning output은 사람이 Confluence에 반영하기 전까지 draft-only로 취급합니다.

`index-export`는 Codex metadata에서 `allow_implicit_invocation: false`로 설정되어 있습니다. 즉 일반 요청에 자동 주입되지 않도록 두고, export 스킬의 성공 후처리 경로에서 실행하는 것이 기본 사용 방식입니다.

## 스킬 선택 기준

| 원하는 작업 | 선택할 스킬 |
|---|---|
| 처음 인증과 기본값을 저장해야 함 | `set-config` |
| 현재 `cme` 설정을 확인해야 함 | `show-config` |
| page 몇 개만 export | `export-page` |
| 상위 page 아래 문서 트리를 export | `export-page-with-descendant` |
| space 전체를 export | `export-space` |
| Confluence instance 전체를 export | `export-org` |
| 이미 export된 Markdown을 다시 색인 | `index-export` |

## 지원하지 않는 것

`confluence-export-kit`은 다음 작업을 맡지 않습니다.

- remote Confluence page 생성, 수정, 삭제
- Jira issue 생성, 수정, 전환
- Confluence/Jira 범용 검색 콘솔
- `cme config` interactive menu 대체
- 기획서 또는 정책서 작성
- export된 Markdown을 source of truth로 승격하는 파생 지식베이스 관리

## 관련 근거 파일

| 파일 | 역할 |
|---|---|
| `confluence-export-kit/README.md` | 플러그인 전체 개요와 설치/워크플로우 |
| `confluence-export-kit/skills/*/SKILL.md` | 각 스킬의 authoritative 실행 규칙 |
| `confluence-export-kit/skills/*/agents/openai.yaml` | Codex 표시 정보와 implicit invocation 정책 |
| `confluence-export-kit/scripts/cme_runtime.py` | 공통 `cme` 실행/runtime helper |
| `confluence-export-kit/docs/confluence-markdown-exporter-supported-features.md` | upstream `cme` 기능과 wrapper 지원 범위 비교 |
