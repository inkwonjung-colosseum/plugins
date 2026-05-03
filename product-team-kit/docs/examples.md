# product-team-kit Examples

## 대화형 기획초안 생성

```text
$plan-draft "주문 취소 기능을 기획하고 싶어"
```

`plan-draft`는 사용자의 답변을 바탕으로 `plan-format`에 넘길 기획초안을 만든다. 핵심 모호함이 남아 있으면 최대 3라운드까지 추가 질문하고, 확정할 수 없는 항목은 `[미정]`, `[가정]`, `[확인 필요]`, `[충돌 후보]`로 남기는 기획 인터뷰다. Claude Code에서는 `AskUserQuestion`, Codex에서는 Plan mode의 `ask_user_question` / `request_user_input` 계열 사용자 질문 도구를 우선 사용한다. Codex에서 질문 도구가 없어도 현재 대화를 이어갈 수 있으면 일반 대화 fallback으로 필요한 질문을 묻고, 다음 사용자 답변을 같은 `plan-draft` 흐름으로 이어받는다. 비대화형 실행처럼 사용자 답변을 이어받을 수 없는 경우에만 저장하지 않고 `질문 필요로 저장 보류`를 반환한다.

예상 흐름:

1. 기능 의도와 현재 입력 수준을 확인한다.
2. 필요한 경우 현재 로컬 프로젝트에서 관련 문서, 화면, 기존 흐름을 좁게 확인한다.
3. 문제/목적, 사용자/범위, 핵심 흐름, 정책/조건, 예외/권한/상태, 확인 기준 순서로 질문한다.
4. 답변이 추상적이면 누가, 언제, 무엇을 보고, 어떤 선택을 하고, 성공·실패 시 결과가 무엇인지 다시 묻는다.
5. 사용자 답변과 로컬 확인 내용을 구분해 기획초안으로 정리하고, 충돌 가능성이 있으면 `[충돌 후보]`로 남긴다.
6. `planning/주문취소--YYYY-MM-DD-HHMMSS/주문취소_기획초안.md`에 저장한다. 같은 폴더가 있으면 덮어쓰지 않고 timestamp 재생성 또는 `--01`/`--02` suffix를 사용한다.

Codex 일반 대화 fallback 예:

```text
plan-draft 일반 대화 질문
- 추출 기능명: 주문 취소
- 초안 생성 가능: 아니오
- 파일 생성: 아니오
- 이유: 질문 도구는 없지만 현재 대화를 이어갈 수 있어 일반 대화 fallback으로 질문함
- 질문 라운드: 1/3

필요한 답변:
1. 주문 취소를 사용하는 주요 사용자는 누구인가요?
2. 사용자는 어떤 행동을 하고 어떤 결과를 기대하나요?
3. 주문 취소를 허용하거나 금지하는 주요 조건은 무엇인가요?
```

위 질문에 답하면 같은 `plan-draft` 흐름으로 이어서 저장 가능성을 판단한다. 별도 `$plan-draft` 재실행은 필요 없다. 비대화형 실행에서는 이 fallback을 쓰지 않고 `질문 필요로 저장 보류`와 재실행 입력 블록을 반환한다.

저장 후 다음 단계는 저장된 기획초안을 `plan-format`에 넘기는 것이다. 이 경우 `plan-format`은 기획초안 폴더를 재사용해 같은 폴더에 기능설계서와 정책서를 저장한다.

```text
$plan-format planning/주문취소--YYYY-MM-DD-HHMMSS/주문취소_기획초안.md
```

`plan-draft` 자체의 저장 보류가 나오면 부족 항목의 답변을 보완해 다시 `plan-draft`를 실행한다.

상세 출력 형식은 `../references/output-contract.md`의 `plan-draft` 템플릿을 따른다.

## 기능설계서/정책서 동시 생성

```text
$plan-format "주문 취소 기능: 주문 취소 가능 조건, 화면 흐름, 예외 처리 메모..."
```

기능명을 입력하지 않는다. 스킬이 입력 본문에서 `주문 취소`를 추출한다.

생성되는 기능설계서와 정책서는 `planning/` 하위 로컬 초안 템플릿이다. 공식 팀 문서가 아니다.

예상 흐름:

1. 입력 본문에서 기능명과 핵심 요구를 추출한다.
2. 초안 생성 가능성 검증으로 문서 생성 가능한 최소 입력인지 확인한다.
3. 충분하면 공통 정리 기준으로 기능명, 범위, 역할명, 공통 용어를 확정한다.
4. 기능설계서와 정책서 본문만 병렬로 작성한다.
5. 단일 흐름에서 역할명·범위·미정 항목을 최종 조정한다.
6. 부족한 세부 조건은 질문하지 않고 `[미정]`, `[가정]`, 확인 필요 질문으로 남긴다.
7. `plan-draft` 산출 `_기획초안.md` 입력이면 같은 기획초안 폴더를 재사용한다. 직접 입력, 일반 파일 입력, AI 대화 결과물, 문서 스크랩 같은 일반 입력은 새 timestamp 폴더에 기능설계서와 정책서를 저장한다.

기능설계서 초안에는 기획자가 정하는 `확인 기준`을 포함한다.

일반 입력이 부족하면 파일을 만들지 않고 아래처럼 저장 보류 피드백을 반환한다. 저장 보류는 기능 목적, 사용자/업무 범위, 핵심 행동/결과, 주요 조건/정책/제약이 없어 초안 골격을 만들 수 없는 경우에만 사용한다.

```text
저장 보류
- 추출 기능명: 주문 취소
- 초안 생성 가능: 아니오
- 재실행 상태: format-insufficient-hold
- 이유: 입력만으로 기능설계서/정책서 초안을 만들기 부족함

부족 항목:
- 적용 대상: 어떤 사용자나 업무 범위에 적용되는지 없음
- 핵심 동작: 사용자가 수행하는 행동과 기대 결과가 없음

다음 단계:
아래 정보를 함께 plan-draft에 전달한다.
- 기획 주제: 주문 취소
- 원 입력 또는 원 입력 파일 경로: 주문 취소 기능
- plan-format에서 부족하다고 판단한 항목: 적용 대상, 핵심 동작

바로 재실행 가능한 입력 블록:
$plan-draft "재실행 상태: format-insufficient-hold
기획 주제: 주문 취소
원 입력 또는 원 입력 파일 경로: 주문 취소 기능
plan-format 저장 보류 사유: 입력만으로 기능설계서/정책서 초안을 만들기 부족함
부족 항목: 적용 대상, 핵심 동작
필요한 답변:
1. 주문 취소를 사용하는 주요 사용자는 누구인가요?
2. 사용자는 어떤 행동을 하고 어떤 결과를 기대하나요?
답변:
1. [사용자 답변]
2. [사용자 답변]"
```

`plan-format`이 `plan-draft` 산출 `_기획초안.md`를 입력받았는데도 부족하면 자동으로 다시 `plan-draft`로 보내지 않고 `사용자 결정 필요`로 종료한다.

```text
사용자 결정 필요
- 추출 기능명: 주문 취소
- 초안 생성 가능: 아니오
- 재실행 상태: format-after-draft-insufficient
- 자동 재질문 중단: 예
- 이유: plan-draft 산출 기획초안 입력으로도 기능설계서/정책서 초안을 만들기 부족함

부족 항목:
- 주요 조건: 주문 취소 허용/금지 기준이 없음

선택 가능한 다음 행동:
1. 부족 항목을 직접 채워 plan-format 재실행
2. 새 기획 인터뷰를 명시적으로 시작
3. 현재 입력으로 생성 범위를 줄여 다시 요청

바로 재실행 가능한 입력 블록:
$plan-format "기능명: 주문 취소
이전 기획초안: planning/주문취소--YYYY-MM-DD-HHMMSS/주문취소_기획초안.md
보완한 부족 항목:
1. 주문 취소는 결제 완료 전까지만 허용한다.
생성 범위 조정: 유지"
```

세부 권한, 예외, 상태, 문구, QA 상세처럼 초안 골격을 막지 않는 항목은 저장을 막지 않고 `[미정]`, `[가정]`, `[확인 필요]`로 남긴다. 확인 필요 항목에는 결정 이유와 결정 주체를 함께 남긴다.

문서가 저장되면 출력에 `초안 생성 가능: 예`가 포함된다. 초안에 `[가정]`, 확인 필요 질문, 원본 문서 피드백이 있으면 외부 공유나 팀 문서 반영 전 `plan-review`로 기능설계서와 정책서를 함께 검토한다.

상세 출력 형식은 `../references/output-contract.md`의 `plan-format` 템플릿을 따르고, 기능설계서/정책서 분류는 `../skills/plan-format/references/classification-contract.md`를 따른다.

## 초안 검토

```text
$plan-review planning/주문취소--YYYY-MM-DD-HHMMSS/
$plan-review planning/주문취소--YYYY-MM-DD-HHMMSS/주문취소_기능설계서.md
```

`plan-review`는 초안 파일과 필요한 Project Docs SSOT 근거를 읽어 근거 패키지를 만든 뒤, 근거·결정/범위·실행/검증 가능성 관점의 가장 보수적인 결과를 최종 결과로 사용한다. 초안 폴더를 넘기면 `_기획초안.md`는 입력 출처로만 두고, 기능설계서와 정책서를 함께 읽어 두 문서의 역할명, 범위, 정책 기준이 어긋나지 않는지 확인한다. `planning/` 하위 파일은 검토 대상일 수 있지만 SSOT 근거로 사용하지 않는다.

검토 관점:

- 근거: `planning/`을 제외한 현재 프로젝트의 Markdown 문서와 linked local resource가 초안 주장과 충돌하는지 확인한다.
- 결정·범위: 결정해야 할 정책과 예외, 결정 주체, 후속 액션, 관련 정책서/기능설계서 문서 연결이 빠졌는지 확인한다.
- 실행·검증 가능성: 상태, 조건, 예외, 사용자 노출 결과, 업무 연동 경계, 외부 채널, 실패 대응이 명확한지 확인한다.

발견 사항은 P0/P1/P2/P3 심각도와 100/75/50 신뢰도 앵커를 가진다. P0/P1은 수정 포인트, P2는 확인 조건, P3는 참고 관찰로 취급한다.

결과는 `pass`, `conditional pass`, `수정 필요` 중 하나다.

- `pass`: 팀의 외부 반영 또는 공유 절차로 넘길 수 있다.
- `conditional pass`: 확인 조건을 기획자가 명시적으로 수용한 뒤 반영 절차로 넘긴다.
- `수정 필요`: 초안을 수정하고 같은 폴더로 `plan-review`를 다시 실행한다. 출력의 `review_repair` 블록은 후속 수정 작업에 넘길 수 있는 입력 계약이다.

짧은 `pass` 예시:

```yaml
publish_readiness:
  status: ready
  target_path: "planning/입고신청--YYYY-MM-DD-HHMMSS/"
  review_result: "pass"
  draft_paths:
    feature_doc_path: "planning/입고신청--YYYY-MM-DD-HHMMSS/입고신청_기능설계서.md"
    policy_doc_path: "planning/입고신청--YYYY-MM-DD-HHMMSS/입고신청_정책서.md"
  evidence_status: "completed"
  publish_candidate:
    destination: "external process"
    team_doc_candidate: "입고 신청"
    freshness_risk: "none"
  remaining_conditions:
    - "없음"
  human_checklist:
    - "검토 대상 초안의 기능설계서/정책서 쌍을 확인한다."
    - "팀 문서 반영 후 팀 문서 ID와 update timestamp를 별도 운영 기록에 남긴다."
  forbidden_actions:
    - "plan-review가 외부 시스템에 직접 게시하지 않는다."
    - "planning/ 산출물을 Project Docs SSOT 근거로 승격하지 않는다."
    - "Project Docs SSOT Markdown 또는 팀 문서 export snapshot을 자동 수정하지 않는다."
```

짧은 `수정 필요` 예시:

```yaml
review_repair:
  status: review-repair-needed
  target_path: "planning/입고신청--YYYY-MM-DD-HHMMSS/"
  review_result: "수정 필요"
  editable_scope:
    - "planning/ 하위 검토 대상 초안"
  forbidden_scope:
    - "Project Docs SSOT Markdown"
    - "팀 문서 export snapshot"
    - "linked local resource"
    - "코드, 테스트, 설정 파일"
  findings:
    - id: "FIX-001"
      severity: "P1"
      target: "입고신청_정책서.md > 7. 역할과 권한"
      title: "승인 권한 기준 누락"
      evidence_quote: "입고 보류 해제는 관리자 승인 후 처리"
      required_change: "정책서에 승인자 역할과 승인 가능 조건을 명시한다."
      acceptance_check: "정책서 7장에 승인자 역할과 승인 조건이 분리되어 있다."
  rerun:
    claude: "/product-team-kit:plan-review planning/입고신청--YYYY-MM-DD-HHMMSS/"
    codex: "$plan-review planning/입고신청--YYYY-MM-DD-HHMMSS/"
```

## 파일 입력

```text
$plan-format /path/to/입고신청-planning-notes.md
```

파일 경로를 넘기면 해당 파일 내용을 읽고, 파일명과 본문에서 기능명을 추출해 같은 방식으로 기능설계서와 정책서 초안을 만든다.
