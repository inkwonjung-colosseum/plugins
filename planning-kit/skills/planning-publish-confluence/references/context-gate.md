# Context Gate

`planning-publish-confluence`는 현재 context memory에 이미 있는 정책서와 기능 설계서 두 본문, 또는 사용자가 명시한 0.2.14 저장 폴더의 canonical 두 파일만 발행 대상으로 사용한다.

## 1. 금지 입력

호출 인자 dispatch:

| 입력 | 처리 |
|---|---|
| 인자 없음 | 현재 context memory gate |
| `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 저장 폴더 1개 | 0.2.14 저장 폴더 입력 gate |
| 그 외 | 금지 입력으로 즉시 취소 |

다음 중 하나라도 있으면 금지 입력으로 즉시 취소한다.

- 허용 형식이 아닌 non-empty positional token
- `--`로 시작하는 option
- `http://` 또는 `https://` URL token
- Confluence page URL
- `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 저장 폴더가 아닌 `planning/` 경로
- `.planning-kit/`, `.md`, `.markdown`, `.txt`, 이미지 확장자처럼 임의 파일이나 경로로 해석될 수 있는 token
- 여러 저장 폴더

금지 입력 분기에서는 다음 tool/action을 모두 실행하지 않는다.

- 로컬 파일 read
- URL fetch
- connector fallback
- Confluence parent 조회
- AskUserQuestion 실행

취소 이유는 다음 문장을 포함한다.

```text
발행 취소 — planning-publish-confluence는 현재 context memory의 두 본문 또는 명시적 planning/[안전기능명]--YYYY-MM-DD-HHMMSS/ 저장 폴더 1개만 발행 대상으로 사용합니다.
```

## 2. Context Memory 정의

context memory는 현재 스킬 실행 시점의 대화, 직전 tool 결과, 현재 turn에 이미 로드된 본문이다.

다음은 context memory가 아니다.

- 장기 memory 파일
- repo 전체 검색 결과
- 새로 읽은 로컬 파일
- 새로 fetch한 URL
- 새 Confluence lookup 결과

## 2A. 0.2.14 저장 폴더 입력

저장 폴더 입력은 사용자가 명시적으로 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 폴더 1개를 인자로 준 경우에만 사용한다.

통과 조건:

1. 폴더가 존재하고 읽기 가능하다.
2. 폴더 경로는 repo root 기준 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` direct child다.
3. `planning/foo/`, `planning/drafts/...`, `planning/여러/중첩/...`는 인정하지 않는다.
4. 폴더 바로 아래 정책서 파일 1개와 기능설계서 파일 1개가 있다.
5. 정책서 파일명은 `*_정책서.md`, 기능설계서 파일명은 `*_기능설계서.md` 형식이다.
6. 하위 폴더 재귀 탐색, sibling 폴더 glob, 최근 폴더 자동 선택은 하지 않는다.
7. 두 파일의 H1 또는 파일명 기반 기능명이 서로 충돌하지 않는다.

처리:

- 통과하면 canonical 정책서·기능설계서 두 파일만 read한다.
- `## 저장 파일`, `## 결론`, `## 체크해야 할 항목`, `## 출처/누락 요약`, `## 검토 결과`, `## 검토 근거 요약`, `## 상세 추적`, `## 저장 실패 상세` 같은 report section은 child page 본문으로 발행하지 않는다.
- `planning/**` 저장 파일은 발행 후보 입력으로만 사용하며 SSOT 검토 근거로 승격하지 않는다.
- URL fetch, Confluence 원문 재조회, 임의 `.md` 파일 묶음 추론은 하지 않는다.

실패 시에는 Confluence parent 조회나 쓰기 확인으로 넘어가지 않고, 어느 조건이 실패했는지만 짧게 보고한다.

## 3. Publishable Candidate

통과 조건:

1. 정책서 candidate 1개.
2. 기능 설계서 candidate 1개.
3. 두 candidate가 같은 기능명으로 묶임.
4. 각 candidate에 제목 또는 wrapper heading이 있음.
5. 각 candidate에 실질 section 2개 이상이 있음.
6. 같은 문서 종류 candidate가 2개 이상 없음.
7. 같은 기능의 candidate revision이 2개 이상 없음.

`candidate가 2개 이상`이면 최신/이전 판단을 하지 않고 취소한다.

## 4. Wrapper Heading

정책서 wrapper:

- `# 정책서`
- `## 정책서`
- `# [기능명] 정책서`
- `## [기능명] 정책서`

기능 설계서 wrapper:

- `# 기능설계서`
- `## 기능설계서`
- `# 기능 설계서`
- `## 기능 설계서`
- `# [기능명] 기능 설계서`
- `## [기능명] 기능 설계서`

`v0.7`은 Confluence title label이며, context body wrapper에는 없어도 된다.

## 5. Excluded Report Sections

다음 heading은 publish metadata 또는 review report로 보고 발행 본문에서 제외한다.

- `## 생성 결과 요약`
- `## 결정 보드`
- `## 저장 파일`
- `## 검증 피드백`
- `## 체크해야 할 항목`
- `## 출처 요약`
- `## 출처/누락 요약`
- `## 입력 제외 요약`
- `## 상세 추적`
- `## 결론`
- `## 검토 결과`
- `## 검토 근거 요약`
- `## 최우선 수정 항목`
- `## 작업 백로그`
- `## 저장 실패 상세`

정책서 본문 종료 경계는 기능 설계서 wrapper 또는 위 report heading 또는 EOF 중 먼저 등장하는 항목이다. 기능 설계서도 같은 규칙을 따른다.

## 6. Ambiguity

다음 경우는 `readable projection boundary ambiguous`로 보고 취소한다.

- 같은 metadata 영역에 duplicate report heading이 있음.
- misplaced `## 생성 결과 요약` 또는 `## 결정 보드`가 본문 중간에 있음.
- fence 밖에 같은 문서 종류 wrapper가 2개 이상 있음.
- code fence 안 wrapper와 fence 밖 wrapper가 같은 문서 종류에서 함께 있음.
- blockquote, list child, table cell 안 heading-like text만 있고 publishable wrapper가 없음.

publish 스킬은 ambiguity warning을 남기고 진행하지 않는다.

## 7. Child Body

본문 추출 후 child page에는 compact publish metadata block을 붙이고, 원문 본문은 그 아래에 둔다. bulky 화면 전용 section과 상세 trace는 child page 본문에 복제하지 않는다.
