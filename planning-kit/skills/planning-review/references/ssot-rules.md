# SSOT Rules (R1)

`planning-review`의 SSOT 충돌 점검 축(R1). 0.2.9부터 기준 문서 묶음은 프로젝트 전체 Markdown이 아니라 폴더명에 독립 `SSOT` 표시가 있는 하위 폴더 안의 Markdown으로 제한한다. `planning/**`과 `.planning-kit/**`은 생성 초안 영역이므로 항상 제외한다.

## 용어

- **기준 문서 묶음**: 폴더명에 독립 `SSOT` 표시가 있는 기준 문서 폴더 안의 Markdown 후보 중 키워드 매칭과 `--ssot-include` narrowing을 통과한 corpus.
- **input collection**: `planning-review`가 review 대상 본문을 만들기 위해 URL·파일·디렉터리·텍스트·이미지를 수집하는 단계. 입력 URL source 자체는 기준 문서 묶음이 아니다.
- **input fetch**: input collection 안 URL fetch. `--no-input-fetch`로 봉쇄하며, R1/R3 기준 문서 link follow와 별도 visited set을 가진다.
- **SSOT fetch**: R1/R3 기준 문서 link follow. `--no-ssot-fetch`로 봉쇄하며, input fetch와 별도 visited set·출처 블록을 가진다.
- **확정 문장**: 변환 본문 중 `[TBD]`가 아닌 단정 표현.
- **본문 없는 문서**: 빈 파일, frontmatter-only, H1-only, "작성 예정" 한 줄, 빈 표/헤더만 있는 표처럼 정책 값·상태·권한·임계값 등 결정 문장이 없는 파일.
- **보조 표 heading 호환**: 0.2.8 clean header(`### N.M ... 보조 표`)와 0.2.4~0.2.7 legacy backlink header(`### N.M ... 보조 표 (§N row M)`)를 모두 보조 표로 인식한다. 일부 중간 산출물의 `(N row M)` backlink도 읽기 호환으로 보조 표 처리한다. legacy header 자체는 R1 발견으로 강제하지 않는다.

## R1.1 `SSOT` 표시 폴더 후보 추출

1. 기준 cwd에서 Markdown 경로를 수집하되 숨김 폴더, `.git/`, `node_modules/`, build/cache 폴더, `planning-kit/skills/**`, `planning-kit/docs/prd/**`, plugin metadata 폴더는 제외한다.
2. `planning/**`과 `.planning-kit/**`은 항상 제외한다. 이 제외가 `SSOT` 표시 폴더 허용보다 우선한다. 예: `planning/[SSOT]/policy.md`도 제외한다.
3. path segment 단위로 폴더명을 검사한다. segment를 공백, 대괄호, 소괄호, 중괄호, underscore로 나눴을 때 `SSOT`와 대소문자 무관으로 같은 token이 있어야 후보다.
4. 단순 substring은 허용하지 않는다. 하이픈으로 이어진 `ssot-audit`는 도구명이지 기준 문서 폴더 token이 아니다.
5. symlink는 기본적으로 follow하지 않는다.
6. `--ssot-include <glob>`이 있으면 위 후보 안에서만 narrowing한다. glob이 `SSOT` 표시 폴더 밖만 가리키면 결과는 0건이고 `검증 범위와 한계` 및 `## 상세 추적`에 `명시 include가 기준 문서 폴더 경계 밖이라 제외됨`을 남긴다.

허용 예:

```text
Product Docs SSOT/**/*.md
[SSOT] 정책서/**/*.md
Confluence [SSOT] Export/**/*.md
Product_SSOT/**/*.md
```

제외 예:

```text
planning/**/*.md
.planning-kit/**/*.md
docs/**/*.md
README.md
planning-kit/docs/prd/**/*.md
planning-kit/skills/ssot-audit/**/*.md
docs/ssot-audit/**/*.md
ProductSSOT/**/*.md
```

`SSOT` 표시 폴더가 없거나 해당 폴더 안 Markdown이 비어 있으면 `기준 문서 묶음: 0건` 또는 `비교 근거 부족: 비교 대상 본문 없음`으로 표시하고, 프로젝트 전체 Markdown으로 fallback하지 않는다.

## R1.2 corpus 매칭 절차

1. 변환 본문에서 키워드 추출: 기능명·도메인 stem·역할명·상태명·권한명·정책 핵심어.
2. R1.1 후보 안에서 키워드 `grep -l` 또는 `rg -l`로 본문 매칭 → 매칭 file 목록 확정.
3. 본문 없는 문서 여부를 판정한다.
4. 매칭 file을 직접 읽는다. 인덱스 스캔 단계 없음.
5. 매칭 file 본문에서 URL·이미지 참조 추출 — markdown link / autolink / HTML href·src·img / plain URL / markdown image / data URI. self-anchor·`mailto:`/`tel:`/`javascript:`/`blob:` 제외.
6. `--no-ssot-fetch` off이면 추출 URL을 fetch queue에 시드하고 이미지를 image queue에 시드한다.
7. 재귀 fetch + connector fallback — `../planning-format/references/connector-routing.md`를 1회 Read 적재해 그대로 사용한다.
8. 이미지 multimodal 해석 — 지원 확장자·해석 프롬프트는 `planning-format` 4 그대로. `--no-ssot-image` ON이면 image content-type 응답 합류 안 함.
9. 외부 fetch 본문 + 이미지 해석 결과를 기준 문서 body에 합류. visited set으로 cycle 방지. cap 없음.

## R1.3 본문 없는 문서 규칙

본문 없는 문서 판정 예:

| 입력 형태 | 판정 |
|---|---|
| 빈 파일 | 본문 없는 문서 |
| frontmatter만 있는 파일 | 본문 없는 문서 |
| H1 하나만 있고 결정 문장이 없는 파일 | 본문 없는 문서 |
| 제목 + "작성 예정" 한 줄 | 본문 없는 문서 |
| 빈 표 또는 헤더만 있는 표 | 본문 없는 문서 |
| 정책 값·상태·권한·임계값 같은 결정 문장이 1개 이상 있는 파일 | 실질 본문 |

규칙:

- R1 count는 `0건`으로 두되, 설명은 `충돌 없음`이 아니라 `비교 근거 부족: 비교 대상 본문 없음`으로 쓴다.
- `ssot` 축이 활성이고 기준 문서 묶음이 0건 또는 모두 본문 없는 문서이면 검증 신뢰도는 `낮음`이다.
- R2/R3에서 P0/P1 발견이 있으면 최종 판정은 `수정 필요`다.
- R2/R3가 P2-only이고 활성 핵심 축의 비교 대상이 없는 상태라면 `검토 필요`보다 `비교 불가`가 우선한다.
- 본문 없는 문서만 있는 한계는 `SSOT 보강` 작업 백로그에 올릴 수 있지만 verdict용 P2 finding count에는 포함하지 않는다.
- 본문 없는 문서 보강 백로그가 있고 verdict용 finding이 0건이면 상단 발견 count는 `P0 0건, P1 0건, P2 0건`으로 유지하고, `작업 백로그`에는 `A*` 항목을 표시한다. `검증 범위와 한계`에는 `SSOT 보강 작업은 있으나 verdict finding에는 포함하지 않음`을 남긴다.
- 0.2.12: 기준 문서 묶음 0건 또는 모두 본문 없는 문서가 유일한 낮은 신뢰도 원인이고 R2/R3 finding이 없으면 결정 보드에 D* 또는 A*를 만들지 않는다. `## 결정 보드`는 출력하되 관련 subsection은 `없음`으로 두고, 보강 작업은 top-level `## 작업 백로그` 호환용 요약에만 표시한다. 판정은 `비교 불가`를 유지하며 첫 화면 또는 결론에 `비교 근거 부족`을 명시한다.
- `--axes ac`처럼 SSOT가 비활성인 호출에서는 SSOT 보강 작업을 결정 보드나 작업 백로그에 만들지 않는다.
- 로컬 기준 문서는 본문 없는 문서지만 그 안의 외부 link follow 결과가 실질 본문을 제공하면, R1은 외부 본문 기준으로 제한적 비교를 수행한다. 이때 신뢰도는 `제한적`이고, `검증 범위와 한계`에 "로컬 기준 문서는 본문 없는 문서, 외부 본문으로 비교"를 명시한다.
- 본문 없는 문서의 외부 link follow 후보는 본문 키워드 매칭뿐 아니라 파일명, H1, link text, URL label도 매칭 신호로 삼는다. 이 신호로도 매칭되지 않은 기준 문서 폴더 전체를 무조건 follow하지는 않는다.

## R1.4 매칭 0건

- `SSOT` 표시 폴더 후보 0건 또는 keyword 매칭 0건 → R1 결과 `비교 근거 부족: 비교 대상 본문 없음`.
- 프로젝트 전체 Markdown으로 fallback하지 않는다.
- `## 검증 범위와 한계`에 `SSOT` 표시 폴더 경계와 제외 요약을 남긴다.
- `## 상세 추적`에는 후보/제외/본문 없는 문서 경로 요약 또는 include 경계 밖 사유를 남긴다.
- R2·R3는 활성 축이면 별도 진행한다.

## R1.5 매칭 ≥1건

- 변환 본문 확정 문장과 매칭 file 본문 + 외부 fetch 본문(link follow 활성 시)을 직접 비교한다.
- 같은 대상(역할·상태·정책 규칙·임계)이 양쪽에 있고 표기·결정·임계값이 어긋나면 발견한다.
- 같은 대상에 대해 SSOT가 침묵하면 R1 발견이 아니다. R3 권고가 될 수 있다.
- 보조 표 인식: 산출물 상위 섹션 + 보조 표(`### N.M ... 보조 표`) 본문 모두 corpus 비교 대상이다. 보조 표 단독 발견 가능.

## R1.6 발견 ID와 우선순위

- 발견 ID는 `R1-1`, `R1-2` 형식을 쓴다.
- R1 SSOT 충돌 기본 우선순위는 P0 또는 P1이다.
- 정책값/상태/권한/임계값이 구현 판정을 막으면 P0, 적용 범위 충돌이나 문서 정합성 문제면 P1로 둔다.

발견 위치 표기:

```markdown
- 위치: 정책서 5.1 row 3 (보조 표 안) vs Product SSOT/zone.md 2
```

상위 섹션 + 보조 표 + row 모두 식별되면 셋 다 표시한다. 상위 섹션 단독도 가능하다.

## R1.7 link follow

### 트리거 조건

- **R1 활성 OR R3 활성** + **매칭 ≥1** + **`--no-ssot-fetch` off** → link follow 진입.
- R1 단독·R3 단독·둘 다 활성 모두 같은 link follow 단계 사용. corpus는 단일 set이라 어느 축이 트리거해도 양쪽이 같은 corpus를 본다.
- `--axes ac`만 활성(R1·R3 비활성) → link follow 진입 안 함.

### visited set·cycle 방지

- visited set: 기준 문서 묶음의 URL normalize key 집합. URL normalize는 `connector-routing.md` 6 그대로.
- input visited set과 SSOT visited set은 의도적으로 cross-set dedup하지 않는다.
- 같은 URL이 여러 매칭 Markdown에서 발견되면 1번만 fetch + 본문 합류. 출처 list에는 origin file 1번만 표시한다.
- 매칭 Markdown 자체 본문은 cycle 방지 대상이 아니다.
- R1/R3이 fetch한 본문에서 발견된 자식 link도 visited set으로만 제어한다. cap 없음.

### sanity

- 매칭 file ≥1 + link 0건 → 정상. corpus는 매칭 file 본문만.
- 매칭 file ≥1 + link N건 + fetch 모두 실패 → 정상. 기준 문서 묶음은 매칭 file 본문만 사용하고, 출처 list에 사유를 남기고 R1/R3 점검을 진행한다.
- 외부 fetch 결과가 image content-type → `planning-format` 4와 동일하게 image queue로 라우팅한다.
- 루트 매칭 file이 모두 본문 없는 문서여도 호출 종료 안 함. 신뢰도/판정에서 처리한다.

## R1.8 출처 list

0.2.9 기본 출력은 full 기준 문서 출처 표를 상단에 두지 않는다. 다음 조건이면 `## 상세 추적` 안에 `### 기준 문서 출처`를 출력한다.

- link follow가 1건 이상 진행됨.
- 기준 문서 묶음 0건.
- 매칭 기준 문서가 모두 본문 없는 문서.
- `--ssot-include`가 SSOT 폴더 경계 밖만 가리켜 후보가 0건.
- 기준 문서 외부 링크 처리 실패, 인증 실패, 본문 미사용 출처가 1건 이상.

```markdown
### 기준 문서 출처

매칭 *.md: N개
본문 없는 문서: P개
재귀 본문 가져오기: 성공 K개 / 실패 J개 (cap 없음)

| # | 출처 종류 | URL/경로 | origin (.md file:line) | 상태 | 본문 사용 |
|---|---|---|---|---|---|
| 1 | 매칭 *.md | Product SSOT/zone.md | - | 실질 본문 | O |
| 2 | 매칭 *.md | Product SSOT/todo.md | - | 본문 없는 문서 | X |
| 3 | 자식 URL | https://wiki.example/policy/zone | Product SSOT/todo.md:3 | 200 (via WebFetch) | O |
| 4 | 자식 URL | https://docs.google.com/.../edit?gid=... | Product SSOT/zone.md:88 | 인증 필요 (Google Drive connector 미인증) | X |
```

실패 행도 list에 포함한다. 실패 0건이면 표 아래 `모든 기준 문서 외부 링크 처리 성공` 한 줄을 둘 수 있다.
