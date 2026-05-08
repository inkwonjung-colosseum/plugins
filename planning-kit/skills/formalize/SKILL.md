---
name: formalize
description: "기획 초안(텍스트·파일·디렉터리·URL·이미지)을 정책서와 기능설계서 두 본문으로 변환하고 같은 응답에서 자동 리뷰까지 출력해야 할 때 사용한다."
argument-hint: "<기획 초안 텍스트 | 파일 | 디렉터리 | URL [URL ...]> [--ssot-include <glob>] [--no-review] [--no-fetch] [--no-image]"
---

# formalize

기획 초안을 받아 **정책서 + 기능설계서 두 본문**으로 변환하고 **같은 응답에서 자동 리뷰**까지 한 번에 출력한다. 산출물은 화면 output(응답 markdown)으로만 반환하고 **로컬 파일에 저장하지 않는다**.

호출 한 번 = 변환 본문 2개 + 입력 제외 항목 + 출처 list + 리뷰 결과.

## 인자

위치 인자 1개 이상 (필수): 기획 초안 텍스트, 파일 경로, 디렉터리 경로, **1개 이상의 URL** 중 하나.

| 인자 | 기본값 | 설명 |
|---|---|---|
| `--ssot-include <glob>` | (없음) | 리뷰 SSOT corpus glob. default = 프로젝트 폴더 안 모든 `*.md` (`.git/`, `node_modules/` 자동 제외). |
| `--no-review` | off | 리뷰 단계 건너뜀. 변환 본문만 출력. |
| `--no-fetch` | off | URL fetch·connector fallback 모두 봉쇄. 디버그·오프라인용. |
| `--no-image` | off | 이미지 multimodal 호출 0건. |

cap 관련 인자(`--depth`, `--max-pages`, `--max-body`, `--max-image`)는 두지 않는다 — cap 없음 정책(품질·검증 우선).

## 동작 시퀀스

### Step 1: 입력 dispatch

분기 우선순위:

```
1. URL 패턴 (1개 이상 토큰, 모두 https?://) → URL 분기
2. 디렉터리 경로                              → 디렉터리 분기
3. 파일 경로                                  → 파일 분기 (이미지 확장자면 image queue 단독 시드)
4. 그 외                                      → 텍스트 분기
```

URL 토큰과 비-URL 토큰이 섞이면 텍스트 분기. `file://`/`ftp://`/`mailto:`/scheme 없는 입력은 URL 분기 아님.

분기 직후 **모든 분기 공통**으로 입력 본문에서 URL·이미지 참조를 추출해 fetch queue + image queue에 시드한다 (markdown link/autolink, HTML href/src/img, plain URL, markdown image, data URI). self-anchor·`mailto:`/`tel:`/`javascript:`/`blob:`은 제외. `--no-fetch`/`--no-image`면 해당 시드 skip.

### Step 2: 빈 입력 sanity check

통합 본문 0byte + 이미지 시드 0건 + URL 시드 0건이면:

```
입력 비어 있음. 기획 초안 텍스트 또는 경로를 인자로 주세요.
```

URL 분기 sanity check는 §3.4.

### Step 3: 재귀 fetch + connector fallback

#### 3.1 재귀 동작

```
queue = [(url, 0) for url in dedup(seed_urls)]
visited = {}
while queue:
  url, depth = queue.pop_front()
  key = normalize(url)               # fragment·tracking query·trailing slash 정리
  if key in visited: continue
  resp = fetch(url)                  # §3.2 (WebFetch + connector fallback)
  visited[key] = resp
  if resp.body 합류 가능:
    body 합류
    queue.push(child_links(body), depth + 1)   # is_followable: http(s) + visited 미포함
    image_queue.push(child_images(body))
  else if image content-type:
    image_queue.push(bytes)
```

depth·pages·body 크기 cap 없음. visited set만 cycle 방지. `--no-fetch`면 §3 전체 skip (root·자식·connector 모두).

#### 3.2 fetch 시퀀스 (URL 1개)

fetch 단계 진입 직전 1회 `references/connector-routing.md`를 `Read`로 적재 — 인증 게이트 휴리스틱·MCP 카탈로그·호스트 매핑표·런타임 추론·fallback 케이스 표·status 표기·sanity check 메시지가 모두 거기에 있다.

1. **WebFetch** 1회 GET (timeout 30초, redirect ≤5).
2. 응답 분류:
   - 200 OK + `text/html|markdown|plain|xhtml` → 본문 추출 → 합류. via=WebFetch.
   - 200 OK + `image/*` → image queue. via=WebFetch.
   - 그 외 (지원 안 하는 content-type / 401 / 403 / 인증 게이트 휴리스틱 / 4xx / 5xx / timeout / network error) → §3.3 fallback 평가.
3. fallback 결과로 합류 또는 skip.

본문 추출은 `<main>`/`<article>` 우선, 없으면 `<body>`에서 `<nav>`/`<aside>`/`<header>`/`<footer>`/`<script>`/`<style>` 제거. 표·헤딩·리스트 markdown 유지.

#### 3.3 connector fallback

`references/connector-routing.md`의 매핑표·런타임 추론·fallback 케이스 표를 따라 connector tool 후보를 산출하고 시도한다. 각 후보 호출은 timeout 30초, 1회. 결과(합류/skip/사유)는 reference §5 케이스 표 그대로.

매핑 lookup 호스트는 **원래 입력된 URL의 호스트** — redirect 최종 호스트 X. connector 응답 본문도 자식 URL을 추출해 visited queue에 push (reference §6).

#### 3.4 URL 분기 sanity check

루트 URL이 **모두** 본문 합류 실패하면 호출 종료한다. 일부만 실패면 §출처 list에 사유만 기록하고 진행한다. 5종 메시지는 `references/connector-routing.md` §8. sanity check 메시지는 `## 리뷰 결과` 블록 없이 단독 한 줄 + 입력 URL list로 출력.

텍스트·파일·디렉터리 분기는 §2 sanity check만 적용. 본문 추출 URL이 모두 fetch 실패해도 원본 본문으로 변환 진행.

### Step 4: 이미지 multimodal 처리

`--no-image`면 §4 전체 skip.

지원 확장자: `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.bmp`, `.heic`, `.svg`. 크기·개수 cap 없음, resize 안 함. `.svg`는 raw XML도 본문 포함하고 multimodal 해석도 시도.

이미지 시드 5경로: 인자 파일·디렉터리·본문 추출(markdown image / HTML img / 상대 경로 resolve)·fetch image content-type 결과·data URI.

각 이미지에 대해 main이 자기 자신에게 multimodal 해석 요청 — 안의 텍스트(라벨·헤더·캡션)를 그대로 옮기고, 다이어그램·플로우는 노드·간선·열·행으로 재구성, 화면 캡처는 화면 요소·흐름을 글로 기술, 추측은 `추정:` 접두로 명시. 결과는 `=== [출처 N] 이미지: <파일명 또는 URL> ===` 헤더와 함께 본문 합류.

실패는 본문 합류 안 하고 출처 list에 사유 기록 (`미지원 이미지 포맷`/`image read 실패`/`빈 해석 결과`). 이미지 실패는 호출 종료 사유 아님.

multimodal 해석 텍스트도 SSOT 키워드 grep 대상이지만, 환각 가능성 때문에 키워드 list에 image 출처는 별도 표시하지 않는다 (단일 list).

### Step 5: 통합 본문 합류 형식

출처 단위로 `=== [출처 N] <원본 입력 / URL / 이미지 경로> ===` 헤더를 붙여 concat. 텍스트·파일·디렉터리 분기는 원본 입력이 항상 `[출처 0]`. URL 분기는 인자 URL이 `[출처 1..M]`. 자식 URL은 visited 순서대로 그 뒤. 이미지 해석은 URL fetch 본문 다음에 visited 순서. 출처 헤더 자체는 변환 본문에 들어가지 않는다 (입력 마커일 뿐).

### Step 6: 변환·리뷰

#### 6.1 기능명 추출

- URL 분기 (단일): 인자 URL의 페이지 `<title>` 또는 첫 `<h1>`.
- URL 분기 (다중): 첫 인자 URL title 우선.
- 텍스트·파일·디렉터리 분기: 입력에 명시된 주제 → 파일명 stem → 디렉터리명 → 본문 반복 제목 → 첫 핵심 명사구.

여러 기능 후보가 있으면 1순위 1개만. 그 외는 입력 제외 추적에 `다른 기능 후보` 사유로.

#### 6.2 두 템플릿 변환 (항상 실행)

`templates/기능설계서.md` (8 섹션) + `templates/정책서.md` (10 섹션) 병렬 `Read`. main이 같은 턴에서 두 본문 작성.

라벨 매핑:
- 화면·흐름·동작·입력 항목·권한·예외 메시지 → 기능설계서.
- 규칙·조건·예외 승인·역할 책임·상태 전이·연동 정책 → 정책서.

라벨 매핑 안 되는 조각·중복·단편적이라 [TBD]로도 못 채우는 조각은 입력 제외 추적으로. 근거 부족 셀은 inline `[TBD]`. 빈 row·빈 섹션 삭제 허용. marker는 `[TBD]` 1종만 (`[미정]`/`[가정]`/`[확인 필요]`/`[충돌 후보]`/`해당 없음` 사용 금지). **파일 저장 안 함**.

#### 6.3 자동 리뷰 (`--no-review` 아닐 때)

`references/review-rules.md` 읽고 2축 기준 확정 후 main이 단일 패스 점검:

- **A. 자체 품질**: 충실도·라벨 cross-bleed·용어 일관성·정책-기능 매핑·누락. 기준은 `review-rules.md` §A.
- **B. SSOT 충돌**: 변환 본문에서 키워드 추출 → §7.2 헤더에 그대로 노출 → `--ssot-include` glob 또는 프로젝트 폴더 전체 `*.md` (외부 fetch 본문 제외)에서 `grep -l`/`rg -l` 매칭 → 매칭 ≥1건이면 `Read`로 비교해 충돌 list화. 매칭 0건이면 B축 `검증 대상 없음`.

자체 품질 + SSOT 충돌 모두 0건 → `통과`. 어느 한쪽이라도 ≥1건 → `발견 N건`.

§3.3 결과 인증 미연결로 skip된 자식 URL이 있으면, 자체 품질 발견의 영향 줄에 그 사실을 한 줄로 부연 권장 (예: `영향: Figma 자식 1개가 미인증으로 합류 누락. 합류 후 재검토 필요할 수 있음.`).

### Step 7: 통합 출력 (화면 output only)

§출력 포맷에 따라 단일 응답 markdown 1개. 변환 본문 2개 + 출처 list(있을 때) + 입력 제외 항목(있을 때) + 리뷰 결과(`--no-review` 아닐 때) 순.

## 출력 포맷

정책서·기능설계서 본문은 ` ```markdown ... ``` ` 코드 펜스로 감싼다.

### 정상 (변환 + 리뷰)

````markdown
# [기능명]

- 입력 처리: [§7.1 분기별 헤더]
- 출처: [§7.1 출처 줄 — URL 1개일 때만 단일 URL 그대로]
- 미결 표기: [TBD] N개
- 입력 제외: N건 (0건이면 "없음")

---

## 정책서

```markdown
[10 섹션]
```

---

## 기능설계서

```markdown
[8 섹션]
```

---

## 출처

(URL fetch·이미지 처리 1건 이상일 때만. 둘 다 0건이면 블록 통째로 생략.)

원본 입력: <"직접 입력" / "파일 N개" / "디렉터리 텍스트 N개" / "URL M개" / "이미지 I개">
재귀 fetch: 성공 N개 / 실패 K개 (cap 없음)

| # | depth | 출처 종류 | URL/경로 또는 위치 | 상태 | 본문 사용 |
|---|---|---|---|---|---|
| 0 | - | 원본 | 직접 입력 / 파일 / 디렉터리 / — | — | O (원본) |
| 1 | 0 | 인자 URL | <Confluence URL> | 200 (via Atlassian MCP) | O |
| 2 | 1 | 자식 URL | <Figma URL> (출처: [#1] §line N) | 200 (via Figma MCP) | O |
| 3 | 1 | 자식 URL | <Google Doc URL> (출처: [#1] §line N) | 인증 필요 (Google Drive connector 미인증) | X |
| 4 | 0 | 추출 URL | <공개 URL> (출처: 원본 §line N) | 200 (via WebFetch) | O |
| 5 | 0 | 인자 이미지 | path/diagram.png | image/png 1.2MB | O (multimodal) |
| 6 | 1 | fetch 이미지 | <URL> (출처: [#1] §img alt) | image/webp 800KB (via Figma MCP) | O (multimodal) |
| 7 | 2 | 자식 URL | <URL> | content-type video/mp4 | X |

---

## 입력 제외 항목

(≥1건일 때만)

1. [한 줄 제목]
   - 사유: [다른 기능 후보 / 라벨 미매핑 / 중복 / 근거 부족 무시 / 포맷 노이즈]
   - 위치: [파일명:라인 / "직접 입력" / "[출처 N] §섹션 또는 줄 N"]
   - 인용: "[입력 원문 ≤80자]"
   - 설명: [왜 본문에 안 넣었는지 한 줄]

---

## 리뷰 결과: [통과 | 발견 N건]

- 자체 품질 발견: N건
- SSOT 검색 키워드: [keyword1, keyword2, ...]
- SSOT 충돌 발견: N건 (SSOT 매칭 파일 N개)

### 자체 품질 (Self-Review)
(≥1건일 때만)
1. [제목]
   - 카테고리: [충실도 / cross-bleed / 용어 일관성 / 정책-기능 매핑 / 누락]
   - 위치: [정책서/기능설계서 §섹션]
   - 근거: "[변환 본문 인용]"
   - 영향: [한 줄]
   - 제안: [최소 수정 또는 확인 조건]

### SSOT 충돌
(≥1건일 때만)
1. [제목]
   - 위치: [정책서/기능설계서 §섹션] vs [SSOT 파일 §섹션]
   - 근거: "[변환 본문 인용]" vs "[SSOT 인용]"
   - 영향: [한 줄]
   - 제안: [최소 수정 또는 확인 조건]
````

규칙:
- 자체 품질·SSOT 충돌 모두 0건이면 `## 리뷰 결과: 통과`로만. 단, `SSOT 검색 키워드`·카운트 줄은 그대로 출력.
- 입력 제외 0건이면 섹션 통째 생략. URL fetch + 이미지 모두 0건이면 `## 출처` 통째 생략.
- 블록 순서: 변환 본문 → 출처 → 입력 제외 → 리뷰 결과.

### 7.1 헤더 — 입력 처리 줄

```
URL 분기 (단일):           - 입력 처리: URL 1개 + 재귀 fetch N개 (MCP 경유 K개)
                          - 출처: <인자 URL>
URL 분기 (다중):           - 입력 처리: URL M개 + 재귀 fetch N개 (MCP 경유 K개)
                          - 출처: M개 (전체 list는 ## 출처 블록 참조)
텍스트/파일/디렉터리 + URL 추출: - 입력 처리: <원본 형태> + 추출 URL M개 (재귀 fetch N개) (MCP 경유 K개) + 이미지 I개
이미지 단독 인자:           - 입력 처리: 이미지 1개
URL·이미지 0건:            - 입력 처리: 직접 입력 / 파일 K개 / 디렉터리 텍스트 K개
```

규칙:
- `재귀 fetch N개`는 root 외 자식 URL fetch 성공 수. fetch 0건이면 괄호 자체 생략.
- `MCP 경유 K개`는 connector를 통해 합류된 URL 수 합계. K=0이면 괄호 생략.
- `--no-fetch`/`--no-image`로 disable된 항목은 헤더에서 누락.

### 7.2 출처 list `상태` 컬럼

표기 규칙은 `references/connector-routing.md` §7. 표는 visited 순서. 실패도 list에 포함. 실패 0건이면 표 아래 `모든 발견 링크·이미지 처리 성공` 한 줄.

### 7.3 sanity check·옵션 출력

- 빈 입력 sanity check (§2): `입력 비어 있음. 기획 초안 텍스트 또는 경로를 인자로 주세요.` 한 줄.
- URL 분기 sanity check (§3.4): `references/connector-routing.md` §8 5종 메시지 중 1개 + 입력 URL list. `## 리뷰 결과` 블록 없음.
- `--no-review`: `## 리뷰 결과` 통째 생략.
- `--no-fetch`/`--no-image`: 비활성 항목은 헤더·출처 list에서 누락. 모두 비활성이면 `## 출처` 통째 생략.

## 참고 파일

- `templates/기능설계서.md` — 8 섹션 표 골격.
- `templates/정책서.md` — 10 섹션 표 골격.
- `references/review-rules.md` — 자동 리뷰 2축 점검 기준.
- `references/connector-routing.md` — 인증 게이트 휴리스틱·MCP 카탈로그·호스트 매핑표·fallback 케이스 표·sanity check 메시지·status 표기.
