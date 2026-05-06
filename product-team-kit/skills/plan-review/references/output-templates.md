# Output Templates

`plan-review`의 최종 출력 단일 기준이다. 최종 취합자는 `review-gate.md`의 판정과 합성 규칙을 적용한 뒤 아래 템플릿 중 하나를 사용한다.

출력은 기획팀이 먼저 읽는 사람용 리포트와 하단의 상세 검토 기록으로 나눈다. 사람용 리포트에는 판정, 한 줄 결론, 먼저 할 일, 역할별 착수 가능성, 기준 문서 충돌을 먼저 둔다. `publish_readiness`, `review_repair`, Coverage, 근거 메타데이터는 삭제하지 않고 하단 상세 검토 기록에 둔다.

상단 라벨은 기획팀용 한국어를 우선한다.

| 내부 값 | 상단 표시 |
|---|---|
| `pass` | 통과 |
| `conditional pass` | 조건부 통과 |
| `수정 필요` | 수정 필요 |
| unsupported input | 올바른 검토 대상이 아님 |

역할별 착수 판단은 아래 라벨을 사용한다.

| 내부 값 | 기획자용 라벨 | 의미 |
|---|---|---|
| `ready` | 착수 가능 | 추가 확인 없이 다음 업무 시작 가능 |
| `conditional` | 확인 후 착수 가능 | 기획자가 조건을 확인하면 시작 가능 |
| `blocked` | 착수 전 보강 필요 | 문서 수정 없이는 해당 역할 판단이 달라질 수 있음 |
| `n/a` | 해당 없음 | 해당 역할 업무에 실질 영향 없음 |

상단 발견 항목은 업무 라벨을 사용한다. 내부 severity 값은 상세 검토 기록에 유지한다.

| 내부 severity | 상단 표시 |
|---|---|
| `P0` / `P1` | 필수 수정 |
| `P2` | 발행 전 확인 |
| `P3` | 참고 |

## pass

````text
판정: 통과
검토 대상: [파일경로]

한 줄 결론:
- 기준 문서와 충돌이 없고, 적용 대상 역할이 다음 업무를 시작할 수 있습니다.

먼저 할 일:
1. 기능/화면설계서와 정책서 묶음이 팀에 공유할 대상인지 최종 확인하세요.
2. 팀의 외부 반영 절차에 따라 문서 반영 여부를 결정하세요.

역할별 착수 가능성:
| 역할 | 착수 판단 | 이유 | 필요한 보강 또는 확인 | 위치 |
|---|---|---|---|---|
| 디자인 | [착수 가능 또는 해당 없음] | [화면/문구/상태 판단 요약 또는 UI 영향 없음 사유] | 없음 | [섹션 또는 없음] |
| 개발 | 착수 가능 | [상태/권한/예외/연동 판단 요약] | 없음 | [섹션 또는 없음] |
| QA | 착수 가능 | [전제조건/기대 결과/예외 확인 기준 요약] | 없음 | [섹션 또는 없음] |
| 운영 | 착수 가능 | [운영 처리/공지/로그/전환 영향 판단 요약] | 없음 | [섹션 또는 없음] |

기준 문서와의 충돌:
| 항목 | 초안 내용 | 기준 문서 | 판단 |
|---|---|---|---|
| 없음 | 없음 | [사용한 기준 문서 요약] | 충돌 없음 |

상세 검토 기록:

검토 기준: 기준 문서(Product Docs SSOT) 근거 패키지 기반 2개 관점 검토

Coverage:
| 관점 | 상태 | 발견 항목 수 | 근거 |
|---|---|---:|---|
| 기준 문서 충돌 | completed | [최종 합성 후 출력에 남는 필수 수정 + 발행 전 확인 + 참고의 합계] | Product Docs SSOT |
| 업무 착수 가능성 | completed | [최종 합성 후 출력에 남는 필수 수정 + 발행 전 확인 + 참고의 합계] | 근거 패키지 사용 |

읽은 근거:
- path: [프로젝트 상대 경로] / kind: [markdown|linked_local_resource] / source_type: [policy|prd|requirement|feature|screen|operations|qa|unknown] / role: [primary|supporting|conflict_candidate|context_only] / version: [vX.Y|unversioned|unknown] / current_evidence: [true|false] / status: [current|draft|archive|deprecated|unknown] / freshness: [explicit_current|dated|undated|unknown]
읽지 않은 관련 후보: 없음
제외된 후보:
- [외부 URL, 코드, 설정, planning 하위 등 / 제외 사유 또는 없음]
검증 한계: 없음

필수 수정 항목: 없음
발행 전 확인 항목: 없음
참고 사항:
| 내부 관점 | 제목 | 위치 | 내부 심각도 | 발견 유형 | 신뢰도 앵커 | 영향 | 근거 인용 | 관찰 | 출력 버킷 |
|---|---|---|---|---|---:|---|---|---|---|
| [관점 또는 없음] | [제목 또는 없음] | [문서 > 섹션 또는 없음] | [P3 또는 없음] | [오류/누락 또는 없음] | [50/75/100 또는 없음] | [영향 또는 없음] | [짧은 인용 또는 없음] | [관찰 또는 없음] | [참고 또는 없음] |

발행 준비 상세:
```yaml
publish_readiness:
  status: ready
  target_path: "[검토 대상 경로]"
  review_result: "pass"
  draft_paths:
    feature_doc_path: "[기능설계서 경로]"
    policy_doc_path: "[정책서 경로]"
  evidence_status: "completed"
  publish_candidate:
    destination: "external process"
    team_doc_candidate: "[문서명 또는 unknown]"
    freshness_risk: "none"
  downstream_readiness:
    design: "[ready|n/a]"
    development: "ready"
    qa: "ready"
    operations: "ready"
  remaining_conditions:
    - "없음"
  human_checklist:
    - "검토 대상 초안의 기능설계서/정책서 쌍을 확인한다."
    - "팀 문서 반영 후 팀 문서 ID와 update timestamp를 별도 운영 기록에 남긴다."
  forbidden_actions:
    - "plan-review가 외부 시스템에 직접 게시하지 않는다."
    - "planning/ 산출물을 Product Docs SSOT 근거로 승격하지 않는다."
    - "Product Docs SSOT Markdown 또는 팀 문서 export snapshot을 자동 수정하지 않는다."
```

관점별 검토 결과:
- 기준 문서 충돌 검토자: pass
- 업무 착수 가능성 검토자: pass
````

## conditional pass

````text
판정: 조건부 통과
검토 대상: [파일경로]

한 줄 결론:
- 문서 수정 없이 발행 후보가 될 수 있지만, 발행 전에 기획자가 명시적으로 확인해야 할 항목이 남아 있습니다.

먼저 할 일:
1. 아래 `발행 전 확인 항목`을 확인하고 수용 여부를 명시하세요.
2. 확인 내용이 앞으로 기준이 되어야 하면 초안 또는 기준 문서(Product Docs SSOT)에 반영한 뒤 외부 반영 절차를 진행하세요.

역할별 착수 가능성:
| 역할 | 착수 판단 | 이유 | 필요한 보강 또는 확인 | 위치 |
|---|---|---|---|---|
| 디자인 | [착수 가능|확인 후 착수 가능|해당 없음] | [이유] | [확인 항목 또는 없음] | [섹션 또는 없음] |
| 개발 | [착수 가능|확인 후 착수 가능|해당 없음] | [이유] | [확인 항목 또는 없음] | [섹션 또는 없음] |
| QA | [착수 가능|확인 후 착수 가능|해당 없음] | [이유] | [확인 항목 또는 없음] | [섹션 또는 없음] |
| 운영 | [착수 가능|확인 후 착수 가능|해당 없음] | [이유] | [확인 항목 또는 없음] | [섹션 또는 없음] |

기준 문서와의 충돌:
| 항목 | 초안 내용 | 기준 문서 | 판단 |
|---|---|---|---|
| [항목 또는 없음] | [초안 내용 또는 없음] | [기준 문서 요약 또는 없음] | [충돌 없음 또는 확인 필요] |

발행 전 확인 항목:
| ID | 구분 | 위치 | 확인할 내용 | 확인 후 처리 |
|---|---|---|---|---|
| COND-001 | 발행 전 확인 | [문서 > 섹션] | [기획자가 확인해야 할 내용] | [문서 반영 필요 여부] |

상세 검토 기록:

검토 기준: 기준 문서(Product Docs SSOT) 근거 패키지 기반 2개 관점 검토

Coverage:
| 관점 | 상태 | 발견 항목 수 | 근거 |
|---|---|---:|---|
| 기준 문서 충돌 | [completed / limited] | [최종 합성 후 출력에 남는 필수 수정 + 발행 전 확인 + 참고의 합계] | [읽은 근거 요약] |
| 업무 착수 가능성 | [completed / limited] | [최종 합성 후 출력에 남는 필수 수정 + 발행 전 확인 + 참고의 합계] | 근거 패키지 사용 |

읽은 근거:
- path: [프로젝트 상대 경로] / kind: [markdown|linked_local_resource] / source_type: [policy|prd|requirement|feature|screen|operations|qa|unknown] / role: [primary|supporting|conflict_candidate|context_only] / version: [vX.Y|unversioned|unknown] / current_evidence: [true|false] / status: [current|draft|archive|deprecated|unknown] / freshness: [explicit_current|dated|undated|unknown]
읽지 않은 관련 후보:
- [후보 문서 또는 resource / 읽지 않은 이유 또는 없음]
제외된 후보:
- [외부 URL, 코드, 설정, planning 하위 등 / 제외 사유 또는 없음]
검증 한계:
- [관련 Markdown 부재, local resource 미확인, status/freshness unknown, 독립 컨텍스트 제한 등 또는 없음]

필수 수정 항목: 없음
발행 전 확인 항목 상세:
| 내부 관점 | 제목 | 위치 | 내부 심각도 | 발견 유형 | 신뢰도 앵커 | 영향 | 근거 인용 | 확인 조건 | 출력 버킷 |
|---|---|---|---|---|---:|---|---|---|---|
| [관점] | [제목] | [문서 > 섹션] | P2 | [오류/누락] | [50/75/100] | [영향] | [짧은 인용] | [발행 전 확인 조건. 문서 반영 필요 여부 포함] | 발행 전 확인 |
참고 사항:
| 내부 관점 | 제목 | 위치 | 내부 심각도 | 발견 유형 | 신뢰도 앵커 | 영향 | 근거 인용 | 관찰 | 출력 버킷 |
|---|---|---|---|---|---:|---|---|---|---|
| [관점] | [제목] | [문서 > 섹션] | P3 | [오류/누락] | [50/75/100] | [영향] | [짧은 인용] | [관찰 또는 없음] | 참고 |

발행 준비 상세:
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
    freshness_risk: "[none|unknown|limited]"
  downstream_readiness:
    design: "[ready|conditional|n/a]"
    development: "[ready|conditional|n/a]"
    qa: "[ready|conditional|n/a]"
    operations: "[ready|conditional|n/a]"
  remaining_conditions:
    - "[conditional pass의 확인 조건]"
  human_checklist:
    - "검토 대상 초안의 기능설계서/정책서 쌍을 확인한다."
    - "남은 확인 조건을 기획자가 명시적으로 수용했는지 확인한다."
    - "팀 문서 반영 후 팀 문서 ID와 update timestamp를 별도 운영 기록에 남긴다."
  forbidden_actions:
    - "plan-review가 외부 시스템에 직접 게시하지 않는다."
    - "planning/ 산출물을 Product Docs SSOT 근거로 승격하지 않는다."
    - "Product Docs SSOT Markdown 또는 팀 문서 export snapshot을 자동 수정하지 않는다."
```

관점별 검토 결과:
- 기준 문서 충돌 검토자: [pass / conditional pass]
- 업무 착수 가능성 검토자: [pass / conditional pass]
````

## 수정 필요

````text
판정: 수정 필요
검토 대상: [파일경로]

한 줄 결론:
- 기준 문서와의 충돌, 필수 정보 누락, 또는 역할별 착수 차단 항목이 있어 발행 전에 초안 수정이 필요합니다.

먼저 고칠 항목:
1. [FIX-001: 문서 > 섹션 / 어떻게 고칠지]
2. [FIX-002: 문서 > 섹션 / 어떻게 고칠지 또는 없음]
3. 수정 후 같은 경로로 plan-review를 다시 실행하세요.

역할별 착수 가능성:
| 역할 | 착수 판단 | 이유 | 필요한 보강 또는 확인 | 위치 |
|---|---|---|---|---|
| 디자인 | [착수 가능|확인 후 착수 가능|착수 전 보강 필요|해당 없음] | [이유] | [보강 또는 확인 항목] | [섹션 또는 없음] |
| 개발 | [착수 가능|확인 후 착수 가능|착수 전 보강 필요|해당 없음] | [이유] | [보강 또는 확인 항목] | [섹션 또는 없음] |
| QA | [착수 가능|확인 후 착수 가능|착수 전 보강 필요|해당 없음] | [이유] | [보강 또는 확인 항목] | [섹션 또는 없음] |
| 운영 | [착수 가능|확인 후 착수 가능|착수 전 보강 필요|해당 없음] | [이유] | [보강 또는 확인 항목] | [섹션 또는 없음] |

기준 문서와의 충돌:
| 항목 | 초안 내용 | 기준 문서 | 판단 |
|---|---|---|---|
| [항목 또는 없음] | [초안 내용 또는 없음] | [기준 문서 요약 또는 없음] | [충돌 / 근거 부족 / 확인 필요] |

필수 수정 항목:
| ID | 구분 | 위치 | 왜 문제인지 | 어떻게 고칠지 |
|---|---|---|---|---|
| FIX-001 | 필수 수정 | [문서 > 섹션] | [디자인/개발/QA/운영 판단에 미치는 영향] | [최소 수정 포인트] |

발행 전 확인 항목:
| ID | 구분 | 위치 | 확인할 내용 | 확인 후 처리 |
|---|---|---|---|---|
| COND-001 또는 없음 | 발행 전 확인 | [문서 > 섹션 또는 없음] | [조건 또는 없음] | [문서 반영 필요 여부 또는 없음] |

상세 검토 기록:

검토 기준: 기준 문서(Product Docs SSOT) 근거 패키지 기반 2개 관점 검토

Coverage:
| 관점 | 상태 | 발견 항목 수 | 근거 |
|---|---|---:|---|
| 기준 문서 충돌 | [completed / limited / failed] | [최종 합성 후 출력에 남는 필수 수정 + 발행 전 확인 + 참고의 합계] | [읽은 근거 요약] |
| 업무 착수 가능성 | [completed / limited / failed] | [최종 합성 후 출력에 남는 필수 수정 + 발행 전 확인 + 참고의 합계] | 근거 패키지 사용 |

읽은 근거:
- path: [프로젝트 상대 경로] / kind: [markdown|linked_local_resource] / source_type: [policy|prd|requirement|feature|screen|operations|qa|unknown] / role: [primary|supporting|conflict_candidate|context_only] / version: [vX.Y|unversioned|unknown] / current_evidence: [true|false] / status: [current|draft|archive|deprecated|unknown] / freshness: [explicit_current|dated|undated|unknown]
읽지 않은 관련 후보:
- [후보 문서 또는 resource / 읽지 않은 이유 또는 없음]
제외된 후보:
- [외부 URL, 코드, 설정, planning 하위 등 / 제외 사유 또는 없음]
검증 한계:
- [관련 Markdown 부재, local resource 미확인, status/freshness unknown, 독립 컨텍스트 제한 등 또는 없음]

필수 수정 항목 상세:
| 내부 관점 | 제목 | 위치 | 내부 심각도 | 발견 유형 | 신뢰도 앵커 | 영향 | 근거 인용 | 최소 수정 포인트 | 출력 버킷 |
|---|---|---|---|---|---:|---|---|---|---|
| [관점] | [제목] | [문서 > 섹션] | [P0/P1] | [오류/누락] | [50/75/100] | [영향] | [짧은 인용] | [수정 포인트] | 필수 수정 |
발행 전 확인 항목 상세:
| 내부 관점 | 제목 | 위치 | 내부 심각도 | 발견 유형 | 신뢰도 앵커 | 영향 | 근거 인용 | 확인 조건 | 출력 버킷 |
|---|---|---|---|---|---:|---|---|---|---|
| [관점] | [제목] | [문서 > 섹션] | P2 | [오류/누락] | [50/75/100] | [영향] | [짧은 인용] | [조건 또는 없음] | 발행 전 확인 |
참고 사항:
| 내부 관점 | 제목 | 위치 | 내부 심각도 | 발견 유형 | 신뢰도 앵커 | 영향 | 근거 인용 | 관찰 | 출력 버킷 |
|---|---|---|---|---|---:|---|---|---|---|
| [관점] | [제목] | [문서 > 섹션] | P3 | [오류/누락] | [50/75/100] | [영향] | [짧은 인용] | [관찰 또는 없음] | 참고 |

재검토용 상세 정보:
```yaml
review_repair:
  status: review-repair-needed
  target_path: "[검토 대상 경로]"
  review_result: "수정 필요"
  editable_scope:
    - "planning/ 하위 검토 대상 초안"
  forbidden_scope:
    - "Product Docs SSOT Markdown"
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
- 기준 문서 충돌 검토자: [pass / conditional pass / 수정 필요 / failed: 결과 없음]
- 업무 착수 가능성 검토자: [pass / conditional pass / 수정 필요 / failed: 결과 없음]

`failed: 결과 없음`이 있으면 최종 결과는 P0 `수정 필요`로 고정한다.
````

## 올바른 검토 대상이 아님

```text
올바른 검토 대상이 아님

검토 대상: [파일경로]
사유: plan-review는 plan-format으로 작성한 기능/화면설계서 또는 정책서 초안만 검토합니다. 상위설계서나 다른 문서 타입은 이 gate의 지원 대상이 아닙니다.

다음 행동:
1. 기능/화면설계서와 정책서 초안 폴더를 지정하세요.
2. 단일 파일을 지정할 경우 같은 폴더에 짝문서가 있는지 확인하세요.
3. Claude Code: /product-team-kit:plan-review <초안 폴더 또는 기능설계서/정책서 파일경로>
4. Codex: $plan-review <초안 폴더 또는 기능설계서/정책서 파일경로>
```
