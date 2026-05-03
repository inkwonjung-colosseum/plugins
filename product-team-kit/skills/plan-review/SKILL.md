---
name: plan-review
description: "plan-format으로 작성한 기능설계서/정책서 초안 폴더 또는 파일을 외부 발행 전에 근거, 결정·범위, 실행·검증 가능성 측면에서 검토하는 스킬."
argument-hint: "<초안 폴더 또는 기능설계서/정책서 파일경로>"
---

# plan-review

`/product-team-kit:plan-format`으로 저장한 초안 폴더 또는 기능설계서/정책서 파일을 발행 전에 검토하는 스킬이다. 템플릿 구조 검사가 아니라 Project Docs SSOT 근거, 결정·범위, 실행·검증 가능성을 확인하는 gate다.

Project Docs SSOT는 `planning/`을 제외한 현재 프로젝트의 Markdown 문서와, 그 Markdown이 상대경로로 명시 참조한 로컬 resource만 포함한다. 코드, 테스트, 설정 파일, 빌드 산출물, dependency/vendor, 외부 URL은 SSOT 근거에서 제외한다. `planning/` 하위 파일은 검토 대상일 수 있지만 SSOT 근거로 사용하지 않는다.

판정 기준, 심각도, 신뢰도, 구조화 출력 상태, 근거 선택 규칙은 `references/review-gate.md`를 단일 기준으로 따른다. 근거 패키지 형식은 `references/evidence-package-schema.md`, 최종 출력 형식은 `references/output-templates.md`를 따른다. `pass`와 `conditional pass` 결과의 발행 준비 증적은 `references/publish-readiness-contract.md`, `수정 필요` 결과의 수정 작업 블록은 `references/review-rerun-contract.md`를 따른다. 역할별 독립 검토 프롬프트가 필요하면 `references/reviewer-prompts.md`를 사용한다.

## 호출

- Claude Code: `/product-team-kit:plan-review <초안 폴더 또는 기능설계서/정책서 파일경로>`
- Codex: `$plan-review <초안 폴더 또는 기능설계서/정책서 파일경로>`

예시:
- `/product-team-kit:plan-review planning/결제기능--YYYY-MM-DD-HHMMSS/`
- `/product-team-kit:plan-review planning/결제기능--YYYY-MM-DD-HHMMSS/결제기능_기능설계서.md`

## 암묵 호출 라우팅

다음 의도에서는 `plan-review`를 선택한다.

- 기존 기능설계서/정책서 초안 또는 초안 폴더 검토
- 발행 전 검토, review-gate 판단, pass/conditional pass/수정 필요 판정
- Project Docs SSOT 근거와 초안의 충돌, 누락, 실행 가능성 확인
- 이미 생성된 초안의 품질 평가

다음 의도에서는 `plan-review`를 선택하지 않는다.

- 질문하면서 기획 입력을 만들거나 모호함을 해소해야 하는 경우 → `plan-draft`
- 기획 입력을 기능설계서와 정책서 초안으로 생성해야 하는 경우 → `plan-format`

사용자가 “정리하고 검토”를 함께 요청했지만 기능설계서/정책서 초안 경로가 아직 없으면 `plan-review`를 먼저 호출하지 않는다. 먼저 `plan-format`으로 초안을 저장한 뒤 저장 경로를 대상으로 검토한다.

## 입력 확정

1. 입력이 폴더면 같은 폴더의 기능설계서와 정책서를 함께 검토 대상으로 잡는다.
2. 입력이 단일 파일이면 지정 파일을 검토 대상으로 잡고, 같은 폴더에서 `plan-format` 산출 파일명인 `[안전기능명]_기능설계서.md` / `[안전기능명]_정책서.md`의 같은 stem을 우선해 짝문서를 찾는다.
3. 짝문서 후보가 여러 개면 같은 `[안전기능명]` stem 후보만 함께 읽고, 나머지는 `읽지 않은 관련 후보`에 남긴다.
4. 짝문서가 없으면 단일 파일만 검토하되 `검증 한계`와 `limited`에 남긴다. 대상 문서가 명시적으로 다른 문서의 정책/기능 판단에 의존하면 P1 또는 P2로 판단한다.
5. 기능설계서/정책서가 아닌 상위설계서나 다른 문서 타입이 입력이면 내부 판정은 P0 gate failure로 처리하고, 사용자 출력은 `references/output-templates.md`의 입력 오류 템플릿을 사용한다.

## 실행 순서

1. 검토 대상, 짝문서 여부, 지원 문서 타입 여부를 확정한다.
2. 지원하지 않는 문서 타입이면 후속 검토를 수행하지 않고 입력 오류 템플릿으로 종료한다.
3. 근거 검토자가 검토 대상 파일과 관련 Project Docs SSOT Markdown 및 linked local resource를 직접 읽고 `references/evidence-package-schema.md` 형식의 근거 패키지를 만든다.
4. 근거 패키지 상태가 `failed`이면 결정·범위 검토와 실행·검증 가능성 검토를 생략하고 최종 결과를 `수정 필요`로 취합한다.
5. 근거 패키지 상태가 `completed` 또는 `limited`이면 결정·범위 검토와 실행·검증 가능성 검토를 검토 대상 파일과 근거 패키지 기반으로 수행한다. 실행 환경이 지원하면 두 관점은 병렬 또는 분리된 독립 컨텍스트로 수행한다.
6. 병렬 또는 분리된 독립 컨텍스트를 만들 수 없는 실행 환경에서는 동일 세션에서 결정·범위 검토 후 실행·검증 가능성 검토를 순차 수행한다. 이 fallback에서도 각 관점은 동일한 reviewer 계약을 따르고, 앞선 관점의 결론을 새 근거로 확정하지 않으며, 독립 컨텍스트 제한을 근거 패키지와 각 후속 관점의 `검증 한계`에 전파한다. 이 경우 최종 `pass`를 반환하지 않는다.
7. 각 관점은 `pass`, `conditional pass`, `수정 필요` 중 하나와 구조화된 발견 사항을 반환한다.
8. 최종 취합자는 `references/review-gate.md`의 합성 규칙으로 가장 보수적인 결과를 선택하고, `references/output-templates.md`의 형식으로 출력한다. 최종 결과가 `pass` 또는 `conditional pass`이면 `references/publish-readiness-contract.md` 기준의 발행 준비 증적을 함께 출력하고, `수정 필요`이면 `references/review-rerun-contract.md` 기준의 수정 작업 블록을 함께 출력한다.

현재 대화 컨텍스트는 근거가 아니다. 대화에서 알게 된 배경, 의도, 작성 당시 판단은 검토 대상 파일 또는 Project Docs SSOT 근거에 없으면 근거 부족 또는 근거 없는 가정으로 본다.

## 규칙

- 검토 기준과 결과 경계는 `references/review-gate.md`만 따른다.
- 근거 패키지는 `references/evidence-package-schema.md` 형식으로 기록한다.
- 최종 출력은 `references/output-templates.md` 형식을 사용한다.
- 역할별 실행 프롬프트가 필요하면 `references/reviewer-prompts.md`를 사용한다.
- `pass`와 `conditional pass`는 발행 실행이 아니라 `publish-readiness-contract.md` 기준의 발행 준비 증적을 출력한다.
- 수정이 필요한 경우 직접 수정하지 않는다. 수정 포인트만 제시한다.
- 수정 작업 블록은 수정 실행이 아니라 후속 작업 입력 계약이다.
- 외부 시스템에 직접 게시하지 않고 Project Docs SSOT Markdown 또는 팀 문서 export snapshot을 자동 수정하지 않는다.
- 읽은 근거 문서, 읽지 않은 관련 후보, 검증 한계를 최종 출력에 남긴다.
