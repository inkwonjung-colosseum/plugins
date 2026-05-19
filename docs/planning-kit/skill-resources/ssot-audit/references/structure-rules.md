# Structure Rules

`ssot-audit` 구조 품질 감사 기준. 구조 품질은 "문서 체계가 유지보수 가능한가"를 본다.

## 1. canonical 후보 중복

같은 도메인/정책/기능에 대해 canonical처럼 보이는 문서가 2개 이상이면 발견 또는 권고한다.

canonical 신호:

- path/title에 `policy`, `정책`, `spec`, `design`, `기능설계서`, `SSOT`, `canonical`, `current`.
- README 또는 index에서 기준 문서처럼 링크됨.
- 본문에 단정형 정책/상태/권한/임계값이 많음.
- archive/draft 신호가 없음.

판정:

- 두 문서가 같은 대상의 다른 기준값을 말하면 `발견`.
- 값 충돌은 없지만 canonical 후보가 여러 개면 `권고`.

Backlog:

- 하나를 canonical로 지정.
- 나머지는 보조 문서/과거 문서/근거 문서 역할을 명시.
- README 또는 index에서 canonical link를 정리.

## 2. canonical 부재

같은 도메인에 회의록/PRD/README 조각은 여러 개 있지만 기준 문서가 없으면 권고한다.

예:

- 주문 취소 관련 PRD와 회의록은 있지만 `docs/policy/order-cancel.md` 같은 기준 문서가 없음.
- 여러 문서가 같은 정책을 언급하지만 "최신 기준" 링크가 없음.

Backlog:

- canonical 정책서 또는 기능설계서 생성.
- 기존 조각 문서에서 canonical 문서로 링크 정리.

## 3. draft/old/archive 활성 참조

`draft`, `old`, `archive`, `deprecated`, `legacy`, `wip` 신호가 있는 문서가 활성 SSOT 문서에서 기준처럼 참조되면 발견한다.

활성 참조 신호:

- README, 정책서, 기능설계서, 최신 PRD에서 archive/draft 문서를 링크.
- "기준", "정책", "참고", "따름" 같은 표현과 함께 링크.

예외:

- archive 내부 문서끼리 참조하는 경우는 발견하지 않는다.

문제는 현재 SSOT 후보가 draft/archive 문서를 기준처럼 참조하는 경우다.

Backlog:

- 활성 문서에서 최신 canonical로 링크를 바꾼다.

## 4. 도메인 문서 흩어짐

같은 도메인의 문서가 여러 위치에 흩어져 있고 상호 링크나 상위 index가 없으면 권고한다.

예:

- `docs/prd/order.md`
- `docs/policy/order.md`
- `meetings/order.md`

위 세 문서가 서로 링크되지 않고 상위 index도 없다면 사용자는 어느 문서를 먼저 읽어야 하는지 알기 어렵다.

Backlog:

- 도메인 index 문서 생성.
- canonical 문서를 중심으로 PRD/회의록/보조 문서 링크 정리.

## 5. 문서 역할 불명확

문서 제목·경로·본문 구조로 역할을 판단하기 어렵거나, 정책/기능/회의 메모가 한 문서에 섞여 있으면 권고한다.

예:

- 제목이 `주문 정리`이고 본문에 정책 결정, 구현 메모, 회의 코멘트가 섞임.
- H1/H2에 문서 종류가 없고 본문도 checklist/메모/정책이 혼재.

Backlog:

- 제목 또는 H1에 문서 역할 명시.
- 정책 기준은 정책서로, 구현 상세는 기능설계서로, 회의 기록은 회의록으로 분리.

## 6. 외부 canonical 의존

로컬 Markdown에는 외부 링크만 있고, 외부 fetch 본문이 사실상 기준 문서라면 권고한다.

신호:

- 로컬 문서 본문이 짧고 외부 링크가 대부분.
- 외부 본문에 정책/상태/권한/임계값이 풍부함.
- 로컬 문서에 외부 문서의 역할, 요약, 최신성, 참조 이유가 없음.

Backlog:

- 로컬 문서에 핵심 결정 요약 추가.
- 외부 문서를 canonical로 명시.
- 외부 문서가 사라지거나 인증 실패해도 최소 기준을 알 수 있는 fallback 설명 추가.

## 7. 분류와 출력 항목

구조 품질 항목은 다음 필드를 가진다.

```markdown
1. [발견 또는 권고 제목]
   - 분류: [발견 | 권고]
   - 카테고리: [canonical 중복 | canonical 부재 | archive 활성 참조 | 도메인 문서 흩어짐 | 역할 불명확 | 외부 canonical 의존 | SSOT token 밖 기준 문서]
   - 위치: [문서 path list]
   - 근거: "[짧은 근거]"
   - 영향: [한 줄]
   - 제안: [최소 개선 방향]
```

명확한 기준값 충돌, archive 활성 참조, SSOT token 밖 기준 문서를 최신 기준처럼 참조하는 문제는 `발견`이다. 사람이 최종 판단해야 하는 구조 개선 후보는 `권고`다.

## 8. SSOT token 밖 기준 문서

폴더명에 독립 `SSOT` token이 없는 문서가 기준 문서처럼 쓰이면 `문서 이동` 또는 `SSOT 보강` backlog를 제안한다. 단순 substring(`ProductSSOT`)이나 도구명(`ssot-audit`)은 SSOT token으로 보지 않는다.

예:

- `docs/policy/order.md`에 결정 문장이 풍부하지만 SSOT token 폴더 밖에 있음.
- `ProductSSOT/order.md`는 `SSOT` 독립 token이 아니므로 corpus 밖이다.
- `planning/[SSOT]/draft.md`는 `planning/**` 생성 초안 영역이라 corpus 밖이다.
