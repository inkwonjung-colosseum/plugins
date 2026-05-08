# planning-kit PRD 0.1.2

> 0.1.1 기반 incremental PRD. 본 문서에 명시된 항목만 변경하고, 그 외 모든 명세(분기 우선순위·재귀 fetch·이미지 multimodal·SSOT 키워드 노출·출력 포맷·marker·템플릿·저장 정책 등)는 [`prd-0.1.1.md`](./prd-0.1.1.md), [`prd-0.1.0.md`](./prd-0.1.0.md)를 그대로 따른다.

## 1. 변경 요약

세 가지 변경:

1. **인증 필요 호스트 fallback 추가** — 일반 `WebFetch`가 실패(인증 게이트·401/403)한 URL을 곧바로 skip하지 않고, 해당 URL의 호스트가 알려진 외부 서비스(Atlassian Confluence/Jira·Figma·Google Workspace·Slack 등)면 **connector/MCP 경유 접근**을 한 번 더 시도한다. 0.1.1까지는 인증 게이트 = 즉시 skip이라, Confluence root URL을 주면 같은 도메인 자식 Confluence 링크는 잘 따라가지만, 자식이 Figma·Google Drive·Slack 링크일 경우 인증 게이트로 분류되어 본문 합류에서 빠지는 문제가 있었다.
2. **고정 호스트 매핑표 + 런타임 MCP 카탈로그 추론 병행** — 자주 등장하는 호스트는 PRD에 매핑을 박아 동작이 예측 가능하게 하고(§4), 매핑되지 않은 호스트는 현재 세션에서 사용 가능한 MCP/connector tool 목록을 보고 라우팅 가능 여부를 추론한다(§5). 두 경로 모두 실패하면 일반 fetch 결과로 폴백.
3. **출처 list·헤더에 fetch 경로 표기** — `## 출처` 표 `상태` 컬럼에 `via WebFetch` / `via Atlassian MCP` / `via Figma MCP` / `via Google Drive connector` / `via Slack MCP` 등 경로를 같이 적는다. 헤더 `입력 처리` 줄에는 `(MCP 경유 N개)` 카운트를 누적해 사용자가 어떤 인증 자원이 동원됐는지 한눈에 본다.

기존 입력 분기·재귀 동작·이미지 multimodal·SSOT 매칭 로직은 그대로 유지한다. 이번 변경은 **fetch 단계(§3 / 0.1.1 §4.3·4.5·4.7) 내부 동작 보강**에 한정되며, 변환·리뷰·출력 본문 형식은 손대지 않는다.

## 2. 동기

- 사용자가 인자로 주는 root URL(예: 회사 Confluence 페이지)에는 사내 도구가 자식 링크로 깔리는 경우가 많다. Confluence ↔ Figma ↔ Google Drive ↔ Slack 메시지 영구링크가 한 페이지에서 같이 등장하는 게 일반적이다.
- 0.1.1의 일반 `WebFetch`는 도메인 무관 단일 GET이라, **로그인 게이트가 걸린 외부 도구는 모두 인증 필요로 분류돼 본문 합류 0**이 된다. 같은 도메인 Confluence 자식은 root와 같은 응답 정책 안에서 풀려 잘 따라간 것처럼 보였지만, 외부 도구 링크는 누락된 채로 변환·리뷰가 진행됐다.
- Claude 환경에는 이미 Atlassian·Figma·Google Drive·Slack·Notion·Linear 등 MCP/connector tool이 인증된 상태로 붙어 있는 경우가 많다. 인증 자원이 있는데도 못 쓰고 skip하는 건 정보 손실이다.
- 한편 connector를 무조건 우선하면, 인증이 안 붙어 있는 환경에서는 매 호출마다 인증 안내가 떠 비용이 늘고, 공개 페이지에는 불필요하다. 따라서 **일반 fetch → 실패 시 connector fallback** 순서가 단순함과 정확성을 동시에 만족한다.

## 3. 비목표

- 인증 자체를 본 스킬 안에서 자동으로 완료시키지 않는다. MCP/connector가 미인증이면 그 URL은 본문 합류 실패로 처리한다 (§5.3).
- 호스트 매핑은 본 PRD에서 다루는 7개 카테고리(§4.1)만 1차로 넣는다. Notion·Linear·Intercom·Canva·Box·HubSpot·monday.com·Microsoft 365·Asana 등은 런타임 카탈로그 경로(§5)로만 잡되, 매핑표 자체는 시간이 흐르며 PR로 추가될 수 있다.
- connector 응답이 변환된 markdown(예: Atlassian MCP의 page body)이 아니라 구조화 JSON일 때, 그 JSON을 사람이 읽기 좋은 markdown으로 완벽히 정렬하는 것은 비목표다. 변환 본문은 어차피 main이 재구성하므로, **본문 합류용 텍스트화**(헤딩·표·리스트·본문 텍스트만 살아남는 수준)면 충분하다.
- root URL의 `is_authentication_gate` 판정 휴리스틱은 0.1.1 §3.7과 동일 — 본 PRD는 그 판정 후 처리(§3.x fallback)만 추가한다.
- connector/MCP 응답 캐시·세션 간 재사용은 하지 않는다. 같은 호출 안의 visited set만 공유한다 (0.1.1 §3.8 그대로).
- 인증 자원 사용에 대한 동의 prompt를 띄우지 않는다. 사용자가 `formalize`를 호출한 시점에 이미 환경에 붙어 있는 MCP/connector를 쓰는 것에 동의한 것으로 본다. 다만 어떤 connector가 사용됐는지 출처 list에 명시(§6)해 사후 가시성은 확보한다.
- `--no-fetch` 옵션이 켜지면 connector fallback도 함께 disable된다 (모든 외부 호출이 봉쇄). MCP 사용 자체를 별도 끌 옵션은 두지 않는다.

## 4. 알려진 호스트 매핑표

### 4.1 1차 매핑

다음 호스트들이 fetch 대상 URL의 호스트(또는 호스트의 등록 가능 도메인 suffix)와 일치하면, **connector fallback 단계에서 명시된 MCP/connector를 우선 시도**한다.

| # | 호스트 패턴 | 사용 MCP / connector | 대상 리소스 | 비고 |
|---|------------|----------------------|--------------|------|
| 1 | `*.atlassian.net` (path가 `/wiki/...`) | Atlassian MCP — `getConfluencePage` (page id 추출 가능 시) / `fetch` (URL 직접) | Confluence page | URL에 `pages/<id>` 또는 `viewpage.action?pageId=<id>`가 있으면 page id 우선 추출. 없으면 `fetch`. |
| 2 | `*.atlassian.net` (path가 `/browse/<KEY-NUM>` 또는 `/jira/...`) | Atlassian MCP — `getJiraIssue` (key 추출) / `fetch` | Jira issue | issue key를 path에서 추출. summary + description + recent comments를 본문 텍스트로 합쳐 합류. |
| 3 | `figma.com/file/...`, `figma.com/design/...`, `figma.com/board/...`, `figma.com/slides/...`, `figma.com/make/...` | Figma MCP — `get_design_context`(`design`) / `get_figjam`(`board`) / `get_metadata`(slides·make) | Figma 파일/노드 | URL에서 `fileKey`(또는 `branchKey`)·`nodeId` 추출 후 호출. node-id의 `-`는 `:`로 변환. 응답 텍스트 + 첨부 스크린샷 캡션을 본문으로 합류. |
| 4 | `docs.google.com/document/...`, `docs.google.com/spreadsheets/...`, `docs.google.com/presentation/...`, `drive.google.com/...`, `sheets.google.com/...`, `slides.google.com/...` | Google Drive connector — `authenticate`(미인증 시) / 자원 조회 도구 | Google Docs / Sheets / Slides / Drive 파일 | connector가 인증돼 있으면 해당 파일 본문 텍스트로 합류. 미인증이면 §5.3. |
| 5 | `*.slack.com/archives/<channel>/p<ts>`, `*.slack.com/archives/<channel>` | Slack MCP — `slack_read_thread`(thread ts) / `slack_read_channel`(채널) | Slack 메시지/스레드 | thread 영구링크면 message ts 추출 후 thread 통째로. 채널 단독이면 최근 메시지 N개(default 50)만. private 채널은 connector 권한 의존. |
| 6 | `*.slack.com` 그 외 path | Slack MCP — `slack_search_public_and_private`(쿼리에 path 토큰) / `fetch` | Slack search/canvas 등 | canvas URL은 `slack_read_canvas`로 분기. 그 외는 `fetch`로 폴백. |
| 7 | `notion.so`, `*.notion.site` | Notion connector — `authenticate`(미인증 시) | Notion page | path에서 page id(마지막 dash 뒤 32자) 추출. 미인증이면 §5.3. |

매핑은 호스트의 **eTLD+1**(또는 `*.atlassian.net`처럼 명시 패턴) 기준으로 한다. `www.` prefix는 무시한다. 매칭 우선순위는 위 #1부터 차례. 한 URL이 여러 카테고리에 걸치는 경우(예: `figma.com/board/...`)는 위에서 먼저 일치한 행을 따른다.

### 4.2 매핑 외 호스트

표에 일치하지 않는 호스트는 §5.2 런타임 MCP 카탈로그 추론으로 fallback. 추론도 안 되면 일반 `WebFetch`만 사용 (= 0.1.1 동작과 동일).

### 4.3 호스트 매핑 비고

- 매핑표는 **이 PRD의 single source of truth**다. 변경은 본 문서에 PR. 코드/스킬 본문은 본 표를 그대로 인용·구현한다.
- 호스트 매핑이 적중해도, 그 connector/MCP가 현재 세션에서 사용 가능(§5.1)하지 않으면 fallback이 일어나지 않고 일반 fetch 결과를 그대로 쓴다.
- Atlassian의 `searchConfluenceUsingCql`·`searchJiraIssuesUsingJql`은 본 매핑표에서 사용하지 않는다 — root URL을 받아 그 URL에 해당하는 단일 자원을 가져오는 게 본 스킬의 목적이라 search는 범위가 다르다.

## 5. fetch 동작 보강

### 5.1 사용 가능 MCP/connector 카탈로그

fetch 단계 진입 직전 1회, 다음을 평가해 메모리에 캐시한다 (호출당 1회):

- 현재 세션에서 사용 가능한 MCP tool 이름 목록 (예: `mcp__claude_ai_Atlassian__*`, `mcp__claude_ai_Figma__*`, `mcp__claude_ai_Google_Drive__*`, `mcp__claude_ai_Slack__*`, `mcp__claude_ai_Notion__*` 등).
- 각 connector의 인증 상태 — `authenticate` 도구가 별도로 노출돼 있고, 실제 자원 조회 도구가 같이 있으면 "인증됨"으로 간주. `authenticate`만 노출되고 자원 조회 도구가 없으면 "미인증" 상태로 본다.
- Atlassian의 경우 `getAccessibleAtlassianResources` 호출이 가능하면 cloud id list를 한 번 가져와 각 매핑 호출에 cloud id가 필요한 도구의 인자로 사용한다.

이 카탈로그는 main 자신이 시스템 프롬프트와 deferred tool list로부터 직접 인지한다. 별도의 외부 호출은 필요 없다 (Atlassian의 `getAccessibleAtlassianResources`만 예외적으로 1회 호출).

### 5.2 런타임 MCP 카탈로그 추론

§4.1 매핑에 없는 호스트라도, 사용 가능한 MCP tool 이름에서 호스트 패턴을 추론한다:

- tool 이름에 `Linear`, `Intercom`, `Canva`, `Box`, `HubSpot`, `monday`, `Microsoft_365`, `Asana`, `Pencil`, `Figma`, `Atlassian`, `Slack`, `Google_Drive`, `Google_Calendar`, `Notion` 등 단서가 있고, fetch 대상 URL의 호스트가 그 단서의 기성 도메인(예: `linear.app`, `intercom.com`, `canva.com`, `box.com`, `hubspot.com`, `monday.com`, `microsoftonline.com`, `asana.com`)과 일치하거나 subdomain이면 해당 MCP의 일반 `fetch` 도구를 우선 시도.
- 추론 결과는 같은 호출 안에서 메모리에 캐시 (호스트 → tool list).
- 추론 실패는 무조건 일반 `WebFetch`로 폴백.

### 5.3 fetch 시퀀스 (URL 1개 처리 단위)

각 URL에 대해 다음 순서로 처리한다 (0.1.1 §3.2를 대체):

```
1. WebFetch로 1회 GET (timeout 30초, redirect ≤5).
2. 응답 분류:
   2a. 200 OK + content-type text/html|markdown|plain|xhtml → 본문 추출(§0.1.1 3.3) → 정상 합류. via=WebFetch.
   2b. 200 OK + image/* → image queue로 라우팅. via=WebFetch.
   2c. 200 OK + 지원 안 하는 content-type → §5.4 fallback 평가.
   2d. 401 / 403 / 인증 게이트 휴리스틱 (200 OK인데 본문이 로그인 폼) → §5.4 fallback 평가.
   2e. 4xx (위 외) / 5xx / timeout / network error → §5.4 fallback 평가.
3. fallback 결과로 본문 합류 또는 skip 결정.
```

휴리스틱: 응답 본문이 200 OK인데도 다음 패턴 중 하나라도 나오면 **인증 게이트로 간주**한다.

- `<form ... action="...login..."` / `<form ... action="...signin..."` 패턴.
- `Atlassian` / `Confluence` / `Jira` 단어 + `Log In` 버튼 텍스트.
- Figma의 `<title>Log in &mdash; Figma</title>` / `Sign up to view`.
- Google `accounts.google.com` redirect 발자국 (`<meta http-equiv="refresh" ...accounts.google.com...>` 또는 `accounts.google.com` 본문 메타).
- Slack의 `Sign in to your workspace` 페이지.
- Notion의 `Log in to Notion` 본문.

휴리스틱에 해당하지 않으면 일반 본문으로 처리.

### 5.4 fallback 평가

URL의 호스트로 §4.1 매핑표 lookup → 일치하면 매핑된 connector tool들을 순서대로 시도. 매핑 미적중 시 §5.2 런타임 추론으로 connector tool 후보 산출. 후보가 없으면 fallback 종료 (= skip + 사유 기록).

각 connector tool 호출은 timeout 30초, 1회 시도. 응답이 비어 있거나 에러면 다음 후보로 넘어간다. 모두 실패하면 다음 분기로:

| 케이스 | 처리 |
|---|---|
| connector 호출 1건 이상 성공 | 그 응답 텍스트로 본문 합류. via=`<connector 이름>`. status 컬럼은 `200 (via <connector>)`. |
| connector 모두 실패하지만 step 2의 `WebFetch` 응답이 200이고 인증 게이트가 아니었음 | step 2 본문 사용. via=WebFetch. |
| connector 모두 실패 + step 2 인증 게이트 | skip. 사유: `인증 필요 (<connector list 시도, 미인증>)`. |
| connector 모두 실패 + step 2 4xx/5xx/timeout | skip. 사유: step 2 status·error 그대로. |
| 매핑·추론 결과 connector 후보 0개 + step 2 인증 게이트 | skip. 사유: `인증 필요 (connector 매핑 없음)`. |
| `--no-fetch` 옵션 ON | step 1·2·3 모두 봉쇄. URL은 visited set에만 기록되고 본문 합류 0. |

connector 응답이 image content-type이면 0.1.1 §4 image queue로 정상 라우팅 (예: Figma의 스크린샷). status 컬럼은 `image/<subtype> <bytesize> (via Figma MCP)`.

### 5.5 connector 응답의 자식 링크 추출

connector를 통해 가져온 본문도 0.1.1 §3.6 `is_followable` 규칙에 따라 자식 URL을 추출하고 visited queue에 push한다. 즉:

- Atlassian Confluence page body 안에 Figma URL이 있으면 그 Figma URL이 자식 후보가 되고, 다음 round에서 §5.3 시퀀스를 다시 탄다 (Figma MCP 인증돼 있으면 본문 합류, 미인증이면 skip).
- Slack thread 안의 영구링크도 자식으로 잡힌다.
- self-link(같은 connector 자원의 alias URL)는 visited normalize로 제거.

이로써 "Confluence root → Figma 자식 링크 → 본문 합류"라는 시나리오가 자연스럽게 동작한다 (현재 0.1.1에서 빠지는 케이스).

### 5.6 캐싱·중복

같은 normalize URL은 한 호출 안에서 한 번만 시도한다 (visited set). via 정보도 visited 기록의 일부.

같은 자원이 여러 URL 형태(Atlassian의 short link `/x/...` ↔ 정식 page URL, Figma의 `figma.com/file/<key>` ↔ `figma.com/design/<key>` 등)로 들어오는 경우는 normalize 후 host+path만 비교하므로 별개 자원으로 본다 — 이 경계 케이스의 dedup은 0.1.2 비목표. (connector 응답에서 canonical URL을 알 수 있으면 그 URL을 visited에 같이 등록해 dedup을 강화하는 정도까지만 시도한다.)

### 5.7 sanity check 영향

0.1.1 §3.4의 5종 sanity check 메시지 중 `모든 URL이 인증 게이트` 케이스는 다음으로 교체된다:

```
모든 URL이 로그인 필요로 보입니다. connector/MCP fallback도 인증되지 않았습니다.
필요한 connector: <Atlassian / Figma / Google Drive / Slack / ...>
```

해당 connector의 인증 흐름을 별도로 안내하지는 않는다 (사용자가 본인의 환경에서 connector를 켜야 함). 한 줄에 어떤 자원이 필요한지만 적어 사용자가 어디부터 보면 되는지 알 수 있게 한다.

## 6. 출처 list·헤더 출력 보강

### 6.1 출처 list `상태` 컬럼

0.1.1 §7.3 출처 표의 `상태` 컬럼은 다음 형태를 추가로 허용한다:

- `200 (via WebFetch)` — 일반 fetch 성공.
- `200 (via Atlassian MCP)` / `200 (via Figma MCP)` / `200 (via Google Drive connector)` / `200 (via Slack MCP)` / `200 (via Notion connector)` 등 — connector 경유 성공.
- `image/png 1.2MB (via Figma MCP)` — connector가 image/* 응답을 줬을 때.
- `인증 필요 (Atlassian MCP 미인증)` — 매핑 적중했지만 connector 미인증.
- `인증 필요 (connector 매핑 없음)` — 매핑·추론 모두 실패한 인증 게이트.

`via WebFetch`는 0.1.1까지의 기본 동작과 동일하며, 0.1.2부터는 명시 표기를 권장한다 (생략 시에도 WebFetch로 해석).

### 6.2 헤더 `입력 처리` 줄

0.1.1 §7.1의 헤더 줄 끝에 connector 카운트가 있을 때만 `(MCP 경유 K개)`를 추가한다.

```
- 입력 처리: URL 1개 + 재귀 fetch 5개 (MCP 경유 2개)
- 입력 처리: 직접 입력 + 추출 URL 3개 (재귀 fetch 7개) (MCP 경유 4개) + 이미지 1개
```

`MCP 경유 K개`는 connector를 통해 본문 합류된 URL 수의 합계 (실패는 카운트 안 함). K=0이면 괄호 자체를 생략한다 (= 0.1.1 헤더 그대로).

### 6.3 리뷰 결과 영향 없음

connector 경유로 합류된 본문이라 해서 SSOT 매칭·자체 품질 점검 기준이 달라지지 않는다 — 여전히 본문 텍스트로만 평가. 다만 자체 품질 발견에서 "본문 정보 부족" 류 코멘트는, 인증 미연결로 skip된 자식 URL이 있다면 그 사실을 발견 사항의 영향 줄에 한 줄로 부연하기를 권장한다 (`영향: Figma 자식 1개가 미인증으로 합류 누락. 합류 후 재검토 필요할 수 있음.`).

## 7. CLI 인자·옵션

본 PRD는 새 옵션을 추가하지 않는다. 0.1.1의 `--ssot-include`·`--no-review`·`--no-fetch`·`--no-image`만 그대로 사용한다. `--no-fetch`는 §5.3 step 1·2·3 전체를 봉쇄하므로 connector fallback도 함께 disable된다.

connector를 끄는 별도 옵션(예: `--no-mcp`)은 두지 않는다 — connector 인증이 안 붙은 환경에서는 §5.1 카탈로그 평가 결과 후보가 0이라 자연스럽게 polyfill처럼 비활성된다. 환경에 인증된 connector가 붙어 있는데도 사용을 막고 싶은 경우는 0.1.2 비목표 (필요해지면 0.1.3에서 추가).

## 8. 호환성

- 0.1.1 → 0.1.2는 **순수 추가**다. 인자·옵션·파일 구조·출력 본문 형식은 그대로다.
- 0.1.1까지 인증 게이트로 skip되던 URL들이 0.1.2에서는 connector를 통해 본문 합류될 수 있다 → 변환 본문이 더 풍부해질 수 있고, SSOT 충돌이 더 잡힐 수 있다.
- connector가 전혀 인증되지 않은 환경에서는 동작이 0.1.1과 거의 동일 — 다만 출처 list `상태` 컬럼에 `via WebFetch` 표기가 추가된다.
- 출력 markdown 구조는 §6.1·6.2 외에는 동일.

## 9. 검증 시나리오

다음 시나리오를 PRD 검수 시점에 main이 직접 트레이스해 본다 (실제 호출은 사용자 환경에서 따로 검증).

1. **Confluence root → Figma 자식**: `/planning-kit:formalize https://acme.atlassian.net/wiki/spaces/PROD/pages/12345/Order-Cancel-Spec`. 본문에 Figma 디자인 링크 존재. 0.1.1: Figma 링크가 인증 게이트로 분류되어 skip. 0.1.2: Figma MCP 인증 시 본문 합류, 출처 표에 `via Figma MCP`. Figma MCP 미인증 시 `인증 필요 (Figma MCP 미인증)`로 정확히 표기.
2. **Confluence root → Google Doc 자식**: 위와 동형. Google Drive connector 인증 시 합류, 미인증 시 skip + 사유.
3. **Slack 영구링크 직접 인자**: `/planning-kit:formalize https://acme.slack.com/archives/C0123/p1700000000000000`. Slack MCP 인증 시 thread 본문 합류 (`via Slack MCP`). 미인증 시 §5.7 sanity check 메시지 + `필요한 connector: Slack`.
4. **공개 페이지 자식**: 매핑·추론 모두 미적중. 일반 WebFetch 그대로 동작 → 0.1.1과 동일.
5. **`--no-fetch`**: 인자 URL 자체 fetch도 막힘. connector 호출 0건. sanity check `통합 본문이 비어 있습니다` 또는 텍스트 분기일 경우 원본 본문만으로 변환.
6. **인증된 Confluence root + 미인증 Figma 자식 + 인증된 Slack 자식**: 출처 표에 3가지 status가 동시에 등장. `MCP 경유 2개` 카운트.
7. **redirect 후 인증 게이트**: WebFetch가 5회 redirect 후 로그인 페이지에 도착. 인증 게이트 휴리스틱이 잡아 fallback 시도. connector 매핑은 최종 redirect 도메인 기준이 아니라 **원래 입력된 URL의 호스트** 기준으로 한다 (사용자가 의도한 자원에 가까움).

## 10. 참고 파일

- `skills/formalize/SKILL.md` — 본 PRD 반영 시 §3.2(fetch)·§3.4(URL sanity check)·§3.7(fetch 실패·skip 케이스)·§7.1(헤더)·§7.3(출처 list) 섹션 보강.
- `skills/formalize/references/review-rules.md` — 변경 없음 (SSOT 매칭·자체 품질 기준 그대로).
- `skills/formalize/templates/기능설계서.md`, `templates/정책서.md` — 변경 없음.
