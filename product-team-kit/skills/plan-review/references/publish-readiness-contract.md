# Publish Readiness Contract

`plan-review`가 발행 후보 결과를 반환할 때 외부 반영 전 사람이 확인할 정보를 구조화하기 위한 출력 계약이다. 이 계약은 readiness manifest이며, 외부 시스템 게시나 Project Docs SSOT 수정을 수행한다는 의미가 아니다.

## 적용 범위

- 적용: 최종 결과가 `pass` 또는 `conditional pass`인 경우.
- 비적용: `수정 필요`, 입력 오류 템플릿.
- `pass` 결과의 `status`는 `ready`로 기록한다.
- `conditional pass` 결과의 `status`는 `conditional`로 기록한다.

## 근거와 책임 경계

- `publish_readiness`는 검토 대상 파일, evidence package, 최종 review 출력만 근거로 채운다.
- 현재 대화 기억이나 외부 URL을 새 근거로 사용하지 않는다.
- `plan-review`는 외부 시스템에 직접 게시하지 않는다.
- Project Docs SSOT Markdown, 팀 문서 export snapshot, linked local resource를 자동 수정하지 않는다.
- `planning/` 산출물을 Project Docs SSOT 근거로 승격하지 않는다.
- 팀 문서 반영 후 page id, update timestamp, 담당자 같은 운영 기록은 별도 외부 절차에서 남긴다.

## 출력 위치

`output-templates.md`의 `pass`와 `conditional pass` 템플릿에서 `다음 행동` 다음, `Coverage` 앞에 YAML fenced block으로 포함한다. `수정 필요` 템플릿에는 포함하지 않는다.

```yaml
publish_readiness:
  status: ready | conditional
  target_path: "[검토 대상 경로]"
  review_result: "pass | conditional pass"
  draft_paths:
    feature_doc_path: "[기능설계서 경로 또는 없음]"
    policy_doc_path: "[정책서 경로 또는 없음]"
  evidence_status: "[completed|limited]"
  publish_candidate:
    destination: "external process"
    team_doc_candidate: "[문서명 또는 unknown]"
    freshness_risk: "[none|unknown|limited]"
  remaining_conditions:
    - "[conditional pass의 확인 조건 또는 없음]"
  human_checklist:
    - "검토 대상 초안의 기능설계서/정책서 쌍을 확인한다."
    - "남은 확인 조건을 기획자가 명시적으로 수용했는지 확인한다."
    - "팀 문서 반영 후 팀 문서 ID와 update timestamp를 별도 운영 기록에 남긴다."
  forbidden_actions:
    - "plan-review가 외부 시스템에 직접 게시하지 않는다."
    - "planning/ 산출물을 Project Docs SSOT 근거로 승격하지 않는다."
    - "Project Docs SSOT Markdown 또는 팀 문서 export snapshot을 자동 수정하지 않는다."
```

## 필드 작성 기준

- `target_path`: 사용자가 지정한 검토 대상 경로.
- `draft_paths.feature_doc_path` / `policy_doc_path`: 입력 확정 단계에서 식별한 기능설계서/정책서 경로. 없으면 `없음`.
- `evidence_status`: evidence package의 `status`. `pass`는 `completed`여야 하며, `conditional pass`는 `completed` 또는 `limited`일 수 있다.
- `team_doc_candidate`: 검토 대상 또는 근거에서 반영 후보 문서명을 식별할 수 있으면 문서명, 아니면 `unknown`.
- `freshness_risk`: 검증 한계가 없으면 `none`, freshness가 불명확하면 `unknown`, limited 상태나 미확인 근거가 있으면 `limited`.
- `remaining_conditions`: `pass`는 `없음`, `conditional pass`는 확인 조건을 요약한다.
