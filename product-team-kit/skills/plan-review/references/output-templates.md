# Output Templates

`plan-review`의 최종 출력 단일 기준이다. 최종 취합자는 `review-gate.md`의 판정과 합성 규칙을 적용한 뒤 아래 템플릿 중 하나를 사용한다. `pass`와 `conditional pass` 결과의 발행 준비 증적은 `publish-readiness-contract.md`, `수정 필요` 결과의 수정 작업 블록은 `review-rerun-contract.md`를 따른다.

Coverage의 `구조화된 발견 사항`은 필수 필드가 유효하고 최종 합성 후 출력에 남는 수정 포인트, 확인 조건, 참고 관찰의 합계다.

## pass

````text
검토 완료 - pass

검증 방식: Project Docs SSOT 근거 패키지 기반 3개 관점 검토
검토 대상: [파일경로]
다음 행동: 팀의 외부 발행 절차에 따라 반영 여부를 결정하세요.

발행 준비 증적:
```yaml
publish_readiness:
  status: ready
  target_path: "[검토 대상 경로]"
  review_result: "pass"
  draft_paths:
    feature_doc_path: "[기능설계서 경로 또는 없음]"
    policy_doc_path: "[정책서 경로 또는 없음]"
  evidence_status: "completed"
  publish_candidate:
    destination: "external process"
    team_doc_candidate: "[문서명 또는 unknown]"
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

Coverage:
| 관점 | 상태 | 구조화된 발견 사항 | 근거 |
|---|---|---:|---|
| 근거 | completed | [최종 합성 후 출력에 남는 수정 포인트 + 확인 조건 + 참고 관찰의 합계] | Project Docs SSOT |
| 결정·범위 | completed | [최종 합성 후 출력에 남는 수정 포인트 + 확인 조건 + 참고 관찰의 합계] | 근거 패키지 사용 |
| 실행·검증 가능성 | completed | [최종 합성 후 출력에 남는 수정 포인트 + 확인 조건 + 참고 관찰의 합계] | 근거 패키지 사용 |

읽은 근거:
- path: [프로젝트 상대 경로] / kind: [markdown|linked_local_resource] / role: [primary|supporting|conflict_candidate|context_only] / status: [current|draft|archive|deprecated|unknown] / freshness: [explicit_current|dated|undated|unknown]
읽지 않은 관련 후보: 없음
제외된 후보:
- [외부 URL, 코드, 설정, planning 하위 등 / 제외 사유 또는 없음]
검증 한계: 없음

수정 포인트: 없음
확인 조건: 없음
참고 관찰:
| 관점 | 제목 | 위치 | 심각도 | 발견 유형 | 신뢰도 앵커 | 영향 | 근거 인용 | 관찰 | 출력 버킷 |
|---|---|---|---|---|---:|---|---|---|---|
| [관점 또는 없음] | [제목 또는 없음] | [문서 > 섹션 또는 없음] | [P3 또는 없음] | [오류/누락 또는 없음] | [50/75/100 또는 없음] | [영향 또는 없음] | [짧은 인용 또는 없음] | [관찰 또는 없음] | [참고 관찰 또는 없음] |

관점별 검토 결과:
- 근거 검토자: pass
- 결정·범위 검토자: pass
- 실행·검증 가능성 검토자: pass
````

## conditional pass

````text
검토 완료 - conditional pass

검증 방식: Project Docs SSOT 근거 패키지 기반 3개 관점 검토
검토 대상: [파일경로]
다음 행동: 확인 조건을 기획자가 명시적으로 확인하세요. 확인 내용이 향후 근거가 되어야 하면 초안 또는 Project Docs SSOT 문서에 반영한 뒤 팀의 외부 발행 절차를 진행하세요.

발행 준비 증적:
```yaml
publish_readiness:
  status: conditional
  target_path: "[검토 대상 경로]"
  review_result: "conditional pass"
  draft_paths:
    feature_doc_path: "[기능설계서 경로 또는 없음]"
    policy_doc_path: "[정책서 경로 또는 없음]"
  evidence_status: "[completed|limited]"
  publish_candidate:
    destination: "external process"
    team_doc_candidate: "[문서명 또는 unknown]"
    freshness_risk: "[unknown|limited]"
  remaining_conditions:
    - "[conditional pass의 확인 조건]"
  human_checklist:
    - "검토 대상 초안의 기능설계서/정책서 쌍을 확인한다."
    - "남은 확인 조건을 기획자가 명시적으로 수용했는지 확인한다."
    - "팀 문서 반영 후 팀 문서 ID와 update timestamp를 별도 운영 기록에 남긴다."
  forbidden_actions:
    - "plan-review가 외부 시스템에 직접 게시하지 않는다."
    - "planning/ 산출물을 Project Docs SSOT 근거로 승격하지 않는다."
    - "Project Docs SSOT Markdown 또는 팀 문서 export snapshot을 자동 수정하지 않는다."
```

Coverage:
| 관점 | 상태 | 구조화된 발견 사항 | 근거 |
|---|---|---:|---|
| 근거 | [completed / limited] | [최종 합성 후 출력에 남는 수정 포인트 + 확인 조건 + 참고 관찰의 합계] | [읽은 근거 요약] |
| 결정·범위 | [completed / limited] | [최종 합성 후 출력에 남는 수정 포인트 + 확인 조건 + 참고 관찰의 합계] | 근거 패키지 사용 |
| 실행·검증 가능성 | [completed / limited] | [최종 합성 후 출력에 남는 수정 포인트 + 확인 조건 + 참고 관찰의 합계] | 근거 패키지 사용 |

읽은 근거:
- path: [프로젝트 상대 경로] / kind: [markdown|linked_local_resource] / role: [primary|supporting|conflict_candidate|context_only] / status: [current|draft|archive|deprecated|unknown] / freshness: [explicit_current|dated|undated|unknown]
읽지 않은 관련 후보:
- [후보 문서 또는 resource / 읽지 않은 이유 또는 없음]
제외된 후보:
- [외부 URL, 코드, 설정, planning 하위 등 / 제외 사유 또는 없음]
검증 한계:
- [관련 Markdown 부재, local resource 미확인, status/freshness unknown, 독립 컨텍스트 제한 등 또는 없음]

수정 포인트: 없음
확인 조건:
| 관점 | 제목 | 위치 | 심각도 | 발견 유형 | 신뢰도 앵커 | 영향 | 근거 인용 | 확인 조건 | 출력 버킷 |
|---|---|---|---|---|---:|---|---|---|---|
| [관점] | [제목] | [문서 > 섹션] | P2 | [오류/누락] | [50/75/100] | [영향] | [짧은 인용] | [발행 전 확인 조건. 문서 반영 필요 여부 포함] | 확인 조건 |
참고 관찰:
| 관점 | 제목 | 위치 | 심각도 | 발견 유형 | 신뢰도 앵커 | 영향 | 근거 인용 | 관찰 | 출력 버킷 |
|---|---|---|---|---|---:|---|---|---|---|
| [관점] | [제목] | [문서 > 섹션] | P3 | [오류/누락] | [50/75/100] | [영향] | [짧은 인용] | [관찰 또는 없음] | 참고 관찰 |

관점별 검토 결과:
- 근거 검토자: [pass / conditional pass]
- 결정·범위 검토자: [pass / conditional pass]
- 실행·검증 가능성 검토자: [pass / conditional pass]

[조건]: [발행 전에 기획자가 명시적으로 확인해야 할 내용]
````

## 수정 필요

````text
수정 필요

검증 방식: Project Docs SSOT 근거 패키지 기반 3개 관점 검토
검토 대상: [파일경로]
다음 행동: 수정 포인트를 반영한 뒤 다시 실행하세요.
- Claude Code: /product-team-kit:plan-review <경로>
- Codex: $plan-review <경로>

Coverage:
| 관점 | 상태 | 구조화된 발견 사항 | 근거 |
|---|---|---:|---|
| 근거 | [completed / limited / failed] | [최종 합성 후 출력에 남는 수정 포인트 + 확인 조건 + 참고 관찰의 합계] | [읽은 근거 요약] |
| 결정·범위 | [completed / limited / failed] | [최종 합성 후 출력에 남는 수정 포인트 + 확인 조건 + 참고 관찰의 합계] | 근거 패키지 사용 |
| 실행·검증 가능성 | [completed / limited / failed] | [최종 합성 후 출력에 남는 수정 포인트 + 확인 조건 + 참고 관찰의 합계] | 근거 패키지 사용 |

읽은 근거:
- path: [프로젝트 상대 경로] / kind: [markdown|linked_local_resource] / role: [primary|supporting|conflict_candidate|context_only] / status: [current|draft|archive|deprecated|unknown] / freshness: [explicit_current|dated|undated|unknown]
읽지 않은 관련 후보:
- [후보 문서 또는 resource / 읽지 않은 이유 또는 없음]
제외된 후보:
- [외부 URL, 코드, 설정, planning 하위 등 / 제외 사유 또는 없음]
검증 한계:
- [관련 Markdown 부재, local resource 미확인, status/freshness unknown, 독립 컨텍스트 제한 등 또는 없음]

수정 포인트:
| 관점 | 제목 | 위치 | 심각도 | 발견 유형 | 신뢰도 앵커 | 영향 | 근거 인용 | 최소 수정 포인트 | 출력 버킷 |
|---|---|---|---|---|---:|---|---|---|---|
| [관점] | [제목] | [문서 > 섹션] | [P0/P1] | [오류/누락] | [50/75/100] | [영향] | [짧은 인용] | [수정 포인트] | 수정 포인트 |
확인 조건:
| 관점 | 제목 | 위치 | 심각도 | 발견 유형 | 신뢰도 앵커 | 영향 | 근거 인용 | 확인 조건 | 출력 버킷 |
|---|---|---|---|---|---:|---|---|---|---|
| [관점] | [제목] | [문서 > 섹션] | P2 | [오류/누락] | [50/75/100] | [영향] | [짧은 인용] | [조건 또는 없음] | 확인 조건 |
참고 관찰:
| 관점 | 제목 | 위치 | 심각도 | 발견 유형 | 신뢰도 앵커 | 영향 | 근거 인용 | 관찰 | 출력 버킷 |
|---|---|---|---|---|---:|---|---|---|---|
| [관점] | [제목] | [문서 > 섹션] | P3 | [오류/누락] | [50/75/100] | [영향] | [짧은 인용] | [관찰 또는 없음] | 참고 관찰 |

수정 작업 블록:
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

관점별 검토 결과:
- 근거 검토자: [pass / conditional pass / 수정 필요 / failed: 결과 없음]
- 결정·범위 검토자: [pass / conditional pass / 수정 필요 / failed: 결과 없음]
- 실행·검증 가능성 검토자: [pass / conditional pass / 수정 필요 / failed: 결과 없음]

`failed: 결과 없음`이 있으면 최종 결과는 P0 `수정 필요`로 고정한다.
````

## 입력 오류 - 지원하지 않는 문서 타입

```text
입력 오류 - 지원하지 않는 문서 타입

검토 대상: [파일경로]
결과: 수정 필요
사유: plan-review는 plan-format으로 작성한 기능설계서 또는 정책서 초안만 검토합니다. 상위설계서나 다른 문서 타입은 이 gate의 지원 대상이 아닙니다.

다음 행동:
- 기능설계서/정책서 초안 폴더 또는 파일을 지정하세요.
- Claude Code: /product-team-kit:plan-review <초안 폴더 또는 기능설계서/정책서 파일경로>
- Codex: $plan-review <초안 폴더 또는 기능설계서/정책서 파일경로>
```
