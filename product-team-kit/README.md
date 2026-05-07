# product-team-kit

기획 입력을 현재 템플릿에 맞춰 기능설계서와 정책서 초안으로 정리하고, 외부 공유나 팀 문서 반영 전에 Product Docs SSOT 근거 기반으로 검토하는 제품팀 도구. Claude Code와 Codex 양쪽에서 동작한다.

## 핵심 원칙

- **Strict-exit on missing config**: `plan-format`은 `.product-team-kit/config.json`이 없거나 핵심 키 검증에 실패하면 즉시 종료하고 `set-config` 사용을 안내한다.
- **Project agent guide**: `set-config`는 config 저장 성공 후 프로젝트 루트 `CLAUDE.md`와 `AGENTS.md`의 product-team-kit 관리 블록을 선택 없이 항상 생성·갱신한다.
- **Lazy read**: `plan-format`과 `plan-review`는 종료 분기가 확정되기 전 필요한 파일만 단계별로 읽는다. templates, references, SSOT corpus를 선행 단계에서 한꺼번에 읽지 않는다.
- **Early review stop**: `plan-review`는 초안 본문만으로 핵심 판단 누락이 과도하면 SSOT 탐색 전에 `수정 필요 (조기 판정)`으로 종료한다.
- **Gate First**: `plan-format`은 변환 가능성을 먼저 판정하고, 통과 전에는 파일 생성 금지다.
- **Formatter first**: `plan-format`은 통과한 입력값을 템플릿에 맞게 구조화한다.
- **No interview loop**: `plan-format`은 질문하지 않는다. 입력이 부족하면 파일을 만들지 않고 부족 항목만 출력한다.
- **Product Docs SSOT**: 기존 내용 검증은 `<outputRoot>/`을 제외한 현재 프로젝트의 제품 정책, PRD/요구사항, 기능/화면 설계, 운영/QA 판단 Markdown과 그 문서가 참조한 로컬 resource를 기준으로 `plan-review`에서 수행한다.
- **읽기**: `plan-format`은 사용자가 준 입력값, 파일, 또는 기획자료 폴더를 읽는다.
- **쓰기**: 입력에서 기능명을 추출해 로컬 `<outputRoot>/[안전기능명]--YYYY-MM-DD-HHMMSS/` 아래에 기능설계서와 정책서 초안을 저장한다. `<outputRoot>` 기본값은 `planning`이다.
- **발행 전 검토**: 외부 공유나 팀 문서 반영 전에는 `plan-review`로 기능설계서와 정책서를 함께 검토한다.

## 로컬 초안 템플릿 경계

`<outputRoot>/` 아래 생성되는 기능설계서와 정책서는 **로컬 초안 템플릿**이다. 기본 `<outputRoot>`는 `planning`이다. 이 산출물은 **공식 팀 문서가 아니다**. 팀 문서 필수 섹션과 1:1로 동기화된 원본이 아니라, 사람이 팀 문서에 반영하기 전 검토하는 작업 초안이다.

팀 문서 히스토리는 반영 이후 관리한다. 따라서 이 플러그인은 팀 문서 export snapshot, Product Docs SSOT Markdown, 팀 문서 이력을 자동 수정하지 않는다.

## Product Docs SSOT

Product Docs SSOT는 현재 프로젝트 안의 제품 정책, PRD/요구사항, 기능/화면 설계, 운영/QA 판단 `*.md`, `*.markdown` 문서와, 그 문서가 상대경로로 명시 참조한 로컬 resource만 포함한다. `<outputRoot>/` 하위 산출물은 검토 대상일 수 있지만 SSOT 근거로 사용하지 않는다.

SSOT 근거에서 제외하는 항목:

- `<outputRoot>/`, `.git/`, dependency/vendor/build/cache/generated 경로
- 코드, 설정 파일
- 외부 URL
- Markdown에서 참조하지 않은 독립 resource

외부 문서 시스템에서 export된 Markdown이 프로젝트에 있더라도 특별 취급하지 않고 일반 Product Docs 후보로만 취급한다.

## 문서 타입

| 타입 | 용도 |
|:-----|:-----|
| 기능설계서 | HOW·화면·플로우. 기획자가 정하는 기능 동작 명세 |
| 정책서 | 규칙·조건·예외 정의 |

## 스킬별 계약

`plan-format`은 3-step 변환 흐름이다 (config strict-exit → Gate First → dispatch 후 main 직접 작성·main 검증·저장). 입력 판정, lazy read 순서, 분류 기준, marker 규칙은 `skills/plan-format/SKILL.md`에서 단일 소스로 따른다. 저장 위치와 안전기능명, 출력 템플릿은 필요한 분기에서만 `skills/plan-format/references/storage-contract.md`와 `skills/plan-format/references/output-contract.md`를 읽어 따른다. `plan-review`의 SSOT corpus 선택, main A축 점검, B/C worker 점검 기준, 합성 규칙, 출력 템플릿은 필요한 시점에 `skills/plan-review/references/review-rules.md`와 `skills/plan-review/references/output-format.md`를 읽어 따른다.

## Start Here

```text
/product-team-kit:set-config
/product-team-kit:plan-format "주문 취소 기능: 주문 취소 정책과 화면 동작 정리..."
/product-team-kit:plan-format /path/to/planning-notes.md
/product-team-kit:plan-format /path/to/planning-folder/
/product-team-kit:plan-review planning/주문취소--YYYY-MM-DD-HHMMSS/
$set-config
$plan-format "반품 접수 기능 관련 AI 대화 결과물 또는 비구조 기획 노트"
$plan-review planning/반품접수--YYYY-MM-DD-HHMMSS/
```

`plan-format`에는 기능명을 별도 인자로 입력하지 않는다. 스킬이 입력 본문, 파일명, 디렉터리명에서 기능명을 추출한다.

전체 스킬 설명과 각 스킬별 워크플로 다이어그램은 [`docs/skills-workflow.md`](docs/skills-workflow.md)를 참고한다.

제품 관점의 요구사항과 기능 정의는 [`docs/prd.md`](docs/prd.md), [`docs/feature-definition.md`](docs/feature-definition.md)에 정리한다.

## 설치

### Claude Code

```bash
claude plugin marketplace add https://github.com/inkwonjung-colosseum/plugins
claude plugin install product-team-kit@inkwonjung-colosseum
```

### Codex

```bash
codex marketplace add https://github.com/inkwonjung-colosseum/plugins
```

marketplace 추가 후 Codex 앱의 `/plugins`에서 `product-team-kit`을 설치/활성화한다.

## Implicit Invocation 라우팅

자연어 요청으로 스킬을 암묵 호출할 때는 아래 우선순위를 따른다.

| 사용자 의도 | 선택 스킬 | 기준 |
|:--|:--|:--|
| 기획 노트·회의록·AI 대화 결과·기획자료 디렉터리를 기능설계서와 정책서로 정리 | `plan-format` | 기능설계서/정책서 초안 생성 또는 저장이 목적 |
| 기존 초안 평가, 발행 전 검토, 통과/조건부 통과/수정 필요 판단 | `plan-review` | 이미 생성된 기능설계서/정책서 초안 또는 초안 폴더가 대상 |

한 요청에 생성과 검토가 함께 있으면 `plan-format`으로 초안을 만든 뒤 `plan-review`를 다음 단계로 안내한다. 사용자가 명시적으로 “생성 후 바로 검토”를 요청하고 초안 저장이 성공한 경우에만 같은 흐름에서 `plan-review`를 이어서 수행한다.

## 워크플로

```text
/product-team-kit:plan-format "기획 입력 또는 파일/디렉터리 경로"
    ↓ Step 1: .product-team-kit/config.json 존재·유효성 확인 (없으면 strict-exit, set-config 안내)
    ↓ Step 2: 입력 dispatch 후 Gate First로 변환 가능성 판정 (불가 시 부족 항목만 출력)
    ↓ Step 3: templates를 필요한 시점에 읽고 dispatch → main 직접 작성 → main 검증 후 <outputRoot>/[안전기능명]--YYYY-MM-DD-HHMMSS/ 에 저장
    ↓
/product-team-kit:plan-review <초안 폴더 또는 기능설계서/정책서 파일경로>
    ↓ 검토 대상 본문만으로 조기 수정 판정 여부 확인
    ↓ 검토 대상·키워드·SSOT 후보를 확정하고 필요한 corpus만 읽기
    ↓ main A축 SSOT 점검 + B/C worker 점검 → merge
    ↓ 기획팀용 리포트로 판정·먼저 할 일 출력
    ↓ 최종 결과는 수정 필요 > 조건부 통과 > 통과 순서로 보수적으로 취합
```

`plan-format`은 3-step 변환 스킬이다. config가 없거나 핵심 키 검증에 실패하면 즉시 strict-exit으로 종료하고 `set-config`를 안내한다. 이때 입력, templates, storage contract는 읽지 않는다. 입력이 부족하면 질문 루프를 만들지 않고 저장 보류를 반환한다. 이때 출력에는 부족 항목만 포함하고 보강용 입력 템플릿은 만들지 않으며, templates와 storage contract도 읽지 않는다. 디렉터리 입력은 기본 제외 경로를 적용한 뒤 모든 텍스트 파일을 읽는다. 입력 크기 상한은 두지 않으며, 검증 정확도를 위해 무거워도 끝까지 읽는다. 기존 기능설계서/정책서도 참고 입력으로 포함할 수 있지만, 저장은 새 timestamp 폴더에만 수행한다. 변환 단계에서는 templates를 본문 작성 직전에 읽고, dispatch가 기능명·역할명·용어·라벨을 고정한다. main이 파일 크기와 무관하게 기능설계서와 정책서 본문을 같은 턴에서 직접 작성한 뒤 구조 일치(9개 섹션 헤더·metadata), 표 의미 보존, 빈 골격, 중복 항목, 라벨 cross-bleed, marker 합산을 검증한다. 표는 컬럼명·순서·개수 exact match가 아니라 semantic validation을 적용하며, 섹션 6~9는 입력 근거가 없으면 한 줄로 압축할 수 있다. 중복과 cross-bleed는 전체 재작성 없이 위반 문장·행·셀만 국소 repair한다. 저장 contract는 main 검증 통과 후 저장 절차 직전에만 읽는다. 읽을 수 없는 파일은 출력의 `[입력 제외 항목]`에 남긴다. 생성된 초안은 review target이지 Product Docs SSOT 근거가 아니다. `plan-format`은 Product Docs SSOT를 검색하거나 검증하지 않는다. Python, Node.js, 별도 CLI helper 설치는 전제하지 않는다.

`plan-review`는 검토 대상과 짝문서를 확정한 뒤, 초안 본문만으로 핵심 섹션의 `[미정]`, 빈 필수 섹션, `[충돌 후보]`가 과도한지 먼저 본다. 기준을 충족하면 SSOT corpus 탐색과 worker 실행 없이 `수정 필요 (조기 판정)`으로 종료한다. 조기 판정이 아니면 키워드로 좁힌 Product Docs Markdown과 필요한 linked local resource만 읽어 3축(SSOT 충돌, 명확성, 용어 일관성)으로 점검한다. config 치명 오류나 지원하지 않는 문서 타입에서는 review rules와 SSOT corpus를 읽지 않고 종료 템플릿만 적용한다. SSOT 키워드 추출에 실패하면 worker를 실행하지 않고 `수정 필요`로 종료한다. 키워드 추출은 성공했지만 corpus 매칭이 0건이면 A축은 `검증 대상 없음`으로 처리하고, B/C는 검토 대상 본문만으로 점검한다. 후보가 있으면 상위 20줄 인덱스 스캔으로 archive/deprecated/낮은 버전/키워드 미매칭 문서를 전문 읽기에서 제외한 뒤 핵심 후보만 읽는다. main이 A축 SSOT 충돌을 직접 점검하고, B/C worker는 본문 기반 발견 사항만 작성한다. 이후 main이 dedup, 보수 합성, 결과 판정, 리포트 출력을 담당한다. 병렬 worker 호출이 불가능한 환경에서는 같은 결과 형식으로 단일 패스 fallback을 사용한다. `<outputRoot>/` 하위 파일은 검토 대상으로 읽을 수 있지만 SSOT 근거로 사용하지 않는다. 출력 상단에는 기획팀이 바로 볼 수 있도록 판정, 한 줄 결론, 먼저 할 일, 기준 문서 충돌을 보여준다. 결과가 `수정 필요`이면 하단에 재검토 안내 체크리스트를 출력하고, 초안을 수정한 뒤 같은 폴더를 다시 검토한다. `통과` 또는 `조건부 통과`이면 발행 준비 체크리스트를 출력한다. 이 체크리스트는 외부 게시가 아니라 팀의 외부 반영 또는 공유 절차로 넘기기 전 사람이 확인할 항목이다. 출력은 사람용 markdown 리포트 하나로 통일하며 별도 YAML manifest 블록은 사용하지 않는다. 기능/화면설계서 또는 정책서가 아닌 입력은 검토 결과가 아니라 `올바른 검토 대상이 아님` 안내로 종료한다.

플러그인 내부 생성·검토 흐름은 루트의 [`docs/diagrams/product-team-kit-workflow.html`](../docs/diagrams/product-team-kit-workflow.html)에서 확인한다. 상세 분석 흐름은 [`docs/diagrams/product-team-kit-workflow-analysis.html`](../docs/diagrams/product-team-kit-workflow-analysis.html)을 참고한다. 두 다이어그램은 [`docs/diagrams/product-team-kit-workflow.source.json`](../docs/diagrams/product-team-kit-workflow.source.json)을 단일 source로 사용해 생성된다.

## 스킬

Claude Code:

```text
/product-team-kit:plan-format
/product-team-kit:plan-review
/product-team-kit:set-config
```

Codex:

```text
$plan-format
$plan-review
$set-config
```

## 포함 구성

- `.claude-plugin/plugin.json` — Claude Code 플러그인 매니페스트
- `.codex-plugin/plugin.json` — Codex 플러그인 매니페스트
- `references/config-contract.md` — 세 skill 공유 로컬 설정(`.product-team-kit/config.json`)과 agent 안내 파일 계약
- `agents/` — plan-review B/C 내부 worker 정의
- `skills/*/agents/` — OpenAI/Codex skill metadata와 implicit invocation routing hint
- `skills/plan-format/` — 기획 입력 → 기능설계서·정책서 동시 생성
- `skills/plan-format/templates/` — 기능설계서·정책서 템플릿
- `skills/plan-format/references/` — `storage-contract.md` (저장 위치, 안전기능명, collision suffix), `output-contract.md` (저장 완료/보류/설정 없음/저장 실패 4종 출력 템플릿)
- `skills/plan-review/` — Product Docs SSOT 근거 기반 발행 전 초안 품질 검토 (3축: SSOT 충돌, 명확성, 용어 일관성)
- `skills/plan-review/references/` — `review-rules.md` (판정·합성·근거 규칙), `output-format.md` (4종 결과 템플릿)
- `skills/set-config/` — `.product-team-kit/config.json` 대화형 갱신과 `CLAUDE.md`/`AGENTS.md` 안내 블록 생성
- `docs/` — 스킬 워크플로 설명, 안전/정책 문서

## 로컬 설정

사용처 프로젝트 루트에 `.product-team-kit/config.json`을 두면 세 skill이 같은 설정 계약을 따른다. `set-config`는 이 파일을 대화형으로 만들거나 갱신하고, 저장 성공 후 같은 root의 `CLAUDE.md`와 `AGENTS.md`에 product-team-kit 안내 블록을 항상 생성·갱신한다. **`plan-format`과 `plan-review`는 config strict-exit**: 파일이 없거나 JSON 파싱 실패, `version` 미일치, `outputRoot` 검증 거부 시 즉시 종료하고 `set-config` 사용을 안내한다. 비치명 검증 거부 (unknown key, ssot 배열 element 비문자열)는 그 키만 default로 fallback하고 사용자 출력 끝에 `[설정 경고]` 블록 한 번을 추가한다. 적용 우선순위는 CLI 인자 > config.json > contract default 순이다.

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

| Key | 사용 skill | default | 의미 |
| --- | --- | --- | --- |
| `version` | 세 skill | (필수, 정수 1) | schema 버전. 미일치 시 `plan-format`과 `plan-review`는 즉시 실패하고, `set-config`는 항상 1 저장 |
| `outputRoot` | `set-config`, `plan-format`, `plan-review` | `planning` | 초안 저장 root 폴더명. 디렉터리 입력 제외 경로와 `plan-review` SSOT exclude에도 자동 반영 |
| `ssot.include` | `set-config`, `plan-review` | `Product Team Space/Product Department/Colonova Product/_AI_ 정책서 & 기능설계서/**/*.md` | SSOT corpus allow-list glob |
| `ssot.exclude` | `set-config`, `plan-review` | (없음) | SSOT corpus 추가 제외 glob. default 제외에 누적. `<outputRoot>/**`은 항상 자동 포함 |

`outputRoot`은 단일 폴더명만 허용한다. 값이 없으면 default `planning`을 사용하지만, 값이 존재하면서 절대경로(`/` 시작 또는 Windows drive prefix `C:\` 등), `..`, 빈 문자열, 경로 구분자(`/`, `\`) 포함, null byte/제어문자 포함, 비문자열이면 `plan-format`과 `plan-review`는 즉시 실패한다. 검색 위치 결정과 검증 규칙 전체는 [`references/config-contract.md`](references/config-contract.md)를 따른다.

JSON을 직접 편집하지 않고 대화형으로 갱신하려면 `/product-team-kit:set-config`(Claude Code) 또는 `$set-config`(Codex)를 사용한다. 각 키마다 현재 값(또는 default)을 유지하거나 직접 입력하는 두 옵션을 차례로 제시한다. config 저장이 성공하면 `CLAUDE.md`와 `AGENTS.md`는 선택 없이 항상 처리되며, 기존 파일 내용은 product-team-kit 관리 블록 밖에서 보존된다.
