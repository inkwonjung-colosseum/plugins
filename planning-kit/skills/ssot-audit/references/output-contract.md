# Output Contract

`ssot-audit`는 화면 markdown only로 출력한다. 파일 저장, `--save`, 점수, 등급, health score를 만들지 않는다. 0.2.9부터 기본 corpus는 프로젝트 전체 Markdown이 아니라 폴더명에 독립 `SSOT` token이 있는 하위 폴더 안의 Markdown이다.

## 1. 기본 출력

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
- full 후보표/제외표/외부 출처표는 5 조건에 따라 하단 `## 상세 추적`에 둔다.

## 2. Section 출력 규칙

- 활성 안 한 축의 발견/권고는 생략한다.
- 발견/권고가 0건이면 `## 발견 및 권고`에 `없음`을 출력한다.
- `## SSOT 인벤토리`는 실질 본문과 placeholder를 구분한다.
- `## 제외 요약`은 SSOT token 밖 Markdown, 생성 초안 영역, 내부 plugin/skill 문서를 최소 1행 이상 요약한다.
- 개선 백로그는 발견/권고를 문제 단위로 묶어 중복을 줄인다.
- 작업 ID는 `A1`, `A2` 형식을 쓴다.

## 3. Backlog 우선순위

| 유형 | 기준 |
|---|---|
| `내용 정합성` | 같은 정책/상태/권한/임계값의 직접 충돌, 핵심 정책값 `[TBD]` |
| `구조 정리` | canonical 부재/중복, 외부 canonical 의존, 핵심 문서 역할 불명확 |
| `SSOT 보강` | SSOT token 폴더 없음, placeholder-only, 결정 문장 부재 |
| `문서 이동` | SSOT 기준 문서가 token 폴더 밖에 있음 |
| `동기화 워크플로` | 생성 초안과 SSOT 기준 문서의 갱신 절차 부재 |

## 4. Sanity Check

| 케이스 | 메시지 |
|---|---|
| SSOT token 폴더 없음 | `감사 불가 — 선언된 SSOT token 폴더 없음` |
| SSOT token 폴더 Markdown 0개 | `감사 불가 — SSOT token 폴더 안 Markdown 없음` |
| `--ssot-include`가 SSOT 경계 밖만 매칭 | `감사 불가 — 명시 include가 SSOT 폴더 경계 밖이라 제외됨` |
| `--axes` 빈 값 | `--axes에 감사 축을 1개 이상 지정하세요. (structure, content)` |
| 알 수 없는 축 | `지원하지 않는 감사 축입니다: <axis>. 사용 가능: structure, content` |
| 외부 URL 모두 실패 | 감사는 계속 진행. `## 상세 추적`의 외부 출처에 실패 행을 기록하고 로컬 SSOT Markdown 기준으로 결과 출력 |
| 로컬 SSOT Markdown 본문 대부분 비어 있음 | 감사는 계속 진행. 결론/인벤토리/개선 백로그에 placeholder 한계를 표시 |

## 5. 상세 추적 조건

| 조건 | 처리 |
|---|---|
| SSOT token 폴더 없음 또는 후보 0건 | 후보 탐색/제외 요약 full table 출력 |
| placeholder가 1건 이상 | placeholder 경로와 판정 사유 요약 출력 |
| `--ssot-include`가 SSOT 경계 밖만 매칭 | include glob, 경계 밖 매칭 수, 제외 사유 출력 |
| 외부 follow 또는 image 처리 1건 이상 | 외부 출처표 출력 |
| 외부 fetch 실패, 인증 실패, 본문 미사용 출처 1건 이상 | 외부 출처표 출력 |

### 5.1 Full Corpus 후보표

```markdown
### SSOT 후보

| 경로 | SSOT token segment | placeholder | 본문 사용 | 비고 |
|---|---|---|---|---|
| Product SSOT/policy.md | Product SSOT | 아니오 | O | 결정 문장 있음 |
| ProductSSOT/policy.md | - | - | X | SSOT substring만 있어 제외 |
| planning/[SSOT]/draft.md | [SSOT] | - | X | planning/** 생성 초안 영역 |
```

### 5.2 외부 출처표

```markdown
### 외부 출처

| # | 출처 종류 | URL/경로 | origin (.md file:line) | 상태 | 본문 사용 |
|---|---|---|---|---|---|
| 1 | 자식 URL | https://wiki.example/policy/order | Product SSOT/order.md:12 | 200 (via WebFetch) | O |
| 2 | 자식 URL | https://docs.google.com/... | Product SSOT/order.md:28 | 200 (via Google Drive connector - read_file_content) | O |
| 3 | 자식 URL | https://private.example/... | Product SSOT/order.md:40 | 인증 필요 | X |
```
