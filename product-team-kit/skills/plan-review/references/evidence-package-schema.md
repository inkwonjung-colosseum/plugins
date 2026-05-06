# Evidence Package Schema

근거 검토자는 아래 YAML 형식으로 근거 패키지를 반환한다. 실행·검증 가능성 검토자와 최종 취합자는 이 패키지 밖의 내용을 새 사실로 확정하지 않는다.

Product Docs SSOT는 `planning/`을 제외한 현재 프로젝트의 Markdown 문서 중 제품 정책, PRD/요구사항, 기능/화면 설계, 운영/QA 판단을 담은 문서와, 그 Markdown이 상대경로로 명시 참조한 로컬 resource만 포함한다. 코드, 테스트, 설정, 빌드 산출물, dependency/vendor, 외부 URL은 SSOT 근거가 아니다.

```yaml
evidence_package:
  status: completed | limited | failed
  target:
    input_path: "<초안 폴더 또는 파일 경로>"
    feature_doc_path: "<기능설계서 경로 또는 없음>"
    policy_doc_path: "<정책서 경로 또는 없음>"
    bundle_complete: true | false
    unsupported_doc_type: false
  corpus:
    project_root: "<근거 탐색 기준 프로젝트 루트>"
    included_patterns:
      - "**/*.md"
      - "**/*.markdown"
      - "linked local resources from selected Markdown"
    excluded_paths:
      - "planning/"
      - ".git/"
      - "vendor/"
      - "node_modules/"
      - "build/"
      - "dist/"
      - ".cache/"
      - "generated/"
    excluded_resource_types:
      - code
      - test
      - config
      - external_url
  evidence_sources:
    - path: "<프로젝트 상대 경로>"
      evidence_kind: markdown | linked_local_resource
      source_type: policy | prd | requirement | feature | screen | operations | qa | unknown
      source_role: primary | supporting | conflict_candidate | context_only
      status_signal: current | draft | archive | deprecated | unknown
      freshness_signal: explicit_current | dated | undated | unknown
      document_version: "<vX.Y 또는 unversioned 또는 unknown>"
      claim_scope: "<이 근거가 뒷받침하거나 충돌 가능성이 있는 주장>"
      referenced_by: "<linked_local_resource인 경우 참조한 Markdown 경로 또는 none>"
      use_as_current_evidence: true
      use_as_current_evidence_reason: "<current evidence 사용 또는 제외 이유>"
  unread_candidates:
    - path_or_title: "<후보 문서 또는 resource>"
      reason: "<읽지 않은 이유>"
  excluded_candidates:
    - path_or_title: "<제외된 파일 또는 링크>"
      rule: planning_excluded | non_product_docs | outdated_version | non_markdown | code_or_test | config | generated_or_vendor | external_url | unreferenced_resource | other
      reason: "<한 문장 설명>"
  verification_limits:
    - type: no_relevant_markdown | linked_resource_unread | status_unknown | freshness_unknown | independent_context_unavailable | corpus_scope_unclear | other
      detail: "<한 문장 설명>"
  summary:
    claim_support: "<근거 지원 여부 요약>"
    conflict_risk: "<충돌 가능성 요약>"
    downstream_readiness_summary: "<디자인/개발/QA/운영 착수 가능성 요약>"
```

## 상태 규칙

- `status: completed`: 검토 대상과 필요한 Product Docs SSOT 근거를 읽었고, 최종 `pass`를 막는 검증 한계가 없다.
- `status: limited`: 관점별 검토는 가능하지만 관련 Markdown 부재, local resource 미확인, 상태·최신성 불명확, 독립 컨텍스트 제한 같은 검증 한계가 있어 최종 `pass`는 불가능하다.
- `status: failed`: 검토 대상, 필수 근거, 또는 근거 패키지 필드를 확보하지 못해 후속 검토와 gate 판정이 불가능하다.

## 필수 기록 규칙

- `status: failed`면 후속 실행·검증 가능성 검토는 실행하지 않고 최종 `수정 필요`로 취합한다.
- `status: limited`면 후속 검토는 가능하지만 최종 `pass` 금지다.
- 관련 Product Docs Markdown을 찾지 못했지만 검토 대상과 남은 조건이 명확하면 `status: limited`로 둘 수 있다. 검토 대상이나 필수 근거 패키지 필드가 없어 gate 판정 자체가 불가능하면 `status: failed`다.
- `planning/` 하위 파일은 검토 대상일 수 있지만 `evidence_sources`에 넣지 않는다.
- Markdown이 상대경로로 참조한 로컬 resource만 `linked_local_resource`로 기록한다.
- 외부 URL, 코드, 테스트, 설정, generated/vendor/dependency 파일은 `excluded_candidates`에 제외 사유를 남긴다.
- 버전 표기가 있는 같은 문서군은 가장 높은 버전을 current evidence 후보로 삼고, 낮은 버전은 `outdated_version` 또는 `use_as_current_evidence: false`로 기록한다.
- 전체 프로젝트의 모든 제외 파일을 나열하지 않는다. 검토 주장과 직접 관련되어 후보로 발견된 제외 항목만 기록한다.
