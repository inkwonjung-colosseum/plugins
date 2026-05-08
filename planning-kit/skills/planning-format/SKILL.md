---
name: planning-format
description: "기획 초안(텍스트·파일·디렉터리·URL·이미지)을 정책서·기능설계서 두 본문으로 변환하고 같은 응답에서 자체 품질 검증까지 출력해야 할 때 사용한다. 외부 SSOT 충돌·acceptance criteria·의존 영향 분석은 planning-review 스킬에서 별도로 수행한다."
argument-hint: "<기획 초안 텍스트 | 파일 | 디렉터리 | URL [URL ...]> [--save] [--no-fetch] [--no-image] [--no-self-review]"
---

# planning-format

## 인자

위치 인자 1개 이상 (필수): 기획 초안 텍스트, 파일 경로, 디렉터리 경로, **1개 이상의 URL** 중 하나.

| 인자 | 기본값 | 설명 |
|---|---|---|
| `--save` | off | `./.planning-kit/<기능명>/정책서.md`, `./.planning-kit/<기능명>/기능설계서.md` 두 파일에 본문 저장. 자체 검증 보고서·출처 list·입력 제외 §은 디스크 저장 안 함 (화면 only). 충돌 시 §8.3. |
| `--no-fetch` | off | URL fetch + connector fallback 봉쇄. |
| `--no-image` | off | 이미지 multimodal 호출 0건. |
| `--no-self-review` | off | 자체 품질 검증 블록 출력 생략. **입력 제외 §은 끄지 않음** — 변환 결과 핵심 정보. |

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

분기 직후 **모든 분기 공통**으로 입력 본문에서 URL·이미지 참조를 추출해 fetch queue + image queue에 시드 (markdown link/autolink, HTML href/src/img, plain URL, markdown image, data URI). self-anchor·`mailto:`/`tel:`/`javascript:`/`blob:`은 제외. `--no-fetch`/`--no-image`면 해당 시드 skip.

### Step 2: 빈 입력 sanity check

통합 본문 0byte + 이미지 시드 0건 + URL 시드 0건이면:

```
입력 비어 있음. 기획 초안 텍스트 또는 경로를 인자로 주세요.
```

URL 분기 sanity check는 §3.4.

### Step 3: 재귀 fetch + connector fallback

#### 3.1 재귀 동작

URL 한 개씩 dequeue → normalize → visited 검사 → §3.2 fetch → 본문 합류 + 자식 URL/이미지 추출 → queue push. depth·pages·body 크기 cap 없음. visited set으로만 cycle 방지. `--no-fetch`면 §3 전체 skip.

#### 3.2 fetch 시퀀스 (URL 1개)

fetch 단계 진입 직전 1회 `references/connector-routing.md`를 Read 적재. 인증 휴리스틱·MCP 카탈로그·호스트 매핑·Google Workspace tool 시퀀스·gid/range·fallback·status 표기·sanity check 메시지 모두 거기에.

1. **WebFetch** 1회 GET (timeout 30초, redirect ≤5).
2. 응답 분류:
   - 200 OK + `text/html|markdown|plain|xhtml` → 의미 있는 본문 영역 추출(`<main>`/`<article>` 우선, navigation·boilerplate 제외) → 합류 (via=WebFetch).
   - 200 OK + `image/*` → image queue (via=WebFetch).
   - 그 외 (지원 안 하는 content-type / 401 / 403 / 인증 게이트 / 4xx / 5xx / timeout / network error) → §3.3 fallback.

#### 3.3 connector fallback

`references/connector-routing.md` 그대로. 매핑 lookup 호스트 = 원 입력 URL 호스트 (redirect 최종 X). connector 응답 본문도 자식 URL 추출해 queue push.

#### 3.4 URL 분기 sanity check

루트 URL **모두** 합류 실패면 호출 종료 (메시지 = `connector-routing.md` §8). 일부 실패면 §출처 list에 사유만. 텍스트·파일·디렉터리 분기는 §2 sanity check만 — 본문 추출 URL fetch 실패해도 원본으로 진행.

### Step 4: 이미지 multimodal 처리

지원 확장자: `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.bmp`, `.heic`, `.svg`. 크기·개수 cap 없음, resize 안 함. `.svg`는 raw XML + multimodal 해석 둘 다 시도.

이미지 시드 5경로: 인자 파일·디렉터리·본문 추출(markdown image / HTML img / 상대 경로 resolve)·fetch image content-type 결과·data URI.

각 이미지에 대해 main이 multimodal 해석 — 안의 텍스트(라벨·캡션) 옮기고 다이어그램·플로우·화면 요소를 글로 기술. 추측은 `추정:` 접두. 결과는 `=== [출처 N] 이미지: <파일명 또는 URL> ===` 헤더와 함께 본문 합류.

실패(`미지원 이미지 포맷`/`image read 실패`/`빈 해석 결과`)는 출처 list에 사유 기록, 호출 종료 사유 아님.

### Step 5: 통합 본문 합류 형식

출처 단위로 `=== [출처 N] <원본 입력 / URL / 이미지 경로> ===` 헤더를 붙여 concat. 텍스트·파일·디렉터리 분기는 원본 입력이 항상 `[출처 0]`. URL 분기는 인자 URL이 `[출처 1..M]`. 자식 URL·이미지 해석은 visited 순서. 출처 헤더 자체는 변환 본문에 들어가지 않는다 (입력 마커일 뿐).

Google Sheets는 `references/connector-routing.md` §3.5 헤더 형식(gid·range 부연) 그대로.

### Step 6: 변환

#### 6.1 기능명 추출

- URL 분기 (단일): 인자 URL의 페이지 `<title>` 또는 첫 `<h1>`.
- URL 분기 (다중): 첫 인자 URL title 우선.
- 텍스트·파일·디렉터리 분기: 입력에 명시된 주제 → 파일명 stem → 디렉터리명 → 본문 반복 제목 → 첫 핵심 명사구.

여러 기능 후보가 있으면 1순위 1개만. 그 외는 입력 제외 추적에 `다른 기능 후보` 사유로.

#### 6.2 두 템플릿 변환

`templates/기능설계서.md` (8 섹션) + `templates/정책서.md` (10 섹션) Read 후 main이 같은 턴에 두 본문 작성.

라벨 매핑:
- 화면·흐름·동작·입력 항목·권한·예외 메시지 → 기능설계서.
- 규칙·조건·예외 승인·역할 책임·상태 전이·연동 정책 → 정책서.

**변환 본문(정책서·기능설계서)에 합류하지 않은 모든 입력 조각**은 §6.3 입력 제외 항목 추적으로 (10 카테고리 중 1개로 라벨링). 라벨 미매핑·중복·범위 외·구조 변환·fetch 실패·원문 정의 부재 등 사유 무관 catch-all. 근거 부족 셀은 inline `[TBD]`. 빈 row·빈 섹션 삭제 허용. **marker는 `[TBD]` 1종만** (`[미정]`/`[가정]`/`[확인 필요]`/`[충돌 후보]`/`해당 없음` 사용 금지).

**list 분해 판단**: 한 셀에 list 항목 ≥2 합류 작성 시, main이 항목별 속성(타입)·동작(클릭/overlay/non-MVP)·정책 ref(§ cross-link)·검증·[TBD]·non-MVP 등 이질성을 평가한다. 이질이면 부모 § 안 sub-§(`### N.x [용도] 보조 표`)로 분해(본 셀엔 `§N.x 참조` 1행만, 컬럼 set은 list 성격에 맞춰 main 결정, 권장 최소 = `순번`·`항목`·`비고`), 동질 enum·동일 동작·동일 ref면 합류 유지. 보조 표 안 셀이 다시 list 합류면 같은 룰 재귀(`§N.x.y`, depth cap 없음). 8/10 섹션 골격은 변경 없고 sub-§만 동적 추가. 판단 형식화(Q-list·체크리스트·카운트 룰) 없음 — main 자유 판단.

#### 6.3 입력 제외 항목 추적 (10 카테고리)

변환 본문(정책서·기능설계서)에 합류하지 않은 모든 입력 조각을 다음 10종 카테고리 중 하나로 라벨링해 입력 제외 §에 기록.

| # | 카테고리 | 정의 |
|---|---|---|
| 1 | `다른 기능 후보` | 기능명 추출 시 1순위 외 후보. 또는 입력에 함께 들어왔지만 별도 기획 대상 |
| 2 | `라벨 미매핑` | 정책서 10 섹션·기능설계서 8 섹션 어디에도 라벨 매핑할 자리가 없음 |
| 3 | `중복` | 같은 사실이 입력에 반복 등장. 한 번만 본문에 합류 |
| 4 | `근거 부족 무시` | 추측·draft 메모·임시 작성으로 본문 신뢰도 떨어뜨림 |
| 5 | `포맷 노이즈` | 인용·꾸밈·자동 metadata·임의 mark-up. 본문 의미 비기여 |
| 6 | `디테일 축약` | 라벨 매핑은 됐으나 본문 디테일 일부가 인접 도메인에 더 가까워 옮기지 않음 |
| 7 | `범위 외` | 정책서 §2 / 기능설계서 §2 제외 범위에 명시된 영역 |
| 8 | `구조 변환` | 의미는 보존되나 원문 표·구조가 분해돼 다른 섹션으로 분산 |
| 9 | `fetch 실패` | 외부 자원(URL·이미지) 본문 미합류. `## 출처` list `본문 사용 = X` 행과 cross-reference |
| 10 | `원문 정의 부재` | 입력 자체가 모호·미정의. 본문은 [TBD] 처리, 미결 §과 cross-reference |

**카테고리 우선순위** (한 항목이 둘 이상에 걸치면 위쪽 1개만):

```
범위 외 > fetch 실패 > 구조 변환 > 디테일 축약 > 원문 정의 부재 >
다른 기능 후보 > 라벨 미매핑 > 중복 > 근거 부족 무시 > 포맷 노이즈
```

경계 처리:
- `fetch 실패`는 입력에서 인용·참조된 자원만. 단순 부수 링크는 출처 list에만.
- `원문 정의 부재`는 입력 측 결손, `라벨 미매핑`은 변환 측 매핑 결손.

#### 6.4 입력 제외 항목 5필드 형식

각 항목:

```markdown
1. [한 줄 제목]
   - 카테고리: [§6.3 10종 중 하나]
   - 위치: [입력 측 위치 — 파일명:라인 / "직접 입력" / "[출처 N] §섹션 또는 줄 N"]
   - 인용: "[입력 원문 ≤80자]"
   - 처리: [§6.5 처리 줄 형식]
   - 설명: [한 줄]
```

#### 6.5 `처리` 줄 형식

| 카테고리 | `처리` 줄 형식 |
|---|---|
| `다른 기능 후보` | `본문 미합류 (별도 기획 대상)` |
| `라벨 미매핑` | `본문 미합류` |
| `중복` | `중복 제거 (1차 합류 위치: 정책서 §N / 기능설계서 §M)` |
| `근거 부족 무시` | `본문 미합류` |
| `포맷 노이즈` | `본문 미합류` |
| `디테일 축약` | `라벨 매핑은 정책서 §N / 기능설계서 §M, 디테일 미합류` |
| `범위 외` | `명시 제외 (정책서 §2 / 기능설계서 §2 참조)` |
| `구조 변환` | `구조 분해 (위치: 정책서 §N1·§N2 / 기능설계서 §M1·§M2)` |
| `fetch 실패` | `본문 미합류 (출처 list #K 참조)` |
| `원문 정의 부재` | `[TBD] 추적 (미결: 정책서 §10 #N / 기능설계서 §8 #M)` |

매핑·합류 위치를 식별 못 하면 `본문 미합류`로 폴백.

### Step 7: 자체 품질 검증

`--no-self-review`면 skip. 그 외엔 `references/self-review-rules.md` 적재 후 6 카테고리(F1 충실도·F2 cross-bleed·F3 용어·F4 정책-기능 매핑·F5 누락·F6 syntax) 단일 패스 점검. F5는 본문 누락 + cross-ref 3종(`cross-ref-fetch`·`cross-ref-scope`·`cross-ref-tbd`) 모두 봄. 기준·예시·발견 형식 모두 reference 그대로.

6 카테고리 모두 0건이면 `통과`, ≥1건이면 `발견 N건`. 외부 corpus·다른 *.md는 보지 않음 (planning-review가 처리).

### Step 8: `--save` 처리

#### 8.1 저장 경로

```
./.planning-kit/<기능명-안전화>/정책서.md
./.planning-kit/<기능명-안전화>/기능설계서.md
```

`## 정책서` / `## 기능설계서` 코드 펜스 안 본문만 추출해 그대로 파일에 쓴다.

#### 8.2 기능명 안전화

1. NFC normalize.
2. 경로 분리자 `/`, `\`, 컨트롤 문자 제거.
3. 양 끝 공백·`.` trim.
4. `..`/`-`로 시작 시 `_` prefix.
5. 64자 초과 시 자름.
6. 결과가 빈 문자열이면 `untitled-<8자 난수 hex>`.

기능명에 영문·한글·숫자·공백·`-`·`_`·괄호·대괄호·`.`·중간 점 등은 그대로 둔다.

#### 8.3 collision

기존 파일 덮어쓰기 안 함. suffix `-2`/`-3`/... 시도. 99까지 모두 충돌이면 `--save` 실패. `--save-overwrite` 같은 강제 옵션은 없음.

```
./.planning-kit/<기능명>/정책서.md         (기존)
./.planning-kit/<기능명>/정책서-2.md       (신규)
```

#### 8.4 저장 실패

본문 변환·자체 검증 결과는 화면에 그대로 출력하고 헤더 `저장:` 줄에 사유 1줄 표시. 호출 종료 사유 아님.

### Step 9: 통합 출력

§출력 포맷에 따라 단일 응답 markdown. 변환 본문 → 출처 → 입력 제외 → 자체 검증 순.

## 출력 포맷

정책서·기능설계서 본문은 ` ```markdown ... ``` ` 코드 펜스로 감싼다.

### 정상 (변환 + 자체 검증)

````markdown
# [기능명]

- 입력 처리: [§7.1 분기별 헤더]
- 출처: [§7.1 출처 줄 — URL 1개일 때만 단일 URL 그대로]
- 미결 표기: [TBD] N개
- 입력 제외: [§7.3 카테고리 분포]
- 저장: [§7.1 저장 줄]

---

## 정책서

```markdown
[10 섹션 + (선택) 보조 표 sub-§ — §6.2 list 분해 판단 결과로 동적 등장]
```

---

## 기능설계서

```markdown
[8 섹션 + (선택) 보조 표 sub-§ — §6.2 list 분해 판단 결과로 동적 등장]
```

---

## 출처

(URL fetch·이미지 처리 1건 이상일 때만)

원본 입력: <"직접 입력" / "파일 N개" / "디렉터리 텍스트 N개" / "URL M개" / "이미지 I개">
재귀 fetch: 성공 N개 / 실패 K개 (cap 없음)

| # | depth | 출처 종류 | URL/경로 또는 위치 | 상태 | 본문 사용 |
|---|---|---|---|---|---|
| 0 | - | 원본 | 직접 입력 / 파일 / 디렉터리 / — | — | O (원본) |
| 1 | 0 | 인자 URL | <Confluence URL> | 200 (via Atlassian MCP) | O |
| 2 | 1 | 자식 URL | <Sheets URL> (출처: [#1] §line N) | 200 (via Google Drive connector — read_file_content) \| 범위 힌트: C13 | O |
| 3 | 1 | 자식 URL | <Google Doc URL> (출처: [#1] §line N) | 인증 필요 (Google Drive connector 미인증) | X |
| 4 | 0 | 인자 이미지 | path/diagram.png | image/png 1.2MB | O (multimodal) |

---

## 입력 제외 항목

(항상 출력. 두 가지 케이스:)

**케이스 A — 0건**:

```
## 입력 제외 항목

없음
```

**케이스 B — ≥1건 (5필드 항목 list)**:

1. [한 줄 제목]
   - 카테고리: [§6.3 10종 중 하나 — 다른 기능 후보 / 라벨 미매핑 / 중복 / 근거 부족 무시 / 포맷 노이즈 / 디테일 축약 / 범위 외 / 구조 변환 / fetch 실패 / 원문 정의 부재]
   - 위치: [파일명:라인 / "직접 입력" / "[출처 N] §섹션 또는 줄 N"]
   - 인용: "[입력 원문 ≤80자]"
   - 처리: [§6.5 처리 줄 형식]
   - 설명: [왜 본문에 안 넣었는지 한 줄]

---

## 자체 검증: [통과 | 발견 N건]

- 충실도: N건
- cross-bleed: N건
- 용어 일관성: N건
- 정책-기능 매핑: N건
- 누락: N건
- syntax: N건

### 발견 사항
(≥1건일 때만)
1. [제목]
   - 카테고리: [충실도 / cross-bleed / 용어 일관성 / 정책-기능 매핑 / 누락 / syntax] (F5 cross-ref면 sub: cross-ref-fetch / cross-ref-scope / cross-ref-tbd)
   - 위치: [정책서/기능설계서 §섹션 또는 line N. cross-ref면 양쪽 위치]
   - 근거: "[변환 본문 인용]"
   - 영향: [한 줄]
   - 제안: [최소 수정 또는 확인 조건]
````

규칙:
- 6 카테고리 모두 0건이면 `## 자체 검증: 통과`로만 + 카운트 줄.
- `## 입력 제외 항목`은 항상 출력 (0건일 때 `없음` 1줄). `--no-self-review`도 본 블록은 끄지 않는다.
- URL fetch + 이미지 모두 0건이면 `## 출처` 통째 생략.
- `--no-self-review`면 `## 자체 검증` 통째 생략.
- 블록 순서: 변환 본문 → 출처 → 입력 제외 → 자체 검증.
- 두 본문 안 `### N.x [용도] 보조 표` sub-§은 §6.2 list 분해 판단 결과로 부모 § 다음 줄에 동적 등장. 8/10 섹션 골격은 변경 없음. 자체 검증·헤더 메타라인은 보조 표 무관.

### 7.1 헤더 줄 형식

**입력 처리 줄**:

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
- `재귀 fetch N개`는 root 외 자식 URL fetch 성공 수. 0건이면 괄호 생략.
- `MCP 경유 K개`는 connector 합류 URL 수 합계. K=0이면 괄호 생략.
- `--no-fetch`/`--no-image`로 disable된 항목은 헤더에서 누락.

**저장 줄**:

| 케이스 | 출력 |
|---|---|
| `--save` off | `- 저장: 화면 only` |
| `--save` 성공 (충돌 없음) | `- 저장: ./.planning-kit/<기능명>/정책서.md, ./.planning-kit/<기능명>/기능설계서.md` |
| `--save` 성공 (충돌 회피) | `- 저장: ./.planning-kit/<기능명>/정책서-2.md, ./.planning-kit/<기능명>/기능설계서-2.md (기존 파일 보존)` |
| `--save` 실패 | `- 저장: 실패 — <사유>. 본문은 화면 only로 반환.` |

### 7.2 출처 list `상태` 컬럼

표기 규칙은 `references/connector-routing.md` §7. 표는 visited 순서. 실패도 list에 포함. 실패 0건이면 표 아래 `모든 발견 링크·이미지 처리 성공` 한 줄.

### 7.3 헤더 `입력 제외` 줄 카테고리 분포

```
- 입력 제외: N건 (다른 후보 K, 라벨 미매핑 L, 중복 M, 근거 부족 P, 포맷 노이즈 Q, 디테일 축약 R, 범위 외 S, 구조 변환 T, fetch 실패 U, 원문 정의 부재 V)
```

규칙:
- 카테고리 카운트가 0인 항목은 괄호에서 누락 (가독성).
- 0건일 때 `- 입력 제외: 없음`.
- 카테고리 라벨은 §6.3 표의 한국어 약형 (`다른 기능 후보` → `다른 후보`, `근거 부족 무시` → `근거 부족`).
- 괄호 안 카운트 합 = N과 일치.

## 참고 파일

- `templates/기능설계서.md` — 8 섹션 표 골격.
- `templates/정책서.md` — 10 섹션 표 골격.
- `references/self-review-rules.md` — 자체 품질 6 카테고리 (F1~F6) 점검 기준.
- `references/connector-routing.md` — 인증 휴리스틱·MCP 카탈로그·호스트 매핑표·Google Workspace tool 시퀀스·gid/range 처리·fallback 케이스 표·sanity check 메시지·status 표기.

외부 검증(SSOT 충돌·acceptance criteria·의존 영향)은 `planning-review` 스킬 별도 호출. 자세한 사용법은 `skills/planning-review/SKILL.md`.
