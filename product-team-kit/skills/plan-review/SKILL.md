---
name: plan-review
description: "Use when an existing plan-format 기능/화면설계서·정책서 초안 또는 초안 폴더를 외부 발행 전에 검토하고 통과/조건부 통과/수정 필요 판정을 내려야 할 때."
argument-hint: "<초안 폴더 또는 기능설계서/정책서 파일경로>"
---

# plan-review

`/product-team-kit:plan-format`으로 저장한 초안 폴더 또는 기능설계서/정책서 파일을 발행 전에 검토하는 스킬이다. 템플릿 구조 검사가 아니라 Product Docs SSOT 충돌과 용어 일관성을 2축으로 점검하는 gate다.

Product Docs SSOT는 `<outputRoot>/`을 제외한 현재 프로젝트의 Markdown 문서 중 제품 정책, PRD/요구사항, 기능/화면 설계, 운영/QA 판단을 담은 문서와, 그 Markdown이 상대경로로 명시 참조한 로컬 resource만 포함한다. 코드, 설정 파일, 빌드 산출물, dependency/vendor, 외부 URL은 SSOT 근거에서 제외한다. `<outputRoot>/` 하위 파일은 검토 대상일 수 있지만 SSOT 근거로 사용하지 않는다.

`<outputRoot>`과 SSOT corpus 범위는 `../../references/config-contract.md`를 따라 결정한다. `outputRoot`의 default는 `planning`이며, `<outputRoot>/**`은 항상 SSOT exclude에 자동 포함된다. `ssot.include`가 지정되면 SSOT corpus를 그 glob 안으로 좁히고, 미지정/빈 배열이면 default `Product Team Space/Product Department/Colonova Product/_AI_ 정책서 & 기능설계서/**/*.md`를 사용한다. `ssot.exclude`는 default 제외(`.git/`, `vendor/`, `node_modules/`, `build/`, `dist/`, `.cache/`, `generated/`)에 누적한다.

판정 기준, 합성 규칙, 2축 점검 기준, 근거 패키지 형식은 `references/review-rules.md`를 단일 기준으로 따른다. 최종 출력 형식은 `references/output-format.md`를 따른다. 사람용 리포트 하나로 출력하며 별도 YAML manifest 블록은 사용하지 않는다.

## 빠른 판정 원칙

- `통과`는 발견 사항이 없다는 뜻이 아니라, **검토 대상·config·SSOT corpus 탐색·2축 점검·출력 형식**이 모두 성립했고 필수 수정/발행 전 확인 항목이 0건이라는 뜻이다.
- config 치명 오류, 올바르지 않은 입력 타입, SSOT corpus 추출 실패는 정상 2축 검토 결과로 포장하지 않고 지정된 종료 분기로 즉시 끝낸다.
- SSOT corpus 추출은 성공했지만 매칭이 0건인 경우만 A축을 `검증 대상 없음`으로 처리할 수 있다. 후보가 있었는데 읽지 못했거나 비용 때문에 생략한 경우는 `통과` 금지다.
- 대화 컨텍스트, 작성자 의도, 기억에만 있는 사실은 근거가 아니다. 검토 대상 본문 또는 읽은 Product Docs SSOT 근거에 없으면 근거 부족으로 처리한다.
- `plan-review`는 초안, Product Docs SSOT, 팀 문서 export, linked resource, 외부 시스템을 수정하거나 게시하지 않는다. 필요한 최소 수정/확인 조건만 제시한다.

## Lazy read 원칙

각 파일은 실제 필요한 sub-step에서만 읽는다. dispatch 시작 시점에 묶어 읽지 않는다. 종료 분기에서 안 쓰는 파일을 읽으면 토큰 낭비이며 **금지**한다.

| 파일 | 읽는 시점 | 용도 |
| --- | --- | --- |
| `<project-root>/.product-team-kit/config.json` | 사전 점검 1 시작 | strict-exit 판정, outputRoot/ssot 확정 |
| 검토 대상 본문 + 짝문서 | 사전 점검 2 입력 타입 검증 통과 후 | 타입 판정 보강, 키워드 추출, 2축 점검 입력 |
| `references/review-rules.md` | 키워드 추출 직후 (`## SSOT corpus 선택 규칙` + `## 2축 점검 기준` + `## 발견 사항 필드` 한 번에) | corpus listing, main A축 점검, B worker prompt inline |
| SSOT corpus 본문 | 키워드 매칭 후보 ≥1개 확인 후 | main A축 SSOT 충돌 점검 |
| `references/output-format.md` | 종료 출력 직전 (분기 확정 후 1회) | "올바른 검토 대상이 아님" / 결과 3종 리포트 |

타입 판정 룰은 `references/review-rules.md`의 `## 검토 대상 타입 판정`을 단일 진실 소스로 따른다. 본문 read 후 룰을 적용한다.

분기별 실제 읽기 순서:

- **config 치명**: `config.json` → `output-format.md` → 종료 (`set-config` 안내)
- **입력 타입 fail** (상위설계서 등): `config.json` → 본문 (타입 판정) → `output-format.md` → 종료
- **SSOT corpus 추출 실패**: `config.json` → 본문/짝문서 → `review-rules.md` → `output-format.md` → 종료 (worker spawn 안 함)
- **SSOT 매칭 0건**: `config.json` → 본문/짝문서 → `review-rules.md` → corpus 후보 listing 후 0건 확인 → main A축 "검증 대상 없음" 처리 + B worker(용어 일관성) 본문 점검 → merge → `output-format.md`
- **정상**: `config.json` → 본문/짝문서 → `review-rules.md` → corpus listing → corpus 본문 read → main A축 점검 + B worker(용어 일관성) → merge → `output-format.md`

## 진행 표시 원칙

실행 중 사용자에게 보이는 narration은 **구조화된 step 헤더 한 줄로만** 표시한다. 각 step 진입 시점에 정확히 한 줄을 출력한다.

형식: `Step N/M: <step 이름>` (M은 분기별 총 step 수, 사전 결정)

분기별 step 시퀀스 (config 검증은 모든 분기에서 silent — 헤더 미출력):

- **config 치명**: 헤더 없음. `output-format.md` 종료 템플릿만 출력.
- **입력 타입 fail** (M=2): `Step 1/2: 입력 타입 검증` → `Step 2/2: 종료 출력`
- **SSOT corpus 추출 실패** (M=3): `Step 1/3: 검토 대상 read` → `Step 2/3: SSOT corpus 탐색` → `Step 3/3: 종료 출력`
- **SSOT 매칭 0건** (M=5): `Step 1/5: 검토 대상 read` → `Step 2/5: SSOT corpus 탐색` → `Step 3/5: 2축 점검 (A 검증 대상 없음 + B 본문)` → `Step 4/5: merge` → `Step 5/5: 리포트 출력`
- **정상** (M=5): `Step 1/5: 검토 대상 read` → `Step 2/5: SSOT corpus 탐색` → `Step 3/5: 2축 점검 (A + B 병렬)` → `Step 4/5: merge` → `Step 5/5: 리포트 출력`

step 헤더 외 금지 항목 (전부 출력 금지):

- file IO 안내: `config.json 먼저 확인`, `검토 대상 파일 2개 동시 read`, `output-format.md 읽는다`
- sub-action 보고: `config 정상`, `직접 관련 SSOT 후보 발견`, `상위 20줄 인덱스 스캔`, `파일이 비어있는지 직접 확인`, `두 파일 모두 빈 파일`
- 추론·계획 narration: `2축 점검 완료`, `최종 리포트 출력`, `이제 ~ 한다`
- 본문 echo: 검토 대상 본문, SSOT corpus 본문, 표 미리보기, marker 인용

Read/Bash/Agent 툴 호출은 Claude Code UI가 자동 표시하므로 텍스트 보고 불필요. Tool 호출 사이에 진행 안내 텍스트 삽입 금지.

분기 결정 시점:

- **config 검증은 silent**로 수행한다. step 헤더를 출력하지 않는다. config 치명 종료면 헤더 없이 곧장 `output-format.md` 종료 템플릿만 출력한다.
- 첫 step 헤더(`Step 1/M: ...`)는 config 검증 통과 후 분기가 확정 가능한 시점에 출력한다.
  - 입력 타입 fail 분기: 첫 헤더 = `Step 1/2: 입력 타입 검증` (총 M=2, `Step 2/2: 종료 출력`).
  - 그 외 분기: 첫 헤더 = `Step 1/M: 검토 대상 read` (M은 분기별 표대로).
- 키워드 추출 후 SSOT 매칭 결과로 M이 추가 확정되면 다음 step 헤더부터 확정된 M 값으로 출력한다. 이전 헤더는 정정하지 않는다. 정상 시작점이 추정 가능한 분기는 정상 분기(M=5) 가정으로 진행하다 확정 시점에 새 M으로 전환한다.
- 사전 점검(`## 사전 점검` 1~4)은 silent config(점검 1) + Step 1(점검 2~4)로 분산된다. config 검증은 silent, 입력 타입·짝문서 탐색은 Step 1 = `검토 대상 read` (또는 입력 타입 fail 분기에서 `입력 타입 검증`).

사용자가 보는 turn 마지막 결과는 Step N/N (마지막 step) 직후 `references/output-format.md` 템플릿 1회 출력이다.

## 호출

- Claude Code: `/product-team-kit:plan-review <초안 폴더 또는 기능설계서/정책서 파일경로>`
- Codex: `$plan-review <초안 폴더 또는 기능설계서/정책서 파일경로>`

예시:
- `/product-team-kit:plan-review planning/결제기능--YYYY-MM-DD-HHMMSS/`
- `/product-team-kit:plan-review planning/결제기능--YYYY-MM-DD-HHMMSS/결제기능_기능설계서.md`

## 암묵 호출 라우팅

다음 의도에서는 `plan-review`를 선택한다.

- 기존 기능설계서/정책서 초안 또는 초안 폴더 검토
- 발행 전 검토, 통과/조건부 통과/수정 필요 판정
- Product Docs SSOT 근거와 초안의 충돌, 용어 일관성 확인
- 이미 생성된 초안 검토

다음 의도에서는 `plan-review`를 선택하지 않는다.

- 기획 입력을 기능설계서와 정책서 초안으로 생성해야 하는 경우 → `plan-format`

사용자가 "정리하고 검토"를 함께 요청했지만 기능설계서/정책서 초안 경로가 아직 없으면 `plan-review`를 먼저 호출하지 않는다. 먼저 `plan-format`으로 초안을 저장한 뒤 저장 경로를 대상으로 검토한다.

## 사전 점검

**진행 표시 매핑**: 1번 = silent (헤더 미출력), 2~4번 = `Step 1/M: 검토 대상 read` (입력 타입 fail 분기는 `Step 1/2: 입력 타입 검증`). step 헤더는 각 step 진입 시점에만 1회 출력하고 sub-action narration은 추가하지 않는다 (`## 진행 표시 원칙`).

**이 단계에서 읽는 파일**: `config.json` (1번), 검토 대상 본문 + 짝문서 (2~4번 통과 후). `review-rules.md`·SSOT corpus·`output-format.md`는 아직 읽지 않는다.

1. `.product-team-kit/config.json` 존재 여부를 확인하고 `outputRoot`, `ssot.include`, `ssot.exclude`를 확정한다. 파일 없음, JSON 파싱 실패, `version` 미일치, `outputRoot` 검증 거부는 치명 설정 오류로 즉시 종료하고 `set-config` 사용을 안내한다. 종료 출력은 `output-format.md`를 이 시점에 read해 적용한다. 비치명 검증 거부만 default fallback과 `[설정 경고]`로 처리한다.
2. 검토 대상이 기능설계서/정책서 초안 파일 또는 그 묶음 폴더인지 `references/review-rules.md`의 `## 검토 대상 타입 판정` 룰로 확인한다 (파일명 stem suffix `*_기능설계서.md`/`*_정책서.md`, H1 제목, 폴더 입력 시 내부 ≥1개 매칭). 다른 문서 타입(상위설계서 등)이면 검토를 수행하지 않고 `output-format.md`를 read해 `올바른 검토 대상이 아님` 템플릿으로 종료한다. 본 룰을 본문 read만으로 평가할 수 없을 때만 `review-rules.md`의 본 섹션을 미리 read한다 (이외 SSOT corpus·`review-rules.md` 본 섹션 외부는 read하지 않음).
3. 입력이 폴더면 같은 폴더의 기능설계서와 정책서를 함께 검토 대상으로 잡는다. 입력이 단일 파일이면 같은 폴더에서 `plan-format` 산출 파일명인 `[안전기능명]_기능설계서.md` / `[안전기능명]_정책서.md`의 같은 stem을 우선해 짝문서를 찾는다.
4. 짝문서가 없으면 단일 검토를 진행하고 `검증 한계`에 `짝문서 없음`을 기록한다. 검토 대상이 명시적으로 다른 문서의 정책/기능 판단에 의존하면 분류를 `필수 수정` 또는 `발행 전 확인`으로 올린다.

## 2축 개요

각 축은 dispatch에서 확정한 검토 대상 본문과 필요한 SSOT 근거 패키지로 점검한다. 상세 기준은 `references/review-rules.md`의 `## 2축 점검 기준` 섹션을 단일 진실 소스로 따른다.

- **A. SSOT 충돌**: 초안 확정 문장 vs Product Docs SSOT current evidence.
- **B. 용어 일관성**: 역할명·상태명·권한명·화면명·도메인 stem 통일성.

발견 사항은 분류(필수 수정 / 발행 전 확인 / 참고)와 함께 기록한다. 마커(`[미정]`/`[가정]`/`[확인 필요]`/`[충돌 후보]`) 자체는 plan-format 책임 영역이며 본 검토는 분류 대상으로 삼지 않는다. 단, 마커 본문이 SSOT 근거와 충돌하면 A축 발견으로, 마커 본문 안에서 같은 대상을 가리키는 표기가 어긋나면 B축 발견으로 기록할 수 있다.

## 실행 단계

`dispatch → main A축 점검 + B worker(용어 일관성) 병렬 → merge` 3단계로 동작한다. SSOT corpus는 main이 보유·사용하므로 A축은 main이 직접 점검하고, 본문만 보는 B만 worker로 분리한다. 병렬 호출 환경이 없거나 입력이 작아 분리 비용이 더 큰 경우 단일 패스 fallback으로 진행해도 결과 형식은 동일해야 한다.

**진행 표시 매핑**: dispatch의 SSOT corpus 탐색·매칭 = `Step 2/M: SSOT corpus 탐색`. main A축 점검 + B worker 병렬 = `Step 3/M: 2축 점검`. merge = `Step 4/M: merge`. 종료 출력 = `Step 5/M: 리포트 출력` (`## 진행 표시 원칙`).

### dispatch (단일 패스)

**읽는 파일**: 사전 점검에서 읽은 `config.json`·본문·짝문서 재사용. `review-rules.md`는 SSOT corpus 선택 단계 직전에 read. SSOT corpus 본문은 키워드 매칭 후보 ≥1개일 때만 read.

분류·고정 항목 결정 + A축 SSOT 충돌 점검을 수행한다. B 용어 일관성 본문 점검은 worker가 담당한다.

- config 확정 (`outputRoot`, `ssot.include`, `ssot.exclude`) — `../../references/config-contract.md` 따름. 치명 설정 오류는 즉시 종료하고 `set-config` 안내.
- 입력 타입 검증 — 기능설계서/정책서가 아니면 `output-format.md`를 read해 `올바른 검토 대상이 아님` 템플릿으로 종료.
- 검토 대상 본문 read + 짝문서 탐색·read (`## 사전 점검` 4단계 그대로).
- 키워드 추출 (기능명, 정책명, 도메인, 역할명, 상태명, 권한명, 화면명, 핵심 조건·예외).
- `review-rules.md` read — 이 시점에서 한 번만. `## SSOT corpus 선택 규칙` + `## 2축 점검 기준`을 함께 적용한다. A축·SSOT 선택 규칙은 main 자체 사용, B는 worker prompt에 inline.
- SSOT corpus 후보 listing — `review-rules.md`의 `## SSOT corpus 선택 규칙` 따름.
- **SSOT 후보 인덱스 스캔** — 후보 파일 상위 20줄을 Bash 1회 호출로 일괄 읽기. archive/deprecated/낮은 버전/키워드 미매칭 문서를 과거 맥락으로 분류하고 전문 읽기에서 제외. 상세 규칙은 `review-rules.md` 규칙 4.5.
- **키워드 매칭 핵심 후보 ≥1개** → 축소된 후보만 전문 read. **0건** → main A축을 "검증 대상 없음"으로 처리, corpus 본문 read skip.
- SSOT corpus 0건 분기 — `review-rules.md`의 (a) 추출 성공 + 매칭 0건 / (b) 추출 실패 처리. 추출 실패는 worker spawn 없이 즉시 `수정 필요` 결과로 종료한다. 이 시점에 `output-format.md`를 read해 적용.
- **main A축 SSOT 충돌 점검** — corpus 본문(또는 0건 신호)과 검토 대상 본문을 비교해 `review-rules.md`의 `## 2축 점검 기준 → A. SSOT 충돌` + `## 발견 사항 필드` 7 필드 형식으로 발견 사항 list 작성. 발견 0건이면 내부적으로 no-findings 동등 처리. corpus 0건(추출 성공)이면 발견 0건 + A축 `검증 대상 없음`으로 표기.
- B worker(용어 일관성) 분배 데이터 준비 — `review-rules.md`의 `## 2축 점검 기준 → B. 용어 일관성`과 `## 발견 사항 필드`를 worker prompt에 inline.

### B worker(용어 일관성) 점검

**읽는 파일**: 없음. dispatch에서 읽은 `review-rules.md`·본문을 worker prompt에 inline 포함. worker가 직접 파일 read하지 않는다. SSOT corpus는 worker에 전달하지 않는다 (A축은 main 직접 점검).

main이 단일 어시스턴트 메시지에 Agent tool 호출 1 block 발행한다. main A축 점검과 B worker 호출은 동시에 진행 가능하다. worker 호출이 회신될 때까지 merge로 가지 않는다.

호출 환경에서 Agent 호출이 불가능하면 (Codex, MCP 단일 패스 환경) 단일 패스 fallback으로 main이 2축을 순차 점검한다. 결과 형식은 동일해야 한다.

| 책임 | 입력 |
|---|---|
| main (A축 SSOT 충돌) | dispatch 결과 + SSOT corpus 본문 + review-rules.md A축 (자체 사용) |
| `plan-review-terminology-worker` (B축) | dispatch 결과 (본문만) + review-rules.md B축 inline + `## 발견 사항 필드` inline |

worker는 `references/review-rules.md`의 `## 발견 사항 필드` 7 필드 표 형식으로 발견 사항만 return한다. 발견 0건 시 응답 끝에 `<!-- worker-flag: no-findings -->` 한 줄 명시.

main A축 점검 결과도 동일한 7 필드 형식을 따른다. 발견 0건이면 내부적으로 no-findings 동등 상태를 기록한다.

worker는 합성·결과 3종 판정·리포트 작성을 하지 않는다. 본문 수정·파일 write도 하지 않는다. 모두 main의 merge가 일괄 처리한다.

### merge (단일 패스)

**읽는 파일**: 없음. dispatch에서 읽은 `review-rules.md`를 재사용 (합성 규칙·결과 3종 기준). 종료 출력 직전에만 `output-format.md`를 read.

출력은 2층 구조다 (`output-format.md`의 `## 출력 2층 구조`). 상단은 dedup·보수 합성된 통합 list, 하단은 agent별 원본 발견 raw. 두 면을 같은 리포트에 출력한다.

- **상단 통합용**: main A축 발견 + B worker 발견 사항을 합쳐 `references/review-rules.md`의 `## 합성 규칙` 적용 (위치+제목+근거 정규화 dedup, NFC, 보수 분류). 축·내부 ID 컬럼은 두지 않는다.
- **하단 agent 원본용**: main A축 / B worker 각 발견을 dedup 없이 그대로 보존해 출력. 같은 발견이 여러 agent에 걸치면 양쪽 모두 노출된다.
- 결과 3종 판정 — `references/review-rules.md`의 `## 결과 3종 기준` + `## 보수 합성 우선순위` 적용 (상단 list 기준).
- main A축 발견 0건 + B worker `<!-- worker-flag: no-findings -->` + `완료 전 자체 점검` 통과 → `통과`.
- worker 발견 사항 형식이 7 필드(제목/위치/분류/발견 유형/근거 인용/영향/최소 수정 또는 확인 조건)와 어긋나면 1회 retry, 2회 어긋나면 `검증 한계`에 기록 후 보수 합성. main A축 발견은 main이 직접 7 필드 형식으로 작성하므로 retry 대상이 아니다.
- 표 형식 보정: worker 출력이 `review-rules.md ## 발견 사항 필드 → 표 출력 형식 (GFM)`을 어겼으면 (separator 행 누락, leading/trailing `|` 누락, cell 안 unescaped `|`로 컬럼 어긋남, backtick·HTML 안 unescaped `|` 포함) main이 cell escape·separator 행 보정만 적용해 하단 블록에 노출한다. cell escape는 `review-rules.md ## 발견 사항 필드 → 표 출력 형식 (GFM)`의 `main 보정 단계 cell escape 알고리즘`을 그대로 따른다 (backtick·HTML 안 `|`도 escape 대상). 보정 적용 사실은 `검증 한계`에 `<worker> 출력 형식 보정 적용` 한 줄 남긴다. 보정해도 컬럼 수가 맞지 않으면 해당 worker 블록을 fenced ` ```text ``` ` 원본 텍스트로 노출하고 사유를 `검증 한계`에 명시. main A축, 상단 통합 list도 동일 GFM 형식과 escape 알고리즘을 따른다 (main이 자기 출력에도 같은 escape 적용).
- `references/output-format.md` 템플릿으로 사람용 리포트 출력. 템플릿을 감싼 ````text ... ```` 또는 ```text ... ``` fence는 docs 가독성용이므로 **출력에 포함하지 않는다**. fence 내부 본문만 raw markdown으로 출력한다. 설정 경고는 dispatch 모은 목록 사용.
- 올바른 검토 대상이 아님 분기는 하단 agent 원본 블록을 출력하지 않는다.

### 완료 전 자체 점검

최종 리포트를 출력하기 직전에 아래를 확인한다. 하나라도 실패하면 `references/review-rules.md`의 `## 통과 금지 조건`과 `## 보수 합성 우선순위`를 적용해 결과를 보수적으로 조정하고, 실패 이유를 `검증 한계` 또는 지정된 종료 템플릿에 남긴다.

1. 검토 대상이 기능/화면설계서 또는 정책서 초안인지 확인했다.
2. `.product-team-kit/config.json` 치명 오류가 없고, 비치명 경고는 `[설정 경고]`에 모았다.
3. SSOT corpus 탐색은 성공했으며, 매칭 0건이면 `SSOT corpus 0건 (관련 Markdown 부재)`로 명시했다.
4. 매칭된 핵심 후보와 필요한 linked local resource를 읽었거나, 읽지 못한 이유를 `읽지 않은 관련 후보`/`검증 한계`에 남겼다.
5. A/B 발견 사항은 7필드 형식이며, 형식 실패 worker는 retry 후에도 실패하면 `검증 한계`에 남겼다.
6. 모든 판정 근거가 검토 대상 본문 또는 읽은 근거에 있고, 대화 컨텍스트만으로 만든 주장은 없다.
7. 결과가 `통과`라면 필수 수정·발행 전 확인이 0건이고, `통과 금지 조건`에 해당하는 신호가 없다.
8. 최종 출력은 `references/output-format.md` 순서와 라벨을 따른다.

현재 대화 컨텍스트는 근거가 아니다. 대화에서 알게 된 배경, 의도, 작성 당시 판단은 검토 대상 파일 또는 SSOT 근거에 없으면 근거 부족으로 본다.

## 규칙

- 검토 기준과 결과 경계는 `references/review-rules.md`만 따른다.
- 최종 출력은 `references/output-format.md`만 따른다. 이 파일은 종료 분기가 확정된 직후 1회만 read한다. YAML manifest 블록은 사용하지 않는다.
- 수정이 필요한 경우 직접 수정하지 않는다. 필수 수정 항목만 제시한다.
- 외부 시스템에 직접 게시하지 않고 Product Docs SSOT Markdown 또는 팀 문서 export snapshot을 자동 수정하지 않는다.
- `<outputRoot>/` 산출물은 review target으로만 읽고 SSOT 근거로 승격하지 않는다.
- 읽은 근거, 읽지 않은 관련 후보, 제외 후보, 검증 한계를 최종 출력에 남긴다.
- 설정 파싱/검증 경고는 사용자 출력 하단에 `[설정 경고]` 블록 한 번으로 표기한다. 경고 포맷은 `../../references/config-contract.md`를 따른다.
