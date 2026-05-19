# planning-kit PRD 0.2.7

> 0.2.6 기반 incremental PRD. `planning-kit`에 신규 스킬 `ssot-audit`를 추가해 현재 프로젝트의 Markdown 문서 전체를 SSOT corpus로 분석하고, SSOT 자체의 구조 품질·내용 품질 발견/권고와 개선 backlog를 화면에 출력한다. 추가로 `planning-review` 단일 파일 입력 시 같은 폴더의 관련 파일을 함께 읽도록 보강한다. 본 PRD 외 기존 `planning-format` / `planning-review` 명세는 [`prd-0.2.6.md`](./prd-0.2.6.md) 이하 chain 그대로.
>
> 핵심 변경: `ssot-audit` 신규 스킬. 기본 범위는 프로젝트 폴더 안 모든 `*.md`이며, 기본으로 외부 링크를 cap 없이 재귀 follow하고 connector fallback을 사용한다. 산출물은 저장 없이 실행 화면 markdown으로만 출력한다. `planning-review <단일 파일>`은 해당 파일의 같은 폴더 안 파일을 non-recursive로 함께 읽어 정책서·기능설계서 쌍을 찾는다.

## 1. 변경 요약

1. **신규 스킬 `ssot-audit` 추가** — `planning-format` / `planning-review`와 별개로 SSOT corpus 자체를 감사한다.
2. **기본 corpus 범위** — 프로젝트 폴더 안 모든 `*.md`를 대상으로 삼고 `.git/`, `node_modules/`는 제외한다. `--ssot-include <glob>` / `--exclude <glob>`로 범위를 조정한다.
3. **버전 기준선 필터** — 문서 제목/파일명/H1에서 `v0.8` 이상(`0.8`, `0.9`, `1.0` 등) 또는 버전 없음이면 SSOT 후보로 남긴다. `v0.8` 미만(`0.7` 등)은 SSOT corpus로 취급하지 않는다.
4. **외부 링크 기본 follow** — 대상 Markdown 안 URL·이미지를 추출해 cap 없이 BFS 재귀 fetch한다. 1차 WebFetch + connector fallback은 `planning-format`의 `connector-routing.md`를 공유한다.
5. **감사 축 2개** — MVP 기본 축은 `structure,content`다. 운영 품질 축은 이번 PRD 비목표다.
6. **화면 output only** — 감사 결과, 출처, 발견/권고, 개선 backlog는 응답 markdown에만 출력한다. 파일 저장 옵션은 도입하지 않는다.
7. **개선 backlog 제공** — 발견/권고를 문제 단위로 묶고 영향 문서·권장 작업·검증 조건을 함께 출력한다.
8. **planning-review 단일 파일 입력 보강** — `planning-review <파일>`은 해당 파일만 보지 않고 같은 폴더의 모든 sibling 파일을 함께 읽어 정책서·기능설계서 본문을 식별한다.

## 2. 동기

`planning-review`는 새로 만든 정책서·기능설계서가 기존 SSOT와 충돌하는지 확인한다. 하지만 planning-kit을 실제 프로젝트에서 계속 쓰면 시간이 지날수록 SSOT corpus 자체가 커지고, 다음 문제가 생긴다.

- 같은 도메인의 기준 문서가 여러 곳에 흩어진다.
- 어떤 문서가 canonical인지 불명확해진다.
- draft/old/archive 문서가 최신 문서처럼 참조된다.
- 정책값·상태명·권한명·임계값이 문서마다 조금씩 달라진다.
- 외부 위키나 Google Docs가 사실상 기준인데 로컬 문서는 링크만 들고 있다.

이 상태에서는 `planning-review`가 충돌을 잘 찾아도, 충돌의 원인이 "새 기획의 문제"인지 "SSOT 체계의 부채"인지 판단하기 어렵다. `ssot-audit`는 주기적으로 현재 프로젝트의 SSOT 구조와 내용을 점검해 유지보수 backlog를 만든다.

## 3. 비목표

- SSOT 문서를 자동 수정하지 않는다.
- 감사 결과를 파일로 저장하지 않는다.
- `--save` 옵션을 추가하지 않는다.
- 운영 품질 축(소유자, 최종 갱신일, 상태, 출처 메타데이터 완비성 등)은 이번 MVP에 포함하지 않는다.
- 점수·등급·health score를 출력하지 않는다.
- PRD, 정책서, 기능설계서 등 기존 문서 포맷을 강제 변경하지 않는다.
- 호출 간 fetch cache, retry/backoff, connector 인증 자동 완료는 도입하지 않는다.
- `planning-review`의 산출물 검증 흐름을 대체하지 않는다.

## 4. 스킬 위치와 책임

`planning-kit`은 0.2.7부터 세 스킬 구조가 된다.

| 스킬 | 책임 |
|---|---|
| `planning-format` | 기획 초안 입력을 정책서·기능설계서 두 본문으로 변환하고 자체 품질을 점검 |
| `planning-review` | 특정 정책서·기능설계서 산출물을 외부 SSOT 충돌·AC·의존 영향 3축으로 검증 |
| `ssot-audit` | 현재 프로젝트의 SSOT corpus 자체를 구조·내용 2축으로 감사하고 개선 backlog 제안 |

`ssot-audit`는 review 대상 산출물을 입력으로 받지 않는다. 기본 실행은 현재 working directory의 Markdown corpus 전체를 대상으로 한다.

### 4.1 planning-review 단일 파일 입력 확장

0.2.7부터 `planning-review`의 **1개 파일 입력**은 해당 파일만 읽는 분기가 아니다. 사용자가 정책서 또는 기능설계서 파일 하나만 지정해도, 같은 폴더 안의 sibling 파일을 함께 읽어 정책서·기능설계서 쌍을 구성한다.

동작 규칙:

1. 입력 파일의 parent directory를 companion scan 범위로 잡는다.
2. scan 범위는 **non-recursive**다. 하위 폴더는 읽지 않는다.
3. 같은 폴더의 모든 읽을 수 있는 UTF-8 텍스트 파일과 planning-kit 지원 이미지 파일을 input collection에 추가한다.
4. 숨김 파일, binary, dependency/build/cache 성격 파일은 읽지 않는다. 판단 기준은 `planning-format` 디렉터리 입력의 기본 제외 규칙을 따른다.
5. source title/path/H1/본문 헤더로 `정책서`와 `기능설계서` 후보를 식별한다.
6. 입력 파일과 같은 기능명/stem/domain으로 보이는 후보를 우선한다.
7. 후보가 1쌍으로 확정되면 두 본문을 함께 리뷰한다.
8. 같은 폴더에 여러 기능의 정책서·기능설계서가 섞여 있고 1쌍으로 좁힐 수 없으면 임의 병합하지 않고 sanity check로 종료한다.
9. 같은 폴더를 모두 읽었는데도 한쪽 본문만 있으면 기존처럼 한쪽 본문 비어 있음 또는 본문 식별 실패 메시지로 종료한다.

이 변경은 단일 파일 입력의 편의 확장이다. `planning-review`가 새 정책서·기능설계서를 생성하거나, 같은 폴더 밖의 파일을 자동 탐색하거나, SSOT corpus를 review 대상 본문으로 승격하는 것은 아니다.

## 5. 인자와 옵션

### 5.1 호출 예시

```bash
/planning-kit:ssot-audit

/planning-kit:ssot-audit --ssot-include "docs/**/*.md"

/planning-kit:ssot-audit \
  --ssot-include "docs/**/*.md" \
  --exclude "docs/archive/**" \
  --axes structure

/planning-kit:ssot-audit --no-follow-links --no-image
```

Codex:

```bash
$ssot-audit
$ssot-audit --ssot-include "docs/**/*.md" --axes structure,content
```

### 5.2 옵션

| 옵션 | 기본값 | 설명 |
|---|---|---|
| `--ssot-include <glob>` | 프로젝트 폴더 안 모든 `*.md` | SSOT corpus 후보 glob. 지정하면 해당 glob에 맞는 Markdown만 1차 후보로 삼는다. |
| `--exclude <glob>` | `.git/**`, `node_modules/**` | corpus 후보에서 제외할 glob. 반복 지정 또는 comma 구분을 허용한다. |
| `--axes <list>` | `structure,content` | 감사 축. `structure`, `content` 콤마 구분. 빈 값이면 sanity check. |
| `--no-follow-links` | off | Markdown 안 외부 URL fetch + connector fallback 봉쇄. 로컬 Markdown만 분석한다. |
| `--no-image` | off | 로컬/외부 이미지 multimodal 해석 0건. URL fetch는 그대로 진행하되 image content-type 응답은 본문 합류하지 않는다. |

cap 관련 인자(`--depth`, `--max-pages`, `--max-body`, `--max-image`)는 두지 않는다. 기존 planning-kit 철학과 같이 품질·검증을 우선하고, cycle은 visited set으로만 차단한다.

## 6. Corpus 수집

### 6.1 로컬 Markdown 수집

1. 기준 cwd에서 `*.md` 파일을 찾는다.
2. `.git/`, `node_modules/`는 항상 제외한다.
3. `--ssot-include`가 있으면 include glob에 맞는 파일만 후보로 둔다.
4. `--exclude`가 있으면 후보에서 제거한다.
5. 각 파일의 path, filename, frontmatter, 첫 heading, heading tree, markdown link를 읽는다.
6. 제목 수준 버전 신호를 판정한다. 대상은 frontmatter `title`, 첫 H1, filename stem, 마지막 path segment다. 본문 중간의 버전 언급은 corpus 포함/제외 기준으로 쓰지 않는다.
7. 버전 신호가 없으면 현재 기준 후보로 보고 SSOT corpus에 남긴다.
8. 버전 신호가 `v0.8` 이상이면 SSOT corpus에 남긴다. 예: `v0.8`, `0.8`, `v0.9`, `1.0`.
9. 버전 신호가 `v0.8` 미만이면 SSOT corpus에서 제외한다. 예: `v0.7`, `0.6`. 제외 문서는 감사 입력 row에는 남기되 SSOT map 생성, 구조 품질 canonical 후보, 내용 품질 충돌 비교에는 사용하지 않는다.

빈 파일은 corpus row로 남기되 본문 분석에는 사용하지 않는다. 버전 비교는 숫자 비교로 수행한다 (`1.0` > `0.9` > `0.8` > `0.7`).

### 6.2 문서 역할 분류

파일명, 경로, 제목, heading 신호로 문서 역할을 분류한다.

| 역할 | 신호 |
|---|---|
| README | `README.md`, title `README`, 설치/사용/구성 안내 중심 |
| PRD | path/title에 `prd`, `PRD`, `requirements`, `요구사항` |
| 정책서 | path/title/header에 `policy`, `정책`, `규칙`, `rule` |
| 기능설계서 | `feature`, `design`, `spec`, `기능설계서`, `기능 명세` |
| 회의록/메모 | `meeting`, `minutes`, `memo`, `회의`, `노트` |
| archive/draft | `archive`, `old`, `deprecated`, `draft`, `wip`, `legacy`, `폐기`, `초안` |
| unknown | 위 신호로 분류 불가 |

역할은 감사 보조 신호다. 역할 분류 자체가 틀릴 수 있으므로, 발견은 `권고`로 시작하고 명확한 충돌 근거가 있을 때만 `발견`으로 승격한다.

`v0.8` 미만으로 제외된 문서는 SSOT 인벤토리 역할 집계에 포함하지 않고, 출력의 `SSOT 제외 문서`에 별도 집계한다. 단, 활성 문서가 낮은 버전 문서를 기준처럼 링크하면 구조 품질 발견으로 다룬다.

### 6.3 외부 링크 follow

`--no-follow-links`가 없으면 모든 대상 Markdown 본문에서 URL·이미지 참조를 추출한다.

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

fetch queue는 기존 planning-kit 0.2.5 결정성 룰을 따른다.

- root URL은 Markdown에서 발견된 외부 URL이다.
- queue push 시점 normalize.
- depth N 모두 dequeue 후 depth N+1 dequeue.
- 같은 depth 안에서는 본문 발견 순서 유지: markdown link → HTML href/src → plain URL.
- dequeue된 visited 미포함 URL은 100% fetch 시도.
- 1차 WebFetch 의무.
- connector fallback은 `skills/planning-format/references/connector-routing.md`를 공유 적재.
- 실패도 출처 행으로 기록하고 visited 등록.

외부 fetch 본문은 SSOT corpus 보조 본문으로 합류한다. 외부 fetch 결과가 사실상 canonical 문서로 보이면 구조 품질 감사에서 별도 권고 후보가 된다.

### 6.4 이미지 처리

`--no-image`가 없으면 image queue는 기존 planning-kit 5경로를 따른다.

1. 로컬 Markdown이 참조한 이미지 파일.
2. Markdown image / HTML img.
3. fetch 응답이 `image/*` content-type.
4. inline `data:image/...;base64,...`.
5. corpus 안 상대 경로 이미지 참조.

이미지는 Claude의 multimodal 해석으로 텍스트 설명을 생성해 corpus 보조 본문에 합류한다.

## 7. SSOT map 생성

수집된 로컬 Markdown + 외부 fetch 본문 + 이미지 해석 결과에서 다음 후보를 추출한다.

- 도메인/기능명 후보: path segment, title, H1/H2, 반복 명사구.
- 정책명 후보: `정책`, `rule`, `policy`, `허용`, `금지`, `필수`, `예외`.
- 상태 후보: `status`, `state`, `상태`, 전이 표현, enum-like list.
- 권한/역할 후보: `admin`, `user`, `owner`, `manager`, `관리자`, `사용자`, `담당자`.
- 임계값 후보: 숫자 + 단위(시간, 일, 회, %, 원, 개수).
- 결정 문장 후보: `[TBD]`가 아니고 단정형인 문장.
- 모호 표현 후보: `[TBD]`, `추후`, `필요 시`, `적절히`, `가능하면`, `협의`, `검토 예정`.

SSOT map은 출력 파일로 저장하지 않는다. 감사 결과와 backlog를 만들기 위한 내부 구조다.

## 8. 구조 품질 감사

구조 품질은 "문서 체계가 유지보수 가능한가"를 본다.

### 8.1 canonical 후보 중복

같은 도메인/정책/기능에 대해 canonical처럼 보이는 문서가 2개 이상이면 발견 또는 권고한다.

canonical 신호:

- path/title에 `policy`, `정책`, `spec`, `design`, `기능설계서`, `SSOT`, `canonical`, `current`.
- README 또는 index에서 기준 문서처럼 링크됨.
- 본문에 단정형 정책/상태/권한/임계값이 많음.
- archive/draft 신호가 없음.

판정:

- 두 문서가 같은 대상의 다른 기준값을 말하면 `발견`.
- 값 충돌은 없지만 canonical 후보가 여러 개면 `권고`.

### 8.2 canonical 부재

같은 도메인에 회의록/PRD/README 조각은 여러 개 있지만 기준 문서가 없으면 권고한다.

예:

- 주문 취소 관련 PRD와 회의록은 있지만 `docs/policy/order-cancel.md` 같은 기준 문서가 없음.
- 여러 문서가 같은 정책을 언급하지만 "최신 기준" 링크가 없음.

권장 backlog:

- canonical 정책서 또는 기능설계서 생성.
- 기존 조각 문서에서 canonical 문서로 링크 정리.

### 8.3 draft/old/archive/낮은 버전 활성 참조

`draft`, `old`, `archive`, `deprecated`, `legacy`, `wip` 신호가 있는 문서나 `v0.8` 미만 낮은 버전 문서가 활성 문서에서 기준처럼 참조되면 발견한다.

활성 참조 신호:

- README, 정책서, 기능설계서, 최신 PRD에서 archive/draft 문서를 링크.
- README, 정책서, 기능설계서, 최신 PRD에서 `v0.7` 등 낮은 버전 문서를 링크.
- "기준", "정책", "참고", "따름" 같은 표현과 함께 링크.

archive 내부 문서끼리 참조하는 경우는 발견하지 않는다.
낮은 버전 문서끼리의 내부 참조도 발견하지 않는다. 문제는 현재 SSOT 후보가 낮은 버전 문서를 기준처럼 참조하는 경우다.

### 8.4 도메인 문서 흩어짐

같은 도메인의 문서가 여러 위치에 흩어져 있고 상호 링크나 상위 index가 없으면 권고한다.

예:

- `docs/prd/order.md`
- `docs/policy/order.md`
- `meetings/order.md`

위 세 문서가 서로 링크되지 않고, 상위 index도 없다면 사용자는 어느 문서를 먼저 읽어야 하는지 알기 어렵다.

권장 backlog:

- 도메인 index 문서 생성.
- canonical 문서를 중심으로 PRD/회의록/보조 문서 링크 정리.

### 8.5 문서 역할 불명확

문서 제목·경로·본문 구조로 역할을 판단하기 어렵거나, 정책/기능/회의 메모가 한 문서에 섞여 있으면 권고한다.

예:

- 제목이 `주문 정리`이고 본문에 정책 결정, 구현 메모, 회의 코멘트가 섞임.
- H1/H2에 문서 종류가 없고 본문도 checklist/메모/정책이 혼재.

권장 backlog:

- 제목 또는 H1에 문서 역할 명시.
- 정책 기준은 정책서로, 구현 상세는 기능설계서로, 회의 기록은 회의록으로 분리.

### 8.6 외부 canonical 의존

로컬 Markdown에는 외부 링크만 있고, 외부 fetch 본문이 사실상 기준 문서라면 권고한다.

신호:

- 로컬 문서 본문이 짧고 외부 링크가 대부분.
- 외부 본문에 정책/상태/권한/임계값이 풍부함.
- 로컬 문서에 외부 문서의 역할, 요약, 최신성, 참조 이유가 없음.

권장 backlog:

- 로컬 문서에 핵심 결정 요약 추가.
- 외부 문서를 canonical로 명시.
- 외부 문서가 사라지거나 인증 실패해도 최소 기준을 알 수 있는 fallback 설명 추가.

## 9. 내용 품질 감사

내용 품질은 "SSOT 본문 안 기준이 서로 일관되고 실행 가능한가"를 본다.

### 9.1 정책/상태/권한/임계값 충돌

같은 대상에 대해 문서마다 결정값이 다르면 발견한다.

예:

- 한 문서: "결제 후 24시간 내 취소 가능"
- 다른 문서: "결제 후 48시간 내 취소 가능"

충돌 유형:

- 정책 결정 충돌: 허용/금지/필수 여부가 다름.
- 상태 전이 충돌: 시작 상태, 종료 상태, 트리거가 다름.
- 권한 충돌: 가능한 역할 또는 승인 주체가 다름.
- 임계값 충돌: 시간, 횟수, 금액, 비율, 개수 기준이 다름.

`v0.8` 미만으로 제외된 낮은 버전 문서는 내용 충돌 비교 source로 사용하지 않는다. 낮은 버전 문서가 최신 기준처럼 참조되는 문제는 8.3 구조 품질 발견으로만 기록한다.

### 9.2 용어 불일치

같은 개념이 여러 이름으로 쓰이면 권고한다. 용어 불일치가 정책값 충돌로 이어지면 발견으로 승격한다.

예:

- `pending`, `waiting`, `대기중`이 같은 상태처럼 사용됨.
- `관리자`, `운영자`, `매니저`가 같은 권한처럼 쓰이지만 차이가 설명되지 않음.

권장 backlog:

- canonical 용어 선택.
- 용어표 또는 정책서 §용어에 반영.
- 기존 문서 표현 일괄 정리.

### 9.3 미결/모호 표현

SSOT 본문에 테스트 불가능한 표현이 남아 있으면 권고한다. 핵심 정책값이 `[TBD]`거나 승인 조건이 비어 있으면 발견으로 승격한다.

대상 표현:

- `[TBD]`, `TODO`, `미정`
- `추후`, `추후 협의`, `검토 예정`
- `필요 시`, `상황에 따라`
- `적절히`, `충분히`, `빠르게`, `가능하면`

권장 backlog:

- 담당 판단 기준 추가.
- 임계값/상태/행위자/결과 조건 추가.
- 결정 보류라면 보류 사유와 결정 예정 시점 명시.

### 9.4 검증 가능한 조건 부재

정책은 있지만 누가, 언제, 어떤 상태에서, 어떤 결과를 확인해야 하는지 없으면 권고한다.

예:

- "부정 사용자는 제한한다."
- "관리자는 필요 시 승인할 수 있다."

권장 backlog:

- 행위자, 트리거, 전/후 상태, 관찰 가능한 결과를 추가.
- acceptance criteria 또는 테스트 가능한 확인 조건 추가.

### 9.5 설명 없는 중복

비슷한 문서가 같은 내용을 반복하지만 차이와 관계가 설명되지 않으면 권고한다. 중복 문서끼리 기준값이 다르면 9.1 충돌 발견으로 승격한다.

권장 backlog:

- 병합.
- 하나를 canonical로 지정.
- 다른 문서는 보조 문서로 역할 명시.
- 중복 유지가 필요하면 차이와 적용 범위를 명시.

## 10. 발견/권고 분류

| 분류 | 기준 |
|---|---|
| 발견 | 문서 간 값 충돌, archive/낮은 버전 활성 참조, 핵심 정책값 `[TBD]`, 같은 대상의 권한/상태 결정 충돌처럼 근거가 명확한 문제 |
| 권고 | canonical 후보 불명확, 문서 역할 불명확, 용어 정리 필요, AC 보강 필요처럼 사람이 최종 판단해야 하는 개선 후보 |

같은 문제가 구조와 내용 양쪽에 걸치면 한 번만 기록한다. 우선순위는 `내용 충돌 발견 > 구조 발견 > 내용 권고 > 구조 권고`다.

## 11. 출력 포맷

출력은 화면 markdown only다.

````markdown
# ssot-audit

- SSOT 범위: [프로젝트 전체 *.md | --ssot-include glob]
- 제외: [glob list]
- 분석 축: [structure, content]
- 외부 링크 처리: [활성, cap 없음 | --no-follow-links]
- 이미지 처리: [활성 | --no-image]
- 로컬 Markdown: N개
- SSOT 제외(낮은 버전): L개
- 외부 출처: fetch 성공 K개 / 실패 J개

---

## 감사 결과

- 구조 품질: 발견 N건 / 권고 M건
- 내용 품질: 발견 N건 / 권고 M건

## SSOT 인벤토리

(`v0.8` 미만 제외 후 SSOT corpus 기준)

| 역할 | 문서 수 | 대표 문서 |
|---|---:|---|
| README | N | ... |
| PRD | N | ... |
| 정책서 | N | ... |
| 기능설계서 | N | ... |
| 회의록/메모 | N | ... |
| archive/draft | N | ... |
| unknown | N | ... |

## SSOT 제외 문서

(`v0.8` 미만 문서가 1개 이상일 때만)

| 사유 | 문서 수 | 대표 문서 |
|---|---:|---|
| 낮은 버전(`< v0.8`) | L | docs/order-v0.7.md |

## 외부 출처

(외부 follow 또는 image 처리 1건 이상일 때만)

| # | 출처 종류 | URL/경로 | origin (.md file:line) | 상태 | 본문 사용 |
|---|---|---|---|---|---|
| 1 | 자식 URL | https://wiki.example/policy/order | docs/order.md:12 | 200 (via WebFetch) | O |
| 2 | 자식 URL | https://docs.google.com/... | docs/order.md:28 | 200 (via Google Drive connector — read_file_content) | O |
| 3 | 자식 URL | https://private.example/... | docs/order.md:40 | 인증 필요 | X |

## 구조 품질

1. [발견 또는 권고 제목]
   - 분류: [발견 | 권고]
   - 카테고리: [canonical 중복 | canonical 부재 | archive 활성 참조 | 낮은 버전 활성 참조 | 도메인 문서 흩어짐 | 역할 불명확 | 외부 canonical 의존]
   - 위치: [문서 path list]
   - 근거: "[짧은 근거]"
   - 영향: [한 줄]
   - 제안: [최소 개선 방향]

## 내용 품질

1. [발견 또는 권고 제목]
   - 분류: [발견 | 권고]
   - 카테고리: [정책 충돌 | 용어 불일치 | 미결/모호 표현 | 검증 조건 부재 | 설명 없는 중복]
   - 위치: [문서 path list]
   - 근거: "[짧은 근거]"
   - 영향: [한 줄]
   - 제안: [최소 개선 방향]

## 개선 backlog

| 우선순위 | 유형 | 문제 | 영향 문서 | 권장 작업 | 검증 조건 |
|---|---|---|---|---|---|
| P0 | 내용 | 주문 취소 시간 기준 24h/48h 충돌 | docs/a.md, docs/b.md | 기준값 결정 후 한쪽 수정 | 두 문서의 취소 기준이 동일 |
| P1 | 구조 | 주문 도메인 canonical 문서 부재 | docs/prd/order.md, meetings/order.md | 정책서 또는 index 생성 | README/index에서 canonical로 연결 |
````

규칙:

- 활성 안 한 축의 section은 생략한다.
- 발견/권고가 0건이면 해당 section에 `없음` 한 줄을 출력한다.
- 점수·등급은 출력하지 않는다.
- 개선 backlog는 발견/권고를 문제 단위로 묶어 중복을 줄인다.
- backlog 우선순위는 작업 순서 안내일 뿐 health score가 아니다.

## 12. Backlog 우선순위

| 우선순위 | 기준 |
|---|---|
| P0 | 같은 정책/상태/권한/임계값의 직접 충돌, archive 또는 낮은 버전 문서가 최신 기준처럼 참조되는 문제 |
| P1 | canonical 부재/중복, 외부 canonical 의존, 핵심 문서 역할 불명확 |
| P2 | 용어 통일, AC 보강, 설명 없는 중복 정리 |

P0/P1/P2는 화면 출력 정렬용이다. 점수화하지 않는다.

## 13. sanity check

| 케이스 | 메시지 |
|---|---|
| corpus Markdown 0개 | `SSOT 감사 대상 Markdown을 찾을 수 없습니다. --ssot-include 범위 또는 현재 작업 디렉터리를 확인하세요.` |
| 버전 필터 적용 후 SSOT 후보 0개 | `v0.8 이상 또는 버전 없는 SSOT 후보 Markdown을 찾을 수 없습니다. 낮은 버전 문서를 기준으로 쓰려면 먼저 문서 버전을 올리거나 최신 기준 문서를 분리하세요.` |
| `--axes` 빈 값 | `--axes에 감사 축을 1개 이상 지정하세요. (structure, content)` |
| 알 수 없는 축 | `지원하지 않는 감사 축입니다: <axis>. 사용 가능: structure, content` |
| 외부 URL 모두 실패 | 감사는 계속 진행. `## 외부 출처`에 실패 행을 기록하고 로컬 Markdown 기준으로 결과 출력 |
| 로컬 Markdown 본문 대부분 비어 있음 | 감사는 계속 진행. 구조 품질에 `본문 없는 SSOT 후보` 권고 가능 |

외부 fetch 실패는 MVP에서 운영 품질 발견으로 자동 승격하지 않는다. 단, 외부 canonical 의존 판단에 필요한 본문을 가져오지 못하면 해당 항목은 `권고`로만 출력한다.

## 14. 호환성

| 영역 | 0.2.6 → 0.2.7 |
|---|---|
| `planning-format` | 변경 없음 |
| `planning-review` | 단일 파일 입력 시 같은 폴더 sibling 파일을 함께 읽어 정책서·기능설계서 쌍을 식별 |
| 신규 skill | `ssot-audit` 추가 |
| manifest | skill list에 `ssot-audit` 추가, version 0.2.7 |
| README | 세 스킬 구조와 `ssot-audit` 예시 추가 필요 |
| 출력 markdown | 신규 스킬 출력이므로 기존 parser 영향 없음 |

## 15. 호출 시나리오

1. **기본 전체 감사**:
   ```bash
   /planning-kit:ssot-audit
   ```
   프로젝트 전체 Markdown + 외부 링크 follow로 구조/내용 2축 감사.

2. **docs 폴더만 감사**:
   ```bash
   /planning-kit:ssot-audit --ssot-include "docs/**/*.md"
   ```
   docs 아래 Markdown만 corpus 후보.

3. **archive 제외**:
   ```bash
   /planning-kit:ssot-audit --exclude "docs/archive/**"
   ```
   archive 문서를 corpus에서 빼고 현재 활성 문서 중심으로 감사. 단 archive 활성 참조 문제를 찾으려면 archive를 제외하지 않는 호출이 더 적합하다.

4. **버전 기준선 적용**:
   ```bash
   /planning-kit:ssot-audit
   ```
   `사용자 관리 v0.9.md`, `권한 관리 v1.0.md`, `버전 없는 정책서.md`는 SSOT 후보로 남긴다. `로케이션 관리 v0.7.md`처럼 `v0.8` 미만인 문서는 SSOT corpus에서 제외하고 `SSOT 제외 문서`에 집계한다.

5. **구조 품질만 감사**:
   ```bash
   /planning-kit:ssot-audit --axes structure
   ```
   canonical, archive 참조, 문서 역할, 외부 canonical 의존만 점검.

6. **오프라인/빠른 감사**:
   ```bash
   /planning-kit:ssot-audit --no-follow-links --no-image
   ```
   로컬 Markdown만 분석. 외부 canonical 의존 판단은 제한된다.

7. **planning-review 단일 파일 입력 + 같은 폴더 companion read**:
   ```bash
   /planning-kit:planning-review ./.planning-kit/주문취소/정책서.md
   ```
   `정책서.md`만 보지 않고 같은 폴더의 `기능설계서.md`, 보조 설명 파일, 지원 이미지 파일을 함께 읽어 review 대상 본문을 구성한다. 같은 폴더에 여러 기능 파일이 섞여 1쌍으로 좁힐 수 없으면 임의 병합하지 않고 sanity check로 종료한다.

## 16. 대안 검토

| 대안 | 채택 여부 |
|---|---|
| `planning-review --audit-ssot` 옵션으로 추가 | 비채택 — `planning-review`는 특정 산출물 검증, `ssot-audit`는 corpus 자체 감사라 책임이 다름 |
| `planning-maintenance` 같은 넓은 운영 스킬 추가 | 비채택 — PRD chain 정리, release checklist, 문서 수정까지 포함하면 MVP가 과대해짐 |
| 운영 품질 축까지 MVP 포함 | 비채택 — 소유자/갱신일/상태 메타데이터 룰을 먼저 정해야 하므로 후속 PRD 후보 |
| 기본 외부 follow off | 비채택 — 사용자는 SSOT 전체 구조·내용 분석을 원하며, 외부 링크가 사실상 기준인 경우를 기본으로 잡아야 함 |
| depth/page/body cap 추가 | 비채택 — 기존 planning-kit의 cap 없음 정책과 불일치 |
| 감사 결과 파일 저장 | 비채택 — 초기 스킬은 실행 화면 output only |
| 점수/등급 출력 | 비채택 — 숫자 과신 위험. 발견/권고와 backlog 중심으로 유지 |

## 17. 마이그레이션

기존 사용자는 변경 없이 `planning-format` → `planning-review` 흐름을 계속 사용한다.

신규 권장 운영 흐름:

```bash
/planning-kit:ssot-audit
/planning-kit:planning-format <기획 초안>
/planning-kit:planning-review
```

정기적으로 `ssot-audit`를 실행해 SSOT backlog를 정리하고, 새 기획 검토에는 기존처럼 `planning-review`를 사용한다.

## 18. 영향 범위

- `skills/ssot-audit/SKILL.md` — 신규 스킬 orchestration.
- `skills/ssot-audit/references/structure-rules.md` — 구조 품질 감사 기준.
- `skills/ssot-audit/references/content-rules.md` — 내용 품질 감사 기준.
- `skills/ssot-audit/references/output-contract.md` — 화면 output 포맷과 backlog 규칙.
- `skills/planning-review/SKILL.md` — 단일 파일 입력 시 same-folder companion read 규칙 반영.
- `skills/planning-format/references/connector-routing.md` — 외부 follow에서 공유 적재. 변경은 최소화하거나 설명 보강만.
- `skills/planning-format/references/conversion-rules.md` — 이미지 multimodal·통합 본문 합류 룰 참조 가능.
- `skills/planning-review/references/ac-rules.md` — 검증 가능한 조건 부재 판단에 참고 가능.
- `planning-kit/README.md` — 세 스킬 구조, quick start, 옵션, 결과 형태, `planning-review` 단일 파일 companion read 예시 갱신.
- `planning-kit/.claude-plugin/plugin.json` / `.codex-plugin/plugin.json` — version 0.2.7, skill 설명 추가.
- `.claude-plugin/marketplace.json` / `.agents/plugins/marketplace.json` — planning-kit version 갱신.
- `docs/prd/README.md` — 0.2.7 row 추가.

## 19. 용어

- **SSOT audit**: 현재 프로젝트 문서 corpus 자체의 구조·내용 품질을 점검하는 작업.
- **companion read**: `planning-review` 단일 파일 입력 시 같은 폴더의 sibling 파일을 함께 읽어 정책서·기능설계서 쌍을 찾는 입력 보강 절차.
- **canonical 문서**: 특정 도메인/정책/기능의 기준으로 읽어야 하는 문서.
- **외부 canonical 의존**: 로컬 Markdown보다 외부 링크 본문이 사실상 기준 역할을 하는 상태.
- **버전 기준선**: SSOT 후보로 인정하는 최소 제목 버전. 0.2.7 기준 `v0.8` 이상 또는 버전 없음만 SSOT 후보이며, `v0.7` 등 낮은 버전 문서는 제외한다.
- **낮은 버전 문서**: 제목/파일명/H1의 버전 신호가 `v0.8` 미만인 Markdown 문서. SSOT corpus로 쓰지 않고 별도 제외 집계한다.
- **구조 품질**: 문서 역할, canonical 위치, 링크/계층 구조, archive/draft 참조 상태.
- **내용 품질**: 정책값, 상태, 권한, 임계값, 용어, 검증 가능 조건의 일관성.
- **개선 backlog**: 감사 결과를 실행 가능한 유지보수 작업으로 묶은 화면 출력 표.

그 외 용어는 0.2.6 §17 / 0.2.5 §17 그대로.

## 20. 참고 파일

- `docs/prd/prd-0.2.6.md` — 본 PRD의 베이스.
- `skills/planning-review/references/ssot-rules.md` — 기존 SSOT corpus 개념과 link follow 규칙.
- `skills/planning-format/references/connector-routing.md` — 외부 URL fetch + connector fallback 공통 규칙.
- `skills/planning-format/references/exclusion-rules.md` — 모호성 표현과 미결 표현 참고.
- `skills/planning-review/references/ac-rules.md` — 검증 가능한 조건 판단 참고.
- `docs/prd/prd-0.2.7.md` — 본 문서.
