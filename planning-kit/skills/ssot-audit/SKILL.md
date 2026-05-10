---
name: ssot-audit
description: "현재 프로젝트의 Markdown SSOT corpus 자체를 구조 품질·내용 품질 2축으로 감사하고, 발견/권고와 개선 backlog를 화면 markdown only로 출력할 때 사용한다. 기본 범위는 프로젝트 폴더 안 모든 *.md이며, v0.8 미만 문서는 SSOT 후보에서 제외하고 외부 링크는 기본으로 cap 없이 follow한다."
argument-hint: "[--ssot-include <glob>] [--exclude <glob>] [--axes <structure,content>] [--no-follow-links] [--no-image]"
---

# ssot-audit

## 책임

`ssot-audit`는 review 대상 산출물을 입력으로 받지 않는다. 현재 working directory의 Markdown corpus를 SSOT 후보로 수집하고, SSOT 체계 자체의 구조 품질과 내용 품질을 점검해 실행 가능한 개선 backlog를 응답 markdown에만 출력한다.

비목표:

- SSOT 문서를 자동 수정하지 않는다.
- 감사 결과를 파일로 저장하지 않는다.
- `--save` 옵션을 만들지 않는다.
- 운영 품질 축(소유자, 갱신일, 상태 메타데이터 완비성)은 MVP에서 다루지 않는다.
- 점수, 등급, health score를 출력하지 않는다.

## 인자

| 옵션 | 기본값 | 설명 |
|---|---|---|
| `--ssot-include <glob>` | 프로젝트 폴더 안 모든 `*.md` | SSOT corpus 후보 glob. 지정하면 해당 glob에 맞는 Markdown만 1차 후보로 삼는다. |
| `--exclude <glob>` | `.git/**`, `node_modules/**` | corpus 후보 제외 glob. 반복 지정 또는 comma 구분을 허용한다. |
| `--axes <list>` | `structure,content` | 감사 축. `structure`, `content` 콤마 구분. 빈 값이면 sanity check. |
| `--no-follow-links` | off | Markdown 안 외부 URL fetch + connector fallback을 봉쇄한다. 로컬 Markdown만 분석한다. |
| `--no-image` | off | 로컬/외부 이미지 multimodal 해석을 0건으로 만든다. URL fetch는 유지하되 `image/*` 응답은 본문 합류하지 않는다. |

cap 관련 인자(`--depth`, `--max-pages`, `--max-body`, `--max-image`)는 두지 않는다. cycle은 visited set으로만 차단한다.

## 동작 시퀀스

### Step 1: 옵션 파싱 + sanity check

1. `--axes`를 파싱한다.
2. 빈 값이면 `--axes에 감사 축을 1개 이상 지정하세요. (structure, content)` 출력 후 종료.
3. 알 수 없는 축이 있으면 `지원하지 않는 감사 축입니다: <axis>. 사용 가능: structure, content` 출력 후 종료.
4. `--ssot-include`, `--exclude`, `--no-follow-links`, `--no-image` 상태를 출력 헤더용으로 기록한다.

### Step 2: 로컬 Markdown 수집

1. 기준 cwd에서 `*.md` 파일을 찾는다.
2. `.git/`, `node_modules/`는 항상 제외한다.
3. `--ssot-include`가 있으면 include glob에 맞는 파일만 후보로 둔다.
4. `--exclude`가 있으면 후보에서 제거한다.
5. 각 파일에서 path, filename, frontmatter, 첫 heading, heading tree, markdown link를 읽는다.
6. 제목 수준 버전 신호를 판정한다. 대상은 frontmatter `title`, 첫 H1, filename stem, 마지막 path segment다. 본문 중간 버전 언급은 포함/제외 기준으로 쓰지 않는다.
7. 버전 신호가 없거나 `v0.8` 이상이면 SSOT 후보로 남긴다.
8. 버전 신호가 `v0.8` 미만이면 SSOT corpus에서 제외한다. 제외 문서는 감사 입력 row에는 남기되 SSOT map 생성, canonical 후보, 내용 충돌 비교에는 사용하지 않는다.
9. 빈 파일은 corpus row로 남기되 본문 분석에는 사용하지 않는다.

버전 비교는 숫자 비교다: `1.0` > `0.9` > `0.8` > `0.7`.

Sanity:

| 케이스 | 메시지 |
|---|---|
| corpus Markdown 0개 | `SSOT 감사 대상 Markdown을 찾을 수 없습니다. --ssot-include 범위 또는 현재 작업 디렉터리를 확인하세요.` |
| 버전 필터 적용 후 SSOT 후보 0개 | `v0.8 이상 또는 버전 없는 SSOT 후보 Markdown을 찾을 수 없습니다. 낮은 버전 문서를 기준으로 쓰려면 먼저 문서 버전을 올리거나 최신 기준 문서를 분리하세요.` |

### Step 3: 문서 역할 분류

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

역할은 감사 보조 신호다. 명확한 충돌 근거가 없으면 발견이 아니라 권고로 시작한다.

`v0.8` 미만 제외 문서는 SSOT 인벤토리 역할 집계에 넣지 않고, 출력의 `SSOT 제외 문서`에 별도 집계한다. 단, 활성 문서가 낮은 버전 문서를 기준처럼 링크하면 구조 품질 발견으로 다룬다.

### Step 4: 외부 링크 follow + 이미지 처리

`--no-follow-links`가 없으면 모든 대상 Markdown 본문에서 URL과 이미지를 추출한다.

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

1. root URL은 Markdown에서 발견된 외부 URL이다.
2. queue push 시점 normalize.
3. depth N 모두 dequeue 후 depth N+1 dequeue.
4. 같은 depth 안에서는 markdown link -> HTML href/src -> plain URL 발견 순서를 유지한다.
5. dequeue된 visited 미포함 URL은 100% fetch 시도한다.
6. 1차 WebFetch는 의무다.
7. connector fallback은 `../planning-format/references/connector-routing.md`를 1회 Read해서 공유한다.
8. 실패도 출처 행으로 기록하고 visited 등록한다.

외부 fetch 본문은 SSOT corpus 보조 본문으로 합류한다. 외부 fetch 결과가 사실상 canonical이면 구조 품질 감사에서 권고 후보가 된다.

`--no-image`가 없으면 image queue는 5경로를 따른다.

1. 로컬 Markdown이 참조한 이미지 파일.
2. Markdown image / HTML img.
3. fetch 응답이 `image/*` content-type.
4. inline `data:image/...;base64,...`.
5. corpus 안 상대 경로 이미지 참조.

이미지는 multimodal 해석으로 텍스트 설명을 생성해 corpus 보조 본문에 합류한다.

### Step 5: SSOT map 생성

수집된 로컬 Markdown + 외부 fetch 본문 + 이미지 해석 결과에서 다음 후보를 추출한다.

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

- 화면 output only다.
- 활성 안 한 축의 section은 생략한다.
- 발견/권고가 0건이면 해당 section에 `없음` 한 줄을 출력한다.
- 점수·등급은 출력하지 않는다.
- 개선 backlog는 발견/권고를 문제 단위로 묶어 중복을 줄인다.

## 참고 파일

- `references/structure-rules.md` — 구조 품질 감사 기준.
- `references/content-rules.md` — 내용 품질 감사 기준.
- `references/output-contract.md` — 출력 포맷, sanity 메시지, backlog 우선순위.
- `../planning-format/references/connector-routing.md` — 외부 URL fetch + connector fallback 공통 규칙.
- `../planning-format/references/conversion-rules.md` — 이미지 multimodal·통합 본문 합류 룰 참고.
- `../planning-review/references/ac-rules.md` — 검증 가능한 조건 부재 판단 참고.
