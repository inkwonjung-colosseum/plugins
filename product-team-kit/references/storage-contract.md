# Storage Contract

`plan-draft`와 `plan-format`은 저장 위치, 안전기능명, timestamp, atomic write, 충돌 처리를 이 계약으로 판단한다.

## 기능명과 안전기능명

기능명은 사용자에게 묻지 않고 입력 본문/파일명에서 추출한다.

우선순위:

1. 문서 제목 또는 명시된 기능명
2. 반복 등장 `~ 기능` / `~ 정책` / `~ 화면` / 메뉴명
3. 파일명
4. 첫 핵심 명사구

확정 불가시 `기획초안`을 사용한다.

저장 경로용 안전기능명 정규화:

- Unicode NFC 정규화
- 앞뒤 공백 제거, 공백은 하이픈으로 변환
- `/`, `\`, `..`, 콜론, 따옴표, 와일드카드, 줄바꿈, 제어문자는 제거 또는 하이픈으로 변환
- zero-width, bidi control, invisible control 제거
- 연속 하이픈은 단일 하이픈으로 축약
- grapheme 기준 50자 이내로 자름
- UTF-8 120 bytes 이내로 자름
- 절단 후 다시 앞뒤 하이픈 제거와 연속 하이픈 단일화
- 비어있으면 `기획초안`

새 timestamp 폴더를 만들 때는 전체 directory component가 timestamp와 optional `--NN` suffix를 포함해 파일시스템 component limit 안에 들어오도록 안전기능명을 더 짧게 자른다.

## 저장 기준 루트

`plan-draft` 저장 기준 루트 우선순위:

1. 사용자가 명시한 로컬 프로젝트 디렉터리
2. 파일 입력이면 해당 파일의 git root 또는 상위 프로젝트 루트
3. 프로젝트 루트를 식별할 수 없으면 입력 파일의 parent directory
4. 그 외 현재 작업 디렉터리

`plan-format` 저장 기준 루트 우선순위:

1. `plan-draft` 산출 기획초안 입력이면 해당 기획초안의 parent folder
2. 일반 파일 입력이면 해당 파일의 git root 또는 상위 프로젝트 루트
3. 프로젝트 루트를 식별할 수 없으면 입력 파일의 parent directory
4. 직접 텍스트 입력이면 현재 작업 디렉터리

Project Docs SSOT 근거 후보 폴더 자체에는 저장하지 않는다. 입력 파일 parent가 Project Docs SSOT 후보 폴더 자체이면 해당 폴더에 직접 쓰지 않고, 해당 문서를 포함한 git root 또는 현재 작업 디렉터리의 `planning/` 아래를 저장 기준으로 둔다.

## `plan-draft` 저장

저장 경로:

```text
planning/[안전기능명]--YYYY-MM-DD-HHMMSS/[안전기능명]_기획초안.md
```

위 경로는 저장 기준 루트 아래의 상대 경로다. 출력에는 실제 생성 경로를 사용한다.

timestamp는 저장 직전 `TZ=Asia/Seoul date +%Y-%m-%d-%H%M%S`로 획득한다. 실패시 고정값을 쓰지 않고 `초안 충분하지만 저장 실패`를 반환한다.

대상 폴더는 atomic `mkdir` 성공을 기준으로 확보한다. 대상 폴더가 이미 있으면 덮어쓰지 않는다. timestamp를 재생성해 새 폴더명을 만들고, 그래도 충돌하면 `--01`/`--02` suffix를 붙인다.

파일은 먼저 같은 대상 폴더의 임시 파일에 쓰고 최종 파일명으로 rename한다. mkdir, write, rename 중 하나라도 실패하면 저장 완료를 출력하지 않는다. 부분 파일이나 빈 폴더가 남을 수 있으면 출력에 시도 경로와 저장 실패 사유를 남긴다.

재실행은 새 timestamp snapshot을 만든다. 기존 파일은 덮어쓰지 않는다.

## `plan-format` 저장

두 문서는 하나의 two-file 저장 단위로 취급한다. 저장 위치와 충돌 처리는 이 단계만 권위로 삼는다.

저장 위치:

- `plan-draft` 산출 기획초안 입력인 경우 새 timestamp 폴더를 만들지 않고 같은 parent folder에 `[안전기능명]_기능설계서.md`, `[안전기능명]_정책서.md`를 저장한다.
- 그 외 직접 붙여넣기, 일반 메모 파일, 다른 경로의 입력 파일, AI 대화 결과물, 문서 스크랩은 저장 기준 루트 아래 새 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 폴더를 만든다.

저장된 초안은 `plan-review`의 검토 대상이지 Project Docs SSOT 근거가 아니다. `planning/` 하위 파일은 후속 검토에서 SSOT corpus에서 제외된다. 기능설계서와 정책서는 로컬 초안 템플릿이며 공식 팀 문서가 아니다. 팀 문서 히스토리는 반영 이후 관리한다.

일반 입력 저장 경로:

- `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/[안전기능명]_기능설계서.md`
- `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/[안전기능명]_정책서.md`

timestamp는 저장 직전 `TZ=Asia/Seoul date +%Y-%m-%d-%H%M%S`로 획득한다. 실패시 고정값을 쓰지 않고 `저장 실패`를 반환한다.

새 timestamp 폴더를 만들 때는 atomic `mkdir` 성공을 기준으로 확보한다. 대상 폴더가 이미 있으면 덮어쓰지 않는다. timestamp를 재생성해 새 폴더명을 만들고, 그래도 충돌하면 `--01`/`--02` suffix를 붙인다. `plan-draft` 기획초안 폴더를 재사용할 때는 새 `mkdir`를 요구하지 않고 기존 final 파일 precheck를 먼저 수행한다.

기존 final 파일 precheck:

- 저장 전 대상 폴더에 `[안전기능명]_기능설계서.md` 또는 `[안전기능명]_정책서.md` final 파일이 하나라도 있으면 tmp write 전에 `기존 산출물 존재 저장 보류`를 반환한다.
- cleanup은 이 precheck 이전부터 존재하던 final 파일을 삭제하지 않는다.

two-file 저장 단위 절차:

1. 같은 대상 폴더에 `[안전기능명]_기능설계서.md.tmp`, `[안전기능명]_정책서.md.tmp`를 각각 쓴다.
2. 두 tmp write가 모두 성공하기 전에는 final 파일명으로 rename하지 않는다.
3. tmp write 중 하나라도 실패하면 생성된 tmp 파일은 best-effort로 삭제하고 `저장 실패`를 반환한다.
4. final rename은 단일 실행 흐름에서 수행한다. 순서: 기능설계서 tmp -> 기능설계서 final, 정책서 tmp -> 정책서 final.
5. rename 중 하나라도 실패하면 저장 완료를 출력하지 않는다. 이미 rename된 final 또는 남은 tmp가 있으면 best-effort cleanup을 시도한다.
6. cleanup 실패로 partial artifact가 남을 수 있으면 해당 경로를 출력에 반드시 남긴다.

저장 완료 성공 조건:

- `[안전기능명]_기능설계서.md` final 파일 존재
- `[안전기능명]_정책서.md` final 파일 존재
- 남은 tmp 파일 없음

`plan-draft` 산출 기획초안 입력이 아닌 재실행은 새 timestamp snapshot을 만든다. `plan-draft` 기획초안 폴더를 재사용하는 경우 기존 파일은 덮어쓰지 않는다.

`plan-format`이 draft artifact input을 정보 부족으로 판정하는 경우에도 저장 경로와 atomic write 규칙은 바꾸지 않는다. 이 경우 저장을 시도하지 않고 `rerun-contract.md`의 `format-after-draft-insufficient` terminal hold를 따른다.
