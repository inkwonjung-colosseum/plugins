# connector-routing

`planning-format`의 fetch 단계 lookup data — 인증 게이트 휴리스틱·MCP 카탈로그·호스트 매핑·Google Workspace tool 시퀀스·gid/range 처리·fallback 케이스 표·status 표기·sanity check 메시지. **0.2.2부터 `planning-review` R1/R3 SSOT corpus link follow도 같이 사용**하고, **0.2.6부터 `planning-review` input collection도 같이 사용**하며, **0.2.7부터 `ssot-audit` 외부 링크 follow도 같이 사용**한다. review 입력 URL fetch, SSOT corpus link follow, ssot-audit 외부 follow는 본 reference를 공유 적재하지만 visited set·출처 블록은 서로 분리한다 (별도 복제 없음).

## 1. 인증 게이트 휴리스틱

WebFetch 응답이 200 OK인데도 다음 중 하나가 보이면 **인증 게이트 분류** (= fallback 진입):

- `<form ... action="...login..."` / `...signin...` 패턴.
- `Atlassian` / `Confluence` / `Jira` 단어 + `Log In` 버튼 텍스트.
- Figma의 `<title>Log in &mdash; Figma</title>` / `Sign up to view`.
- Google `accounts.google.com` redirect 발자국 (`<meta http-equiv="refresh" ...accounts.google.com...>` 또는 본문 메타).
- Slack의 `Sign in to your workspace`.
- Notion의 `Log in to Notion`.

## 2. MCP/connector 카탈로그 평가

세션의 사용 가능 MCP tool 이름(예: `mcp__claude_ai_Atlassian__*`, `mcp__claude_ai_Figma__*`, `mcp__claude_ai_Google_Drive__*`, `mcp__claude_ai_Slack__*`, `mcp__claude_ai_Notion__*`)을 메모리 캐시.

### 인증 상태 판정 (3분류)

- **인증됨**: 자원 조회 도구가 1개 이상 노출 (`authenticate` 노출 여부 무관).
- **미인증**: `authenticate`만 노출 + 자원 조회 도구 모두 부재.
- **미연결**: `authenticate`·자원 조회 도구 모두 부재 → fallback 후보 0.

### 서비스별 자원 조회 도구

- Atlassian: `getConfluencePage` / `getJiraIssue` / `fetch` 중 하나 이상.
- Figma: `get_design_context` / `get_figjam` / `get_metadata` / `get_screenshot` 중 하나 이상.
- Google Drive: `read_file_content` / `get_file_metadata` / `search_files` / `download_file_content` 중 하나 이상.
- Slack: `slack_read_thread` / `slack_read_channel` / `slack_read_canvas` / `slack_search_*` 중 하나 이상.
- Notion: `authenticate` 외 페이지 조회 도구.

Atlassian만 예외적으로 `getAccessibleAtlassianResources` 1회 호출해 cloud id list 캐시.

## 3. 호스트 매핑표

매칭 규칙: 호스트의 **eTLD+1** (또는 명시 패턴) 기준. `www.` prefix 무시. 한 URL이 여러 행에 걸치면 위에서 먼저 일치한 행.

| # | 호스트 패턴 | 사용 MCP / connector | 대상 리소스 | 비고 |
|---|------------|----------------------|--------------|------|
| 1 | `*.atlassian.net` (path가 `/wiki/...`) | Atlassian MCP — `getConfluencePage` (page id 추출 가능 시) / `fetch` | Confluence page | URL에 `pages/<id>` 또는 `viewpage.action?pageId=<id>`가 있으면 page id 추출. 없으면 `fetch`. |
| 2 | `*.atlassian.net` (path가 `/browse/<KEY-NUM>` 또는 `/jira/...`) | Atlassian MCP — `getJiraIssue` (key 추출) / `fetch` | Jira issue | issue key를 path에서 추출. summary + description + recent comments 합류. |
| 3 | `figma.com/file/...`, `figma.com/design/...`, `figma.com/board/...`, `figma.com/slides/...`, `figma.com/make/...` | Figma MCP — `get_design_context`(design) / `get_figjam`(board) / `get_metadata`(slides·make) | Figma 파일/노드 | URL에서 `fileKey`(또는 `branchKey`)·`nodeId` 추출. node-id의 `-`를 `:`로 변환. |
| 4 | Google Workspace 호스트 (3.4 표) | Google Drive connector — 자원별 tool 시퀀스 (3.4) | Docs / Sheets / Slides / Drive 파일·폴더 | fileId·folderId·gid·range 추출. fragment 처리 3.5. |
| 5 | `*.slack.com/archives/<channel>/p<ts>`, `*.slack.com/archives/<channel>` | Slack MCP — `slack_read_thread`(thread ts) / `slack_read_channel`(채널) | Slack 메시지/스레드 | thread 영구링크면 ts 추출. 채널 단독이면 최근 메시지 N개(default 50). private 채널은 connector 권한 의존. |
| 6 | `*.slack.com` 그 외 path | Slack MCP — `slack_read_canvas`(canvas URL) / `slack_search_public_and_private`(쿼리=path 토큰) / `fetch` | Slack search/canvas 등 | canvas는 `slack_read_canvas` 우선. 그 외 `fetch` 폴백. |
| 7 | `notion.so`, `*.notion.site` | Notion connector — 페이지 조회 도구 | Notion page | path에서 page id(마지막 dash 뒤 32자) 추출. |

### 3.4 Google Workspace 자원별 tool 시퀀스

| 자원 | URL 패턴 | fileId 추출 정규식 | tool 시퀀스 (1순위 → 폴백) |
|---|---|---|---|
| Google Docs | `docs.google.com/document/d/<fileId>/edit...` | `/document/d/([A-Za-z0-9_-]+)` | `read_file_content({ id })` → `get_file_metadata({ id })` |
| Google Sheets | `docs.google.com/spreadsheets/d/<fileId>/edit...` | `/spreadsheets/d/([A-Za-z0-9_-]+)` | `read_file_content({ id })` → `download_file_content({ id, mimeType: "text/csv" })` → `get_file_metadata({ id })` |
| Google Slides | `docs.google.com/presentation/d/<fileId>/edit...` | `/presentation/d/([A-Za-z0-9_-]+)` | `read_file_content({ id })` → `get_file_metadata({ id })` |
| Google Drive 파일 | `drive.google.com/file/d/<fileId>/...`, `drive.google.com/open?id=<fileId>` | `/file/d/([A-Za-z0-9_-]+)` 또는 `[?&]id=([A-Za-z0-9_-]+)` | `read_file_content({ id })` → `download_file_content({ id, mimeType: <export> })` → `get_file_metadata({ id })` |
| Google Drive 폴더 | `drive.google.com/drive/folders/<folderId>` | `/folders/([A-Za-z0-9_-]+)` | `search_files({ parents: folderId })`. 자식 file은 visited queue로 push. |
| Sheets 단축 | `sheets.google.com/...` | spreadsheets 동일 | spreadsheets 시퀀스 |
| Slides 단축 | `slides.google.com/...` | presentation 동일 | presentation 시퀀스 |

### 3.5 Sheets fragment 처리 (`#gid=`, `&range=`)

1. **gid 추출**: query 또는 fragment에서 `gid=<digits>` 매칭. 추출 시 → `read_file_content` 응답에서 해당 시트만 합류 (분할 안 됐으면 전체).
2. **range 추출**: fragment에서 `range=<cellRange>` (예: `C13`, `A1:D20`). 추출 시 → 응답 표에서 범위만 잘라 합류. 자르기 어려우면 시트 전체 + 출처 list `상태` 컬럼 부연 `범위 힌트: <range>`.
3. **추출 실패** → 시트 전체 합류.
4. 본문 합류 헤더 형식:
   ```
   === [출처 N] Google Sheets: <원본 URL> (gid=<sheetGid>, range=<cellRange>) ===
   ```

## 4. 런타임 MCP 카탈로그 추론 (매핑 외 호스트)

2 카탈로그 tool 이름에서 외부 서비스 단서를 본다 — `Linear`/`Intercom`/`Canva`/`Box`/`HubSpot`/`monday`/`Microsoft_365`/`Asana`/`Pencil` 등. 대상 URL 호스트가 단서의 기성 도메인(`linear.app`, `intercom.com`, `canva.com`, `box.com`, `hubspot.com`, `monday.com`, `microsoftonline.com`, `asana.com`)과 일치하거나 subdomain이면 해당 MCP의 일반 `fetch` 도구를 후보로. 추론 결과는 호출 안 메모리 캐시. 추론 실패 = 후보 0.

## 5. fallback 평가 케이스 표

**진입 조건 (0.2.5)**: 모든 케이스는 "**1차 WebFetch 시도 후**" 결과 분류. main이 2 connector 카탈로그 사전 평가로 "미연결"·"미인증"·"매핑 없음" 판정해도 1차 WebFetch는 강제로 진행 (사전 skip 금지). 각 후보 호출 timeout 30초, 1회. 응답 비어 있거나 에러면 다음 후보. 모두 실패하면 status 기록 + visited 등록 후 다음 URL.

매핑 lookup 호스트는 **원래 입력된 URL의 호스트** — redirect 최종 호스트 X.

connector fallback 후보는 2 카탈로그 인증 상태에 따라:
- **인증됨**: 1회 호출 시도.
- **미인증·미연결**: 호출 안 함 (시도해도 실패 자명). 1차 WebFetch 결과로만 분류.

| 케이스 (1차 WebFetch 시도 후) | 처리 |
|---|---|
| connector 호출 1건 이상 성공 | 응답 텍스트로 본문 합류. status=`200 (via <connector> — <tool>)`. |
| connector 모두 실패 + 1차 200 OK + 인증 게이트 아님 | 1차 본문 사용. status=`200 (via WebFetch)`. |
| connector 모두 실패 + 1차 인증 게이트 | 본문 합류 안 함. status=`인증 필요 (<connector> 미인증)`. |
| connector 모두 실패 + 1차 4xx/5xx/timeout | 본문 합류 안 함. status=1차 status·error 그대로. |
| 매핑·추론 후보 0 + 1차 인증 게이트 | 본문 합류 안 함. status=`인증 필요 (connector 매핑 없음)`. |
| connector 미연결 + 1차 인증 게이트 | 본문 합류 안 함. status=`인증 필요 (<connector> 미연결)`. |
| Google Drive 본문 추출 실패 + `get_file_metadata` 성공 | metadata만 합류. status=`metadata only (via Google Drive connector — get_file_metadata)`. |
| fetch 봉쇄 옵션 ON | 1차·fallback 모두 봉쇄. visited만 기록, 본문 합류 0. `planning-format --no-fetch`, `planning-review --no-input-fetch`, `planning-review --no-ssot-fetch`, `ssot-audit --no-follow-links`가 각자 적용 범위에서 유일한 fetch 미시도 케이스다. |

**0.2.5 변경**: 본문 합류 안 함 케이스도 출처 list에 1행 차지. dequeue 후 행 누락 금지. status는 위 표 사유 그대로 기록.

connector 응답이 image content-type이면 image queue로 라우팅. status=`image/<subtype> <bytesize> (via <connector>)`.

## 6. 자식 링크 추출

connector 경유 본문도 자식 URL을 추출해 visited queue로 push (`is_followable`: http(s) + visited 미포함). 같은 자원의 다른 URL 형태(Atlassian short link `/x/...` ↔ 정식 page URL, Figma `figma.com/file/<key>` ↔ `figma.com/design/<key>`, Sheets `?gid=` ↔ `#gid=`)는 normalize 후 host+path만 비교라 별개 자원으로 본다 (dedup 강화 비목표). connector 응답 canonical URL을 알 수 있으면 visited에 같이 등록해 dedup 시도.

## 7. 출처 list `상태` 컬럼 표기

**성공**:
- `200 (via WebFetch)`
- `200 (via Atlassian MCP)` / `200 (via Figma MCP)` / `200 (via Slack MCP)` / `200 (via Notion connector)`
- `200 (via Google Drive connector — read_file_content)` / `... — download_file_content` / `... — search_files`
- `metadata only (via Google Drive connector — get_file_metadata)`
- `image/<subtype> <bytesize> (via Figma MCP)`
- 부연 형식: `200 (via Google Drive connector — read_file_content) | 범위 힌트: C13`

**실패·skip**:
- `인증 필요 (<connector> 미인증)` — Atlassian/Figma/Google Drive/Slack/Notion 매핑 적중 + 미인증.
- `인증 필요 (Google Drive connector 미연결)` — 자원 조회 도구·`authenticate` 모두 부재.
- `인증 필요 (connector 매핑 없음)` — 매핑·추론 모두 실패한 인증 게이트.
- `content-type <type>` / `빈 본문` / `미지원 이미지 포맷` / `image read 실패` / `빈 해석 결과` / `timeout` / `network error`.

## 8. URL 분기 sanity check 메시지

루트 URL이 모두 다음 사유로 본문 합류 실패한 경우만 호출 종료:

| 케이스 | 메시지 |
|---|---|
| `http`/`https` 외 scheme | `http(s) URL만 지원합니다. (입력: <scheme>)` |
| 모든 root URL fetch 실패 | `모든 URL fetch 실패. 첫 번째 사유: <status 또는 error>` |
| 모든 root 인증 게이트 + connector fallback 모두 미인증/실패 | `모든 URL이 로그인 필요로 보입니다. connector/MCP fallback도 인증되지 않았습니다.\n필요한 connector: <Atlassian / Figma / Google Drive / Slack / Notion / ...>` |
| 모든 root 지원 안 하는 content-type | `모든 URL이 지원 안 하는 content-type: <type list>` |
| 통합 본문 추출 0byte | `통합 본문이 비어 있습니다. URL 본문 확인 후 다시 시도하세요.` |

산출물 본문이나 `## 검증 피드백` 없이 단독 한 줄 + 입력 URL list로 출력.

## 11. connector별 anchor 추출 (deep link, 0.2.4)

`output-contract.md`의 상세 추적 full 출처 list URL deep link 형식과 `exclusion-rules.md` 4.1 입력 제외 섹션 위치 markdown link를 위해, anchor 지원 source는 deep link 형식으로 저장한다. 추출 실패·미지원 source = page-level URL fallback (link는 작동, 점프는 page 단위).

| Source | Anchor 형식 | 추출 방법 | 도입 |
|---|---|---|---|
| Google Sheets | `URL#gid=<id>&range=<cell>` | URL fragment 그대로 (이미 3.5) | 0.1.1 |
| Figma | `URL?node-id=<id>` | URL query 그대로 | 0.1.2 |
| Slack thread | thread 영구링크 | URL 자체 영구링크 | 0.1.2 |
| **Confluence** | `URL#<heading-id>` | Atlassian MCP body XHTML `<h1 id="..."`/`<h2 id="...">` 등 추출. 본문 합류 heading id 매핑. | **0.2.4 신규** |
| **Google Docs** | `URL#heading=h.<digest>` | `read_file_content` 응답에서 heading anchor 추출. heading text → digest 매핑. | **0.2.4 신규** |
| **Google Slides** | `URL#slide=id.<id>` | slide ID를 응답에서 추출. | **0.2.4 신규** |
| **Notion** | `URL#<block-id>` | Notion connector 응답에서 block id 추출 (best-effort). | **0.2.4 신규** |
| Jira | page-level (anchor 없음) | summary·description 단위는 anchor 없음. comment ref 시 `#comment-<id>` 가능. | 부분 |
| 기타 (WebFetch HTML) | heading id 있으면 추출 | `<h*> id="..."` parsing. 없으면 page-level. | best-effort |

### 11.1 Confluence heading id

- Atlassian MCP `getConfluencePage` body XHTML에 `<ac:structured-macro>` 무관 `<h1>`/`<h2>`/`<h3>`/... 태그의 `id` 속성 추출.
- heading id가 없으면 heading text를 slug 변환 (공백 → `-`, 한글 그대로). 변환 결과가 페이지 내 unique이면 사용, 그 외 page-level.
- 본문 합류 heading id 매핑은 main 판단. 입력 제외 섹션 항목 인용이 특정 heading 본문에서 발췌된 경우 그 heading id 사용.

### 11.2 Google Docs heading anchor

- `read_file_content` 응답에서 heading 항목의 anchor (`heading=h.<digest>`) 추출.
- heading text → digest 매핑이 응답에 없으면 page-level fallback.
- Docs URL 끝 `?tab=...&headingId=...` 형식이 응답에 등장하면 그대로 사용.

### 11.3 Google Slides slide id

- `read_file_content` 또는 `get_file_metadata` 응답에서 slide id (`id.<id>`) 추출.
- 슬라이드 단위 anchor: `URL#slide=id.<id>`.
- slide id 추출 실패 = page-level.

### 11.4 Notion block id

- Notion connector 응답에서 block id (32자 dash 구분 또는 raw 32자) 추출.
- Notion page URL 마지막 `-<32자>` 형태가 page id, 안쪽 block은 응답 본문의 block id 매칭.
- 추출 실패 = page-level (best-effort).

### 11.5 anchor 매칭 — 입력 제외 섹션 항목 단위

같은 source가 여러 항목 위치로 분산 인용될 때 각 항목별로 가장 가까운 anchor 사용. 매칭 우선순위:

1. 항목 인용 내용이 source 특정 heading 본문에서 발췌된 명확한 경우 → 해당 heading anchor.
2. 항목이 source 전체에 걸친 일반 정보 → page-level URL.
3. 매칭 불확실 → page-level URL.

main 판단. 강제 매핑 룰 없음.

### 11.6 visited set 영향

URL normalize는 fragment 제거 그대로 (6). visited set은 fragment 무관 같은 자원 1번만 fetch. 출처 list 표 행 URL은 fragment 포함 deep link로 저장 — visited와 별도 컬럼.
