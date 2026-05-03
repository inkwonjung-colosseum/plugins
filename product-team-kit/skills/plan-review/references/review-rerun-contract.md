# Review Rerun Contract

`plan-review`가 `수정 필요`를 반환할 때 후속 수정 작업과 재검토를 구조화하기 위한 계약이다. 이 계약은 출력 계약이며, `plan-review`가 파일을 직접 수정한다는 의미가 아니다.

## 적용 범위

- 적용: 최종 결과가 `수정 필요`인 경우.
- 비적용: `pass`, `conditional pass`, 입력 오류 템플릿.
- 수정 대상으로 제안할 수 있는 범위: `planning/` 하위의 검토 대상 기능설계서/정책서 초안.
- 수정 대상으로 제안하지 않는 범위: Project Docs SSOT Markdown, 팀 문서 export snapshot, linked local resource, 코드, 테스트, 설정 파일.
- Project Docs SSOT Markdown은 수정 대상으로 제안하지 않는다.

## 수정 근거

- 수정 작업 블록은 최종 합성 후 출력에 남은 P0/P1 `수정 포인트`만 포함한다.
- P2 `확인 조건`과 P3 `참고 관찰`은 `findings`에 넣지 않는다.
- 현재 대화 컨텍스트, 작성 당시 기억, 외부 URL, 코드, 테스트, 설정 파일을 수정 근거로 사용하지 않는다.
- 검토 대상 파일 또는 Project Docs SSOT 근거에 없는 내용은 새 사실로 추가하지 않고 `[확인 필요]`로 남기도록 요구한다.

## Finding ID

- 최종 합성 후 출력에 남은 P0/P1 수정 포인트 순서대로 `FIX-001`, `FIX-002`, `FIX-003` 형식으로 부여한다.
- 같은 발견 사항이 dedup 규칙으로 병합되면 병합 후 하나의 id만 부여한다.
- id는 해당 `plan-review` 출력 안에서만 안정적이면 된다.

## 출력 블록

`output-templates.md`의 `수정 필요` 템플릿에서 `참고 관찰` 표 다음, `관점별 검토 결과` 앞에 아래 YAML fenced block을 포함한다.

```yaml
review_repair:
  status: review-repair-needed
  target_path: "[검토 대상 경로]"
  review_result: "수정 필요"
  editable_scope:
    - "planning/ 하위 검토 대상 초안"
  forbidden_scope:
    - "Project Docs SSOT Markdown"
    - "팀 문서 export snapshot"
    - "linked local resource"
    - "코드, 테스트, 설정 파일"
  constraints:
    - "초안을 직접 고칠 때도 새 사실을 만들지 않는다."
    - "근거 인용 또는 검토 대상 본문에 없는 내용은 [확인 필요]로 남긴다."
    - "수정 후 같은 경로로 plan-review를 다시 실행한다."
  findings:
    - id: "FIX-001"
      severity: "[P0/P1]"
      target: "[문서 > 섹션]"
      title: "[제목]"
      evidence_quote: "[짧은 근거 인용]"
      required_change: "[최소 수정 포인트]"
      acceptance_check: "[수정 후 충족해야 할 확인 기준]"
  rerun:
    claude: "/product-team-kit:plan-review [검토 대상 경로]"
    codex: "$plan-review [검토 대상 경로]"
```

## Acceptance Check 작성 기준

`acceptance_check`는 후속 수정자가 수정 완료 여부를 확인할 수 있는 한 문장으로 쓴다.

- 좋은 예: `기능설계서 6. 권한과 데이터 접근에 승인자 역할과 가능한 행위가 명시되어 있다.`
- 나쁜 예: `권한을 잘 정리한다.`
