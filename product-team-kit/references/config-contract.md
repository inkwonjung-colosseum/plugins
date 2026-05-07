# Config Contract

`product-team-kit`의 `set-config`, `plan-format`, `plan-review`가 공통으로 따르는 로컬 설정 계약이다. Python, Node.js, 별도 CLI helper 설치를 전제하지 않는다. 설정 파일은 일반 JSON이며 표준 JSON 파싱으로 읽는다. `set-config`는 이 설정을 저장한 뒤 같은 프로젝트 루트의 `CLAUDE.md`와 `AGENTS.md` product-team-kit 안내 블록도 항상 생성·갱신한다.

## 위치

- 파일 경로: `<project-root>/.product-team-kit/config.json`
- agent 안내 파일 경로: `<project-root>/CLAUDE.md`, `<project-root>/AGENTS.md`
- `<project-root>` 결정 규칙은 `skills/plan-format/references/storage-contract.md`의 "저장 기준 루트"와 같다.
  1. 파일/디렉터리 입력이면 해당 경로의 git root 또는 상위 프로젝트 루트
  2. 프로젝트 루트를 식별할 수 없으면 입력 파일 또는 입력 디렉터리의 parent directory
  3. 존재하지 않는 path-like 입력 또는 직접 텍스트 입력이면 현재 작업 디렉터리
- walk-up 검색은 하지 않는다. 위에서 결정된 단일 root만 확인한다.
- `plan-format`과 `plan-review`는 config 파일이 없으면 즉시 실패한다. `set-config`만 이 파일을 새로 만들 수 있으며, config 저장 성공 후 `CLAUDE.md`와 `AGENTS.md` 안내 블록을 선택 없이 항상 upsert한다.

## Agent 안내 파일

`CLAUDE.md`와 `AGENTS.md`는 config schema가 아니며 `plan-format`/`plan-review`의 runtime source of truth도 아니다. 두 파일은 일반 agent가 프로젝트를 열었을 때 Product Docs SSOT 위치를 먼저 읽도록 돕는 로컬 안내 파일이다.

`set-config`는 config 저장 성공 후 두 파일을 모두 처리한다. 사용자에게 생성 여부를 묻지 않는다.

- 파일이 없으면 product-team-kit 관리 블록만 포함해 새로 만든다.
- 기존 `<!-- product-team-kit:start -->` / `<!-- product-team-kit:end -->` 블록이 있으면 그 블록만 교체한다.
- 관리 블록이 없으면 파일 끝에 append한다.
- start marker 또는 end marker가 하나만 있으면 해당 파일은 변경하지 않고 `agent-guide-write` 실패로 보고한다.
- 관리 블록은 `.product-team-kit/config.json`의 `ssot.include`, `ssot.exclude`, `<outputRoot>/**` 제외, Product Docs SSOT 경계를 우선 확인하라고 안내한다.

## Schema

```json
{
  "version": 1,
  "outputRoot": "planning",
  "ssot": {
    "include": ["Product Team Space/Product Department/Colonova Product/_AI_ 정책서 & 기능설계서/**/*.md"],
    "exclude": ["planning/**", "**/node_modules/**"]
  }
}
```

| Key | 타입 | default | 사용 skill | 의미 |
| --- | --- | --- | --- | --- |
| `version` | integer | (필수, 현재 `1`) | 세 skill | schema 버전. runtime 미일치 시 `plan-format`과 `plan-review`는 즉시 실패하고, `set-config`는 항상 1 저장 |
| `outputRoot` | string | `planning` | `set-config`, `plan-format`, `plan-review` | 초안 저장 root 폴더명. `plan-review` SSOT exclude 자동 추가에 사용 |
| `ssot.include` | string array | `["Product Team Space/Product Department/Colonova Product/_AI_ 정책서 & 기능설계서/**/*.md"]` | `set-config`, `plan-review` | SSOT corpus allow-list glob. 미지정/빈 배열이면 Product Team Space의 `_AI_ 정책서 & 기능설계서` Markdown을 기본 근거로 사용 |
| `ssot.exclude` | string array | (없음) | `set-config`, `plan-review` | SSOT corpus 추가 제외 glob. 기존 default 제외에 누적. `<outputRoot>/**`은 항상 자동 포함 |

위 표 외 키는 모두 unknown key다.

## 우선순위

CLI 인자 > `.product-team-kit/config.json` > 본 contract와 각 skill contract의 default.

## 검증 규칙

설정값은 아래 기준으로 검증한다. `plan-format`과 `plan-review`는 치명 설정 오류가 있으면 이후 단계를 수행하지 않고 즉시 실패한다. 비치명 설정 오류만 해당 키를 default로 fallback하고 사용자 출력에 `[설정 경고]` 한 줄을 남긴다.

### 치명 설정 오류

다음 중 하나면 `plan-format`과 `plan-review`는 즉시 실패한다. 파일 생성, 입력 gate, SSOT 탐색, 검토를 수행하지 않는다.

- `.product-team-kit/config.json` 파일 없음
- JSON 파싱 실패
- 파일 읽기 실패 또는 UTF-8 디코딩 실패
- `version` 누락, 비정수, 또는 `1`이 아닌 값
- `outputRoot`가 존재하지만 검증 거부

`set-config`는 위 오류가 있어도 새 설정 파일을 만들거나 기존 파일을 덮어쓸 수 있는 유일한 스킬이다.

### `version`

- 정수 `1`이 아니면 (포함: 누락, 비정수, 다른 정수) 치명 설정 오류다.

### `outputRoot`

값이 없으면 default `planning`을 사용한다. 값이 존재하지만 다음 중 하나면 치명 설정 오류다.

- 문자열이 아님
- 빈 문자열
- 절대경로: `/`로 시작, 또는 Windows drive prefix(`C:\`, `D:/` 등)
- 경로 segment에 `..` 포함
- null byte(`\0`) 또는 제어문자 포함
- `/`, `\` 등 경로 구분자 포함 (단일 폴더명만 허용)

### `ssot.include`, `ssot.exclude`

- 배열이 아니면 그 키만 무시 + 경고
- 배열 원소 중 문자열이 아닌 것은 그 원소만 무시 + 경고 (배열 전체는 살림)
- 빈 배열은 정상값이다. `include`의 빈 배열은 default SSOT include 경로로 해석한다.

### Unknown key

- 표 정의 키 외에 top-level 키가 있으면 그 키는 무시 + 경고
- `ssot` 안의 unknown sub-key도 동일

### JSON 파싱 실패

- 파일은 존재하나 표준 JSON으로 파싱되지 않으면 치명 설정 오류다.
- 파일 읽기 실패(권한 오류, 디코딩 실패 등)와 UTF-8 디코딩 실패도 치명 설정 오류다.

## 경고 출력 포맷

설정 파싱/검증 중 경고가 1개 이상 있으면 사용자 출력 맨 아래에 `[설정 경고]` 블록을 한 번 추가한다. 경고가 없으면 블록을 출력하지 않는다.

```text
[설정 경고] (N개):
- [경로 또는 키]: [거부 사유와 fallback 결과]
```

예시:

```text
[설정 경고] (2개):
- ssot.include[1]: 비문자열 element 무시
- extra: 알 수 없는 키. 무시
```

## 적용 매핑

| Config key | 영향 받는 contract |
| --- | --- |
| `outputRoot` | `skills/plan-format/references/storage-contract.md` 저장 경로, `skills/plan-review`의 SSOT exclude 자동 추가 (`<outputRoot>/**`) |
| `ssot.include` | `skills/plan-review/SKILL.md` "Product Docs SSOT" 정의, `skills/plan-review/references/review-rules.md`의 SSOT corpus 선택 규칙 |
| `ssot.exclude` | `skills/plan-review/references/review-rules.md`의 SSOT corpus 선택 규칙(default 제외에 누적) |
| `CLAUDE.md`, `AGENTS.md` 안내 블록 | schema key는 아니지만 `set-config` 저장 성공 후 항상 생성·갱신된다. 일반 agent가 Product Docs SSOT 범위를 `.product-team-kit/config.json` 기준으로 우선 조회하도록 안내한다. |

config 적용으로 SSOT 범위가 좁혀진 것은 의도된 좁힘이므로 plan-review의 `검증 한계`에 새 항목으로 남기지 않는다. 좁힘 결과는 plan-review의 `읽은 근거`/`제외 후보` 출력에 그대로 반영한다.
