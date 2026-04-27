# confluence-markdown-exporter 지원 기능 정리

## 문서 목적

이 문서는 `confluence-markdown-exporter` 본체가 현재 지원하는 기능을 코드와 공식 배포 문서 기준으로 정리한 것입니다.
또한 이 저장소의 `confluence-export-kit` 래퍼가 그중 어떤 기능만 감싸고 있는지도 같이 정리합니다.

## 확인 기준

- 확인 일자: 2026-04-23
- upstream 패키지 최신 확인 버전: `confluence-markdown-exporter 4.0.8`
- 로컬 래퍼 플러그인 버전: `confluence-export-kit 0.1.2`

## 한눈에 보기

| 구분 | 범위 |
| --- | --- |
| `confluence-markdown-exporter` 본체 | Confluence page/space/org export CLI, config/auth 관리, Markdown 변환, attachment export, 증분 export, stale cleanup, Jira enrichment |
| `confluence-export-kit` 래퍼 | auth 설정, page/space/org/page-with-descendants export, export 후 자동 local index, exported Markdown local index |

## 1. upstream `confluence-markdown-exporter` 본체 기능

### 1.1 CLI 명령

본체 CLI 엔트리포인트는 `cme` 와 `confluence-markdown-exporter` 둘 다 지원합니다.

지원 명령은 다음과 같습니다.

| 명령 | 설명 |
| --- | --- |
| `pages` | 하나 이상의 Confluence page URL을 Markdown으로 export |
| `page` | `pages`의 단수 alias |
| `pages-with-descendants` | 지정한 page와 모든 descendant page를 export |
| `page-with-descendants` | `pages-with-descendants`의 단수 alias |
| `spaces` | 하나 이상의 space 전체를 export |
| `space` | `spaces`의 단수 alias |
| `orgs` | 하나 이상의 Confluence 조직 base URL 아래 모든 space/page를 export |
| `org` | `orgs`의 단수 alias |
| `config` | interactive menu 또는 subcommand로 설정 관리 |
| `version` | 설치된 패키지 버전 출력 |
| `bugreport` | 민감정보를 가린 진단 정보 출력 |

### 1.2 지원 URL 형식

문서와 코드 기준으로 다음 URL 형식을 지원합니다.

| 대상 | 지원 형식 |
| --- | --- |
| Confluence Cloud page | `https://company.atlassian.net/wiki/spaces/SPACEKEY/pages/123456789/Page+Title` |
| Atlassian API gateway page | `https://api.atlassian.com/ex/confluence/CLOUDID/wiki/spaces/SPACEKEY/pages/123456789/Page+Title` |
| Confluence Server page | `https://wiki.company.com/display/SPACEKEY/Page+Title` |
| Confluence Server short page | `https://wiki.company.com/SPACEKEY/Page+Title` |
| Confluence Cloud space | `https://company.atlassian.net/wiki/spaces/SPACEKEY` |
| Atlassian API gateway space | `https://api.atlassian.com/ex/confluence/CLOUDID/wiki/spaces/SPACEKEY` |
| org export base URL | `https://company.atlassian.net` 같은 Confluence instance root |

### 1.3 export 범위

본체가 직접 지원하는 export 범위는 네 단계입니다.

1. page 단건 또는 다건 export
2. page-with-descendants export
3. space 전체 export
4. organization 전체 export

즉, 특정 page만 뽑는 것부터 Confluence instance 전체를 뽑는 것까지 모두 지원합니다.

### 1.4 config 관리 기능

`cme config` 하위 기능은 다음과 같습니다.

| 명령 | 설명 |
| --- | --- |
| `cme config` | interactive 설정 메뉴 열기 |
| `cme config list` | 전체 설정 출력 |
| `cme config list -o json` | 전체 설정을 JSON으로 출력 |
| `cme config get <key>` | 단일 설정 조회 |
| `cme config set key=value` | 하나 이상의 설정 변경 |
| `cme config edit <key>` | 특정 설정 키를 interactive editor로 수정 |
| `cme config path` | 현재 config 파일 경로 출력 |
| `cme config reset` | 전체 설정 초기화 |
| `cme config reset <key>` | 특정 키 또는 섹션 초기화 |

### 1.5 인증 기능

본체는 단일 계정만 다루는 구조가 아니라 URL별 multi-instance auth를 지원합니다.

지원 항목은 다음과 같습니다.

- `auth.confluence` 와 `auth.jira` 를 instance URL별 dict로 저장
- exact URL 매칭과 host/path 기반 fallback 매칭 지원
- `username + api_token` 방식 지원
- `PAT` 기반 인증 지원
- Atlassian Cloud용 `cloud_id` 저장 지원
- Atlassian Cloud에서 `/_edge/tenant_info` 호출로 `cloud_id` 자동 fetch 지원
- `cloud_id`가 있으면 `https://api.atlassian.com/ex/confluence/{cloud_id}` 또는 `.../jira/{cloud_id}` gateway 경로로 SDK 연결
- auth 미설정 상태에서 export를 시도하면 interactive config flow로 유도

### 1.6 환경변수/설정 override

본체는 JSON config와 환경변수 override를 같이 지원합니다.

주요 동작은 다음과 같습니다.

- 기본 config 파일 위치는 app data 디렉터리의 `app_data.json`
- `CME_CONFIG_PATH` 로 config 파일 위치 override 가능
- `CME_...__...` 형식으로 nested 설정 override 가능
- 예: `CME_EXPORT__OUTPUT_PATH`, `CME_CONNECTION_CONFIG__MAX_WORKERS`

### 1.7 export 설정 키

코드상 `ExportConfig` 와 `ConnectionConfig` 가 지원하는 주요 키는 다음과 같습니다.

| 키 | 설명 |
| --- | --- |
| `export.log_level` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `export.output_path` | export 결과 저장 디렉터리 |
| `export.page_href` | page link를 `relative` 또는 `absolute` 로 생성 |
| `export.page_path` | page 파일 경로 template |
| `export.attachment_href` | attachment link를 `relative` 또는 `absolute` 로 생성 |
| `export.attachment_path` | attachment 파일 경로 template |
| `export.attachment_export_all` | 참조된 첨부만이 아니라 전체 attachment export 여부 |
| `export.page_breadcrumbs` | 문서 상단 breadcrumb 포함 여부 |
| `export.filename_encoding` | 파일명 문자 치환 규칙 |
| `export.filename_length` | 최대 파일명 길이 |
| `export.filename_lowercase` | 경로/파일명 강제 lowercase 여부 |
| `export.include_document_title` | 문서 첫머리에 H1 제목 포함 여부 |
| `export.enable_jira_enrichment` | Jira issue summary enrichment 여부 |
| `export.skip_unchanged` | lockfile 기준 unchanged page skip 여부 |
| `export.cleanup_stale` | 삭제되었거나 이동된 page의 로컬 파일 cleanup 여부 |
| `export.lockfile_name` | 증분 export 추적용 lockfile 이름 |
| `export.existence_check_batch_size` | stale page 존재 여부 확인 batch 크기 |
| `connection_config.backoff_and_retry` | retry 활성화 |
| `connection_config.backoff_factor` | backoff multiplier |
| `connection_config.max_backoff_seconds` | retry backoff 상한 |
| `connection_config.max_backoff_retries` | retry 횟수 |
| `connection_config.retry_status_codes` | retry 대상 HTTP status |
| `connection_config.verify_ssl` | SSL 검증 여부 |
| `connection_config.timeout` | API timeout |
| `connection_config.use_v2_api` | Confluence REST API v2 사용 여부 |
| `connection_config.max_workers` | 병렬 export worker 수 |

### 1.8 path template 기능

page와 attachment export path는 template 기반으로 생성됩니다.

지원 변수는 다음과 같습니다.

| 영역 | 지원 변수 |
| --- | --- |
| 공통 | `{space_key}`, `{space_name}`, `{homepage_id}`, `{homepage_title}`, `{ancestor_ids}`, `{ancestor_titles}` |
| page 추가 변수 | `{page_id}`, `{page_title}` |
| attachment 추가 변수 | `{attachment_id}`, `{attachment_title}`, `{attachment_file_id}`, `{attachment_extension}` |

이 template 시스템으로 대상 시스템에 맞는 디렉터리 구조를 만들 수 있습니다.

### 1.9 Markdown 변환 지원 요소

README와 실제 converter 구현을 합치면 다음 요소를 지원합니다.

#### 기본 문서 구조

- heading
- paragraph
- ordered list
- unordered list
- link
- image
- code block
- bold
- italic
- underline 계열 HTML 변환
- blockquote

#### 표와 레이아웃

- 일반 table Markdown 변환
- `rowspan`, `colspan` 보정
- table cell 안 줄바꿈을 `<br/>` 로 보존
- column layout를 table 형태로 변환

#### Confluence 전용 요소

- task list를 GitHub task list로 변환
- breadcrumb 링크 출력
- page link를 export된 Markdown 경로로 재작성
- attachment link를 export된 attachment 경로로 재작성
- heading anchor link 처리
- user mention을 표시 이름으로 변환
- `time` 태그를 datetime 문자열로 변환
- `sub` 는 HTML `<sub>` 유지
- `sup` 는 footnote 문법으로 변환
- page label을 front matter `tags` 로 노출
- page properties를 front matter로 추출
- page properties report(`metadata-summary-macro`)를 표로 변환

#### 매크로 변환

| 매크로/요소 | 변환 방식 |
| --- | --- |
| `panel`, `info`, `note`, `tip`, `warning` | GitHub alert block |
| `details` | page properties 추출 |
| expand container | HTML `<details><summary>` |
| `attachments` | attachment 목록 table |
| `jira` issue macro | 이슈 링크, 필요시 summary enrichment |
| `jira` table macro | Jira table HTML을 Markdown으로 변환 |
| `toc` | body_export 기준 TOC macro 변환 |
| `scroll-ignore` | HTML comment 처리 |
| `drawio` | preview image + 원본 `.drawio` 링크 |
| draw.io preview image inside content | 가능하면 Mermaid 코드블록으로 추출 |
| `plantuml` | ` ```plantuml ` 코드블록 |
| `markdown` | 내부 Markdown 본문 직접 추출 |
| `mohamicorp-markdown` | 내부 Markdown 본문 직접 추출 |

#### add-on / 확장 기능

upstream README에서 명시적으로 언급한 add-on 지원은 다음과 같습니다.

- draw.io
- PlantUML
- Markdown Extensions

### 1.10 attachment 처리 기능

attachment 관련 기능은 단순 다운로드보다 더 넓습니다.

- page export 전에 attachment를 먼저 export
- 기본적으로는 page 본문에 실제로 참조된 attachment만 export
- `export.attachment_export_all=true` 이면 모든 attachment export
- attachment 버전 추적
- unchanged attachment skip
- attachment export path template 적용
- attachment link/image 경로 재작성
- draw.io 원본 `.drawio` 와 preview `.drawio.png` 특수 처리
- attachment 재버전 시 old file cleanup

### 1.11 draw.io / Mermaid / PlantUML 처리

diagram 관련 기능은 다음과 같습니다.

- draw.io 매크로를 preview image와 원본 drawio 파일 링크로 export
- draw.io PNG preview가 가리키는 원본 `.drawio` attachment를 찾아 export
- `.drawio` XML 안 `mermaidData` 가 있으면 Mermaid 코드블록으로 추출
- PlantUML macro는 editor2 XML에서 `umlDefinition` 을 찾아 코드블록으로 변환

### 1.12 Jira enrichment

본체는 선택적으로 Jira API를 같이 사용합니다.

- Jira issue key만 남기는 단순 링크 모드 지원
- Jira enrichment가 켜져 있으면 issue summary를 같이 표시
- Jira auth 실패 시 cached client invalidate 후 auth 재설정 flow로 유도
- Confluence URL에서 Jira base URL을 유도해 Jira client 연결

### 1.13 증분 export / cleanup

본체는 lockfile 기반 증분 export를 지원합니다.

- 기본 lockfile 이름은 `confluence-lock.json`
- page version, export path, attachment version을 기록
- unchanged page skip
- output file이 사라졌으면 재export
- export path가 바뀌면 old path file 삭제
- Confluence에서 삭제된 page는 local file과 lock entry를 cleanup
- stale check는 v2 API 또는 v1 CQL 방식으로 batch 수행

### 1.14 병렬 처리 / 실행 동작

- `ThreadPoolExecutor` 기반 page export 병렬 처리
- 기본 `max_workers=20`
- thread-local Confluence client 사용
- `DEBUG` 또는 `max_workers <= 1` 이면 serial mode
- Rich progress bar, spinner, summary panel 출력
- CI 환경에서는 컬러와 live redraw를 줄여 log-friendly 하게 동작

### 1.15 디버깅 / 진단 기능

- `DEBUG` 로그 레벨에서 page별 raw source 파일 export
- `_body_view.html`
- `_body_export_view.html`
- `_body_editor2.xml`
- `bugreport` 명령으로 버전, 플랫폼, redacted config 출력

## 2. 확인된 제약과 주의사항

코드 기준으로 확인된 주의사항은 다음과 같습니다.

- upstream 본체에는 `keyword search export` 전용 CLI 명령이 없습니다.
- `TOC macro` 여러 개가 있는 경우 현재 구현은 다중 TOC를 지원하지 않고 무시 또는 경고합니다.
- `Jira table macro` 여러 개가 있는 경우 현재 구현은 다중 table을 지원하지 않고 무시 또는 경고합니다.
- 접근 불가 page는 `"Page not accessible"` placeholder로 처리하고 export를 건너뜁니다.
- self-hosted CQL 기반 stale existence check는 batch size가 내부적으로 최대 25로 cap 됩니다.

## 3. 이 저장소의 `confluence-export-kit` 래퍼가 제공하는 기능

`confluence-export-kit` 는 upstream 전체를 노출하지 않고 Confluence export와 local export-index workflow만 좁게 감쌉니다.

### 3.1 래퍼 명령

| 명령 | 설명 |
| --- | --- |
| `/confluence-export-kit:help` | 사용법 안내 |
| `/confluence-export-kit:set-config [--api-key <api-key> --email <email>] [--output-path <path>] [--url <base-url>] [--skip-jira] [--config-path <path>]` | auth와 기본 export 출력 경로 통합 설정 |
| `/confluence-export-kit:export-page <page-url> [<page-url> ...] [output-path]` | 하나 이상의 page URL export |
| `/confluence-export-kit:export-page-with-descendant <page-url> [<page-url> ...] [output-path]` | 하나 이상의 page와 모든 descendant export |
| `/confluence-export-kit:export-space <space-url> [<space-url> ...] [output-path]` | 하나 이상의 space 전체 export |
| `/confluence-export-kit:export-org <org-url> [<org-url> ...] [output-path]` | 하나 이상의 org 전체 export |
| `/confluence-export-kit:index-export <export-path> [--source-id <id>] [--index-root <path>] [--no-agent-rules] [--agent-files <file> ...]` | 이미 export된 로컬 Markdown 폴더 색인 및 Reading Rule 설치 |
| `/confluence-export-kit:show-config [--json]` | 현재 `cme` 설정 출력 (`cme config list` 래퍼) |

모든 export 명령은 다음 공통 플래그를 지원합니다.

| 플래그 | 설명 |
| --- | --- |
| `--skip-unchanged` / `--no-skip-unchanged` | lockfile 기반 증분 export 제어. 기본값은 on |
| `--cleanup-stale` / `--no-cleanup-stale` | Confluence에서 삭제/이동된 page의 로컬 파일 cleanup 제어. 기본값은 on |
| `--jira-enrichment` | Jira issue summary를 export된 Markdown에 포함 |
| `--max-workers N` | `CME_CONNECTION_CONFIG__MAX_WORKERS` 설정으로 병렬 worker 수 제어 |

### 3.2 래퍼가 추가하는 기능

래퍼는 upstream에 없는 workflow 기능도 일부 추가합니다.

- export 명령은 `cme`와 config/auth가 이미 준비되어 있다고 가정
- `set-config` 명령은 `pip` 기준으로 `confluence-markdown-exporter` 설치 여부를 확인하고, 없으면 설치
- `set-config` 실행 시 token probe 없이 credential 저장
- `set-config` 실행 시 기본적으로 `auth.jira` 도 같은 URL로 맞춤 (`--skip-jira` 로 생략 가능)
- 모든 export 명령에서 `output-path` 를 환경변수 override로만 적용하고 config는 영구 수정하지 않음
- 명시적 output path가 없으면 현재 helper는 `confluence` 를 effective output path로 사용
- 모든 export 명령은 `cme` export 성공 후 같은 effective output path를 자동으로 `index-export` 처리
- post-export `index-export` 는 기본적으로 `AGENTS.md` / `CLAUDE.md` Reading Rule 관리 블록도 설치 또는 갱신
- `set-config` 명령으로 `cme` config의 `export.output_path` 를 영구 저장
- 모든 export 명령에서 `--skip-unchanged` / `--no-skip-unchanged` 플래그로 `CME_EXPORT__SKIP_UNCHANGED` 설정 가능
- 모든 export 명령에서 `--cleanup-stale` / `--no-cleanup-stale` 플래그로 `CME_EXPORT__CLEANUP_STALE` 설정 가능
- 모든 export 명령에서 `--jira-enrichment` 플래그로 `CME_EXPORT__ENABLE_JIRA_ENRICHMENT=true` 설정 가능
- 모든 export 명령에서 `--max-workers N` 플래그로 `CME_CONNECTION_CONFIG__MAX_WORKERS` 설정 가능
- `show-config` 명령으로 `cme config list` 결과를 Claude Code / Codex workflow에서 직접 확인 가능
- `index-export` 명령으로 이미 export된 로컬 Markdown을 `.confluence-index/sources/<source-id>/` 로 색인 가능
- `index-export` 명령으로 현재 작업 폴더의 `AGENTS.md` / `CLAUDE.md` 또는 `--agent-files` 로 지정한 guidance 파일에 Reading Rule 관리 블록 설치 가능

### 3.3 래퍼가 의도적으로 제외한 범위

로컬 README 기준 non-goal은 다음과 같습니다.

- planning brief 작성
- remote Confluence/Jira write workflow
- 범용 CQL console
- `cme config` interactive menu 노출

## 4. 본체 기능 대비 래퍼 노출 범위

| 기능 | upstream 본체 | `confluence-export-kit` 래퍼 |
| --- | --- | --- |
| page export | 지원 | 직접 노출 (`export-page`) |
| page-with-descendants export | 지원 | 직접 노출 (`export-page-with-descendant`) |
| space export | 지원 | 직접 노출 (`export-space`) |
| org export | 지원 | 직접 노출 (`export-org`) |
| 증분 export (`skip_unchanged`) | 지원 | 모든 export 명령에 `--skip-unchanged` / `--no-skip-unchanged` 플래그로 노출 |
| 기본 출력 경로 설정 | config set으로 가능 | `set-config` 명령으로 config 저장 노출. 현재 export helper의 no-override 기본값은 `confluence` |
| config interactive menu | 지원 | 미노출 |
| config list | 지원 | `show-config` 명령으로 제한 노출 |
| config set | 지원 | `set-config` workflow로 제한 노출 |
| config get/edit/reset/path | 지원 | 미노출 |
| version/bugreport | 지원 | 미노출 |
| multi-instance auth | 지원 | helper script로 일부 지원 |
| keyword search export | 표준 CLI 없음 | 미노출 |
| label search export | 표준 CLI 없음 | 미노출 |
| 병렬 worker 수 제어 | `connection_config.max_workers` 지원 | 모든 export 명령에 `--max-workers N` 플래그로 노출 |
| stale page cleanup | `export.cleanup_stale` 지원 | 모든 export 명령에 `--cleanup-stale` / `--no-cleanup-stale` 플래그로 노출 |
| Jira enrichment toggle | `export.enable_jira_enrichment` 지원 | 모든 export 명령에 `--jira-enrichment` 플래그로 노출 |
| `confluence-markdown-exporter` 설치 확인 | 본체 설치 문서만 제공 | `set-config` 가 pip 기준으로 확인하고 없으면 설치 |
| exported Markdown local index | 표준 CLI 없음 | export 후 자동 실행 및 `index-export` 명령으로 `.confluence-index/` 생성 |
| AGENTS.md / CLAUDE.md Reading Rule 설치 | 표준 CLI 없음 | export 후 자동 실행 및 `index-export` 명령으로 관리 블록 설치 |

## 5. 문서 해석 가이드

- 이 문서는 `confluence-markdown-exporter` 본체가 할 수 있는 일 전체를 기준으로 썼습니다.
- `confluence-export-kit` 사용 가능 범위만 보려면 3장과 4장을 보면 됩니다.
- 래퍼 문서를 확장할 때는 upstream 본체가 이미 지원하는 기능인지, 래퍼가 새 workflow를 얹은 기능인지 먼저 분리해서 다루는 것이 안전합니다.

## 6. 근거 자료

### upstream

- PyPI: <https://pypi.org/project/confluence-markdown-exporter/>
- GitHub: <https://github.com/Spenhouet/confluence-markdown-exporter>

### 로컬 래퍼

- `confluence-export-kit/README.md`
- `confluence-export-kit/.claude-plugin/plugin.json`
- `confluence-export-kit/.codex-plugin/plugin.json`
- `confluence-export-kit/scripts/cme_runtime.py`
- `confluence-export-kit/skills/help/SKILL.md`
- `confluence-export-kit/skills/set-config/SKILL.md`
- `confluence-export-kit/skills/set-config/scripts/set_config.py`
- `confluence-export-kit/skills/export-page/SKILL.md`
- `confluence-export-kit/skills/export-page/scripts/export_page.py`
- `confluence-export-kit/skills/export-page-with-descendant/SKILL.md`
- `confluence-export-kit/skills/export-page-with-descendant/scripts/export_page_with_descendant.py`
- `confluence-export-kit/skills/export-space/SKILL.md`
- `confluence-export-kit/skills/export-space/scripts/export_space.py`
- `confluence-export-kit/skills/export-org/SKILL.md`
- `confluence-export-kit/skills/export-org/scripts/export_org.py`
- `confluence-export-kit/skills/index-export/SKILL.md`
- `confluence-export-kit/skills/index-export/scripts/index_export.py`
- `confluence-export-kit/skills/show-config/SKILL.md`
- `confluence-export-kit/skills/show-config/scripts/show_config.py`
- `confluence-export-kit/tests/test_export_page.py`
- `confluence-export-kit/tests/test_export_page_with_descendant.py`
- `confluence-export-kit/tests/test_export_space.py`
- `confluence-export-kit/tests/test_export_org.py`
- `confluence-export-kit/tests/test_set_config.py`
- `confluence-export-kit/tests/test_show_config.py`
