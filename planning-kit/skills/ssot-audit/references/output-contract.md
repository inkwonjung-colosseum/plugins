# Output Contract

`ssot-audit`는 화면 markdown only로 출력한다. 파일 저장, `--save`, 점수, 등급, health score를 만들지 않는다.

## 1. 기본 출력

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
| 2 | 자식 URL | https://docs.google.com/... | docs/order.md:28 | 200 (via Google Drive connector - read_file_content) | O |
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

## 2. Section 출력 규칙

- 활성 안 한 축의 section은 생략한다.
- 발견/권고가 0건이면 해당 section에 `없음` 한 줄을 출력한다.
- `## SSOT 제외 문서`는 `v0.8` 미만 문서가 1개 이상일 때만 출력한다.
- `## 외부 출처`는 외부 follow 또는 image 처리가 1건 이상일 때만 출력한다.
- 개선 backlog는 발견/권고를 문제 단위로 묶어 중복을 줄인다.
- backlog 우선순위는 작업 순서 안내일 뿐 health score가 아니다.

## 3. Backlog 우선순위

| 우선순위 | 기준 |
|---|---|
| P0 | 같은 정책/상태/권한/임계값의 직접 충돌, archive 또는 낮은 버전 문서가 최신 기준처럼 참조되는 문제 |
| P1 | canonical 부재/중복, 외부 canonical 의존, 핵심 문서 역할 불명확 |
| P2 | 용어 통일, AC 보강, 설명 없는 중복 정리 |

## 4. Sanity Check

| 케이스 | 메시지 |
|---|---|
| corpus Markdown 0개 | `SSOT 감사 대상 Markdown을 찾을 수 없습니다. --ssot-include 범위 또는 현재 작업 디렉터리를 확인하세요.` |
| 버전 필터 적용 후 SSOT 후보 0개 | `v0.8 이상 또는 버전 없는 SSOT 후보 Markdown을 찾을 수 없습니다. 낮은 버전 문서를 기준으로 쓰려면 먼저 문서 버전을 올리거나 최신 기준 문서를 분리하세요.` |
| `--axes` 빈 값 | `--axes에 감사 축을 1개 이상 지정하세요. (structure, content)` |
| 알 수 없는 축 | `지원하지 않는 감사 축입니다: <axis>. 사용 가능: structure, content` |
| 외부 URL 모두 실패 | 감사는 계속 진행. `## 외부 출처`에 실패 행을 기록하고 로컬 Markdown 기준으로 결과 출력 |
| 로컬 Markdown 본문 대부분 비어 있음 | 감사는 계속 진행. 구조 품질에 `본문 없는 SSOT 후보` 권고 가능 |

외부 fetch 실패는 MVP에서 운영 품질 발견으로 자동 승격하지 않는다. 단, 외부 canonical 의존 판단에 필요한 본문을 가져오지 못하면 해당 항목은 `권고`로만 출력한다.
