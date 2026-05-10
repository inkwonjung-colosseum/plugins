---
name: planning-review
description: "planning-format 산출물(정책서·기능설계서 두 본문)을 외부 SSOT corpus 충돌·acceptance criteria 검증가능성·의존 영향 분석 3축으로 점검할 때 사용한다. 직전 turn의 planning-format 출력, 디렉터리·파일 경로, raw markdown 텍스트, 1개 이상의 URL 입력을 모두 받는다."
argument-hint: "[<URL... | 정책서·기능설계서 경로 | 디렉터리 | raw markdown>] [--ssot-include <glob>] [--axes <list>] [--no-input-fetch] [--no-input-image] [--no-ssot-fetch] [--no-ssot-image]"
---

# planning-review

## 인자

위치 인자:

- **0개** = conversation 참조 모드. 직전 turn의 `planning-format` 출력에서 두 본문 추출.
- **1개 이상이고 모든 비어 있지 않은 토큰이 `^https?://`** = URL 분기. 모든 URL을 depth 0 root input source로 fetch한다. 다중 URL 허용.
- **1개 (디렉터리)** = `정책서*.md` + `기능설계서*.md` 자동 검색. 디렉터리 안 지원 이미지 파일도 input image queue 시드.
- **1개 (파일)** = 본문 안 두 섹션 자동 분리. 이미지 확장자면 input image queue 단독 시드.
- **2개 non-URL path** = `<정책서> <기능설계서>` 또는 역순 (헤더/파일명으로 자동 식별).
- **그 외** = raw markdown 텍스트 분기. URL 토큰과 비-URL 토큰이 섞이면 `planning-format`처럼 텍스트 분기로 본다. 텍스트 안 plain URL은 공통 URL 추출 단계에서 input fetch queue에 시드된다.

`file://` / `ftp://` / `mailto:` / scheme 없는 입력은 URL 분기 아님.

| 인자 | 기본값 | 설명 |
|---|---|---|
| `--ssot-include <glob>` | (없음) | SSOT corpus glob. default = 프로젝트 폴더 안 모든 `*.md` (`.git/`, `node_modules/` 자동 제외). R1·R3 corpus 공유. |
| `--axes <list>` | `ssot,ac,deps` | 점검 축 콤마 구분. 빈 값이면 sanity check. |
| `--no-input-fetch` | off | review 대상 입력 수집 단계의 URL root fetch + 본문 URL fetch + connector fallback 봉쇄. 파일/텍스트/디렉터리 본문 자체는 읽는다. |
| `--no-input-image` | off | review 대상 입력 이미지 multimodal 호출 0건. URL fetch는 진행하되 image content-type 응답은 본문 합류하지 않는다. |
| `--no-ssot-fetch` | off (즉 link follow 활성) | SSOT corpus *.md 본문 안 외부 URL fetch + connector fallback 봉쇄. 매칭 file 본문만 corpus에 들어간다. |
| `--no-ssot-image` | off (즉 image multimodal 활성) | SSOT corpus 본문 안 이미지 참조·fetch image content-type 응답 multimodal 호출 0건. URL fetch는 그대로 (`--no-ssot-fetch`와 독립). |

옵션 범위:

- `--no-input-fetch` / `--no-input-image`는 review 대상 본문을 만드는 input collection에만 적용.
- `--no-ssot-fetch` / `--no-ssot-image`는 R1/R3 SSOT corpus link follow에만 적용.
- `--no-ssot-fetch`는 입력 URL fetch를 막지 않는다. `--no-input-fetch`는 SSOT corpus link follow를 막지 않는다.

## 동작 시퀀스

### Step 1: 입력 dispatch + input collection + sanity check

토큰/입력 형태에 따라 분기 → input collection → 통합 입력 본문 구성 → 본문 분리 → 빈 본문 검사. 식별 실패 시 sanity check 메시지 출력 후 종료.

#### Step 1.1 입력 dispatch

분기 우선순위:

```
1. 0개                                      → conversation 참조 모드
2. URL 패턴 (1개 이상 토큰, 모두 https?://) → URL 분기
3. 1개 디렉터리 경로                       → 디렉터리 분기
4. 1개 파일 경로                           → 파일 분기 (이미지 확장자면 image queue 단독 시드)
5. 2개 non-URL path                         → 두 파일 분기
6. 그 외                                    → 텍스트 분기
```

#### Step 1.2 input collection (0.2.6)

`planning-format` Step 1~5와 같은 URL 판별, URL·이미지 추출, 재귀 fetch, connector fallback, image multimodal, 통합 본문 합류 룰을 사용한다.

- URL 분기의 모든 URL은 depth 0 root input source다.
- 모든 분기 공통으로 본문에서 markdown link/autolink, HTML `href`/`src`/`img`, plain URL, markdown image, data URI를 추출한다. self-anchor·`mailto:`/`tel:`/`javascript:`/`blob:`·non-http scheme은 제외.
- input fetch queue는 `planning-format` 0.2.5 결정성 룰을 따른다: push 시점 normalize, depth BFS, 같은 depth 안 markdown link → HTML href/src → plain URL 발견 순서, dequeue된 visited 미포함 URL은 100% fetch 시도, 실패도 visited 등록 + 출처 행 기록.
- depth·pages·body·fanout cap은 두지 않는다. cycle·중복은 input visited set으로만 막는다.
- fetch 진입 직전 `../planning-format/references/connector-routing.md`를 1회 Read 적재한다. 1차 WebFetch + connector fallback·인증 휴리스틱·MCP 카탈로그·Google Workspace tool 시퀀스·gid/range·status 표기를 그대로 공유한다.
- input visited set은 SSOT visited set과 별도다. 같은 URL이 input source와 SSOT corpus link에 동시에 등장해도 `## 입력 출처`와 `## SSOT 출처`에 각각 나타날 수 있다.
- `--no-input-fetch` ON이면 input fetch queue 전체를 봉쇄한다. 입력이 URL뿐이면 review 대상 본문을 만들 수 없으므로 §sanity check 메시지를 출력한다.
- input image queue는 5경로(이미지 파일 인자, 디렉터리 이미지, markdown image/HTML img, fetch `image/*`, inline data URI)를 따른다. `--no-input-image` ON이면 image multimodal 0건이며 image content-type 응답은 본문 합류하지 않는다.
- fetch·image 처리가 1건 이상이면 `## 입력 출처` 블록에 root URL, 자식 URL, 입력 이미지 행을 모두 기록한다. 실패 행도 포함한다.
- fetch·image 처리가 끝나면 source 단위 헤더로 concat한다.

```markdown
=== [입력 출처 1] URL: https://wiki.example/policy/order-cancel ===
...

=== [입력 출처 2] URL: https://docs.example/feature/order-cancel ===
...
```

Google Sheets gid/range, connector deep link anchor, metadata only 상태 등은 `planning-format`과 동일하게 부연한다.

#### Step 1.3 본문 분리

통합 입력 본문에서 정책서·기능설계서·입력 제외 §을 분리한다.

1. `# 정책서` / `## 정책서` 헤더 → 정책서 본문.
2. `# 기능설계서` / `## 기능설계서` 헤더 → 기능설계서 본문.
3. `## 입력 제외 항목` 헤더 → 입력 제외 § 본문 (옵션 — 부재해도 sanity check 아님, 0.2.0 산출물 호환). 여러 개면 발견 순서대로 concat하고 dedup하지 않는다.
4. markdown 코드 펜스 안 헤더 → 펜스 안 본문에서 1~3 반복.
5. source title/path/URL label이 `정책서`, `policy`, `정책`, `기능설계서`, `feature`, `design`, `spec` 중 하나를 명확히 가리키면 source 단위 fallback 배정.
6. 위 절차 후 정책서·기능설계서 둘 다 확보하지 못하면 sanity check.

source 단위 fallback은 명확한 1:1 신호일 때만 사용한다. 두 source가 모두 같은 종류로 추정되거나 둘 다 불명확하면 fallback하지 않는다.

분리 결과는 메모리에만. `--axes` 활성 무관 분리 단계는 항상 시도.

| 케이스 | 메시지 |
|---|---|
| conversation 모드 + 직전 planning-format 출력 없음 | `직전 turn에서 planning-format 출력을 찾을 수 없습니다. 경로 또는 markdown을 인자로 주세요.` |
| URL 입력 + `--no-input-fetch` | `입력 URL fetch가 --no-input-fetch로 봉쇄되어 정책서·기능설계서 본문을 식별할 수 없습니다. 파일/markdown 입력을 주거나 --no-input-fetch를 제거하세요.` |
| URL root 모두 본문 합류 실패 | `모든 review 입력 URL fetch 실패. 첫 번째 사유: <status 또는 error>` |
| URL root 모두 인증 게이트 + fallback 실패 | `모든 review 입력 URL이 로그인 필요로 보입니다. connector/MCP fallback도 인증되지 않았습니다.` + `필요한 connector: <Atlassian / Figma / Google Drive / Slack / Notion / ...>` |
| 본문 식별 실패 | `정책서·기능설계서 두 본문을 식별할 수 없습니다. URL 본문에 # 정책서 / # 기능설계서 헤더를 두거나, 정책서·기능설계서가 구분되는 별도 링크/파일로 주세요.` |
| 한쪽 본문 비어 있음 | `<정책서 또는 기능설계서>가 비어 있습니다. 입력 URL/파일이 planning-format 산출물인지 확인하세요.` |
| `--axes` 빈 값 | `--axes에 점검 축을 1개 이상 지정하세요. (ssot, ac, deps)` |

### Step 2: 검증 축 점검

`--axes` 활성 축만 main 단일 패스. 각 축은 reference 적재 후 그대로 따른다.

**sub-§ 인식 (0.2.4)**: R1·R2·R3 모두 산출물 부모 § + sub-§(`### N.M ... 보조 표`) 본문을 함께 점검 대상으로 본다. 절차 detail은 각 reference 그대로 — 부모 § 룰을 sub-§ 본문에 자연 확장.

| 축 | 키 | 적재 reference | 발견 sub-category |
|---|---|---|---|
| R1. SSOT 충돌 | `ssot` | `references/ssot-rules.md` | (단일) |
| R2. Acceptance Criteria 검증가능성 | `ac` | `references/ac-rules.md` | 정량성 / 상태 / 행위자 / 결과 관찰 |
| R3. 의존·영향 분석 | `deps` | `references/deps-rules.md` | 정책 변경 / 상태 전이 / 권한·역할 / 외부 의존 (발견·권고 분류) |

R1·R3 corpus 공유 (`--ssot-include`). R2는 input collection 이후 분리된 본문 자체만 본다.

#### R1 link follow (0.2.2)

R1 활성 OR R3 활성 + 매칭 ≥1 + `--no-ssot-fetch` off → 매칭 *.md 본문 안 URL·이미지를 fetch + connector fallback으로 corpus body에 합류. 절차·visited set·sanity check·출처 list 형식 모두 `references/ssot-rules.md` §R1.4·§R1.5. connector lookup은 `../planning-format/references/connector-routing.md` 공유 적재. `--no-ssot-image` ON이면 image content-type 합류 skip (URL fetch는 별도).

입력 URL source 자체는 SSOT corpus가 아니다. input fetch는 review 대상 본문 생성용이고, SSOT fetch는 비교 corpus 확장용이다.

#### R3 입력 제외 § 보조 신호 (0.2.2)

R3 활성 + Step 1 분리 성공 시 카테고리별 가중치. 절차·신호 카테고리·헤더 카운트 K 산출 모두 `references/deps-rules.md` §R3.2.1.

### Step 3: 발견 합산 + 결과

같은 발견이 두 축에 걸치면 한 번만 기록. 우선순위: **R1 > R3 > R2**.

- 모든 활성 축 발견 0건 → `통과`
- ≥1건 → `발견 N건` (R3 `권고`도 카운트 포함)

## 출력 포맷

````markdown
# planning-review: [기능명]

- 입력: [경로 list / URL list / "직전 planning-format 출력 (conversation)" / "직접 입력 markdown"]
- 입력 처리: [conversation 본문 사용 | local/raw 본문 사용 | URL root R개 + 입력 fetch 성공 K개 / 실패 J개 + 입력 이미지 M개 (cap 없음)]
- 입력 제외 §: 분리 N건 (R3 신호 K건: fetch 실패 a, 범위 외 b, 구조 변환 c, 디테일 축약 d / R3 무관 N-K건)
- 점검 축: [ssot, ac, deps]
- SSOT corpus: 매칭 N개 + 외부 fetch 성공 K개 / 실패 J개 (총 시도 K+J건, cap 없음)
- SSOT 검색 키워드: [keyword1, keyword2, ...]

---

## 리뷰 결과: [통과 | 발견 N건]

- SSOT 충돌: N건 (활성 시)
- 검증가능성: N건 (활성 시)
- 영향 분석: N건 (활성 시, 발견+권고 합계)

## 입력 출처
(input fetch 또는 input image 처리 1건 이상일 때만)

root 입력: R개
재귀 fetch: 성공 K개 / 실패 J개 (cap 없음)
이미지: 성공 M개 / 실패 L개

| # | 출처 종류 | URL/경로 | origin | 상태 | 본문 사용 |
|---|---|---|---|---|---|
| 1 | 입력 root URL | https://wiki.example/policy/order-cancel | — | 200 (via WebFetch) | O |
| 2 | 입력 root URL | https://docs.example/feature/order-cancel | — | 200 (via Google Drive connector — read_file_content) | O |
| 3 | 입력 자식 URL | https://figma.com/design/... | 입력 출처 2 | 인증 필요 (Figma MCP 미인증) | X |
| 4 | 입력 이미지 | ./diagram.png | 입력 출처 1 | image/png 0.4MB | O (multimodal) |

## SSOT 출처
(link follow 1건 이상일 때만, §R1.5 표 형식)

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
   - 분류: [발견 / 권고]
   - 카테고리: [정책 변경 / 상태 전이 / 권한·역할 / 외부 의존]
   - 위치: [정책서/기능설계서 §섹션]
   - 영향 후보: [SSOT 파일 path list]
   - 근거: "[변환 본문 인용]" + (선택) "[SSOT 인용 또는 입력 제외 § cross-reference]"
   - 영향: [한 줄]
   - 제안: [후속 검토 조건]
````

규칙:

- 활성 안 한 축의 sub-section은 통째 생략. `SSOT 검색 키워드` 줄은 R1 활성 시에만.
- `입력 처리` 줄: conversation 모드에서 직전 `planning-format` 출력을 그대로 쓰고 input fetch가 0건이면 `conversation 본문 사용`. 파일/디렉터리/raw markdown 본문만 사용하고 fetch/image가 0건이면 `local/raw 본문 사용`. input fetch 또는 input image가 1건 이상이면 성공/실패 카운트를 표기.
- `SSOT corpus` 줄: link follow ≥1 = `매칭 N개 + 외부 fetch 성공 K개 / 실패 J개 (총 시도 K+J건, cap 없음)`. link 0건 = `매칭 N개`. 매칭 0건 = `매칭 0개 (검증 대상 없음)`. R1·R3 모두 비활성 = 줄 미출력.
- `입력 제외 §` 줄: 분리 성공 = `분리 N건 (R3 신호 K건: fetch 실패 a, 범위 외 b, 구조 변환 c, 디테일 축약 d / R3 무관 N-K건)` (K 산출은 `deps-rules.md` §R3.2.1). 분리 성공 + 0건 = `분리 0건`. 분리 실패·0.2.0 이전 = `없음 (또는 0.2.0 이전 산출물)`.
- `## 입력 출처` 블록 위치 = `## 리뷰 결과` 다음, `## SSOT 출처` 앞. input fetch·input image 처리가 0건이면 생략.
- `## SSOT 출처` 블록 위치 = `## 입력 출처` 다음, 발견 sub-section 위. R1·R3 모두 비활성·매칭 0건·`--no-ssot-fetch`·link 0건이면 통째 생략.
- R3 발견·권고 항목이 입력 제외 § 보조 신호로 만들어진 경우 `근거` 줄에 입력 제외 § cross-reference 표시.

## 참고 파일

- `references/ssot-rules.md` — R1 SSOT 충돌 점검 절차·매칭·발견 형식·link follow·출처 list.
- `references/ac-rules.md` — R2 4 sub-category 기준.
- `references/deps-rules.md` — R3 4 sub-category 기준 + 발견·권고 분류 + 입력 제외 § 보조 신호.
- `../planning-format/references/connector-routing.md` — input fetch와 SSOT link follow에서 공유 적재. 인증 게이트 휴리스틱·MCP 카탈로그·호스트 매핑·Google Workspace tool 시퀀스·gid/range·fallback·status 표기.
- `../planning-format/references/conversion-rules.md` — input image multimodal·통합 본문 합류 룰을 공유 참조.

변환·자체 품질 점검·`--save`는 `planning-format` 스킬에서 별도 처리. 자세한 절차는 `skills/planning-format/SKILL.md`.
