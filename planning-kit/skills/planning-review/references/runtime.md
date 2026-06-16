# Runtime

dispatch, 입력, SSOT 식별, fetch, 출력 계약을 한곳에 둔다. `SKILL.md`가 유일한 메타·트리거 소스다.

## 입력

검토 대상은 정책서 1개 + 기능설계서 1개. 입력 형태:

- 인자 없음: 직전 `planning-format` 출력 또는 `## 저장 파일` 핸드오프(`planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 하나).
- `https?://` URL: 각 URL = 검토 소스 루트.
- 디렉터리 1개: 안에서 정책서+기능설계서를 찾는다.
- 파일 1개: 같은 폴더 동반 파일을 스캔해 짝을 식별.
- 비-URL 경로 2개: 파일명·헤딩으로 정책/기능 식별.
- 그 외: 붙여넣은 Markdown.

옵션 없음 — 모든 동작 기본 ON. SSOT 표식 폴더는 항상 R1 외부 교차검증 소스로 포함하고, 입력·SSOT 양쪽의 URL fetch와 이미지 해석을 항상 수행한다.

URL과 비-URL 토큰이 섞이면 텍스트(붙여넣기) 모드. `file://`, `ftp://`, `mailto:`, 스킴 없는 문자열은 URL 모드가 아니다.

## SSOT 마커

- SSOT 근거는 SSOT 표식 폴더만. `planning/**`·`.planning-kit/**`는 SSOT 근거가 아니다.
- SSOT 표식 폴더는 파일명 버전 `>= v0.8` 이거나 버전이 없을 때만 적격. 그 미만 버전은 제외.
- 적격 SSOT가 하나도 없으면 R1은 보류 — SSOT 부재를 finding으로 만들지 않고 검증 보류로 표기한다.

## Dispatch

1. 모든 토큰이 `https?://` URL → URL 모드.
2. 디렉터리 경로 → 디렉터리 모드.
3. 파일 경로 → 파일 모드 (동반 파일 스캔).
4. 비-URL 경로 2개 → 2-경로 모드.
5. 그 외 → 텍스트(붙여넣기) 모드.

## Sequence

1. 입력 dispatch → 정책서·기능설계서 1쌍 식별. 모호하면 중단.
2. SSOT 소스 식별 (표식 폴더만, 항상 포함). 적격 SSOT 없으면 R1 보류.
3. URL 본문을 BFS로 fetch (입력·SSOT 항상). 비공개로 보여도 시도 후 실패를 기록.
4. 이미지 해석 (입력·SSOT 항상).
5. R1+R2+R3 한 패스 (`review-axes.md`). 물류 신호 감지 시 R4 추가 (`logistics-lens.md`).
6. 병합 우선순위 `R1 > R2 > R3 > R4`로 중복 finding을 접는다.
7. 출력 계약 방출.

## URL 수집 / connector

- dequeue된 모든 `https?://` URL을 먼저 직접 fetch. BFS 순회, 정규화 후 visited 집합으로 사이클 방지.
- `mailto:`, `tel:`, `javascript:`, `blob:`, self anchor, 스킴 없는 문자열 무시.
- connector는 직접 fetch가 막히거나 비거나 인증 필요일 때만: Atlassian(Confluence/Jira), Google Drive, Browser/Chrome(로그인 렌더링 필요 시).
- dequeue된 URL마다 출처 행 1개: URL / status / body used / note.

## 출력 계약

최종 출력은 검토 핸드오프지 실행 로그가 아니다. `# [기능명] 검토 결과`로 시작.

- `## 결론`: 검토 합격 / 조건부 / 보류 한 줄 + 핵심 근거.
- `## 검토 결과`: 축별 발견 사항을 깔끔한 표시 라벨로. raw R* 미노출.
- `## 체크해야 할 항목`: `### 결정 필요`, `### 문서 보강 필요`, `### 출처/누락 참고` 하위 순서. 빈 값은 `없음`. 항목 형식 — 확인할 것 / 이유 / 반영 위치(`POL-XXX`·`FUNC-XXX`만).
- `## 상세 추적`: raw R1/R2/R3/R4 ID는 여기서만 노출.

코드펜스 래핑 금지. `SSOT corpus`·`fetch`·`connector fallback` 같은 내부어 노출 금지.

## 경계

- 출력 전용 — 문서 생성·auto-fix 안 함. 의미 변경 제안은 `## 체크해야 할 항목`으로만.
- "미결 사항" 섹션·`(Non-MVP)` 항목은 검토 제외. 기능설계서 8·9 결번은 finding 아님.
- 구현 상세(데이터 모델·API 계약·NFR 수치·테스트)·PM 전략 장식(RACI·Power×Interest·로드맵 게이트 등)은 검토 축이 아니다. 부재를 finding으로 만들지 않으며, 새로 끼어든 경우만 self-review 위임 사항으로 한 줄 언급.
- SSOT 폴더 구조·위치 감사는 `ssot-audit`, 발행은 `planning-publish-confluence` 담당.
