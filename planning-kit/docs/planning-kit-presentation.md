# planning-kit 기반 기획 문서 운영 가이드

> Confluence 게시용 운영 문서
> 작성일: 2026-05-10
> 최종 수정일: 2026-05-12
> 대상: 기획팀, 개발팀, 디자인/QA/운영 협업자
> 문서 상태: 초안 v0.12

---

## 1. 목적

`planning-kit`은 기획자가 작성한 초안, 기존 문서, 링크, 이미지 자료를 바탕으로 기획 내용을 **정책서**와 **기능설계서**로 구조화하고, 기획팀/실무팀 리뷰 전에 확인해야 할 `[TBD]`, 누락, 충돌, 검증 불가능한 요구사항을 드러내는 도구입니다.

이 문서의 목적은 `planning-kit` 산출물을 Confluence에 게시하고 리뷰할 때의 표준 운영 방식을 정하는 것입니다.

핵심 원칙은 다음과 같습니다.

- 초안 작성은 기존 방식대로 자유롭게 진행하고, AI는 `planning-format`, `planning-review`, `planning-publish-confluence` 단계에서 formatting, review, 후보 발행에 활용한다.
- SSOT corpus 자체의 중복, 낮은 버전 참조, 내용 충돌은 새 기획 리뷰와 분리해 필요 시 `ssot-audit`로 점검한다.
- Confluence `[Origin]`은 개인 자유 작성 결과물이 올라오는 공간으로 둔다.
- Confluence `[SSOT]`는 `planning-kit`을 활용해 formatting/review한 결과물과 `v0.7` 후보 발행본이 올라오는 공간으로 둔다.
- 최종 기획 v1.0은 `planning-format`/`planning-review` 산출물이 아니라 기획/개발/디자인/QA/운영 등 관련 팀 리뷰와 합의 이후 Confluence `[SSOT]`에서 공식 기획 완료 문서로 확정한다.

---

## 2. 한 줄 정의

`planning-kit`은 초안 단계의 기획 내용을 정책서와 기능설계서로 구조화하고 사전 점검한 뒤, Confluence 리뷰에 올릴 수 있는 상태로 만드는 **기획 문서화 품질 게이트**입니다.

Confluence 게시 시 아래 문구를 문서 상단 또는 안내 블록에 포함합니다.

> `planning-kit` 산출물은 최종 결정본이 아니라, 기획/개발/디자인/QA/운영이 검토할 수 있도록 초안을 정책서와 기능설계서로 구조화하고 리스크를 표시한 검토용 초안입니다. 최종 책임과 확인 권한은 관련 팀 리뷰 프로세스를 따릅니다.

---

## 3. 왜 필요한가

기획 초안에는 보통 여러 종류의 정보가 섞여 있습니다.

- 정책 기준: 무엇을 허용하고 금지할지
- 화면/동작: 사용자가 어디서 무엇을 누르는지
- 예외 처리: 실패, 취소, 승인, 운영 대응
- 권한: 누가 볼 수 있고 누가 처리할 수 있는지
- 의존성: 결제, 배송, 알림, 정산, 외부 시스템 영향
- 미결 사항: 아직 결정되지 않았지만 개발 전에 정리해야 하는 질문

이 정보가 섞인 채로 개발팀에 전달되면 다음 문제가 반복됩니다.

- 정책 결정과 화면 동작이 구분되지 않는다.
- 테스트 가능한 Acceptance Criteria가 부족하다.
- 상태 전이, 권한, 예외 처리가 뒤늦게 발견된다.
- 기존 Confluence 문서나 SSOT와 충돌하는지 알기 어렵다.
- 리뷰 회의가 문장 수정이 아니라 누락 찾기로 흘러간다.

`planning-kit`은 초안을 먼저 구조화하고, 리뷰 전에 확인해야 할 항목을 드러내 이 문제를 줄입니다.

---

## 4. 표준 운영 흐름

```text
Confluence [Origin] / SSOT 자료 확인
-> 필요 시 ssot-audit로 기존 SSOT backlog 확인
-> 기존 방식으로 개인 기획 작성(~v0.7)
-> Confluence [Origin] upload
-> planning-format으로 기획서 formatting 및 기존 문서 기반 발견사항 보정
-> planning-review로 리뷰/사전 점검 및 발견사항 수정
-> planning-publish-confluence로 Confluence [SSOT]에 v0.7 후보 발행
-> 기획팀 리뷰 진행(v0.8)
-> 실무 리뷰 진행(v0.9)
-> 이슈 발견 시 simple update 또는 mass update
-> Confluence [SSOT]에서 공식 기획 완료 문서(v1.0) 확정
```

| 구간 | 역할 | 산출물/상태 |
|---|---|---|
| Confluence [Origin] / SSOT | 개인 자유 작성 결과물, 기존 기획, 제품 기준 확인 | 참조 자료, 기존 기준 |
| ssot-audit | 기존 SSOT corpus 자체의 구조·내용 품질을 점검 | SSOT 인벤토리, 제외 문서, 개선 backlog |
| 개인 기획 작성 | 기존 방식으로 자유롭게 초안 작성 | 개인 기획 초안 |
| Confluence [Origin] upload | 개인 기획 초안을 Confluence `[Origin]`에 업로드 | `[Origin]` 개인 기획 초안 v0.7 |
| planning-format | `[Origin]` upload본을 정책서와 기능설계서로 구조화하고 기존 문서 기반 발견사항을 보정 | 정책서, 기능설계서, 출처, 입력 제외, 자체 검증 |
| planning-review | SSOT 충돌, AC 검증가능성, 의존 영향을 확인하고 발견사항을 수정 | 리뷰 결과, 수정 반영본, 잔여 발견/권고 목록 |
| planning-publish-confluence | 현재 context memory의 정책서·기능 설계서 두 본문을 Confluence `[SSOT]` 하위에 발행 | `[기능명] v0.7` 후보 container와 정책서/기능 설계서 child page |
| 기획팀 리뷰 | 정책, 범위, 우선순위, 미결 사항 확인 | 기획팀 리뷰 v0.8 |
| 실무 리뷰 | 개발, 디자인, QA, 운영 영향 확인 | 실무 리뷰 v0.9 |
| 공식 기획 완료 | Confluence `[SSOT]`에서 개발 착수 가능한 공식 기준 문서로 확정 | `[SSOT]` 공식 기획 완료 문서 v1.0 |

운영 기준:

- Confluence `[Origin]`과 `[SSOT]`의 목적을 섞지 않는다.
- Confluence `[SSOT]`는 기획/개발/디자인/QA/운영 등 관련 팀이 함께 검토하는 협업 공간으로 사용한다.
- v1.0 확정본은 Confluence `[SSOT]`에서 공식 기획 완료 문서로 관리한다.
- Confluence `[SSOT]`에 게시됐다는 사실만으로 공식 완료 문서로 보지 않는다.
- simple update와 mass update는 기획팀 리뷰 또는 실무 리뷰 중 이슈가 발견됐을 때 선택하는 보정 옵션이다.
- 의미가 바뀌는 변경은 기획팀/실무 리뷰 단계에서 확인한다.

발표 중 `planning-format`/`planning-review`/`planning-publish-confluence`/`ssot-audit`의 내부 흐름을 더 자세히 설명해야 할 때는 [planning-kit workflow 발표 가이드](./planning-kit-workflow-guide.md)를 함께 사용한다.

## 5. planning-kit이 하는 일

`planning-kit`은 기본 기획 변환/리뷰/후보 발행 세 단계와, 필요 시 실행하는 SSOT corpus 감사 단계로 동작합니다.

### 5.1 planning-format

`planning-format`은 기획 초안을 정책서와 기능설계서로 나누고, 기존 문서나 참조 자료에서 발견한 누락/불명확/충돌 후보를 본문, `[TBD]`, 입력 제외 항목, 자체 검증 결과에 반영합니다.

```text
$planning-format <기획 초안 또는 URL>
```

주요 입력:

- 텍스트 초안
- Markdown 파일
- 디렉터리
- URL
- 이미지

주요 출력:

- 정책서
- 기능설계서
- 출처 목록
- 입력 제외 항목
- 자체 검증 결과

이 단계에서 발견한 내용은 최종 결정이 아니라 보정 후보입니다. planning-kit 실행 담당과 기획팀은 Confluence `[SSOT]` 게시 전에 반영 내용과 `[TBD]`, 입력 제외 항목을 확인합니다.

정책서에는 결정 기준, 규칙, 예외, 권한, 상태 기준이 정리됩니다.

기능설계서에는 사용자 흐름, 화면/입력 항목, 시스템 동작, 예외 메시지, 검증 조건이 정리됩니다.

### 5.2 planning-review

`planning-review`는 `planning-format` 산출물이 개발 착수 전에 검토 가능한지 확인하고, 발견사항을 수정 반영합니다.

```text
$planning-review
$planning-review https://wiki.example/policy/order-cancel https://docs.example/feature/order-cancel
```

0.2.6부터 정책서와 기능설계서가 서로 다른 URL에 있어도 직접 review 입력으로 줄 수 있습니다. 이 경우 `planning-review`가 URL root fetch, 본문 URL 재귀 fetch, connector fallback, 이미지 multimodal 처리를 수행한 뒤 `## 입력 출처`와 `## SSOT 출처`를 분리해 보여줍니다.
0.2.7부터 정책서 또는 기능설계서 파일 하나만 입력해도 같은 폴더 sibling 파일을 non-recursive로 함께 읽어 한 쌍을 찾습니다.

점검 축:

- SSOT 충돌: 기존 문서와 새 기획이 어긋나는지 확인
- Acceptance Criteria 검증가능성: 테스트 가능한 조건인지 확인
- 의존/영향 분석: 상태, 권한, 외부 연동, 다른 문서 영향 확인

주의:

- `planning-review`의 수정 반영은 승인 판정이 아니라 리뷰 전 보완입니다.
- 해결하지 못한 발견 항목은 회의 안건 또는 후속 보완 작업으로 전환합니다.

상세 workflow와 발표용 다이어그램은 [planning-kit workflow 발표 가이드](./planning-kit-workflow-guide.md)를 참고합니다.

### 5.3 planning-publish-confluence

`planning-publish-confluence`는 현재 context memory에 정책서와 기능 설계서 두 본문이 명확히 있을 때만 Confluence `[SSOT]` 하위에 `v0.7` 후보 문서로 발행합니다. 파일 경로, URL, 저장 산출물 경로는 인자로 받지 않습니다.

```text
$planning-publish-confluence
```

주요 출력:

- Confluence 발행 판정
- `v0.7` 발행 label
- 생성/업데이트 page URL
- readback 검증 결과
- 실패 또는 부분 완료 사유

주의:

- 기본 parent는 `https://colosseum.atlassian.net/wiki/spaces/PROD/pages/1767604270/SSOT`이지만 실행 중 다른 parent URL을 직접 입력할 수 있습니다.
- 발행 title은 `[기능명] v0.7`, `[기능명] 정책서 v0.7`, `[기능명] 기능 설계서 v0.7` 형식입니다.
- Confluence write 전 최종 확인이 필요하며, write 후 readback으로 검증합니다.
- `v0.7` 후보는 공식 v1.0 SSOT가 아닙니다.

### 5.4 ssot-audit

`ssot-audit`는 새 기획 산출물을 리뷰하는 단계가 아니라, 기존 SSOT corpus 자체를 점검하는 유지보수 도구입니다.

```text
$ssot-audit
$ssot-audit --ssot-include "docs/**/*.md" --axes structure,content
```

주요 출력:

- SSOT 인벤토리
- 낮은 버전(`< v0.8`) 제외 문서
- 구조 품질 발견/권고
- 내용 품질 발견/권고
- 개선 backlog

결과는 화면 output only이며, 문서를 자동 수정하지 않습니다.

---

## 6. 산출물 읽는 법

`planning-kit` 결과물에서 가장 중요한 부분은 본문만이 아닙니다.

| 항목 | 의미 | 주 담당 |
|---|---|---|
| 정책서 | 결정 기준, 규칙, 예외, 권한, 상태 기준 | 기획팀 |
| 기능설계서 | 사용자 흐름, 화면, 시스템 동작, 예외 메시지 | 개발/디자인/QA |
| 출처 | 어떤 입력과 링크를 근거로 했는지. `planning-review`는 입력 출처와 SSOT 출처를 분리 | planning-kit 실행 담당/리뷰어 |
| 입력 제외 항목 | 본문에 반영하지 않은 이유 | 기획팀 |
| 자체 검증 | 문서 품질 점검 결과 | planning-kit 실행 담당 |
| review 결과 | SSOT/AC/의존 영향 발견 사항 | 기획팀/실무팀 |
| publish 결과 | `v0.7` Confluence 후보 page와 readback 검증 결과 | planning-kit 실행 담당/기획팀 |

해석 기준:

- `[TBD]`가 있다는 것은 실패가 아니라 결정해야 할 질문이 드러났다는 뜻입니다.
- 입력 제외 항목은 버려진 내용이 아니라, 본문에 넣기 어렵거나 근거가 부족해서 검토 대상으로 남긴 내용입니다.
- SSOT 충돌은 누가 틀렸다는 판정이 아니라 기존 기준과 새 기획이 다르다는 알림입니다.

---

## 7. Confluence 게시 규칙

Confluence `[Origin]`에는 개인 자유 작성 결과물을 올립니다. Confluence `[SSOT]`에는 `planning-review`까지 확인한 결과를 `planning-publish-confluence`로 `v0.7` 후보 문서로 올립니다. 게시 전에 planning-kit 실행 담당 또는 기획팀이 산출물을 확인하고, 상태와 담당 팀, 리뷰 단계를 명확히 둡니다.

### 7.1 문서 상태

| 상태 | 의미 | 위치/버전 |
|---|---|---|
| 개인 초안 | 기획자가 기존 방식으로 작성한 최초 입력 | 작성자 관리 / v0.7 이하 |
| Origin upload | 개인 기획 초안을 Confluence `[Origin]`에 업로드 | `[Origin]` / v0.7 |
| formatting 초안 | `planning-format`으로 구조화, 보정한 결과물 | 대화 context 또는 작업 초안 / v0.7 후보 전 |
| review 반영본 | `planning-review` 발견사항을 수정 반영 | 대화 context 또는 작업 초안 / v0.7 후보 전 |
| v0.7 후보 발행본 | `planning-publish-confluence`로 Confluence `[SSOT]` 하위에 발행 | `[SSOT]` / v0.7 후보 |
| 기획팀 리뷰 | 정책, 범위, TBD 확인 | `[SSOT]` / v0.8 |
| 기획팀 내부 검토 | 우선순위, 메시지, 정책 정합성 확인 | `[SSOT]` / v0.8.x |
| 실무 리뷰 | 개발, 디자인, QA, 운영 영향 검토 | `[SSOT]` / v0.9 |
| 실무 협의 완료 | 주요 쟁점 합의 완료 | `[SSOT]` / v0.9.x |
| 공식 기획 완료 | 개발 착수 기준 문서 | `[SSOT]` / v1.0 |

### 7.2 문서 상단 메타정보

Confluence에 게시할 때는 문서 상단에 아래 정보를 표로 고정합니다.

| 항목 | 값 |
|---|---|
| 문서 상태 | 기획팀 리뷰 / 실무 리뷰 / 공식 기획 완료 |
| 버전 | v0.7 후보 / v0.8 / v0.9 / v1.0 |
| 담당 팀 | 기획팀 |
| 원본 작성자 | 개인 기획 초안 작성자 |
| planning-kit 실행 담당 | planning-format / planning-review / planning-publish-confluence 실행자, 필요 시 ssot-audit 실행자 |
| 리뷰어 | 기획팀, 개발팀, 디자인팀, QA, 운영/CS |
| 기준일 | YYYY-MM-DD |
| 출처 | 원본 초안, Figma, Slack, 기존 문서 링크 |
| TBD 수 | N개 |
| 입력 제외 항목 | 있음/없음 |
| SSOT 충돌 | 있음/없음 |
| 최종 확인 | 기획팀 + 개발팀 |

### 7.3 게시 전 체크리스트

- 문서 상태와 버전이 맞는가
- 개인 자유 작성 결과물은 `[Origin]`, `planning-kit` 처리 결과물은 `planning-publish-confluence`로 `[SSOT]`에 `v0.7` 후보로 게시했는가
- 담당 팀과 리뷰어가 지정되어 있는가
- `[TBD]`와 입력 제외 항목을 숨기지 않았는가
- `planning-review` 발견 항목을 본문 또는 리뷰 안건으로 연결했는가
- Confluence 발행 title과 metadata에 `v0.7`이 포함됐는가
- SSOT corpus 자체의 중복/낮은 버전 참조/내용 충돌이 의심되면 `ssot-audit` 결과를 별도 backlog로 분리했는가
- 출처 링크 접근 권한을 리뷰어가 확인할 수 있는가
- `[Origin]`과 `[SSOT]` 중 문서 목적에 맞는 위치를 선택했는가

---

## 8. 변경 운영 기준

simple update와 mass update는 모든 문서에 반드시 발생하는 단계가 아닙니다. 기획팀 리뷰 또는 실무 리뷰 중 이슈가 발견됐을 때, 변경의 영향 범위에 따라 선택합니다.

### 8.1 Simple Update 기준

다음 이슈는 simple update로 처리할 수 있습니다.

| 항목 | 예시 |
|---|---|
| 오탈자/문구 수정 | 표현 개선, 용어 통일 |
| 링크/출처 보강 | Figma, Jira, 참고 문서 추가 |
| 기존 정책의 설명 보강 | 동작 변경 없이 예시 추가 |
| 리뷰 코멘트 반영 | 이미 합의된 내용의 문서화 |
| 담당자/일정 업데이트 | 정책 의미 변화 없음 |

Simple update는 담당 팀 확인 후 바로 반영합니다.

### 8.2 Mass Update 기준

다음 이슈는 mass update로 보고 재검토합니다.

| 항목 | 예시 |
|---|---|
| 정책 기준 변경 | 취소 가능 시간, 승인 조건 변경 |
| 권한 변경 | 관리자/사용자/운영자 역할 변경 |
| 상태 전이 변경 | 주문 상태, 승인 상태, 실패 상태 추가 |
| API/DB/외부 연동 영향 | 결제, 배송, 알림, 정산 연동 변경 |
| AC 변경 | 테스트 기준 자체가 바뀜 |
| 기존 SSOT와 충돌 | 기존 정책 문서와 다른 기준 등장 |

Mass update는 다시 `planning-format` 또는 `planning-review`를 돌리고, 기획팀 리뷰와 실무 리뷰를 거쳐 최종 확인합니다.

### 8.3 최종 확인 기준

v1.0으로 올리기 전에는 아래 조건을 확인합니다.

- `[TBD]`가 없거나 합의된 후속 과제로 명시되어 있다.
- 입력 제외 항목을 기획팀이 확인했다.
- SSOT 충돌이 해결됐거나 담당 팀이 갱신 방향을 확인했다.
- 개발팀이 상태, 권한, 예외, 의존성을 확인했다.
- QA가 Acceptance Criteria의 검증 가능성을 확인했다.
- 최종 문서가 Confluence `[SSOT]`에서 공식 기획 완료 문서로 정리되어 있다.

---

## 9. 역할과 책임

| 역할 | 책임 |
|---|---|
| 원본 작성자 | 기존 방식으로 개인 기획 초안을 작성하고 Confluence `[Origin]`에 업로드 |
| planning-kit 실행 담당 | `planning-format`, `planning-review`, `planning-publish-confluence` 실행, 발견사항 수정 반영, Confluence `[SSOT]` `v0.7` 후보 발행, 필요 시 `ssot-audit`로 SSOT backlog 분리 |
| 기획팀 | 정책 판단, 범위와 우선순위 결정, TBD 해소, 공식 기획 완료 확인 |
| 개발팀 | 상태 전이, 권한, 예외, 외부 연동, 구현 영향 확인 |
| QA | Acceptance Criteria 검증가능성 확인, 테스트 관점 누락 제기 |
| 디자인 | 화면 흐름, 입력 항목, 메시지, UX 예외 검토 |
| 운영/CS | 운영 예외, 고객 안내, 수동 처리 기준 검토 |

---

## 10. FAQ

### Q1. AI가 기획을 임의로 확정하는 것 아닌가요?

아닙니다. `planning-kit`은 확정 도구가 아니라 검토용 초안을 만드는 도구입니다. 근거가 부족하거나 모호한 부분은 `[TBD]`, 입력 제외 항목, 충돌 후보로 남깁니다. 최종 결정은 관련 팀 리뷰와 합의 프로세스가 합니다.

### Q2. 기존 PRD나 Confluence 문서를 대체하나요?

대체하지 않습니다. 기존 문서 체계를 대체하기보다, 초안과 참고자료를 개발 전달 가능한 구조로 정리하는 전처리 단계입니다.

### Q3. 결과를 그대로 개발 티켓에 붙여도 되나요?

가능은 하지만 권장 흐름은 아닙니다. 먼저 `[TBD]`, 입력 제외 항목, review 발견 사항, SSOT 충돌 여부를 확인해야 합니다.

### Q4. SSOT 충돌은 어느 쪽이 맞다는 뜻인가요?

정답 판정이 아닙니다. 기존 문서와 새 기획이 다르다는 신호입니다. 어떤 문서를 갱신할지, 어떤 기준을 최종으로 삼을지는 관련 팀 리뷰에서 결정합니다.

### Q5. Confluence [SSOT]에 올리면 바로 공식 완료 문서인가요?

아닙니다. Confluence `[SSOT]`에 올라간 문서는 리뷰 공간에 들어간 것입니다. 기획팀 리뷰, 실무 리뷰, 최종 확인 기준을 통과해야 v1.0 공식 기획 완료 문서로 봅니다.

### Q6. simple update와 mass update는 왜 나누나요?

문구 수정과 정책 변경을 같은 수준으로 처리하면 공식 문서 신뢰도가 떨어집니다. 의미가 바뀌는 변경은 다시 점검하고 리뷰해야 합니다.

### Q7. 개발팀은 무엇을 보면 되나요?

기능설계서의 사용자 흐름, 기능 동작, 예외 메시지, 권한과 데이터 접근, 그리고 `planning-review`의 AC 검증가능성/의존 영향 결과를 보면 됩니다.

### Q8. 기획팀은 무엇을 보면 되나요?

정책서의 세부 규칙, 상태 및 처리 기준, 예외 및 승인 기준, `[TBD]`, 입력 제외 항목, SSOT 충돌 여부를 보면 됩니다.
