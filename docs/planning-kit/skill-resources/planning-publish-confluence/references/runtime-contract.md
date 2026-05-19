---
name: planning-publish-confluence
description: "현재 context memory 안에 정책서와 기능 설계서 두 본문이 모두 명확하거나, 명시적 planning/[안전기능명]--YYYY-MM-DD-HHMMSS/ 저장 폴더 입력이 있을 때만 Confluence SSOT parent 아래 v0.7 후보 문서로 발행한다. URL/임의 .md/여러 폴더 입력은 받지 않고, parent 선택·중복 처리·최종 확인 후 Confluence page create/update와 readback을 수행한다."
argument-hint: "(인자 없음 | [planning/[안전기능명]--YYYY-MM-DD-HHMMSS/])"
---

# planning-publish-confluence

현재 context memory에 이미 있는 정책서와 기능 설계서 본문, 또는 사용자가 명시한 0.2.14 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 저장 폴더의 canonical 두 파일을 Confluence SSOT 하위에 `v0.7` 후보 문서로 발행하는 스킬이다.

## 호출

- Claude Code: `/planning-kit:planning-publish-confluence`
- Codex: `$planning-publish-confluence`

지원 입력:

- 인자 없음: 현재 context memory에서 정책서·기능 설계서 두 본문을 찾는다.
- 저장 폴더 경로 1개: `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` direct child 폴더에서 canonical 정책서·기능설계서 두 파일만 읽는다.

URL, Confluence page URL, 임의 `.md`, 임의 경로, 여러 저장 폴더, `planning/` 밖 경로, `planning/foo/`, `planning/drafts/...`, 중첩 폴더는 받지 않는다.

## 책임과 경계

- 현재 context memory 또는 명시적 저장 폴더에서 정책서 1개와 기능 설계서 1개를 식별한다.
- 기본 Confluence parent는 `https://colosseum.atlassian.net/wiki/spaces/PROD/pages/1767604270/SSOT`이다.
- AskUserQuestion 또는 동일한 일반 질문으로 기본 parent 사용, 다른 parent URL 입력, 취소를 받는다.
- Confluence title과 metadata에는 항상 `v0.7` 발행 label을 붙인다.
- 사용자 최종 확인 전에는 Confluence page create/update를 호출하지 않는다.
- page move, 자동 merge, blind overwrite, append update, batch publish, 예약 publish는 하지 않는다.
- SSOT 품질 검토는 하지 않는다. `planning-review`와 `ssot-audit`가 담당한다.

## 동작 시퀀스

### Step 1: 입력 dispatch와 금지 입력 확인

호출 인자에 따라 다음 중 하나로 분기한다.

| 입력 | 처리 |
|---|---|
| 인자 없음 | Step 2 context memory gate로 진행 |
| `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 저장 폴더 1개 | Step 2A 저장 폴더 gate로 진행 |
| 그 외 non-empty positional token 또는 `--` option | 즉시 취소 |

금지 입력 분기에서는 다음을 모두 금지한다.

- 로컬 파일 read
- URL fetch
- connector fallback
- Confluence parent 조회
- AskUserQuestion 실행

출력은 `references/output-contract.md`의 금지 입력 취소 형식을 따른다.

### Step 2: context memory gate

`references/context-gate.md`를 읽고 현재 context memory에서 정책서·기능 설계서 두 본문을 식별한다.

통과 조건:

- 정책서 publishable candidate 1개
- 기능 설계서 publishable candidate 1개
- 같은 기능명 1개
- 각 본문에 제목/heading과 실질 section 2개 이상
- `readable projection boundary ambiguous`에 해당하는 ambiguity 없음

통과하지 못하면 Confluence 조회 없이 취소한다.

### Step 2A: 저장 폴더 gate

명시적 저장 폴더 입력이 있으면 `references/context-gate.md`의 `0.2.14 저장 폴더 입력` 규칙을 따른다.

통과 조건:

- repo root 기준 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` direct child 폴더 1개
- 폴더 바로 아래 정책서 파일 1개와 기능설계서 파일 1개
- 정책서 파일명 `*_정책서.md`, 기능설계서 파일명 `*_기능설계서.md`
- 하위 폴더 재귀 탐색, sibling folder glob, 최근 폴더 자동 선택 없음
- 두 파일의 H1 또는 파일명 기반 기능명이 서로 충돌하지 않음

통과하면 canonical 정책서·기능설계서 두 파일만 발행 후보 본문으로 읽는다. `## 저장 파일`, `## 결론`, `## 체크해야 할 항목`, `## 출처/누락 요약`, `## 검토 결과`, `## 검토 근거 요약`, `## 상세 추적`, `## 저장 실패 상세` 같은 report section은 child page body로 발행하지 않는다.

### Step 3: parent 선택

context gate 통과 후에만 parent 선택 질문을 한다.

선택지:

| 선택지 | 동작 |
|---|---|
| 기본 SSOT 사용 | 기본 parent URL을 사용한다. |
| 다른 parent URL 입력 | 사용자가 Confluence page URL을 직접 입력한다. |
| 취소 | Confluence 변경 없이 종료한다. |

AskUserQuestion을 사용할 수 없으면 같은 선택지를 일반 사용자 질문 1회로 표시한다. 응답이 없거나 불명확하면 기본값을 추측하지 않고 취소한다.

### Step 4: parent preflight

`references/confluence-page-contract.md`의 parent 검증 규칙을 따른다.

검증 항목:

- `https://colosseum.atlassian.net/wiki/spaces/` URL
- page id 추출 가능
- parent read 가능
- page title, page id, current version, ancestor path 확인
- archived/deleted 아님
- selected parent 아래 child page create 권한 있음
- 기존 page update가 예정되면 target page update 권한 있음

검증 실패 시 Confluence write 없이 취소한다.

### Step 5: target hierarchy와 duplicate preflight

`references/confluence-page-contract.md`의 `v0.7` hierarchy를 만든다.

```text
[선택된 parent]
└── [기능명] v0.7
    ├── [기능명] 정책서 v0.7
    └── [기능명] 기능 설계서 v0.7
```

중복 조회는 parent level과 container level을 나눠 수행한다.

- parent level: `[기능명] v0.7` container title
- container level: `[기능명] 정책서 v0.7`, `[기능명] 기능 설계서 v0.7`
- legacy flat level: parent 바로 아래 정책서/기능 설계서 title 또는 `v0.7` 없는 unversioned title

같은 target 위치의 같은 역할 page와 같은 `v0.7` label page만 update target이 될 수 있다. `v0.7` 없는 page는 update target이 아니다.

### Step 6: 최종 확인

Confluence page create/update 직전에 최종 확인을 받는다.

최종 확인에 반드시 포함한다.

- parent title, URL, page id, space key, current version
- target hierarchy와 page title
- 발행 label: `v0.7`
- 문서 상태: `SSOT 후보`
- 신규 생성 page 수
- 업데이트 page 수
- update target page id, URL, current version, last updated
- content fingerprint
- operation id
- write order
- page move 없음

확인 전에는 Confluence page create/update를 호출하지 않는다.

### Step 7: write 실행과 readback

Confluence page create/update는 다음 순서로만 실행한다.

1. parent와 update target page version을 다시 읽는다.
2. parent가 바뀌었거나 update target version이 preflight와 다르면 version conflict로 취소한다.
3. container page create/update.
4. container readback.
5. container readback 실패 시 child write 중단.
6. 정책서 child page create/update.
7. 정책서 readback 실패 시 기능 설계서 write 중단.
8. 기능 설계서 child page create/update.
9. 기능 설계서 readback.

각 readback은 page id, title, parent id, version, operation id, content fingerprint, 문서 종류 marker, `v0.7` label을 확인한다.

Confluence write는 transaction이 아니므로 자동 rollback/delete하지 않는다. 실패 이후 남은 write는 실행하지 않고 `부분 완료`로 출력한다.

### Step 8: 결과 출력

`references/output-contract.md`에 따라 출력한다.

결과는 항상 `# planning-publish-confluence`로 시작한다.

성공, 부분 완료, 변경 없음, 취소를 구분한다. 성공한 page와 실패한 page를 섞어 숨기지 않는다.

## 참고 파일

- `references/context-gate.md` — 금지 입력, context memory 본문 추출, ambiguity 취소 기준.
- `references/confluence-page-contract.md` — parent preflight, `v0.7` hierarchy, duplicate/update/readback 규칙.
- `references/output-contract.md` — 취소/완료/부분 완료 출력 형식.
