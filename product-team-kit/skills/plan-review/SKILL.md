---
name: plan-review
description: "Review a 기능설계서/정책서 draft folder or file from plan-format for evidence, decision scope, and execution readiness before external publishing."
argument-hint: "<초안 폴더 또는 기능설계서/정책서 파일경로>"
---

# plan-review

`/product-team-kit:plan-format`으로 저장한 초안 폴더 또는 초안 파일을 3개 관점으로 검토하는 스킬. `plan-review`는 템플릿 구조 검증 도구가 아니라 발행 전 근거·결정·실행 가능성 검토 도구다. Confluence 반영이나 외부 공유 같은 외부 발행 전에는 필수로 사용한다.

검토 신뢰성을 위해 `plan-review`는 항상 **독립 검토 3개 관점**을 사용한다. 새 검증 에이전트 3개가 지정 파일과 근거 문서를 직접 읽어 각 관점별 검토 결과를 내리고, 현재 대화 컨텍스트는 결과 취합과 명백한 누락 확인에만 사용한다.

## 호출

- Claude Code: `/product-team-kit:plan-review <초안 폴더 또는 기능설계서/정책서 파일경로>`
- Codex: `$plan-review <초안 폴더 또는 기능설계서/정책서 파일경로>`

예시: `/product-team-kit:plan-review planning/drafts/결제기능--YYYY-MM-DD-HHMMSS/`

초안 폴더를 받으면 기능설계서와 정책서를 함께 검토한다. 단일 파일을 받으면 지정 파일을 검토하되, 같은 폴더에 짝이 되는 기능설계서 또는 정책서가 있으면 함께 읽어 역할명·범위·정책 기준이 두 문서에서 충돌하지 않는지 확인한다.

## 언제 사용하나

- 중요한 정책 변경이나 신규 기능 설계서를 외부 발행 절차에 넘기기 전 품질을 확인할 때
- Confluence 반영이나 외부 공유 전에는 필수로 사용한다
- 초안에 `[미정]`, `[가정]`, 기존 문서와의 충돌 경고가 남아 있으면 publish 전에 필수로 사용한다

## 검토 관점 (3개)

검토 기준과 결과 경계는 `references/review-gate.md`를 따른다.

### ① 근거
- 기존 Confluence 문서 내용과 충돌하는 부분이 있는가?
- `[가정]` 태그가 붙은 항목 중 실제로 확인이 필요한 것은 무엇인가?

### ② 결정·범위
- 이 문서에서 결정해야 할 사항이 모두 담겼는가?
- `[미정]` 항목마다 결정 주체나 후속 액션이 있는가?
- 관련 정책서/기능설계서가 필요한 문맥에서 문서명이나 경로가 빠진 곳은 없는가?

### ③ 실행·검증 가능성
- 개발·운영·QA가 이 문서만 보고 같은 판단을 할 수 있는가?
- 모호한 조건, 정의되지 않은 상태, 누락된 예외 케이스가 있는가?
- 업무 연동 경계, 업무 데이터, 외부 채널, 실패 대응, 운영 영향이 필요한 수준으로 드러나는가?

## 독립 검토 3개 관점 절차

1. 지정한 초안 폴더 또는 파일 경로를 검토 대상으로 확정한다.
2. 공통 입력 패키지를 구성한다.
   - 검토 대상 폴더 또는 파일 경로
   - 폴더 입력이면 기능설계서와 정책서 파일 경로
   - 본 `plan-review` 지침
   - `references/review-gate.md`
   - 담당 검토자 역할과 관점 범위
3. 새 검증 에이전트 3개를 생성해 각각 `독립 검토자`로 지정한다.
4. 검토자 3개를 병렬로 실행한다.
   - 근거 검토자: 기존 Confluence 원문과의 충돌, 근거 없는 가정, `[가정]`, stale/archive 근거의 발행 영향 확인
   - 결정·범위 검토자: `[미정]`, 결정 누락, 결정 주체/후속 액션, 적용/비적용/예외 범위, 관련 정책서/기능설계서 문서 연결 확인
   - 실행·검증 가능성 검토자: 개발·운영·QA 착수 가능성, 모호한 조건, 상태·예외·권한, 업무 연동 경계, 업무 데이터, 외부 채널, 실패 대응, 운영 영향 확인
5. 각 검토자는 검토 대상 파일을 직접 읽고, 초안에 명시된 관련 문서와 필요한 최소 Confluence 원문만 추가로 읽는다. 폴더 입력 또는 짝문서가 있는 단일 파일 입력이면 기능설계서와 정책서를 모두 읽는다.
6. 각 검토자는 현재 대화 컨텍스트를 근거로 사용하지 않는다. 대화에서 알게 된 배경, 의도, 작성 당시 판단은 파일 또는 근거 문서에 없으면 `[미정]` 또는 근거 없는 가정으로 본다.
7. 각 검토자는 `pass`, `conditional pass`, `수정 필요` 중 하나를 관점별 검토 결과로 낸다.
8. 현재 컨텍스트는 검토자 결과를 취합하되, 근거 없이 검토 결과를 완화하지 않는다. 최종 검토 결과는 더 보수적인 검토 결과를 사용한다.
   - `수정 필요 > conditional pass > pass`
   - 검토자 중 1개라도 `수정 필요`이면 최종 검토 결과는 `수정 필요`
   - `수정 필요`가 없고 1개라도 `conditional pass`이면 최종 검토 결과는 `conditional pass`
   - 3개 검토자가 모두 `pass`일 때만 최종 검토 결과는 `pass`

새 검증 에이전트 3개를 병렬 생성할 수 없는 실행 환경에서는 `pass`를 반환하지 않는다. 이 경우 검증 방식 제한을 명시하고 `conditional pass` 또는 `수정 필요`로 결론낸다.

## 출력 형식

### pass
```
✅ 검토 완료 — pass

검증 방식: 독립 검토 3개 관점
검토 대상: [파일경로]
읽은 근거 문서:
- source-id: [source-id] / raw exported Markdown path: [파일경로] / status: current / stale: no
관점별 검토 결과:
- 근거 검토자: pass
- 결정·범위 검토자: pass
- 실행·검증 가능성 검토자: pass

팀의 외부 발행 절차에 따라 Confluence 반영 여부를 결정하세요.
```

### 조건부 pass
```
✅ 검토 완료 — conditional pass

검증 방식: 독립 검토 3개 관점
검토 대상: [파일경로]
읽은 근거 문서:
- source-id: [source-id 또는 metadata unavailable] / raw exported Markdown path: [파일경로 또는 metadata unavailable] / status: [current/draft/archive 또는 metadata unavailable] / stale: [yes/no/metadata unavailable]
관점별 검토 결과:
- 근거 검토자: [pass / conditional pass]
- 결정·범위 검토자: [pass / conditional pass]
- 실행·검증 가능성 검토자: [pass / conditional pass]

[조건]: [발행 전에 기획자가 명시적으로 확인해야 할 내용]

조건을 확인한 뒤 팀의 외부 발행 절차를 진행하세요.
```

### 수정 필요
```
⚠️ 수정 필요

검증 방식: 독립 검토 3개 관점
검토 대상: [파일경로]
읽은 근거 문서:
- source-id: [source-id 또는 metadata unavailable] / raw exported Markdown path: [파일경로 또는 metadata unavailable] / status: [current/draft/archive 또는 metadata unavailable] / stale: [yes/no/metadata unavailable]
관점별 검토 결과:
- 근거 검토자: [pass / conditional pass / 수정 필요]
- 결정·범위 검토자: [pass / conditional pass / 수정 필요]
- 실행·검증 가능성 검토자: [pass / conditional pass / 수정 필요]

[관점]: [이유]
→ [수정 포인트]

[관점]: [이유]
→ [수정 포인트]

수정 후 다시 /product-team-kit:plan-review 를 실행하세요.
```

## 규칙

- 검토는 지정한 초안 폴더 또는 파일을 독립 검토자 3개 관점이 직접 읽어서 수행한다
- 초안 폴더를 받으면 기능설계서와 정책서를 함께 검토한다
- 단일 파일을 받더라도 같은 폴더의 짝문서가 있으면 함께 읽고, 역할명·범위·정책 기준이 두 문서에서 충돌하지 않는지 확인한다
- 3개 검토자는 근거 검토자, 결정·범위 검토자, 실행·검증 가능성 검토자로 나눈다
- 로컬 Confluence 파일을 추가로 읽어 근거를 확인할 수 있다
- 수정이 필요한 경우 직접 수정하지 않는다. 수정 포인트만 제시한다
- 현재 대화 컨텍스트를 근거로 사용하지 않는다
- 현재 컨텍스트와 검토자 판단이 다르면 더 보수적인 검토 결과를 최종 검토 결과로 사용한다
- `[미정]`, `[가정]`, 충돌 경고가 publish를 막을 정도인지 판단하고 pass / conditional pass / 수정 필요 중 하나로 결론낸다
- `metadata unavailable`, stale 확인 불가, raw exported Markdown 미확인 상태에서는 `pass`를 반환하지 않는다
- 상위설계서는 지원하지 않는다. 기능설계서와 정책서만 검토한다
