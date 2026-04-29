# Review Gate

`plan-format` 결과물을 외부 발행 절차에 넘길 수 있는지 판단할 때 사용하는 참조 기준이다.

`plan-review`는 매번 독립 검토자 3개 관점을 사용한다. 각 검토자는 초안을 만든 대화가 아니라 검토 대상 파일과 로컬 근거 문서를 직접 읽고 판단한다.

## 필수 검토 입력

- 검토 대상 초안 폴더 또는 파일 경로.
- 각 독립 검토자가 직접 읽은 초안 본문.
- 초안에 명시된 관련 문서.
- 구체적인 주장을 확인할 때 필요한 최소 로컬 Confluence 원문.
- 검토자 역할과 관점별 범위.

현재 대화는 근거가 아니다. 어떤 사실이 대화 맥락에만 있고 초안이나 선택한 근거 문서에 없으면 근거 부족으로 본다.

## Confluence 근거 선택

로컬 Confluence 근거가 필요하면 저장소 reading rule을 따른다.

1. `.confluence-index/registry.json`에서 관련 export source를 고른다.
2. `.confluence-index/sources/<source-id>/source-index.jsonl`에서 후보 문서와 metadata를 확인한다.
3. `.confluence-index/sources/<source-id>/tree.md`로 문서 위치와 계층을 파악한다.
4. 확인할 주장에 필요한 가장 작은 raw exported Markdown 파일을 선택한다.
5. 판단 전에 raw exported Markdown 본문을 직접 읽는다.

전체 export 공간을 한 번에 읽지 않는다. 로컬 exported Markdown은 Confluence의 읽기 전용 snapshot으로 취급한다. index 또는 page metadata가 없으면 `metadata unavailable`로 기록하고 status나 freshness를 추론하지 않는다.

## 검토자 역할

### 근거 검토자

출처 지원 여부, Confluence 원문과의 충돌, 근거 없는 가정, 오래된 근거, 발행 가능성에 영향을 주는 `[가정]` 항목을 확인한다.

### 결정·범위 검토자

남은 `[미정]`, 결정 누락, 결정 주체 또는 후속 액션, 적용/비적용/예외 범위, 지원하지 않는 문서 타입, 관련 정책서/기능설계서 문서 연결을 확인한다.

### 실행·검증 가능성 검토자

개발·운영·QA가 대화 기억 없이 초안만 보고 움직일 수 있는지 확인한다. 조건, 상태, 예외, 권한, 업무 연동 경계, 업무 데이터, 외부 채널, 실패 대응, 운영 영향, 확인 기준을 필요한 수준으로 점검한다.

## 필수 검토 출력

- 검토 방식: `독립 검토자`.
- 검토자 역할.
- 검토 대상 경로.
- 읽은 근거 문서: `source-id`, `raw exported Markdown path`, `current/draft/archive` status, 각 로컬 Confluence source의 `stale` 판단.
- source metadata, document status, freshness를 로컬 export에서 확인할 수 없으면 `metadata unavailable` 사용.
- 담당 관점의 발견 사항.
- 관점별 검토 결과: `pass`, `conditional pass`, `수정 필요`.
- 필요한 최소 수정 사항 또는 확인 조건.

근거 제한:
- metadata unavailable이면 pass 금지.
- stale 값을 확인할 수 없으면 pass 금지.
- raw exported Markdown을 읽지 못했으면 pass 금지.
- 위 경우는 누락된 근거가 외부 발행에 중요하지 않고 남은 확인 조건이 명확할 때만 `conditional pass`가 될 수 있다.

## 검토 결과 취합

현재 컨텍스트는 독립 검토자 결과를 정리하고 요약할 수 있지만, 파일 기반 근거 없이 어떤 검토자의 결과도 완화할 수 없다.

최종 검토 결과는 관점별 검토 결과 중 가장 보수적인 값을 사용한다. 보수 순서: `수정 필요 > conditional pass > pass`.

- 검토자 중 하나라도 `수정 필요`를 반환하면 최종 검토 결과는 `수정 필요`.
- `수정 필요`가 없고 하나라도 `conditional pass`를 반환하면 최종 검토 결과는 `conditional pass`.
- 세 검토자가 모두 `pass`일 때만 최종 검토 결과는 `pass`.

현재 컨텍스트와 독립 검토자 판단이 다르면 더 보수적인 검토 결과를 사용한다.

1. `수정 필요`
2. `conditional pass`
3. `pass`

## 발행 전 확인 신호

다음 신호는 발행 전에 명확한 검토 결과가 필요하다.

- `[미정]`
- `[가정]`
- `충돌 경고`

## 결과 기준

### pass

중요한 `[미정]`, `[가정]`, 충돌 문제가 남아 있지 않고, source metadata가 있으며, 필요한 로컬 Confluence 원문을 읽었고, freshness가 확인되었으며, 개발 또는 운영이 움직일 만큼 초안이 구체적일 때만 사용한다.

### conditional pass

남은 문제가 명시적이고 기획자가 발행 전에 확인하거나 수용할 수 있을 때 사용한다. 조건은 한 문장으로 정확히 적는다.

### 수정 필요

누락된 결정, 충돌, 불명확한 규칙, 근거 없는 가정 때문에 구현 또는 운영 판단이 달라질 수 있으면 사용한다.

## 검토 경계

- 초안을 직접 다시 쓰지 않는다.
- 필요한 최소 수정 사항만 짚는다.
- 대화 기억을 근거로 사용하지 않는다.
- archive 문서는 현재 정책이 아니라 과거 맥락으로 취급한다.
- 로컬 근거가 오래되었거나 부족하면 가정으로 채우지 말고 어떤 근거가 부족한지 말한다.
