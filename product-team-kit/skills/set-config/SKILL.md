---
name: set-config
description: "Use when a user wants to create or update product-team-kit local settings, change outputRoot, adjust Product Docs SSOT include/exclude globs, or refresh CLAUDE.md/AGENTS.md guidance for plan-format/plan-review. Do not use for global Claude Code settings."
argument-hint: "(인자 없음. 대화형 입력으로 키 값을 받는다)"
---

# set-config

`product-team-kit`의 로컬 설정 파일 `.product-team-kit/config.json`을 대화형으로 만들거나 갱신하고, 같은 프로젝트 루트의 `CLAUDE.md`와 `AGENTS.md`에 product-team-kit 안내 블록을 항상 생성·갱신하는 스킬이다. 검증 규칙과 schema는 `../../references/config-contract.md`를 단일 기준으로 따른다. Python, Node.js, 별도 CLI helper 설치를 전제하지 않는다.

## 호출

- Claude Code: `/product-team-kit:set-config`
- Codex: `$set-config`

인자는 받지 않는다. 모든 입력은 대화형으로 수집한다.

## 대화형 질문 원칙

- `AskUserQuestion` 또는 Codex Plan mode의 사용자 입력 도구를 사용할 수 있으면 우선 사용한다.
- 질문 도구가 없으면 일반 대화 메시지 **한 번**으로 `outputRoot`, `ssot.include`, `ssot.exclude`의 현재값 유지/다른 값 입력 선택지를 함께 제시하고 응답을 기다린다. 도구가 없다는 이유로 기본값을 추정 저장하지 않는다.
- 사용자가 취소 의사를 밝히거나 저장 확인에서 `취소`를 고르면 파일을 변경하지 않는다.

## 역할 경계

- 본 skill은 `.product-team-kit/config.json`과 프로젝트 루트의 `CLAUDE.md`, `AGENTS.md` 안 product-team-kit 관리 블록만 갱신한다. `<outputRoot>/` 산출물, Product Docs SSOT, 그 외 설정 파일은 손대지 않는다.
- `CLAUDE.md`와 `AGENTS.md`는 사용자에게 별도 선택을 묻지 않고 항상 생성·갱신한다. 기존 파일 전체를 덮어쓰지 않고 `<!-- product-team-kit:start -->` / `<!-- product-team-kit:end -->` 사이 관리 블록만 replace하거나 append한다.
- `plan-format`, `plan-review`의 동작 자체는 변경하지 않는다.
- 검증 거부값은 저장하지 않는다. runtime의 치명 설정 오류 또는 비치명 fallback 처리와 달리, 거부 사유를 보여주고 거부된 키만 다시 입력받는다.
- 기존 config.json의 unknown key와 기존 `CLAUDE.md`/`AGENTS.md`의 관리 블록 밖 사용자 내용은 보존한다.

## 동작 순서

1. config 위치 결정: `../../references/config-contract.md`의 root 결정 규칙으로 단일 위치 `.product-team-kit/config.json`을 확정한다. 인자 입력이 없으므로 cwd가 기준이다. cwd의 git root가 있으면 git root, 없으면 cwd를 사용한다.
2. 기존 config 로드: 파일이 있으면 표준 JSON 파싱으로 읽는다. 파싱 실패면 사용자에게 "기존 config 파싱 실패. 빈 상태에서 새로 만든다"를 알리고 빈 객체에서 시작한다. 파일이 없으면 빈 객체에서 시작한다.
3. effective seed 계산: 각 키마다 (현재값 if 존재 else default)를 시드로 만든다. `outputRoot` default는 `planning`. `ssot.include` default는 `Product Team Space/Product Department/Colonova Product/_AI_ 정책서 & 기능설계서/**/*.md`. `ssot.exclude` default는 미지정(키 없음).
4. 다음 3개 키를 **한 번의 AskUserQuestion 호출에 묶어** 동시에 묻는다. 키별로 따로 호출하지 않는다.
   - `outputRoot`
   - `ssot.include`
   - `ssot.exclude`
5. 단일 AskUserQuestion 호출에 questions 배열로 3개 question을 전달한다. 질문 도구가 없으면 같은 내용을 일반 대화 prompt 하나로 제시한다. 각 question은 두 옵션을 가진다.
   - 옵션 A label: `현재 값 유지: <시드 표기>` (시드가 default면 `default 유지: planning` 형식)
   - 옵션 B label: `다른 값 입력`
   - question 텍스트는 키별 안내(아래 키별 입력 형식)의 prompt 문구를 사용한다.
   - header는 `outputRoot`, `ssot.include`, `ssot.exclude` 등 키 이름(12자 이내)으로 한다.
6. 응답 처리:
   - 옵션 A를 고른 키는 시드를 그대로 채택한다.
   - 옵션 B를 고른 키들에 대해서만 일반 대화 prompt로 새 값을 받는다. B를 고른 키가 여러 개면 prompt 한 번으로 키별 줄 분리해서 한꺼번에 받는다 (예: `outputRoot: <값>` 형식, 줄바꿈 구분). B가 1개면 단일 prompt 한 번.
7. 받은 값들을 `../../references/config-contract.md` 검증 규칙으로 일괄 검증한다. 거부된 키들만 모아 거부 사유를 한꺼번에 보여주고, 거부된 키들에 대해서만 다시 단일 AskUserQuestion으로 옵션 A/B를 batch 제시한다 (재입력 루프).
8. 모든 키 입력이 끝나면 저장 전 자체 점검을 수행한다: project root와 대상 경로가 확정됐는지, `outputRoot`가 검증 통과했는지, `ssot.include`/`ssot.exclude`가 배열 또는 제거 상태인지, `version`이 `1`인지, 검증 거부값이 남아 있지 않은지 확인한다. 실패하면 저장하지 않고 거부 사유를 재입력 루프로 돌린다.
9. 변경 요약을 보여주고 AskUserQuestion으로 최종 저장 확인을 받는다. 질문 도구가 없으면 일반 대화 prompt로 `저장`/`취소`만 묻는다.
   - 옵션 A: `저장`
   - 옵션 B: `취소`
10. `저장`이면 `.product-team-kit/config.json`을 atomic write로 쓴다. `취소`면 파일을 변경하지 않고 종료한다.
11. config write가 성공하면 프로젝트 루트의 `CLAUDE.md`와 `AGENTS.md`를 순서대로 upsert한다. 두 파일 모두 항상 처리하며 사용자에게 별도 생성 여부를 묻지 않는다.
12. 결과 출력 (아래 출력 포맷)을 반환한다.

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

저장 객체는 기존 config JSON object를 base로 삼아 merge한다. 기존 파일 파싱에 실패했거나 기존 값이 object가 아니면 빈 object를 base로 한다.

- `version`은 항상 `1`로 덮어쓴다.
- `outputRoot`은 default `planning`과 동일해도 항상 명시 저장한다 (effective config 추적성을 위해).
- 기존 top-level unknown key는 보존한다.
- 기존 `ssot`가 object면 unknown sub-key를 보존하고, object가 아니면 새 object로 대체한다.
- `ssot.include`/`ssot.exclude`가 빈 배열이면 해당 managed sub-key를 제거한다. `ssot.include`가 제거되면 plan-review는 기본 SSOT include 경로를 사용한다.
- managed sub-key 제거 후 `ssot` 안에 보존할 sub-key가 하나도 없으면 `ssot` 객체 자체를 제거한다.

config 저장은 atomic write로 수행한다.

1. 대상 폴더 `.product-team-kit/`이 없으면 만든다.
2. `.product-team-kit/config.json.tmp`에 직렬화된 JSON을 쓴다 (UTF-8, 2-space indent, 끝에 줄바꿈).
3. tmp write가 성공하면 `.product-team-kit/config.json`으로 rename한다.
4. tmp write 또는 rename 실패 시 best-effort cleanup 후 사용자 출력 `저장 실패`로 보고한다.

## Agent 안내 파일

config 저장 성공 후 프로젝트 루트에 `CLAUDE.md`와 `AGENTS.md`를 항상 생성·갱신한다. `AGENT.md` 단수 파일은 만들지 않는다.

각 파일은 같은 product-team-kit 관리 블록을 가진다.

```markdown
<!-- product-team-kit:start -->
## product-team-kit

- 이 프로젝트는 product-team-kit을 사용한다.
- Product Docs SSOT 범위는 `.product-team-kit/config.json`의 `ssot.include`를 우선한다.
- SSOT 탐색 시 `ssot.exclude`, 기본 제외 경로, `<outputRoot>/**` 제외를 함께 적용한다.
- `<outputRoot>/` 아래 기능설계서/정책서 산출물은 로컬 초안이며 검토 대상일 수 있지만 Product Docs SSOT 근거로 사용하지 않는다.
- 제품 정책, PRD/요구사항, 기능/화면 설계, 운영/QA 판단 Markdown을 기준 문서로 우선 읽는다.
- 외부 URL, 코드, 설정 파일, 빌드 산출물, dependency/vendor/cache/generated 경로는 Product Docs SSOT 근거로 사용하지 않는다.
- 초안 생성은 `/product-team-kit:plan-format` 또는 `$plan-format`, 발행 전 검토는 `/product-team-kit:plan-review` 또는 `$plan-review`를 사용한다.
<!-- product-team-kit:end -->
```

Upsert 규칙:

1. 파일이 없으면 위 블록만 포함해 새로 만든다.
2. 파일이 있고 관리 블록이 있으면 start/end marker 사이만 새 내용으로 교체한다.
3. 파일이 있고 관리 블록이 없으면 파일 끝에 빈 줄 2개 뒤 위 블록을 append한다.
4. start marker만 있거나 end marker만 있으면 파일을 임의 복구하지 않는다. 해당 파일은 변경하지 않고 `agent-guide-write` 실패로 보고한다.
5. 각 파일은 `<파일명>.tmp`에 쓴 뒤 rename하는 방식으로 atomic write한다.

## 출력 포맷

### 저장 완료

```text
설정 저장 완료
- 경로: <project-root>/.product-team-kit/config.json
- version: 1
- agent 안내 파일:
  - <project-root>/CLAUDE.md: [생성/갱신]
  - <project-root>/AGENTS.md: [생성/갱신]

변경 요약:
- outputRoot: [기존값] -> [새값] (또는 변경 없음)
- ssot.include: [기존값] -> [새값] (또는 추가/삭제/변경 없음)
- ssot.exclude: [기존값] -> [새값] (또는 추가/삭제/변경 없음)

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
- 실패 단계: [tmp-write/rename/mkdir/cleanup/agent-guide-write]
- 남은 파일: [경로 또는 없음]
- 이유: [짧은 실패 사유]
- 복구 참고: [남은 tmp 파일 경로, 부모 폴더 권한, 또는 CLAUDE.md/AGENTS.md 관리 블록 marker 확인]
```

## 암묵 호출 라우팅

다음 의도에서는 `set-config`를 선택한다.

- `.product-team-kit/config.json`과 프로젝트 agent 안내 파일을 처음 만들거나 갱신하려는 경우
- `outputRoot` 또는 SSOT corpus 범위(`ssot.include`, `ssot.exclude`)를 바꾸려는 경우
- 설정 값을 직접 편집하지 않고 대화형으로 정하고 싶은 경우

다음 의도에서는 `set-config`를 선택하지 않는다.

- 기획 입력을 기능설계서/정책서로 변환하려는 경우 → `plan-format`
- 기존 초안을 발행 전 검토하려는 경우 → `plan-review`
- 현재 effective config만 확인하려는 경우 → `set-config`는 변경 흐름이므로 적합하지 않다. 사용자에게 직접 `.product-team-kit/config.json`을 읽어 확인하도록 안내한다.

## 규칙

- schema, 위치, 검증 규칙은 `../../references/config-contract.md`만 따른다.
- 검증 거부값은 저장하지 않고 거부된 키만 재입력 받는다.
- 저장 확인 전 자체 점검을 통과하지 못하면 파일을 쓰지 않는다.
- 기존 config의 unknown key와 `CLAUDE.md`/`AGENTS.md`의 관리 블록 밖 사용자 내용은 보존한다.
- 각 파일 write는 atomic write다. config 저장 성공 후 agent 안내 파일 갱신 중 실패하면 실패 파일은 변경하지 않고 `agent-guide-write` 실패로 보고한다.
- config 저장이 성공하면 `CLAUDE.md`와 `AGENTS.md` product-team-kit 관리 블록은 선택 없이 항상 생성·갱신한다.
- 사용자 입력 값에서 발견된 위험 문자(null byte, 제어문자)는 거부 사유로 명시한다.
- 비밀값/secret은 schema에 포함되지 않는다. 본 skill은 비밀값을 다루지 않는다.
