# planning-kit PRD 0.2.0

> 0.1.x 기반 **breaking** PRD. `formalize` 단일 스킬을 **`planning-format` + `planning-review` 두 스킬**로 분리하고 자체 품질 검증을 `planning-format` 단계로 흡수한다. 본 문서에서 다루지 않은 명세(URL 분기·재귀 fetch·connector fallback·이미지 multimodal·marker·템플릿 골격 등)는 [`prd-0.1.2.md`](./prd-0.1.2.md), [`prd-0.1.1.md`](./prd-0.1.1.md), [`prd-0.1.0.md`](./prd-0.1.0.md)를 그대로 따른다.

## 1. 변경 요약

네 가지 변경:

1. **스킬 분할** — 기존 `formalize` 단일 스킬을 `planning-format`(변환 + 자체 검증) + `planning-review`(외부 일관성 + SSOT 충돌 등) 두 스킬로 나눈다. 호출은 항상 두 번 — `planning-format` 산출물에서 검토를 원하면 사용자가 직접 `planning-review`를 호출. 두 스킬 사이에 자동 chain 없음.
2. **planning-format이 자체 품질 검증을 흡수** — 0.1.x `formalize` 자동 리뷰 A축(섹션 충실도·라벨 cross-bleed·용어 일관성·정책-기능 매핑·누락 핵심 정보) + markdown lint 수준의 syntax 검사가 `planning-format` 산출물에 합류된다. 변환과 같은 응답에서 자체 보고서가 함께 출력된다. 즉 `planning-format`은 단순 변환기가 아니라 **변환 + 자기 점검**까지 책임진다.
3. **planning-review 스킬은 외부 검증만** — `planning-review`는 `planning-format` 산출물(또는 동등한 두 본문 markdown)을 받아 외부 SSOT corpus와의 충돌, acceptance criteria 검증가능성, 의존·영향 분석 세 축으로 점검한다. 자체 품질은 점검하지 않는다 (이미 `planning-format`에서 처리).
4. **Google Workspace connector 라우팅 버그 fix** — 0.1.2 `connector-routing.md`의 Google 행이 추상적이라 `docs.google.com/spreadsheets/...`, `/document/...`, `/presentation/...`, `drive.google.com/...` URL이 connector 인증돼 있는데도 fallback 후보 0으로 skip되던 케이스를 §5.8 라우팅 표·fileId 추출 규칙·gid/range fragment 처리·카탈로그 평가 보정으로 정정. 동일 버그 위험을 다른 connector(자원 조회 도구만 노출되고 `authenticate` 미노출인 경우)로 일반화해 인증 판정 규칙도 보정.

이 분할로 사용자가 "변환만 빨리" 받고 싶을 때와 "외부 SSOT 충돌 포함 깊은 검토"가 필요할 때를 분리할 수 있다. 변환만 100번 돌려도 SSOT corpus 매칭·외부 비교 비용을 안 치른다.

추가로 `planning-format`에 `--save` 옵션을 도입한다 — default는 0.1.x와 동일한 화면 markdown only이고, `--save`만 켤 때 고정 관습 경로(`./.planning-kit/<기능명>/`)에 두 본문이 떨어진다.

## 2. 동기

- 현재 `formalize`는 한 호출에 변환 + 자동 리뷰 2축을 묶어 처리. 사용자 시나리오 두 가지가 섞여 있다:
  1. **빠른 초안 변환**: 회의 메모·draft를 일단 정책서·기능설계서 골격으로 받아 보고 싶다. 외부 SSOT 비교는 지금 필요 없다 (corpus 매칭 비용·노이즈 회피).
  2. **출고 전 검수**: 변환된 본문을 두고 외부 *.md, 인접 PRD, 변경 이력과의 충돌을 깊이 점검한다. 검수 자체는 본문이 안정된 뒤에 하면 된다.
- 0.1.x의 단일 호출 모델은 (1) 시나리오에서도 (2)를 항상 돌리거나 `--no-review`로 끄도록 강제. (2) 시나리오에서는 `formalize`를 다시 돌릴 수 없으니 변환을 또 한 번 한다 (낭비).
- 한편 자체 품질 점검(섹션 충실도·라벨 cross-bleed·용어 일관성)은 **본문 자체만 보고 결정**되므로 SSOT corpus와 같이 묶일 필연이 없다. 외부 corpus 없이도 의미 있는 즉시 피드백이라 변환 단계와 함께 가는 게 자연스럽다.
- 결국 검증 축을 **본문 자체 점검(planning-format 단계)** vs **외부 비교 점검(planning-review 단계)** 로 가르는 게 사용자의 멘탈 모델과 더 가깝다. 0.2.0은 이 경계를 스킬 경계로 노출한다.

## 3. 비목표

- 두 스킬 사이의 자동 chain·체이닝 헬퍼는 두지 않는다. 사용자는 `planning-format` 호출 후 결과 확인 → 필요 시 `planning-review` 호출. 같은 응답에 한 번에 보고 싶으면 0.1.x `formalize`(0.1.2)를 사용 (병행 유지하지 않음 — §7 호환성 참조).
- `planning-format` 산출물의 영구 저장은 `--save` 옵션 사용 시에만. 옵션 없으면 0.1.x와 동일하게 화면 markdown only.
- 자체 품질 검증을 `planning-review`에서 다시 돌리는 옵션은 두지 않는다. `planning-format` 결과를 신뢰. 사용자가 본문을 손으로 수정한 뒤 `planning-review`를 부르는 시나리오에서는 자체 품질 발견은 사용자 책임.
- `planning-review`에서 본문을 다시 변환하지 않는다. 입력 markdown을 그대로 신뢰하고 외부 corpus와 비교만.
- 0.1.x `formalize` 스킬은 0.2.0에서 **삭제**한다. 마이그레이션 가이드(§8)로 호출자만 `planning-format` + `planning-review`로 분리.
- `--save`가 만든 파일을 `planning-review`가 자동으로 찾아 입력으로 쓰는 magic 동작은 두지 않는다. 사용자가 명시 경로로 호출.
- product-team-kit의 outputRoot·CLAUDE.md upsert·gate-first·다중 marker 정책은 본 PRD 도입하지 않는다. planning-kit는 single-file·skill-only.

## 4. 스킬 구조

```
planning-kit/
├── .claude-plugin/plugin.json        # skills: planning-format, planning-review (formalize 삭제)
├── .codex-plugin/plugin.json         # 동일
├── README.md
├── docs/
│   ├── planning-format-workflow.md            # 0.1.x formalize-workflow.md → format용 다이어그램
│   ├── planning-review-workflow.md            # 신규: review 단일 패스 다이어그램
│   └── prd/
│       ├── prd-0.1.0.md
│       ├── prd-0.1.1.md
│       ├── prd-0.1.2.md
│       └── prd-0.2.0.md              # 본 release
└── skills/
    ├── planning-format/
    │   ├── SKILL.md
    │   ├── templates/
    │   │   ├── 기능설계서.md          # 0.1.x formalize/templates 그대로
    │   │   └── 정책서.md
    │   └── references/
    │       ├── self-review-rules.md  # 0.1.x review-rules.md A축 + lint 항목
    │       └── connector-routing.md  # 0.1.x 그대로
    └── planning-review/
        ├── SKILL.md
        └── references/
            ├── ssot-rules.md         # 0.1.x review-rules.md B축 (corpus 추출·매칭·발견 형식)
            ├── ac-rules.md           # 신규: acceptance criteria 검증가능성 기준
            └── deps-rules.md         # 신규: 의존·영향 분석 기준
```

`skills/formalize/`는 0.2.0에서 제거. `references/review-rules.md`는 분해되어 `planning-format/references/self-review-rules.md` + `planning-review/references/ssot-rules.md`로 흡수된다.

## 5. `planning-format` 스킬

### 5.1 인자

위치 인자 1개 이상 (필수): 기획 초안 텍스트, 파일 경로, 디렉터리 경로, 1개 이상의 URL 중 하나. 분기 우선순위는 0.1.2 §3.1 그대로.

| 인자 | 기본값 | 설명 |
|---|---|---|
| `--save` | off | `./.planning-kit/<기능명>/정책서.md`, `./.planning-kit/<기능명>/기능설계서.md` 두 파일에 본문을 저장. 자체 검증 보고서는 저장하지 않음(화면 only). 기존 파일이 있으면 §5.7 collision 정책. |
| `--no-fetch` | off | URL fetch + connector fallback 봉쇄. 0.1.2 그대로. |
| `--no-image` | off | 이미지 multimodal 호출 0건. 0.1.2 그대로. |
| `--no-self-review` | off | 자체 품질 검증 블록 출력 생략. 변환 본문 + 출처 list + 입력 제외만 출력. 빠른 변환만 필요할 때. |

`--ssot-include`는 `planning-format`에서 제거된다 (`planning-review`로 이동). `--no-review`도 의미가 사라져 제거.

### 5.2 동작 시퀀스

1. **입력 dispatch** (0.1.2 §3.1) — 텍스트/파일/디렉터리/URL 분기.
2. **빈 입력 sanity check** (0.1.2 §3.2).
3. **재귀 fetch + connector fallback** (0.1.2 §3.3·3.4) — `references/connector-routing.md` 그대로 사용.
4. **이미지 multimodal 처리** (0.1.2 §4).
5. **통합 본문 합류** (0.1.2 §5).
6. **기능명 추출** (0.1.2 §6.1).
7. **두 템플릿 변환** (0.1.2 §6.2) — `templates/기능설계서.md` + `templates/정책서.md` 병렬 Read, main이 같은 턴에 두 본문 작성. marker는 `[TBD]` 1종.
8. **자체 품질 검증** (§5.3) — `--no-self-review`가 아니면 실행.
9. **`--save` 처리** (§5.5) — 옵션이 켜져 있으면 두 본문을 디스크에 떨어뜨림. 보고서·출처 list는 저장하지 않음.
10. **통합 출력** (§5.4).

§3·4·5·6·7은 0.1.2와 동일하므로 이 PRD에서 재기술하지 않는다.

### 5.3 자체 품질 검증 (`planning-format` 내부)

`planning-format`은 변환 직후 같은 응답에서 다음 5개 카테고리를 main 단일 패스로 점검한다. 입력·변환 본문(메모리)만 근거. 외부 SSOT corpus·다른 *.md 파일은 보지 않는다.

| 카테고리 | 점검 기준 (요약) | 출처 |
|---|---|---|
| **F1. 섹션 충실도** | [TBD] 셀 비율 50% 초과 / 빈 row / 빈 섹션 발견 | 0.1.2 review-rules A1 |
| **F2. 라벨 cross-bleed** | 정책서에 화면·동작 단어 / 기능설계서에 정책 단어 침범 | 0.1.2 review-rules A2 |
| **F3. 용어 일관성** | 역할명·상태명·권한명·도메인 stem이 두 문서 또는 한 문서 안에서 흔들림 | 0.1.2 review-rules A3 |
| **F4. 정책-기능 매핑** | 정책서 §5·§6 규칙이 기능설계서 §5·§7에 누락 / 정책서 `금지` 액션이 기능설계서 정상 흐름 | 0.1.2 review-rules A4 |
| **F5. 누락 핵심 정보** | 입력의 명시 사실(역할·상태·기능명·임계)이 두 본문·입력 제외에 모두 부재 | 0.1.2 review-rules A5 |
| **F6. Markdown syntax lint** (신규) | 코드 펜스 미닫힘 / 표 컬럼 수 mismatch / 헤더 레벨 점프(예: `#` → `###`) / 빈 인용 부호 / 잘못된 list nesting | 본 PRD §5.3.1 |

상세 기준은 `skills/planning-format/references/self-review-rules.md`에 옮긴다 (0.1.x `review-rules.md` A축 그대로 + F6 lint 추가).

#### 5.3.1 F6 — Markdown syntax lint

본문이 코드 펜스 안에 들어가는데 펜스 자체가 깨지면 출력 markdown이 무너진다. 다음 항목만 자동 점검:

- 코드 펜스 ` ``` `의 짝이 맞는지 (열고 안 닫음 / 닫음 마커가 부족 / triple-backtick이 inline에 잘못 등장).
- 표 한 행의 셀 수가 헤더와 다르면 발견 (`|---|---|`로 선언한 컬럼 수와 다음 row의 `|` 카운트 불일치).
- 헤더 레벨 점프 (`#` 다음 첫 자식 헤더가 `###` 이상). `[TBD]` 셀로 인한 점프는 예외.
- 빈 인용 부호(`> ` 한 줄만 + 다음 줄 비어 있음).
- 같은 list 안에서 marker 일관성 (`-`와 `*`가 섞이면 발견; `1.`과 `2.` 순서가 깨지면 발견).

각 항목은 카테고리 `syntax`로 발견 list에 합류. 수정 제안은 1줄 + 최소 변경.

#### 5.3.2 발견 사항 형식

각 항목:

- `카테고리`: F1~F6 라벨 — `충실도` / `cross-bleed` / `용어 일관성` / `정책-기능 매핑` / `누락` / `syntax`.
- `위치`: 정책서/기능설계서 §섹션 (또는 syntax의 경우 line 번호).
- `근거`: 변환 본문 인용 (≤80자) 또는 lint failure 인용.
- `영향`: 한 줄.
- `제안`: 최소 수정 또는 확인 조건 한 줄.

### 5.4 출력 포맷

정책서·기능설계서 본문은 0.1.2와 동일하게 ` ```markdown ... ``` ` 코드 펜스로 감싼다.

#### 5.4.1 정상 (변환 + 자체 검증)

````markdown
# [기능명]

- 입력 처리: [0.1.2 §7.1 분기별 헤더 그대로]
- 출처: [0.1.2 §7.1]
- 미결 표기: [TBD] N개
- 입력 제외: N건 (0건이면 "없음")
- 저장: [화면 only / `./.planning-kit/<기능명>/` 2개 파일]

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

(URL fetch + 이미지 처리 1건 이상일 때만. 0.1.2 §7 그대로.)

---

## 입력 제외 항목

(≥1건일 때만. 0.1.2 그대로.)

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
   - 카테고리: [충실도 / cross-bleed / 용어 일관성 / 정책-기능 매핑 / 누락 / syntax]
   - 위치: [정책서/기능설계서 §섹션 또는 line N]
   - 근거: "[변환 본문 인용]"
   - 영향: [한 줄]
   - 제안: [최소 수정 또는 확인 조건]
````

규칙:

- 6개 카테고리 모두 0건이면 `## 자체 검증: 통과`로만. 카운트 줄은 그대로 출력.
- `--no-self-review`면 `## 자체 검증` 블록 통째 생략. 다른 블록 영향 없음.
- 블록 순서: 변환 본문 → 출처 → 입력 제외 → 자체 검증.
- `## 리뷰 결과` 블록은 0.2.0 `planning-format`에 없다 (`planning-review` 스킬로 이동).

#### 5.4.2 sanity check

- 빈 입력: 0.1.2 §7.3 그대로 (`입력 비어 있음. ...` 한 줄).
- URL 분기 실패: 0.1.2 §3.4 + `connector-routing.md` §8 5종.
- `--save` 실패: §5.7.

### 5.5 `--save` 동작

`--save`가 켜진 경우 두 본문을 디스크에 저장한다. 화면 markdown 출력은 default와 동일 — 헤더 줄에 `저장:` 항목만 갱신.

#### 5.5.1 저장 경로

```
./.planning-kit/<기능명-안전화>/정책서.md
./.planning-kit/<기능명-안전화>/기능설계서.md
```

`./`는 호출 시점 cwd. 폴더가 없으면 mkdir(부모 포함). `.planning-kit/`은 본 스킬이 만든 표시. `.gitignore` 자동 추가는 하지 않는다 (사용자가 결정).

자체 검증 보고서·출처 list·입력 제외 항목은 저장하지 않는다 (화면 only). `## 정책서` / `## 기능설계서` 코드 펜스 안 본문만 추출해 그대로 파일에 쓴다.

#### 5.5.2 기능명 안전화

기능명에서 다음을 제거·변환:

1. NFC normalize (한글 풀어쓰기 → 합쳐쓰기).
2. 경로 분리자 `/`, `\`, 컨트롤 문자 제거.
3. 양 끝 공백·점(`.`) trim.
4. 앞에 `..`/`-`로 시작 시 `_` prefix.
5. 64자 초과 시 64자에서 자름.
6. 안전화 결과가 빈 문자열이면 `untitled-<8자 난수 hex>`로 폴백.

기능명에 영문·한글·숫자·공백·`-`·`_`·`(`·`)`·`[`·`]`·`.`·중간 점 등은 그대로 둔다 (가독성 우선). 윈도우 예약어(`CON`, `PRN`, `NUL`, `LPT1`...)는 충돌 시 `_` suffix.

#### 5.5.3 collision 정책

같은 경로에 파일이 이미 있으면:

```
./.planning-kit/<기능명>/정책서.md         (기존)
./.planning-kit/<기능명>/정책서-2.md       (신규, suffix 증가)
./.planning-kit/<기능명>/정책서-3.md
```

기능설계서도 같은 규칙. 기존 파일 덮어쓰기 안 함. suffix는 2부터 시작 — 99까지 시도, 그래도 충돌이면 `--save` 실패로 처리.

`--save-overwrite` 같은 강제 옵션은 두지 않는다. 사용자는 직접 기존 파일을 옮기거나 `--save` 빼고 화면 출력으로 받음.

#### 5.5.4 저장 실패

mkdir / write 실패(권한·디스크 full)는 본문 변환·자체 검증 결과는 그대로 화면에 출력하고 헤더 `저장:` 줄에 사유 1줄 표시:

```
- 저장: 실패 — <한 줄 사유 (예: "permission denied: ./.planning-kit/")>. 본문은 화면 only로 반환.
```

호출 종료 사유는 아니다. 저장 실패가 자체 검증 결과를 변경하지 않는다.

### 5.6 product-team-kit과의 관계

product-team-kit의 `outputRoot`·`<연도>/` prefix·CLAUDE.md upsert는 도입하지 않는다. `planning-format --save`는 단순 `./.planning-kit/<기능명>/` 고정. 사용자가 다른 위치에 옮기고 싶으면 이후 직접 mv.

### 5.7 헤더 `저장:` 줄

| 케이스 | 출력 |
|---|---|
| `--save` off | `- 저장: 화면 only` |
| `--save` 성공 (충돌 없음) | `- 저장: ./.planning-kit/<기능명>/정책서.md, ./.planning-kit/<기능명>/기능설계서.md` |
| `--save` 성공 (충돌 회피) | `- 저장: ./.planning-kit/<기능명>/정책서-2.md, ./.planning-kit/<기능명>/기능설계서-2.md (기존 파일 보존)` |
| `--save` 실패 | `- 저장: 실패 — <사유>. 본문은 화면 only로 반환.` |

### 5.8 Google Workspace connector 라우팅 (0.1.2 버그 fix)

#### 5.8.1 문제 진단 (0.1.x)

0.1.2 `connector-routing.md` §3 row 4는 Google 호스트(`docs.google.com/document/...`, `/spreadsheets/...`, `/presentation/...`, `drive.google.com/...`)에 대해 connector 후보를 `Google Drive connector — authenticate(미인증 시) / 자원 조회 도구`로만 명시. 구체 tool 이름·인자 추출 규칙·fragment(`#gid=`, `&range=`) 처리가 빠져 있다.

실제 세션의 Google Drive MCP 도구는:

```
mcp__claude_ai_Google_Drive__copy_file
mcp__claude_ai_Google_Drive__create_file
mcp__claude_ai_Google_Drive__download_file_content
mcp__claude_ai_Google_Drive__get_file_metadata
mcp__claude_ai_Google_Drive__get_file_permissions
mcp__claude_ai_Google_Drive__list_recent_files
mcp__claude_ai_Google_Drive__read_file_content
mcp__claude_ai_Google_Drive__search_files
```

연결돼 있는데도 main은 다음 순서로 실패한다:

1. WebFetch가 `accounts.google.com`으로 redirect → 인증 게이트 휴리스틱 적중.
2. fallback 평가에서 후보 tool 이름을 `connector-routing.md`로부터 못 찾음(매핑이 추상적).
3. `fetch`라는 일반 도구가 Google Drive MCP에 없음(Atlassian의 `fetch`만 있음).
4. 후보 0 → skip → 출처 list `인증 필요 (connector 매핑 없음)`.

결과: connector 인증돼 있는데도 본문 합류 0건.

대표 케이스 — `https://docs.google.com/spreadsheets/d/1EkCTH6PPB-OC8a1WOm5nzNFCw4ZXocxI7SmkFPaQrKs/edit?gid=1105223495#gid=1105223495&range=C13`. 0.1.2에서는 인증 게이트 → skip. 0.2.0에서 §5.8.2 라우팅으로 합류.

#### 5.8.2 URL 패턴별 tool 시퀀스

호스트 매칭이 적중하면(eTLD+1 = `google.com` + path 또는 `drive.google.com`) 다음 시퀀스를 시도. 실패 시 다음 후보로.

| 자원 종류 | URL 패턴 | fileId 추출 정규식 | tool 시퀀스 |
|---|---|---|---|
| Google Docs | `docs.google.com/document/d/<fileId>/edit...` | `/document/d/([A-Za-z0-9_-]+)` | 1) `read_file_content(fileId)` → 2) `get_file_metadata(fileId)` (제목·소유자만이라도) |
| Google Sheets | `docs.google.com/spreadsheets/d/<fileId>/edit...` | `/spreadsheets/d/([A-Za-z0-9_-]+)` | 1) `read_file_content(fileId)` → 2) `download_file_content(fileId, mimeType="text/csv")` (단일 시트 export) → 3) `get_file_metadata(fileId)` |
| Google Slides | `docs.google.com/presentation/d/<fileId>/edit...` | `/presentation/d/([A-Za-z0-9_-]+)` | 1) `read_file_content(fileId)` → 2) `get_file_metadata(fileId)` |
| Google Drive 일반 | `drive.google.com/file/d/<fileId>/...`, `drive.google.com/open?id=<fileId>`, `drive.google.com/drive/folders/<folderId>` | `/file/d/([A-Za-z0-9_-]+)` 또는 `[?&]id=([A-Za-z0-9_-]+)` 또는 `/folders/([A-Za-z0-9_-]+)` | 폴더면 `search_files(parents=folderId)`로 list, 파일이면 `read_file_content(fileId)` → `download_file_content` → `get_file_metadata` |
| Google Sheets (`sheets.google.com`) | sheets.google.com 단축 URL | spreadsheets 동일 추출 시도 | spreadsheets 시퀀스 그대로 |
| Google Slides (`slides.google.com`) | slides.google.com 단축 URL | presentation 동일 | presentation 시퀀스 |

Tool 호출 인자:
- `read_file_content` → `{ "id": fileId }` (response: 본문 markdown 또는 텍스트). 본문 합류용 1순위.
- `download_file_content` → `{ "id": fileId, "mimeType": <export type> }` (Sheets는 `text/csv`, Docs는 `text/markdown` 또는 `text/plain`). `read_file_content`가 빈 본문이거나 미지원이면 폴백.
- `get_file_metadata` → `{ "id": fileId }` (response: 제목·last modified·소유자). 본문 합류 실패 시 최소한 제목·메타라도 출처에 기록.

#### 5.8.3 gid·range fragment 처리

Sheets URL의 `#gid=<sheetGid>&range=<cellRange>` 또는 query `?gid=<sheetGid>` fragment는 다음과 같이 다룬다:

1. `gid` 추출 가능 시 → `read_file_content` 응답에서 해당 시트만 골라 본문 합류. 응답이 시트 list로 분할돼 있으면 gid에 해당하는 시트 텍스트만 합류. 분할 안 돼 있으면 전체 합류.
2. `range`(예: `C13`, `A1:D20`) 추출 가능 시 → 응답 표에서 해당 범위만 잘라 합류. 자르기 어려우면 시트 전체를 합류하고 출처 list에 `범위 힌트: <range>` 부연.
3. fragment 추출 실패 시 → 시트 전체 합류 (cap 없음 정책 그대로).
4. 본문 합류 헤더(0.1.2 §5)는 다음 형태:
   ```
   === [출처 N] Google Sheets: <원본 URL> (gid=<sheetGid>, range=<cellRange>) ===
   ```
5. multimodal 호환 — 응답에 차트·그림이 있으면 image queue로 라우팅 (0.1.2 §4 그대로).

#### 5.8.4 카탈로그 평가 보정

0.1.2 `connector-routing.md` §2의 인증 판정은 "`authenticate` 도구만 노출 + 자원 조회 도구 부재 → 미인증"이지만, Google Drive는 세션에 `authenticate` 도구가 노출되지 않은 상태에서도 자원 조회 도구만 활성인 경우가 있다. 다음 규칙을 추가:

- `mcp__claude_ai_Google_Drive__read_file_content`(또는 `get_file_metadata`·`search_files` 중 하나)가 deferred tool list에 보이면 **인증됨**.
- `mcp__claude_ai_Google_Drive__authenticate`만 보이고 위 자원 조회 도구가 모두 부재면 **미인증**.
- 둘 다 부재면 **미연결** — fallback 후보 0.

이 규칙은 Atlassian/Figma/Slack/Notion에도 일반화: 자원 조회 도구가 1개 이상 있으면 `authenticate` 노출 여부와 무관하게 인증된 것으로 간주한다.

#### 5.8.5 출처 list `상태` 컬럼 (Google 추가 표기)

| 상태 | 의미 |
|---|---|
| `200 (via Google Drive connector — read_file_content)` | `read_file_content` 1차 성공. |
| `200 (via Google Drive connector — download_file_content)` | export 폴백 성공. |
| `metadata only (via Google Drive connector — get_file_metadata)` | 본문 못 가져오고 메타만 합류. 자체 검증 발견 가능. |
| `인증 필요 (Google Drive connector 미인증)` | `authenticate` 노출 + 자원 도구 부재. |
| `미연결 (Google Drive connector)` | 도구 자체 미노출. 일반 WebFetch 결과로 fallback. |

#### 5.8.6 `connector-routing.md` 갱신 범위

본 PRD §5.8.2~5.8.5는 `skills/planning-format/references/connector-routing.md` §3 row 4 + §2 + §5 + §7에 반영된다. 0.1.2 다른 행(Atlassian/Figma/Slack/Notion)은 §5.8.4의 일반화된 인증 판정 규칙만 영향, 그 외 동작 동일.

#### 5.8.7 검증 시나리오

§9 검증 시나리오 list 16~19 항목 참조.

## 6. `planning-review` 스킬

### 6.1 개요

`planning-review`는 정책서·기능설계서 두 본문 markdown을 받아 외부 검증 3축으로 점검하고 발견 사항을 화면 markdown으로 반환. 변환·재변환 안 함, 본문 저장 안 함.

### 6.2 인자

위치 인자 0개 또는 1~2개 (소스에 따라):

- 0개 = conversation 참조 모드. 직전 turn(들)에서 `planning-format`이 출력한 정책서·기능설계서 코드 펜스 본문을 main이 메모리에서 직접 읽는다. 직전 `planning-format` 출력이 없으면 sanity check.
- 1개 = 단일 경로. 디렉터리면 안에서 `정책서*.md` + `기능설계서*.md`를 자동으로 찾는다 (suffix `-2`/`-3` 등 허용). 파일이면 본문 안에서 두 섹션을 자동 분리(헤더 `# 정책서` / `# 기능설계서` 또는 `## 정책서` / `## 기능설계서` 또는 코드 펜스).
- 2개 = `<정책서 경로> <기능설계서 경로>` 또는 `<기능설계서> <정책서>` (헤더로 자동 식별).
- raw markdown 텍스트 1개 = 따옴표로 감싼 markdown. 두 본문이 모두 들어 있으면 자동 분리. 한 본문만 있으면 sanity check.

| 인자 | 기본값 | 설명 |
|---|---|---|
| `--ssot-include <glob>` | (없음) | SSOT corpus glob. default = 프로젝트 폴더 안 모든 `*.md` (`.git/`, `node_modules/` 자동 제외). 0.1.2 그대로. |
| `--axes <list>` | `ssot,ac,deps` | 점검할 축. 콤마 구분. 빈 값이면 sanity check. 예: `--axes ssot`만 돌리면 0.1.x B축과 동일 동작. |

### 6.3 입력 dispatch

```
1. 인자 토큰 수에 따라 분기:
   0개  → conversation 참조 모드
   1개  → path / 단일 markdown 텍스트 (자동 판별: 파일 시스템 lstat 우선)
   2개  → 두 path
   3개+ → sanity check ("정책서·기능설계서 외 추가 인자는 받지 않습니다.")
2. 두 본문 분리:
   2a. 양쪽 본문에 `# 정책서` / `## 정책서` 또는 `# 기능설계서` / `## 기능설계서` 헤더 매칭.
   2b. 매칭 실패 시 코드 펜스 ` ```markdown ... ``` ` 안 첫 헤더로 식별.
   2c. 식별 실패 시 sanity check.
3. 빈 본문 sanity check:
   3a. 정책서 또는 기능설계서가 0byte이거나 헤더만 있으면 발견 처리 안 하고 종료 메시지.
```

#### 6.3.1 sanity check 메시지

| 케이스 | 메시지 |
|---|---|
| conversation 모드 + 직전 planning-format 출력 없음 | `직전 turn에서 planning-format 출력을 찾을 수 없습니다. 경로 또는 markdown을 인자로 주세요.` |
| 1개 인자 + 본문 식별 실패 | `정책서·기능설계서 두 본문을 식별할 수 없습니다. 헤더(# 정책서 / # 기능설계서) 또는 별도 파일/경로로 주세요.` |
| 한쪽 본문 비어 있음 | `<정책서 또는 기능설계서>가 비어 있습니다. planning-format 산출물을 확인하세요.` |
| `--axes` 빈 값 | `--axes에 점검 축을 1개 이상 지정하세요. (ssot, ac, deps)` |

호출 종료. 발견 list 출력 안 함.

### 6.4 검증 축

`--axes`로 활성화된 축만 main이 단일 패스로 점검. axes 사이의 의존은 없다 (병렬 점검 가능).

#### 6.4.1 R1. SSOT 충돌 (`ssot`)

0.1.2 review-rules B축 그대로. `skills/planning-review/references/ssot-rules.md`에 그대로 옮긴다.

요약:

1. 변환 본문에서 키워드 추출 (기능명·도메인 stem·역할명·상태명·권한명·정책 핵심어).
2. 키워드 list는 출력 헤더에 그대로 노출.
3. 프로젝트 폴더 `find . -name '*.md'` (`.git`/`node_modules` 제외, `--ssot-include`로 좁힘).
4. `grep -l` / `rg -l`로 매칭 → `Read`로 직접 비교.
5. 매칭 0건이면 `검증 대상 없음`. 매칭 ≥1건이면 같은 대상의 표기·결정·임계값 어긋남을 발견 list화.

#### 6.4.2 R2. Acceptance criteria 검증가능성 (`ac`)

상세 기준은 `skills/planning-review/references/ac-rules.md`. 핵심:

- 정책서 §5(세부 규칙)·§6(상태 처리), 기능설계서 §5(기능 동작)·§7(예외)의 **확정 문장**(=`[TBD]` 아님)이 테스트 가능한 형태인지.
- 점검 휴리스틱:
  - **수치 임계 명시**: `빨리`, `자주`, `많이`, `대부분` 같은 비정량 부사 + 임계값 부재면 발견.
  - **상태 명시**: 상태 전이 규칙이 시작 상태·종료 상태·트리거를 모두 적시하는지. `취소된다`만 있고 트리거 부재면 발견.
  - **행위자 명시**: `허용한다`, `차단한다`의 주어가 시스템·사용자 역할 중 하나로 명확한지. 주어 부재면 발견.
  - **결과 관찰가능성**: 행위 후 검증 가능한 신호(상태 필드 변경, 응답 코드, 알림 발송 등)가 적시되는지. 부재면 발견.
- Given-When-Then 변형도 허용 — 한 문장 안에 트리거(When)·전제(Given)·결과(Then) 셋이 다 보이면 통과로 본다.
- 발견 카테고리: `정량성` / `상태` / `행위자` / `결과 관찰`.

#### 6.4.3 R3. 의존·영향 분석 (`deps`)

상세 기준은 `skills/planning-review/references/deps-rules.md`. 핵심:

- 변환 본문의 확정 문장이 어떤 다른 SSOT 문서·기능에 파급 효과를 줄지 추론.
- 점검 휴리스틱:
  - **정책 변경 추론**: 정책서 §5·§6에 새/변경 규칙이 있고, SSOT corpus에 같은 도메인 stem 매칭 파일이 있으면 그 파일들을 영향 후보로 list화.
  - **상태 전이 변경**: 정책서 §6 상태 전이 규칙이 변경되면 같은 도메인의 기능설계서·README·정책서 후보 모두 영향 후보.
  - **권한·역할 변경**: 정책서 §7 역할 권한이 변경되면 권한 매트릭스 문서·인증 정책 문서 후보 영향.
  - **외부 의존**: fetch한 외부 URL(0.1.2 §3) 본문에 등장하는 도메인 stem이 변환 본문 정책과 충돌 또는 일치하는지.
- 결과는 "영향 후보" 형식 — 충돌이 단정적이면 발견, 단지 검토 권고면 권고. 둘 다 출력 list에 합류.
- corpus는 SSOT 축과 같은 set 사용 (`--ssot-include` 공유).

### 6.5 발견 사항 형식

각 발견 항목 (planning-review 공통):

- `축`: R1/R2/R3 — `SSOT 충돌` / `검증가능성` / `영향 분석`.
- `카테고리`: 축 안 sub-category.
- `위치`: 정책서/기능설계서 §섹션 또는 SSOT 파일 §섹션.
- `근거`: 변환 본문 인용 (+ R1·R3는 비교 대상 인용).
- `영향`: 한 줄.
- `제안`: 최소 수정 또는 확인 조건.

같은 발견이 두 축에 걸치면 한 번만 기록 (보수적인 쪽 = 영향이 큰 쪽으로). 0.1.x §발견 사항 형식과 동일.

### 6.6 결과 결정

- 모든 활성 축의 발견 0건 → `통과`
- ≥1건 → `발견 N건` (N = 활성 축 발견 합계)

조건부 통과·수정 필요 같은 3분 결과는 두지 않음 (0.1.x 정책 그대로).

### 6.7 출력 포맷

````markdown
# planning-review: [기능명]

- 입력: [경로 list / "직전 planning-format 출력 (conversation)" / "직접 입력 markdown"]
- 점검 축: [ssot, ac, deps]
- SSOT corpus: [매칭 N개 / 매칭 0개 (검증 대상 없음)]
- SSOT 검색 키워드: [keyword1, keyword2, ...]

---

## 리뷰 결과: [통과 | 발견 N건]

- SSOT 충돌: N건 (활성 시)
- 검증가능성: N건 (활성 시)
- 영향 분석: N건 (활성 시)

### SSOT 충돌
(≥1건일 때만)
1. [제목]
   - 위치: [정책서/기능설계서 §섹션] vs [SSOT 파일 §섹션]
   - 근거: "[변환 본문 인용]" vs "[SSOT 인용]"
   - 영향: [한 줄]
   - 제안: [최소 수정 또는 확인 조건]

### 검증가능성
(≥1건일 때만)
1. [제목]
   - 카테고리: [정량성 / 상태 / 행위자 / 결과 관찰]
   - 위치: [정책서/기능설계서 §섹션]
   - 근거: "[변환 본문 인용]"
   - 영향: [한 줄]
   - 제안: [최소 수정]

### 영향 분석
(≥1건일 때만)
1. [제목]
   - 카테고리: [정책 변경 / 상태 전이 / 권한·역할 / 외부 의존]
   - 위치: [정책서/기능설계서 §섹션]
   - 영향 후보: [SSOT 파일 path list]
   - 근거: "[변환 본문 인용]" + "[SSOT 인용]"
   - 영향: [한 줄]
   - 제안: [후속 검토 조건]
````

규칙:

- 활성 안 한 축의 sub-section은 통째 생략.
- 모든 활성 축이 0건이면 `## 리뷰 결과: 통과`로만 + 카운트 줄.
- SSOT 검색 키워드 줄은 R1 활성 시에만 출력 (다른 축은 corpus 매칭 사용해도 키워드 노출 안 함 — R1 전용 표시).

## 7. 호환성

- 0.1.x → 0.2.0은 **breaking**. `formalize` 스킬은 제거. 호출자는 `planning-format` + `planning-review`로 분리해야 함.
- 인자·옵션 매핑:
  - 0.1.x `formalize <input>` → 0.2.0 `format <input>` (단, default가 자체 검증 포함이라 사용자 체감은 비슷).
  - 0.1.x `formalize --no-review` → 0.2.0 `format --no-self-review` (자체 검증만 끔; 0.1.x의 `--no-review`는 자체 + SSOT 둘 다 끄지만, 0.2.0에서는 SSOT가 별 스킬이라 호출 안 하는 것으로 동등).
  - 0.1.x `formalize --ssot-include <glob>` → 0.2.0 `planning-review --ssot-include <glob>` (planning-format에서 사라지고 planning-review로 이동).
  - 0.1.x `formalize --no-fetch` / `--no-image` → 0.2.0 `format --no-fetch` / `--no-image` (그대로).
- 출력 markdown 구조:
  - 0.1.x `formalize`의 `## 리뷰 결과` 블록 → 0.2.0에서 자체 품질은 `planning-format`의 `## 자체 검증` + SSOT는 `planning-review`의 `## 리뷰 결과`로 분리.
  - 0.1.x `## 출처` 블록 → 0.2.0 `planning-format` `## 출처` 그대로.
- 0.1.2 connector fallback·이미지 multimodal·재귀 fetch 동작은 0.2.0 `planning-format`에서 그대로 유지. `planning-review`는 외부 fetch 안 함.
- product-team-kit과의 병행은 그대로 가능. 두 플러그인은 독립.

## 8. 마이그레이션 가이드

### 8.1 사용자 호출 매핑

| 0.1.x 호출 | 0.2.0 대응 |
|---|---|
| `/planning-kit:formalize <input>` | `/planning-kit:planning-format <input>` 후 필요 시 `/planning-kit:planning-review` |
| `/planning-kit:formalize <input> --no-review` | `/planning-kit:planning-format <input>` (planning-review 호출 생략) |
| `/planning-kit:formalize <input> --ssot-include "<glob>"` | `/planning-kit:planning-format <input>` → `/planning-kit:planning-review --ssot-include "<glob>"` |
| `/planning-kit:formalize <input> --no-fetch --no-image` | `/planning-kit:planning-format <input> --no-fetch --no-image` |

### 8.2 codex 매핑

| 0.1.x | 0.2.0 |
|---|---|
| `$formalize <input>` | `$planning-format <input>` + `$planning-review` |

### 8.3 자동 chain이 필요한 사용자

본 PRD는 chain 헬퍼를 두지 않는다. 한 응답에 변환 + SSOT까지 받고 싶은 사용자는 0.1.2 호출 형태를 두 번 나누어 쓰거나, 자기 워크플로 위에 wrapper 스킬을 별도로 둔다 (kit 외부).

### 8.4 plugin.json 갱신

```json
{
  "skills": [
    { "name": "planning-format", "path": "skills/planning-format" },
    { "name": "planning-review", "path": "skills/planning-review" }
  ]
}
```

`formalize` 항목 삭제. README의 `quick start` 예시도 두 호출로 분리.

## 9. 검증 시나리오

PRD 검수 시점 main이 트레이스 (실 호출은 사용자 환경 검증):

1. **planning-format 단독, 자체 검증 통과**: 깨끗한 입력에 `planning-format` 호출. 변환 + 출처 + `## 자체 검증: 통과`. SSOT 미접근.
2. **planning-format + 자체 검증 발견**: cross-bleed 의도 입력 (정책서 자리에 화면·버튼 단어 다수). `## 자체 검증: 발견 N건`에 cross-bleed 항목 포함. SSOT 미접근.
3. **planning-format `--save` 성공**: `--save`로 호출. `./.planning-kit/<기능명>/정책서.md`·`기능설계서.md` 생성. 화면 헤더 `저장:` 줄에 두 경로 노출.
4. **planning-format `--save` collision**: 기존 `정책서.md` 존재 상태. `--save` 호출 시 `정책서-2.md`로 저장. 화면 `저장:` 줄에 collision 회피 표기.
5. **planning-format `--save` 권한 실패**: 부모 폴더 read-only. 본문은 화면에, `저장: 실패 — permission denied`.
6. **planning-review conversation 모드**: 직전 turn에 `planning-format` 호출 결과 있는 상태에서 인자 없는 `planning-review`. 자동으로 두 본문 추출, 3축 점검.
7. **planning-review path 모드 (1개 dir)**: `--save`로 떨어진 디렉터리를 인자로 줌. 자동으로 두 *.md 식별, 3축 점검.
8. **planning-review path 모드 (2개 file)**: 명시 두 경로. 헤더로 정책/기능 식별 후 점검.
9. **planning-review `--axes ssot`만**: 0.1.x B축과 동등 동작. R2·R3 sub-section 생략.
10. **planning-review SSOT 매칭 0건**: 깨끗한 새 프로젝트. R1 `검증 대상 없음`. R2·R3는 본문 내부 점검만으로 진행.
11. **planning-review AC 발견**: 본문에 `자주 알림을 보낸다` (비정량 부사) → R2 `정량성` 발견.
12. **planning-review 의존·영향 발견**: 정책서 §6 상태 전이 변경 + 같은 도메인 다른 *.md에 같은 도메인 stem 매칭. R3에 영향 후보 file path list.
13. **planning-format 직후 planning-review**: 같은 conversation 안 두 호출. planning-format은 connector fallback 사용 → 화면 출처 list `via Figma MCP` 표기. 이어 planning-review는 외부 fetch 0건, SSOT 매칭만.
14. **planning-review 인자 3개**: sanity check 메시지 + 종료.
15. **planning-review 입력 한쪽 비어 있음**: sanity check + 종료.
16. **Google Sheets URL fragment 합류**: 본 PRD §5.8.1 예시 URL 인자. 0.1.2: `인증 필요` skip. 0.2.0: `read_file_content`로 합류, gid·range 부연.
17. **Google Docs URL 본문 합류**: `/document/d/<fileId>/edit` URL. `read_file_content` 본문 그대로 합류.
18. **Google Drive 폴더 URL**: `/drive/folders/<folderId>` URL. `search_files`로 자식 file list만 합류, 각 file은 별도 자식 URL 후보로 visited queue push. cap 없음 정책 그대로.
19. **인증 안 된 환경에서 Google URL**: `read_file_content` 부재. `미연결 (Google Drive connector)` + 일반 WebFetch 인증 게이트 → `인증 필요 (Google Drive connector 미연결)`.

## 10. 참고 파일

- `skills/planning-format/SKILL.md` — 본 PRD §5 반영. 0.1.2 SKILL.md에서 `## 자동 리뷰` 섹션을 `## 자체 품질 검증`으로 교체, B축 SSOT 부분 제거, `--save` 동작 추가.
- `skills/planning-format/references/self-review-rules.md` — 0.1.x `review-rules.md` A축 + 본 PRD §5.3.1 lint 항목.
- `skills/planning-format/references/connector-routing.md` — 본 PRD §5.8 반영. §2 인증 판정 보정, §3 row 4 Google Workspace tool 시퀀스·fileId 정규식·gid/range 처리 명시, §5 fallback 케이스 표 + Google 케이스 추가, §7 출처 list 상태 컬럼 Google 표기 추가.
- `skills/planning-review/SKILL.md` — 신규. 본 PRD §6 반영.
- `skills/planning-review/references/ssot-rules.md` — 0.1.x `review-rules.md` B축 그대로 옮김.
- `skills/planning-review/references/ac-rules.md` — 신규. 본 PRD §6.4.2 기준 상세화.
- `skills/planning-review/references/deps-rules.md` — 신규. 본 PRD §6.4.3 기준 상세화.
- `skills/planning-format/templates/기능설계서.md`, `templates/정책서.md` — 0.1.x 그대로.
- `docs/planning-format-workflow.md`, `docs/planning-review-workflow.md` — 신규 다이어그램 (각 스킬 단일 패스 흐름).
- `README.md` — 0.2.0 호출 예시·옵션·구성 표 갱신. product-team-kit 비교 표는 `Skill 수: 1 → 2` 등 갱신.
