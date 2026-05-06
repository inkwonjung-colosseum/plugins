---
name: set-config
description: "product-team-kit 플러그인 전용 로컬 설정 `.product-team-kit/config.json`(outputRoot, ssot.include, ssot.exclude)을 대화형으로 생성·갱신한다. 'product-team-kit 설정 변경', 'plan-format/plan-review 출력 폴더 변경', 'SSOT corpus 범위 조정', 'config.json 만들기/수정' 같은 요청에서 호출. 각 키마다 현재 값(또는 default)을 제시하고 유지/직접입력을 선택받는다. 글로벌 Claude Code 설정(settings.json)은 update-config 사용."
argument-hint: "(인자 없음. 대화형 입력으로 키 값을 받는다)"
---

# set-config

`product-team-kit`의 로컬 설정 파일 `.product-team-kit/config.json`을 대화형으로 만들거나 갱신하는 스킬이다. 검증 규칙과 schema는 `../../references/config-contract.md`를 단일 기준으로 따른다. Python, Node.js, 별도 CLI helper 설치를 전제하지 않는다.

## 호출

- Claude Code: `/product-team-kit:set-config`
- Codex: `$set-config`

인자는 받지 않는다. 모든 입력은 대화형으로 수집한다.

## 역할 경계

- 본 skill은 `.product-team-kit/config.json`만 갱신한다. `<outputRoot>/` 산출물, Product Docs SSOT, 다른 설정 파일은 손대지 않는다.
- `plan-format`, `plan-review`의 동작 자체는 변경하지 않는다.
- 검증 거부값은 저장하지 않는다. runtime의 치명 설정 오류 또는 비치명 fallback 처리와 달리, 거부 사유를 보여주고 같은 키를 다시 입력받는다.
- 기존 config.json의 다른 키는 보존한다 (merge 동작).

## 동작 순서

1. config 위치 결정: `../../references/config-contract.md`의 root 결정 규칙으로 단일 위치 `.product-team-kit/config.json`을 확정한다. 인자 입력이 없으므로 cwd가 기준이다. cwd의 git root가 있으면 git root, 없으면 cwd를 사용한다.
2. 기존 config 로드: 파일이 있으면 표준 JSON 파싱으로 읽는다. 파싱 실패면 사용자에게 "기존 config 파싱 실패. 빈 상태에서 새로 만든다"를 알리고 빈 객체에서 시작한다. 파일이 없으면 빈 객체에서 시작한다.
3. effective seed 계산: 각 키마다 (현재값 if 존재 else default)를 시드로 만든다. `outputRoot` default는 `planning`. `ssot.include` default는 `Product Team Space/Product Department/Colonova Product/_AI_ 정책서 & 기능설계서/**/*.md`. `ssot.exclude` default는 미지정(키 없음).
4. 키별 대화형 입력을 다음 순서로 수행한다.
   - `outputRoot`
   - `ssot.include`
   - `ssot.exclude`
5. 각 키마다 AskUserQuestion으로 두 옵션을 제시한다.
   - 옵션 A label: `현재 값 유지: <시드 표기>` (시드가 default면 `default 유지: planning` 형식)
   - 옵션 B label: `다른 값 입력`
6. 옵션 A를 고르면 시드를 그대로 채택한다. 옵션 B를 고르면 일반 대화 prompt 한 번으로 새 값을 받는다. prompt 문구는 키별 안내(아래 키별 입력 형식)를 따른다.
7. 입력값을 `../../references/config-contract.md` 검증 규칙으로 검증한다. 거부되면 거부 사유 한 줄을 보여주고 같은 키에 대해 다시 옵션 A/B를 제시한다 (재입력 루프).
8. 모든 키 입력이 끝나면 변경 요약을 보여주고 AskUserQuestion으로 최종 저장 확인을 받는다.
   - 옵션 A: `저장`
   - 옵션 B: `취소`
9. `저장`이면 atomic write로 파일을 쓴다. `취소`면 파일을 변경하지 않고 종료한다.
10. 결과 출력 (아래 출력 포맷)을 반환한다.

## 키별 입력 형식

### `outputRoot`

- 안내 prompt: "초안 저장 root 폴더명을 입력해주세요. 단일 폴더명만 허용합니다 (예: `planning`, `drafts`)."
- 입력 정규화: 앞뒤 공백 제거.
- 검증: `../../references/config-contract.md`의 `outputRoot` 검증 규칙. 절대경로, `..`, 빈 문자열, 경로 구분자(`/`, `\`) 포함, 비문자열, null byte/제어문자 → 거부.
- 거부 메시지 예: `outputRoot: 절대경로(/etc)는 허용하지 않음. 단일 폴더명을 입력해주세요`.

### `ssot.include`

- 안내 prompt: "SSOT corpus allow-list glob을 입력해주세요. 여러 개면 줄바꿈 또는 콤마로 구분합니다. 기본 경로를 사용하려면 빈 입력으로 두면 됩니다 (기본: `Product Team Space/Product Department/Colonova Product/_AI_ 정책서 & 기능설계서/**/*.md`)."
- 입력 정규화: 줄바꿈/콤마로 split, 각 원소 trim, 빈 원소 제거.
- 결과가 빈 배열이면 키를 config에서 제거한다 (기본 SSOT include 경로 사용 의미).
- 결과가 1개 이상이면 `ssot.include`로 저장한다.
- 검증: 각 원소가 비어있지 않은 문자열. 비문자열은 발생하지 않음 (입력 자체가 텍스트).

### `ssot.exclude`

- 안내 prompt: "SSOT corpus 추가 제외 glob을 입력해주세요. 여러 개면 줄바꿈 또는 콤마로 구분합니다. 추가 제외가 없으면 빈 입력으로 두면 됩니다."
- 입력 정규화: 위와 동일.
- 결과가 빈 배열이면 키를 config에서 제거한다.
- 결과가 1개 이상이면 `ssot.exclude`로 저장한다.

## 저장

`version`은 항상 `1`로 고정 저장한다. 사용자에게 묻지 않는다.

config 객체 구성:

```json
{
  "version": 1,
  "outputRoot": "<확정값>",
  "ssot": {
    "include": ["..."],
    "exclude": ["..."]
  }
}
```

`outputRoot`이 default `planning`과 동일해도 항상 명시 저장한다 (effective config 추적성을 위해). `ssot.include`/`ssot.exclude`가 빈 배열이면 해당 sub-key를 제거한다. `ssot.include`가 제거되면 plan-review는 기본 SSOT include 경로를 사용한다. `ssot` 안의 sub-key가 모두 없으면 `ssot` 객체 자체를 제거한다.

저장은 atomic write로 수행한다.

1. 대상 폴더 `.product-team-kit/`이 없으면 만든다.
2. `.product-team-kit/config.json.tmp`에 직렬화된 JSON을 쓴다 (UTF-8, 2-space indent, 끝에 줄바꿈).
3. tmp write가 성공하면 `.product-team-kit/config.json`으로 rename한다.
4. tmp write 또는 rename 실패 시 best-effort cleanup 후 사용자 출력 `저장 실패`로 보고한다.

## 출력 포맷

### 저장 완료

```text
설정 저장 완료
- 경로: <project-root>/.product-team-kit/config.json
- version: 1

변경 요약:
- outputRoot: [기존값] -> [새값] (또는 변경 없음)
- ssot.include: [기존값] -> [새값] (또는 추가/삭제/변경 없음)
- ssot.exclude: [기존값] -> [새값]

다음 단계:
- 변경된 설정은 다음 plan-format / plan-review 호출부터 적용된다.
```

### 사용자 취소

```text
설정 변경 취소
- 경로: <project-root>/.product-team-kit/config.json
- 결과: 변경 사항 미반영. 기존 파일 유지.
```

### 저장 실패

```text
설정 저장 실패
- 경로: <project-root>/.product-team-kit/config.json
- 실패 단계: [tmp-write/rename/mkdir/cleanup]
- 남은 파일: [경로 또는 없음]
- 이유: [짧은 실패 사유]
- 복구 참고: [남은 tmp 파일 경로 또는 부모 폴더 권한 확인]
```

## 암묵 호출 라우팅

다음 의도에서는 `set-config`를 선택한다.

- `.product-team-kit/config.json`을 처음 만들거나 갱신하려는 경우
- `outputRoot` 또는 SSOT corpus 범위(`ssot.include`, `ssot.exclude`)를 바꾸려는 경우
- 설정 값을 직접 편집하지 않고 대화형으로 정하고 싶은 경우

다음 의도에서는 `set-config`를 선택하지 않는다.

- 기획 입력을 기능설계서/정책서로 변환하려는 경우 → `plan-format`
- 기존 초안을 발행 전 검토하려는 경우 → `plan-review`
- 현재 effective config만 확인하려는 경우 → `set-config`는 변경 흐름이므로 적합하지 않다. 사용자에게 직접 `.product-team-kit/config.json`을 읽어 확인하도록 안내한다.

## 규칙

- schema, 위치, 검증 규칙은 `../../references/config-contract.md`만 따른다.
- 검증 거부값은 저장하지 않고 같은 키에서 재입력 받는다.
- 기존 config의 다른 키는 보존한다.
- 저장은 atomic write다. 부분 저장 상태를 남기지 않는다.
- 사용자 입력 값에서 발견된 위험 문자(null byte, 제어문자)는 거부 사유로 명시한다.
- 비밀값/secret은 schema에 포함되지 않는다. 본 skill은 비밀값을 다루지 않는다.
