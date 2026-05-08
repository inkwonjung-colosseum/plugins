---
name: planning-review
description: "planning-format 산출물(정책서·기능설계서 두 본문)을 외부 SSOT corpus 충돌·acceptance criteria 검증가능성·의존 영향 분석 3축으로 점검할 때 사용한다. 직전 turn의 planning-format 출력, 디렉터리·파일 경로, raw markdown 텍스트 모두 입력 받는다."
argument-hint: "[<정책서·기능설계서 경로 | 디렉터리 | raw markdown>] [--ssot-include <glob>] [--axes <list>] [--no-ssot-fetch] [--no-ssot-image]"
---

# planning-review

## 인자

위치 인자 0개 또는 1~2개:

- **0개** = conversation 참조 모드. 직전 turn의 `planning-format` 출력에서 두 본문 추출.
- **1개 (디렉터리)** = `정책서*.md` + `기능설계서*.md` 자동 검색.
- **1개 (파일)** = 본문 안 두 섹션 자동 분리. 헤더 `# 정책서`/`## 정책서`/`# 기능설계서`/`## 기능설계서` 또는 코드 펜스 ` ```markdown ... ``` ` 식별. 0.2.2부터 `## 입력 제외 항목` 블록도 함께 분리.
- **1개 (raw markdown 텍스트)** = 따옴표로 감싼 markdown. 두 본문 + 입력 제외 § 모두 포함 시 자동 분리.
- **2개** = `<정책서> <기능설계서>` 또는 역순 (헤더로 자동 식별).

| 인자 | 기본값 | 설명 |
|---|---|---|
| `--ssot-include <glob>` | (없음) | SSOT corpus glob. default = 프로젝트 폴더 안 모든 `*.md` (`.git/`, `node_modules/` 자동 제외). R1·R3 corpus 공유. |
| `--axes <list>` | `ssot,ac,deps` | 점검 축 콤마 구분. 빈 값이면 sanity check. |
| `--no-ssot-fetch` | off (즉 link follow 활성) | SSOT corpus *.md 본문 안 외부 URL fetch + connector fallback 봉쇄. 매칭 file 본문만 corpus에 들어간다. |
| `--no-ssot-image` | off (즉 image multimodal 활성) | SSOT corpus 본문 안 이미지 참조·fetch image content-type 응답 multimodal 호출 0건. URL fetch는 그대로 (`--no-ssot-fetch`와 독립). |

`--no-ssot-fetch` / `--no-ssot-image`는 `planning-format`의 `--no-fetch` / `--no-image`와 의미가 비슷하지만 대상이 다름 — planning-format은 입력 본문, planning-review는 SSOT corpus 본문.

## 동작 시퀀스

### Step 1: 입력 dispatch + sanity check

토큰 수에 따라 분기 → 본문 분리 → 빈 본문 검사. 식별 실패 시 sanity check 메시지 출력 후 종료.

본문 분리 우선순위 (0.2.2 신규):

1. `# 정책서` / `## 정책서` 헤더 → 정책서 본문.
2. `# 기능설계서` / `## 기능설계서` 헤더 → 기능설계서 본문.
3. `## 입력 제외 항목` 헤더 → 입력 제외 § 본문 (옵션 — 부재해도 sanity check 아님, 0.2.0 산출물 호환).
4. 위 3종 중 정책서·기능설계서가 둘 다 매칭 안 되면 sanity check.

분리 결과는 메모리에만. `--axes` 활성 무관 분리 단계는 항상 시도.

| 케이스 | 메시지 |
|---|---|
| conversation 모드 + 직전 planning-format 출력 없음 | `직전 turn에서 planning-format 출력을 찾을 수 없습니다. 경로 또는 markdown을 인자로 주세요.` |
| 1개 인자 + 본문 식별 실패 | `정책서·기능설계서 두 본문을 식별할 수 없습니다. 헤더(# 정책서 / # 기능설계서) 또는 별도 파일/경로로 주세요.` |
| 한쪽 본문 비어 있음 | `<정책서 또는 기능설계서>가 비어 있습니다. planning-format 산출물을 확인하세요.` |
| `--axes` 빈 값 | `--axes에 점검 축을 1개 이상 지정하세요. (ssot, ac, deps)` |
| 인자 3개+ | `정책서·기능설계서 외 추가 인자는 받지 않습니다.` |

### Step 2: 검증 축 점검

`--axes` 활성 축만 main 단일 패스. 각 축은 reference 적재 후 그대로 따른다.

**sub-§ 인식 (0.2.4)**: R1·R2·R3 모두 산출물 부모 § + sub-§(`### N.M ... 보조 표`) 본문을 함께 점검 대상으로 본다. 절차 detail은 각 reference 그대로 — 부모 § 룰을 sub-§ 본문에 자연 확장.

| 축 | 키 | 적재 reference | 발견 sub-category |
|---|---|---|---|
| R1. SSOT 충돌 | `ssot` | `references/ssot-rules.md` | (단일) |
| R2. Acceptance Criteria 검증가능성 | `ac` | `references/ac-rules.md` | 정량성 / 상태 / 행위자 / 결과 관찰 |
| R3. 의존·영향 분석 | `deps` | `references/deps-rules.md` | 정책 변경 / 상태 전이 / 권한·역할 / 외부 의존 (발견·권고 분류) |

R1·R3 corpus 공유 (`--ssot-include`). R2는 본문 자체만.

#### R1 link follow (0.2.2)

R1 활성 OR R3 활성 + 매칭 ≥1 + `--no-ssot-fetch` off → 매칭 *.md 본문 안 URL·이미지를 fetch + connector fallback으로 corpus body에 합류. 절차·visited set·sanity check·출처 list 형식 모두 `references/ssot-rules.md` §R1.4·§R1.5. connector lookup은 `../planning-format/references/connector-routing.md` 공유 적재. `--no-ssot-image` ON이면 image content-type 합류 skip (URL fetch는 별도).

#### R3 입력 제외 § 보조 신호 (0.2.2)

R3 활성 + Step 1 분리 성공 시 카테고리별 가중치. 절차·신호 카테고리·헤더 카운트 K 산출 모두 `references/deps-rules.md` §R3.2.1.

### Step 3: 발견 합산 + 결과

같은 발견이 두 축에 걸치면 한 번만 기록. 우선순위: **R1 > R3 > R2**.

- 모든 활성 축 발견 0건 → `통과`
- ≥1건 → `발견 N건` (R3 `권고`도 카운트 포함)

## 출력 포맷

````markdown
# planning-review: [기능명]

- 입력: [경로 list / "직전 planning-format 출력 (conversation)" / "직접 입력 markdown"]
- 입력 제외 §: 분리 N건 (R3 신호 K건: fetch 실패 a, 범위 외 b, 구조 변환 c, 디테일 축약 d / R3 무관 N-K건)
- 점검 축: [ssot, ac, deps]
- SSOT corpus: 매칭 N개 + 외부 fetch 성공 K개 / 실패 J개 (총 시도 K+J건, cap 없음)
- SSOT 검색 키워드: [keyword1, keyword2, ...]

---

## 리뷰 결과: [통과 | 발견 N건]

- SSOT 충돌: N건 (활성 시)
- 검증가능성: N건 (활성 시)
- 영향 분석: N건 (활성 시, 발견+권고 합계)

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
- `SSOT corpus` 줄: link follow ≥1 = `매칭 N개 + 외부 fetch 성공 K개 / 실패 J개 (총 시도 K+J건, cap 없음)`. link 0건 = `매칭 N개`. 매칭 0건 = `매칭 0개 (검증 대상 없음)`. R1·R3 모두 비활성 = 줄 미출력.
- `입력 제외 §` 줄: 분리 성공 = `분리 N건 (R3 신호 K건: fetch 실패 a, 범위 외 b, 구조 변환 c, 디테일 축약 d / R3 무관 N-K건)` (K 산출은 `deps-rules.md` §R3.2.1). 분리 성공 + 0건 = `분리 0건`. 분리 실패·0.2.0 이전 = `없음 (또는 0.2.0 이전 산출물)`.
- `## SSOT 출처` 블록 위치 = `## 리뷰 결과` 다음, 발견 sub-section 위. R1·R3 모두 비활성·매칭 0건·`--no-ssot-fetch`·link 0건이면 통째 생략.
- R3 발견·권고 항목이 입력 제외 § 보조 신호로 만들어진 경우 `근거` 줄에 입력 제외 § cross-reference 표시.

## 참고 파일

- `references/ssot-rules.md` — R1 SSOT 충돌 점검 절차·매칭·발견 형식·link follow·출처 list.
- `references/ac-rules.md` — R2 4 sub-category 기준.
- `references/deps-rules.md` — R3 4 sub-category 기준 + 발견·권고 분류 + 입력 제외 § 보조 신호.
- `../planning-format/references/connector-routing.md` — link follow에서 공유 적재. 인증 게이트 휴리스틱·MCP 카탈로그·호스트 매핑·Google Workspace tool 시퀀스·gid/range·fallback·status 표기.

변환·자체 품질 점검·`--save`는 `planning-format` 스킬에서 별도 처리. 자세한 절차는 `skills/planning-format/SKILL.md`.
