---
name: plan-review
description: "Review a 기능설계서 or 정책서 file from plan-format for evidence, scope, and implementation readiness before external publishing."
argument-hint: "<파일경로>"
---

# plan-review

`/product-team-kit:plan-format`으로 저장한 초안 파일을 3개 관점으로 검토하는 선택 스킬.

검토 신뢰성을 위해 `plan-review`는 항상 **parallel fresh-context reviewers**를 사용한다. 새 검증 에이전트 3개가 지정 파일과 근거 문서를 직접 읽어 각 관점별 verdict를 내리고, 현재 대화 컨텍스트는 결과 취합과 명백한 누락 확인에만 사용한다.

## 호출

- Claude Code: `/product-team-kit:plan-review <파일경로>`
- Codex: `$plan-review <파일경로>`

예시: `/product-team-kit:plan-review planning/결제기능/결제기능_기능설계서.md`

## 언제 사용하나

- 중요한 정책 변경이나 신규 기능 설계서를 외부 발행 절차에 넘기기 전 품질을 확인하고 싶을 때
- 초안에 `[미정]`, `[가정]`, 확인 필요 질문, 충돌 경고가 없으면 건너뛸 수 있다. 단, 외부 발행 전 팀 정책에 맞춰 최종 확인한다.
- 초안에 `[미정]`, `[가정]`, 기존 문서와의 충돌 경고가 남아 있으면 publish 전에 필수로 사용한다

## 검토 관점 (3개)

검토 기준과 verdict 경계는 `references/review-gate.md`를 따른다.

### ① 근거
- 기존 Confluence 문서 내용과 충돌하는 부분이 있는가?
- `[가정]` 태그가 붙은 항목 중 실제로 확인이 필요한 것은 무엇인가?

### ② 범위
- 이 문서에서 결정해야 할 사항이 모두 담겼는가?
- `[미정]` 항목이 남아 있는가?

### ③ 실행
- 개발팀이 이 문서만 보고 구현을 시작할 수 있는가?
- 모호한 조건, 정의되지 않은 상태, 누락된 예외 케이스가 있는가?

## parallel fresh-context reviewers 절차

1. 지정한 파일 경로만 검토 대상으로 확정한다.
2. 공통 입력 패키지를 구성한다.
   - 검토 대상 파일 경로
   - 본 `plan-review` 지침
   - `references/review-gate.md`
   - 담당 reviewer 역할과 관점 범위
3. 새 검증 에이전트 3개를 생성해 각각 `fresh-context reviewer`로 지정한다.
4. reviewer 3개를 병렬로 실행한다.
   - 근거 reviewer: 기존 Confluence 원문과의 충돌, unsupported assumption, `[가정]`의 publish 영향 확인
   - 범위 reviewer: `[미정]`, 결정 누락, 지원 문서 타입 확인
   - 실행 reviewer: 개발·운영 착수 가능성, 모호한 조건, 상태·예외·권한·API 누락 확인
5. 각 reviewer는 검토 대상 파일을 직접 읽고, 초안에 명시된 관련 문서와 필요한 최소 Confluence 원문만 추가로 읽는다.
6. 각 reviewer는 현재 대화 컨텍스트를 근거로 사용하지 않는다. 대화에서 알게 된 배경, 의도, 작성 당시 판단은 파일 또는 근거 문서에 없으면 `[미정]` 또는 unsupported assumption으로 본다.
7. 각 reviewer는 `pass`, `conditional pass`, `수정 필요` 중 하나를 role verdict로 낸다.
8. 현재 컨텍스트는 reviewer 결과를 취합하되, 근거 없이 verdict를 완화하지 않는다. 최종 verdict는 더 보수적인 verdict를 사용한다.
   - `수정 필요 > conditional pass > pass`
   - reviewer 중 1개라도 `수정 필요`이면 최종 verdict는 `수정 필요`
   - `수정 필요`가 없고 1개라도 `conditional pass`이면 최종 verdict는 `conditional pass`
   - 3개 reviewer가 모두 `pass`일 때만 최종 verdict는 `pass`

새 검증 에이전트 3개를 병렬 생성할 수 없는 실행 환경에서는 `pass`를 반환하지 않는다. 이 경우 검증 방식 제한을 명시하고 `conditional pass` 또는 `수정 필요`로 결론낸다.

## 출력 형식

### pass
```
✅ 검토 완료 — pass

검증 방식: parallel fresh-context reviewers
검토 대상: [파일경로]
읽은 근거 문서:
- [문서명 또는 파일경로]
관점별 verdict:
- 근거 reviewer: pass
- 범위 reviewer: pass
- 실행 reviewer: pass

팀의 외부 발행 절차에 따라 Confluence 반영 여부를 결정하세요.
```

### 조건부 pass
```
✅ 검토 완료 — conditional pass

검증 방식: parallel fresh-context reviewers
검토 대상: [파일경로]
읽은 근거 문서:
- [문서명 또는 파일경로]
관점별 verdict:
- 근거 reviewer: [pass / conditional pass]
- 범위 reviewer: [pass / conditional pass]
- 실행 reviewer: [pass / conditional pass]

[조건]: [발행 전에 기획자가 명시적으로 확인해야 할 내용]

조건을 확인한 뒤 팀의 외부 발행 절차를 진행하세요.
```

### 수정 필요
```
⚠️ 수정 필요

검증 방식: parallel fresh-context reviewers
검토 대상: [파일경로]
읽은 근거 문서:
- [문서명 또는 파일경로]
관점별 verdict:
- 근거 reviewer: [pass / conditional pass / 수정 필요]
- 범위 reviewer: [pass / conditional pass / 수정 필요]
- 실행 reviewer: [pass / conditional pass / 수정 필요]

[관점]: [이유]
→ [수정 포인트]

[관점]: [이유]
→ [수정 포인트]

수정 후 다시 /product-team-kit:plan-review 를 실행하세요.
```

## 규칙

- 검토는 지정한 파일을 parallel fresh-context reviewers가 직접 읽어서 수행한다
- 3개 reviewer는 근거 reviewer, 범위 reviewer, 실행 reviewer로 나눈다
- 로컬 Confluence 파일을 추가로 읽어 근거를 확인할 수 있다
- 수정이 필요한 경우 직접 수정하지 않는다. 수정 포인트만 제시한다
- 현재 대화 컨텍스트를 근거로 사용하지 않는다
- 현재 컨텍스트와 reviewer 판단이 다르면 더 보수적인 verdict를 최종 verdict로 사용한다
- `[미정]`, `[가정]`, 충돌 경고가 publish를 막을 정도인지 판단하고 pass / conditional pass / 수정 필요 중 하나로 결론낸다
- 상위설계서는 지원하지 않는다. 기능설계서와 정책서만 검토한다
