# planning-kit PRD 0.2.9

> 0.2.8 기반 incremental PRD. `planning-format`과 `planning-review`의 화면 출력이 너무 실행 로그·원시 trace 중심으로 길어지는 문제를 줄이고, 사용자가 바로 복사·검토·판단할 수 있는 산출물/리뷰 보고서 중심 출력으로 정리한다. 본 PRD 외 기존 `planning-format` / `planning-review` / `ssot-audit` 명세는 [`prd-0.2.8.md`](./prd-0.2.8.md) 이하 chain 그대로 유지하되, 출력 구조·저장 경로·SSOT corpus 경계·호환성에서 충돌이 있으면 본 0.2.9 명세가 우선한다.
>
> 핵심 변경: 최종 응답은 진행 로그가 아니라 산출물이어야 한다. `planning-format`은 사람이 읽기 좋은 일반 Markdown 형태의 `정책서`와 `기능설계서`를 먼저 보여준다. `planning-review`는 `판정`, `검증 신뢰도`, `최우선 수정 항목`, `작업 백로그`를 먼저 보여준다. 추적 정보는 새 옵션 없이 결과 하단의 상세 섹션으로 분리한다. `planning-format --save` 저장 위치는 `planning/`으로 고정하고, `planning/**`은 SSOT corpus에서 항상 제외한다. SSOT corpus는 폴더명에 독립 `SSOT` 토큰이 있는 하위 폴더 안의 Markdown만 대상으로 한다.

## 1. 변경 요약

1. **공통 실행 로그 제거** — 최종 출력 앞에 "이제 URL fetch...", "본문 취득 성공", "Both Confluence pages fetched" 같은 진행 문장을 쓰지 않는다. fetch 경로와 실패 사유는 요약/trace 영역에만 기록한다.
2. **planning-format 결정 문서 우선 출력** — 기본 출력은 헤더 요약 다음 바로 일반 Markdown으로 렌더링되는 `정책서`와 `기능설계서`를 보여준다. 출처·입력 제외·검증 상세는 문서 본문 뒤에 둔다.
3. **planning-review 보고서 우선 출력** — 기본 출력은 `판정`, `검증 신뢰도`, `결론`, `최우선 수정 항목`, `작업 백로그`를 축별 원시 발견 목록보다 먼저 보여준다.
4. **추적 정보 하단 분리** — 출처, 입력 제외, 자체 검증 상세 로그, SSOT 출처, 축별 원시 발견은 상단 산출물 뒤의 상세 섹션으로 내린다. 사용자 결정용 `검증 피드백`은 산출물 뒤 기본 섹션에 둔다.
5. **저장 산출물 경계 고정** — `planning-format --save`는 산출물을 `planning/` 아래에만 저장한다. 저장된 초안은 review 대상일 수 있지만 SSOT 근거가 될 수 없다.
6. **SSOT 폴더 경계 고정** — `planning-review`와 `ssot-audit`의 SSOT corpus는 폴더명에 독립 `SSOT` 토큰이 있는 하위 폴더 안의 Markdown으로 제한한다.
7. **planning-format 자체 검증 피드백 우선** — cross-bleed, 용어 일관성, 의미 구조가 불명확한 markdown syntax처럼 고칠 수 있는 발견도 최종 본문에 조용히 반영하지 않는다. 먼저 사용자에게 피드백과 수정 제안을 보여준다.
8. **planning-review 우선순위/작업화** — R1/R2/R3 발견은 P0/P1/P2로 재정렬하고, 수정 작업 단위의 backlog로 묶는다.
9. **본문 자동 수정 전 피드백 우선** — 검증에서 발견한 의미 변경 항목은 `검증 피드백`에 먼저 노출한다. 사용자가 명시적으로 반영을 요청하기 전까지 정책서·기능설계서 canonical 본문을 자동 수정하지 않는다.
10. **readable 본문 우선** — 기본 화면에서는 정책서·기능설계서를 코드 펜스로 감싸지 않고 일반 Markdown으로 보여준다. 같은 본문을 코드 펜스 블록으로 중복 출력하지 않는다.
11. **용어 표기 레이어 분리** — 기능설계서의 UI label은 한국어 표기를 우선하고, 시스템 용어는 괄호 병기한다. 정책서는 시스템 용어를 우선하되 화면 컴포넌트명은 핵심 규칙 자리에 쓰지 않는다.
12. **출력 아티팩트 레이어 분리** — 내부 canonical 본문, 화면 렌더링, 저장 파일, 상세 추적, 검증 피드백을 서로 다른 산출물 레이어로 다룬다.
13. **호환성·마이그레이션 명시** — 0.2.8 이하 코드펜스 출력과 `.planning-kit/**` 저장 산출물은 review 입력으로 계속 읽되, 신규 저장과 SSOT 근거로는 사용하지 않는다.

## 2. 동기

0.2.8까지의 `planning-format`과 `planning-review`는 추적성과 결정성을 강화하는 방향으로 발전했다. URL fetch, connector fallback, 입력 제외 추적, 자체 검증, SSOT corpus trace는 품질에는 필요하지만 실제 사용 출력에서는 다음 문제가 생긴다.

- 최종 응답 상단에 진행 로그가 먼저 노출되어 산출물의 시작점이 흐려진다.
- `MCP`, `WebFetch`, `connector fallback` 같은 도구 내부 표현이 사용자 문서 검토 흐름을 방해한다.
- `## 출처`와 `## 입력 제외 항목`이 너무 길어져 정작 정책서·기능설계서보다 로그가 더 눈에 띈다.
- 자체 검증이 고칠 수 있는 문제를 조용히 고쳐버리면 사용자는 원본에서 어떤 문제가 있었는지, 어떤 기준으로 바뀌었는지 판단할 기회를 잃는다.
- 코드 펜스가 깨지면 정책서·기능설계서 복사가 어려워지고, downstream parser도 문서 경계를 안정적으로 찾기 어렵다.
- 반대로 기본 화면에서 정책서·기능설계서를 통째로 코드 펜스에 넣으면 Markdown이 렌더링되지 않아 사람이 읽기 어렵다.
- 코드 펜스를 제거해도 5열 이상 표나 긴 문장이 들어간 표는 좁은 채팅 화면에서 가로로 무너져 읽기 어렵다.
- `--save`로 만든 초안 폴더가 SSOT corpus에 섞이면, 생성 산출물이 자기 자신 또는 이전 초안을 근거로 삼는 순환 검증이 생긴다.
- SSOT가 프로젝트 전체 Markdown 어디에나 있을 수 있으면 `planning-review`가 README, PRD, 예시, 과거 초안까지 근거로 끌어올 수 있다. SSOT는 폴더명에서 명시적으로 구분되어야 한다.
- `planning-review`의 `SSOT 충돌: 0건`이 SSOT 품질 문제와 함께 나오면 "정말 통과인지, 비교할 본문이 없어서 0건인지"가 모호하다.
- 발견 10건이 축별 순서로 길게 나열되면, 당장 고쳐야 할 2~3개와 후속 관리 항목이 섞인다.

예를 들어 Zone 관리 출력에서 다음 두 발견은 생성기가 수정 제안을 만들 수 있는 유형이다. 하지만 본문에는 자동 반영하지 않고, 사용자 피드백으로 먼저 올린다.

| 발견 | 피드백/수정 제안 방향 |
|---|---|
| 정책서 §6에 UI 용어 `배너`가 핵심 처리 기준으로 들어감 | 정책서에서는 `상태 유지 및 운영자 알림 조건 해소 대기`로 바꾸는 방안을 제안. 배너 표현은 기능설계서 §7에만 두도록 피드백 |
| `Zone Type`, `Zone Code`, `존 이름` 표기가 한 표 안에서 혼용됨 | 기능설계서 UI label을 `존 유형 (Zone Type)`, `존 코드 (Zone Code)`, `존 이름 (Zone Name)`처럼 통일하라고 제안 |

예를 들어 Zone 관리 review에서 SSOT 기준 문서 묶음 6개가 모두 placeholder라면 먼저 보여야 하는 정보는 "R1 충돌 0건"이 아니라 `검증 신뢰도: 낮음 — R1은 비교 대상 본문이 없어 충돌을 판단하지 못함`이다.

이 PRD는 산출물의 정보량을 줄이는 것이 아니라, 기본 출력에서 사용자가 먼저 봐야 할 정보와 디버그/추적 정보를 분리하는 변경이다.

## 3. 비목표

- URL fetch, BFS 순서, connector fallback, image multimodal 처리 규칙은 변경하지 않는다.
- 입력 제외 항목의 11 카테고리와 full 5필드 형식은 폐기하지 않는다.
- `--save` 저장 파일 개수는 변경하지 않는다. 저장 루트만 `planning/`으로 고정한다.
- 기본 출력에서 같은 정책서·기능설계서 본문을 읽기용과 원문 블록으로 항상 중복 출력하지 않는다.
- `planning-review`의 R1/R2/R3 검증 기준 자체는 변경하지 않는다.
- SSOT 충돌, 원문 정의 부재, 정책 의사결정이 필요한 발견을 자동으로 고치지 않는다.
- 화면 렌더링 안정화를 위해 fence escape, 중복 wrapper 제거, 표 표시 변환 같은 비의미적 보정을 할 수는 있지만, 정책 값·상태·권한·임계값·문구 의미를 자동 변경하지 않는다.
- 토큰 절약을 위해 fetch cap, source cap, page cap을 도입하지 않는다.
- 기존 0.2.8 이하 산출물을 자동 마이그레이션하지 않는다.
- SSOT corpus placeholder를 자동 생성/보강하지 않는다.

## 4. 기본 출력 구조

0.2.9부터 `planning-format` 기본 출력은 다음 순서를 따른다. 정책서·기능설계서 본문은 화면에서 바로 읽히도록 일반 Markdown으로 출력하며, 코드 펜스로 감싸지 않는다.

````markdown
# [기능명]

- 입력: [사람이 읽는 요약]
- 산출물: 정책서, 기능설계서
- 검증: 피드백 N건, 사용자 확인 필요 M건[, 최우선 확인: 요약 1건]
- 저장: 없음 (--save 미사용) / [저장 경로]

---

## 정책서

[정책서 본문 — 일반 Markdown]

---

## 기능설계서

[기능설계서 본문 — 일반 Markdown]

---

## 검증 피드백

[검증 피드백 / 사용자 확인 필요 요약]

## 출처 요약

[source type별 요약 + 실패/본문 미사용 행]

## 입력 제외 요약

[카테고리별 카운트 + high-signal 항목]

## 상세 추적

[조건 충족 시에만 출력. full 출처표 / 입력 제외 5필드 list / SSOT 출처 / 원시 발견 목록]
````

규칙:

- 최종 출력은 반드시 `# [기능명]`으로 시작한다.
- 최종 출력 앞에 fetch 진행 문장, 도구 fallback 설명, "변환을 시작합니다" 같은 로그 문장을 쓰지 않는다.
- `정책서`와 `기능설계서`는 상세 출처/검증보다 먼저 나온다. 단, 사용자 확인 필요 항목이 있으면 상단 `검증:` 줄에 최우선 확인 항목 1건을 짧게 표시한다.
- 기본 화면의 `정책서`와 `기능설계서`는 Markdown heading, table, list가 렌더링되는 일반 본문이어야 한다.
- 기본 화면에서는 정책서·기능설계서 전체를 ` ```markdown ` 코드 펜스로 감싸지 않는다.
- 화면 출력에서는 넓은 표를 그대로 유지하지 않는다. 5열 이상 표, 셀 문장이 긴 표, 모바일 폭에서 읽기 어려운 표는 항목별 카드/필드 목록으로 분해한다.
- `저장: 화면 only` 표현은 쓰지 않는다. `저장: 없음 (--save 미사용)`으로 바꾼다.
- `--save` 성공 시 저장 경로는 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 형식으로 표시한다.
- `## 상세 추적`은 조건 충족 시 `## 입력 제외 요약` 뒤에 둔다.

### 4.1 출력 아티팩트 레이어

0.2.9부터 `planning-format`은 한 번의 응답 안에서도 다음 레이어를 구분한다.

| 레이어 | 목적 | 출력/저장 위치 | 주요 규칙 |
|---|---|---|---|
| canonical 본문 | 정책서·기능설계서의 의미 기준 | 메모리 내부 + `--save` 파일 | 정책 값·상태·권한·임계값·문구 의미를 보존한다. 화면 가독성 변환 때문에 의미 구조를 바꾸지 않는다. |
| 화면 렌더링 | 사용자가 채팅 화면에서 바로 읽고 판단하는 표시 | 기본 응답의 `## 정책서`, `## 기능설계서` | 코드 펜스 wrapper 제거, 넓은 표 분해, 긴 셀 bullet화 같은 표시 변환 가능. 의미 변경 금지. |
| 저장 파일 | 원문 Markdown으로 재사용 가능한 산출물 | `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` | 정책서 1개 + 기능설계서 1개. 화면용 카드/필드 목록 변환을 반드시 그대로 따를 필요는 없다. |
| 검증 피드백 | self-review 발견과 수정 제안 | 기본 응답의 `## 검증 피드백` | 사용자 승인 전 의미 수정 금지. 위치·문제·영향·제안·사용자 확인 여부를 표시한다. |
| 상세 추적 | 출처·입력 제외·SSOT 출처·원시 발견 | 하단 `## 상세 추적` | 기본 상단을 방해하지 않도록 하단에 둔다. 디버깅과 parser 호환이 필요한 경우에 사용한다. |

이 구분은 downstream parser에도 적용된다. 정확한 정책서·기능설계서 원문이 필요하면 `--save` 산출물을 기준으로 삼고, 기본 응답 화면 렌더링은 사람이 읽기 좋은 표시 결과로 취급한다. `--save`를 사용하지 않은 기본 응답은 canonical 원문이 아니라 readable projection이다. parser가 표 구조, 코드 블록, 원문 Markdown을 안정적으로 재사용해야 하면 `--save` 파일을 요구하거나 사용자가 저장된 산출물을 review 입력으로 넘겨야 한다.

`planning-review`가 직전 turn의 unsaved `planning-format` 화면 출력을 입력으로 사용할 수는 있다. 이 경우 review 대상은 readable projection이며, 저장 파일 기반 canonical review보다 신뢰도가 낮을 수 있다. `planning-review`는 `검증 범위와 한계`에 `검토 대상: 직전 화면 출력(readable projection, --save 미사용)`을 표시하고, 표 분해로 원문 구조가 달라질 수 있음을 남긴다.

#### 4.1.1 readable projection 추출 문법

0.2.9 화면 출력은 코드 펜스 wrapper가 없으므로 `planning-review`와 downstream parser는 다음 경계 규칙을 사용한다.

1. 저장 경로가 있으면 화면 projection보다 `--save` 파일을 우선한다.
2. unsaved 화면 출력은 readable projection으로만 취급한다.
3. 정책서 본문은 첫 `## 정책서` wrapper heading 다음 줄에서 시작해 다음 `## 기능설계서` wrapper heading 직전에서 끝난다.
4. 기능설계서 본문은 첫 `## 기능설계서` wrapper heading 다음 줄에서 시작해 `## 검증 피드백`, `## 출처 요약`, `## 입력 제외 요약`, `## 상세 추적` 중 가장 먼저 나오는 wrapper heading 직전에서 끝난다.
5. wrapper heading은 줄 시작에 있는 정확한 heading만 인정한다. 들여쓰기된 heading, blockquote 안 heading, fenced code block 안 heading은 경계로 보지 않는다.
6. 생성된 정책서·기능설계서 본문 안에서는 `## 검증 피드백`, `## 출처 요약`, `## 입력 제외 요약`, `## 상세 추적`을 최상위 wrapper heading으로 쓰지 않는다. 본문에서 같은 의미의 heading이 필요하면 `###` 이하 하위 heading을 사용한다.
7. 경계가 둘 이상으로 해석되거나 한쪽 본문을 확정할 수 없으면 `planning-review`는 임의 병합하지 않고 `검증 범위와 한계` 또는 sanity check에 `readable projection 경계 불명확`을 남긴다.

### 4.2 사용자-facing 용어

기본 상단 출력은 내부 도구 용어보다 한국어 업무 용어를 우선한다.

| 내부/기술 용어 | 기본 화면 권장 표기 |
|---|---|
| `Action Backlog` / `액션 Backlog` | `작업 백로그` |
| `placeholder` | `본문 없는 자리표시자 (placeholder)` |
| `SSOT corpus` | `SSOT 기준 문서 묶음` |
| `fetch` | `본문 가져오기` 또는 `외부 본문 확인` |
| `connector fallback` | 기본 상단 노출 금지. 실패/인증 문제가 있을 때만 출처 요약 비고에 짧게 표시 |

상세 추적 섹션에서는 기존 parser 호환을 위해 `SSOT corpus`, `fetch`, `connector` 같은 기존 기술 용어를 병기할 수 있다.

## 5. 추적 정보 압축

### 5.1 기본 출력

기본 출력은 상세 추적 정보를 모두 펼치지 않고 요약한다.

#### 출처 요약

```markdown
## 출처 요약

- 원본 입력: URL 1개
- 추가 출처: 성공 4개 / 실패 0개
- 본문 미사용 출처: 없음

| 종류 | 건수 | 본문 사용 | 비고 |
|---|---:|---:|---|
| Confluence | 2 | 2 | 원본 1, 자식 1 |
| Google Sheets | 2 | 2 | 같은 파일 range 재사용 포함 |
| Figma | 1 | 1 | FigJam board |
```

도구 경로(`via Atlassian MCP`, `via Google Drive connector`)는 기본 요약 표의 핵심 문구가 아니다. 실패나 인증 문제가 있을 때만 `비고`에 짧게 남긴다.

#### 입력 제외 요약

```markdown
## 입력 제외 요약

- 총 8건: 범위 외 3, 포맷 노이즈 2, 디테일 축약 2, 구조 변환 1
- 본문 반영에 영향 있는 항목: 없음
- 별도 의사결정 필요: 없음
```

기본 출력에서 개별 제외 항목을 모두 펼치지 않는다. 단, 다음 항목은 기본 출력에도 상세 1줄을 남긴다.

| 조건 | 기본 출력 처리 |
|---|---|
| `fetch 실패` | 실패 source와 영향 1줄 표시 |
| `충돌 후보` | 충돌 값과 선택/미선택 상태 표시 |
| `원문 정의 부재` | 연결된 `[TBD]` 위치 표시 |
| `라벨 미매핑` | 문서 본문 반영 누락 가능성이 있으므로 표시 |

### 5.2 상세 추적 정보

새 옵션을 추가하지 않는다. 기존 출력에 포함되던 상세 추적 정보는 상단 산출물 뒤로 이동한다.

규칙:

- `planning-format`의 full `## 출처` 표와 full `## 입력 제외 항목` 5필드 list는 §5.2 조건 충족 시 하단의 `## 상세 추적` 섹션에 둔다.
- `planning-review`의 full `## 입력 출처` 표, full `## SSOT 출처` 표, 축별 원시 발견 목록도 §5.2 조건 충족 시 하단의 `## 상세 추적` 섹션에 둔다.
- 기본 상단에는 사람이 먼저 읽어야 하는 산출물/판정/수정 항목만 둔다.
- 정책서·기능설계서 본문은 화면에서 읽기 좋은 일반 Markdown으로 한 번만 출력한다.
- 같은 본문을 원문 코드 펜스 블록으로 중복 출력하지 않는다.
- 정확한 원문 Markdown 파일이 필요하면 기존 `--save` 동작을 사용한다. 이 PRD는 새 저장/복사 옵션을 만들지 않는다.

`## 상세 추적` 출력 여부는 다음 기준을 따른다.

| 조건 | 처리 |
|---|---|
| fetch 실패, 인증 실패, 본문 미사용 출처가 1건 이상 | 상세 추적에 full 출처 표를 반드시 포함한다. |
| `충돌 후보`, `원문 정의 부재`, `라벨 미매핑`이 1건 이상 | 상세 추적에 해당 입력 제외 5필드 항목을 반드시 포함한다. |
| `planning-review`에서 P0/P1 발견이 1건 이상 | 상세 추적에 축별 원시 발견 목록을 반드시 포함한다. |
| SSOT 기준 문서 묶음이 0건이거나 모두 placeholder | 상세 추적에 SSOT 후보/제외/placeholder 경로 요약을 반드시 포함하고, 기본 상단의 `검증 범위와 한계`에도 원인을 쓴다. |
| `--ssot-include`가 SSOT 폴더 경계 밖만 가리켜 후보가 0건 | 상세 추적에 include glob, 제외 사유, 경계 밖 매칭 수를 반드시 포함한다. |
| 모두 성공이고 제외/발견이 요약으로 충분 | 상세 추적을 생략할 수 있다. |

상세 추적을 출력하더라도 기본 상단보다 먼저 나오면 안 된다. 상세 추적은 사람이 읽는 결론을 보조하는 디버그/호환 영역이다.

## 6. 자체 검증 피드백 우선

여기서 "피드백 우선"은 정책서·기능설계서보다 먼저 전체 피드백 표를 출력한다는 뜻이 아니다. 기본 출력은 산출물 우선 순서를 유지하되, 의미 변경이 필요한 발견을 canonical 본문에 자동 반영하기 전에 사용자에게 먼저 알린다는 뜻이다. 사용자 확인 필요 항목이 있으면 상단 `검증:` 줄에 최우선 확인 항목 1건을 짧게 표시한다.

### 6.1 피드백 루프

0.2.9부터 self-review는 다음 순서로 동작한다.

1. 정책서·기능설계서 초안을 생성한다.
2. 기존 F1~F6 6패스 체크리스트를 실행한다.
3. 발견을 `기계적 안정화`, `화면 전용 표시 변환`, `수정 제안 가능`, `사용자/외부 결정 필요`로 분류한다.
4. `기계적 안정화`는 의미를 바꾸지 않는 범위에서 canonical 본문과 저장 파일에 반영할 수 있다.
5. `화면 전용 표시 변환`은 의미를 바꾸지 않는 범위에서 화면 렌더링에만 반영할 수 있다.
6. `수정 제안 가능`과 `사용자/외부 결정 필요` 발견은 정책서·기능설계서 canonical 본문에 자동 반영하지 않는다.
7. 최종 출력에는 생성된 정책서·기능설계서 본문과 함께 `## 검증 피드백`을 싣는다.
8. `## 검증 피드백`에는 ID, 위치, 문제, 영향, 제안 수정 방향, 사용자 확인 필요 여부를 표시한다.
9. 사용자가 명시적으로 "반영해" 또는 특정 ID 반영을 요청한 뒤에만 다음 응답에서 의미 변경이 포함된 수정 본문을 만든다.

검증 pass는 의미 수정 pass가 아니다. self-review는 사용자에게 먼저 피드백을 제공하는 gate이며, 사용자 승인 전 의미 변경 자동 수정은 금지한다.

### 6.2 수정 제안 가능 항목

기계적 안정화와 화면 전용 표시 변환은 다음 기준으로 구분한다.

| 구분 | 자동 반영 가능 예 | 적용 범위 | 제약 |
|---|---|---|
| 기계적 안정화 | 정책서·기능설계서 전체를 감싼 외부 코드 펜스 wrapper 제거 | canonical + 저장 파일 + 화면 렌더링 | 본문 안 코드 예시 의미는 보존 |
| 기계적 안정화 | 표 구분선 누락처럼 header/cell 개수가 명확한 Markdown syntax 보정 | canonical + 저장 파일 + 화면 렌더링 | 값·컬럼명·행 순서 변경 금지 |
| 기계적 안정화 | 보조 표 heading의 escape/문자열 정규화처럼 의미가 바뀌지 않는 Markdown 표시 보정 | canonical + 저장 파일 + 화면 렌더링 | 위치와 보정 사실을 검증 피드백 또는 상세 추적에 남김 |
| 화면 전용 표시 변환 | 내부 코드 블록 때문에 최종 응답 fence 짝이 깨질 위험이 있음 | 화면 렌더링만 | 저장 파일의 코드 블록은 원문 구조 유지 |
| 화면 전용 표시 변환 | 5열 이상 표를 항목별 필드 목록으로 표시 | 화면 렌더링만 | 행·셀 의미를 삭제하거나 합치지 않음 |

다음은 사용자 승인 전 canonical 본문에 반영하지 않고 제안으로만 보여준다.

| 카테고리 | 수정 제안 가능 예 | 제안 기준 |
|---|---|---|
| F2 cross-bleed | 정책서 핵심 규칙 자리에 `버튼`, `클릭`, `배너`가 들어감 | 정책 문장으로 바꾸고 UI 표현은 기능설계서에만 남기도록 제안 |
| F3 용어 일관성 | 같은 표 안 `Zone Code`와 `존 이름` 혼용 | 문서 레이어별 표기 원칙에 맞춰 통일하도록 제안 |
| F6 syntax | 보조 표 legacy backlink 잔존, 의미 구조가 불명확한 표 컬럼 깨짐, 코드 블록 경계가 불명확한 fence 깨짐 | markdown 구조 수정안을 제안 |
| F4 정책-기능 매핑 | 정책서 규칙이 기능설계서 예외 메시지에 이미 존재하지만 위치 표시가 틀림 | 위치/참조 정리안을 제안 |

### 6.3 자동 수정 금지 항목

| 카테고리 | 금지 사유 |
|---|---|
| 의미 변경이 필요한 검증 발견 | 사용자 피드백이 우선이며, 사용자 승인 전 canonical 본문 자동 수정 금지 |
| `원문 정의 부재`로 생긴 `[TBD]` | 원문에 없는 결정을 생성하면 안 됨 |
| `충돌 후보` | 어느 값이 맞는지 외부 결정 필요 |
| `fetch 실패` | 본문이 없으므로 추론 보정 금지 |
| SSOT 충돌 | `planning-format` 범위가 아니라 `planning-review` 범위 |
| 정책 의사결정 | 사용자/기획/운영 책임자의 결정 필요 |

금지 대상은 canonical 본문의 의미 변경이다. 기계적 안정화와 화면 전용 표시 변환은 허용되지만, 보정 사실이 검증 피드백 또는 상세 추적에 남아야 한다.

### 6.4 검증 피드백 형식

```markdown
## 검증 피드백

- 피드백: 2건
- 사용자 확인 필요: 2건

| ID | 구분 | 위치 | 문제 | 제안 | 사용자 확인 |
|---|---|---|---|---|---|
| F2-1 | cross-bleed | 정책서 §6 | `배너 유지`가 정책서 핵심 처리 기준에 있음 | 정책 표현으로 바꾸고 배너는 기능설계서에만 둠 | 필요 |
| F3-1 | 용어 일관성 | 기능설계서 §4.3 | UI label과 시스템 용어 혼용 | `존 유형 (Zone Type)` 형식으로 통일 | 필요 |
```

피드백 ID는 `F2-1`, `F3-1`, `F4-1`, `F6-1`처럼 self-review 카테고리와 순번으로 만든다. 같은 출력 안에서만 stable하면 된다. 사용자가 "F3-1 반영"처럼 특정 ID를 지정하면 다음 응답은 해당 피드백과 직전 canonical snapshot을 기준으로 수정 본문을 만든다.

직전 canonical snapshot은 바로 앞 `planning-format` 출력에서 생성한 정책서·기능설계서 의미 본문을 뜻한다. 중간에 다른 `planning-format` 출력이 끼었거나, 세션이 바뀌었거나, 직전 snapshot을 확정할 수 없으면 ID만으로 반영하지 않는다. 이때는 저장 경로, 정책서·기능설계서 본문, 또는 다시 생성한 최신 출력을 받아 기준 snapshot을 명시해야 한다.

self-review를 실행했고 피드백이 0건이면 `## 검증 피드백` 섹션은 유지하고 다음처럼 표시한다.

```markdown
## 검증 피드백

없음
```

피드백이 있으면 본문 아래에 반드시 노출한다. 피드백을 이유로 의미 변경을 canonical 본문에 자동 반영하지 않는다.

### 6.5 `--no-self-review` 처리

`--no-self-review`가 지정되면 F1~F6 self-review를 실행하지 않는다.

규칙:

- 상단 검증 줄은 `- 검증: 생략 (--no-self-review)`로 표시한다.
- `## 검증 피드백` 섹션은 생략한다.
- 코드 펜스 wrapper 제거, 넓은 표 화면용 분해처럼 0.2.9 기본 화면 렌더링 규칙은 계속 적용한다.
- self-review를 생략해도 fetch 실패, 입력 제외 요약, 저장 경로, 상세 추적 배치 규칙은 유지한다.

## 7. 용어 표기 레이어

`planning-format`은 정책서와 기능설계서에서 같은 개념을 다른 레이어로 표현할 수 있다. 하지만 한 레이어 안에서는 흔들리면 안 된다.

| 레이어 | 표기 원칙 | 예 |
|---|---|---|
| 정책서 | 시스템/도메인 용어 우선 | `Zone Type`, `Zone Code`, `Closing Planned` |
| 기능설계서 UI label | 사용자 화면 표기 우선 + 시스템 용어 괄호 병기 | `존 유형 (Zone Type)`, `존 코드 (Zone Code)` |
| 기능설계서 동작/검증 | UI label과 상태값을 연결 | `상태 드롭다운 값: 활성 / 폐쇄 예정 / 비활성` |
| 용어 정의 | 영문 시스템명과 한국어 UI label 관계 명시 | `Zone Name: 화면 표기는 존 이름` |

이 규칙은 F3 용어 일관성 검사에 반영한다. "영문과 한국어가 함께 등장했다" 자체가 문제가 아니라, 같은 레이어 안에서 표기 기준이 흔들리는 것이 문제다.

## 8. readable output 우선

정책서·기능설계서 본문은 기본 화면에서 코드 펜스가 아니라 일반 Markdown으로 렌더링되어야 한다.

### 8.1 화면용 표 표시 기준

기본 화면 출력은 "문서 원문 보존"보다 "사람이 읽을 수 있는 표시"를 우선한다.

| 조건 | 화면 출력 방식 |
|---|---|
| 2~4열이고 셀이 짧은 표 | Markdown 표 유지 |
| 5열 이상 표 | 행 단위 카드/필드 목록으로 변환 |
| 셀 안 문장이 긴 표 | 주요 필드는 bullet로 분리 |
| 상태·권한·예외처럼 항목별 설명이 긴 표 | `### 항목명` 하위에 `처리 등급`, `메시지`, `운영 조치`처럼 필드 목록으로 표시 |
| 저장 파일 | 기존 템플릿/원문 Markdown 구조 유지 가능 |

판정 기준:

- `긴 셀`: 한 셀이 60자를 넘거나, 쉼표/문장부호 기준으로 2개 이상의 독립 조건을 포함하거나, 줄바꿈/list를 포함하는 경우.
- `모바일 폭에서 읽기 어려운 표`: 열이 5개 이상이거나, 4열 이하라도 셀 평균 길이가 40자를 넘는 경우.
- `planning-review`의 `최우선 수정 항목`, `작업 백로그` 표는 5열까지, `출처 요약` 표는 6열까지 허용한다. 단, 셀이 길어져 읽기 어려우면 동일한 필드명을 가진 카드/필드 목록으로 분해할 수 있다. 이때 `최우선 수정 항목`과 `작업 백로그` 섹션 존재 요구는 유지하되, 물리적 Markdown 표만을 필수로 보지 않는다.
- 화면용 분해는 행·필드 의미를 보존해야 하며, 저장 파일의 canonical 표 구조를 바꾸는 근거가 아니다.
- 표를 카드/필드 목록으로 분해할 때는 원문 행 순서, 열 이름, 셀 값, escaped pipe, 셀 내부 list/code span을 모두 보존한다. 한 셀의 값을 여러 bullet로 나눌 수는 있지만 삭제·합성·재해석은 금지한다.

예를 들어 다음 원문 표를 화면에 그대로 노출하지 않는다.

```markdown
| 상황 | 처리 등급 | 사용자 메시지 / 결과 | 운영 조치 |
|---|---|---|---|
| Closing Planned 상세 진입 | 경고 | 폐쇄 예정 Zone 입니다... | 조건 충족 시 자동 제거 |
```

화면에서는 다음처럼 풀어 쓴다.

```markdown
### Closing Planned 상세 진입

- 처리 등급: 경고
- 사용자 메시지: 폐쇄 예정 Zone이며 잔존 재고와 미완료 작업 수를 표시
- 운영 조치: 조건 충족 시 안내 제거
```

이 방식은 화면 출력의 가독성을 위한 표시 변환이다. 정확한 원문 Markdown 파일이 필요하면 기존 `--save` 산출물을 사용한다.

허용:

```markdown
## 정책서

# 정책서 본문

| 항목 | 정책 |
|---|---|
| 예시 | 일반 표로 렌더링 |

## 기능설계서

# 기능설계서 본문
```

금지:

````markdown
## 정책서

```markdown
...
```
````

같은 본문을 다음처럼 원문 블록으로 다시 중복 출력하지 않는다.

````markdown
## 원문 Markdown

```markdown
[정책서 전체 본문 중복]
```
````

본문 안에 원문 코드 블록을 보존해야 하면 내부 triple backtick을 네 칸 들여쓰기 또는 inline code로 변환한다. 최종 출력에서 fence 짝이 깨진 상태로 사용자에게 반환하지 않는다.

## 9. Zone 관리 출력 개선 예시

0.2.9 기본 출력은 다음처럼 시작해야 한다.

````markdown
# Zone 관리

- 입력: Confluence URL 1개, 추가 출처 4개
- 산출물: 정책서, 기능설계서
- 검증: 피드백 2건, 사용자 확인 필요 2건
- 저장: 없음 (--save 미사용)

---

## 정책서

> [!IMPORTANT]
> - 도메인: Tenant Domain WMS

## 1. 목적

| 항목 | 내용 |
|---|---|
| 관리 대상 | Zone |

---

## 기능설계서

> [!IMPORTANT]
> - 적용 사용자: Authority Layer

## 1. 개요

| 항목 | 내용 |
|---|---|
| 목적 | Zone 조회·등록·수정·상태 전환 |

---

## 검증 피드백

- 피드백: 2건
- 사용자 확인 필요: 2건
````

상단에 다음 문장은 나오면 안 된다.

```text
이제 URL fetch와 템플릿 파일을 함께 로드합니다.
WebFetch는 도구 제한으로 불가 → Atlassian MCP fallback으로 진행합니다.
본문 취득 성공. BFS 자식 링크 추출 및 병렬 fetch를 진행합니다.
```

이 정보가 필요하면 상세 추적 섹션의 상세 출처 로그에서만 확인한다.

## 10. planning-review 기본 출력 구조

0.2.9부터 `planning-review` 기본 출력은 다음 순서를 따른다.

````markdown
# planning-review: [기능명]

- 판정: [통과 / 조건부 통과 / 수정 필요 / 검토 필요 / 비교 불가]
- 검증 신뢰도: [충분 / 제한적 / 낮음] — [이유]
- 입력: [사람이 읽는 요약]
- 점검 축: ssot, ac, deps
- 발견: P0 N건, P1 N건, P2 N건

---

## 결론

[1~3문장 bottom line]

## 최우선 수정 항목

| ID | 우선순위 | 항목 | 이유 | 권장 처리 |
|---|---|---|---|---|

## 작업 백로그

| ID | 유형 | 대상 | 작업 | 완료 조건 |
|---|---|---|---|---|

## 발견 요약

[축별 count + high-signal finding only]

## 검증 범위와 한계

[입력/SSOT 기준 문서 묶음/본문 없는 자리표시자/본문 가져오기 실패/비활성 축 요약]

## 출처 요약

[기본 압축 출처]

## 상세 추적

[조건 충족 시에만 출력. full 입력 출처표 / full SSOT 출처표 / 축별 원시 발견 목록]
````

규칙:

- 최종 출력은 반드시 `# planning-review: [기능명]`으로 시작한다.
- 최종 출력 앞에 fetch 진행 문장, project scan 진행 문장, "분석 결과를 정리합니다" 같은 로그를 쓰지 않는다.
- 전체 리포트를 ` ```markdown ` 또는 ` ```text ` 코드 펜스로 감싸지 않는다.
- `결론`은 발견 상세보다 먼저 온다.
- `최우선 수정 항목`은 P0/P1만 기본 노출한다. P2는 `작업 백로그`나 `발견 요약`에 압축한다.
- full 입력 출처표, full SSOT 출처표, 축별 원시 발견 목록은 하단 `## 상세 추적` 섹션으로 이동한다.
- P0/P1 발견이 없으면 `## 최우선 수정 항목`에는 빈 표를 출력하지 않고 `없음` 한 줄을 쓴다.
- 작업 단위가 없으면 `## 작업 백로그`에는 빈 표를 출력하지 않고 `없음` 한 줄을 쓴다.
- P2만 있는 경우 `## 최우선 수정 항목`은 `없음`, `## 작업 백로그`와 `## 발견 요약`에는 P2 관련 작업/요약을 압축 표시한다.
- `## 상세 추적`은 조건 충족 시 `## 출처 요약` 뒤에 둔다.

## 11. planning-review 판정과 신뢰도

### 11.1 판정 값

| 판정 | 조건 |
|---|---|
| `수정 필요` | P0 또는 P1 발견이 1건 이상 있다. |
| `검토 필요` | P0/P1은 없고, 핵심 축이 판단 가능하며, P2 권고가 있거나 외부 결정이 필요한 항목이 있다. |
| `비교 불가` | 요청한 핵심 축이 증거 부족으로 판단 불가다. 예: `--axes ssot`인데 SSOT 기준 문서 묶음이 모두 placeholder. P2 권고가 함께 있어도 핵심 축이 판단 불가이면 `비교 불가`가 우선한다. |
| `조건부 통과` | P0/P1/P2 발견이 없고, 활성 축은 평가됐지만 검증 신뢰도가 `제한적`이다. 예: 일부 외부 link follow 실패가 있지만 실질 SSOT 본문으로 R1 비교를 수행함. |
| `통과` | P0/P1/P2 발견이 없고, 검증 신뢰도가 `충분`이다. |

판정 우선순위는 `수정 필요` → `비교 불가` → `검토 필요` → `조건부 통과` → `통과`다. 예를 들어 SSOT 기준 문서 묶음이 모두 placeholder라도 R2에서 P0가 발견되면 최종 판정은 `수정 필요`다.

기존 `리뷰 결과: 발견 N건`은 `발견` count로 유지하되, 판정의 보조 정보가 된다.

### 11.2 검증 신뢰도

| 신뢰도 | 조건 |
|---|---|
| `충분` | review 대상 본문이 충분하고, 활성 축에 필요한 비교 대상/증거가 실질 본문을 포함하며, 활성 축을 정상 평가했다. |
| `제한적` | review 대상 본문은 충분하고 활성 축을 평가했지만, 일부 SSOT 파일이 placeholder이거나 특정 외부 link follow가 실패해 증거 범위가 일부 제한된다. |
| `낮음` | 활성 핵심 축을 평가할 비교 대상 대부분이 비어 있거나, 입력 fetch 실패로 review 대상 본문 일부만 확보했다. `ssot` 축이 활성이고 SSOT 기준 문서 묶음이 0건 또는 모두 placeholder이면 `낮음`이다. |

신뢰도 줄은 반드시 이유를 함께 쓴다.

```markdown
- 검증 신뢰도: 낮음 — 매칭 SSOT 기준 문서 6개가 모두 placeholder라 R1은 실질 비교를 수행하지 못함
```

신뢰도는 활성 축 기준으로 판단한다. 예를 들어 `--axes ac`만 활성인 경우 SSOT 기준 문서 묶음 부재는 신뢰도 산정에 영향을 주지 않는다. `낮음`이고 P0/P1/P2 발견이 0건이면 최종 판정은 `비교 불가`다. `낮음`이더라도 P0/P1 발견이 있으면 판정 우선순위에 따라 `수정 필요`다.

### 11.3 placeholder corpus 규칙

매칭 SSOT 파일이 1~2줄 수준이고 본문 heading/표/결정 문장이 없으면 placeholder로 본다.

- R1 count는 `0건`으로 두되, 설명은 `충돌 없음`이 아니라 `비교 대상 본문 없음`으로 쓴다.
- `판정`은 R2/R3의 P0/P1 발견이 있으면 `수정 필요`다. R2/R3가 P2-only이고 활성 핵심 축의 비교 대상이 없는 상태라면 `검토 필요`가 아니라 `비교 불가`다. R2/R3 발견이 없고 R1만 요청됐어도 `비교 불가`다.
- `검증 범위와 한계`에 placeholder 파일 수와 경로 요약을 남긴다.
- placeholder-only 한계는 `SSOT 보강` 작업 백로그에 올릴 수 있지만, verdict용 P2 finding count에는 포함하지 않는다. 즉 placeholder-only 때문에 `검토 필요`가 `비교 불가`보다 앞서면 안 된다.
- placeholder-only 백로그가 있고 verdict용 finding이 0건이면 상단 `발견`은 `P0 0건, P1 0건, P2 0건`으로 두고, `작업 백로그`에는 `A*` 항목을 표시한다. `검증 범위와 한계`에는 `SSOT 보강 작업은 있으나 verdict finding에는 포함하지 않음`을 남긴다.
- 로컬 SSOT Markdown은 placeholder지만 그 안의 외부 link follow 결과가 실질 본문을 제공하면, R1은 외부 본문 기준으로 제한적 비교를 수행한다. 이때 신뢰도는 `제한적`이고, `검증 범위와 한계`에 "로컬 SSOT는 placeholder, 외부 본문으로 비교"를 명시한다.
- placeholder 파일의 외부 link follow 후보는 본문 키워드 매칭뿐 아니라 파일명, H1, link text, URL label도 매칭 신호로 삼는다. 이 신호로도 매칭되지 않은 SSOT 폴더 전체를 무조건 follow하지는 않는다.

placeholder 판정 예:

| 입력 형태 | 판정 |
|---|---|
| 빈 파일 | placeholder |
| frontmatter만 있는 파일 | placeholder |
| H1 하나만 있고 결정 문장이 없는 파일 | placeholder |
| 제목 + "작성 예정" 한 줄 | placeholder |
| 빈 표 또는 헤더만 있는 표 | placeholder |
| 정책 값·상태·권한·임계값 같은 결정 문장이 1개 이상 있는 파일 | 실질 본문 |

## 12. planning-review 우선순위와 작업 백로그

기본 출력은 축 순서가 아니라 우선순위 기준으로 정렬한다.

| 우선순위 | 의미 | 예 |
|---|---|---|
| P0 | 구현/운영 판정을 결정할 수 없어 기능 동작이 비결정적 | 자동 비활성 조건의 `미사용`, `외부 시스템 미참조` 미정의 |
| P1 | 정책/기능 문서 간 범위 충돌 또는 외부 시스템 영향이 큼 | `연동 여부`가 non-MVP 컬럼이면서 수정 항목에는 MVP 토글로 노출 |
| P2 | 후속 SSOT 보강, cross-link, 변경 워크플로 권고 | Putaway·피킹 전략 정책서 작성 후 cross-link 필요 |

축별 기본 매핑:

| 축 | 기본 우선순위 |
|---|---|
| R1 SSOT 충돌 | P0 또는 P1 |
| R2 검증가능성 | P0 또는 P1 |
| R3 발견 | P1 또는 P2 |
| R3 권고 | P2 |

검토기는 영향도에 따라 한 단계 올리거나 내릴 수 있다. 조정 시 발견 요약에 이유를 짧게 남긴다.

`planning-review`는 발견을 그대로 나열하기 전에 수정 작업 단위로 묶은 작업 백로그를 만든다.

| 유형 | 설명 |
|---|---|
| `문서 수정` | 정책서·기능설계서 본문을 직접 고쳐야 함 |
| `정책 결정` | 담당자/도메인 owner가 값을 결정해야 함 |
| `SSOT 보강` | 본문 없는 자리표시자(placeholder) 또는 부재한 기준 문서를 작성/보강해야 함 |
| `외부 인터페이스` | WCS/API/시트 등 외부 의존 계약을 명시해야 함 |
| `동기화 워크플로` | 시트·정책서·기능설계서 동시 갱신 절차가 필요함 |

예:

```markdown
## 작업 백로그

| ID | 유형 | 대상 | 작업 | 완료 조건 |
|---|---|---|---|---|
| A1 | 문서 수정 | 정책서 §6, 기능설계서 §5 | 자동 비활성 조건의 `미사용`과 `외부 시스템 미참조`를 판정 가능한 조건으로 재정의 | 상태 enum 또는 정량 조건과 참조 시스템 목록이 명시됨 |
| A2 | 외부 인터페이스 | 정책서 §9, 기능설계서 §4.4 | `연동 여부` 토글의 WCS 효과와 MVP 적용 시점을 확정 | ON/OFF 효과, 감사 로그, non-MVP 여부가 두 문서에서 일치 |
```

모든 기본 출력 발견은 `R1-1`, `R2-1`, `R3-1` 형식의 stable id를 가진다. 작업 백로그 항목은 `A1`, `A2` 형식을 쓴다. id는 같은 출력 안에서만 stable하면 된다.

## 13. planning-review 발견/범위/출처 요약

기본 출력의 `## 발견 요약`은 full 발견 목록이 아니다.

```markdown
## 발견 요약

- SSOT 충돌: 비교 대상 본문 없음 (매칭 6개 모두 placeholder)
- 검증가능성: 4건 중 P0 2건, P1 2건
- 영향 분석: 6건 중 P1 3건, P2 3건

### P0

1. R2-1 자동 비활성 조건 판정 불가
   - 위치: 정책서 §6 / 기능설계서 §5
   - 핵심: `미사용`, `외부 시스템 미참조`가 관찰 가능한 조건이 아님
   - 연결 액션: A1
```

규칙:

- 기본 출력은 P0/P1 발견만 상세를 펼친다.
- P2는 count와 backlog 연결로 충분하면 상세를 생략한다.
- 축별 원시 발견 형식은 하단 `## 상세 추적` 섹션으로 이동한다.

`## 검증 범위와 한계`는 review 신뢰도에 영향을 주는 제약을 모은다.

```markdown
## 검증 범위와 한계

- 입력 본문: 정책서 1개, 기능설계서 1개 확보
- SSOT corpus: 키워드 매칭 6개
- SSOT 한계: 6개 모두 placeholder라 R1 충돌 비교는 수행 불가
- 외부 link follow: 시도 0건 (매칭 파일에 링크 없음)
- 비활성 축: 없음
```

기본 `## 출처 요약`은 full table 대신 source type별 카운트를 보여준다.

```markdown
## 출처 요약

| 구분 | 건수 | 성공 | 실패 | 본문 사용 | 비고 |
|---|---:|---:|---:|---:|---|
| 입력 URL | 2 | 2 | 0 | 2 | 정책서, 기능설계서 |
| 입력 이미지 | 0 | 0 | 0 | 0 | 없음 |
| SSOT Markdown | 6 | 6 | 0 | 0 | 모두 placeholder |
| SSOT 외부 링크 | 0 | 0 | 0 | 0 | 링크 없음 |
```

connector 세부(`via Atlassian connector`)는 기본 출력에서 숨긴다. 실패나 인증 문제만 `비고`에 짧게 남긴다.

## 14. 상세 정보 배치

0.2.9부터 새 옵션을 추가하지 않고, 기본 결과 안에서 정보의 배치만 바꾼다.

| 스킬 | 상단 기본 출력 | 하단 상세 정보 |
|---|---|---|
| `planning-format` | 일반 Markdown으로 렌더링되는 정책서/기능설계서 + 화면용 표 분해 + 검증/출처/입력 제외 요약 | 조건 충족 시 full `## 출처` 표, full `## 입력 제외 항목` 5필드 list, fetch status 세부 |
| `planning-review` | 판정/결론/최우선 수정/작업 백로그 우선 + 범위/출처 요약 | 조건 충족 시 full `## 입력 출처` 표, full `## SSOT 출처` 표, 축별 원시 발견 목록, 입력 제외 § R3 보조 신호 상세 |

정책서·기능설계서 코드 펜스 블록을 기본 결과에 중복 출력하지 않는다. 정확한 파일 형태가 필요하면 기존 `--save` 계약을 그대로 사용한다.
전체 `planning-review` 결과도 코드 펜스 안에 넣지 않는다. 예외적으로 원시 발견 원문이 markdown 표로 보정 불가능할 때만 하단 `## 상세 추적` 안의 해당 원문 조각을 ` ```text `로 감쌀 수 있다.

## 15. 저장 경로와 SSOT 범위 계약

0.2.9부터 `--save` 산출물과 SSOT corpus의 물리적 위치를 분리한다. 목적은 생성 초안이 SSOT 근거로 재유입되는 순환 검증을 막고, SSOT 문서 위치를 사람이 폴더명만 보고 구분할 수 있게 하는 것이다.

### 15.1 `planning-format --save` 저장 경로

`planning-format --save`는 현재 작업 디렉터리 기준 `planning/` 아래에만 정책서·기능설계서 2개 파일을 저장한다.

```text
planning/[안전기능명]--YYYY-MM-DD-HHMMSS/
  [안전기능명]_정책서.md
  [안전기능명]_기능설계서.md
```

규칙:

- 숨김 폴더인 `.planning-kit/`은 신규 저장 경로로 사용하지 않는다.
- 저장 파일 개수는 기존처럼 정책서 1개 + 기능설계서 1개다.
- `[안전기능명]`은 NFC normalize 후 경로 분리자(`/`, `\`), 컨트롤 문자, 파일명 금지 문자(`:`, `*`, `?`, `"`, `<`, `>`, `|`)를 `-`로 바꾸고, 양끝 공백·마침표를 제거한다.
- `[안전기능명]`이 비면 `untitled`를 사용한다. 80자를 넘으면 Unicode grapheme cluster 경계에서 80자 이하로 자르고, 자른 뒤 양끝 공백·마침표를 다시 제거한다.
- Windows 예약 basename(`CON`, `PRN`, `AUX`, `NUL`, `COM1`~`COM9`, `LPT1`~`LPT9`)은 대소문자 무관으로 금지하고 뒤에 `-file`을 붙인다.
- timestamp는 사용자 locale 기준 현재 시각을 `YYYY-MM-DD-HHMMSS`로 기록한다. 같은 초에 충돌하면 `--2`, `--3` suffix를 폴더명 끝에 붙인다.
- 저장 폴더는 review 대상 입력이 될 수 있다.
- 저장 폴더와 그 하위 파일은 SSOT corpus 근거가 될 수 없다.
- `planning/` 폴더는 생성 산출물·작업 초안·review target의 영역이며, 기준 문서 저장소가 아니다.
- `planning-review`가 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 디렉터리를 입력으로 받으면 `*정책서*.md`와 `*기능설계서*.md` 파일명을 모두 후보로 인식한다. 파일명으로 확정할 수 없으면 H1/H2의 `정책서`/`기능설계서` heading을 fallback으로 사용한다.
- `planning-review`가 위 저장 파일 중 하나만 입력받아도 same-folder companion read로 같은 폴더의 짝 파일을 찾아야 한다.
- `--save` 저장 파일은 화면용 카드/필드 목록이 아니라 canonical Markdown 구조를 우선 보존한다.

### 15.2 SSOT corpus 위치

`planning-review`와 `ssot-audit`가 SSOT corpus로 삼을 수 있는 로컬 Markdown은 폴더명에 독립 `SSOT` 토큰이 있는 하위 폴더 안에 있어야 한다.

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
docs/**/*.md
README.md
planning-kit/docs/prd/**/*.md
planning-kit/skills/ssot-audit/**/*.md
docs/ssot-audit/**/*.md
ProductSSOT/**/*.md
```

규칙:

- `planning/**`은 항상 SSOT corpus에서 제외한다.
- 프로젝트 루트 전체 `*.md`를 기본 SSOT corpus로 삼지 않는다.
- SSOT 폴더명 매칭은 path segment 단위로 판단한다. segment를 공백, 대괄호, 소괄호, 중괄호, underscore로 나눴을 때 `SSOT`와 대소문자 무관으로 같은 token이 있어야 허용 후보다. 단순 substring은 허용하지 않는다.
- 허용 예: `Product Docs SSOT`, `[ssot] policy`, `Confluence Ssot Export`, `Product_SSOT`.
- 제외 예: `ProductSSOT`, `docs/ssot-audit`, `planning-kit/skills/ssot-audit`. 하이픈으로 이어진 `ssot-audit`는 도구명이지 기준 문서 폴더 token이 아니다.
- `planning/**` 제외가 SSOT 폴더명 허용보다 우선한다. 예: `planning/[SSOT]/policy.md`는 SSOT corpus에서 제외한다.
- 숨김 폴더, `.git/`, `node_modules/`, build/cache 폴더, `planning-kit/skills/**`, `planning-kit/docs/prd/**`, plugin metadata 폴더는 기존 제외 관례를 유지한다.
- symlink는 기본적으로 follow하지 않는다. follow가 필요하면 후속 명시 옵션에서 다룬다.
- 폴더명에 독립 `SSOT` token이 없는 문서는 review 대상이나 참고 입력이 될 수는 있지만, R1 SSOT 충돌의 기준 근거가 될 수 없다.
- SSOT token 폴더가 없거나 SSOT token 폴더 안 Markdown이 비어 있으면 `SSOT corpus: 0건` 또는 `비교 대상 본문 없음`으로 표시하고, 프로젝트 전체 Markdown으로 fallback하지 않는다.
- `planning-review`가 `planning/` 안의 저장 초안을 입력으로 받더라도, SSOT 탐색은 `planning/` 밖의 SSOT 폴더에서만 수행한다.

`--ssot-include <glob>`은 SSOT token 폴더명 규칙을 우회하지 않는다. 기본 후보를 SSOT token 폴더명 하위 Markdown으로 만든 뒤, 그 후보 안에서 include glob을 적용해 좁힌다. 명시 glob이 SSOT 폴더 밖만 가리키면 결과는 0건이며, 출력에 `명시 include가 SSOT 폴더 경계 밖이라 제외됨`을 남긴다.

### 15.3 출력 표시

`planning-format --save` 성공 시 상단 저장 줄은 다음처럼 표시한다.

```markdown
- 저장: planning/Zone-관리--2026-05-11-143000/
```

`planning-review`의 범위 요약은 SSOT 위치 경계를 명시한다.

```markdown
## 검증 범위와 한계

- 검토 대상: planning/Zone-관리--2026-05-11-143000/
- SSOT corpus: 폴더명에 독립 `SSOT` token이 있는 하위 폴더의 Markdown만 사용
- SSOT 제외: planning/** (생성 초안 영역)
```

### 15.4 `ssot-audit` 출력 계약

0.2.9에서 `ssot-audit`는 기본 corpus를 프로젝트 전체 Markdown이 아니라 SSOT token 폴더 하위 Markdown으로 제한한다. 이 변경은 "선언된 SSOT 영역의 구조/내용 품질 감사"를 기본 책임으로 삼기 위한 것이다. SSOT 후보 발굴 또는 프로젝트 전체 Markdown inventory 감사는 0.2.9 범위가 아니며, 필요하면 후속 명시 옵션에서 다룬다.

기본 출력은 다음 순서를 따른다.

````markdown
# ssot-audit

- 감사 범위: SSOT token 폴더 Markdown N개
- 제외: planning/**, .planning-kit/**, 내부 plugin/skill 문서, SSOT token 밖 Markdown M개
- 분석 축: structure, content
- 외부 링크: 활성 / --no-follow-links
- 이미지: 활성 / --no-image
- placeholder: N개

---

## 결론

[1~3문장 bottom line]

## SSOT 인벤토리

| 구분 | 건수 | 대표 경로 | 비고 |
|---|---:|---|---|
| 실질 본문 | N | Product SSOT/policy.md | 결정 문장 있음 |
| 본문 없는 자리표시자 | M | Product SSOT/todo.md | 비교/감사 한계 |

## 제외 요약

| 사유 | 건수 | 대표 경로 |
|---|---:|---|
| SSOT token 폴더 밖 | N | docs/example.md |
| 생성 초안 영역 | N | planning/example/정책서.md |
| 내부 plugin/skill 문서 | N | planning-kit/skills/ssot-audit/SKILL.md |

## 발견 및 권고

[구조 품질 / 내용 품질 발견·권고 요약]

## 개선 백로그

| ID | 유형 | 대상 | 작업 | 완료 조건 |
|---|---|---|---|---|

## 상세 추적

[조건 충족 시 full corpus 후보표 / 제외표 / 외부 출처표]
````

규칙:

- 최종 출력은 반드시 `# ssot-audit`로 시작하고, 그 앞에 project scan 진행 로그를 쓰지 않는다.
- 점수, 등급, health score는 만들지 않는다.
- SSOT token 폴더가 없으면 프로젝트 전체 Markdown으로 fallback하지 않는다. `## 결론`에는 `감사 불가 — 선언된 SSOT token 폴더 없음`을 쓰고, `## 개선 백로그`에 SSOT 폴더 생성/이동 작업을 제안한다.
- `planning/**`, `.planning-kit/**`, `planning-kit/skills/**`, `planning-kit/docs/prd/**`는 감사 corpus가 아니라 제외 요약 대상이다.
- full 후보표/제외표/외부 출처표는 §5.2 조건에 따라 하단 `## 상세 추적`에 둔다.

## 16. Zone 관리 review 출력 개선 예시

0.2.9 `planning-review` 기본 출력은 다음처럼 시작해야 한다.

````markdown
# planning-review: Zone 관리

- 판정: 수정 필요
- 검증 신뢰도: 낮음 — 매칭 SSOT 기준 문서 6개가 모두 placeholder라 R1은 실질 비교를 수행하지 못함
- 입력: Confluence 정책서 1개, 기능설계서 1개
- 점검 축: ssot, ac, deps
- 발견: P0 2건, P1 3건, P2 5건

---

## 결론

Zone 관리 문서는 SSOT 충돌은 확인되지 않았지만, 이는 충돌이 없어서가 아니라 비교할 SSOT 본문이 없기 때문이다. 실제 수정 우선순위는 자동 비활성 조건의 비결정성과 WCS 연동 플래그의 범위 충돌이다.

## 최우선 수정 항목

| ID | 우선순위 | 항목 | 이유 | 권장 처리 |
|---|---|---|---|---|
| R2-1 | P0 | 자동 비활성 조건 판정 불가 | `미사용`, `외부 시스템 미참조`가 관찰 가능한 조건이 아님 | 상태 enum/정량 조건/참조 시스템 목록 명시 |
| R2-4 | P1 | `연동 여부` 토글 의미 불명확 | non-MVP 컬럼과 수정 가능 토글이 충돌 | WCS 연동 플래그의 MVP 적용 시점과 ON/OFF 효과 정의 |
````

상단에 다음 문장은 나오면 안 된다.

```text
Both Confluence pages fetched.
Now I need to scan the project folder for the SSOT corpus.
SSOT corpus 후보 파일들이 모두 빈 placeholder...
```

이 정보는 `## 검증 범위와 한계` 또는 하단 `## 상세 추적` 섹션에만 둔다.

## 17. 호환성

| 영역 | 0.2.8 → 0.2.9 |
|---|---|
| `planning-format` 기본 화면 출력 | trace-heavy + 코드펜스 원문 출력에서 readable deliverable-first 출력으로 변경. 넓은 표는 화면용 카드/필드 목록으로 분해. 자체 검증 발견은 자동 수정하지 않고 피드백으로 먼저 노출 |
| `planning-format --save` | 저장 파일은 정책서·기능설계서 2개로 유지. 저장 경로는 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/`로 고정 |
| SSOT corpus 위치 | 프로젝트 전체 Markdown 기본 탐색에서 독립 `SSOT` token 폴더명 하위 Markdown 탐색으로 변경. `planning/**`은 항상 제외 |
| `planning-review` 기본 화면 출력 | 축별 원시 발견 목록에서 report-first 출력으로 변경 |
| 상세 추적 정보 | 새 옵션 없이 결과 하단으로 이동 |
| R1/R2/R3 검증 기준 | 변경 없음 |
| downstream parser | 기본 출력 상단에서 상세 추적 정보를 기대하면 하단 `## 상세 추적` 섹션을 읽어야 함. 정확한 정책서·기능설계서 원문은 `--save` 산출물을 우선 사용 |
| legacy read | 0.2.8 이하 코드펜스 출력과 `.planning-kit/**` 저장 산출물은 `planning-review` 입력으로 계속 읽을 수 있어야 함 |
| legacy write | 신규 `planning-format --save`는 `.planning-kit/**`에 쓰지 않음 |
| PRD chain | 0.2.9 incremental로 유지할 수 있으나, release note에는 `migration required`를 명시해야 함. 별도 major/minor 기준을 적용하면 0.3.0 후보 |

### 17.1 마이그레이션 안내

릴리스 문서에는 다음을 반드시 포함한다.

- `planning-format --save` 신규 경로: `.planning-kit/<기능명>/`에서 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/`로 변경.
- 0.2.8 이하 `.planning-kit/**` 산출물은 자동 이동하지 않지만, review 입력으로는 계속 허용.
- 신규 `planning/**`과 legacy `.planning-kit/**`은 모두 SSOT corpus 근거가 될 수 없음.
- SSOT 기준 문서를 쓰려면 폴더명에 독립 `SSOT` token이 있는 하위 폴더로 옮기거나 복제해야 함.
- `ssot-audit`는 기본적으로 선언된 SSOT token 폴더 내부 품질을 감사한다. 프로젝트 전체 Markdown에서 SSOT 후보를 발굴하는 동작은 0.2.9 기본 동작이 아님.
- 기본 화면 출력에서 정책서·기능설계서가 코드 펜스 없이 렌더링되므로, parser는 `## 정책서`/`## 기능설계서` heading과 `--save` 파일을 우선 사용해야 함.

## 18. 구현 영향 범위

- `skills/planning-format/SKILL.md` — Step 7 self-review 이후 피드백 우선 출력, 기계적 안정화/화면 전용 표시 변환/의미 변경 금지 경계, Step 9 output 순서 설명 추가.
- `skills/planning-format/references/output-contract.md` — 기본 출력 구조, 출력 아티팩트 레이어, `저장: 없음 (--save 미사용)` 문구, `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 저장 경로, 요약 섹션 형식 추가.
- `skills/planning-format/references/self-review-rules.md` — 발견 분류(`기계적 안정화` / `화면 전용 표시 변환` / `수정 제안 가능` / `사용자/외부 결정 필요`)와 사용자 피드백 우선 규칙 추가.
- `skills/planning-format/references/conversion-rules.md` — 용어 표기 레이어, readable output 우선, 넓은 표 화면용 분해 규칙 반영.
- `skills/planning-format/references/exclusion-rules.md` — 기본 요약 출력과 상세 추적 정보 출력의 관계 설명 추가.
- `skills/planning-review/SKILL.md` — 출력 포맷 섹션을 report-first 구조로 변경.
- `skills/planning-review/references/ssot-rules.md` — `planning/**` 상시 제외, 독립 `SSOT` token 폴더명 기반 corpus 탐색, `--ssot-include` 우선순위, placeholder corpus 판정과 R1 `비교 대상 없음` 설명 규칙 추가.
- `skills/planning-review/references/ac-rules.md` — R2 finding priority 기본값(P0/P1) 안내 추가.
- `skills/planning-review/references/deps-rules.md` — R3 finding/권고 priority 기본값(P1/P2)과 backlog grouping 신호 추가.
- `skills/ssot-audit/SKILL.md` / `references/structure-rules.md` / `references/output-contract.md` — 기본 감사 corpus를 독립 `SSOT` token 폴더명 하위 Markdown으로 제한하고 `planning/**` 제외와 report-first 출력 계약을 명시.
- `planning-kit/README.md` — 결과 형태에 0.2.9 출력 개선/상세 추적 섹션 반영.
- `planning-kit/README.md` 또는 release note — 0.2.8 이하에서 0.2.9로 넘어가는 migration 안내 추가.
- `planning-kit/docs/prd/README.md` — 0.2.9 chain row 추가.
- `planning-kit/.claude-plugin/plugin.json` / `.codex-plugin/plugin.json` — release 구현 시 version 0.2.9.
- `.claude-plugin/marketplace.json` / `.agents/plugins/marketplace.json` — release 구현 시 planning-kit version 갱신.

## 19. 수용 기준

1. 기본 `planning-format` 최종 출력은 `# [기능명]`으로 시작하고, 그 앞에 진행 로그 문장이 없다.
2. 기본 출력의 순서는 헤더 요약 → 정책서 → 기능설계서 → 검증 피드백 → 출처 요약 → 입력 제외 요약 → 상세 추적(조건 충족 시)이다. 단, `--no-self-review`에서는 `검증 피드백` 섹션을 생략한다.
3. 기본 화면의 정책서·기능설계서는 코드 펜스로 감싸지 않고 일반 Markdown으로 렌더링된다.
4. 5열 이상 표나 긴 셀을 가진 표는 화면용 카드/필드 목록으로 분해된다. 단, `planning-review`의 `최우선 수정 항목`/`작업 백로그`는 5열까지, `출처 요약`은 6열까지 허용한다. 긴 셀 때문에 분해할 때도 원문 행 순서, 열 이름, 셀 값은 보존한다.
5. 같은 정책서·기능설계서 본문을 코드 펜스 블록으로 중복 출력하지 않는다.
6. `저장: 화면 only` 표현은 더 이상 사용하지 않고, `저장: 없음 (--save 미사용)` 또는 저장 경로를 출력한다.
7. `planning-format --save` 성공 시 저장 경로는 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/`로 표시된다. 같은 초 collision이 있으면 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS--2/`처럼 suffix가 붙는다. 해당 폴더에는 canonical Markdown 구조의 정책서 1개와 기능설계서 1개만 저장된다.
8. `.planning-kit/`은 신규 저장 경로로 사용하지 않는다.
9. `planning/**`은 `planning-review`와 `ssot-audit`의 SSOT corpus에서 항상 제외된다.
10. SSOT corpus 기본 탐색은 폴더명에 독립 `SSOT` token이 있는 하위 폴더 안의 Markdown만 대상으로 한다.
11. SSOT token 폴더가 없거나 본문이 비어 있으면 프로젝트 전체 Markdown으로 fallback하지 않고 `SSOT corpus: 0건` 또는 `비교 대상 본문 없음`을 명시한다.
12. URL/connector fetch 상세 경로는 기본 출력 상단에 노출하지 않는다.
13. 기존 full `## 출처` 표와 full `## 입력 제외 항목` 5필드 list는 §5.2 조건 충족 시 하단 `## 상세 추적` 섹션에 둔다.
14. 자체 검증에서 발견한 F2/F3/F4/F6 의미 변경 항목은 최종 정책서·기능설계서 canonical 본문에 자동 반영되지 않고 `## 검증 피드백`에 ID와 함께 출력된다.
15. 수정 제안 가능 항목도 사용자 승인 전에는 본문을 바꾸지 않는다.
16. 원문 정의 부재, 충돌 후보, 정책 의사결정 항목은 `[TBD]` 또는 사용자 확인 필요 피드백으로 남긴다.
17. Zone 관리 예시 입력에서 `배너` cross-bleed와 `Zone 이름` 용어 혼용은 본문에 조용히 반영되지 않고, 위치·문제·제안·사용자 확인 필요 여부가 `## 검증 피드백`에 출력된다.
18. 기본 `planning-review` 최종 출력은 `# planning-review: [기능명]`으로 시작하고, 그 앞에 진행 로그 문장이 없다.
19. 기본 `planning-review` 출력 상단에는 `판정`, `검증 신뢰도`, `입력`, `점검 축`, `발견` 줄이 있다.
20. 전체 `planning-review` 리포트는 코드 펜스로 감싸지 않는다.
21. SSOT 매칭 파일이 모두 placeholder이면 신뢰도는 `낮음`이며, R1 0건을 `충돌 없음`으로만 표현하지 않고 `비교 대상 본문 없음`을 명시한다.
22. 기본 `planning-review` 출력에는 `## 결론`이 축별 상세 발견보다 먼저 나온다.
23. 기본 `planning-review` 출력에는 `## 최우선 수정 항목` 섹션과 `## 작업 백로그` 섹션이 있다. P0/P1이 있을 때만 `최우선 수정 항목` 표 또는 동일 필드의 카드/필드 목록을 출력하고, 없으면 `없음`을 표시한다.
24. 모든 기본 `planning-review` 발견은 `R1-*`, `R2-*`, `R3-*` id를 가지고, 작업 백로그 항목은 `A*` id를 가진다.
25. §5.2 상세 추적 조건 충족 시 full 입력 출처표, full SSOT 출처표, connector 세부 status는 기본 `planning-review` 상단에서 숨기고 하단 `## 상세 추적` 섹션에서 확인할 수 있다. SSOT 0건, all-placeholder, SSOT 경계 밖 include도 상세 추적을 출력한다.
26. Zone 관리 review 예시에서 자동 비활성 조건과 WCS 연동 플래그 문제는 P0/P1 최우선 수정 항목으로 올라온다.
27. 화면 렌더링의 넓은 표 분해와 저장 파일의 canonical Markdown 구조는 서로 독립적으로 검증된다.
28. 기계적 안정화는 의미를 바꾸지 않는 범위에서 canonical 본문과 저장 파일에 반영될 수 있고, 화면 전용 표시 변환은 화면 렌더링에만 반영된다. 의미 변경은 사용자 승인 전 canonical 본문에 반영되지 않는다.
29. `--no-self-review` 사용 시 상단 검증 줄은 `검증: 생략 (--no-self-review)`로 표시되고 `## 검증 피드백`은 생략된다.
30. `planning-review`는 0.2.8 이하 코드펜스 출력과 `.planning-kit/**` 저장 산출물을 review 입력으로 계속 읽을 수 있다.
31. `.planning-kit/**`과 `planning/**`은 모두 SSOT corpus 근거가 될 수 없다.
32. SSOT 폴더명 매칭은 path segment 단위의 독립 token 기준이며, 대소문자 무관 substring만으로는 허용하지 않는다. `planning/**` 제외가 항상 우선한다.
33. `--ssot-include`는 SSOT 폴더명 경계를 우회하지 않고, SSOT 후보 안에서만 corpus를 좁힌다.
34. SSOT placeholder 판정은 빈 파일, frontmatter-only, heading-only, 빈 표, "작성 예정" 문서를 포함한다. placeholder-only 한계는 작업 백로그에 올릴 수 있지만 verdict용 P2 finding에는 포함하지 않는다. all-placeholder + P2-only 조합은 핵심 축 비교 불가이면 `비교 불가`가 `검토 필요`보다 우선한다.
35. `planning-review` 판정은 `수정 필요` → `비교 불가` → `검토 필요` → `조건부 통과` → `통과` 우선순위를 따른다.
36. release note 또는 README에는 0.2.8 이하에서 0.2.9로 넘어갈 때 필요한 migration 안내가 포함된다.
37. self-review 실행 결과 피드백이 0건이면 `## 검증 피드백` 섹션은 `없음`을 표시한다.
38. `planning-review`에서 P0/P1이 없으면 `## 최우선 수정 항목`은 빈 표가 아니라 `없음`을 표시하고, 작업 단위가 없으면 `## 작업 백로그`도 `없음`을 표시한다.
39. `--axes ac`처럼 SSOT가 비활성인 호출은 SSOT corpus 부재를 신뢰도 저하 사유로 삼지 않는다.
40. 로컬 SSOT placeholder 안의 외부 link follow가 실질 본문을 제공하면 R1은 외부 본문 기준으로 제한적 비교를 수행하고 신뢰도는 `제한적`으로 표시한다.
41. 0.2.8 이하 PRD chain과 본 PRD가 충돌하면 출력 구조, 저장 경로, SSOT corpus 경계, 호환성에서는 본 0.2.9 규칙이 우선한다.
42. 직전 turn의 unsaved 화면 출력으로 `planning-review`를 실행하면 검토 대상이 readable projection임을 `검증 범위와 한계`에 표시한다.
43. placeholder-only 작업 백로그가 있고 verdict용 finding이 0건이면 상단 발견 count는 0건으로 유지하고, 작업 백로그와 검증 범위에 비대칭 사유를 표시한다.
44. 사용자가 `F*-*` 피드백 ID 반영을 요청했지만 직전 canonical snapshot을 확정할 수 없으면 저장 경로나 최신 본문을 요구하고, 모호한 snapshot에 의미 변경을 적용하지 않는다.
45. `planning-review`는 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 디렉터리와 그 안의 단일 저장 파일 입력에서 `*정책서*.md`/`*기능설계서*.md` 또는 H1/H2 fallback으로 정책서·기능설계서 쌍을 식별한다.
46. readable projection parser는 `## 정책서`, `## 기능설계서`, `## 검증 피드백`, `## 출처 요약`, `## 입력 제외 요약`, `## 상세 추적` wrapper heading 경계를 따른다. 경계가 모호하면 임의 병합하지 않는다.
47. `ssot-audit` 기본 출력은 `# ssot-audit`로 시작하고, 감사 범위, 제외 요약, SSOT 인벤토리, 발견 및 권고, 개선 백로그, 조건부 상세 추적을 report-first 순서로 출력한다.
48. `ssot-audit`는 SSOT token 폴더가 없을 때 프로젝트 전체 Markdown으로 fallback하지 않고, 선언된 SSOT token 폴더 없음과 개선 백로그를 표시한다.
49. `planning-kit/skills/ssot-audit/**`, `docs/ssot-audit/**`, `ProductSSOT/**`처럼 `ssot` substring만 있는 경로는 SSOT corpus가 아니다.
50. release 검증에는 README/release note migration 문구, PRD chain row, plugin version bump 대상 확인이 포함된다.

## 20. 최소 검증 fixture

구현 검증은 최소한 다음 fixture를 포함한다.

| Fixture | 검증 목적 |
|---|---|
| `planning-format` 기본 출력 | 로그 선행 금지, `# [기능명]` 시작, 섹션 순서, 코드 펜스 wrapper 금지, `저장: 없음 (--save 미사용)` 확인 |
| 넓은 표/긴 셀 입력 | 화면 렌더링의 항목별 필드 목록 분해와 저장 파일의 canonical 표 구조 분리 확인 |
| self-review gate | `배너`, `클릭`, `Zone Code`/`존 이름` 혼용이 본문 자동 수정 없이 `F*-*` 피드백으로 노출되는지 확인 |
| `--no-self-review` | 검증 생략 줄, `## 검증 피드백` 생략, 화면 렌더링 규칙 유지 확인 |
| 저장 경로와 파일 | unsafe 기능명, 빈 기능명, 80자 초과, Windows 예약어, truncation 후 trailing dot/space, 같은 초 collision, 정책서 1개 + 기능설계서 1개 저장, `.planning-kit/` 미사용 확인 |
| 저장 산출물 review 입력 | `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 디렉터리 입력과 단일 저장 파일 입력에서 정책서·기능설계서 쌍 식별 확인 |
| SSOT 경계 | `Product SSOT/`, `[ssot]/`, `Product_SSOT/`, `ProductSSOT/`, `docs/ssot-audit/`, `planning-kit/skills/ssot-audit/`, `docs/`, `planning/[SSOT]/`, `.planning-kit/`, symlink 내부/외부/broken 포함·제외 확인 |
| `--ssot-include` | SSOT 후보 내부 narrowing과 SSOT 밖 glob 0건 + 제외 사유 + 상세 추적 표시 확인 |
| placeholder corpus | 빈 파일, frontmatter-only, H1-only, 작성 예정, 빈 표, 실질 결정문 판정 확인 |
| review 판정 | P0/P1/P2 혼합, P2-only, low-confidence 0 finding, `제한적 + finding 0 = 조건부 통과`, `충분 + finding 0 = 통과`, `낮음 + P0 = 수정 필요`, `all-placeholder + P2-only = 비교 불가`, `--axes ac` 호출의 판정/신뢰도 확인 |
| legacy 입력 | 0.2.8 코드펜스 출력과 `.planning-kit/**` 저장 산출물 read 호환 및 SSOT 근거 제외 확인 |
| readable projection parser | 직전 화면 출력 기반 review의 범위 한계 표시, wrapper heading 추출, reserved heading 충돌, 내부 code block heading 무시 확인 |
| placeholder backlog asymmetry | placeholder-only 작업 백로그와 verdict finding count 분리 표시 확인 |
| 상세 추적 trigger matrix | fetch 실패, 인증 실패, 본문 미사용 출처, 충돌 후보, 원문 정의 부재, 라벨 미매핑, SSOT 0건, all-placeholder, SSOT 밖 include 각각의 상단 요약/하단 상세 추적 분리 확인 |
| ssot-audit output contract | `# ssot-audit` 시작, 감사 범위, 제외 요약, SSOT 인벤토리, 발견 및 권고, 개선 백로그, SSOT token 폴더 없음 no-fallback 확인 |
| feedback snapshot ambiguity | `F3-1 반영` 요청 시 직전 canonical snapshot이 없거나 다른 출력이 끼었으면 기준 본문 재지정을 요구하는지 확인 |
| release migration | README/release note migration 문구, PRD README chain row, plugin version bump 대상 확인 |
