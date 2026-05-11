---
name: ssot-audit
description: "현재 프로젝트에서 폴더명에 독립 SSOT token이 있는 Markdown 기준 문서 묶음만 구조 품질·내용 품질 2축으로 감사하고, 제외 요약·SSOT 인벤토리·발견/권고·개선 백로그를 report-first markdown으로 출력할 때 사용한다. planning/**, .planning-kit/**, 내부 plugin/skill 문서는 corpus가 아니며 SSOT token 폴더가 없으면 프로젝트 전체 Markdown으로 fallback하지 않는다."
argument-hint: "[--ssot-include <glob>] [--exclude <glob>] [--axes <structure,content>] [--no-follow-links] [--no-image]"
---

# ssot-audit

## 책임

`ssot-audit`는 review 대상 산출물을 입력으로 받지 않는다. 현재 working directory에서 선언된 SSOT token 폴더의 Markdown만 corpus로 수집하고, SSOT 체계 자체의 구조 품질과 내용 품질을 점검해 실행 가능한 개선 백로그를 응답 markdown에만 출력한다.

비목표:

- SSOT 문서를 자동 수정하지 않는다.
- 감사 결과를 파일로 저장하지 않는다.
- `--save` 옵션을 만들지 않는다.
- 프로젝트 전체 Markdown inventory 감사 또는 SSOT 후보 발굴을 기본 동작으로 하지 않는다.
- 점수, 등급, health score를 출력하지 않는다.

## 인자

| 옵션 | 기본값 | 설명 |
|---|---|---|
| `--ssot-include <glob>` | (없음) | SSOT token 폴더 후보 안에서 corpus를 좁히는 glob. SSOT token 경계를 우회하지 않는다. |
| `--exclude <glob>` | `.git/**`, `node_modules/**`, `planning/**`, `.planning-kit/**`, 내부 plugin/skill 문서 | corpus 후보 제외 glob. 반복 지정 또는 comma 구분 허용. 기본 제외는 항상 유지한다. |
| `--axes <list>` | `structure,content` | 감사 축. `structure`, `content` 콤마 구분. 빈 값이면 sanity check. |
| `--no-follow-links` | off | Markdown 안 외부 URL fetch + connector fallback을 봉쇄한다. 로컬 SSOT Markdown만 분석한다. |
| `--no-image` | off | 로컬/외부 이미지 multimodal 해석을 0건으로 만든다. URL fetch는 유지하되 `image/*` 응답은 본문 합류하지 않는다. |

cap 관련 인자(`--depth`, `--max-pages`, `--max-body`, `--max-image`)는 두지 않는다. cycle은 visited set으로만 차단한다.

## 동작 시퀀스

### Step 1: 옵션 파싱 + sanity check

1. `--axes`를 파싱한다.
2. 빈 값이면 `--axes에 감사 축을 1개 이상 지정하세요. (structure, content)` 출력 후 종료.
3. 알 수 없는 축이 있으면 `지원하지 않는 감사 축입니다: <axis>. 사용 가능: structure, content` 출력 후 종료.
4. `--ssot-include`, `--exclude`, `--no-follow-links`, `--no-image` 상태를 출력 헤더용으로 기록한다.

### Step 2: SSOT token Markdown 수집

1. 기준 cwd에서 Markdown 파일을 찾는다.
2. 숨김 폴더, `.git/`, `node_modules/`, build/cache 폴더, `planning-kit/skills/**`, `planning-kit/docs/prd/**`, plugin metadata 폴더는 제외한다.
3. `planning/**`과 `.planning-kit/**`은 항상 제외한다. 이 제외가 SSOT token 폴더 허용보다 우선한다.
4. path segment 단위로 폴더명을 검사한다. segment를 공백, 대괄호, 소괄호, 중괄호, underscore로 나눴을 때 `SSOT`와 대소문자 무관으로 같은 token이 있어야 corpus 후보다.
5. 단순 substring은 허용하지 않는다. `ProductSSOT/**`, `docs/ssot-audit/**`, `planning-kit/skills/ssot-audit/**`는 corpus가 아니다.
6. `--ssot-include`가 있으면 SSOT token 후보 안에서만 narrowing한다. SSOT 폴더 밖 glob은 0건으로 처리하고 제외 사유를 남긴다.
7. `--exclude`가 있으면 후보에서 제거한다. 기본 제외는 유지한다.
8. 각 후보 파일에서 path, filename, frontmatter, 첫 heading, heading tree, markdown link, decision sentence 후보를 읽는다.
9. 빈 파일, frontmatter-only, H1-only, "작성 예정" 한 줄, 빈 표는 placeholder로 판정한다.

Sanity:

| 케이스 | 메시지 |
|---|---|
| SSOT token 폴더 없음 | `감사 불가 — 선언된 SSOT token 폴더 없음` |
| SSOT token 폴더 Markdown 0개 | `감사 불가 — SSOT token 폴더 안 Markdown 없음` |
| `--ssot-include`가 SSOT 경계 밖만 매칭 | `감사 불가 — 명시 include가 SSOT 폴더 경계 밖이라 제외됨` |

위 케이스에서도 프로젝트 전체 Markdown으로 fallback하지 않는다. 출력에는 제외 요약과 개선 백로그를 포함한다.

### Step 3: 문서 역할과 placeholder 분류

파일명, 경로, title, H1/H2, 본문 헤더 신호로 역할을 분류한다.

| 역할 | 신호 |
|---|---|
| README | `README.md`, title `README`, 설치/사용/구성 안내 중심 |
| PRD | path/title에 `prd`, `PRD`, `requirements`, `요구사항` |
| 정책서 | path/title/header에 `policy`, `정책`, `규칙`, `rule` |
| 기능설계서 | `feature`, `design`, `spec`, `기능설계서`, `기능 명세` |
| 회의록/메모 | `meeting`, `minutes`, `memo`, `회의`, `노트` |
| archive/draft | `archive`, `old`, `deprecated`, `draft`, `wip`, `legacy`, `폐기`, `초안` |
| unknown | 위 신호로 분류 불가 |

placeholder는 SSOT 인벤토리에서 별도 집계한다. placeholder-only corpus는 감사 한계이며, 프로젝트 전체 Markdown으로 보강하지 않는다.

### Step 4: 외부 링크 follow + 이미지 처리

`--no-follow-links`가 없으면 대상 SSOT Markdown 본문에서 URL과 이미지를 추출한다.

추출 대상:

- markdown link
- autolink
- HTML `href` / `src` / `img`
- plain URL
- markdown image
- data URI

제외:

- self-anchor
- `mailto:`
- `tel:`
- `javascript:`
- `blob:`
- non-http scheme URL (`data:image/...`는 URL fetch가 아니라 image queue로만 보낸다)

Fetch queue:

1. root URL은 SSOT Markdown에서 발견된 외부 URL이다.
2. queue push 시점 normalize.
3. depth N 모두 dequeue 후 depth N+1 dequeue.
4. 같은 depth 안에서는 markdown link -> HTML href/src -> plain URL 발견 순서를 유지한다.
5. dequeue된 visited 미포함 URL은 100% fetch 시도한다.
6. 1차 WebFetch는 의무다.
7. connector fallback은 `../planning-format/references/connector-routing.md`를 1회 Read해서 공유한다.
8. 실패도 출처 행으로 기록하고 visited 등록한다.

외부 fetch 본문은 SSOT corpus 보조 본문으로 합류한다. `--no-image`가 없으면 image queue는 planning-format 5경로를 따른다.

### Step 5: SSOT map 생성

수집된 로컬 SSOT Markdown + 외부 fetch 본문 + 이미지 해석 결과에서 다음 후보를 추출한다.

- 도메인/기능명 후보: path segment, title, H1/H2, 반복 명사구.
- 정책명 후보: `정책`, `rule`, `policy`, `허용`, `금지`, `필수`, `예외`.
- 상태 후보: `status`, `state`, `상태`, 전이 표현, enum-like list.
- 권한/역할 후보: `admin`, `user`, `owner`, `manager`, `관리자`, `사용자`, `담당자`.
- 임계값 후보: 숫자 + 단위(시간, 일, 회, %, 원, 개수).
- 결정 문장 후보: `[TBD]`가 아니고 단정형인 문장.
- 모호 표현 후보: `[TBD]`, `추후`, `필요 시`, `적절히`, `가능하면`, `협의`, `검토 예정`.

SSOT map은 파일로 저장하지 않는다. 감사 결과와 backlog를 만들기 위한 내부 구조다.

### Step 6: 감사 축 실행

활성 축 reference만 lazy read한다.

| 축 | 키 | 적재 reference |
|---|---|---|
| 구조 품질 | `structure` | `references/structure-rules.md` |
| 내용 품질 | `content` | `references/content-rules.md` |

같은 문제가 구조와 내용 양쪽에 걸치면 한 번만 기록한다. 우선순위는 `내용 충돌 발견 > 구조 발견 > 내용 권고 > 구조 권고`다.

### Step 7: 화면 markdown 출력

`references/output-contract.md`를 Read하고 그 형식으로 응답한다.

규칙:

- 최종 출력은 반드시 `# ssot-audit`로 시작한다.
- 최종 출력 앞에 project scan 진행 로그를 쓰지 않는다.
- 화면 output only다.
- 활성 안 한 축의 section은 생략한다.
- 발견/권고가 0건이면 해당 section에 `없음` 한 줄을 출력한다.
- 점수·등급은 출력하지 않는다.
- 개선 backlog는 발견/권고를 문제 단위로 묶어 중복을 줄인다.

## 참고 파일

- `references/structure-rules.md` — 구조 품질 감사 기준.
- `references/content-rules.md` — 내용 품질 감사 기준.
- `references/output-contract.md` — report-first 출력 포맷, sanity 메시지, backlog 우선순위.
- `../planning-format/references/connector-routing.md` — 외부 URL fetch + connector fallback 공통 규칙.
- `../planning-format/references/conversion-rules.md` — 이미지 multimodal·통합 본문 합류 룰 참고.
- `../planning-review/references/ac-rules.md` — 검증 가능한 조건 부재 판단 참고.
