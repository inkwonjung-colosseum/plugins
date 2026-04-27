---
name: plan-draft
description: "Read local Confluence exports, ask focused planning questions, and draft a 상위설계서, 기능설계서, or 정책서."
argument-hint: "<기획 의도>"
---

# plan-draft

기획 의도를 입력받아 로컬 Confluence 문서를 읽고, 구체화 질문을 통해 초안을 생성하는 메인 스킬.

## 호출

- Claude Code: `/planning-team-kit:plan-draft <기획 의도>`
- Codex: `$plan-draft <기획 의도>`

## 동작 순서

### 1. 로컬 문서 탐색

먼저 `references/confluence-retrieval.md`의 index 기반 retrieval 절차를 따른다. 입력에서 제품, 도메인, 문서 영역, 키워드를 추출하고 `.confluence-index/registry.json`에서 관련 export source를 고른 뒤 로컬 Confluence 파일을 읽는다.
- 도메인/제품/문서 영역은 사용자 입력, `source-index.jsonl`, `tree.md`에서 추론한다
- 고정 export root를 가정하지 않는다. `.confluence-index/registry.json`의 `display_path`와 source metadata를 따른다
- 읽기 우선순위: 정책/상세 문서 → 상위 설계 문서 → 최근 결정사항이 담긴 회의록
- 로컬에서 찾을 수 있는 것은 질문하지 않는다
- `.confluence-index/`는 retrieval metadata로만 사용하고, claim은 raw exported Markdown을 읽은 뒤에만 한다

### 2. 신규 vs 수정 판별

**수정 모드** — 유사한 기존 문서가 있을 때:
- `confluence/confluence-lock.json`의 모든 `orgs > {site_url} > spaces > {space_id} > pages`에서 제목과 export path 후보를 찾는다
- 후보가 정확히 1개이면 해당 `site_url`, `space_id`, `page_id`를 사용한다
- 후보가 없거나 여러 개이면 추측하지 않고 사용자에게 대상 페이지 또는 source를 확인한다
- 필드: `title`, `version`, `export_path`

**신규 모드** — 유사한 문서가 없을 때:
- 문서 타입 판별 후 적합한 Confluence 위치 제안
- 위치는 선택한 export source의 hierarchy와 유사 문서 위치를 기준으로 제안한다
- 적절한 parent 후보가 1개로 좁혀지지 않으면 사용자에게 parent page 또는 위치를 확인한다

### 3. 문서 타입 자동 판별

| 판별 기준 | 문서 타입 |
|:---------|:---------|
| 방향·범위·WHY·배경 | 상위설계서 |
| 화면·기능·플로우·HOW | 기능설계서 |
| 규칙·예외·조건·정책 | 정책서 |

### 4. 질문 루프

구체화 완료될 때까지 질문한다. 제한 없음.

**원칙:**
- 한 번에 한 개만 질문한다
- 로컬 파일로 확인할 수 있는 것은 질문하지 않고 직접 읽는다
- 가정이 필요한 경우 `[가정]` 태그로 명시한 뒤 계속 진행한다
- 질문은 짧고 명확하게. 선택지 제공 가능

**확인해야 할 것들 (상황에 따라 선택적으로):**
- 왜 필요한가? (문제/배경)
- 어떤 사용자/역할에게 적용되는가?
- 정상 케이스 동작
- 예외·엣지케이스 처리 (동시성, 빈값, 권한 없을 때 등)
- 기존 어떤 기능/정책과 연결되는가?
- 이번 범위에서 제외하는 것
- 아직 결정되지 않은 사항
- 개발팀이 알아야 할 제약

**구체화 완료 기준:**
- 문서 타입이 확정됨
- 적용 범위가 명확함
- 핵심 규칙/동작을 서술할 수 있음
- 주요 예외 케이스를 파악함

### 5. 초안 생성

구체화 완료 후 해당 문서 타입 템플릿을 기반으로 초안을 생성한다.
- 템플릿 위치: `skills/plan-draft/templates/`
- 모든 섹션을 채운다. 정보가 없는 필드는 `[미정]`으로 표시
- 가정한 내용은 `[가정]` 태그로 명시

## 출력 형식

### 신규 문서
```
📄 신규 [문서타입]
위치: <문서그룹>/<문서영역>/[제목].md
상위 페이지: [parent_title] (page_id: XXXXXXXXXX)
Publish gate: clean / review-required
Review required reason: [미정] / [가정] / 충돌 경고 / 없음

---
[문서 전체 내용]
---

다음 단계: /planning-team-kit:plan-review 또는 /planning-team-kit:plan-publish
```

### 기존 문서 수정
```
✏️ 수정: [기존 파일명]
page_id: XXXXXXXXXX (현재 버전: N)
Publish gate: clean / review-required
Review required reason: [미정] / [가정] / 충돌 경고 / 없음

변경 내용:
[기존] ...
[변경] ...

다음 단계: /planning-team-kit:plan-review 또는 /planning-team-kit:plan-publish
```

## 규칙

- 기존 Confluence 내용과 충돌하는 내용을 초안에 포함하지 않는다. 충돌이 있으면 먼저 언급한다.
- 초안에 `[미정]`, `[가정]`, 기존 문서와의 충돌 경고가 있으면 `Publish gate: review-required`로 표시한다.
- `Publish gate: review-required`인 초안은 `/planning-team-kit:plan-review` 결과 또는 명시적 사용자 확인 없이는 publish 대상으로 넘기지 않는다.
- 초안은 항상 로컬에만 존재한다. Confluence 반영은 `/planning-team-kit:plan-publish`에서 한다.
- Daily Sync나 Weekly Sync에 오늘 관련 결정사항이 있으면 컨텍스트에 반영한다.
