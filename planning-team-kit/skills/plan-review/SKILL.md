---
name: plan-review
description: "Review a planning draft from plan-draft for evidence, scope, and implementation readiness before publish."
---

# plan-review

`/planning-team-kit:plan-draft`으로 생성한 초안을 3개 관점으로 검토하는 선택 스킬.

## 호출

- Claude Code: `/planning-team-kit:plan-review`
- Codex: `$plan-review`

## 언제 사용하나

- 중요한 정책 변경이나 신규 기능 설계서를 Confluence에 반영하기 전 품질을 확인하고 싶을 때
- 초안이 clean 상태이면 건너뛸 수 있다. `/planning-team-kit:plan-draft` 후 바로 `/planning-team-kit:plan-publish` 가능
- 초안에 `[미정]`, `[가정]`, 기존 문서와의 충돌 경고가 남아 있으면 publish 전에 필수로 사용한다

## 검토 관점 (3개)

검토 기준과 verdict 경계는 `references/review-gate.md`를 따른다.

### ① 근거
- 기존 Confluence 문서 내용과 충돌하는 부분이 있는가?
- `[가정]` 태그가 붙은 항목 중 실제로 확인이 필요한 것은 무엇인가?

### ② 범위
- 이 문서에서 결정해야 할 사항이 모두 담겼는가?
- 빠진 섹션이나 `[미정]` 항목이 남아 있는가?

### ③ 실행
- 개발팀이 이 문서만 보고 구현을 시작할 수 있는가?
- 모호한 조건, 정의되지 않은 상태, 누락된 예외 케이스가 있는가?

## 출력 형식

### pass
```
✅ 검토 완료 — pass

/planning-team-kit:plan-publish 로 Confluence에 반영하세요.
```

### 조건부 pass
```
✅ 검토 완료 — conditional pass

[조건]: [publish 전에 기획자가 명시적으로 확인해야 할 내용]

조건을 확인한 뒤 /planning-team-kit:plan-publish 진행하세요.
```

### 수정 필요
```
⚠️ 수정 필요

[관점]: [이유]
→ [수정 포인트]

[관점]: [이유]
→ [수정 포인트]

수정 후 /planning-team-kit:plan-publish 진행하세요.
```

## 규칙

- 검토는 현재 대화 컨텍스트의 초안을 기준으로 한다
- 로컬 Confluence 파일을 추가로 읽어 근거를 확인할 수 있다
- 수정이 필요한 경우 직접 수정하지 않는다. 수정 포인트만 제시한다
- `[미정]`, `[가정]`, 충돌 경고가 publish를 막을 정도인지 판단하고 pass / conditional pass / 수정 필요 중 하나로 결론낸다
