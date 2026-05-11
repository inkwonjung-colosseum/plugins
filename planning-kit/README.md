# planning-kit (0.2.8)

기획 초안을 **정책서·기능설계서 두 본문**으로 변환하고 자체 품질을 점검하는 `planning-format`, 그 산출물을 **외부 SSOT 충돌·acceptance criteria·의존 영향** 3축으로 검증하는 `planning-review`, 현재 프로젝트의 Markdown **SSOT corpus 자체를 구조·내용 2축으로 감사**하는 `ssot-audit` 세 스킬로 구성된 플러그인. 0.2.7부터 `ssot-audit`가 추가되고, `planning-review <단일 파일>`은 같은 폴더 sibling 파일을 non-recursive로 함께 읽어 정책서·기능설계서 쌍을 식별한다. 0.2.8부터 `planning-format` 신규 출력의 보조 표 헤더는 내부 backlink 없는 clean header만 사용하고, 부모 §/row 추적 정보는 `## 입력 제외 항목`의 `구조 변환` 처리 줄에 기록한다.

산출물은 default로 화면 output(응답 markdown)으로만 반환한다. `planning-format --save`를 사용하면 `./.planning-kit/<기능명>/`에 두 본문 markdown 파일이 추가로 떨어진다 (자체 검증 보고서·출처 list는 화면 only). `ssot-audit`는 저장 옵션 없이 항상 화면 output only다.

Claude Code · Codex 양쪽에서 동작한다.

---

## 빠른 시작

### Claude Code

```
# 변환 + 자체 품질 검증
/planning-kit:planning-format 주문 취소 정책 정리해줘. 사용자가 결제 후 24시간 내 1회 취소 가능.

# 위 출력에 대해 외부 SSOT 충돌·AC·의존 영향 3축 점검 (직전 turn 자동 참조)
/planning-kit:planning-review

# 프로젝트 문서 corpus 자체의 구조·내용 품질 감사
/planning-kit:ssot-audit
```

### Codex

```
$planning-format 주문 취소 정책 정리해줘. 사용자가 결제 후 24시간 내 1회 취소 가능.
$planning-review
$ssot-audit
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

# 단일 파일 입력 (같은 폴더 sibling 파일을 함께 읽음)
/planning-kit:planning-review ./.planning-kit/주문취소/정책서.md

# 두 파일 명시
/planning-kit:planning-review ./docs/주문-정책.md ./docs/주문-기능.md

# raw markdown 텍스트
/planning-kit:planning-review "## 정책서 ... ## 기능설계서 ..."

# URL (1개 이상, 정책서·기능설계서가 서로 다른 링크여도 가능)
/planning-kit:planning-review https://wiki.example/policy/order-cancel
/planning-kit:planning-review https://wiki.example/policy/order-cancel https://docs.example/feature/order-cancel

# 점검 축 부분 활성
/planning-kit:planning-review --axes ssot
/planning-kit:planning-review --axes ssot,ac
```

URL 입력은 `planning-format`과 같은 규칙으로 root URL fetch, 본문 URL 재귀 fetch, connector fallback, 이미지 multimodal 처리를 수행한다. 입력 URL fetch는 review 대상 본문 생성용이며, R1/R3의 SSOT corpus link follow와 visited set·출처 블록이 분리된다. 단일 파일 입력은 해당 파일만 보지 않고 같은 폴더의 읽을 수 있는 sibling 텍스트/지원 이미지 파일을 non-recursive로 함께 읽어 한 쌍을 찾는다.

### 입력 분기 (ssot-audit)

```
# 프로젝트 전체 Markdown SSOT 감사
/planning-kit:ssot-audit

# docs 하위만 감사
/planning-kit:ssot-audit --ssot-include "docs/**/*.md"

# archive 제외 + 구조 품질만 감사
/planning-kit:ssot-audit --exclude "docs/archive/**" --axes structure

# 외부 링크와 이미지 해석 없이 로컬 Markdown만 감사
/planning-kit:ssot-audit --no-follow-links --no-image
```

기본 corpus는 프로젝트 폴더 안 모든 `*.md`이며 `.git/`, `node_modules/`는 제외한다. 제목/파일명/H1/마지막 path segment의 버전 신호가 `v0.8` 이상이거나 버전이 없으면 SSOT 후보로 남기고, `v0.8` 미만 문서는 `SSOT 제외 문서`로 집계한다.

---

## 결과 형태

### planning-format 출력

1. **정책서 본문** (10 섹션 markdown, 코드 펜스로 감싼 형태). 표 셀 안 list가 이질이면 부모 § 안 sub-§(`### N.M ... 보조 표`)에 분해 (0.2.3, main 판단). 0.2.8부터 보조 표 헤더에는 `(§N row M)` 같은 내부 backlink를 쓰지 않는다.
2. **기능설계서 본문** (8 섹션 markdown, 코드 펜스로 감싼 형태). 표 셀 안 list가 이질이면 부모 § 안 sub-§(`### N.M ... 보조 표`)에 분해 (0.2.3, main 판단). 부모 §/row 추적은 입력 제외 항목의 `구조 변환` 처리 줄에 둔다.
3. **출처 list** (URL fetch나 이미지 처리가 1건 이상일 때만)
4. **입력 제외 항목** (항상 출력. 0건이면 `없음` 1줄. 변환 본문에 반영 안 한 입력 조각을 11 카테고리로 분류 + 항목별 `처리` 줄로 본문·출처·미결 § cross-reference)
5. **자체 검증 결과** (`통과` 또는 `발견 N건`, 6개 카테고리 카운트 포함)

자체 품질 6개 카테고리 — 섹션 충실도(F1) / 라벨 cross-bleed(F2) / 용어 일관성(F3) / 정책-기능 매핑(F4) / 누락(F5, sub: `cross-ref-fetch` / `cross-ref-scope` / `cross-ref-tbd`) / Markdown syntax lint(F6). F1·F2는 sub-§(보조 표) 본문도 점검 (0.2.4). 0.2.8부터 신규 출력에 legacy backlink header가 남으면 F6 syntax 발견으로 잡는다.

입력 제외 11 카테고리 — `다른 기능 후보` / `라벨 미매핑` / `중복` / `근거 부족 무시` / `포맷 노이즈` / `디테일 축약` / `범위 외` / `구조 변환` / `fetch 실패` / `원문 정의 부재` / `충돌 후보`(0.2.4 신규). 헤더 `- 입력 제외:` 줄에 카테고리별 분포 표기. 위치 필드는 `[출처 N](URL#anchor)` markdown link 형식으로 외부 source 특정 위치까지 1-hop 점프 (0.2.4).

### planning-review 출력

1. **헤더** — 입력·입력 처리(0.2.6)·입력 제외 § 분리 카운트(0.2.2)·점검 축·SSOT corpus(매칭 + 외부 fetch 성공/실패)·SSOT 검색 키워드
2. **리뷰 결과** — `통과` 또는 `발견 N건`, 3축 카운트
3. **입력 출처** (0.2.6) — input fetch 또는 input image 1건 이상이면 입력 root URL + 입력 자식 URL/이미지 표 (origin·상태·본문 사용 컬럼)
4. **SSOT 출처** (0.2.2) — link follow 1건 이상이면 매칭 *.md + 자식 URL/이미지 표 (origin·상태·본문 사용 컬럼)
5. **발견 list** — 활성 축별 sub-section
   - **SSOT 충돌** (R1): 변환 본문 vs 다른 *.md 파일 + 매칭 *.md 본문 안 외부 link follow 본문(0.2.2) 표기·결정·임계값 어긋남
   - **검증가능성** (R2): 정량성 / 상태 / 행위자 / 결과 관찰가능성
   - **영향 분석** (R3): 정책 변경 / 상태 전이 / 권한·역할 / 외부 의존 — 발견·권고 분류. 입력 제외 § 보조 신호로 만들어진 항목은 `근거`에 cross-ref (0.2.2)

### ssot-audit 출력

1. **헤더** — SSOT 범위, 제외 glob, 분석 축, 외부 링크 처리, 이미지 처리, 로컬 Markdown 수, `SSOT 제외(낮은 버전)` 수, 외부 fetch 성공/실패
2. **감사 결과** — 구조 품질·내용 품질별 발견/권고 카운트
3. **SSOT 인벤토리** — `v0.8` 미만 제외 후 role별 문서 수와 대표 문서
4. **SSOT 제외 문서** — 낮은 버전(`< v0.8`) 문서가 있을 때만 출력
5. **외부 출처** — 외부 follow 또는 image 처리 1건 이상이면 origin·상태·본문 사용 표
6. **구조 품질 / 내용 품질** — 발견/권고 항목. 0건이면 `없음`
7. **개선 backlog** — 문제 단위로 묶은 P0/P1/P2 권장 작업과 검증 조건

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
| `--no-input-fetch` | review 대상 입력 URL fetch + 본문 URL fetch + connector fallback 봉쇄. URL-only 입력이면 본문 식별 불가 sanity check. |
| `--no-input-image` | review 대상 입력 이미지 multimodal 호출 0건. URL fetch는 그대로 진행하되 image content-type 응답은 본문 합류하지 않음. |
| `--no-ssot-fetch` | SSOT corpus *.md 본문 안 외부 URL fetch + connector fallback 봉쇄. 매칭 file 본문만 corpus. (0.2.2) |
| `--no-ssot-image` | SSOT corpus 본문 안 이미지 참조·fetch image content-type 응답 multimodal 호출 0건. URL fetch는 별도 (`--no-ssot-fetch`로 봉쇄). (0.2.2) |

### ssot-audit

| 옵션 | 동작 |
|---|---|
| `--ssot-include <glob>` | SSOT corpus 후보 glob. default = 프로젝트 폴더 안 모든 `*.md` (`.git/`, `node_modules/` 제외). |
| `--exclude <glob>` | corpus 후보 제외 glob. 반복 지정 또는 comma 구분 허용. |
| `--axes <list>` | 감사 축. `structure,content` 콤마 구분. default = 둘 다 활성. |
| `--no-follow-links` | Markdown 안 외부 URL fetch + connector fallback 봉쇄. 로컬 Markdown만 분석. |
| `--no-image` | 로컬/외부 이미지 multimodal 해석 0건. URL fetch는 유지하되 image content-type 응답은 본문 합류하지 않음. |

cap 관련 인자(`--depth`, `--max-pages`, `--max-body`, `--max-image`)는 두지 않는다 — **cap 없음 정책** (품질·검증 > 토큰 절약). cycle은 visited set으로만 차단.

---

## URL 분기·재귀 fetch + connector fallback

- `planning-format`과 `planning-review` 모두 인자가 1개 이상의 `^https?://` 토큰이면 URL 분기로 진입한다. 모든 URL을 fetch → 본문 추출 → 통합한다.
- `planning-review` URL 분기의 모든 URL은 review 대상 본문을 만드는 depth 0 root input source다. 이 input fetch는 SSOT corpus link follow가 아니다.
- `ssot-audit`는 로컬 Markdown 안에서 발견한 외부 URL을 root URL로 삼아 기본 follow한다.
- 텍스트/파일/디렉터리 분기에서도 입력 본문 안 URL을 자동 추출해 fetch한다. `planning-review`도 0.2.6부터 같은 input collection을 수행한다.
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
- 인증 게이트·지원 안 하는 content-type·timeout·4xx/5xx는 fallback까지 거친 뒤 본문 합류에서 제외하되 호출은 종료하지 않고 출처 list에 사유 기록. `planning-format`과 `planning-review`는 **입력 루트 URL이 모두 실패한 경우만** 한 줄 sanity check로 종료한다. `ssot-audit`는 외부 URL이 모두 실패해도 로컬 Markdown 기준으로 감사를 계속하고 실패 행을 `## 외부 출처`에 남긴다. `planning-format`은 `## 출처`, `planning-review` input collection은 `## 입력 출처`, SSOT link follow는 `## SSOT 출처`, `ssot-audit`는 `## 외부 출처`에 기록한다.

상세 명세: `skills/planning-format/SKILL.md` §3, `skills/planning-review/SKILL.md` Step 1.2, `skills/ssot-audit/SKILL.md` Step 4. lookup data는 `skills/planning-format/references/connector-routing.md`를 공유한다.

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

## 검증 3단

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

- **R1. SSOT 충돌**: 변환 본문 확정 문장이 프로젝트 폴더 안 다른 `*.md`와 어긋나는지. 키워드 grep → 매칭 file Read → 직접 비교. R1/R3 활성 + 매칭 ≥1 + `--no-ssot-fetch` off이면 매칭 file 안 외부 URL도 재귀 fetch + connector fallback으로 corpus에 합류한다(0.2.2). sub-§ 본문 포함 (0.2.4).
- **R2. Acceptance criteria 검증가능성**: 정책서 §5·§6, 기능설계서 §5·§7 + 그 안 sub-§(보조 표) 확정 문장이 테스트 가능한 형태인지 (0.2.4). 정량성 / 상태 / 행위자 / 결과 관찰가능성 4개 sub-category.
- **R3. 의존·영향 분석**: 이번 산출물이 다른 SSOT 문서·기능에 미치는 파급 효과. 정책 변경 / 상태 전이 / 권한·역할 / 외부 의존 4개 sub-category. 영향 후보 키워드는 부모 § + sub-§ 합집합에서 추출 (0.2.4). `발견`(단정적 충돌) / `권고`(검토 권장) 분류.

리뷰 결과 헤더에 **SSOT 검색 키워드 list**가 그대로 노출된다 — 매칭 0건이거나 통과여도 키워드 줄은 출력 (R1 활성 시).

상세 기준은 `skills/planning-review/references/ssot-rules.md`·`ac-rules.md`·`deps-rules.md`.

### 3. SSOT corpus 감사 — `ssot-audit` 호출 시 (2축)

- **구조 품질**: canonical 중복/부재, archive·낮은 버전 활성 참조, 도메인 문서 흩어짐, 문서 역할 불명확, 외부 canonical 의존을 점검한다.
- **내용 품질**: 정책/상태/권한/임계값 충돌, 용어 불일치, 미결/모호 표현, 검증 가능한 조건 부재, 설명 없는 중복을 점검한다.

`ssot-audit`는 새 산출물 리뷰가 아니라 프로젝트 문서 corpus 자체의 유지보수 backlog를 만들기 위한 감사다. 상세 기준은 `skills/ssot-audit/references/structure-rules.md`·`content-rules.md`·`output-contract.md`.

---

## 구성

```
planning-kit/
├── .claude-plugin/plugin.json
├── .codex-plugin/plugin.json
├── README.md
├── docs/
│   ├── planning-kit-install-guide-windows.md # Windows 기획팀 설치 가이드
│   ├── planning-kit-presentation.md      # Confluence 운영 가이드
│   ├── planning-kit-workflow-guide.md    # 발표용 workflow 해설
│   ├── planning-format-workflow.md       # planning-format 흐름 mermaid
│   ├── planning-review-workflow.md       # planning-review 흐름 mermaid
│   ├── diagram/
│   │   ├── README.md                     # planning-kit docs Mermaid 변환 산출물 index
│   │   └── *.html                        # standalone HTML/SVG 다이어그램
│   └── prd/
│       ├── README.md                     # PRD chain 안내 (0.2.2 신규)
│       ├── prd-0.1.0.md
│       ├── prd-0.1.1.md
│       ├── prd-0.1.2.md
│       ├── prd-0.2.0.md                  # 스킬 분할 + Google 라우팅 fix
│       ├── prd-0.2.1.md                  # 입력 제외 10종 + 항상 출력 + F5 cross-ref
│       ├── prd-0.2.2.md                  # R1 link follow + 입력 제외 § R3 보조 신호
│       ├── prd-0.2.3.md                  # 표 셀 list 분해 판단 + 보조 표 sub-§
│       ├── prd-0.2.4.md                  # sub-§ 정밀화·SKILL 분해·deep link·11 카테고리
│       ├── prd-0.2.5.md                  # 결정성 강화 7 항목
│       ├── prd-0.2.6.md                  # planning-review input fetch parity
│       ├── prd-0.2.7.md                  # ssot-audit + companion read
│       └── prd-0.2.8.md                  # 본 release (clean header + 구조 변환 trace 이동)
└── skills/
    ├── planning-format/
    │   ├── SKILL.md                      # orchestration only (0.2.4) + Step 3 fetch 시도 의무·BFS / Step 6·7 결정 트리·체크리스트 (0.2.5) + clean header (0.2.8)
    │   ├── templates/
    │   │   ├── 기능설계서.md
    │   │   └── 정책서.md
    │   └── references/
    │       ├── conversion-rules.md       # multimodal·통합 본문·기능명·라벨 매핑·list 분해 판단·보조 표 번호·clean header (0.2.8) + §4 라벨 매핑 결정 트리 + §4.2 양 매핑 분배 + §5.4 max-depth cap=3 (0.2.5)
    │       ├── exclusion-rules.md        # 11 카테고리·5필드(위치 markdown link)·처리 줄·우선순위·marker 1종 (0.2.4) + 구조 변환 본문/부모 위치 추적 (0.2.8)
    │       ├── output-contract.md        # 출력 포맷·헤더 줄·--save·출처 list deep link + clean header 출력 계약 (0.2.8)
    │       ├── self-review-rules.md      # 자체 품질 6 카테고리 (F1·F2 sub-§ 인식) + F1~F6 27 항목 체크리스트 6패스 (0.2.8)
    │       └── connector-routing.md      # 호스트 매핑·Google tool 시퀀스·fallback·§11 connector별 anchor 추출 (0.2.4) + §5 진입 조건 1차 WebFetch 시도 후 통일 (0.2.5)
    ├── planning-review/
    │   ├── SKILL.md                      # input collection 0.2.6 + companion read 0.2.7 + 외부 검증 orchestration
    │   └── references/
    │       ├── ssot-rules.md             # R1 SSOT 충돌
    │       ├── ac-rules.md               # R2 검증가능성 4 sub-category
    │       └── deps-rules.md             # R3 의존·영향 4 sub-category
    └── ssot-audit/
        ├── SKILL.md                      # SSOT corpus 구조·내용 감사 orchestration
        └── references/
            ├── structure-rules.md        # 구조 품질 감사 기준
            ├── content-rules.md          # 내용 품질 감사 기준
            └── output-contract.md        # 화면 output + backlog 계약
```

---

## product-team-kit과의 차이

`planning-kit`(0.2.8)은 `product-team-kit`(`set-config` + `plan-format` + `plan-review` 3 스킬)의 흐름을 **`planning-format` + `planning-review` + `ssot-audit` 세 스킬**로 재구성한다. 차이 요점:

| 항목 | product-team-kit | planning-kit (0.2.8) |
|---|---|---|
| Skill 수 | 3 | 3 |
| 변환·리뷰 호출 | 2번 (`plan-format` → `plan-review`) | 2번 (`planning-format` → `planning-review`) + 필요 시 `ssot-audit` |
| 입력 분기 | 텍스트·파일·디렉터리 | `planning-format`: 텍스트·파일·디렉터리·URL(다중)·이미지. `planning-review`: conversation·파일·디렉터리·단일 파일 companion read·raw markdown·URL(다중)·이미지 input collection. `ssot-audit`: 프로젝트 Markdown corpus glob |
| URL fetch / 이미지 multimodal | 없음 | 모든 분기 공통 (본문 추출 + 재귀, cap 없음). 인증 게이트는 MCP/connector fallback (Atlassian·Figma·Google Workspace·Slack·Notion). Google Workspace는 자원별 tool 시퀀스 + Sheets gid·range fragment 처리. |
| Agent worker | 1 (terminology) | 0 |
| Reference 수 | 5 | 11 (planning-format 5 / planning-review 3 / ssot-audit 3) |
| Template 수 | 2 (정책서 + 기능설계서) | 2 (정책서 + 기능설계서) |
| 산출물 | 정책서 + 기능설계서 2 file (`<outputRoot>/.../*.md`) | 화면 output (default) + `planning-format --save` 시 `./.planning-kit/<기능명>/` 2 file. `ssot-audit`는 화면 output only |
| 파일 IO | mkdir + Write 호출 (항상) | `--save`일 때만 |
| Config 파일 | `.product-team-kit/config.json` 필수 | 없음 (default + CLI 인자) |
| `CLAUDE.md`/`AGENTS.md` upsert | 항상 | 안 함 |
| Marker | 4종 + `해당 없음` fill | 1종 (`[TBD]`) |
| Gate First | 4 조건 + 2 문서 최소 검사 | 없음 (literal 빈 입력 + URL 분기 sanity check만) |
| 빈 위치 보존 | row·셀 삭제 금지 | 삭제 허용 |
| 본문 검사 | 빈 골격/구조 일치 retry/중복/cross-bleed | 자체 6 카테고리 (planning-format 단계에서) |
| 저장 절차 | staging→write→verify→rename + collision `--01..99` | mkdir + write + collision `-2`/`-3` (planning-format `--save`) |
| 안전기능명 정규화 | 폴더명 안전화 (NFC, 특수문자 제거 등) | NFC + 분리자 제거 + 64자 cap (planning-format `--save`) |
| 출력 템플릿 | 4종 (설정없음/저장보류/저장완료/저장실패) | 6종 (변환+자체검증 / planning-review 결과+입력 출처(0.2.6) / ssot-audit 감사 결과+backlog / 빈 입력 / URL 분기 sanity / 저장 실패). 입력 제외 § 항상 출력 (0건 = `없음`). 표 셀 list 이질 시 부모 § 안 sub-§(보조 표) 동적 추가 (0.2.3) — 보조 표 번호 부모 § 안 순차(`§N.1`·`§N.2`) + clean header (0.2.8) — list 분해 max-depth cap=3 (0.2.5) |
| 입력 제외 처리 | 없음 | 11 카테고리 (`충돌 후보` 0.2.4 신규) + 처리 줄 + 위치 markdown link (0.2.4) + R3 보조 신호 (0.2.2) — 결정 트리 + 모호성 강제 [TBD] (정규식 6 + 16 어구) (0.2.5) |
| 결정성 (같은 입력 일치율) | — | 0.9% (0.2.4) → 25~39% (0.2.5, 28~43배). fetch 시도 의무화·BFS 순서·exclusion 결정 트리·모호성 [TBD]·max-depth cap·6패스 체크리스트·라벨 매핑 트리 (0.2.5 신규 7 항목) |
| 리뷰 축 | 2축 (SSOT 충돌 + 용어 일관성) | 자체 6 카테고리 (F5 cross-ref 3종 포함) + 외부 3축 (R1 corpus link follow 포함). SSOT 검색 키워드 노출 |
| 리뷰 worker | B축 worker 분리 | 없음 (각 스킬 main 단일 패스) |
| SSOT corpus 처리 | 인덱스 스캔 + version + archive 분류 | `planning-review`: grep 매칭 + 직접 read + 매칭 file 본문 안 외부 링크 재귀 fetch. `ssot-audit`: 프로젝트 Markdown corpus 전체 수집 + `v0.8` 미만 제외 + 외부 링크 follow + 구조/내용 감사 |
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
- **0.2.3 → 0.2.4**: 출력 markdown **추가·micro-change**. 인자 변경 없음, `planning-review` 동작 변경 없음 (sub-§ 인식 외).
  - **sub-§ 정밀화** — 보조 표 번호 부모 § 안 순차 부여(`§N.1`·`§N.2`, 다층 도트 chain `§N.M.K`, 임의 letter 금지). 헤더 backlink (`### 4.1 ... (§4 row 3)`) — row 식별 못 하면 부모 §만. `구조 변환` 처리 줄에 sub-§ 위치 명시 (`정책서 §5.1·§5.2`).
  - **검증 sub-§ 인식** — `planning-format` F1·F2 자체 검증, `planning-review` R1·R2·R3 외부 검증 모두 sub-§(`### N.M ... 보조 표`) 본문을 점검 대상으로 인식. 부모 § 룰 그대로 sub-§ 확장.
  - **SKILL.md 분해** — `planning-format/SKILL.md` orchestration only (~120 line). 세부 룰 3종 신규 reference로 split: `conversion-rules.md`(multimodal·통합 본문·기능명·라벨 매핑·list 분해 판단·보조 표 번호·backlink) / `exclusion-rules.md`(11 카테고리·5필드·처리 줄·우선순위) / `output-contract.md`(출력 포맷·헤더 줄·`--save`·출처 list deep link). lazy read.
  - **입력 제외 § + 출처 list deep link** — `## 출처` list URL이 page-level → deep link 형식(`URL#취소-정책` / `#heading=h.xyz` 등). 입력 제외 § 5필드 위치 필드 = `[출처 N](URL)` markdown link. 정책서·기능설계서 본문은 cite 없음 (결정문서 깨끗 유지).
  - **connector별 anchor 추출** (Confluence·Docs·Slides·Notion 4종 신규) — `connector-routing.md` §11. Sheets·Figma·Slack은 0.1.x부터 이미 지원. 추출 실패 = page-level URL fallback.
  - **충돌 후보 카테고리 추가** — 입력 제외 § 11 카테고리(#11 끝 배치). 같은 사실 ≥2 다른 값 시 1순위 합류 + 나머지 추적. 본문 셀 1순위 미명확 = `[TBD]` + cross-ref. marker 1종(`[TBD]`) 정책 유지.
  - **신규 인자·옵션 0건**. 기존 인자·옵션·planning-review 동작·재귀 fetch·multimodal·sanity check 그대로 (sub-§ 인식 + connector anchor 추출 외).
  - 다운스트림 파서 영향: 보조 표 헤더 backlink 괄호 + 입력 제외 § 위치 필드 markdown link + 출처 list URL deep link fragment + `충돌 후보` 카테고리.
- **0.2.4 → 0.2.5**: 결정성 강화. 인자·출력 markdown 형식·`planning-review` 동작 변경 없음. 같은 입력 N회 실행 시 산출물 일치율을 0.9% → 25~39%(28~43배) 개선.
  - **fetch 시도 의무화** — queue dequeue된 visited 미포함 URL은 100% fetch 시도 강제. 사전 판단(인증 미연결·매핑 없음·미인증 추정)으로 시도 자체를 생략 금지. 시도 후 실패는 출처 list `상태` 컬럼 기록 + visited 등록. fetch 미시도 허용은 `--no-fetch` 단 1케이스. dequeue된 모든 URL은 출처 list 1행 차지 (행 누락 금지).
  - **BFS 순서 강제** — depth N 모두 dequeue 완료 후 depth N+1 dequeue. 같은 depth 안에선 본문 발견 순서 (markdown link → HTML href → plain URL). LIFO·우선순위 휴리스틱 금지. 출처 list `#` 번호 = BFS dequeue 순서.
  - **exclusion 11 카테고리 결정 트리** — `exclusion-rules.md` §2 우선순위를 11 분기 if-elif chain으로 룰화. 라벨 미매핑은 단일 폴백(분기 11)으로 이동, 그 외 카테고리 우선순위는 그대로. main 자유 판단을 syntactic feature 진입 조건으로 대체.
  - **모호성 강제 [TBD] 룰** — 원문 syntactic 결함(괄호 미닫힘 `\([^)]*$` / 말줄임표 / 빈 list / 공란 row / 16 어구 / `[ ]`·`_____`·`—` 단독) 자동 [TBD] 단정. LLM 추론 단정 금지. 16 어구 카탈로그 = TBD/TODO/FIXME · 추후 정의/결정/협의 · 별도 정의/협의/확정 · 확정 시 재정의 · 미정/미확정/미결 · 기획 시 정의.
  - **list 분해 max-depth cap = 3** — `conversion-rules.md` §5.4. 허용 depth = `§N.M`·`§N.M.K`·`§N.M.K.L`. depth 4 진입 시도 시 합류 유지 폴백 + 입력 제외 § `디테일 축약` 항목 추가. cap 없음 정책의 단일 예외.
  - **self-review F1~F6 체크리스트화** — `self-review-rules.md`에 카테고리별 yes/no 체크리스트 (F1: 5 + F2: 4 + F3: 4 + F4: 4 + F5: 4 + F6: 5 = 26 항목). 6패스 진행 (카테고리당 1패스). 단일 LLM 패스 → 6패스로 검출 누락 차단.
  - **라벨 매핑 룰 강화** — `conversion-rules.md` §4.1 결정 트리 (9 분기) + §4.2 양 매핑 분배 룰 (권한·연동·상태 측면별 위치 분배표 6 row). F2 cross-bleed 룰 그대로.
  - **신규 인자·옵션 0건**. 기존 인자·옵션·planning-review 동작·재귀 fetch·multimodal·sanity check 그대로.
  - 다운스트림 파서 영향: 출처 list 항목 수가 늘어날 수 있음 (이전 미시도 URL이 행으로 기록됨). 분해 깊이 4 이상 산출물은 cap 폴백.
- **0.2.5 → 0.2.6**: `planning-review` 입력 처리 parity. `planning-format` 동작·출력은 동일, `planning-review` 출력 markdown은 micro-breaking.
  - **다중 URL 입력 허용** — `/planning-kit:planning-review https://policy ... https://feature ...` 형태를 URL 분기로 처리. 모든 URL은 depth 0 root input source.
  - **input collection 추가** — review 입력도 URL 추출·재귀 fetch·connector fallback·image multimodal·통합 본문 합류를 `planning-format` Step 1~5와 같은 규칙으로 수행.
  - **input fetch와 SSOT fetch 분리** — review 대상 본문 생성용 input fetch와 R1/R3 비교 corpus 확장용 SSOT fetch는 별도 visited set·출처 블록을 사용.
  - **신규 옵션** — `--no-input-fetch` / `--no-input-image`. 기존 `--no-ssot-fetch` / `--no-ssot-image`는 SSOT corpus에만 적용.
  - **출력 추가** — 헤더 `입력 처리:` 줄과 조건부 `## 입력 출처` 블록 추가. `## 입력 출처`는 `## 리뷰 결과` 다음, `## SSOT 출처` 앞에 위치.
  - **본문 식별 fallback** — fetch된 root source의 title/path/URL label이 정책서·기능설계서를 명확히 가리키면 source 단위 fallback 배정 가능.
- **0.2.6 → 0.2.7**: `ssot-audit` 신규 스킬 + `planning-review` 단일 파일 입력 확장. 기존 `planning-format` 동작은 동일.
  - **ssot-audit 추가** — 프로젝트 폴더 안 모든 `*.md`를 기본 corpus로 수집하고 `.git/`, `node_modules/`는 제외. `--ssot-include`, `--exclude`, `--axes`, `--no-follow-links`, `--no-image` 지원.
  - **버전 기준선 필터** — title/filename/H1/path segment의 버전 신호가 `v0.8` 이상이거나 버전 없음이면 SSOT 후보. `v0.8` 미만은 내용 비교에서 제외하고 `SSOT 제외 문서`로 집계.
  - **구조·내용 2축 감사** — canonical 중복/부재, archive·낮은 버전 활성 참조, 외부 canonical 의존, 정책/상태/권한/임계값 충돌, 용어 불일치, 검증 조건 부재를 발견/권고로 출력.
  - **개선 backlog** — 발견/권고를 문제 단위 P0/P1/P2로 묶고 영향 문서, 권장 작업, 검증 조건을 출력.
  - **planning-review companion read** — 단일 파일 입력 시 같은 폴더 sibling 파일을 non-recursive로 함께 읽어 정책서·기능설계서 쌍을 식별. 여러 기능이 섞여 1쌍으로 좁힐 수 없으면 sanity check.
- **0.2.7 → 0.2.8**: `planning-format` 보조 표 헤더 정리. `planning-review`와 `ssot-audit` 기본 책임은 동일.
  - **clean header** — 신규 출력 보조 표 헤더는 `### N.M [용도] 보조 표`만 허용. `(§N row M)` 같은 내부 backlink 괄호를 본문 헤더에 남기지 않는다.
  - **구조 변환 추적 이동** — 부모 §/row 정보는 `## 입력 제외 항목`의 `구조 변환` 처리 줄에 `본문 위치`와 `부모 위치`로 기록한다.
  - **저장 결과 정리** — `planning-format --save`로 저장되는 정책서·기능설계서 본문에는 내부 backlink 메타데이터가 없다. 입력 제외/출처는 기존처럼 화면 only다.
  - **legacy read 호환** — `planning-review`는 0.2.4~0.2.7 legacy backlink header와 0.2.8 clean header를 모두 보조 표로 인식한다.
  - **self-review 보강** — 신규 `planning-format` 출력에서 legacy backlink header가 남으면 F6 syntax 발견으로 기록한다.

---

## 라이선스

MIT
