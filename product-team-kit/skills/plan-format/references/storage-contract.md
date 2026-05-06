# Storage Contract

`plan-format`의 저장 위치, 안전기능명, timestamp, two-file write는 이 계약을 따른다. Python, Node.js, 별도 CLI helper 설치를 전제하지 않는다.

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
- 50자, UTF-8 120 bytes 이내 절단
- 비어있으면 `기능정리`

## 저장 기준 루트

저장 기준 루트는 다음 순서로 정한다.

1. 파일/디렉터리 입력이면 해당 경로의 git root 또는 상위 프로젝트 루트
2. 프로젝트 루트를 식별할 수 없으면 입력 파일 또는 입력 디렉터리의 parent directory
3. 존재하지 않는 path-like 입력 또는 직접 텍스트 입력이면 현재 작업 디렉터리

Product Docs SSOT 후보 폴더 자체에는 직접 쓰지 않고, 해당 문서를 포함한 git root 또는 현재 작업 디렉터리 아래 `planning/`을 사용한다.

## 저장 경로

일반 입력 저장 경로:

- `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/[안전기능명]_기능설계서.md`
- `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/[안전기능명]_정책서.md`

`Asia/Seoul` timestamp로 새 폴더를 확보한다. 폴더명이 충돌하면 `--01`, `--02` suffix를 사용한다.

## 기존 산출물과 target precheck

입력 디렉터리에 기존 `[안전기능명]_기능설계서.md` 또는 `[안전기능명]_정책서.md`가 있어도 저장 보류 사유가 아니다. 이 파일들은 참고 입력으로만 읽고 덮어쓰지 않는다.

새 timestamp 폴더와 collision suffix를 사용하므로 정상 실행은 기존 final 파일 때문에 hold되지 않는다. 선택된 target folder에 final 파일이 이미 있으면 race 또는 partial artifact로 보고 `output-contract.md`의 저장 실패 템플릿에 `precheck` 또는 `verify` 실패로 기록한다.

## two-file 저장 단위

두 문서는 하나의 저장 단위로 취급한다.

1. 같은 대상 폴더에 `[안전기능명]_기능설계서.md.tmp`, `[안전기능명]_정책서.md.tmp`를 쓴다.
2. tmp write 전 target final 파일이 없어야 한다. 이미 있으면 덮어쓰지 않고 `precheck` 저장 실패를 반환한다.
3. 두 tmp write가 모두 성공하기 전에는 final 파일명으로 rename하지 않는다.
4. tmp write 또는 rename 실패 시 best-effort cleanup 후 저장 실패 출력을 반환한다.
5. 저장 완료 성공 조건은 두 final 파일 존재와 남은 tmp 파일 0개다.
6. cleanup 실패나 partial artifact가 있으면 남은 경로를 저장 실패 출력에 반드시 남긴다.

저장된 초안은 `plan-review`의 검토 대상이지 Product Docs SSOT 근거가 아니다. `planning/` 하위 파일은 후속 검토에서 SSOT corpus에서 제외된다.
