# planning-kit PRD 0.2.13

> 0.2.12 기반 incremental PRD. 0.2.12는 `planning-format` 결과 인지성과 `planning-review` 결정 보드 실행 기준을 정리했다. 그러나 검토가 끝난 정책서·기능설계서를 Product Team Space의 SSOT 하위 페이지로 옮기는 마지막 단계는 아직 사람의 수동 작업으로 남아 있다.
>
> 핵심 변경: `planning-publish-confluence` 스킬을 추가한다. 이 스킬은 현재 실행 context memory 안에서 정책서와 기능 설계서 본문을 둘 다 명확히 식별할 수 있을 때만 Confluence 발행을 진행한다. 기본 parent는 Product Team Space의 SSOT 페이지이며, 사용자는 AskUserQuestion 단계에서 다른 parent URL을 직접 입력할 수 있다. 아직 확정 SSOT가 아니므로 Confluence title과 metadata에는 `v0.7` 발행 label을 붙인다.

## 1. 상태

| 항목 | 값 |
|---|---|
| PRD 상태 | 목표 계약. 실제 릴리즈 완료 전까지 runtime 현재 계약으로 간주하지 않는다. |
| 베이스 | 0.2.12 |
| 변경 성격 | incremental, 신규 스킬 추가 |
| 릴리즈 조건 | 13장 롤아웃 계획과 12장 검증 계획 완료 |
| 현재 runtime 주의 | manifest, README, marketplace/cache가 0.2.13으로 동기화되기 전에는 설치 표면이 이전 버전일 수 있다. |

## 2. 변경 계약 요약

1. **신규 스킬 추가** — `planning-publish-confluence`를 추가해 현재 context memory의 정책서·기능 설계서 두 본문을 Confluence SSOT 하위 페이지로 발행한다.
2. **Context memory gate** — 파일 경로, URL, `planning-format --save` 산출물 경로를 스킬 인자로 받아 탐색하지 않는다. 현재 실행 context memory에서 두 본문이 명확히 분리되지 않으면 취소한다.
3. **기본 parent 고정 + 직접 입력 지원** — 기본 parent는 `https://colosseum.atlassian.net/wiki/spaces/PROD/pages/1767604270/SSOT`이며, AskUserQuestion으로 기본값 사용, 직접 입력, 취소를 지원한다.
4. **기능 단위 페이지 구조 + `v0.7` label** — SSOT parent 아래 `[기능명] v0.7` container page를 만들고, 그 아래에 `[기능명] 정책서 v0.7`, `[기능명] 기능 설계서 v0.7` child page를 만든다.
5. **중복 title 안전장치** — target hierarchy 기준으로 container level과 child level을 나눠 `v0.7` title 중복을 확인한다. 자동 덮어쓰기와 page move는 금지한다.
6. **업데이트 preflight** — 기존 page 업데이트는 같은 target 위치의 같은 문서 종류와 같은 `v0.7` label page에만 허용하고, page id, URL, 현재 version, parent, 최종 수정 시각, 교체 범위를 최종 확인에 포함한다.
7. **쓰기 전 최종 확인** — Confluence에 쓰기 전에 생성·수정 대상 title, 발행 label, parent, page hierarchy, page id/version, 문서 종류, content fingerprint를 요약하고 사용자 확인을 받는다.
8. **readback 검증과 부분 실패 계약** — 각 write 후 page를 다시 읽어 version과 fingerprint를 확인한다. Confluence write는 transaction이 아니므로 자동 rollback하지 않고 성공/실패와 재개 기준을 분리해 출력한다.
9. **발행 결과 우선 출력** — 완료 응답은 생성/수정된 페이지 URL과 스킵/실패 사유를 먼저 보여준다.

## 3. 문제와 범위

### 문제

- `planning-format`과 `planning-review` 이후 SSOT 발행이 수동 복사 작업으로 남아 있어, 최신 검토본이 Confluence에 반영되지 않거나 잘못된 parent에 붙을 수 있다.
- SSOT 루트 바로 아래에 정책서와 기능 설계서를 평면적으로 계속 쌓으면 기능 단위 탐색성이 떨어진다.
- 현재 context에 없는 문서를 파일/URL 탐색으로 임의 수집하면 사용자가 발행하려던 본문과 다른 문서가 PROD space에 올라갈 수 있다.
- Confluence write는 외부 시스템 변경이므로 parent 선택, 중복 title 처리, 최종 쓰기 확인이 필요하다.

### 비목표

- `planning-format`이 Confluence에 직접 발행하지 않는다.
- `planning-review`가 검토와 발행을 한 번에 수행하지 않는다.
- 0.2.13에서는 파일 경로, URL, 저장 산출물 경로를 publish 입력으로 받지 않는다.
- 현재 context memory에 없는 정책서·기능 설계서를 로컬 파일, Confluence, Google Drive, Slack, 장기 memory store에서 검색하지 않는다.
- Confluence의 기존 PROD 문서 구조를 자동 재정렬하지 않는다.
- 기존 page parent를 이동하지 않는다. page move는 0.2.13 범위 밖이다.
- SSOT 문서 품질을 다시 감사하지 않는다. 품질 검토는 `planning-review`와 `ssot-audit` 책임이다.
- 확정 SSOT title을 만들지 않는다. 0.2.13 발행 title은 반드시 `v0.7` label을 포함한다.
- 자동 publish 모드, batch publish, 예약 publish를 만들지 않는다.

## 4. 용어

| 용어 | 정의 |
|---|---|
| context memory | 현재 스킬 실행 시점에 모델이 접근 가능한 현재 대화·직전 도구 결과·현재 turn에 로드된 본문. 장기 memory 파일, repo 전체 검색 결과, 새 파일 read 결과가 아니다. |
| 발행 대상 본문 | context memory에서 추출한 정책서 본문 1개와 기능 설계서 본문 1개. |
| SSOT parent | 정책서·기능 설계서를 붙일 Confluence parent page. 기본값은 Product Team Space의 SSOT page. |
| container page | 기능명 단위로 정책서와 기능 설계서 child page를 묶는 Confluence page. |
| child page | container page 아래에 생성되는 `[기능명] 정책서 v0.7`, `[기능명] 기능 설계서 v0.7` page. |
| 발행 label | Confluence title과 metadata에 붙이는 문서 성숙도 label. 0.2.13 기본값은 `v0.7`이며, 확정 SSOT가 아님을 표시한다. |

## 5. 신규 스킬 계약

### 5.1 스킬 이름과 호출

Claude Code:

```text
/planning-kit:planning-publish-confluence
```

Codex:

```text
$planning-publish-confluence
```

위치 인자와 옵션은 0.2.13에서 받지 않는다. parent URL 선택은 실행 중 AskUserQuestion으로만 처리한다.

금지 입력 예:

- `/planning-kit:planning-publish-confluence ./planning/기능--2026-05-12-120000/`
- `/planning-kit:planning-publish-confluence ./정책서.md ./기능설계서.md`
- `/planning-kit:planning-publish-confluence https://colosseum.atlassian.net/wiki/...`
- `/planning-kit:planning-publish-confluence --save`

금지 입력이 있으면 context gate 전에 종료한다. 로컬 파일 read, URL fetch, Confluence parent 조회를 모두 수행하지 않는다.

### 5.2 책임

`planning-publish-confluence`는 다음만 책임진다.

1. 현재 context memory에서 정책서·기능 설계서 두 본문을 식별한다.
2. 사용자가 지정한 Confluence parent 아래 기능 단위 hierarchy를 만든다.
3. parent와 target page의 읽기·쓰기 권한을 확인한다.
4. 중복 title과 기존 page update 가능 여부를 확인한다.
5. 사용자 최종 확인 후 Confluence page를 생성 또는 업데이트한다.
6. 생성/수정 URL과 실패 사유를 report-first로 출력한다.

## 6. Context Memory Gate

### 6.1 통과 조건

다음 조건을 모두 만족해야 한다.

1. context memory 안에 정책서 본문 1개가 있다.
2. context memory 안에 기능 설계서 본문 1개가 있다.
3. 두 본문의 경계가 명확하다.
4. 각 본문이 제목/heading과 최소 2개 이상의 실질 section을 가진다.
5. 기능명을 한 개로 추출할 수 있다.

본문 식별 신호:

- `## 정책서`, `# 정책서`, `[기능명] 정책서`
- `## 기능설계서`, `## 기능 설계서`, `# 기능설계서`, `# 기능 설계서`, `[기능명] 기능 설계서`
- 0.2.12 `planning-format` 화면 출력의 `## 생성 결과 요약`, `## 결정 보드`, `## 검증 피드백`, `## 출처 요약`, `## 입력 제외 요약`, `## 상세 추적`은 발행 본문에서 제외한다.
- `planning-format --save` 저장 파일에서 나온 canonical 본문이 현재 context memory에 이미 로드되어 있다면 사용할 수 있다. 단, 경로를 새로 읽지는 않는다.

### 6.2 금지 입력 처리

호출 인자에 위치 인자나 옵션이 있으면 즉시 취소한다.

금지 입력 판정:

- non-empty positional token 1개 이상
- `--`로 시작하는 option 1개 이상
- `http://` 또는 `https://` URL token
- `planning/`, `.planning-kit/`, `.md`, `.markdown`, `.txt`, 이미지 확장자처럼 경로로 해석될 수 있는 token

금지 입력 응답:

```text
발행 취소 — 0.2.13은 현재 context memory 안의 정책서·기능 설계서만 발행 대상으로 사용합니다.
```

이 분기에서는 다음을 모두 금지한다.

- 로컬 파일 read
- URL fetch
- connector fallback
- Confluence parent 조회
- AskUserQuestion 실행

### 6.3 본문 추출 boundary

0.2.13은 publish 스킬이므로 `planning-review`의 0.2.12 readable projection boundary보다 보수적으로 동작한다.

추출 규칙:

1. 정책서 wrapper heading은 `# 정책서`, `## 정책서`, `# [기능명] 정책서`, `## [기능명] 정책서`만 인정한다.
2. 기능 설계서 wrapper heading은 `# 기능설계서`, `## 기능설계서`, `# 기능 설계서`, `## 기능 설계서`, `# [기능명] 기능 설계서`, `## [기능명] 기능 설계서`만 인정한다.
3. `## 생성 결과 요약`, `## 결정 보드`, `## 검증 피드백`, `## 출처 요약`, `## 입력 제외 요약`, `## 상세 추적`, `## 결론`, `## 최우선 수정 항목`, `## 작업 백로그`는 publish metadata 또는 review report로 보고 발행 본문에서 제외한다.
4. 정책서 본문 종료 경계는 다음 publish/review wrapper heading 중 먼저 등장하는 항목이다: 기능 설계서 wrapper, `## 생성 결과 요약`, `## 결정 보드`, `## 검증 피드백`, `## 출처 요약`, `## 입력 제외 요약`, `## 상세 추적`, `## 결론`, `## 최우선 수정 항목`, `## 작업 백로그`, EOF.
5. 기능 설계서 본문 종료 경계도 같은 규칙을 따른다.
6. code fence 안의 wrapper heading은 0.2.8 이하 legacy display 호환으로만 읽는다. fence 밖에 같은 종류의 wrapper가 다시 있으면 duplicate candidate로 보고 취소한다.
7. blockquote, list child, table cell 안 heading-like text는 wrapper로 보지 않는다.
8. 같은 문서 종류의 publishable candidate가 2개 이상이면 최신/이전 판단을 하지 않고 취소한다.
9. 같은 기능명으로 보이는 정책서·기능 설계서 쌍이 2개 이상 있으면 취소한다.
10. `readable projection boundary ambiguous`에 해당하는 중복·misplaced metadata가 있으면 취소한다. publish 스킬은 ambiguity warning만 남기고 진행하지 않는다.

본문 추출 후 각 child page에는 compact publish metadata block을 붙이고, 원문 본문은 그 아래에 둔다. bulky 화면 전용 section과 상세 trace는 child page 본문에 복제하지 않는다.

### 6.4 취소 조건

다음 중 하나라도 해당하면 Confluence 조회·쓰기 절차를 시작하지 않고 취소한다.

- 정책서 또는 기능 설계서 중 하나만 있다.
- 두 본문이 요약만 있고 실제 본문 section이 부족하다.
- 두 본문의 경계가 불명확하다.
- 같은 문서 종류의 publishable candidate가 2개 이상이다.
- 같은 기능의 후보 revision이 2개 이상이다.
- context memory 안에 여러 기능의 정책서·기능 설계서가 섞여 있고 1쌍으로 좁힐 수 없다.
- 기능명을 한 개로 정할 수 없다.
- 사용자가 parent 선택 또는 최종 확인 단계에서 취소한다.

취소 메시지:

```text
발행 취소 — 현재 context memory에서 정책서·기능 설계서 두 본문을 명확히 식별할 수 없습니다.
```

부족 항목은 최대 5개 bullet로만 표시한다. 파일 경로, URL, 저장 산출물 경로를 달라는 재실행 안내는 0.2.13에서 출력하지 않는다.

## 7. Parent 선택 계약

### 7.1 기본값

기본 parent:

```text
https://colosseum.atlassian.net/wiki/spaces/PROD/pages/1767604270/SSOT
```

표시 이름:

```text
Product Team Space / SSOT
```

### 7.2 AskUserQuestion

context memory gate 통과 후 AskUserQuestion을 실행한다.

질문:

```text
Confluence 발행 위치를 선택하세요.
```

선택지:

| 선택지 | 동작 |
|---|---|
| 기본 SSOT 사용 | 기본 parent URL을 사용한다. |
| 다른 parent URL 입력 | 사용자가 Confluence page URL을 직접 입력한다. |
| 취소 | 스킬을 종료하고 Confluence에 쓰지 않는다. |

parent 검증은 기본 parent와 직접 입력 parent 모두에 적용한다.

- `https://colosseum.atlassian.net/wiki/spaces/`로 시작해야 한다.
- URL에서 page id를 추출할 수 있어야 한다.
- 해당 page를 읽을 수 있어야 한다.
- space key가 `PROD`인지 확인한다. 다른 space면 최종 확인에 space key와 title을 명시하고, 사용자 확인 없이는 진행하지 않는다.
- page title, page id, current version, ancestor path를 조회한다.
- page가 archived/deleted 상태이면 취소한다.
- 선택된 parent 아래 child page를 만들 권한이 있어야 한다.
- 기존 page 업데이트가 예정된 경우 해당 page update 권한이 있어야 한다.

직접 입력이 검증 실패하면 재질문은 1회만 허용한다. 2회 실패하면 취소한다.

AskUserQuestion을 사용할 수 없는 실행 환경에서는 같은 선택지를 일반 사용자 질문 1회로 표시한다. 응답이 없거나 불명확하면 기본값을 추측해 진행하지 않고 취소한다.

## 8. Confluence Page Hierarchy

### 8.1 기본 구조

선택된 parent 아래에 다음 구조를 만든다.

```text
[선택된 parent]
└── [기능명] v0.7
    ├── [기능명] 정책서 v0.7
    └── [기능명] 기능 설계서 v0.7
```

규칙:

- 발행 label은 `v0.7`로 고정한다.
- container page title은 `[안전화된 기능명] v0.7`을 사용한다.
- child page title은 `[안전화된 기능명] 정책서 v0.7`, `[안전화된 기능명] 기능 설계서 v0.7`을 기본값으로 한다.
- title에 `v0.7`이 빠지면 실패다.
- 기능명에 `/`, `\`, 줄바꿈, control character가 있으면 공백으로 정규화한다.
- title 앞뒤 공백은 제거하고, 연속 공백은 1개로 줄인다.

### 8.2 Container Page 본문

container page는 긴 문서 본문을 복제하지 않는다. child page 링크와 발행 메타데이터만 둔다.

필수 내용:

- 기능명
- 정책서 child link
- 기능 설계서 child link
- 발행 일시
- 발행 label: `v0.7`
- 문서 상태: `SSOT 후보`
- 발행 도구: `planning-kit planning-publish-confluence`
- 발행 기준: `현재 context memory`
- 발행 operation id
- 정책서 content fingerprint
- 기능 설계서 content fingerprint
- target page id와 version (readback 후 갱신)

### 8.3 Child Page 본문

child page에는 compact publish metadata block과 해당 문서 본문만 넣는다.

metadata block 필수 항목:

- 문서 종류: `정책서` 또는 `기능 설계서`
- 기능명
- 발행 일시
- 발행 label: `v0.7`
- 문서 상태: `SSOT 후보`
- 발행 도구: `planning-kit planning-publish-confluence`
- 발행 기준: `현재 context memory`
- content fingerprint
- operation id
- source 상태: `context memory`
- 검토 상태: context에 `planning-review` 통과/수정 필요 신호가 명확하면 반영, 없으면 `확인 불가`

제외할 화면 전용 section:

- `## 생성 결과 요약`
- `## 결정 보드`
- `## 검증 피드백`
- `## 출처 요약`
- `## 입력 제외 요약`
- `## 상세 추적`
- `## 최우선 수정 항목`
- `## 작업 백로그`

정책서와 기능 설계서 본문 내부 heading, 표, list, marker는 유지한다.

## 9. 중복 Title 처리

### 9.1 중복 조회

쓰기 전 target hierarchy 기준으로 2단계 조회한다.

1. 선택된 parent의 child page에서 `v0.7` container title 중복을 확인한다.
2. container가 새로 생성될 예정이면 child page title 중복은 container 생성 후가 아니라 preflight plan에서 `중복 없음`으로 표시한다.
3. container가 이미 있거나 업데이트 대상이면 해당 container의 child page에서 `v0.7` 정책서·기능 설계서 title 중복을 확인한다.
4. 선택된 parent 바로 아래에 정책서·기능 설계서 title이 이미 있거나, `v0.7` 없는 unversioned title이 있으면 legacy flat-child collision으로 분류한다.
5. suffix 적용 후와 최종 write 직전에 같은 조회를 다시 수행해 race를 확인한다.

확인 대상:

- parent level: `[기능명] v0.7` container page title
- container level: `[기능명] 정책서 v0.7`, `[기능명] 기능 설계서 v0.7` child page title
- legacy flat level: parent 바로 아래의 정책서·기능 설계서 title 또는 `v0.7` 없는 unversioned title

### 9.2 중복 발견 시 AskUserQuestion

같은 target 위치에 같은 title의 page가 있으면 자동 덮어쓰기하지 않는다.

선택지:

| 선택지 | 동작 |
|---|---|
| 기존 페이지 업데이트 | 같은 target 위치의 같은 역할 page(container/policy/feature)와 같은 `v0.7` label page만 full-body replacement로 업데이트한다. |
| 새 title로 생성 | title suffix를 입력받아 새 page를 만든다. |
| 취소 | 스킬을 종료하고 Confluence에 쓰지 않는다. |

기존 페이지 업데이트 preflight 필수 항목:

- page id
- page URL
- current version
- current parent title과 URL
- last updated
- page 역할 marker: `container`, `정책서`, `기능 설계서`
- 발행 label: `v0.7`
- 교체 범위: full-body replacement
- 기존 본문 fingerprint
- 새 본문 fingerprint

업데이트 직전 current version을 다시 읽고 preflight version과 다르면 version conflict로 취소한다. `v0.7` label이 없는 page는 update target이 아니며, 자동 merge, blind overwrite, append update는 금지한다.

AskUserQuestion을 사용할 수 없는 실행 환경에서는 같은 선택지를 일반 사용자 질문 1회로 표시한다. 응답이 없거나 불명확하면 취소한다.

새 title suffix 규칙:

- 기본 제안: `vYYYY-MM-DD`
- 사용자가 직접 suffix를 입력할 수 있다.
- suffix 적용 후에도 중복이면 재질문 1회. 2회 중복이면 취소한다.

### 9.3 부분 중복

container는 없는데 child title만 parent 아래에 이미 있는 경우:

- 임의로 기존 child를 새 container 아래로 이동하지 않는다.
- 기존 flat child와 `v0.7` 없는 unversioned page를 업데이트하지 않는다.
- 새 title suffix 생성 또는 취소만 허용한다.
- page move는 0.2.13 범위 밖이므로 별도 스킬/수동 작업으로 남긴다.

## 10. 쓰기 전 최종 확인

Confluence create/update 호출 직전에 AskUserQuestion으로 최종 확인을 받는다.

표시 내용:

- parent title과 URL
- parent page id, space key, current version
- 생성 또는 수정될 page title과 target hierarchy
- 발행 label: `v0.7`
- 문서 상태: `SSOT 후보`
- 업데이트 대상 page id, URL, current version, last updated
- 신규 생성 page 수
- 업데이트 page 수
- 정책서/기능 설계서 본문 추출 상태
- 중복 처리 선택 결과
- content fingerprint
- operation id
- write order
- page move 없음

선택지:

| 선택지 | 동작 |
|---|---|
| 발행 진행 | Confluence write를 실행한다. |
| 취소 | Confluence에 쓰지 않고 종료한다. |

이 확인 전에는 Confluence에 page create/update를 호출하지 않는다.

AskUserQuestion을 사용할 수 없는 실행 환경에서는 일반 사용자 질문 1회로 최종 확인을 받는다. 명확한 진행 의사가 없으면 취소한다.

### 10.1 Write 순서와 readback

쓰기 전 모든 page body를 memory에서 render하고 fingerprint를 계산한다.

write 순서:

1. 최종 확인 후 parent와 update target page version을 다시 읽는다.
2. parent가 바뀌었거나 update target version이 preflight와 다르면 취소한다.
3. container page를 create/update한다.
4. container write 후 readback으로 page id, URL, version, fingerprint metadata를 확인한다.
5. container readback 실패 시 child page write를 시작하지 않는다.
6. 정책서 child page를 create/update한다.
7. 정책서 readback 실패 시 기능 설계서 write를 시작하지 않는다.
8. 기능 설계서 child page를 create/update한다.
9. 기능 설계서 readback을 확인한다.

각 readback은 다음을 확인한다.

- page id
- title (`v0.7` 포함)
- parent id
- version 증가 또는 신규 version
- operation id
- content fingerprint
- 문서 종류 marker
- 발행 label: `v0.7`

### 10.2 부분 실패와 재개

Confluence write는 transaction이 아니므로 자동 rollback/delete를 하지 않는다.

부분 실패 규칙:

- 성공한 page는 삭제하지 않는다.
- 실패 이후 남은 write는 실행하지 않는다.
- 결과를 `부분 완료`로 표시한다.
- 성공 page URL, page id, version을 출력한다.
- 실패 page title, 실패 step, 실패 사유를 출력한다.
- 다음 실행에서 같은 operation id와 fingerprint가 확인되면 성공 page는 `변경 없음`으로 보고 남은 page만 재개할 수 있다.
- fingerprint가 다르면 자동 재개하지 않고 새 발행 시도로 취급해 최종 확인을 다시 받는다.

## 11. 출력 계약

### 11.1 취소 출력

```markdown
# planning-publish-confluence

- 결과: 발행 취소
- 이유: 현재 context memory에서 정책서·기능 설계서 두 본문을 명확히 식별할 수 없습니다.
- Confluence 변경: 없음

## 부족 항목

- 정책서 본문 없음
- 기능 설계서 경계 불명확
```

### 11.2 완료 출력

```markdown
# planning-publish-confluence

- 결과: Confluence 발행 완료
- parent: Product Team Space / SSOT
- 기능: [기능명]
- 발행 label: v0.7
- 문서 상태: SSOT 후보
- 생성: 3개
- 업데이트: 0개
- operation id: publish-YYYYMMDD-HHMMSS-[short-hash]

## 생성/수정 페이지

| 문서 | 동작 | page id | version | URL |
|---|---|---:|---:|---|
| [기능명] v0.7 | 생성 | 123 | 1 | https://... |
| [기능명] 정책서 v0.7 | 생성 | 124 | 1 | https://... |
| [기능명] 기능 설계서 v0.7 | 생성 | 125 | 1 | https://... |

## Fingerprint

| 문서 | fingerprint |
|---|---|
| 정책서 | sha256:... |
| 기능 설계서 | sha256:... |

## 주의

- 발행 기준: 현재 context memory
- 문서 상태: SSOT 후보
- 화면 전용 section은 child page 본문에서 제외했습니다.
```

규칙:

- 최종 출력은 반드시 `# planning-publish-confluence`로 시작한다.
- 완료 출력은 URL을 먼저 보여준다.
- 성공한 page와 실패한 page를 섞어 숨기지 않는다.
- 일부 실패가 있으면 결과를 `부분 완료`로 표시하고 성공/실패를 분리한다.
- 업데이트 결과에는 이전 version과 새 version을 함께 표시한다.
- `변경 없음` page는 생성/수정 count와 별도로 표시한다.
- 모든 생성/수정 page title에는 `v0.7`이 포함되어야 한다.

## 12. 검증 계획

`planning-kit/docs/prd/fixtures/prd-0.2.13-fixtures.yml`은 release gate다.

1. 금지 입력 fixture 작성
   - positional path 입력 → 취소, local read 0건, Confluence 조회 0건
   - source URL 입력 → 취소, URL fetch 0건, Confluence 조회 0건
   - `planning/...` save path 입력 → 취소, local read 0건
   - option 입력 → 취소
2. context memory gate fixture 작성
   - 두 본문 있음 → 통과
   - 정책서만 있음 → 취소
   - 기능 설계서만 있음 → 취소
   - 두 기능이 섞임 → 취소
   - 0.2.12 화면 출력 metadata 제외 → 통과
   - planning-review 출력이 섞임 → report section 제외
   - 같은 문서 종류 candidate 2개 → 취소
3. parent URL 검증 fixture 작성
   - 기본 SSOT URL
   - 유효한 직접 입력 URL
   - page id 없는 URL
   - 다른 host URL
   - default parent 403/404 → 취소
   - 직접 입력 parent archived/deleted → 취소
   - create-child 권한 없음 → 취소
4. duplicate title fixture 작성
   - 중복 없음 → 신규 생성
   - container 중복 → `v0.7` label page만 업데이트/새 title/취소 분기
   - container child 중복 → `v0.7` label page만 업데이트 preflight
   - legacy flat child 중복 → 새 title/취소만 허용
   - unversioned title 중복 → update 금지, 새 title/취소만 허용
   - suffix collision 2회 → 취소
   - duplicate check 후 write 직전 race → 취소
5. write safety fixture 작성
   - 최종 확인 전 create/update 0건
   - update version conflict → 취소
   - container write 실패 → child write 0건
   - 정책서 readback 실패 → 기능 설계서 write 0건
   - 부분 완료 출력에 성공 URL/page id/version과 실패 step 포함
   - 같은 fingerprint 재실행 → 변경 없음 또는 남은 page 재개
   - readback fingerprint mismatch → 부분 완료 또는 실패
6. title/version label fixture 작성
   - container title에 `v0.7` 포함
   - 정책서 child title에 `v0.7` 포함
   - 기능 설계서 child title에 `v0.7` 포함
   - metadata에 발행 label `v0.7` 포함
   - `v0.7` 없는 title 생성 시도 → 실패
7. Confluence write는 mock 또는 connector dry-run으로 검증한다.
8. `claude plugin validate ./planning-kit`
9. plugin manifest JSON parse
10. root marketplace JSON parse
11. `git diff --check -- planning-kit`
12. README와 PRD chain에 0.2.13 노출 확인

## 13. 롤아웃 계획

1. 신규 skill 추가
   - `planning-kit/skills/planning-publish-confluence/SKILL.md`
   - context gate, parent selection, duplicate handling, final confirmation, output contract를 orchestration에 명시
2. reference 분리
   - `references/context-gate.md`
   - `references/confluence-page-contract.md`
   - `references/output-contract.md`
3. README/workflow 업데이트
   - 네 번째 스킬로 `planning-publish-confluence` 추가
   - `planning-format → planning-review → planning-publish-confluence → ssot-audit` 흐름 설명
   - root `README.md`
   - `planning-kit/README.md`
   - `planning-kit/docs/planning-kit-workflow-guide.md`
   - `planning-kit/docs/planning-format-workflow.md`
   - `planning-kit/docs/planning-review-workflow.md`
   - `planning-kit/docs/planning-kit-install-guide-windows.md`
   - `planning-kit/docs/planning-kit-presentation.md`
   - workflow diagram이 공개 surface에 있으면 diagram source와 rendered image도 갱신
4. PRD chain 업데이트
   - `docs/prd/README.md`에 0.2.13 추가
5. fixture 추가
   - `planning-kit/docs/prd/fixtures/prd-0.2.13-fixtures.yml`
   - context gate, forbidden input, parent selection, duplicate handling, update conflict, no-write-before-confirm, readback, partial failure, `v0.7` title label, output contract
6. manifest 업데이트
   - `planning-kit/.claude-plugin/plugin.json`
   - `planning-kit/.codex-plugin/plugin.json`
   - Codex interface capabilities에 `Write` 추가
   - description/defaultPrompt에 Confluence publish 흐름 추가
   - 외부 Confluence write에 필요한 privacy/terms 문서가 없으면 추가하거나, 기존 정책 문서 적용 범위를 명시
7. marketplace/cache 동기화
   - `.claude-plugin/marketplace.json`
   - `.agents/plugins/marketplace.json`
8. 검증
   - `claude plugin validate ./planning-kit`
   - manifest JSON parse
   - marketplace JSON parse
   - `git diff --check`
   - Confluence write mock 검증
9. rollback 기준
   - context memory에 없는 문서를 검색해 발행하려 하면 release 중단
   - 사용자 최종 확인 전 create/update가 발생하면 release 중단
   - 중복 title을 자동 덮어쓰면 release 중단
   - page move를 수행하려 하면 release 중단
   - update version conflict를 무시하고 overwrite하면 release 중단
   - readback 없이 성공 처리하면 release 중단
   - Codex manifest에 `Write` capability가 빠지면 release 중단
   - 기본 parent와 직접 입력 parent가 구분되지 않으면 release 중단
   - Confluence title 또는 metadata에 `v0.7` label이 빠지면 release 중단
   - `v0.7` 없는 unversioned page를 update target으로 삼으면 release 중단

## 14. 릴리즈 노트 초안

`planning-kit` 0.2.13은 검토가 끝난 정책서와 기능 설계서를 Confluence SSOT 하위 페이지로 발행하는 `planning-publish-confluence` 스킬을 추가합니다. 이 스킬은 현재 context memory에 두 본문이 모두 명확히 있을 때만 동작하며, 아직 확정 SSOT가 아니므로 container와 child page title에 `v0.7`을 붙여 발행합니다. 기본 SSOT parent를 제안하되 사용자가 직접 parent URL을 입력할 수 있고, Confluence write 전에는 parent, page hierarchy, 중복 처리 결과, page id/version, content fingerprint를 다시 확인하며, write 후 readback으로 성공 여부를 검증합니다.
