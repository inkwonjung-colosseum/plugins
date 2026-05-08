# planning-kit PRD 0.1.1

> 0.1.0 기반 incremental PRD. 본 문서에 명시된 항목만 변경하고, 그 외 모든 명세(출력 포맷·리뷰 축·marker·템플릿·저장 정책 등)는 [`prd-0.1.0.md`](./prd-0.1.0.md)를 그대로 따른다.

## 1. 변경 요약

다섯 가지 변경:

1. **URL 입력 분기 추가 (다중 URL 허용)** — `formalize` 입력 dispatch에 URL(링크) 분기를 추가한다. **인자로 1개 이상의 URL을 줄 수 있다**. 모든 URL을 fetch → 본문 추출 후 통합한다.
2. **모든 분기에서 본문 URL 추출** — 텍스트·파일·디렉터리 분기에서도 입력 본문에 포함된 URL을 자동 추출해 fetch에 투입한다. URL 추출은 모든 분기 공통 전처리 단계가 된다.
3. **재귀 fetch (필수, cap 없음)** — 인자 URL이든 본문에서 추출된 URL이든, 추출 본문 안에 또 외부 링크가 있으면 그 링크들도 재귀적으로 fetch해 본문에 합류시킨다. depth·pages·body 크기 cap을 두지 않는다 — 품질·검증 우선. cycle 방지(visited set)만 유지.
4. **이미지 multimodal 처리** — 입력 파일·디렉터리·fetch 결과·markdown image 참조에 이미지가 있으면 Claude multimodal 능력으로 읽어 텍스트(설명·차트 데이터·도면 라벨 등)로 변환해 본문에 합류한다. 다이어그램·스크린샷·스케치 기반 기획도 변환 입력이 될 수 있다.
5. **SSOT 키워드 노출** — 리뷰 SSOT 단계에서 grep에 사용한 키워드 list를 결과 화면에 출력한다. 사용자가 grep 범위와 매칭 근거를 검증할 수 있다.

기존 입력 분기(텍스트 / 파일 / 디렉터리)는 그대로 유지한다. URL은 4번째 분기로 추가되되, 본문 URL 추출과 이미지 처리는 4분기 모두에 공통으로 적용된다.

## 2. 동기

- 사용자가 기획을 Notion·Confluence·Google Docs·블로그·이슈 트래커·공개 위키 같은 외부 페이지에 두고 작업하는 경우, 현재는 본문을 수동으로 복사해 텍스트 인자로 다시 넣어야 한다.
- 링크 한 줄로 같은 결과를 얻을 수 있으면 호출 비용이 줄고, 입력 누락/편집 사고도 줄어든다.
- 산출물은 여전히 화면 output only이므로 0.1.0의 단순성을 깨지 않는다 (fetch만 추가, 저장은 여전히 없음).

## 3. 비목표

- 인증 필요한 페이지(로그인 게이트·사내 SSO·private Notion·private Confluence 등) 자동 인증 처리는 하지 않는다. fetch 실패한 URL은 본문 합류에서 제외하고 출처 list에 실패 사유와 함께 기록한다.
- HTML→Markdown 완벽 변환은 목표 아님. 본문 텍스트 추출 수준이면 충분하다 (변환 본문은 어차피 main이 재구성).
- JS 렌더링 페이지(SPA) 별도 headless 브라우저 처리는 하지 않는다. fetch 가능한 정적 본문만 대상.
- URL 결과 캐시·세션 간 재사용은 하지 않는다. 매 호출마다 새로 fetch (단, 같은 호출 내에서는 §4.7 visited set으로 중복 fetch는 방지).
- 텍스트·파일·디렉터리 분기에서 URL 추출 시, **이미지 안 글자에서의 URL 추출**(이미지에 적힌 URL 글자 OCR)은 하지 않는다. plain text·markdown·HTML attribute(`href`/`src`)에서 보이는 URL만 대상.
- 별도 OCR 엔진(Tesseract 등)·외부 vision 서비스는 사용하지 않는다. 이미지 해석은 **Claude의 내장 multimodal 능력만** 사용 (§4.8).
- 동영상·음성·PDF 본문 추출은 하지 않는다. PDF는 content-type skip, 동영상·음성은 파일 분기에서도 skip한다.
- 이미지 변환 결과를 별도 파일로 저장하지 않는다. multimodal 해석으로 만든 텍스트는 통합 본문에 합류만 한다 (0.1.0 저장 없음 정책 유지).

## 4. 입력 dispatch 변경

### 4.1 분기 우선순위

기존 (0.1.0):

```
1. 디렉터리 경로  → 디렉터리 분기
2. 파일 경로      → 파일 분기
3. 그 외          → 텍스트 분기
```

신규 (0.1.1):

```
1. URL 패턴 (1개 이상)  → URL 분기      (NEW)
2. 디렉터리 경로        → 디렉터리 분기 (지원 이미지 파일도 같이 수집 — §4.8)
3. 파일 경로            → 파일 분기 (이미지 확장자면 §4.8 image queue로 단독 시드)
4. 그 외                → 텍스트 분기

추가 공통 단계 (모든 분기 공통, 분기 결정 직후 실행):
5. 본문 URL·이미지 참조 추출 → §4.7 fetch queue + §4.8 image queue에 시드
6. 재귀 fetch + 이미지 multimodal 처리 → 통합 본문 합류
```

### 4.2 URL 판별 규칙

#### 4.2.1 인자 단계 (URL 분기 진입)

다음 조건을 **모두** 만족하면 URL 분기로 처리한다:

- 입력 인자를 공백·줄바꿈으로 토큰화한 결과, **모든 비어 있지 않은 토큰**이 URL 패턴이다.
- 각 토큰이 `^https?://`로 시작한다 (`http://`, `https://`만 허용).
- 각 토큰의 호스트부가 비어 있지 않다.

토큰이 1개면 단일 URL 분기, 2개 이상이면 다중 URL 분기. 다중 URL은 모두 `depth=0` root로 visited queue에 시드된다 (§4.7).

`file://`, `ftp://`, `s3://`, `mailto:`, scheme 없는 입력(`example.com/...`)은 URL 분기로 보지 않는다 — 기존 텍스트/파일/디렉터리 분기로 흐른다.

URL 토큰과 비-URL 토큰이 섞여 있으면 (예: `https://x.com 추가 메모`) URL 분기로 보지 않고 **텍스트 분기**로 흐른다. 그 텍스트 본문에서 §4.2.2 추출 규칙이 동작해 URL은 fetch에 시드된다.

#### 4.2.2 본문 URL·이미지 참조 추출 (모든 분기 공통)

분기가 결정된 직후, 입력 본문(텍스트·파일·디렉터리에서 읽은 모든 텍스트의 합)에서 URL과 이미지 참조를 추출한다. URL 분기에서는 인자 URL의 fetch 본문이 추출 대상에 포함되며, 그 본문 추출은 §4.7 재귀 단계에서 처리한다 (본 단계는 인자가 아닌 입력 본문 한정).

**URL 추출 패턴:**

- **markdown link**: `[text](https?://...)` → URL 부분만 추출.
- **markdown autolink**: `<https?://...>`.
- **HTML href/src**: `href="https?://..."` / `src="https?://..."` (속성 따옴표 종류 무관).
- **plain URL**: 위 형식이 아닌 본문에서 `https?://[^\s<>"\)]+` 매칭. trailing 구두점(`,`, `.`, `;`, `:`, `)`, `]`)은 제거.

**이미지 참조 추출 패턴:**

- **markdown image**: `![alt](path-or-url)` → path/URL 추출. URL이면 §4.7 fetch queue에 image content-type 시드. 상대 경로면 입력 파일·디렉터리 기준으로 resolve해서 §4.8 image queue에 시드.
- **HTML img**: `<img src="path-or-url" ...>` → 동일 처리.

추출된 URL은 §4.7 visited queue에 `depth=0` root로 시드된다 (인자 URL과 동등 취급). 추출된 이미지 참조는 §4.8 image queue에 시드된다. 동일 URL/경로가 중복 발견되면 visited set으로 중복 제거된다.

self-anchor (`#section`만 있는 fragment)·`mailto:`/`tel:`/`javascript:`·blob scheme은 추출 대상에서 제외한다. `data:image/...;base64,...` URI는 inline 이미지로 §4.8 image queue에 시드 (디코딩 후 multimodal 입력).

### 4.3 fetch 동작

- WebFetch 툴(또는 환경에서 사용 가능한 동등 fetch 수단)로 1회 GET.
- timeout: 30초.
- redirect: 따라간다 (최대 5회).
- User-Agent: 기본값 그대로 (별도 위장 안 함).
- 응답 content-type:
  - `text/html`, `text/markdown`, `text/plain`, `application/xhtml+xml` → 본문 추출 진행.
  - 그 외(`image/*`, `application/pdf`, `application/octet-stream` 등) → §4.5 sanity check로 안내 후 종료.

### 4.4 본문 추출

HTML이면 다음 우선순위로 본문 텍스트를 추출한다 (main이 직접 처리):

1. `<main>` / `<article>` / `role="main"` 영역.
2. (1)이 없으면 `<body>` 전체에서 `<nav>`, `<aside>`, `<header>`, `<footer>`, `<script>`, `<style>` 제거 후 텍스트.
3. 표는 markdown 표로, 헤딩은 `#` 레벨 유지, 리스트는 `-` 유지. 그 외는 plain text.

Markdown/plain text면 그대로 사용.

추출 결과는 메모리에만 둔다 (저장 없음, 0.1.0 정책 그대로).

### 4.5 URL 분기 sanity check

루트 URL이 **모두** 다음 사유로 본문 합류 실패한 경우만 호출이 종료된다. 일부 root만 실패하면 종료하지 않고 §5.4 출처 list에 사유만 기록한다.

| 케이스 | 사유 메시지 |
|---|---|
| `http`/`https` 외 scheme (인자에 단 1개라도) | `http(s) URL만 지원합니다. (입력: <scheme>)` |
| 모든 root URL fetch 실패 | `모든 URL fetch 실패. 첫 번째 사유: <status 또는 error>` |
| 모든 root URL이 인증 게이트 | `모든 URL이 로그인 필요로 보입니다. 본문을 직접 텍스트로 주세요.` |
| 모든 root URL이 지원 안 하는 content-type | `모든 URL이 지원 안 하는 content-type: <type list>` |
| 통합 본문 추출 결과 0byte | `통합 본문이 비어 있습니다. URL 본문 확인 후 다시 시도하세요.` |

sanity check 메시지는 `## 리뷰 결과` 블록 없이 단독 한 줄 + 입력 URL list를 함께 출력한다.

**텍스트·파일·디렉터리 분기**의 sanity check는 0.1.0과 동일 (literal 빈 입력만 거름). 본문에서 URL이 추출되었지만 모든 fetch가 실패해도 텍스트 본문 자체로 변환을 진행한다 (URL fetch는 부가 정보일 뿐, 주 입력은 텍스트).

### 4.6 변환·리뷰 흐름

분기와 §4.2.2 본문 URL 추출이 끝나면, §4.7 재귀 fetch를 마친 뒤 **통합 본문**(원본 입력 + fetch한 모든 페이지 본문)이 0.1.0 §6.2 변환·리뷰 경로로 합류한다.

- 기능명 추출:
  - URL 분기 (단일 인자): 인자 URL의 페이지 `<title>` 또는 첫 `<h1>` 우선.
  - URL 분기 (다중 인자): 첫 번째 인자 URL의 title 우선. 그 외는 텍스트 분기와 동일 fallback.
  - 텍스트·파일·디렉터리 분기: 0.1.0 그대로 (반복 등장 제목 → 첫 핵심 명사구). 본문에서 추출돼 fetch한 자식 URL의 title은 기능명 추출에 영향 주지 않는다.
- 두 템플릿 변환·자동 리뷰·입력 제외 추적: 0.1.0 §6.2 그대로.
- SSOT 매칭: 통합 본문 전체 키워드로 grep. fetch한 외부 URL 본문은 SSOT corpus에는 포함하지 않는다 (외부 문서·일회성). SSOT corpus는 0.1.0 §13 정의 그대로 — 프로젝트 폴더 내 `*.md`만.

### 4.7 재귀 fetch 정책

**모든 분기 공통**. 인자 URL이든 본문에서 추출된 URL이든 동일 절차로 fetch하고 그 본문도 통합 입력에 합류시킨다.

#### 4.7.1 동작

```
# seed: 분기에 따라 결정
seed_urls = []
if URL 분기:        seed_urls += 인자 URL 토큰 list
                    seed_urls += §4.2.2 인자 URL fetch 본문에서 추출된 URL  (1차 fetch 후 합류)
if 텍스트/파일/디렉터리 분기:
                    seed_urls += §4.2.2 입력 본문에서 추출된 URL

queue = [(url, depth=0) for url in dedup(seed_urls)]
visited = {}
while queue:
  url, depth = queue.pop()
  key = normalize(url)
  if key in visited: continue
  visited[key] = fetch(url)            # §4.3 동일 절차
  if visited[key].status != ok: continue
  body = extract(visited[key])         # §4.4 동일 절차 (cap 없음)
  for link in find_links(body):        # §4.2.2 추출 패턴 동일
    if not is_followable(link): continue
    queue.push((normalize(link), depth + 1))
combined_body = concat(원본 입력 본문, visited[*].body with 출처 표기)
```

depth·pages·body 크기 cap을 두지 않는다. visited set의 cycle 방지로만 무한 루프를 차단한다. 한 호출이 길어지거나 토큰이 커지더라도 사용자가 받는 변환·리뷰의 품질·검증을 우선한다.

#### 4.7.2 cap 정책

**cap 없음**. depth·pages·body 크기 hard limit을 두지 않는다.

이유: 사용자 명시 요청 — 품질·검증이 토큰 절약보다 우선. 누락된 본문 때문에 변환·리뷰가 부정확해지는 비용이, fetch가 길어지는 비용보다 크다.

cycle·중복은 §4.7.4 `visited set` + URL normalize로 차단한다. 같은 URL은 한 번만 fetch되므로 같은 호스트 안에서도 무한 루프는 발생하지 않는다.

`(reserved)` — 향후 운영 중 명백한 폭주가 관찰되면 후속 PRD에서 hard cap을 재도입할 수 있다. 0.1.1은 cap 없이 release한다.

#### 4.7.3 따라갈 링크 판별 (`is_followable`)

다음 조건을 **모두** 만족하면 따라간다:

- scheme이 `http` 또는 `https` (다른 scheme·blob/data/mailto/tel/javascript 모두 제외).
- self-anchor 아님 (루트 page와 같은 URL의 `#section` 형태는 제외).
- visited set에 없음.
- normalize 후 visited set에 없음 (트래킹 파라미터·fragment 제거 후 비교 — §4.7.4).

**호스트 제한 없음**: 외부 도메인도 그대로 따라간다. 사용자 명시 요청 — "외부 링크는 무조건 재귀". 본 PRD는 same-host 제한을 두지 않는다.

#### 4.7.4 URL normalize

같은 페이지를 중복 fetch하지 않도록 visited 비교 전 정규화한다:

- fragment(`#...`) 제거.
- trailing `/` 정리 (path 끝의 `/` 한 개 단위로 통일).
- 트래킹 query 제거: `utm_*`, `fbclid`, `gclid`, `mc_cid`, `mc_eid`, `_hsenc`, `_hsmi`, `ref`, `ref_src`.
- 호스트 lowercase.
- query 키 정렬 (값은 보존).

#### 4.7.5 fetch 실패·skip 케이스

다음 경우는 해당 URL 본문을 본문 합류에서 제외하되, 호출은 종료하지 않고 §5.4 출처 list에 사유와 함께 기록한다:

| 사유 | 처리 |
|---|---|
| timeout / 네트워크 오류 / 4xx / 5xx | 본문 0, status·error 기록. |
| 인증 게이트(2xx인데 본문이 로그인 폼 휴리스틱) | 본문 0, `사유: 인증 필요` 기록. |
| 이미지 content-type (`image/*`) | §4.8 image 처리로 라우팅. fetch는 성공했으나 텍스트 추출 대신 multimodal 입력으로 사용. |
| 지원 안 하는 content-type (`application/pdf`, `application/octet-stream`, `video/*`, `audio/*` 등) | 본문 0, `사유: content-type <type>` 기록. |
| 본문 추출 결과 0byte | 본문 0, `사유: 빈 본문` 기록. |

**루트 URL 자체가 위 사유로 실패**한 경우만 §4.5 sanity check가 적용되어 호출이 종료된다. 자식 URL 실패는 종료 사유가 아니다. 이미지 content-type은 실패 아님 — §4.8로 정상 라우팅된다. depth/pages/body size cap은 두지 않으므로 cap 초과 사유는 발생하지 않는다.

#### 4.7.6 본문 합류 형식

통합 본문은 출처 단위로 헤더를 붙여 concat한다. 분기에 따라 첫 블록이 다르다.

**URL 분기 (인자 URL만 있는 경우):**

```
=== [출처 1] <인자 URL 1> ===
<URL 1 본문>

=== [출처 2] <인자 URL 2> ===   (인자가 다중일 때만)
<URL 2 본문>

=== [출처 N] <자식 URL> ===
<자식 본문>
```

**텍스트·파일·디렉터리 분기 (원본 입력 + 본문 추출 URL fetch 결과):**

```
=== [출처 0] 원본 입력 (직접 입력 / 파일 N개 / 디렉터리 텍스트 N개) ===
<원본 입력 본문 그대로>

=== [출처 1] <추출 URL 1> ===
<URL 1 본문>

=== [출처 N] <자식 URL> ===
<자식 본문>
```

원본 입력은 항상 `[출처 0]`로 표기. URL fetch 본문은 `[출처 1..N]`로 visited 순서대로. main이 두 템플릿 변환 시 출처 헤더로 본문 출처를 식별할 수 있다. 출처 헤더 자체는 변환 본문에 들어가지 않는다 (입력 마커일 뿐).

#### 4.7.7 cycle·중복 방지

- 같은 normalize URL은 한 번만 fetch (visited set).
- redirect chain은 최종 URL을 visited에 기록.
- 2개 페이지가 서로 링크해도 visited set으로 무한 루프 차단.

### 4.8 이미지 multimodal 처리

이미지 입력을 Claude의 내장 multimodal 능력으로 읽어 텍스트 설명을 생성하고 통합 본문에 합류시킨다.

#### 4.8.1 이미지 시드 경로

다음 4가지 경로로 이미지가 image queue에 시드된다:

1. **파일 분기 — 직접 인자**: 인자 파일 확장자가 §4.8.2 지원 목록이면 파일 자체를 image queue에 시드.
2. **디렉터리 분기**: 디렉터리 안 모든 지원 이미지 파일을 iteration 중에 image queue에 시드. 0.1.0 디렉터리 분기는 UTF-8 텍스트 파일만 읽었지만, 0.1.1부터 지원 이미지도 함께 읽는다.
3. **본문 추출 — markdown image / HTML img**: §4.2.2의 `![alt](path)` / `<img src="path">`. 상대 경로면 입력 파일·디렉터리 기준으로 resolve.
4. **fetch 결과 — image content-type**: §4.7.5의 `image/*` content-type 응답. fetch한 byte를 그대로 image queue에 시드.
5. **inline data URI**: `data:image/...;base64,...` 본문 내 등장 시 디코딩 후 image queue에 시드.

#### 4.8.2 지원 포맷

| 항목 | 값 | 비고 |
|---|---|---|
| 지원 확장자 | `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.bmp`, `.heic`, `.svg` | Claude multimodal 입력 지원 포맷에 맞춘다. |
| 크기 cap | **없음** | byte size·해상도 hard limit 두지 않는다. 품질·검증 우선. |
| 개수 cap | **없음** | 한 호출에서 처리할 이미지 수 상한 두지 않는다. |
| resize | 안 함 | 원본 byte 그대로 multimodal 입력. |

`.svg`는 텍스트 포맷이지만 multimodal 모델이 raster 이미지보다 잘 다루지 못할 수 있다. SVG는 1차로 raw XML 텍스트로 본문에 포함하고, 그 위에 multimodal 해석도 시도한다.

cycle·중복 방지는 visited set(파일 경로 또는 URL normalize key)으로 충분하다.

#### 4.8.3 multimodal 해석

각 이미지에 대해 main이 다음 prompt 패턴으로 자기 자신(또는 동일 LLM 호출)에 해석을 요청한다:

```
이미지: [출처 N] <파일명 또는 URL>
역할: 기획 초안의 일부.
해석 목표:
- 이미지 안 텍스트(라벨·헤더·캡션·주석)를 가능한 한 그대로 옮긴다.
- 다이어그램/플로우/표는 구조를 텍스트로 재구성한다 (노드·간선·열·행).
- 화면 캡처면 화면 요소(버튼·입력 필드·메뉴·상태)와 흐름을 글로 기술한다.
- 그림이나 사진이면 등장 객체·관계·상태를 1~2문단으로 묘사한다.
- 추측은 표시한다 ("추정:" 접두). 확실히 보이는 것만 단정한다.
출력: markdown. 헤더 깊이는 ##부터.
```

해석 결과 텍스트는 출처 헤더 `=== [출처 N] 이미지: <파일명 또는 URL> ===` 아래에 본문 합류된다 (§4.7.6 형식과 동일).

#### 4.8.4 실패·skip 케이스

| 사유 | 처리 |
|---|---|
| 지원 안 하는 확장자 (`.tiff`, `.psd`, `.ai`, etc.) | 본문 합류 안 함, `사유: 미지원 이미지 포맷` 출처 list에 기록. |
| 파일 없음 / 권한 없음 / 손상된 이미지 | 본문 합류 안 함, `사유: image read 실패: <error>` 기록. |
| multimodal 해석이 빈 응답 | 본문 합류 0, `사유: 빈 해석 결과` 기록. |
| `--no-image` 옵션 | 모든 이미지 시드 skip, list에도 기록 안 함. |

이미지 실패는 호출 종료 사유 아님 — 텍스트 본문이 있으면 그대로 변환 진행. size·개수 cap은 두지 않으므로 cap 초과 사유는 발생하지 않는다.

#### 4.8.5 본문 합류 위치

이미지 해석 결과는 visited 순서대로 일반 URL fetch 본문 다음에 합류한다. 같은 출처 번호 체계(`[출처 N]`) 그대로 사용. 이미지인지 텍스트인지 구분은 출처 헤더의 `이미지:` 접두로 표시.

#### 4.8.6 SSOT 매칭

multimodal 해석 텍스트도 통합 본문 일부로 SSOT 키워드 grep 대상이 된다. 단, multimodal 해석은 추정·환각 가능성이 있으므로 §5.2 SSOT 검색 키워드 list에는 image 출처 키워드만 별도 표시하지 않는다 (단순화).

## 5. 출력 변경

### 5.1 헤더 — 출처 요약

0.1.0 §7.1 정상 출력 헤더의 `입력 처리` 줄에 **fetch 결과**를 덧붙인다. URL 발견·fetch가 한 건이라도 있으면 추가 줄도 붙는다.

분기별 헤더 형태:

```
# URL 분기 (단일 인자)
- 입력 처리: URL 1개 + 재귀 fetch N개
- 출처: <인자 URL>
- 미결 표기: [TBD] N개
- 입력 제외: N건

# URL 분기 (다중 인자)
- 입력 처리: URL M개 + 재귀 fetch N개
- 출처: M개 (전체 list는 ## 출처 블록 참조)
- ...

# 텍스트/파일/디렉터리 분기 + 본문 URL 추출 발생
- 입력 처리: 직접 입력 + 추출 URL M개 (재귀 fetch N개) + 이미지 I개   # 텍스트
- 입력 처리: 파일 K개 + 추출 URL M개 (재귀 fetch N개) + 이미지 I개    # 파일
- 입력 처리: 디렉터리 텍스트 K개 + 이미지 I개 + 추출 URL M개 (재귀 fetch N개) # 디렉터리
- ...

# 텍스트/파일/디렉터리 분기 + URL·이미지 0건
- 입력 처리: 직접 입력 / 파일 K개 / 디렉터리 텍스트 K개   # 0.1.0 헤더 그대로

# 이미지 단독 인자 (파일 분기, 이미지 1개)
- 입력 처리: 이미지 1개

# 이미지 다수 인자 (파일 분기 다중)
- 입력 처리: 파일 0개 + 이미지 K개
```

규칙:

- 인자 URL 수 + 추출 URL 수 (root 합산) = 헤더 첫 숫자.
- `재귀 fetch N개`는 root 외 자식 URL fetch 성공 수. 0이면 `(재귀 fetch 0개)`로 명시. fetch 자체가 0건이면 (모든 분기에서 URL 발견 0건이면) 괄호 자체를 생략.
- `출처:` 줄은 인자 URL이 1개일 때만 단일 URL을 그대로 출력. 인자 URL 다중·추출 URL 다수일 때는 `M개 (전체 list는 ## 출처 블록 참조)`로 갈음.

`## 입력 제외 항목` 블록에서 인용·위치 표기 시, URL fetch 본문에서 나온 인용은 위치를 `[출처 N] §섹션 또는 줄 N` 형태로, 원본 입력에서 나온 인용은 0.1.0 형식 그대로(`파일명:라인 또는 "직접 입력"`) 표기한다.

### 5.2 리뷰 결과 — SSOT 키워드 줄

`## 리뷰 결과` 블록의 요약 줄에 **SSOT 검색 키워드 list**를 추가한다.

기존 (0.1.0):

```
## 리뷰 결과: [통과 | 발견 N건]

- 자체 품질 발견: N건
- SSOT 충돌 발견: N건 (SSOT 매칭 파일 N개)
```

신규 (0.1.1):

```
## 리뷰 결과: [통과 | 발견 N건]

- 자체 품질 발견: N건
- SSOT 검색 키워드: [keyword1, keyword2, keyword3, ...]
- SSOT 충돌 발견: N건 (SSOT 매칭 파일 N개)
```

규칙:

- 키워드 list는 `[]` 안에 콤마 구분으로 출력. 키워드가 없으면 `[]`로 빈 list.
- `--no-review`로 리뷰 자체를 skip한 경우 이 줄도 출력 안 함 (블록 통째로 없음).
- 추출 키워드 출처 카테고리(기능명·도메인·역할·상태·정책 핵심어) 구분은 출력에 반영하지 않는다 — 단순 list로만.
- 키워드 수 상한 두지 않는다. 추출된 그대로 노출.
- 매칭 0건이라 SSOT 점검을 skip한 경우에도 검색에 사용한 키워드는 그대로 출력하고, `SSOT 충돌 발견: 0건 (SSOT 매칭 파일 0개)` 한 줄을 함께 출력한다. 사용자가 "왜 매칭이 없었는지"를 키워드로 즉시 판단할 수 있다.

### 5.3 그 외

리뷰 결과 발견 사항 list, 정책서·기능설계서 본문, 입력 제외 항목 출력 형태는 0.1.0과 동일.

### 5.4 출처 list

URL fetch나 이미지 처리가 한 건이라도 발생한 모든 분기에서 출력된다 (URL 분기 전용 아님). 위치는 `## 입력 제외 항목` 블록 **앞**에 둔다 (변환 본문 → 출처 list → 입력 제외 → 리뷰 결과 순).

```
## 출처

원본 입력: <"직접 입력" / "파일 N개" / "디렉터리 텍스트 N개" / "URL M개" / "이미지 I개">
재귀 fetch: 성공 N개 / 실패 K개 (cap 없음)

| # | depth | 출처 종류 | URL/경로 또는 위치 | 상태 | 본문 사용 |
|---|-------|----------|--------------------|------|-----------|
| 0 | -     | 원본     | 직접 입력 / 파일 / 디렉터리 / —      | —                       | O (원본) |
| 1 | 0     | 인자 URL | <URL>                                | 200                     | O |
| 2 | 0     | 추출 URL | <URL> (출처: 원본 §line N)           | 200                     | O |
| 3 | 1     | 자식 URL | <URL> (출처: [#1] §line N)           | 401 인증 필요            | X |
| 4 | 0     | 인자 이미지 | path/diagram.png                  | image/png 1.2MB         | O (multimodal) |
| 5 | 0     | 추출 이미지 | <URL or 경로> (출처: 원본 §line N) | image/jpeg 0.4MB        | O (multimodal) |
| 6 | 1     | fetch 이미지 | <URL> (출처: [#1] §img alt)        | image/webp 800KB        | O (multimodal) |
| 7 | -     | 추출 이미지 | path/broken.png                    | image read 실패         | X |
| 8 | 2     | 자식 URL | <URL>                                | content-type video/mp4   | X |
| ... | | | | | |
```

규칙:

- `#` 번호는 본문 합류 순서. 변환 본문에서 `[출처 N]`로 참조한다. `[출처 0]`은 원본 입력 (URL 분기에서는 별도 행 없이 1번부터 시작).
- `출처 종류`: 7종.
  - `원본`: 사용자가 직접 준 텍스트·파일·디렉터리.
  - `인자 URL`: URL 분기에서 인자로 받은 URL (depth=0).
  - `추출 URL`: 원본 입력 본문에서 §4.2.2로 추출된 URL (depth=0).
  - `자식 URL`: fetch한 페이지 본문에서 재귀로 발견된 URL (depth ≥ 1).
  - `인자 이미지`: 인자나 디렉터리 안에서 직접 발견된 이미지 파일 (depth=0).
  - `추출 이미지`: 원본 입력 본문에서 §4.2.2로 추출된 markdown image / HTML img 참조.
  - `fetch 이미지`: fetch 중 `image/*` content-type 응답으로 받은 이미지.
- `URL/경로 또는 위치` 컬럼에서 옆 괄호는 어디서 발견됐는지 추적용. `(출처: 원본 §line N)` / `(출처: [#K] §line N)` / `(출처: [#K] §img alt)` 형식.
- `상태`: HTTP status (성공) 또는 skip 사유 (`인증 필요`, `content-type <type>`, `빈 본문`, `미지원 이미지 포맷`, `image read 실패`, `빈 해석 결과`, `timeout`, `network error`). 이미지 성공 행은 `image/<subtype> <bytesize>` 형태.
- `본문 사용`: 본문이 실제 통합 입력에 합류했는지(O/X). 이미지 multimodal 합류는 `O (multimodal)`로 명시. 인증 게이트·실패는 X. 원본 행은 항상 O.
- 표는 visited 순서 그대로. 정렬 안 함.
- 실패로 처리 못 한 URL/이미지도 list에 포함해 사용자가 추적 가능하도록 한다.

실패가 0건이면 표 아래에 `모든 발견 링크·이미지 처리 성공` 한 줄. URL fetch와 이미지 처리가 모두 0건이면 `## 출처` 블록 자체를 생략한다 (헤더의 `입력 처리` 줄로 충분).

## 6. CLI 인자

기존 `--ssot-include`, `--no-review`는 모든 분기에서 동일하게 동작한다.

신규 인자 (모든 분기 공통, 모두 optional):

| 인자 | 기본값 | 설명 |
|---|---|---|
| `--no-fetch` | off | 본문에서 URL이 발견되어도 fetch하지 않는다. URL 분기 인자도 fetch 안 함. 디버그·오프라인 모드용. |
| `--no-image` | off | 모든 이미지 시드(인자·디렉터리·추출·fetch)를 무시한다. multimodal 호출 0건. 텍스트 본문만 변환 입력으로 사용. |

cap 관련 인자(`--depth`, `--max-pages`, `--max-body`, `--max-image`)는 두지 않는다. §4.7.2·§4.8.2에서 cap 자체를 두지 않기 때문 — 품질·검증 우선 정책.

`--no-fetch`/`--no-image` 사용 시 `## 출처` 블록은 해당 종류만 비워서 표시하거나(부분 사용), 모두 비활성이면 블록 통째로 생략한다. 헤더 `입력 처리` 줄도 disable된 항목은 누락된다.

## 7. 구성 변경

폴더 구조 변경 없음. `skills/formalize/SKILL.md` 본문에 URL 분기 처리 절차(§4.2~§4.7), 이미지 multimodal 처리(§4.8), 출력 변경(§5)을 추가한다.

추정 size 증가: ~220 line (URL dispatch + 본문 URL/이미지 추출 + 재귀 fetch 루프 + 이미지 multimodal 루프 + visited 관리 + sanity check + 헤더·출처 list·SSOT 키워드 줄). cap 코드 제거로 0.1.0 대비 분량은 줄어듦. 전체 ~720 line 내외.

## 8. 마일스톤

1. **M1 — URL 판별 (인자) + fetch 호출**: §4.2.1, §4.3 구현. 단일·다중 URL 인자 분기 진입. http(s) 외 scheme 거부.
2. **M2 — 본문 URL·이미지 참조 추출**: §4.2.2 구현. markdown link / autolink / HTML href·src / plain URL 4종 + markdown image / HTML img / data URI 추출. self-anchor·blob·mailto·tel·javascript 제외.
3. **M3 — 본문 추출**: §4.4 구현. HTML/Markdown/plain text 분기.
4. **M4 — sanity check**: §4.5 처리 (URL 분기 종료 조건 + 텍스트 분기 비종료 정책).
5. **M5 — 재귀 fetch 루프**: §4.7 — visited set + URL normalize로 cycle 방지. is_followable 판별. 통합 본문 형식 (원본+fetch). cap 없음.
6. **M6 — 이미지 multimodal 처리**: §4.8 — 이미지 시드 5경로(인자·디렉터리·추출·fetch image content-type·data URI), 지원 포맷, multimodal 해석 prompt, 실패·skip 케이스, 본문 합류. cap 없음.
7. **M7 — CLI 인자**: §6의 `--no-fetch`, `--no-image` 파싱·적용.
8. **M8 — 변환·리뷰 합류**: §4.6 — 통합 본문(텍스트+fetch+이미지 해석)이 텍스트 분기와 동일 경로로 흐르는지 확인. 다중 URL 분기·이미지 단독 분기에서 기능명 추출 확인.
9. **M9 — 출력 헤더**: §5.1 — 분기별 6 케이스 (단일/다중 URL, 텍스트+추출, 이미지 단독·다수).
10. **M10 — 출처 list 블록**: §5.4 — `## 출처` 표 (원본·인자 URL·추출 URL·자식 URL·인자 이미지·추출 이미지·fetch 이미지 7종). cap 초과·실패 사유 표기.
11. **M11 — SSOT 키워드 줄**: §5.2 리뷰 결과 요약에 검색 키워드 list 출력. 매칭 0건/--no-review 케이스 동작 확인.
12. **M12 — Claude Code + Codex 양쪽 동작 확인** (Codex multimodal 능력 차이 검증).
13. **M13 — release v0.1.1**.

## 9. 성공 기준

- `formalize https://...` 한 번 호출로 페이지 본문이 정책서·기능설계서로 변환되고 리뷰까지 출력된다.
- fetch 실패·인증 게이트·지원 안 하는 content-type은 한 줄 사유로 명확히 종료한다.
- 0.1.0의 모든 기존 분기(텍스트/파일/디렉터리)는 회귀 없이 그대로 동작한다.
- 출력 헤더의 `입력 처리` 줄이 분기 + URL 추출/fetch + 이미지 결과를 정확히 반영한다.
- URL fetch·이미지 해석 결과는 디스크에 저장되지 않는다 (0.1.0 저장 없음 정책 유지).
- 리뷰가 실행될 때마다 `SSOT 검색 키워드: [...]` 줄이 출력된다. 매칭 파일 0건이어도 키워드 list는 보인다 (사용자가 검색 범위 검증 가능).
- **다중 URL 인자**(`formalize https://a https://b https://c`)가 정상 동작하며, 각 URL이 모두 root로 fetch되고 cycle 방지 외 cap 없이 자식까지 재귀 fetch된다.
- **텍스트·파일·디렉터리 분기에서도 본문에 URL이 포함되면 자동 추출되어 fetch 대상**이 된다. URL 추출 0건이면 0.1.0과 동일하게 동작한다 (회귀 없음).
- **이미지 처리**: 인자 이미지(`formalize diagram.png`), 디렉터리 안 이미지, 본문에 등장한 markdown image / HTML img, fetch한 image content-type 응답, inline data URI 모두 multimodal 해석 후 본문 합류된다.
- 미지원 포맷·읽기 실패는 호출 종료 사유 아님 — 출처 list에 사유만 기록.
- **cap 없음**: depth·pages·body·image size 모두 hard limit을 두지 않는다. 큰 입력도 끝까지 처리해 변환·리뷰 품질을 우선한다. cycle은 visited set으로만 차단.
- `## 출처` 블록에 fetch한 URL과 처리한 이미지 list (출처 종류 7종·status·본문 사용 여부 포함)가 표로 출력된다. 인증 게이트·content-type skip·이미지 실패가 모두 사유와 함께 추적 가능하다.
- 자식 URL fetch 실패는 호출을 종료시키지 않는다. 실패 사유만 출처 list에 남긴다 (URL 분기에서는 모든 root URL 실패 시에만 sanity check로 종료).
- `--no-fetch` / `--no-image`로 URL/이미지 처리를 끄고 0.1.0 동작과 동등하게 처리할 수 있다 (디버그·오프라인·multimodal 토큰 절약 필요 시).

## 10. 비호환·마이그레이션

- 0.1.0 → 0.1.1은 **순수 추가** 변경이다. 기존 호출은 모두 동일하게 동작한다.
- 사용자가 0.1.0에서 URL 문자열을 텍스트 인자로 그대로 넣어 변환을 시도했던 경우(드물지만), 0.1.1에서는 URL 분기로 흘러 fetch가 일어난다. URL 자체를 텍스트로 처리하고 싶다면 URL 앞뒤를 따옴표로 감싸거나 본문 텍스트를 직접 입력한다.

## 11. 용어 추가

- **URL 분기**: `formalize` 인자가 1개 이상의 `^https?://` 토큰인 경우의 처리 경로. 인자 URL fetch → 본문 추출 → 재귀 fetch → 텍스트 분기 합류.
- **인자 URL**: 사용자가 호출 인자로 직접 준 URL. URL 분기에서만 존재. depth=0.
- **추출 URL**: 텍스트·파일·디렉터리 분기의 입력 본문(또는 URL 분기 인자 URL fetch 본문)에서 §4.2.2 패턴으로 추출된 URL. depth=0.
- **자식 URL**: fetch한 페이지 본문에서 다시 발견되어 재귀로 따라간 URL. depth ≥ 1.
- **root URL**: 인자 URL과 추출 URL을 통칭. depth=0인 fetch 시드.
- **원본 입력**: 사용자가 인자로 직접 준 텍스트·파일·디렉터리 콘텐츠. URL fetch 본문이 아닌 부분. 출처 list에서 `[#0]`.
- **출처(Source)**: 통합 본문에 합류한 콘텐츠의 출처. 원본 입력 / 인자 URL / 추출 URL / 자식 URL / 인자 이미지 / 추출 이미지 / fetch 이미지 7종. 출력 §5.4 출처 list에 번호와 함께 명시.
- **visited set**: 같은 호출 안에서 이미 fetch한 URL과 처리한 이미지의 normalize key 집합. cycle·중복 방지용. 0.1.1에서 폭주 차단의 유일한 메커니즘.
- **cap 없음 정책**: 0.1.1은 depth·pages·body 크기·image size·image 개수 hard limit을 두지 않는다. 사용자 명시 요청 — 토큰 절약보다 변환·리뷰 품질·검증 우선. 후속 PRD에서 운영 데이터 보고 재도입 가능.
- **이미지 multimodal 처리**: 이미지 입력을 Claude의 내장 vision 능력으로 해석해 텍스트 설명을 생성하고 통합 본문에 합류시키는 절차. §4.8.
- **인자 이미지**: 인자 또는 디렉터리 분기에서 직접 발견된 이미지 파일.
- **추출 이미지**: 본문의 markdown image / HTML img / data URI 등으로 발견된 이미지 참조.
- **fetch 이미지**: URL fetch 결과 content-type이 `image/*`로 응답된 이미지.

그 외 모든 용어는 0.1.0 §13 그대로.
