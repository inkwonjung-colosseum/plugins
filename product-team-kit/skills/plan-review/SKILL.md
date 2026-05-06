---
name: plan-review
description: "plan-format으로 작성한 정책서와 기능/화면설계서 묶음을 외부 발행 전에 Product Docs SSOT 충돌과 디자인·개발·QA·운영 착수 가능성 측면에서 검토하는 스킬."
argument-hint: "<초안 폴더 또는 기능설계서/정책서 파일경로>"
---

# plan-review

`/product-team-kit:plan-format`으로 저장한 초안 폴더 또는 기능설계서/정책서 파일을 발행 전에 검토하는 스킬이다. 템플릿 구조 검사가 아니라 Product Docs SSOT 충돌, 명확성, 용어 일관성, 디자인·개발·QA·운영 착수 가능성을 4축으로 점검하는 gate다.

Product Docs SSOT는 `<outputRoot>/`을 제외한 현재 프로젝트의 Markdown 문서 중 제품 정책, PRD/요구사항, 기능/화면 설계, 운영/QA 판단을 담은 문서와, 그 Markdown이 상대경로로 명시 참조한 로컬 resource만 포함한다. 코드, 설정 파일, 빌드 산출물, dependency/vendor, 외부 URL은 SSOT 근거에서 제외한다. `<outputRoot>/` 하위 파일은 검토 대상일 수 있지만 SSOT 근거로 사용하지 않는다.

`<outputRoot>`과 SSOT corpus 범위는 `../../references/config-contract.md`를 따라 결정한다. `outputRoot`의 default는 `planning`이며, `<outputRoot>/**`은 항상 SSOT exclude에 자동 포함된다. `ssot.include`가 지정되면 SSOT corpus를 그 glob 안으로 좁히고, 미지정/빈 배열이면 default `Product Team Space/Product Department/Colonova Product/_AI_ 정책서 & 기능설계서/**/*.md`를 사용한다. `ssot.exclude`는 default 제외(`.git/`, `vendor/`, `node_modules/`, `build/`, `dist/`, `.cache/`, `generated/`)에 누적한다.

판정 기준, 합성 규칙, 4축 점검 기준, 근거 패키지 형식은 `references/review-rules.md`를 단일 기준으로 따른다. 최종 출력 형식은 `references/output-format.md`를 따른다. 사람용 리포트 하나로 출력하며 별도 YAML manifest 블록은 사용하지 않는다.

## Lazy read 원칙

각 파일은 실제 필요한 sub-step에서만 읽는다. dispatch 시작 시점에 묶어 읽지 않는다. 종료 분기에서 안 쓰는 파일을 읽으면 토큰 낭비이며 **금지**한다.

| 파일 | 읽는 시점 | 용도 |
| --- | --- | --- |
| `<project-root>/.product-team-kit/config.json` | 사전 점검 1 시작 | strict-exit 판정, outputRoot/ssot 확정 |
| 검토 대상 본문 + 짝문서 | 사전 점검 2 입력 타입 검증 통과 후 | 키워드 추출, 4축 점검 입력 |
| `references/review-rules.md` | SSOT corpus 선택 규칙 적용 직전 (`## SSOT corpus 선택 규칙` + `## 4축 점검 기준` 한 번에) | corpus listing, worker prompt inline |
| SSOT corpus 본문 | 키워드 매칭 후보 ≥1개 확인 후 | A축 SSOT 충돌 점검 |
| `references/output-format.md` | 종료 출력 직전 (분기 확정 후 1회) | "올바른 검토 대상이 아님" / 결과 4종 리포트 |

분기별 실제 읽기 순서:

- **config 치명**: `config.json` → `output-format.md` → 종료 (`set-config` 안내)
- **입력 타입 fail** (상위설계서 등): `config.json` → 본문 (타입 확인) → `output-format.md` → 종료
- **SSOT 키워드 추출 실패**: `config.json` → 본문/짝문서 → `review-rules.md` → `output-format.md` → 종료 (worker spawn 안 함)
- **SSOT 매칭 0건**: `config.json` → 본문/짝문서 → `review-rules.md` → corpus 후보 listing 후 0건 확인 → 4 worker 병렬 (A는 "SSOT 근거 없음" 처리, B/C/D는 본문만 점검) → merge → `output-format.md`
- **정상**: `config.json` → 본문/짝문서 → `review-rules.md` → corpus listing → corpus 본문 read → 4 worker 병렬 → merge → `output-format.md`

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
- Product Docs SSOT 근거와 초안의 충돌, 누락, 착수 가능성 확인
- 이미 생성된 초안의 품질 평가

다음 의도에서는 `plan-review`를 선택하지 않는다.

- 기획 입력을 기능설계서와 정책서 초안으로 생성해야 하는 경우 → `plan-format`

사용자가 "정리하고 검토"를 함께 요청했지만 기능설계서/정책서 초안 경로가 아직 없으면 `plan-review`를 먼저 호출하지 않는다. 먼저 `plan-format`으로 초안을 저장한 뒤 저장 경로를 대상으로 검토한다.

## 사전 점검

**이 단계에서 읽는 파일**: `config.json` (1번), 검토 대상 본문 + 짝문서 (2~4번 통과 후). `review-rules.md`·SSOT corpus·`output-format.md`는 아직 읽지 않는다.

1. `.product-team-kit/config.json` 존재 여부를 확인하고 `outputRoot`, `ssot.include`, `ssot.exclude`를 확정한다. 파일 없음, JSON 파싱 실패, `version` 미일치, `outputRoot` 검증 거부는 치명 설정 오류로 즉시 종료하고 `set-config` 사용을 안내한다. 종료 출력은 `output-format.md`를 이 시점에 read해 적용한다. 비치명 검증 거부만 default fallback과 `[설정 경고]`로 처리한다.
2. 검토 대상이 기능설계서/정책서 초안 파일 또는 그 묶음 폴더인지 확인한다. 다른 문서 타입(상위설계서 등)이면 검토를 수행하지 않고 `output-format.md`를 read해 `올바른 검토 대상이 아님` 템플릿으로 종료한다. `review-rules.md`·SSOT corpus는 read하지 않는다.
3. 입력이 폴더면 같은 폴더의 기능설계서와 정책서를 함께 검토 대상으로 잡는다. 입력이 단일 파일이면 같은 폴더에서 `plan-format` 산출 파일명인 `[안전기능명]_기능설계서.md` / `[안전기능명]_정책서.md`의 같은 stem을 우선해 짝문서를 찾는다.
4. 짝문서가 없으면 단일 검토를 진행하고 `검증 한계`에 `짝문서 없음`을 기록한다. 검토 대상이 명시적으로 다른 문서의 정책/기능 판단에 의존하면 분류를 `필수 수정` 또는 `발행 전 확인`으로 올린다.

## 4축 개요

각 축은 dispatch에서 확정한 검토 대상 본문과 필요한 SSOT 근거 패키지로 점검한다. 상세 기준은 `references/review-rules.md`의 `## 4축 점검 기준` 섹션을 단일 진실 소스로 따른다.

- **A. SSOT 충돌**: 초안 확정 문장 vs Product Docs SSOT current evidence.
- **B. 명확성**: `[미정]`/`[가정]`/`[확인 필요]`/`[충돌 후보]` markers 처리, 모호 문장, 결정 가능 수준.
- **C. 용어 일관성**: 역할명·상태명·권한명·화면명·도메인 stem 통일성.
- **D. 4역할 넘김 가능성**: design/development/qa/operations 각각이 대화 기억 없이 다음 업무 시작 가능 여부.

발견 사항은 분류(필수 수정 / 발행 전 확인 / 참고)와 함께 기록한다.

## 실행 단계

`dispatch → 4 worker 병렬 → merge` 3단계로 동작한다. 병렬 호출 환경이 없거나 입력이 작아 분리 비용이 더 큰 경우 단일 패스 fallback으로 진행해도 결과 형식은 동일해야 한다.

### dispatch (단일 패스)

**읽는 파일**: 사전 점검에서 읽은 `config.json`·본문·짝문서 재사용. `review-rules.md`는 SSOT corpus 선택 단계 직전에 read. SSOT corpus 본문은 키워드 매칭 후보 ≥1개일 때만 read.

본문 검토는 하지 않는다. 분류·고정 항목만 결정한다.

- config 확정 (`outputRoot`, `ssot.include`, `ssot.exclude`) — `../../references/config-contract.md` 따름. 치명 설정 오류는 즉시 종료하고 `set-config` 안내.
- 입력 타입 검증 — 기능설계서/정책서가 아니면 `output-format.md`를 read해 `올바른 검토 대상이 아님` 템플릿으로 종료.
- 검토 대상 본문 read + 짝문서 탐색·read (`## 사전 점검` 4단계 그대로).
- 키워드 추출 (기능명, 정책명, 도메인, 역할명, 상태명, 권한명, 화면명, 핵심 조건·예외).
- **조기 판정** — 검토 대상 본문만으로 아래 기준 확인:
  - 핵심 섹션(상태·권한·예외·처리기준) `[미정]` 3개 이상
  - 필수 섹션(1~5) 중 2개 이상 실질 내용 없음
  - `[충돌 후보]` 3개 이상
  기준 충족 시 `output-format.md`를 read해 `수정 필요 (조기 판정)` 템플릿으로 종료. SSOT corpus 탐색·4 worker·merge를 수행하지 않는다.
- `review-rules.md` read — 이 시점에서 한 번만. `## SSOT corpus 선택 규칙`과 `## 4축 점검 기준` 4 섹션을 worker prompt에 inline.
- SSOT corpus 후보 listing — `review-rules.md`의 `## SSOT corpus 선택 규칙` 따름.
- **SSOT 후보 인덱스 스캔** — 후보 파일 상위 20줄을 Bash 1회 호출로 일괄 읽기. archive/deprecated/낮은 버전/키워드 미매칭 문서를 과거 맥락으로 분류하고 전문 읽기에서 제외. 상세 규칙은 `review-rules.md` 규칙 4.5.
- **키워드 매칭 핵심 후보 ≥1개** → 축소된 후보만 전문 read. **0건** → A worker에 "SSOT 근거 없음" 전달, corpus 본문 read skip.
- SSOT corpus 0건 분기 — `review-rules.md`의 (a) 추출 성공 + 매칭 0건 / (b) 추출 실패 처리. 추출 실패는 worker spawn 없이 즉시 `수정 필요` 결과로 종료한다. 이 시점에 `output-format.md`를 read해 적용.
- 4 worker 분배 데이터 준비 — `review-rules.md`의 `## 4축 점검 기준` 4 섹션을 각 worker prompt에 inline.

### 4 worker 병렬 작성

**읽는 파일**: 없음. dispatch에서 읽은 `review-rules.md`·본문·SSOT corpus를 worker prompt에 inline 포함. worker가 직접 파일 read하지 않는다.

main이 단일 어시스턴트 메시지에 Agent tool 호출 4 block 동시 발행한다. 4 호출이 모두 회신될 때까지 merge로 가지 않는다.

호출 환경에서 Agent 병렬 호출이 불가능하면 (Codex, MCP 단일 패스 환경) 단일 패스 fallback으로 main이 4축을 순차 점검한다. 결과 형식은 동일해야 한다.

| worker | 받는 데이터 |
|---|---|
| `plan-review-ssot-worker` (A축) | dispatch 결과 + SSOT corpus 본문 + review-rules.md A축 inline |
| `plan-review-clarity-worker` (B축) | dispatch 결과 (본문만) + review-rules.md B축 inline |
| `plan-review-terminology-worker` (C축) | dispatch 결과 (본문만) + review-rules.md C축 inline |
| `plan-review-readiness-worker` (D축) | dispatch 결과 (본문만) + review-rules.md D축 inline |

각 worker는 `references/review-rules.md`의 `## 발견 사항 필드` 8 필드 표 형식으로 발견 사항만 return한다. 발견 0건 시 응답 끝에 `<!-- worker-flag: no-findings -->` 한 줄 명시. D worker는 readiness 4행 표 (design/development/qa/operations × ready/conditional/blocked/n/a + 사유 + 위치)를 추가 return한다.

worker는 합성·결과 4종 판정·리포트 작성을 하지 않는다. 본문 수정·파일 write도 하지 않는다. 모두 main의 merge가 일괄 처리한다.

### merge (단일 패스)

**읽는 파일**: 없음. dispatch에서 읽은 `review-rules.md`를 재사용 (합성 규칙·결과 4종 기준). 종료 출력 직전에만 `output-format.md`를 read.

- 4 worker 발견 사항 합치기 + `references/review-rules.md`의 `## 합성 규칙` 적용 (위치+제목+근거 정규화 dedup, NFC, 보수 분류).
- 결과 4종 판정 — `references/review-rules.md`의 `## 결과 4종 기준` + `## 보수 합성 우선순위` 적용.
- D readiness 표 검증 — `blocked` 1개라도 → `수정 필요`. 4행 미만이면 1회 retry, 2회 누락 시 해당 역할 `n/a` + 사유 `worker 응답 누락`으로 보수 합성.
- 모든 worker `<!-- worker-flag: no-findings -->` + readiness 모두 `ready`/`n/a` → `통과`.
- worker 발견 사항 형식이 8 필드와 어긋나면 1회 retry, 2회 어긋나면 `검증 한계`에 기록 후 보수 합성.
- `references/output-format.md` 템플릿으로 사람용 리포트 출력. 설정 경고는 dispatch 모은 목록 사용.

현재 대화 컨텍스트는 근거가 아니다. 대화에서 알게 된 배경, 의도, 작성 당시 판단은 검토 대상 파일 또는 SSOT 근거에 없으면 근거 부족으로 본다.

## 규칙

- 검토 기준과 결과 경계는 `references/review-rules.md`만 따른다.
- 최종 출력은 `references/output-format.md`만 따른다. 이 파일은 종료 분기가 확정된 직후 1회만 read한다. YAML manifest 블록은 사용하지 않는다.
- 수정이 필요한 경우 직접 수정하지 않는다. 필수 수정 항목만 제시한다.
- 외부 시스템에 직접 게시하지 않고 Product Docs SSOT Markdown 또는 팀 문서 export snapshot을 자동 수정하지 않는다.
- `<outputRoot>/` 산출물은 review target으로만 읽고 SSOT 근거로 승격하지 않는다.
- 읽은 근거, 읽지 않은 관련 후보, 제외 후보, 검증 한계를 최종 출력에 남긴다.
- 설정 파싱/검증 경고는 사용자 출력 하단에 `[설정 경고]` 블록 한 번으로 표기한다. 경고 포맷은 `../../references/config-contract.md`를 따른다.
