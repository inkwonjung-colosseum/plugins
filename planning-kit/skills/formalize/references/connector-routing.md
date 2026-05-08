# connector-routing

formalize의 fetch 단계가 WebFetch 1차 시도 후 인증 게이트·실패 시 어떤 MCP/connector로 fallback할지 결정하는 lookup data + 케이스 표.

main은 fetch 단계 진입 직전 1회 이 파일을 `Read`로 적재해 메모리에 보관한다. 호출당 1회.

## 1. 인증 게이트 휴리스틱

WebFetch 응답이 200 OK인데도 다음 단서 중 하나가 보이면 **인증 게이트로 분류**한다 (= fallback 평가 진입).

- `<form ... action="...login..."` / `<form ... action="...signin..."` 패턴.
- `Atlassian` / `Confluence` / `Jira` 단어 + `Log In` 버튼 텍스트.
- Figma의 `<title>Log in &mdash; Figma</title>` / `Sign up to view`.
- Google `accounts.google.com` redirect 발자국 (`<meta http-equiv="refresh" ...accounts.google.com...>` 또는 본문 안 `accounts.google.com` 메타).
- Slack의 `Sign in to your workspace` 페이지.
- Notion의 `Log in to Notion` 본문.
- 일반 패턴: 외부 도구의 로그인 화면 표지(서비스명 + Sign in/Log in 단서)가 응답 본문 첫 화면에 단독으로 등장하면 인증 게이트로 본다.

휴리스틱에 해당하지 않으면 일반 본문으로 처리.

## 2. MCP/connector 카탈로그 평가

세션에서 다음을 평가해 메모리에 캐시:

- 사용 가능한 MCP tool 이름 list (예: `mcp__claude_ai_Atlassian__*`, `mcp__claude_ai_Figma__*`, `mcp__claude_ai_Google_Drive__*`, `mcp__claude_ai_Slack__*`, `mcp__claude_ai_Notion__*`).
- 각 connector의 인증 상태:
  - `authenticate` 도구만 노출되고 자원 조회 도구가 없음 → **미인증**.
  - 자원 조회 도구가 같이 있음 → **인증됨**.
- Atlassian만 예외적으로 `getAccessibleAtlassianResources` 1회 호출해 cloud id list를 캐시 (cloud id 인자가 필요한 도구에 사용).

main이 system prompt와 deferred tool list로부터 직접 인지한다 — 카탈로그 평가 자체는 외부 호출이 사실상 0회 (Atlassian의 `getAccessibleAtlassianResources` 1회만 예외).

## 3. 알려진 호스트 매핑표

대상 URL의 호스트가 다음 패턴과 일치하면 §5 fallback에서 명시된 connector tool을 우선 시도한다.

매칭 규칙:
- 호스트의 **eTLD+1** (또는 명시 패턴) 기준.
- `www.` prefix 무시.
- 한 URL이 여러 행에 걸치면 위에서 먼저 일치한 행을 따른다.

| # | 호스트 패턴 | 사용 MCP / connector | 대상 리소스 | 비고 |
|---|------------|----------------------|--------------|------|
| 1 | `*.atlassian.net` (path가 `/wiki/...`) | Atlassian MCP — `getConfluencePage` (page id 추출 가능 시) / `fetch` (URL 직접) | Confluence page | URL에 `pages/<id>` 또는 `viewpage.action?pageId=<id>`가 있으면 page id 우선 추출. 없으면 `fetch`. |
| 2 | `*.atlassian.net` (path가 `/browse/<KEY-NUM>` 또는 `/jira/...`) | Atlassian MCP — `getJiraIssue` (key 추출) / `fetch` | Jira issue | issue key를 path에서 추출. summary + description + recent comments를 본문 텍스트로 합쳐 합류. |
| 3 | `figma.com/file/...`, `figma.com/design/...`, `figma.com/board/...`, `figma.com/slides/...`, `figma.com/make/...` | Figma MCP — `get_design_context`(design) / `get_figjam`(board) / `get_metadata`(slides·make) | Figma 파일/노드 | URL에서 `fileKey`(또는 `branchKey`)·`nodeId` 추출. node-id의 `-`를 `:`로 변환. 응답 텍스트 + 첨부 스크린샷 캡션 합류. |
| 4 | `docs.google.com/document/...`, `docs.google.com/spreadsheets/...`, `docs.google.com/presentation/...`, `drive.google.com/...`, `sheets.google.com/...`, `slides.google.com/...` | Google Drive connector — `authenticate`(미인증 시) / 자원 조회 도구 | Google Docs / Sheets / Slides / Drive 파일 | 인증 시 본문 합류. 미인증 시 §5 skip. |
| 5 | `*.slack.com/archives/<channel>/p<ts>`, `*.slack.com/archives/<channel>` | Slack MCP — `slack_read_thread`(thread ts) / `slack_read_channel`(채널) | Slack 메시지/스레드 | thread 영구링크면 ts 추출 후 thread 통째로. 채널 단독이면 최근 메시지 N개(default 50)만. private 채널은 connector 권한 의존. |
| 6 | `*.slack.com` 그 외 path | Slack MCP — `slack_read_canvas`(canvas URL) / `slack_search_public_and_private`(쿼리=path 토큰) / `fetch` | Slack search/canvas 등 | canvas URL은 `slack_read_canvas` 우선. 그 외는 `fetch` 폴백. |
| 7 | `notion.so`, `*.notion.site` | Notion connector — `authenticate`(미인증 시) / 자원 조회 도구 | Notion page | path에서 page id(마지막 dash 뒤 32자) 추출. 미인증 시 §5 skip. |

매핑이 적중해도 §2 카탈로그 평가에서 해당 connector가 **사용 가능하지 않다**(인증·tool 미노출)면 connector 시도 자체가 일어나지 않고 1차 WebFetch 결과를 그대로 쓴다.

`searchConfluenceUsingCql`·`searchJiraIssuesUsingJql`은 매핑표에서 사용하지 않는다 — root URL 단일 자원 조회가 본 스킬의 목적이라 search는 범위가 다르다.

## 4. 런타임 MCP 카탈로그 추론 (매핑 외 호스트)

§3 매핑에 없는 호스트는 §2 카탈로그의 tool 이름에서 외부 서비스 단서를 본다:

- tool 이름에 `Linear`, `Intercom`, `Canva`, `Box`, `HubSpot`, `monday`, `Microsoft_365`, `Asana`, `Pencil`, `Figma`, `Atlassian`, `Slack`, `Google_Drive`, `Google_Calendar`, `Notion` 등 단서가 있고, 대상 URL 호스트가 그 단서의 기성 도메인(`linear.app`, `intercom.com`, `canva.com`, `box.com`, `hubspot.com`, `monday.com`, `microsoftonline.com`, `asana.com` 등)과 일치하거나 subdomain이면 해당 MCP의 일반 `fetch` 도구를 후보로.
- 추론 결과는 같은 호출 안에서 메모리 캐시 (호스트 → tool list).
- 추론 실패 = 후보 0.

## 5. fallback 평가 케이스 표

각 후보 connector tool 호출은 timeout 30초, 1회 시도. 응답이 비어 있거나 에러면 다음 후보로. 모두 실패하면 다음 케이스 표 분기.

매핑 lookup 호스트는 **원래 입력된 URL의 호스트**(혹은 추출된 자식 URL 자체의 호스트)를 사용한다. WebFetch가 redirect를 5회까지 따라가다가 `accounts.google.com` 같은 다른 호스트에 도착하더라도, 매핑·추론은 redirect 최종 호스트가 아니라 원래 의도된 자원의 호스트로 한다.

| 케이스 | 처리 |
|---|---|
| connector 호출 1건 이상 성공 | 응답 텍스트로 본문 합류. via=`<connector 이름>`. status=`200 (via <connector>)`. |
| connector 모두 실패 + 1차 WebFetch가 200 OK + 인증 게이트 아님 | 1차 본문 사용. via=`WebFetch`. |
| connector 모두 실패 + 1차가 인증 게이트 | skip. 사유=`인증 필요 (<connector list 시도, 미인증>)`. |
| connector 모두 실패 + 1차가 4xx/5xx/timeout | skip. 사유=1차 status·error 그대로. |
| 매핑·추론 결과 후보 0 + 1차가 인증 게이트 | skip. 사유=`인증 필요 (connector 매핑 없음)`. |
| `--no-fetch` ON | 1차·fallback 모두 봉쇄. URL은 visited에만 기록되고 본문 합류 0. |

connector 응답이 image content-type이면 image queue로 정상 라우팅 (예: Figma 스크린샷). status=`image/<subtype> <bytesize> (via Figma MCP)`.

## 6. connector 응답의 자식 링크 추출

connector 경유 본문도 일반 fetch 본문과 동일하게 자식 URL을 추출하고 visited queue에 push한다 (`is_followable`: http(s) + visited 미포함). 다음 round에서 fetch 시퀀스를 다시 탄다 → "Confluence root → Figma 자식 → 본문 합류" 시나리오가 자연스럽게 동작.

같은 자원의 다른 URL 형태(Atlassian short link `/x/...` ↔ 정식 page URL, Figma `figma.com/file/<key>` ↔ `figma.com/design/<key>`)는 normalize 후 host+path 비교라 별개 자원으로 본다 (dedup 강화는 비목표). connector 응답에서 canonical URL을 알 수 있으면 그 URL을 visited에 같이 등록해 dedup 시도까지만.

## 7. 출처 list `상태` 컬럼 표기

성공:
- `200 (via WebFetch)` — 일반 fetch 성공.
- `200 (via Atlassian MCP)` / `200 (via Figma MCP)` / `200 (via Google Drive connector)` / `200 (via Slack MCP)` / `200 (via Notion connector)` — connector 경유 성공.
- `image/<subtype> <bytesize> (via Figma MCP)` — connector가 image/* 응답을 줬을 때.

실패·skip:
- `인증 필요 (Atlassian MCP 미인증)` — 매핑 적중했지만 connector 미인증.
- `인증 필요 (connector 매핑 없음)` — 매핑·추론 모두 실패한 인증 게이트.
- `content-type <type>` / `빈 본문` / `미지원 이미지 포맷` / `image read 실패` / `빈 해석 결과` / `timeout` / `network error`.

## 8. URL 분기 sanity check 메시지

루트 URL이 모두 다음 사유로 본문 합류 실패한 경우만 호출 종료. 일부 root만 실패면 §출처 list에 사유만 기록하고 진행.

| 케이스 | 사유 메시지 |
|---|---|
| `http`/`https` 외 scheme (인자에 단 1개라도) | `http(s) URL만 지원합니다. (입력: <scheme>)` |
| 모든 root URL fetch 실패 | `모든 URL fetch 실패. 첫 번째 사유: <status 또는 error>` |
| 모든 root 인증 게이트 + connector fallback 모두 미인증/실패 | `모든 URL이 로그인 필요로 보입니다. connector/MCP fallback도 인증되지 않았습니다.\n필요한 connector: <Atlassian / Figma / Google Drive / Slack / Notion / ...>` (필요한 connector list는 시도된 매핑 결과로 산출) |
| 모든 root URL이 지원 안 하는 content-type | `모든 URL이 지원 안 하는 content-type: <type list>` |
| 통합 본문 추출 결과 0byte | `통합 본문이 비어 있습니다. URL 본문 확인 후 다시 시도하세요.` |

sanity check 메시지는 `## 리뷰 결과` 블록 없이 단독 한 줄 + 입력 URL list를 함께 출력한다.
