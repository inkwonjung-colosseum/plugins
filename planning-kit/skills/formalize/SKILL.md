---
name: formalize
description: "기획 초안(텍스트·파일·디렉터리·URL·이미지)을 정책서와 기능설계서 두 본문으로 변환하고 같은 응답에서 자동 리뷰까지 출력해야 할 때 사용한다."
argument-hint: "<기획 초안 텍스트 | 파일 | 디렉터리 | URL [URL ...]> [--ssot-include <glob>] [--no-review] [--no-fetch] [--no-image]"
---

# formalize

기획 초안을 받아 **정책서 + 기능설계서 두 본문**으로 변환하고, **같은 응답에서 자동 리뷰**까지 한 번에 출력하는 단일 스킬이다. 산출물은 **로컬 파일로 저장하지 않는다**. 모두 화면 output(응답 markdown)으로만 반환한다.

호출 한 번 = 변환 본문 2개 + 입력 제외 항목 + 리뷰 결과. 사용자는 응답 markdown을 보고 직접 복사·붙여넣는다.

0.1.1부터 추가:
- **URL 분기 (다중 허용)**: `formalize https://a https://b ...`로 페이지 본문을 fetch해 변환 입력으로 쓴다.
- **본문 URL/이미지 추출**: 모든 분기에서 입력 본문 안 URL·이미지 참조를 자동 추출해 fetch/multimodal 처리에 합류시킨다.
- **재귀 fetch (cap 없음)**: visited set만 cycle 방지. depth·pages·body 크기 cap 없음.
- **이미지 multimodal**: 인자·디렉터리·본문·fetch·data URI에서 발견된 이미지를 Claude 내장 vision으로 텍스트화해 본문에 합류.
- **SSOT 키워드 노출**: 리뷰 결과 블록에 SSOT grep 키워드 list를 출력한다.

## 인자

위치 인자 1개 이상 (필수): 기획 초안 텍스트, 파일 경로, 디렉터리 경로, **1개 이상의 URL** 중 하나.

| 인자 | 기본값 | 설명 |
|---|---|---|
| `--ssot-include <glob>` | (없음) | 리뷰 SSOT corpus glob. default = 프로젝트 폴더 안 모든 `*.md` (`.git/`, `node_modules/` 자동 제외). |
| `--no-review` | off | 리뷰 단계 건너뜀. 변환 본문만 출력. |
| `--no-fetch` | off | 본문에서 URL이 발견되어도 fetch하지 않는다. URL 분기 인자도 fetch 안 함. 디버그·오프라인용. |
| `--no-image` | off | 모든 이미지 시드(인자·디렉터리·추출·fetch·data URI)를 무시한다. multimodal 호출 0건. |

cap 관련 인자(`--depth`, `--max-pages`, `--max-body`, `--max-image`)는 두지 않는다 — cap 없음 정책(품질·검증 우선).

## 동작 시퀀스

### Step 1: 입력 dispatch (4 분기 + 공통 추출)

분기 결정 우선순위:

```
1. URL 패턴 (1개 이상)        → URL 분기      (NEW)
2. 디렉터리 경로              → 디렉터리 분기  (지원 이미지 파일도 함께 수집)
3. 파일 경로                  → 파일 분기      (이미지 확장자면 image queue로 단독 시드)
4. 그 외                      → 텍스트 분기
```

분기 직후 모든 분기 공통:

```
5. 본문 URL·이미지 참조 추출 → fetch queue + image queue에 시드
6. 재귀 fetch + 이미지 multimodal 처리 → 통합 본문 합류
```

#### 1.1 URL 분기 판별 (인자 단계)

다음 조건을 **모두** 만족하면 URL 분기:

- 인자를 공백·줄바꿈으로 토큰화한 결과, **모든 비어 있지 않은 토큰**이 URL 패턴이다.
- 각 토큰이 `^https?://`로 시작한다 (`http://`, `https://`만 허용).
- 각 토큰의 호스트부가 비어 있지 않다.

토큰 1개 = 단일 URL 분기. 토큰 ≥2 = 다중 URL 분기. 다중 URL은 모두 `depth=0` root로 visited queue에 시드.

`file://`, `ftp://`, `s3://`, `mailto:`, scheme 없는 입력(`example.com/...`)은 URL 분기 아님 — 텍스트/파일/디렉터리 분기로 흐른다.

URL 토큰과 비-URL 토큰이 섞여 있으면 (`https://x.com 추가 메모`) 텍스트 분기로 흐른다 — 그 본문에서 §1.3으로 URL 추출.

#### 1.2 디렉터리·파일·텍스트 분기 (0.1.0 + 이미지 확장)

1. 디렉터리 분기: `find <dir> -type f`로 파일 목록을 만든다. 노이즈 폴더(`.git/`, `node_modules/`) 제외.
   - UTF-8 텍스트 파일(`.md`, `.txt`, `.markdown` 등)은 `Read`로 읽어 본문 통합.
   - 지원 이미지 확장자(§4.1)면 image queue에 시드.
2. 파일 분기: 인자 파일을 `Read`. 이미지 확장자면 image queue에 단독 시드 (텍스트 본문은 비어 있음 — image 단독 입력).
3. 텍스트 분기: 인자 문자열 자체가 본문.
4. 통합 본문이 literal 빈 문자열·whitespace·0byte이고 이미지·URL 시드도 0건이면 §2 빈 입력 sanity check로 점프.

#### 1.3 본문 URL·이미지 참조 추출 (모든 분기 공통)

분기가 결정된 직후, 입력 본문(텍스트·파일·디렉터리에서 읽은 모든 텍스트)에서 URL·이미지 참조를 추출한다.

URL 분기에서는 **인자 URL의 fetch 본문**도 추출 대상이지만, 그 단계는 §3 재귀 fetch에서 처리한다 (본 단계는 인자가 아닌 입력 본문 한정 — URL 분기에서는 적용 대상 본문 없음).

**URL 추출 패턴:**

- `markdown link`: `[text](https?://...)` → URL 부분만 추출.
- `markdown autolink`: `<https?://...>`.
- `HTML href/src`: `href="https?://..."`/`src="https?://..."` (속성 따옴표 종류 무관).
- `plain URL`: 그 외 본문에서 `https?://[^\s<>"\)]+` 매칭. trailing 구두점(`,`, `.`, `;`, `:`, `)`, `]`) 제거.

**이미지 참조 추출 패턴:**

- `markdown image`: `![alt](path-or-url)` → path/URL 추출. URL이면 fetch queue에 image content-type 시드. 상대 경로면 입력 파일·디렉터리 기준으로 resolve해 image queue에 시드.
- `HTML img`: `<img src="path-or-url" ...>` → 동일 처리.
- `data URI`: `data:image/...;base64,...` → 디코딩 후 image queue에 시드.

**제외:** self-anchor (`#section`만 있는 fragment)·`mailto:`/`tel:`/`javascript:`/`blob:` scheme. 이미지 안에 글자로 적힌 URL OCR도 안 함.

추출된 URL은 visited queue에 `depth=0` root로 시드된다 (인자 URL과 동등). 추출된 이미지는 image queue에 시드. 동일 URL/경로 중복은 visited set으로 제거.

`--no-fetch`면 URL 추출·시드 자체를 skip한다. `--no-image`면 이미지 시드 자체를 skip한다.

### Step 2: 빈 입력 sanity check

다음 한 줄만 출력하고 종료:

```
입력 비어 있음. 기획 초안 텍스트 또는 경로를 인자로 주세요.
```

조건: 통합 본문이 literal 빈 문자열·whitespace·0byte이고 **이미지 시드 0건 + URL 시드 0건**.

URL 분기 sanity check는 §3.4 별도 정의 (모든 root URL 실패 시).

그 외 모든 입력은 변환 시도. 근거 부족·범위 모호도 변환 진행. 부족분은 [TBD], 라벨 매핑이 안 되는 조각은 입력 제외 추적에 기록.

### Step 3: 재귀 fetch + 이미지 multimodal 처리

#### 3.1 재귀 fetch 동작

```
seed_urls = []
if URL 분기:        seed_urls += 인자 URL 토큰 list
if 텍스트/파일/디렉터리 분기:
                    seed_urls += §1.3 입력 본문에서 추출된 URL

queue = [(url, depth=0) for url in dedup(seed_urls)]
visited = {}
while queue:
  url, depth = queue.pop_front()
  key = normalize(url)            # §3.5
  if key in visited: continue
  resp = fetch(url)               # §3.2
  visited[key] = resp
  if resp.status != ok: continue
  if resp.content_type matches image/*: 
      image_queue.push((bytes, source=url))
      continue
  if resp.content_type not text/html|text/markdown|text/plain|application/xhtml+xml:
      record skip reason; continue
  body = extract_text(resp)       # §3.3
  for link in find_links(body):   # §1.3 패턴 동일
    if not is_followable(link): continue
    queue.push((normalize(link), depth + 1))
  for img in find_images(body):
    if URL: queue.push((normalize(img), depth + 1))   # image content-type 응답으로 자연 분기
    else if relative path: image_queue.push((resolved_path, source=url))
combined_body = concat(원본 입력 본문, visited[*].body, image_interpretations,
                       각각 [출처 N] 헤더 prefix)
```

depth·pages·body 크기 cap 없음. visited set의 cycle 방지로만 무한 루프 차단. 한 호출이 길어지더라도 변환·리뷰 품질을 우선한다.

`--no-fetch`면 §3.1 전체 skip — root·자식 모두 fetch 안 함.

#### 3.2 fetch 동작

- `WebFetch` 툴(또는 환경에서 사용 가능한 동등 fetch 수단)로 1회 GET.
- timeout: 30초.
- redirect: 따라간다 (최대 5회).
- User-Agent: 기본값 (위장 안 함).
- 응답 content-type 분기:
  - `text/html`, `text/markdown`, `text/plain`, `application/xhtml+xml` → 본문 추출(§3.3).
  - `image/*` → image queue로 라우팅 (multimodal 입력으로 사용, §4).
  - `application/pdf`, `application/octet-stream`, `video/*`, `audio/*` 등 → skip + 출처 list에 사유 기록.

#### 3.3 본문 추출

HTML 응답이면 우선순위:

1. `<main>` / `<article>` / `role="main"` 영역.
2. (1)이 없으면 `<body>` 전체에서 `<nav>`, `<aside>`, `<header>`, `<footer>`, `<script>`, `<style>` 제거 후 텍스트.
3. 표는 markdown 표로, 헤딩은 `#` 레벨 유지, 리스트는 `-` 유지. 그 외는 plain text.

Markdown/plain text 응답이면 그대로 사용. 추출 결과는 메모리에만 보관 (저장 없음).

#### 3.4 URL 분기 sanity check

루트 URL이 **모두** 다음 사유로 본문 합류 실패한 경우만 호출 종료. 일부 root만 실패하면 종료하지 않고 §7.3 출처 list에 사유만 기록.

| 케이스 | 사유 메시지 |
|---|---|
| `http`/`https` 외 scheme (인자에 단 1개라도) | `http(s) URL만 지원합니다. (입력: <scheme>)` |
| 모든 root URL fetch 실패 | `모든 URL fetch 실패. 첫 번째 사유: <status 또는 error>` |
| 모든 root URL이 인증 게이트 | `모든 URL이 로그인 필요로 보입니다. 본문을 직접 텍스트로 주세요.` |
| 모든 root URL이 지원 안 하는 content-type | `모든 URL이 지원 안 하는 content-type: <type list>` |
| 통합 본문 추출 결과 0byte | `통합 본문이 비어 있습니다. URL 본문 확인 후 다시 시도하세요.` |

sanity check 메시지는 `## 리뷰 결과` 블록 없이 단독 한 줄 + 입력 URL list를 함께 출력한다.

**텍스트·파일·디렉터리 분기**의 sanity check는 §2 (literal 빈 입력만 거름). 본문에서 URL이 추출됐지만 모든 fetch가 실패해도 텍스트 본문 자체로 변환을 진행한다.

#### 3.5 URL normalize

같은 페이지 중복 fetch 방지:

- fragment(`#...`) 제거.
- trailing `/` 정리 (path 끝의 `/` 한 개 단위로 통일).
- 트래킹 query 제거: `utm_*`, `fbclid`, `gclid`, `mc_cid`, `mc_eid`, `_hsenc`, `_hsmi`, `ref`, `ref_src`.
- 호스트 lowercase.
- query 키 정렬 (값은 보존).

#### 3.6 따라갈 링크 판별 (`is_followable`)

다음 조건을 **모두** 만족:

- scheme이 `http` 또는 `https` (그 외 `blob`/`data`/`mailto`/`tel`/`javascript` 모두 제외).
- self-anchor 아님 (루트 page와 같은 URL의 `#section` 형태는 제외).
- normalize 후 visited set에 없음.

**호스트 제한 없음**: 외부 도메인도 그대로 따라간다 — 본 PRD는 same-host 제한을 두지 않는다.

#### 3.7 fetch 실패·skip 케이스

다음 경우는 해당 URL 본문을 본문 합류에서 제외하되, 호출은 종료하지 않고 §7.3 출처 list에 기록:

| 사유 | 처리 |
|---|---|
| timeout / 네트워크 오류 / 4xx / 5xx | 본문 0, status·error 기록. |
| 인증 게이트 (2xx인데 본문이 로그인 폼 휴리스틱) | 본문 0, `사유: 인증 필요` 기록. |
| 이미지 content-type | image 처리로 라우팅. fetch는 성공. multimodal 입력으로 사용 (§4). |
| 지원 안 하는 content-type (PDF/video/audio/octet-stream 등) | 본문 0, `사유: content-type <type>` 기록. |
| 본문 추출 결과 0byte | 본문 0, `사유: 빈 본문` 기록. |

루트 URL 자체가 위 사유로 모두 실패한 경우만 §3.4 sanity check가 적용되어 호출 종료. 자식 URL 실패는 종료 사유 아님.

#### 3.8 cycle·중복 방지

- 같은 normalize URL은 한 번만 fetch (visited set).
- redirect chain은 최종 URL을 visited에 기록.
- 2개 페이지가 서로 링크해도 visited set으로 무한 루프 차단.

### Step 4: 이미지 multimodal 처리

이미지 입력을 Claude의 내장 vision 능력으로 읽어 텍스트 설명을 생성하고 통합 본문에 합류시킨다.

`--no-image`면 §4 전체 skip. 모든 이미지 시드 무시. multimodal 호출 0건.

#### 4.1 지원 포맷·크기·개수

| 항목 | 값 |
|---|---|
| 지원 확장자 | `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.bmp`, `.heic`, `.svg` |
| 크기 cap | **없음** (byte size·해상도 hard limit 없음) |
| 개수 cap | **없음** (호출당 처리 이미지 수 상한 없음) |
| resize | 안 함 (원본 byte 그대로 multimodal 입력) |

`.svg`는 텍스트 포맷 → 1차로 raw XML 텍스트로 본문 포함, 그 위에 multimodal 해석도 시도한다.

cycle·중복 방지는 visited set(파일 경로 또는 URL normalize key)으로 차단.

#### 4.2 이미지 시드 5경로

1. **인자 파일**: 인자 파일 확장자가 §4.1 지원 목록이면 파일 자체를 image queue에 시드.
2. **디렉터리**: 디렉터리 안 모든 지원 이미지 파일을 iteration 중 image queue에 시드.
3. **본문 추출 — markdown image / HTML img**: §1.3 패턴. 상대 경로면 입력 파일·디렉터리 기준으로 resolve.
4. **fetch 결과 — image content-type**: §3.7 응답이 `image/*`면 fetch byte를 image queue에 시드.
5. **inline data URI**: `data:image/...;base64,...` 본문 등장 시 디코딩 후 image queue에 시드.

#### 4.3 multimodal 해석

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

해석 결과 텍스트는 출처 헤더 `=== [출처 N] 이미지: <파일명 또는 URL> ===` 아래에 본문 합류된다 (§5 형식과 동일).

#### 4.4 실패·skip 케이스

| 사유 | 처리 |
|---|---|
| 지원 안 하는 확장자 (`.tiff`, `.psd`, `.ai`, ...) | 본문 합류 안 함, `사유: 미지원 이미지 포맷` 기록. |
| 파일 없음 / 권한 없음 / 손상된 이미지 | 본문 합류 안 함, `사유: image read 실패: <error>` 기록. |
| multimodal 해석이 빈 응답 | 본문 합류 0, `사유: 빈 해석 결과` 기록. |
| `--no-image` 옵션 | 모든 이미지 시드 skip, list에도 기록 안 함. |

이미지 실패는 호출 종료 사유 아님 — 텍스트 본문이 있으면 그대로 변환 진행.

#### 4.5 SSOT 매칭 영향

multimodal 해석 텍스트도 통합 본문 일부 → SSOT 키워드 grep 대상. 단, 추정·환각 가능성이 있으므로 §7.2 SSOT 키워드 list에는 image 출처 키워드만 별도 표시하지 않는다 (단순화 — 단일 list).

### Step 5: 통합 본문 합류 형식

통합 본문은 출처 단위로 헤더를 붙여 concat. 분기에 따라 첫 블록이 다르다.

**URL 분기 (인자 URL만):**

```
=== [출처 1] <인자 URL 1> ===
<URL 1 본문>

=== [출처 2] <인자 URL 2> ===   (인자 다중일 때만)
<URL 2 본문>

=== [출처 N] <자식 URL> ===
<자식 본문>

=== [출처 N+1] 이미지: <URL or 경로> ===   (이미지가 있을 때)
<multimodal 해석>
```

**텍스트·파일·디렉터리 분기 (원본 + 본문 추출 URL fetch 결과 + 이미지):**

```
=== [출처 0] 원본 입력 (직접 입력 / 파일 N개 / 디렉터리 텍스트 N개) ===
<원본 입력 본문 그대로>

=== [출처 1] <추출 URL 1> ===
<URL 1 본문>

=== [출처 N] <자식 URL> ===
<자식 본문>

=== [출처 N+1] 이미지: <파일명 or URL> ===
<multimodal 해석>
```

원본 입력은 항상 `[출처 0]`. URL fetch 본문은 `[출처 1..N]` visited 순서. 이미지 해석은 일반 URL fetch 본문 다음에 visited 순서로 합류. 출처 헤더 자체는 변환 본문에는 들어가지 않는다 (입력 마커일 뿐).

### Step 6: 변환·리뷰 흐름

§3·§4가 끝난 통합 본문을 받아 변환·리뷰 진행.

#### 6.1 기능명 추출

- URL 분기 (단일 인자): 인자 URL의 페이지 `<title>` 또는 첫 `<h1>` 우선.
- URL 분기 (다중 인자): 첫 번째 인자 URL의 title 우선. 그 외는 텍스트 분기와 동일 fallback.
- 텍스트·파일·디렉터리 분기: 0.1.0 그대로.
- 본문에서 추출돼 fetch한 자식 URL의 title은 기능명 추출에 영향 주지 않는다.

선택 우선순위 (URL 분기 외):

1. 입력에 명시된 주제 (`# 주문 취소`, `## 입고 기능`, `[기능명]: ...`).
2. 단일 파일 입력이면 파일명 stem.
3. 디렉터리 입력이면 디렉터리명.
4. 본문에 반복 등장하는 제목.
5. 첫 핵심 명사구.

여러 기능 후보가 있으면 **1순위 1개만** 처리. 그 외 후보는 변환 제외 + 입력 제외 추적에 `다른 기능 후보` 사유로 기록.

#### 6.2 두 템플릿 변환 (항상 실행)

1. 두 템플릿 병렬 `Read`:
   - `templates/기능설계서.md` (8 섹션)
   - `templates/정책서.md` (10 섹션)
2. main이 같은 턴에서 두 본문을 직접 작성.
3. 라벨 매핑:
   - 화면·흐름·동작·입력 항목·권한·예외 메시지 → 기능설계서.
   - 규칙·조건·예외 승인·역할 책임·상태 전이·연동 정책 → 정책서.
4. 라벨 매핑 안 되는 조각, 같은 내용이 다른 위치에 이미 들어간 조각, 단편적이라 [TBD]로도 못 채우는 조각은 입력 제외 추적으로.
5. 근거 부족 셀은 inline `[TBD]`. 빈 row·빈 섹션 삭제 허용.
6. marker는 `[TBD]` 1종만. `[미정]`/`[가정]`/`[확인 필요]`/`[충돌 후보]`/`해당 없음` 모두 사용 금지.
7. 작성 결과는 메모리에만. **파일 저장 안 함** (`Write`·`mkdir`·`Bash` 저장 호출 없음).

#### 6.3 자동 리뷰 (`--no-review`가 아닐 때)

1. `references/review-rules.md`를 `Read`로 읽어 2축 기준 확정.
2. 메모리의 두 본문 + 통합 본문 + SSOT corpus만 근거로 main이 단일 패스 점검.
3. **A. 본문 자체 품질 (Self-Review)**: 충실도·라벨 cross-bleed·용어 일관성·정책-기능 매핑·누락. 기준은 `review-rules.md` §A.
4. **B. SSOT 충돌**:
   - 변환 본문에서 키워드 추출 (기능명·도메인·역할·상태·정책 핵심어).
   - **추출 키워드 list를 §7.2 리뷰 결과 헤더 줄에 그대로 노출**한다.
   - `--ssot-include` 인자가 있으면 해당 glob, 없으면 프로젝트 폴더 전체 `*.md`(`.git/`, `node_modules/` 자동 제외)에서 `grep -l`/`rg -l`로 매칭.
   - **SSOT corpus는 프로젝트 폴더 내 `*.md`만**. fetch한 외부 URL 본문은 SSOT corpus에 포함하지 않는다 (외부 문서·일회성).
   - 매칭 0건 → B축 `검증 대상 없음`. 출력에 `SSOT 매칭 파일 0개` 표시. 결과 낮추지 않음.
   - 매칭 ≥1건 → 매칭 file 직접 `Read`. 변환 본문 확정 문장과 비교해 충돌 list화.
5. 결과 결정:
   - 자체 품질 0건 + SSOT 충돌 0건 → `통과`.
   - 어느 한쪽이라도 ≥1건 → `발견 N건`. 카테고리별 발견 list 출력.

### Step 7: 통합 출력 (화면 output only)

§출력 포맷에 따라 **단일 응답 markdown** 1개 출력. 변환 본문 2개 + 입력 제외 항목(있을 때) + 출처 list(URL fetch·이미지 처리 1건 이상일 때) + 리뷰 결과(`--no-review` 아닐 때)를 한 응답에 합친다.

## 출력 포맷

모든 출력은 응답 markdown. 정책서·기능설계서 본문은 ` ```markdown ... ``` ` 코드 펜스로 감싸 사용자가 통째로 복사할 수 있게 한다.

### 정상 (변환 + 리뷰)

응답 markdown 1개에 다음을 순서대로 (아래 템플릿은 docs 가독성용 4-backtick fence — 실제 응답에서는 wrapper 없이 안쪽만 출력):

````markdown
# [기능명]

- 입력 처리: [§7.1 분기별 헤더 형태 참조]
- 출처: [§7.1 출처 줄 — URL 1개일 때만 단일 URL 그대로]
- 미결 표기: [TBD] N개
- 입력 제외: N건 (0건이면 "없음")

---

## 정책서

```markdown
[정책서 본문 — 10 섹션 markdown 그대로]
```

---

## 기능설계서

```markdown
[기능설계서 본문 — 8 섹션 markdown 그대로]
```

---

## 출처

(URL fetch나 이미지 처리가 한 건이라도 발생할 때만 출력. 둘 다 0건이면 블록 통째로 생략.)

원본 입력: <"직접 입력" / "파일 N개" / "디렉터리 텍스트 N개" / "URL M개" / "이미지 I개">
재귀 fetch: 성공 N개 / 실패 K개 (cap 없음)

| # | depth | 출처 종류 | URL/경로 또는 위치 | 상태 | 본문 사용 |
|---|-------|----------|--------------------|------|-----------|
| 0 | -     | 원본     | 직접 입력 / 파일 / 디렉터리 / —   | —                       | O (원본) |
| 1 | 0     | 인자 URL | <URL>                             | 200                     | O |
| 2 | 0     | 추출 URL | <URL> (출처: 원본 §line N)        | 200                     | O |
| 3 | 1     | 자식 URL | <URL> (출처: [#1] §line N)        | 401 인증 필요           | X |
| 4 | 0     | 인자 이미지 | path/diagram.png               | image/png 1.2MB         | O (multimodal) |
| 5 | 0     | 추출 이미지 | <URL or 경로> (출처: 원본 §line N) | image/jpeg 0.4MB     | O (multimodal) |
| 6 | 1     | fetch 이미지 | <URL> (출처: [#1] §img alt)     | image/webp 800KB        | O (multimodal) |
| 7 | -     | 추출 이미지 | path/broken.png                 | image read 실패         | X |
| 8 | 2     | 자식 URL | <URL>                             | content-type video/mp4   | X |

---

## 입력 제외 항목

발견 사항 (≥1건일 때만 출력. 0건이면 이 섹션 통째로 생략):

1. [한 줄 제목]
   - 사유: [다른 기능 후보 / 라벨 미매핑 / 중복 / 근거 부족 무시 / 포맷 노이즈]
   - 위치: [파일명:라인 / "직접 입력" / "[출처 N] §섹션 또는 줄 N"]
   - 인용: "[입력 원문 ≤80자]"
   - 설명: [왜 본문에 안 넣었는지 한 줄]

---

## 리뷰 결과: [통과 | 발견 N건]

- 자체 품질 발견: N건
- SSOT 검색 키워드: [keyword1, keyword2, keyword3, ...]
- SSOT 충돌 발견: N건 (SSOT 매칭 파일 N개)

### 자체 품질 (Self-Review)

발견 사항 (≥1건일 때만):

1. [제목]
   - 카테고리: [충실도 / cross-bleed / 용어 일관성 / 정책-기능 매핑 / 누락]
   - 위치: [정책서/기능설계서 §섹션]
   - 근거: "[변환 본문 인용]"
   - 영향: [한 줄]
   - 제안: [최소 수정 또는 확인 조건]

### SSOT 충돌

발견 사항 (≥1건일 때만):

1. [제목]
   - 위치: [정책서/기능설계서 §섹션] vs [SSOT 파일 §섹션]
   - 근거: "[변환 본문 인용]" vs "[SSOT 인용]"
   - 영향: [한 줄]
   - 제안: [최소 수정 또는 확인 조건]
````

규칙:

- 자체 품질·SSOT 충돌 모두 0건이면 `## 리뷰 결과: 통과`로만 출력하고 두 sub-section 생략. 단, **`SSOT 검색 키워드` 줄과 카운트 줄은 그대로 출력** (사용자가 키워드로 검색 범위 검증 가능하도록).
- 입력 제외 0건이면 `## 입력 제외 항목` 섹션 통째로 생략.
- URL fetch·이미지 처리가 모두 0건이면 `## 출처` 블록 통째로 생략.
- `## 출처` 블록의 위치는 `## 입력 제외 항목` 블록 **앞**: 변환 본문 → 출처 list → 입력 제외 → 리뷰 결과 순.

### 7.1 헤더 — 입력 처리 줄

분기·발견 종류에 따라 형태 변동:

```
# URL 분기 (단일 인자)
- 입력 처리: URL 1개 + 재귀 fetch N개
- 출처: <인자 URL>

# URL 분기 (다중 인자)
- 입력 처리: URL M개 + 재귀 fetch N개
- 출처: M개 (전체 list는 ## 출처 블록 참조)

# 텍스트/파일/디렉터리 분기 + 본문 URL 추출 발생
- 입력 처리: 직접 입력 + 추출 URL M개 (재귀 fetch N개) + 이미지 I개
- 입력 처리: 파일 K개 + 추출 URL M개 (재귀 fetch N개) + 이미지 I개
- 입력 처리: 디렉터리 텍스트 K개 + 이미지 I개 + 추출 URL M개 (재귀 fetch N개)

# 텍스트/파일/디렉터리 분기 + URL·이미지 0건
- 입력 처리: 직접 입력 / 파일 K개 / 디렉터리 텍스트 K개          # 0.1.0 헤더 그대로

# 이미지 단독 인자 (파일 분기, 이미지 1개)
- 입력 처리: 이미지 1개

# 이미지 다수 인자 (파일 분기 다중)
- 입력 처리: 파일 0개 + 이미지 K개
```

규칙:

- 인자 URL 수 + 추출 URL 수 (root 합산) = 헤더 첫 숫자.
- `재귀 fetch N개`는 root 외 자식 URL fetch 성공 수. 0이면 `(재귀 fetch 0개)`로 명시. fetch 자체가 0건이면 괄호 자체를 생략.
- `출처:` 줄은 인자 URL이 1개일 때만 단일 URL 그대로 출력. 인자 다중·추출 URL 다수일 때는 `M개 (전체 list는 ## 출처 블록 참조)`로 갈음.
- `--no-fetch`/`--no-image`로 disable된 항목은 헤더에서 누락 (해당 종류 0건처럼 표기).

### 7.2 리뷰 결과 — SSOT 키워드 줄

`## 리뷰 결과` 블록 요약 줄에 **SSOT 검색 키워드 list**를 추가한다.

```
## 리뷰 결과: [통과 | 발견 N건]

- 자체 품질 발견: N건
- SSOT 검색 키워드: [keyword1, keyword2, keyword3, ...]
- SSOT 충돌 발견: N건 (SSOT 매칭 파일 N개)
```

규칙:

- 키워드 list는 `[]` 안에 콤마 구분. 키워드 0개면 `[]`로 빈 list.
- `--no-review`로 리뷰 자체를 skip한 경우 이 줄도 출력 안 함 (블록 통째로 없음).
- 카테고리(기능명·도메인·역할·상태·정책 핵심어) 구분은 출력에 반영하지 않음 — 단순 list.
- 키워드 수 상한 없음. 추출된 그대로 노출.
- 매칭 0건이라 SSOT 점검을 skip한 경우에도 검색 키워드는 그대로 출력하고, `SSOT 충돌 발견: 0건 (SSOT 매칭 파일 0개)` 한 줄을 함께 출력.

### 7.3 출처 list 블록

`## 출처` 블록은 §출력 포맷의 표 그대로 출력한다. 추가 규칙:

- `#` 번호는 본문 합류 순서. 변환 본문에서 `[출처 N]`로 참조. `[출처 0]`은 원본 입력 (URL 분기에서는 별도 행 없이 1번부터 시작).
- `출처 종류`: 7종 — `원본` / `인자 URL` / `추출 URL` / `자식 URL` / `인자 이미지` / `추출 이미지` / `fetch 이미지`.
- `URL/경로 또는 위치` 컬럼 옆 괄호는 추적용 — `(출처: 원본 §line N)` / `(출처: [#K] §line N)` / `(출처: [#K] §img alt)`.
- `상태`: HTTP status (성공) / skip 사유 (`인증 필요`, `content-type <type>`, `빈 본문`, `미지원 이미지 포맷`, `image read 실패`, `빈 해석 결과`, `timeout`, `network error`). 이미지 성공은 `image/<subtype> <bytesize>`.
- `본문 사용`: O/X. 이미지 multimodal 합류는 `O (multimodal)`. 인증·실패는 X. 원본 행은 항상 O.
- 표는 visited 순서 그대로. 정렬 안 함.
- 실패 URL/이미지도 list에 포함 (사용자 추적 가능하도록).

실패 0건이면 표 아래에 `모든 발견 링크·이미지 처리 성공` 한 줄. URL fetch와 이미지 처리가 모두 0건이면 `## 출처` 블록 통째로 생략.

### 7.4 빈 입력 sanity check

```
입력 비어 있음. 기획 초안 텍스트 또는 경로를 인자로 주세요.
```

literal 빈 문자열·whitespace·0byte 파일·완전 비어 있는 디렉터리 + 이미지 시드 0건 + URL 시드 0건일 때만 출력. 그 외 모든 케이스는 §정상 (변환 + 리뷰) 흐름으로 진행.

### 7.5 URL 분기 sanity check

§3.4의 5종 메시지 중 1개를 단독 한 줄로 출력 + 입력 URL list. `## 리뷰 결과` 블록 없음.

### 7.6 `--no-review` 사용 시

`## 리뷰 결과` 섹션 전체 생략. 정책서·기능설계서 본문 + (있다면) 입력 제외 항목 + (있다면) 출처 list만 출력.

### 7.7 `--no-fetch` / `--no-image` 사용 시

해당 종류 시드를 처리하지 않으므로 `## 출처` 블록은 비활성 종류 없이 표시되거나, 모두 비활성이면 블록 통째로 생략. 헤더 `입력 처리` 줄도 disable된 항목은 누락.

## CLI 인자 예시

```
# 단일 URL
/planning-kit:formalize https://example.com/spec/order-cancel

# 다중 URL
/planning-kit:formalize https://a.com/p1 https://b.com/p2 https://c.com/p3

# 이미지 단독
/planning-kit:formalize ./diagrams/order-flow.png

# 디렉터리 (텍스트 + 이미지 혼합)
/planning-kit:formalize ./docs/draft/입고기능/

# 텍스트 + URL 본문 추출
/planning-kit:formalize "주문 취소 정책. 자세한 건 https://wiki.example/order-cancel 참조"

# 옵션 조합
/planning-kit:formalize ./draft/취소정책.md --ssot-include "docs/policy/**/*.md"
/planning-kit:formalize ./draft/입고.md --no-review
/planning-kit:formalize https://example.com/spec --no-fetch    # 인자 URL도 fetch 안 함 (디버그)
/planning-kit:formalize ./docs/draft/ --no-image               # multimodal 호출 0건
```

## 호환성

- 0.1.0 → 0.1.1은 **순수 추가** 변경. 기존 호출은 모두 동일하게 동작.
- 0.1.0에서 URL 문자열을 텍스트 인자로 그대로 넣어 변환했던 경우, 0.1.1에서는 URL 분기로 흘러 fetch가 일어난다. URL을 텍스트로 처리하고 싶다면 따옴표로 감싸 다른 텍스트와 함께 넣거나(`"https://x.com 메모"` → 텍스트 분기) `--no-fetch` 옵션을 사용한다.

## 참고 파일

- `templates/기능설계서.md` — 8 섹션 표 골격.
- `templates/정책서.md` — 10 섹션 표 골격.
- `references/review-rules.md` — 자동 리뷰 2축 점검 기준.
