# Storage Contract

`plan-format`의 저장 위치, 안전기능명, timestamp, 파일 write 규칙이다. Python·Node.js·별도 CLI helper 설치를 전제하지 않는다.

저장 root 폴더명은 `../../../references/config-contract.md`의 `outputRoot`로 결정한다. default는 `planning`이며 본 문서의 `<outputRoot>` 표기는 그 값이다.

## 기능명과 안전기능명

기능명은 사용자에게 묻지 않고 입력 본문/파일명/디렉터리명에서 추출한다.

우선순위:

1. 문서 제목 또는 명시된 기능명
2. 반복 등장 `~ 기능` / `~ 정책` / `~ 화면` / 메뉴명
3. 파일명 또는 디렉터리명
4. 첫 핵심 명사구

확정 불가시 `기능정리`를 사용한다.

기능명은 안전기능명으로 정규화한다.

- Unicode NFC 정규화
- 앞뒤 공백 제거, 공백은 하이픈으로 변환
- `/`, `\`, `..`, 콜론, 따옴표, 와일드카드, 제어문자 제거 또는 하이픈 변환
- zero-width, bidi control, invisible control 제거
- 연속 하이픈 축약
- 길이 한도: 50자 이내, UTF-8 120 bytes 이내
- **char-boundary truncation**: byte 한도 초과 시 UTF-8 multi-byte char 경계 직전까지 round-down. 한 char가 byte 경계에서 쪼개지지 않도록 보장. 예: 한글 "기능정리관리화면" (24 bytes) + ... 형태에서 120 bytes 도달 직전 char 경계까지만 유지.
- 비어있으면 `기능정리`

## 저장 기준 루트

저장 기준 루트는 다음 순서로 정한다.

1. 파일/디렉터리 입력이면 해당 경로의 git root 또는 상위 프로젝트 루트
2. 프로젝트 루트를 식별할 수 없으면 입력 파일 또는 입력 디렉터리의 parent directory
3. 존재하지 않는 path-like 입력 또는 직접 텍스트 입력이면 현재 작업 디렉터리

Product Docs SSOT 후보 폴더 자체에는 직접 쓰지 않고, 해당 문서를 포함한 git root 또는 현재 작업 디렉터리 아래 `<outputRoot>/`을 사용한다.

## 저장 경로

```
<outputRoot>/[안전기능명]--YYYY-MM-DD-HHMMSS/[안전기능명]_기능설계서.md
<outputRoot>/[안전기능명]--YYYY-MM-DD-HHMMSS/[안전기능명]_정책서.md
```

`Asia/Seoul` timestamp로 새 폴더를 확보한다. 폴더명 구분자는 안전기능명·timestamp 사이, timestamp·collision suffix 사이 모두 **이중 대시 `--`** 로 통일한다. 안전기능명은 안전화 단계에서 연속 대시가 단일 대시로 축약되므로(`## 기능명과 안전기능명` 참조) 안전기능명에 `--`이 등장할 수 없어 구분자와 충돌하지 않는다.

## Collision suffix

폴더명 충돌 시 `--01`, `--02`, ..., `--99` suffix를 timestamp **뒤에** 순차로 붙여 시도한다. 최종 폴더명은 `[안전기능명]--YYYY-MM-DD-HHMMSS--NN` 형태다 (예: `결제승인--2026-05-07-103045--01`). `--99`까지 모두 충돌하면 `references/output-contract.md`의 "저장 실패" 템플릿(`실패 단계: folder`)을 반환한다. 같은 timestamp 단위로 99회 이상 호출은 비정상 사용으로 간주한다.

## 기존 산출물

입력 디렉터리에 기존 `[안전기능명]_기능설계서.md` 또는 `[안전기능명]_정책서.md`가 있어도 저장 보류 사유가 아니다. 참고 입력으로만 읽고 덮어쓰지 않는다. 새 timestamp 폴더 + collision suffix 사용으로 정상 실행은 기존 final 파일 때문에 hold되지 않는다.

선택된 target folder가 이미 있으면 race 또는 이전 실패 잔여물로 보고 덮어쓰지 않는다. 다음 collision suffix를 시도하고, `--99`까지 모두 충돌하면 "저장 실패" 템플릿(`실패 단계: folder`)을 반환한다.

## 저장 절차

두 문서는 하나의 저장 단위로 취급한다. final 파일은 staging folder 안에 먼저 쓰고, 두 파일 검증이 끝난 뒤 staging folder 전체를 target folder로 rename한다.

1. 안전기능명·timestamp로 target folder 경로 결정. 충돌 시 collision suffix 적용 (위 규칙).
2. target folder와 같은 parent 아래에 숨김 staging folder를 생성한다. staging folder 예: `<outputRoot>/.tmp-[안전기능명]--YYYY-MM-DD-HHMMSS` (collision suffix 적용 시 `<outputRoot>/.tmp-[안전기능명]--YYYY-MM-DD-HHMMSS--NN`). 생성 실패 시 "저장 실패" (`실패 단계: folder`).
3. staging folder 안에 `[안전기능명]_기능설계서.md`와 `[안전기능명]_정책서.md`를 final 파일명 그대로 쓴다. 두 파일 Write 툴 호출은 단일 메시지에 동시 발행한다 (병렬). 둘 중 하나라도 write 실패 시 target folder는 만들지 않고 staging folder를 best-effort cleanup한 뒤 "저장 실패" (`실패 단계: write`)를 반환한다.
4. staging folder 안에 두 파일이 모두 존재하고 target folder가 여전히 존재하지 않는지 검증한다. 검증 실패 시 staging folder를 best-effort cleanup한 뒤 "저장 실패" (`실패 단계: verify`)를 반환한다.
5. staging folder를 target folder로 rename한다. rename 실패 시 staging folder를 best-effort cleanup한 뒤 "저장 실패" (`실패 단계: rename`)를 반환한다.
6. rename 후 target folder에 두 final 파일이 모두 존재하고 staging folder가 남아 있지 않은지 검증한다. 실패 시 "저장 실패" (`실패 단계: verify`)를 반환한다.
7. 저장 완료 성공 조건: target folder에 두 final 파일이 모두 존재하고 staging folder가 남아 있지 않음.

cleanup 실패나 애매한 rename 실패로 파일 또는 폴더가 남으면 "저장 실패" 출력의 `남은 파일 또는 폴더`에 반드시 노출한다. 정상 실패는 target folder 아래에 한쪽 문서만 남기지 않아야 한다.

## Config 검증

`<outputRoot>` 값이 config-contract 검증에서 거부되는 경우 strict-exit 사유다 (`../SKILL.md` `## 1. 설정 확인`). 본 contract에 도달하기 전에 `output-contract.md`의 "설정 없음" 템플릿으로 종료된다.

비치명 검증 거부 (unknown key, ssot 배열 element 비문자열 등)는 default fallback + `[설정 경고]`로 처리되어 본 contract 단계까지 도달한다. 이 경우 fallback된 값을 그대로 사용한다.

## SSOT 경계

저장된 초안은 `plan-review`의 검토 대상이지 Product Docs SSOT 근거가 아니다. `<outputRoot>/` 하위 파일은 후속 검토에서 SSOT corpus에서 제외된다.
