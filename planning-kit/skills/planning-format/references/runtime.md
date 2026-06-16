# Runtime

dispatch, 입력, 수집, 저장, 출력 계약을 한곳에 둔다. `SKILL.md`가 유일한 메타·트리거 소스다.

## 입력

필수 위치 인자: 텍스트, 파일 경로, 디렉터리 경로, 이미지 경로, 또는 하나 이상의 `https?://` URL.

옵션:

- `--save`: 기본값/별칭(no-op).
- `--no-save`: 파일을 쓰지 않고 본문을 출력.
- `--no-fetch`: URL fetch와 connector fallback 생략.
- `--no-image`: 이미지 해석 생략.
- `--no-self-review`: 자가검증만 생략. 제외 추적과 출력 형태는 유지.

## Dispatch

1. 모든 토큰이 `https?://` URL → URL 모드.
2. 디렉터리 경로 → 디렉터리 모드.
3. 파일 경로 → 파일 모드.
4. 그 외 → 텍스트 모드.

URL과 비-URL 토큰이 섞이면 텍스트 모드. `file://`, `ftp://`, `mailto:`, 스킴 없는 문자열은 URL 모드가 아니다.

## Sequence

1. 입력 dispatch.
2. 병합 텍스트·이미지 시드·URL 시드가 모두 비면 그때만 거부.
3. 모든 모드에서 링크/이미지 수집.
4. `--no-fetch`가 아니면 URL 본문을 BFS로 fetch.
5. `--no-image`가 아니면 이미지 해석.
6. 소스 병합.
7. 두 템플릿으로 정책서·기능설계서 생성 (`conversion.md`).
8. 제외 추적 (`conversion.md`).
9. `--no-self-review`가 아니면 자가검증 (`self-review.md`).
10. `--no-save`가 아니면 저장.
11. 출력 계약 방출.

## URL 수집 / connector

- `--no-fetch`가 아니면 dequeue된 모든 `https?://` URL을 먼저 직접 fetch.
- 비공개로 보여도 건너뛰지 말고 시도한 뒤 실패를 기록.
- BFS 순회. 정규화 후 visited 집합으로 사이클 방지. 깊이·크기 제한 없음.
- `mailto:`, `tel:`, `javascript:`, `blob:`, self anchor, 스킴 없는 문자열 무시.
- connector는 직접 fetch가 막히거나 비거나 인증 필요일 때만 쓴다: Atlassian(Confluence/Jira), Google Drive(Docs/Sheets/Slides/Drive), Gmail·Slack·Calendar(URL 호스트와 작업이 명확히 일치할 때), Browser/Chrome(로그인 렌더링이 필요하고 connector 텍스트가 없을 때).
- dequeue된 URL마다 출처 행 1개: URL / status(success·auth required·timeout·4xx·5xx·unsupported·empty) / body used(yes·no) / note. Google Sheets는 `gid`·범위를 note에 포함.

## 저장

기본은 저장. `--save`는 호환 no-op. `--no-save`만 저장을 끈다. 저장 위치 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/`. 충돌은 `--2`, `--3` 등으로 해소.

## 출력 계약

최종 출력은 산출물 핸드오프지 실행 로그가 아니다. `# [기능명]`으로 시작.

헤더:

- 입력: 사람이 읽을 출처 요약
- 산출물: 정책서, 기능설계서
- 검증: 확인 필요 N건, 문서 보강 M건, 출처 누락 K건 / 확인 필요 없음 / 생략 (--no-self-review)
- 저장: `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` / `없음 (--no-save)` / `실패 - 사유`

저장 성공: 헤더 → `## 저장 파일` → `## 체크해야 할 항목`만 보여준다. 본문 미출력.

`--no-save`: 헤더 → `## 정책서` → `## 기능설계서` → `## 체크해야 할 항목`.

저장 실패: no-save 본문 + `## 저장 실패 상세`(실패 단계·대상 경로·남은 파일/폴더).

체크리스트 하위 순서: `### 결정 필요`, `### 문서 보강 필요`, `### 출처/누락 참고`. 빈 값은 `없음`. 항목 형식 — 확인할 것 / 이유 / 반영 위치. 요구사항 ID가 있으면 반영 위치에 `POL-XXX` 또는 `FUNC-XXX`만 표기한다.

## 경계

- `planning/**` 산출물은 나중에 검토·발행될 수 있으나 SSOT 근거로 치지 않는다.
- SSOT 충돌, 수용 기준, 의존성 영향은 `planning-review` 담당.
- 저장 실패는 중단 조건이 아니다. 전체 본문 + 실패 상세를 출력한다.
