# planning-kit PRD 0.2.2

> 0.2.1 기반 incremental PRD. 두 갈래 변경 — (1) `planning-review` R1 SSOT corpus가 매칭된 `*.md` 본문 안 외부 URL을 자동으로 따라가 corpus에 합류시키도록 확장, (2) 0.2.1 release 후 발견된 4종 일관성 갭 fix. 본 PRD에서 다루지 않는 명세(스킬 분할·자체 검증·입력 제외·재귀 fetch·이미지 multimodal 등)는 [`prd-0.2.1.md`](./prd-0.2.1.md), [`prd-0.2.0.md`](./prd-0.2.0.md), [`prd-0.1.2.md`](./prd-0.1.2.md), [`prd-0.1.1.md`](./prd-0.1.1.md), [`prd-0.1.0.md`](./prd-0.1.0.md)를 그대로 따른다.

## 1. 변경 요약

다섯 가지 변경:

1. **R1 SSOT corpus link follow** — `planning-review` R1이 매칭된 `*.md` 파일을 Read한 뒤, 본문 안 외부 URL을 추출해 fetch + connector fallback으로 corpus body에 합류시킨다. `planning-format` §3·§4(재귀 fetch + connector + 이미지 multimodal) 절차를 그대로 공유. 봉쇄 옵션 `--no-ssot-fetch` / `--no-ssot-image` 신설.
2. **planning-review가 0.2.1 입력 제외 § 인지** — `planning-format` 산출물(또는 동등 markdown)을 받을 때 `## 입력 제외 항목` 블록을 자동 분리해 R3 영향 후보 산출의 보조 신호로 활용. `fetch 실패` / `범위 외` / `원문 정의 부재` 카테고리는 R3 영향 후보 추가 신호, `다른 기능 후보` / `라벨 미매핑` / `중복` / `근거 부족 무시` / `포맷 노이즈`는 R3와 무관(noise). `구조 변환` / `디테일 축약`은 R3 영향 후보 약신호로 권고 분류.
3. **Codex plugin.json longDescription 압축** — 0.2.1에서 한 줄이 매우 길어져 display 환경에서 잘릴 위험. 핵심 1줄 + 신규 변경 5종 압축으로 정리.
4. **README 비교 표 0.2.1·0.2.2 갱신** — `product-team-kit`과의 차이 표에서 입력 제외 §·자체 검증 F5 cross-ref·R1 link follow 항목 row를 명시. 일부 row는 0.2.1·0.2.2 영향 반영.
5. **PRD chain 안내** — `docs/prd/README.md` 신규 생성. 0.1.0부터 0.2.2까지의 PRD 관계(breaking·incremental)·읽는 순서·핵심 변경 1줄 요약을 한 문서로 가이드.

이 다섯 변경은 (1) `planning-review` 동작 확장 + (2~5) 문서·메타 일관성 보강. `planning-format` 동작·인자·출력은 변경 없음.

## 2. 동기

### 2.1 R1 SSOT corpus link follow

0.2.1 release 운영 중 다음 패턴 발견:

- 사내 `*.md` SSOT 문서가 정책 본문을 외부 위키(Confluence·Notion·Google Docs)에 두고 본문에는 link 1~2줄만 두는 경우가 많다.
- 현재 R1은 `*.md` 파일 본문만 grep + Read. 외부 link는 무시 → "정책서가 외부 위키 X와 충돌" 같은 발견을 잡지 못한다.
- planning-format은 입력 본문 안 URL을 재귀 fetch + connector fallback (cap 없음)으로 합류한다. 같은 입력을 review 단계에서는 외부 본문이 corpus에 없는 비대칭.
- 결과: 사용자가 "왜 review에서 외부 위키 충돌을 못 잡았냐"를 묻는다.

### 2.2 0.2.1 잔여 일관성 갭

0.2.1 PRD release 후 review 시 4종 갭 발견:

- **Gap 1 — planning-review 입력 제외 § 처리 부재**: 0.2.1부터 산출물에 `## 입력 제외 항목` 블록이 항상 등장. 그러나 `planning-review` SKILL.md에 본 블록 처리 명시 없음. 입력 분리(`# 정책서` / `# 기능설계서`) 단계에서 입력 제외 §은 무시되는데, 그 안에는 R3 영향 후보 산출에 보조 신호가 될 수 있는 정보(`fetch 실패`로 누락된 외부 자원, `범위 외`로 인근 도메인 영향)가 있다.
- **Gap 2 — Codex plugin.json longDescription 길이**: 0.2.1에서 longDescription이 한 줄로 매우 길어져 (~700자) 일부 display 환경에서 잘림.
- **Gap 3 — README 비교 표 0.2.1 변경 일부만 반영**: `출력 템플릿` row만 갱신. `리뷰 worker`·`marker`·`출력 구조`·`SSOT corpus 처리` 등은 0.2.1 영향 점검 없이 0.2.0 상태.
- **Gap 4 — PRD chain 안내 부재**: PRD 5건(0.1.0/0.1.1/0.1.2/0.2.0/0.2.1)이 누적되었으나 어느 PRD부터 읽어야 하는지·관계가 어떻게 되는지 가이드 부재. 신규 사용자가 0.2.1만 읽으면 "0.2.0 그대로 따른다"는 본문을 만나 chain 추적이 필요하다.

## 3. 비목표

- `planning-format`의 입력 처리·재귀 fetch·connector fallback·이미지 multimodal·자체 검증·입력 제외 §·`--save` 동작은 변경하지 않는다.
- R1 link follow가 planning-format의 재귀 fetch와 같은 캐시를 공유하지 않는다. 두 호출은 독립 — `planning-format` 호출에서 fetch한 본문이 같은 conversation의 `planning-review` 호출에서 자동 재사용되지 않음 (호출 간 캐시는 후속 PRD).
- R1 link follow는 corpus *.md 본문 안에서 발견된 link만 대상. R1이 fetch한 본문에서 발견된 자식 link는 cycle 방지 set으로만 제어 (cap 없음 정책 그대로).
- R3은 R1 corpus를 공유하지만 link follow 결과를 R3 "외부 의존" sub-category 점검 대상으로 자동 변환하지는 않는다. R3 점검은 deps-rules.md 그대로 — link follow가 corpus에 합류한 본문도 deps-rules R3 절차를 그대로 적용.
- `planning-review`가 입력 제외 § 분리 결과를 자체 검증 점검 대상으로 삼지는 않는다 (planning-format이 처리). R3 영향 후보 산출 보조 신호로만.
- 두 스킬 chain helper·매크로·자동 호출은 도입하지 않는다 (0.2.0 §3 비목표 그대로).
- product-team-kit의 outputRoot·CLAUDE.md upsert·gate-first는 도입하지 않는다.
- 0.2.2도 화면 output default. `planning-review`에 `--save` 옵션 도입하지 않는다.

## 4. R1 SSOT corpus link follow

### 4.1 동작 시퀀스 (R1 보강)

기존 R1.1 절차에 link follow 단계 추가. `planning-format` §3·§4와 동일한 절차.

```
1. 변환 본문에서 키워드 추출 (기존, ssot-rules.md R1.1 그대로).
2. 프로젝트 폴더 *.md grep 매칭 → 매칭 file list 확정 (기존).
3. 매칭 file을 Read (기존).
4. (신규) 각 매칭 file 본문에서 URL·이미지 참조 추출 — markdown link / autolink / HTML href·src·img / plain URL / markdown image / data URI.
5. (신규) 추출된 URL을 fetch queue에 시드, 이미지를 image queue에 시드. self-anchor·mailto:/tel:/javascript:/blob: 제외.
6. (신규) 재귀 fetch + connector fallback — `references/connector-routing.md`(planning-format에서 공유) 그대로 사용. WebFetch → 인증 게이트 휴리스틱 → MCP/connector 매핑 → 호스트별 tool 시퀀스 → fallback 케이스 표 → status 표기.
7. (신규) 이미지 multimodal 해석 — 지원 확장자·5 시드 경로·해석 프롬프트는 planning-format §4 그대로.
8. (신규) 외부 fetch 본문 + 이미지 해석 결과를 corpus body에 합류. visited set으로 cycle 방지. cap 없음.
9. corpus 본문 = (3) 매칭 *.md + (8) 외부 fetch 본문 + 이미지 해석.
10. R1 비교 — 변환 본문 확정 문장과 corpus 본문 직접 비교 (기존).
```

### 4.2 fetch queue 시드 형식

매칭 file이 `./docs/policy/order.md`이고 본문에 `자세한 내용은 https://wiki.example/policy/order-cancel 참조` 줄이 있으면:

```
seed_urls = [
  ("https://wiki.example/policy/order-cancel", origin="./docs/policy/order.md", line=N),
]
```

origin·line 필드는 §4.7 출처 list 표기에만 사용. fetch 동작 자체는 planning-format §3 그대로.

### 4.3 connector-routing.md 공유

`skills/planning-review/`는 `connector-routing.md`를 직접 보유하지 않고 `planning-format/references/connector-routing.md`를 그대로 공유 적재. 두 스킬이 같은 lookup data 사용.

planning-review SKILL.md는 fetch 진입 직전 1회 `../planning-format/references/connector-routing.md`를 Read 적재. 인증 휴리스틱·MCP 카탈로그·호스트 매핑표·Google Workspace tool 시퀀스·gid/range 처리·fallback 케이스 표·status 표기·sanity check 메시지가 모두 거기에 있다.

플러그인 구조상 같은 디렉터리 트리에 있어 상대 path로 접근 가능. 별도 reference 파일을 복제하지 않는다.

### 4.4 cycle·중복 방지

- visited set: SSOT corpus의 URL normalize key 집합. URL normalize는 `connector-routing.md` §6 / 0.1.1 PRD §4.7.4 그대로 — fragment 제거·trailing `/`·트래킹 query 제거·호스트 lowercase·query 키 정렬.
- visited set은 한 호출 내에서만 유효. planning-format 호출의 visited set과 별도. 호출 간 캐시는 두 스킬 모두 도입하지 않음 (후속 PRD).
- 같은 URL이 여러 매칭 *.md에서 발견되면 1번만 fetch + 본문 합류. 출처 list에는 origin file 1번만 표시 (첫 발견).
- 매칭 *.md 자체 본문은 cycle 방지 대상 아님 (이미 corpus). 매칭 *.md를 follow URL이 가리키는 자기 자신은 skip — 같은 호스트의 markdown 파일은 보통 외부 wiki라 self-reference 가능성 낮으나 dedup 강화 비목표.

### 4.5 트리거 조건 + sanity check

#### 4.5.1 link follow 트리거

- **R1 활성 OR R3 활성** 시 link follow 진입 (둘 중 하나라도 활성이면 corpus 확장 효과 발생).
- 매칭 file 0건이면 corpus 자체가 없으므로 link follow 진입 의미 없음 → skip.
- R1·R3 모두 비활성(`--axes ac`만) → link follow 진입 안 함.
- `--no-ssot-fetch` ON → R1·R3 활성 무관 link follow 봉쇄.

R1 단독 활성·R3 단독 활성·둘 다 활성 모두 같은 link follow 단계 사용. corpus는 단일 set이라 어느 축이 트리거해도 양쪽이 같은 corpus를 본다.

#### 4.5.2 sanity check

- 매칭 file 1건 이상 + link 0건 → 정상. corpus는 매칭 file 본문만.
- 매칭 file 1건 이상 + link N건 + fetch 모두 실패 → 정상 (corpus는 매칭 file 본문만, 출처 list에 사유). R1·R3 점검 진행.
- 매칭 file 0건 → 0.2.0 R1.2 그대로 (`검증 대상 없음`). link follow 단계 진입 자체 없음.
- 외부 fetch 결과가 image content-type → planning-format §4와 동일하게 image queue로 라우팅, multimodal 해석.

루트 매칭 file이 모두 비어 있어도 호출 종료 안 함. R2는 별도 진행 (R2는 corpus 무관).

### 4.6 옵션 신규

| 옵션 | 기본값 | 설명 |
|---|---|---|
| `--no-ssot-fetch` | off (즉 link follow 활성) | SSOT corpus *.md 본문 안 외부 URL fetch + connector fallback 봉쇄. 매칭 file 본문만 corpus에 들어간다. |
| `--no-ssot-image` | off (즉 image multimodal 활성) | SSOT corpus 본문 안 이미지 참조·fetch image content-type 응답 multimodal 호출 0건. URL fetch는 그대로 (`--no-ssot-fetch`와 독립). |

`planning-format`의 `--no-fetch` / `--no-image`와 의미가 비슷하지만 대상이 다름 — planning-format은 입력 본문, planning-review는 SSOT corpus 본문. 사용자가 헷갈리지 않도록 옵션 이름 분리.

### 4.7 출처 list 신설

link follow를 1건 이상 진행한 호출에서만 출처 list block 출력 (R1 또는 R3 트리거 무관). R1·R3 모두 비활성·매칭 0건·`--no-ssot-fetch`·link 0건이면 통째 생략.

```markdown
## SSOT 출처

매칭 *.md: N개
재귀 fetch: 성공 K개 / 실패 J개 (cap 없음)

| # | 출처 종류 | URL/경로 | origin (.md file:line) | 상태 | 본문 사용 |
|---|---|---|---|---|---|
| 1 | 매칭 *.md | ./docs/policy/order.md | — | — | O |
| 2 | 자식 URL | https://wiki.example/policy/order-cancel | ./docs/policy/order.md:42 | 200 (via WebFetch) | O |
| 3 | 자식 URL | https://confluence.example/wiki/spaces/POL/pages/123 | ./docs/policy/order.md:58 | 200 (via Atlassian MCP) | O |
| 4 | 자식 이미지 | path/diagram.png | ./docs/policy/order.md:71 | image/png 0.4MB | O (multimodal) |
| 5 | 자식 URL | https://docs.google.com/.../edit?gid=... | ./docs/policy/order.md:88 | 인증 필요 (Google Drive connector 미인증) | X |
```

규칙:
- `매칭 *.md` 행은 항상 origin·상태 컬럼이 `—` (1차 corpus, fetch 안 함).
- `자식 URL` / `자식 이미지` 행은 origin 컬럼에 발견 위치 표시.
- 상태 표기는 `connector-routing.md` §7 그대로.
- 실패 행도 list 포함. 실패 0건이면 표 아래 `모든 corpus 외부 링크 처리 성공` 한 줄.

### 4.8 R3 영향 — corpus 확장 효과

R3은 R1 corpus를 공유. R3 단독 활성(`--axes deps`)에서도 R3 트리거로 link follow 진입 (§4.5.1) → corpus가 *.md + 외부 fetch 본문으로 확장.

단 link follow가 가져온 외부 fetch 본문을 **자동으로** R3 "외부 의존" sub-category 영향 후보로 분류하지는 않는다. R3 deps-rules.md §R3.1 외부 의존 절차를 그대로 적용 — fetch 본문 안 도메인 stem이 변환 본문 정책과 충돌·일치하면 deps 발견·권고로 분류. R3 점검 절차 자체는 변경 없음.

결과적으로 R3 비교 대상 자체가 늘어나 R3 발견·권고 카운트가 0.2.1 대비 증가할 가능성.

## 5. 0.2.1 잔여 일관성 갭 4종 fix

### 5.1 Gap 1: planning-review가 0.2.1 입력 제외 § 인지

본 갭 fix는 3 단계 분리 — **분리** / **헤더 표기** / **R3 보조 신호 적용**. 트리거 조건이 다르다:

| 단계 | 트리거 |
|---|---|
| 5.1.1 분리 | 항상 (입력 dispatch). R3 활성 무관. |
| 5.1.3 헤더 표기 | 분리 성공 시 항상. R3 활성 무관. |
| 5.1.2 R3 보조 신호 적용 | 분리 성공 + R3 활성 시. |

#### 5.1.1 분리 단계 추가 (항상)

`planning-review` Step 1 입력 dispatch에서 본문 분리 시:

- 정책서 / 기능설계서 두 본문 + (신규) `## 입력 제외 항목` 블록을 함께 인식.
- 분리 우선순위:
  1. `# 정책서` / `## 정책서` 헤더 → 정책서 본문.
  2. `# 기능설계서` / `## 기능설계서` 헤더 → 기능설계서 본문.
  3. (신규) `## 입력 제외 항목` 헤더 → 입력 제외 § 본문.
  4. 위 3종 중 정책서·기능설계서가 둘 다 매칭 안 되면 sanity check (입력 제외 §은 옵션).

입력 제외 §이 부재해도 sanity check 아님 (0.2.0 산출물 호환). 분리 결과는 메모리에만 — `--axes` 활성 무관 분리 단계는 항상 시도.

#### 5.1.2 R3 보조 신호로 활용 (R3 활성 + 분리 성공 시)

R3 deps-rules.md §R3.1 영향 후보 산출에서 입력 제외 § 카테고리별로 보조 신호 가중치 부여. R3 비활성이면 본 단계 skip:

| 입력 제외 카테고리 | R3 처리 | 헤더 카운트 포함 여부 |
|---|---|---|
| `fetch 실패` | 영향 후보 추가 신호 — 해당 외부 자원이 미합류라 정책 충돌 가능성. R3 "외부 의존" sub-category로 권고. | O |
| `범위 외` | 인근 도메인 영향 후보 약신호. 같은 도메인 stem grep 매칭 file이 있으면 R3 "정책 변경" sub-category로 권고. | O |
| `구조 변환` | 분해 위치(처리 줄) 참조. 분해된 §1·§2가 SSOT 다른 file과 매칭되면 R3 약신호로 권고. | O |
| `디테일 축약` | 인접 도메인 라벨이 다른 SSOT file과 매칭되면 R3 약신호로 권고. | O |
| `원문 정의 부재` | 미결 [TBD] 항목과 cross-reference. R3 영향 후보 강화 안 함 (충돌 단정 불가). 발견·권고 모두 안 만들고 R3 corpus 매칭에서 제외. | **X** (R3 영향 없음 — 헤더 카운트에서도 제외) |
| `다른 기능 후보` / `라벨 미매핑` / `중복` / `근거 부족 무시` / `포맷 노이즈` | 무시 (R3 신호 아님). | X |

**도메인 stem grep 기준**: R1.1 키워드 set (변환 본문 추출 키워드) + 입력 제외 § 항목 본문에서 추가 추출한 stem. 두 set의 합집합으로 grep.

**R3 신호로 만든 항목 분류**: 단정 충돌 단서 없으므로 default `권고` 분류 (deps-rules.md §R3.3에서 `발견`은 단정 충돌, `권고`는 검토 권장).

**신호 강도** — `fetch 실패` > `범위 외` > `구조 변환` ≈ `디테일 축약`.

#### 5.1.3 출력 반영 (분리 성공 시 항상)

`planning-review` 출력 헤더에 입력 제외 § 인지 표기:

```
- 입력: [경로 list / "직전 planning-format 출력 (conversation)" / "직접 입력 markdown"]
- 입력 제외 §: 분리 N건 (R3 신호 K건: fetch 실패 a, 범위 외 b, 구조 변환 c, 디테일 축약 d / R3 무관 N-K건)
```

규칙:
- N = 입력 제외 § 전체 항목 수 (10 카테고리 합).
- K = R3 신호 카테고리 카운트 합 (fetch 실패 + 범위 외 + 구조 변환 + 디테일 축약). `원문 정의 부재`·R3 무관 5종은 K에 포함 안 함.
- `R3 무관 N-K건`은 `원문 정의 부재` + `다른 기능 후보` / `라벨 미매핑` / `중복` / `근거 부족 무시` / `포맷 노이즈` 합계. 카테고리별 분포는 입력 제외 §의 헤더(planning-format)에 이미 있으므로 review 헤더에선 합계만.
- R3 비활성이면 K건은 표기는 하되 R3 점검에 적용 안 됨 (보조 신호 단계 skip).
- 분리 실패 또는 0.2.0 이전 산출물(블록 부재) → `- 입력 제외 §: 없음 (또는 0.2.0 이전 산출물)` 1줄.
- 분리 성공 + 0건 (`없음` 본문) → `- 입력 제외 §: 분리 0건`.

### 5.2 Gap 2: Codex plugin.json longDescription 압축

현재 (0.2.1):

> 두 스킬 분리 구조. planning-format은 텍스트·파일·디렉터리·URL(다중)·이미지 입력을 ... [~700자]

목표 (0.2.2): ≤300자, 핵심 1줄 + 신규 5변경 압축.

```
두 스킬 분리(planning-format 변환+자체 검증 / planning-review 외부 SSOT·AC·의존 영향 3축). 텍스트·파일·디렉터리·URL(다중)·이미지 입력을 정책서·기능설계서 두 본문으로 변환하고 입력 제외 §은 항상 출력. 0.2.2부터 review가 SSOT *.md 안 외부 링크도 재귀 fetch해 corpus에 합류시킨다. Atlassian·Figma·Google Workspace·Slack·Notion connector fallback 지원.
```

shortDescription·developerName·brandColor 등은 변경 없음.

### 5.3 Gap 3: README 비교 표 0.2.1·0.2.2 갱신

`product-team-kit`과의 차이 표(`README.md` line 225~)에서 다음 row 갱신·추가:

| row | 0.2.1 상태 | 0.2.2 갱신 |
|---|---|---|
| 리뷰 축 | "자체 6 카테고리 + 외부 3축" | "자체 6 카테고리 (F5 cross-ref 3종 포함) + 외부 3축 (R1 corpus link follow 포함)" |
| 출력 템플릿 | "5종 ... 입력 제외 § 항상 출력" | 그대로 |
| 입력 제외 처리 (신규 row) | (없음) | "10 카테고리 + 처리 줄 + R3 보조 신호" |
| SSOT corpus 처리 | "grep 매칭 후 직접 read" | "grep 매칭 + 직접 read + 매칭 file 본문 안 외부 링크 재귀 fetch (cap 없음, connector fallback)" |
| 진행 표시 | "자유" | 그대로 |

비교 표 머리 줄도 `planning-kit (0.2.2)`로 갱신.

### 5.4 Gap 4: PRD chain 안내

`docs/prd/README.md` 신규 생성. 내용:

- PRD 5건의 관계 (breaking·incremental·base) 1줄 요약.
- 읽는 순서 가이드 — 신규 사용자는 0.2.2부터 역방향, 기존 사용자는 marginal 변경만.
- 각 PRD 파일별 핵심 변경 1줄.
- 호환성 요약 (0.1.x → 0.2.0 breaking, 그 외 incremental).

### 5.4.1 docs/prd/README.md 골격

```markdown
# planning-kit PRD chain

## 읽는 순서

신규 사용자: 본 README → 0.2.2 → (필요 시) 역방향.
기존 사용자: 신규 PRD만 읽으면 충분 — 각 PRD가 incremental 베이스를 명시.

## PRD 관계도

| PRD | 관계 | 베이스 | 핵심 변경 (1줄) |
|---|---|---|---|
| 0.1.0 | base | (없음) | formalize 단일 스킬 — 텍스트·파일·디렉터리 입력 → 정책서·기능설계서 변환 + 자동 리뷰 (A·B축) |
| 0.1.1 | incremental | 0.1.0 | URL 분기·재귀 fetch·이미지 multimodal·SSOT 검색 키워드 노출 |
| 0.1.2 | incremental | 0.1.1 | connector fallback (Atlassian·Figma·Slack·Notion) + 인증 게이트 휴리스틱 |
| 0.2.0 | **breaking** | 0.1.2 | formalize 분할 → planning-format + planning-review. F6 markdown lint 추가. --save 옵션. Google Workspace 자원별 tool 시퀀스 |
| 0.2.1 | incremental | 0.2.0 | 입력 제외 § 카테고리 5 → 10종 + 항상 출력 + 처리 줄 + 헤더 분포 + F5 cross-ref 3종 |
| 0.2.2 | incremental | 0.2.1 | R1 SSOT corpus link follow + planning-review 입력 제외 § 인지 + Codex desc 압축 + README 비교표 갱신 + PRD chain 안내 |

## 호환성 요약

- 0.1.x → 0.2.0: **breaking** (스킬 이름 변경 + 분할).
- 그 외: incremental, 출력 markdown micro-breaking 가능.
```

## 6. 인자 (planning-review)

기존 (0.2.1):

| 인자 | 기본값 | 설명 |
|---|---|---|
| `--ssot-include <glob>` | (없음) | SSOT corpus glob. R1·R3 공유. |
| `--axes <list>` | `ssot,ac,deps` | 점검 축. |

신규 (0.2.2):

| 인자 | 기본값 | 설명 |
|---|---|---|
| `--no-ssot-fetch` | off | SSOT corpus *.md 본문 안 외부 URL fetch + connector fallback 봉쇄. 매칭 file 본문만 corpus. |
| `--no-ssot-image` | off | SSOT corpus 본문 안 이미지 참조·fetch image content-type 응답 multimodal 호출 0건. URL fetch는 별도 (`--no-ssot-fetch`로 봉쇄). |

`planning-format`은 인자 변경 없음.

## 7. 출력 변경

### 7.1 planning-review 헤더

기존 (0.2.1):

```
# planning-review: [기능명]

- 입력: [경로 list / "직전 planning-format 출력 (conversation)" / "직접 입력 markdown"]
- 점검 축: [ssot, ac, deps]
- SSOT corpus: [매칭 N개 / 매칭 0개 (검증 대상 없음)]
- SSOT 검색 키워드: [keyword1, keyword2, ...]
```

신규 (0.2.2):

```
# planning-review: [기능명]

- 입력: [경로 list / "직전 planning-format 출력 (conversation)" / "직접 입력 markdown"]
- 입력 제외 §: [§5.1.3 형식]
- 점검 축: [ssot, ac, deps]
- SSOT corpus: 매칭 N개 + 외부 fetch 성공 K개 / 실패 J개 (총 시도 K+J건, cap 없음)
- SSOT 검색 키워드: [keyword1, keyword2, ...]
```

규칙:
- `입력 제외 §:` 줄은 본문 분리 단계 결과 표시. 분리 실패·0.2.0 이전 산출물이면 `없음 (또는 0.2.0 이전 산출물)` 1줄.
- `SSOT corpus:` 줄 형식:
  - link follow 1건 이상 시도: `매칭 N개 + 외부 fetch 성공 K개 / 실패 J개 (총 시도 K+J건, cap 없음)`. K = 본문 합류 성공 자원, J = fetch 실패·인증·content-type skip 등.
  - link 0건: `매칭 N개`.
  - 매칭 0건: `매칭 0개 (검증 대상 없음)`.
  - R1·R3 모두 비활성: 줄 통째 미출력 (R1·R3 corpus 무관 점검).
- `SSOT 검색 키워드:` 줄은 R1 활성 시에만 (0.2.1 그대로).

### 7.2 SSOT 출처 § 신설

link follow 1건 이상 시도(R1 또는 R3 트리거)면 §4.7 형식으로 `## SSOT 출처` 블록 출력. R1·R3 모두 비활성·매칭 0건·`--no-ssot-fetch`·link 0건이면 통째 생략.

블록 위치: `## 리뷰 결과` 다음, 발견 sub-section 위.

```
## 리뷰 결과: [통과 | 발견 N건]
- ...

## SSOT 출처
[§4.7 표]

### SSOT 충돌
[기존]

### 검증가능성
[기존]

### 영향 분석
[기존]
```

### 7.3 R3 영향 분석 § 보조 신호 표시

R3 발견·권고 list에서 입력 제외 § 보조 신호로 만들어진 항목은 `근거` 줄에 출처 표시:

```markdown
1. 외부 위키와 정책 충돌 가능
   - 분류: 권고
   - 카테고리: 외부 의존
   - 위치: 정책서 §5
   - 영향 후보: ./docs/wiki-link.md (외부 fetch 미합류)
   - 근거: "[변환 본문 인용]" + "[입력 제외 § fetch 실패 항목 cross-reference]"
   - 영향: 외부 wiki 본문이 corpus에 미합류라 정책 충돌 잠재
   - 제안: --no-ssot-fetch off + 인증 connector 재확인 또는 외부 wiki 본문 수동 합류
```

기존 발견 형식에 `근거` 줄에 cross-reference만 추가. 새 필드 추가 안 함.

## 8. SKILL.md / reference 갱신

| 파일 | 변경 |
|---|---|
| `skills/planning-review/SKILL.md` | Step 1 입력 dispatch에 입력 제외 § 분리 추가. Step 2 R1 활성 시 link follow + connector fallback + image multimodal 절차 추가. 출력 포맷 갱신 (`SSOT 출처` 블록 + 헤더 줄). 인자 표에 `--no-ssot-fetch` / `--no-ssot-image` 추가. |
| `skills/planning-review/references/ssot-rules.md` | R1.1 절차에 link follow 단계 추가. visited set·sanity check 명시. cycle 방지 규칙. |
| `skills/planning-review/references/deps-rules.md` | §R3.1·§R3.2에 입력 제외 § 보조 신호 가중치 표 추가 (§5.1.2 그대로). |
| `skills/planning-format/references/connector-routing.md` | 변경 없음 (planning-review에서 그대로 공유). 단 §1 헤더에 "planning-review도 같이 사용" 1줄 명시 보강. |
| `docs/planning-review-workflow.md` | Step 1·Step 2 mermaid 다이어그램 갱신 — 입력 제외 § 분리 노드 + R1 link follow 단계 추가. |
| `.codex-plugin/plugin.json` | longDescription 압축 (§5.2). |
| `.claude-plugin/plugin.json` | version 0.2.1 → 0.2.2. description 갱신 (link follow + 입력 제외 § 인지 1줄 추가). |
| `README.md` | 옵션 표에 `--no-ssot-fetch` / `--no-ssot-image` 추가. 결과 형태 §에 `SSOT 출처` 블록 + R3 입력 제외 § 인지 명시. 비교 표 row 갱신 (§5.3). 호환성 §에 0.2.1 → 0.2.2 항목 추가. |
| `docs/prd/README.md` | 신규 생성 (§5.4.1 골격). |
| `docs/prd/prd-0.2.2.md` | 본 문서. |

추정 line 증가:
- `planning-review/SKILL.md`: ~70 line.
- `ssot-rules.md`: ~30 line.
- `deps-rules.md`: ~25 line.
- `planning-review-workflow.md`: ~40 line.
- README: ~30 line.
- `docs/prd/README.md` 신규: ~40 line.

## 9. 호환성

- 0.2.1 → 0.2.2는 `planning-review` **출력 markdown micro-breaking** + `planning-format` 변경 없음.
- micro-breaking 변경:
  - `planning-review` 출력 헤더에 `입력 제외 §:` 줄 추가.
  - `## SSOT 출처` 블록 신규 (R1 link follow 1건 이상 호출에서만).
  - `SSOT corpus:` 줄에 외부 fetch 카운트 추가.
- 0.2.1 산출물(또는 동등 markdown)을 review에 입력해도 무리 없음 — 입력 제외 § 부재 시 R3 보조 신호 단계 skip, 0.2.0 동작과 동등.
- 0.2.0 이전 산출물 호환성 그대로 (입력 제외 § 없거나 5 카테고리 사양).
- `planning-review`가 외부 fetch를 시도하므로 매칭 *.md 본문 안에 외부 link가 많고 connector 미인증 환경이면 호출 시간 증가 가능. `--no-ssot-fetch`로 0.2.1 동작 그대로 유지 가능.
- `--axes ac`만 활성한 호출은 link follow 영향 없음 (R1·R3 비활성).

### 9.1 다운스트림 파서

다음 형식 변경에 따라 정형 파싱 코드 갱신:
- 헤더 `SSOT corpus:` 줄: 정규식 `매칭 (\d+)개` → `매칭 (\d+)개( \+ 외부 fetch (\d+)개)?`.
- 헤더 `입력 제외 §:` 줄 신규.
- `## SSOT 출처` 블록 신규.

### 9.2 환경 의존성

`planning-review` link follow는 `planning-format`과 동일한 connector 환경 의존. Atlassian·Figma·Google Workspace·Slack·Notion connector 인증 상태에 따라 link follow 결과가 다르다. `connector-routing.md` §2 인증 판정 그대로 적용.

## 10. 마이그레이션

### 10.1 사용자 호출

호출 형식 그대로:

```
/planning-kit:planning-format <input> [--save] [--no-fetch] [--no-image] [--no-self-review]
/planning-kit:planning-review [<input>] [--ssot-include <glob>] [--axes <list>] [--no-ssot-fetch] [--no-ssot-image]
```

기존 호출 모두 동일하게 동작. 신규 옵션 미사용 시 0.2.1 + link follow 활성 default.

### 10.2 다운스트림

§9.1 정규식 갱신 + `## SSOT 출처` 블록 처리 추가.

### 10.3 link follow 봉쇄

오프라인·디버그·토큰 절약 필요 시 `--no-ssot-fetch` 사용. `--no-ssot-image` 별도로 이미지 multimodal만 끔.

```
/planning-kit:planning-review --no-ssot-fetch --no-ssot-image  # 0.2.1과 동등
```

## 11. 검증 시나리오

PRD 검수 시점 main이 트레이스 (실 호출은 사용자 환경 검증):

1. **link follow 비활성 (`--no-ssot-fetch`)**: 0.2.1과 동등. 헤더 `SSOT corpus: 매칭 N개`. `## SSOT 출처` 블록 미출력.
2. **link follow 활성, 매칭 *.md 본문 안 link 0건**: 헤더 `매칭 N개` (외부 fetch 절 통째 누락). 출처 블록 미출력. R1·R3 비교는 매칭 *.md만으로.
3. **link follow 활성, link 5건 모두 fetch 성공**: 헤더 `매칭 N개 + 외부 fetch 성공 5개 / 실패 0개 (총 시도 5건, cap 없음)`. `## SSOT 출처` 블록에 매칭 *.md N행 + 자식 5행. corpus = 매칭 *.md + 5 외부 본문.
4. **link follow 활성, link 5건 중 3건 인증 게이트 미인증**: 헤더 `매칭 N개 + 외부 fetch 성공 2개 / 실패 3개 (총 시도 5건, cap 없음)`. 출처 블록에 자식 5행 (X 3건). 호출 종료 안 함, R1·R3 진행.
5. **외부 link가 Confluence + Atlassian connector 인증됨**: connector fallback 성공. 출처 행 status `200 (via Atlassian MCP)`.
6. **외부 link가 Google Sheets fragment**: `connector-routing.md` §3.5 gid·range 처리 그대로. 출처 행 부연 `범위 힌트: C13`.
7. **link follow + image multimodal**: 외부 fetch 응답이 image content-type. multimodal 해석 후 corpus 합류. 출처 행 `image/png 0.4MB ... O (multimodal)`.
8. **`--no-ssot-image` ON, link follow 활성**: URL fetch는 진행. image content-type 응답은 합류 안 함. 출처 행 X + 사유 `--no-ssot-image`.
9. **planning-review 입력 = 0.2.1 산출물 (입력 제외 § 7건: fetch 실패 1, 범위 외 2, 라벨 미매핑 3, 원문 정의 부재 1)**: 헤더 `입력 제외 §: 분리 7건 (R3 신호 3건: fetch 실패 1, 범위 외 2 / R3 무관 4건)`. R3 활성이면 보조 신호 적용 → R3 권고 3건 추가 (fetch 실패 1 + 범위 외 2).
10. **planning-review 입력 = 0.2.0 이전 산출물 (입력 제외 § 부재)**: 헤더 `입력 제외 §: 없음 (또는 0.2.0 이전 산출물)`. R3 보조 신호 단계 skip. 0.2.0 동등.
11. **입력 제외 § 카테고리 = `fetch 실패` 1건만**: 헤더 `분리 1건 (R3 신호 1건: fetch 실패 1 / R3 무관 0건)`. R3 활성이면 권고 1건 추가 (외부 의존).
12. **입력 제외 § 카테고리 = `라벨 미매핑`만 3건**: 헤더 `분리 3건 (R3 신호 0건 / R3 무관 3건)`. R3 변경 없음 (보조 신호 0).
13. **입력 제외 § 카테고리 = `원문 정의 부재`만 2건**: 헤더 `분리 2건 (R3 신호 0건 / R3 무관 2건)`. `원문 정의 부재`는 R3 영향 없음(헤더 카운트에서도 R3 신호 제외).
14. **입력 제외 § 분리 실패** (헤더 매칭 안 됨): sanity check 아님. 정책서·기능설계서만 분리 성공이면 진행. 헤더 `입력 제외 §: 없음 (또는 0.2.0 이전 산출물)`.
15. **`--axes ac`만 활성**: link follow 단계 진입 안 함 (R1·R3 비활성). 헤더 `SSOT corpus:` 줄 통째 미출력. 입력 제외 § 분리는 진행 — 헤더 `입력 제외 §: 분리 N건 (...)` 표기는 됨, 단 R3 보조 신호 적용 안 함.
16. **`--axes deps`만 활성 (R3 단독)**: R1 비활성이지만 R3 트리거로 link follow 진입. corpus 확장 효과 발생. R3 영향 후보 = 매칭 *.md + 외부 fetch 본문. R1 sub-section 미출력.
17. **`--axes ssot`만 활성 (R1 단독)**: R1 트리거로 link follow 진입. R3 sub-section 미출력. 입력 제외 § R3 보조 신호 skip.
18. **link follow가 매칭 file 자기 자신 가리킴**: visited set으로 skip. 출처 list에 등장 안 함.
19. **외부 link cycle (A.md → wiki1 → wiki2 → wiki1)**: visited set으로 wiki1 1번만 fetch. 출처 list에 wiki1·wiki2 각 1행.
20. **Codex plugin.json longDescription**: §5.2 압축 형태 적용. ≤300자 + 핵심 5변경 명시.
21. **README 비교 표**: §5.3 갱신 그대로. `리뷰 축` row + `SSOT corpus 처리` row + `입력 제외 처리` (신규 row).
22. **docs/prd/README.md**: §5.4 골격 그대로. PRD 6건 (0.2.2 포함) 1줄 요약.

## 12. 성공 기준

- `planning-review`가 R1 link follow 1건 이상 진행한 호출에서 출처 list 블록을 출력한다.
- 매칭 *.md 본문 안 외부 URL이 fetch + connector fallback으로 corpus body에 합류한다.
- `--no-ssot-fetch`로 0.2.1 동작과 동등하게 유지 가능.
- `--no-ssot-image`로 link follow는 진행하되 image multimodal만 봉쇄 가능.
- 0.2.1 산출물을 review 입력으로 줄 때 입력 제외 § 자동 분리 + R3 보조 신호 적용.
- 0.2.0 이전 산출물 호환 (입력 제외 § 부재 무리 없음).
- Codex plugin.json longDescription ≤300자 + 핵심 5변경 압축.
- README 비교 표가 0.2.1·0.2.2 변경 반영.
- `docs/prd/README.md`로 PRD chain 안내 가능.
- `connector-routing.md`는 두 스킬에서 공유 적재되며 별도 복제 안 함.

## 13. 비호환·마이그레이션 정리

- **인자**: `planning-review`에 `--no-ssot-fetch` / `--no-ssot-image` 추가. `planning-format` 변경 없음.
- **출력 markdown**: `planning-review` micro-breaking — 헤더 줄·SSOT 출처 블록.
- **자체 검증**: 변경 없음.
- **`planning-format`**: 변경 없음.
- **저장 정책 / connector / 이미지 / 재귀 fetch (planning-format 측)**: 0.2.1 그대로.

## 14. 용어 추가

- **R1 link follow**: `planning-review` R1이 매칭된 *.md 본문 안 URL을 추출해 fetch + connector fallback으로 corpus body에 합류시키는 절차. §4.
- **SSOT 출처 블록**: link follow 1건 이상이면 출력되는 corpus 외부 fetch 표 (§4.7).
- **입력 제외 § R3 보조 신호**: `planning-format` 산출물 입력 제외 § 카테고리 중 R3 영향 후보 산출에 가중치를 주는 5종 (`fetch 실패` / `범위 외` / `구조 변환` / `디테일 축약` / `원문 정의 부재`).
- **PRD chain**: `docs/prd/README.md`에 정리된 PRD 5건 + 0.2.2의 관계도·읽는 순서·핵심 변경 1줄 요약.

그 외 모든 용어는 0.2.1 §13 / 0.2.0 §11 그대로.

## 15. 참고 파일

- `skills/planning-review/SKILL.md` — 본 PRD §4·§5.1·§7 반영.
- `skills/planning-review/references/ssot-rules.md` — §4 link follow 절차 반영.
- `skills/planning-review/references/deps-rules.md` — §5.1.2 입력 제외 § 보조 신호 가중치 반영.
- `skills/planning-format/references/connector-routing.md` — 변경 없음 (공유 적재).
- `docs/planning-review-workflow.md` — Step 1·Step 2 mermaid 갱신.
- `.claude-plugin/plugin.json` / `.codex-plugin/plugin.json` — version 0.2.2 + description 갱신.
- `README.md` — 옵션 표·결과 형태·비교 표·호환성 §.
- `docs/prd/README.md` — 신규 PRD chain 안내.
- `docs/prd/prd-0.2.2.md` — 본 문서.
