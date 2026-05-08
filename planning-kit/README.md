# planning-kit

기획 초안을 **정책서·기능설계서 두 본문**으로 변환하고 자체 품질을 점검하는 `planning-format` 스킬과, 그 산출물을 **외부 SSOT 충돌·acceptance criteria·의존 영향** 3축으로 검증하는 `planning-review` 스킬로 구성된 플러그인.

산출물은 default로 화면 output(응답 markdown)으로만 반환한다. `planning-format --save`를 사용하면 `./.planning-kit/<기능명>/`에 두 본문 markdown 파일이 추가로 떨어진다 (자체 검증 보고서·출처 list는 화면 only).

Claude Code · Codex 양쪽에서 동작한다.

---

## 빠른 시작

### Claude Code

```
# 변환 + 자체 품질 검증
/planning-kit:planning-format 주문 취소 정책 정리해줘. 사용자가 결제 후 24시간 내 1회 취소 가능.

# 위 출력에 대해 외부 SSOT 충돌·AC·의존 영향 3축 점검 (직전 turn 자동 참조)
/planning-kit:planning-review
```

### Codex

```
$planning-format 주문 취소 정책 정리해줘. 사용자가 결제 후 24시간 내 1회 취소 가능.
$planning-review
```

### 입력 분기 (planning-format)

```
# 텍스트
/planning-kit:planning-format "주문 취소 정책 ..."

# 파일
/planning-kit:planning-format ./docs/draft/주문취소.md

# 디렉터리 (텍스트 + 이미지 혼합 가능)
/planning-kit:planning-format ./docs/draft/입고기능/

# URL (1개 이상)
/planning-kit:planning-format https://wiki.example/spec/order-cancel
/planning-kit:planning-format https://a.com/p1 https://b.com/p2 https://c.com/p3

# 이미지 단독 (multimodal 해석)
/planning-kit:planning-format ./diagrams/order-flow.png

# 디스크 저장
/planning-kit:planning-format ./docs/draft/주문취소.md --save
```

디렉터리 입력은 안의 모든 UTF-8 텍스트 파일과 지원 이미지 파일을 함께 읽어 통합한다. 텍스트·파일·디렉터리 분기에서도 본문에 URL이 있으면 자동 추출해 fetch하고, markdown image / HTML img / data URI도 자동으로 multimodal 해석에 합류.

### 입력 분기 (planning-review)

```
# 직전 turn의 planning-format 출력 자동 참조 (가장 흔한 흐름)
/planning-kit:planning-review

# --save로 떨어진 디렉터리
/planning-kit:planning-review ./.planning-kit/주문취소/

# 두 파일 명시
/planning-kit:planning-review ./docs/주문-정책.md ./docs/주문-기능.md

# raw markdown 텍스트
/planning-kit:planning-review "## 정책서 ... ## 기능설계서 ..."

# 점검 축 부분 활성
/planning-kit:planning-review --axes ssot
/planning-kit:planning-review --axes ssot,ac
```

---

## 결과 형태

### planning-format 출력

1. **정책서 본문** (10 섹션 markdown, 코드 펜스로 감싼 형태). 표 셀 안 list가 이질이면 부모 § 안 sub-§(`### N.x ... 보조 표`)에 분해 (0.2.3, main 판단)
2. **기능설계서 본문** (8 섹션 markdown, 코드 펜스로 감싼 형태). 표 셀 안 list가 이질이면 부모 § 안 sub-§(`### N.x ... 보조 표`)에 분해 (0.2.3, main 판단)
3. **출처 list** (URL fetch나 이미지 처리가 1건 이상일 때만)
4. **입력 제외 항목** (항상 출력. 0건이면 `없음` 1줄. 변환 본문에 반영 안 한 입력 조각을 10 카테고리로 분류 + 항목별 `처리` 줄로 본문·출처·미결 § cross-reference)
5. **자체 검증 결과** (`통과` 또는 `발견 N건`, 6개 카테고리 카운트 포함)

자체 품질 6개 카테고리 — 섹션 충실도(F1) / 라벨 cross-bleed(F2) / 용어 일관성(F3) / 정책-기능 매핑(F4) / 누락(F5, sub: `cross-ref-fetch` / `cross-ref-scope` / `cross-ref-tbd`) / Markdown syntax lint(F6).

입력 제외 10 카테고리 — `다른 기능 후보` / `라벨 미매핑` / `중복` / `근거 부족 무시` / `포맷 노이즈` / `디테일 축약` / `범위 외` / `구조 변환` / `fetch 실패` / `원문 정의 부재`. 헤더 `- 입력 제외:` 줄에 카테고리별 분포 표기.

### planning-review 출력

1. **헤더** — 입력·입력 제외 § 분리 카운트(0.2.2)·점검 축·SSOT corpus(매칭 + 외부 fetch 성공/실패)·SSOT 검색 키워드
2. **리뷰 결과** — `통과` 또는 `발견 N건`, 3축 카운트
3. **SSOT 출처** (0.2.2) — link follow 1건 이상이면 매칭 *.md + 자식 URL/이미지 표 (origin·상태·본문 사용 컬럼)
4. **발견 list** — 활성 축별 sub-section
   - **SSOT 충돌** (R1): 변환 본문 vs 다른 *.md 파일 + 매칭 *.md 본문 안 외부 link follow 본문(0.2.2) 표기·결정·임계값 어긋남
   - **검증가능성** (R2): 정량성 / 상태 / 행위자 / 결과 관찰가능성
   - **영향 분석** (R3): 정책 변경 / 상태 전이 / 권한·역할 / 외부 의존 — 발견·권고 분류. 입력 제외 § 보조 신호로 만들어진 항목은 `근거`에 cross-ref (0.2.2)

---

## 옵션

### planning-format

| 옵션 | 동작 |
|---|---|
| `--save` | `./.planning-kit/<기능명>/정책서.md`, `./.planning-kit/<기능명>/기능설계서.md` 저장. 충돌 시 `-2`/`-3` suffix. 자체 검증 보고서·출처 list·입력 제외 §은 디스크 저장 안 함 (화면 only). |
| `--no-self-review` | 자체 품질 검증 블록 출력 생략. 변환 본문 + 출처 list + 입력 제외 §은 그대로 출력 (입력 제외 §은 끄지 않음). |
| `--no-fetch` | 본문에서 URL이 발견되어도 fetch하지 않음. URL 분기 인자도 fetch 안 함. connector fallback도 봉쇄. |
| `--no-image` | 모든 이미지 시드(인자·디렉터리·추출·fetch·data URI)를 무시. multimodal 호출 0건 |

### planning-review

| 옵션 | 동작 |
|---|---|
| `--ssot-include <glob>` | SSOT corpus glob. default = 프로젝트 폴더 안 모든 `*.md` (`.git/`, `node_modules/` 자동 제외). R1·R3 corpus 공유. |
| `--axes <list>` | 점검할 축. `ssot,ac,deps` 콤마 구분. default = 셋 다 활성. |
| `--no-ssot-fetch` | SSOT corpus *.md 본문 안 외부 URL fetch + connector fallback 봉쇄. 매칭 file 본문만 corpus. (0.2.2) |
| `--no-ssot-image` | SSOT corpus 본문 안 이미지 참조·fetch image content-type 응답 multimodal 호출 0건. URL fetch는 별도 (`--no-ssot-fetch`로 봉쇄). (0.2.2) |

cap 관련 인자(`--depth`, `--max-pages`, `--max-body`, `--max-image`)는 두지 않는다 — **cap 없음 정책** (품질·검증 > 토큰 절약). cycle은 visited set으로만 차단.

---

## URL 분기·재귀 fetch + connector fallback

- 인자가 1개 이상의 `^https?://` 토큰이면 URL 분기로 진입. 모든 URL을 fetch → 본문 추출 → 통합.
- 텍스트/파일/디렉터리 분기에서도 입력 본문 안 URL을 자동 추출해 fetch.
- 추출 본문 안에 또 외부 링크가 있으면 **재귀로 따라간다** (depth·pages·body 크기 cap 없음). 호스트 제한 없음.
- visited set으로 cycle·중복 방지 (URL normalize: fragment 제거, trailing `/`, 트래킹 query 제거, 호스트 lowercase, query 키 정렬).
- **connector fallback** — 1차 `WebFetch`가 인증 게이트·4xx·5xx·timeout으로 실패하면, 호스트가 알려진 외부 서비스(Atlassian Confluence/Jira·Figma·Google Workspace·Slack·Notion)면 MCP/connector 경유 접근을 한 번 더 시도.
- **Google Workspace 자원별 tool 시퀀스** (0.2.0):
  - Docs (`/document/d/<fileId>`) → `read_file_content` → `get_file_metadata`
  - Sheets (`/spreadsheets/d/<fileId>`) → `read_file_content` → `download_file_content (text/csv)` → `get_file_metadata`
  - Slides (`/presentation/d/<fileId>`) → `read_file_content` → `get_file_metadata`
  - Drive 파일 (`/file/d/<fileId>`) → `read_file_content` → `download_file_content` → `get_file_metadata`
  - Drive 폴더 (`/folders/<folderId>`) → `search_files(parents=folderId)` → 자식 file은 별도 자식 URL 후보로 push
  - Sheets URL의 `#gid=<sheetGid>&range=<cellRange>` fragment는 시트 분리·범위 부연으로 처리
- 출처 list `상태` 컬럼에 `200 (via WebFetch)` / `200 (via Atlassian MCP)` / `200 (via Figma MCP)` / `200 (via Google Drive connector — read_file_content)` / `인증 필요 (Slack MCP 미인증)` / `인증 필요 (Google Drive connector 미연결)` 형태로 fetch 경로가 표기된다.
- 인증 게이트·지원 안 하는 content-type·timeout·4xx/5xx는 fallback까지 거친 뒤 본문 합류에서 제외하되 호출은 종료하지 않고 `## 출처` list에 사유 기록. **루트 URL이 모두 실패한 경우만** 한 줄 sanity check로 종료.

상세 명세: `skills/planning-format/SKILL.md` §3, lookup data: `skills/planning-format/references/connector-routing.md`, 다이어그램: `docs/planning-format-workflow.md`.

---

## 이미지 multimodal 처리

다음 5경로에서 이미지가 시드된다 — Claude의 내장 vision 능력으로 텍스트 설명을 생성해 통합 본문에 합류:

1. 인자 파일이 이미지 확장자일 때.
2. 디렉터리 안 지원 이미지 파일.
3. 본문의 markdown image (`![alt](path)`) / HTML img (`<img src="...">`).
4. fetch 응답이 `image/*` content-type일 때.
5. 본문 안 inline `data:image/...;base64,...` URI.

지원 확장자: `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.bmp`, `.heic`, `.svg`. 크기·개수 cap 없음. 별도 OCR·외부 vision 서비스 사용 안 함 (Claude multimodal 능력만).

상세 명세는 `skills/planning-format/SKILL.md` §4 참조.

---

## 검증 2단

### 1. 자체 품질 검증 — `planning-format` 안에서 (6 카테고리)

본문 자체와 입력만 근거. 외부 corpus 안 봄.

- **F1. 섹션 충실도**: [TBD] 비율·빈 row·빈 섹션
- **F2. 라벨 cross-bleed**: 정책서 ↔ 기능설계서 내용 어긋남
- **F3. 용어 일관성**: 역할명·상태명·권한명·도메인 stem 통일
- **F4. 정책-기능 매핑**: 정책서 규칙이 기능설계서 동작에 반영
- **F5. 누락 핵심 정보**: 입력에는 있었지만 본문에 빠진 항목
- **F6. Markdown syntax lint**: 코드 펜스 / 표 컬럼 / 헤더 레벨 / list marker

상세 기준은 `skills/planning-format/references/self-review-rules.md`.

### 2. 외부 검증 — `planning-review` 호출 시 (3축)

- **R1. SSOT 충돌**: 변환 본문 확정 문장이 프로젝트 폴더 안 다른 `*.md`와 어긋나는지. 키워드 grep → 매칭 file Read → 직접 비교. fetch한 외부 URL 본문·multimodal 이미지 해석은 corpus에 포함하지 않음(외부·일회성).
- **R2. Acceptance criteria 검증가능성**: 정책서 §5·§6, 기능설계서 §5·§7 확정 문장이 테스트 가능한 형태인지. 정량성 / 상태 / 행위자 / 결과 관찰가능성 4개 sub-category.
- **R3. 의존·영향 분석**: 이번 산출물이 다른 SSOT 문서·기능에 미치는 파급 효과. 정책 변경 / 상태 전이 / 권한·역할 / 외부 의존 4개 sub-category. `발견`(단정적 충돌) / `권고`(검토 권장) 분류.

리뷰 결과 헤더에 **SSOT 검색 키워드 list**가 그대로 노출된다 — 매칭 0건이거나 통과여도 키워드 줄은 출력 (R1 활성 시).

상세 기준은 `skills/planning-review/references/ssot-rules.md`·`ac-rules.md`·`deps-rules.md`.

---

## 구성

```
planning-kit/
├── .claude-plugin/plugin.json
├── .codex-plugin/plugin.json
├── README.md
├── docs/
│   ├── planning-format-workflow.md       # planning-format 흐름 mermaid
│   ├── planning-review-workflow.md       # planning-review 흐름 mermaid
│   └── prd/
│       ├── README.md                     # PRD chain 안내 (0.2.2 신규)
│       ├── prd-0.1.0.md
│       ├── prd-0.1.1.md
│       ├── prd-0.1.2.md
│       ├── prd-0.2.0.md                  # 스킬 분할 + Google 라우팅 fix
│       ├── prd-0.2.1.md                  # 입력 제외 10종 + 항상 출력 + F5 cross-ref
│       ├── prd-0.2.2.md                  # R1 link follow + 입력 제외 § R3 보조 신호
│       └── prd-0.2.3.md                  # 본 release (표 셀 list 분해 판단 + 보조 표 sub-§)
└── skills/
    ├── planning-format/
    │   ├── SKILL.md
    │   ├── templates/
    │   │   ├── 기능설계서.md
    │   │   └── 정책서.md
    │   └── references/
    │       ├── self-review-rules.md      # 자체 품질 6 카테고리
    │       └── connector-routing.md      # 호스트 매핑·Google tool 시퀀스·fallback 케이스
    └── planning-review/
        ├── SKILL.md
        └── references/
            ├── ssot-rules.md             # R1 SSOT 충돌
            ├── ac-rules.md               # R2 검증가능성 4 sub-category
            └── deps-rules.md             # R3 의존·영향 4 sub-category
```

---

## product-team-kit과의 차이

`planning-kit`(0.2.3)은 `product-team-kit`(`set-config` + `plan-format` + `plan-review` 3 스킬)의 흐름을 **`planning-format` + `planning-review` 두 스킬**로 재구성한다. 차이 요점:

| 항목 | product-team-kit | planning-kit (0.2.3) |
|---|---|---|
| Skill 수 | 3 | 2 |
| 변환·리뷰 호출 | 2번 (`plan-format` → `plan-review`) | 2번 (`planning-format` → `planning-review`) |
| 입력 분기 | 텍스트·파일·디렉터리 | 텍스트·파일·디렉터리·URL(다중)·이미지 |
| URL fetch / 이미지 multimodal | 없음 | 모든 분기 공통 (본문 추출 + 재귀, cap 없음). 인증 게이트는 MCP/connector fallback (Atlassian·Figma·Google Workspace·Slack·Notion). Google Workspace는 자원별 tool 시퀀스 + Sheets gid·range fragment 처리. |
| Agent worker | 1 (terminology) | 0 |
| Reference 수 | 5 | 5 (planning-format: self-review-rules + connector-routing / planning-review: ssot-rules + ac-rules + deps-rules) |
| Template 수 | 2 (정책서 + 기능설계서) | 2 (정책서 + 기능설계서) |
| 산출물 | 정책서 + 기능설계서 2 file (`<outputRoot>/.../*.md`) | 화면 output (default) + `--save` 시 `./.planning-kit/<기능명>/` 2 file |
| 파일 IO | mkdir + Write 호출 (항상) | `--save`일 때만 |
| Config 파일 | `.product-team-kit/config.json` 필수 | 없음 (default + CLI 인자) |
| `CLAUDE.md`/`AGENTS.md` upsert | 항상 | 안 함 |
| Marker | 4종 + `해당 없음` fill | 1종 (`[TBD]`) |
| Gate First | 4 조건 + 2 문서 최소 검사 | 없음 (literal 빈 입력 + URL 분기 sanity check만) |
| 빈 위치 보존 | row·셀 삭제 금지 | 삭제 허용 |
| 본문 검사 | 빈 골격/구조 일치 retry/중복/cross-bleed | 자체 6 카테고리 (planning-format 단계에서) |
| 저장 절차 | staging→write→verify→rename + collision `--01..99` | mkdir + write + collision `-2`/`-3` (planning-format `--save`) |
| 안전기능명 정규화 | 폴더명 안전화 (NFC, 특수문자 제거 등) | NFC + 분리자 제거 + 64자 cap (planning-format `--save`) |
| 출력 템플릿 | 4종 (설정없음/저장보류/저장완료/저장실패) | 5종 (변환+자체검증 / planning-review 결과 / 빈 입력 / URL 분기 sanity / 저장 실패). 입력 제외 § 항상 출력 (0건 = `없음`). 표 셀 list 이질 시 부모 § 안 sub-§(보조 표) 동적 추가 (0.2.3) |
| 입력 제외 처리 | 없음 | 10 카테고리 + 처리 줄 + R3 보조 신호 (0.2.2) |
| 리뷰 축 | 2축 (SSOT 충돌 + 용어 일관성) | 자체 6 카테고리 (F5 cross-ref 3종 포함) + 외부 3축 (R1 corpus link follow 포함). SSOT 검색 키워드 노출 |
| 리뷰 worker | B축 worker 분리 | 없음 (각 스킬 main 단일 패스) |
| SSOT corpus 처리 | 인덱스 스캔 + version + archive 분류 | grep 매칭 + 직접 read + 매칭 file 본문 안 외부 링크 재귀 fetch (cap 없음, connector fallback) |
| 검토 결과 | 3종 (통과/조건부/수정 필요) | 2종 (통과/발견 N건) |
| 출력 구조 | 2층 (상단 합의 + 하단 agent 원본) | 1층 (각 스킬 단일 응답) |
| GFM cell escape | 단일 진실 소스 알고리즘 | 없음 (numbered list) |
| 진행 표시 | step header 시퀀스 통제 | 자유 |

두 플러그인은 **별도 동작하며 병행 사용 가능**하다.

---

## 호환성

- **0.1.0 → 0.1.1 → 0.1.2**: 0.1.x 단일 `formalize` 스킬 흐름. 자세한 변경 이력은 각 PRD 참조.
- **0.1.x → 0.2.0**: **breaking change**. `formalize` 스킬 제거, `planning-format` + `planning-review` 두 스킬로 분리. 호출자 마이그레이션 필요.
  - `/planning-kit:formalize <input>` → `/planning-kit:planning-format <input>` + 필요 시 `/planning-kit:planning-review`
  - `/planning-kit:formalize <input> --no-review` → `/planning-kit:planning-format <input>` (planning-review 호출 생략)
  - `/planning-kit:formalize <input> --ssot-include "<glob>"` → `/planning-kit:planning-format <input>` → `/planning-kit:planning-review --ssot-include "<glob>"`
  - `/planning-kit:formalize <input> --no-fetch --no-image` → `/planning-kit:planning-format <input> --no-fetch --no-image`
- **0.2.0 신규**:
  - 자체 품질 검증이 `planning-format`에 흡수. F6 markdown lint 추가.
  - `--save` 옵션으로 `./.planning-kit/<기능명>/`에 두 본문 저장 가능.
  - Google Workspace connector 라우팅이 자원별 tool 시퀀스로 구체화 (이전엔 추상적이라 인증돼 있어도 fallback 후보 0이던 케이스 정정).
  - `planning-review`에 R2(검증가능성)·R3(의존·영향) 축 신규.
  - 카탈로그 평가 보정: 자원 조회 도구가 1개 이상 노출되면 인증된 것으로 간주 (`authenticate` 노출 여부 무관). 다른 connector(Atlassian·Figma·Slack·Notion)에도 일반화 적용.
- **0.2.0 → 0.2.1**: 출력 markdown micro-breaking. `planning-review`·인자·`--save`·connector 동작 변경 없음.
  - 입력 제외 § 카테고리 5종 → 10종 (`디테일 축약` / `범위 외` / `구조 변환` / `fetch 실패` / `원문 정의 부재` 추가).
  - 입력 제외 § 블록 항상 출력 (0건 = `없음`). 0.2.0의 "≥1건일 때만" 정책 deprecated.
  - 항목 형식에 `처리` 줄 추가 (4필드 → 5필드). 변환 본문·출처 list·미결 § cross-reference 위치를 1줄로 명시.
  - 헤더 `- 입력 제외:` 줄에 카테고리 분포 괄호 표기.
  - 자체 검증 F5(누락)에 cross-reference 3종 추가 (`cross-ref-fetch` / `cross-ref-scope` / `cross-ref-tbd`). 본문 누락 + 추적 누락 모두 발견.
- **0.2.1 → 0.2.2**: `planning-review` 출력 markdown micro-breaking. `planning-format` 동작·인자·출력 변경 없음.
  - **R1 SSOT corpus link follow** — 매칭 *.md 본문 안 외부 URL을 자동 fetch + connector fallback (`connector-routing.md` 공유 적재)으로 corpus body에 합류. 트리거: R1 또는 R3 활성 + 매칭 ≥1 + `--no-ssot-fetch` off.
  - 신규 옵션 `--no-ssot-fetch` / `--no-ssot-image`. 둘 다 ON이면 0.2.1 동작과 동등.
  - `## SSOT 출처` 블록 신규 (link follow 1건 이상일 때만). 매칭 *.md + 자식 URL/이미지 + origin·상태·본문 사용 컬럼.
  - `planning-review`가 입력 제외 § 분리 + R3 영향 후보 산출의 **보조 신호**로 활용 (`fetch 실패` / `범위 외` / `구조 변환` / `디테일 축약` 신호, `원문 정의 부재` + 5종 무관). 헤더 `입력 제외 §:` 줄 신규.
  - `SSOT corpus:` 줄에 외부 fetch 카운트 추가 (`매칭 N개 + 외부 fetch 성공 K개 / 실패 J개 (총 시도 K+J건, cap 없음)`).
  - Codex `plugin.json` longDescription 압축 (~700자 → ≤300자).
  - PRD chain 안내 (`docs/prd/README.md` 신규).
- **0.2.2 → 0.2.3**: `planning-format` 출력 markdown **추가만** (sub-§). 인자·옵션·`planning-review` 변경 없음.
  - **list 분해 판단** — 표 셀에 list 항목 ≥2 합류 작성 시 main이 항목별 속성·동작·정책 ref 이질성을 매 케이스 판단. 이질이면 부모 § 안 sub-§(`### N.x [용도] 보조 표`)로 분해, 동질 enum·동일 동작·동일 ref면 합류 유지. 보조 표 안 셀이 또 list 합류면 다층 재귀(`### N.x.y`, depth cap 없음).
  - 판단 형식화(Q-list·체크리스트·카운트 룰) 없음 — main 자유 판단.
  - 8/10 섹션 골격 변경 없음. sub-§만 동적 추가.
  - 다운스트림 파서: 부모 § 안 sub-§을 child로 인식해야 함.

---

## 라이선스

MIT
