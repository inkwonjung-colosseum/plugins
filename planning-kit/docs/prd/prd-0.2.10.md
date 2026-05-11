# planning-kit PRD 0.2.10

> 0.2.9 기반 incremental PRD. `planning-format`과 `planning-review`가 산출물/report-first 구조로 개선됐지만, 실제 Zone 관리 사례에서는 상단 정보가 여전히 "읽을 수 있는 분석 보고서"에 가깝고, PM/현업/개발/QA가 바로 결정·수정·검증으로 옮기려면 재해석이 필요했다. 0.2.10은 기본 출력 상단을 `결정 보드` 중심으로 재정렬해, 긴 정책서·기능설계서·상세 추적 전에 사용자가 지금 결정해야 할 항목, 바로 수정할 문서 작업, 릴리즈 차단 항목, 검증 가능한 완료 조건을 먼저 보게 한다.
>
> 핵심 변경: 0.2.9의 readable/report-first 원칙은 유지하되, 사용자 확인·외부 결정 필요 P0/P1·릴리즈 차단 항목이 있으면 `결정 보드`를 정책서/기능설계서 또는 review 상세보다 먼저 출력한다. `planning-review`는 finding 나열을 넘어 `결정 항목(D*)`, `연결 finding(R*)`, `작업 백로그(A*)`, `릴리즈 차단 항목(T*)`을 한 줄 추적 체계로 묶고, 백로그에는 `완료 조건`, `검증 방법`, `담당/결정 필요자`를 포함한다. 0.2.9의 top-level `## 최우선 수정 항목`과 `## 작업 백로그`는 parser 호환을 위해 최소 0.2.x 동안 유지한다.

## 1. 변경 요약

1. **결정 보드 도입** — `planning-format`은 결정·확인·릴리즈 차단 항목이 있을 때만 `## 결정 보드`를 추가하고, 없으면 0.2.9 순서를 유지한다. `planning-review`는 항상 `## 결정 보드`를 출력하되 항목이 없으면 `없음`으로 압축한다.
2. **오늘 결정해야 할 항목 우선** — PM/현업이 답해야 하는 질문을 `D1`, `D2` 형식의 결정 항목으로 분리하고, 추천안·결정 필요자·반영 위치를 함께 표시한다.
3. **동일 원인 finding 병합** — `R2-1`과 `R3-1`처럼 같은 원인에서 나온 발견은 하나의 결정 항목 또는 작업 항목 아래에 묶는다. 원시 finding ID는 유지하되 상단에서는 중복 노출하지 않는다.
4. **작업 백로그 실행성 강화** — `작업 백로그` 필드를 `ID / 연결 / 유형 / 대상 / 작업 / 완료 조건 / 검증 방법 / 담당/결정 필요자 / 상태`로 확장한다. 기본 화면에서는 카드/필드 목록을 우선하고, 표는 셀이 짧은 요약 또는 저장/상세용으로만 쓴다.
5. **차단 항목 등급화** — `[TBD]`, `fetch 실패`, `원문 정의 부재`, `라벨 미매핑`을 같은 무게로 보여주지 않는다. `릴리즈 차단`, `결정 필요`, `후속 과제`, `추적 로그`로 등급을 나눠 상단 노출 여부를 결정한다.
6. **검증 가능한 AC 문장화** — P0/P1 finding에는 최소 1개 이상의 Given/When/Then 또는 동등한 테스트 문장을 제안한다.
7. **사용자-facing 용어 정리** — 상단 기본 출력에서는 `SSOT corpus`, `R2`, `deps`, `AC Blocker` 같은 내부 용어보다 `SSOT 기준 문서 묶음`, `검증가능성`, `영향 분석`, `구현 차단` 같은 한국어 업무 표현을 우선한다. 내부 축명은 상세 추적 또는 괄호 병기로만 둔다.
8. **상세 추적 보존** — 0.2.9의 full 출처, 입력 제외, 원시 발견, connector status 하단 분리 원칙은 유지한다. 0.2.10은 정보를 삭제하지 않고 상단 decision layer를 추가한다.

## 2. 동기

0.2.9는 진행 로그와 원시 trace를 뒤로 내리고 산출물/report를 먼저 보여주는 데 성공했다. 하지만 Zone 관리 실제 출력에서는 다음 문제가 남았다.

- `planning-format`은 정책서·기능설계서 전문이 먼저 길게 나오면서, 최우선 확인 항목인 `메모 입력 항목 등록/수정 스펙`이 본문에 묻혔다.
- `planning-review`는 P0/P1 우선순위와 작업 백로그를 제공했지만, PM/현업 입장에서는 "무엇을 결정해야 하는지"와 "추천안이 무엇인지"를 다시 해석해야 했다.
- `R2-1` 외부 시스템 미참조 미정의와 `R3-1` WCS 플래그 연결 계약 부재는 사실상 같은 문제인데, 별도 finding으로 보여져 같은 결정을 두 번 읽게 했다.
- `A1~A7` 작업 백로그는 후속 작업 단위로 유용했지만, 완료 조건과 검증 방법이 부족해 개발/QA 티켓으로 옮길 때 재가공이 필요했다.
- `[TBD]`가 본문 곳곳에 흩어져 있어 릴리즈 차단 항목과 후속 과제를 구분하기 어려웠다.

0.2.10의 목적은 분석량을 줄이는 것이 아니라, 사람이 먼저 행동할 수 있는 순서로 출력의 계층을 나누는 것이다.

## 3. 비목표

- 정책 값, 상태값, 권한, 임계값, 외부 시스템 계약을 AI가 임의로 확정하지 않는다.
- Confluence, Jira, Linear, Google Docs 등에 티켓이나 문서를 자동 생성하지 않는다.
- `planning-review`의 R1/R2/R3 검증 기준 자체를 바꾸지 않는다.
- 0.2.9의 저장 경로(`planning/`), SSOT token 폴더 경계, 상세 추적 하단 분리 계약을 되돌리지 않는다.
- 모든 표를 물리적 Markdown 표로 강제하지 않는다. 넓은 표는 화면용 카드/필드 목록으로 분해할 수 있다.
- P2 권고를 상단에서 모두 펼치지 않는다. P2는 릴리즈 차단과 직접 연결될 때만 결정 보드에 올린다.

## 4. 출력 레이어

0.2.10은 0.2.9의 출력 아티팩트 레이어에 `결정 보드` 레이어를 추가한다.

| 레이어 | 목적 | 기본 위치 | 주요 규칙 |
|---|---|---|---|
| 결정 보드 | 사용자가 지금 결정·수정·검증할 항목을 파악 | 헤더 요약 바로 아래 | D*/A*/T* 차단 항목을 우선 노출. 원시 trace 금지 |
| 산출 본문 | 정책서·기능설계서 또는 review 결론/요약 | 결정 보드 아래 | 0.2.9 readable/report-first 원칙 유지 |
| 검증 피드백 | self-review 발견과 수정 제안 | 산출 본문 뒤 또는 결정 보드에서 참조 | 의미 변경은 사용자 승인 전 자동 반영 금지 |
| 상세 추적 | 출처·입력 제외·SSOT 출처·원시 발견 | 하단 | 디버그/감사용. 상단 결정을 방해하지 않음 |

결정 보드는 canonical 본문이 아니다. 결정 보드는 사용자가 행동하기 위한 projection이며, 정확한 정책서·기능설계서 원문은 산출 본문 또는 `--save` 저장 파일을 기준으로 한다.

## 5. 결정 보드 기본 구조

결정 보드는 다음 순서를 따른다. 기본 화면은 카드/필드 목록을 우선한다. 표는 항목 수가 적고 셀이 짧을 때만 사용할 수 있다.

```markdown
## 결정 보드

범례: D=결정, A=문서/구현 작업, R=검토 발견 원본(상세용), T=릴리즈 차단
읽는 순서: 오늘 결정 → 릴리즈 차단 확인 → 바로 수정 → 상세 추적

### 첫 화면 요약

- 오늘 결정: D1 외부 시스템 미참조 정의
- 릴리즈 차단: D1 - WCS 플래그 효과 미정으로 자동 전환 QA 불가
- 바로 수정(결정 불필요): 없음
- 결정 후 반영: A1 정책서·기능설계서 전환 조건 반영

### 지금 결정해야 할 항목

- D1 [P0] 외부 시스템 미참조의 정의 — PM/현업

#### D1 [P0] 외부 시스템 미참조의 정의

- 결정 질문: WCS 연동 여부 플래그 ON을 외부 시스템 참조 중으로 볼 것인가?
- 선택지: 1) ON = 참조 중, 2) 별도 외부 참조 테이블로 판단, 3) MVP에서는 WCS 참조 조건 제외
- 초안 추천(확정 필요): WCS 연동 여부 플래그 ON = 외부 참조 중
- 결정 필요자: PM/현업
- 반영 위치: 정책서 §6·§9, 기능설계서 §5
- 연결: 관련 발견 2건 (상세 추적의 결정 보드 연결 맵에서 D1로 확인)

### 릴리즈 차단 항목

D1에 연결됨 - 외부 시스템 미참조 범위와 WCS 플래그 효과가 미정이라 자동 전환 QA 불가. 별도 T* 반복 항목 없음.

### 바로 수정할 문서 작업

- A1 [D1 대기] 외부 시스템 미참조 정의 반영 — PM/현업

#### A1 [정책+기능설계][D1 대기][Open] 외부 시스템 미참조 정의 반영

- 연결: D1, 관련 발견 2건 (상세 추적의 결정 보드 연결 맵에서 A1로 확인)
- 대상: 정책서 §6·§9, 기능설계서 §5
- 작업: 외부 시스템 미참조 정의와 WCS 플래그 연결 명시
- 완료 조건: 두 문서에 같은 전환 보류 규칙이 반영됨
- 검증 방법:
  - Given Zone이 Closing Planned이고 WCS 연동 플래그가 ON일 때
  - When 나머지 자동 전환 조건이 모두 충족되어도
  - Then Zone은 Inactive로 전환되지 않고 보류 사유가 기록된다
- 담당/결정 필요자: PM/현업
```

규칙:

- 결정 보드가 출력되면 맨 위에 한 줄 범례, `읽는 순서`, `첫 화면 요약`을 둔다. `planning-format`은 `오늘 결정`, `릴리즈 차단`, `바로 수정(결정 불필요)`을 기본으로 하고, 결정 의존 작업이 있으면 `결정 후 반영`을 추가한다. `planning-review`는 필요하면 첫 줄에 `결론`을 추가하되 줄 순서는 `결론 → 오늘 결정 → 릴리즈 차단 → 바로 수정(결정 불필요) → 결정 후 반영`을 따른다.
- `지금 결정해야 할 항목`은 외부 사용자, PM/현업, 기획, 운영 등 권한 있는 결정 필요자의 판단이 필요한 P0/P1, 사용자 확인 필요, 릴리즈 차단 항목만 기본 노출한다. 문서 수정만으로 해소되는 P0/P1은 `D*` 없이 `A*`로 표시할 수 있다.
- 상단 결정 보드는 결정 항목 최대 3개, 작업 항목 최대 5개까지만 펼친다. 초과분은 `그 외 N건은 발견 요약/상세 추적 참조`로 압축한다. 첫 화면 요약의 각 줄은 최대 2개 ID와 `외 N건`까지만 표시한다.
- `릴리즈 차단 항목`이 이미 D* 결정 항목에 연결된 경우, 해당 D* 또는 A*에 `릴리즈 차단` 표시를 붙인다. 그래도 `릴리즈 차단 항목` subsection에는 차단 사유를 한 줄로 남겨 QA/개발이 다시 찾아 올라가지 않게 한다.
- 항목이 없는 subsection은 heading 아래 본문을 정확히 `없음`으로 표시한다. 예: `### 지금 결정해야 할 항목` 다음 줄에 `없음`.
- `D*` 카드에는 `결정 질문`, `선택지`, `초안 추천(확정 필요)`, `결정 필요자`, `반영 위치`, `연결`을 포함한다. 선택지가 원문에서 충분하지 않으면 값을 만들지 말고 `선택지: 확정 필요`로 둔다.
- `A*` 카드는 `유형`, `의존성`, `상태`를 제목 badge로 압축할 수 있다. 연결 D*가 없으면 `[즉시 수정]`, 연결 D*가 있으면 `[D1 대기]`처럼 표시한다. 상세 record와 저장용 구조에서는 `ID`, `연결`, `유형`, `의존성`, `대상`, `작업`, `완료 조건`, `검증 방법`, `담당/결정 필요자`, `상태`를 보존한다.
- `T*` 카드는 `위치`, `차단 이유`, `해소 조건`, `연결`을 포함한다.
- 상단 결정 보드에서 원시 R*/F* ID는 `관련 발견 N건 (상세 추적의 결정 보드 연결 맵에서 D1로 확인)`처럼 해당 D*/A* 추적 키로 접어 표시한다. `planning-review`의 원본 ID mapping은 `발견 요약`, `상세 추적`, fixture의 structured mapping에 유지한다. `planning-format`의 원본 F* mapping은 `검증 피드백`, `상세 추적`, structured mapping에 유지한다.
- `결정 필요자`는 `사용자`, `PM/현업`, `기획`, `운영` 중 하나 또는 조합으로 표시한다. `담당/결정 필요자`는 여기에 `개발`, `QA`를 추가로 허용한다. 알 수 없으면 D* 결정 필요자는 `PM/현업`, A* 담당/결정 필요자는 `PM/현업` 또는 `개발/QA` 역할 단위로 둔다.
- 상단 결정 보드에는 connector 이름, fetch status code, 원시 source table, 원시 finding 전문을 넣지 않는다.

화면 예산:

- 1280x800 데스크톱 첫 화면에서는 헤더 요약, `첫 화면 요약`, 그리고 D* 제목 목록이 보인다.
- 모바일 폭에서는 가로 스크롤 없이 카드/필드 목록으로 줄바꿈한다.
- `지금 결정해야 할 항목`과 `바로 수정할 문서 작업` subsection은 제목 목록(ID / 제목 / 결정 필요자 또는 담당 / 의존성)을 먼저 보여주고, `결정 질문`, `선택지`, `검증 방법` 같은 긴 필드는 제목 목록 아래 상세 카드나 접힘 영역에 둔다.
- 상단 D*/A* 상세 카드 하나는 기본 6개 필드 이하로 접고, 검증 방법처럼 긴 필드는 카드 하단 또는 상세 섹션에 둔다.
- Markdown 표 사용 여부를 판단하는 `60자`는 Markdown link URL, backtick, 강조 기호를 제거한 표시 문자열 기준이다. CJK 글자와 숫자·영문자는 각각 1자로 세고, 연속 공백은 1칸으로 접는다.

## 6. `planning-format` 출력 계약

0.2.10부터 `planning-format` 기본 출력은 사용자 확인 필요 항목 또는 릴리즈 차단 항목이 있을 때 다음 순서를 따른다. 릴리즈 차단 항목은 `[TBD]`뿐 아니라 `fetch 실패`, `원문 정의 부재`, `라벨 미매핑`처럼 현재 MVP 구현·QA 판정을 막는 입력 제외 항목을 포함한다.

````markdown
# [기능명]

- 입력: [사람이 읽는 요약]
- 산출물: 정책서, 기능설계서
- 검증: 피드백 N건, 사용자 확인 필요 M건[, 최우선 확인: 요약 1건]
- 저장: 없음 (--save 미사용) / [저장 경로]

---

## 결정 보드

[범례 / 첫 화면 요약 / 지금 결정해야 할 항목 / 릴리즈 차단 항목 / 바로 수정할 문서 작업]

---

## 정책서

[정책서 본문]

---

## 기능설계서

[기능설계서 본문]

---

## 검증 피드백

[self-review 피드백]

## 출처 요약

[압축 요약]

## 입력 제외 요약

[압축 요약]

## 상세 추적

[조건 충족 시]
````

사용자 확인 필요 항목과 릴리즈 차단 항목이 모두 없으면 `planning-format`은 결정 보드를 생략하고 0.2.9 순서를 유지한다. 이때 상단 검증 줄은 `사용자 확인 필요 없음`을 명확히 표시한다.

### 6.1 `planning-format` 결정 항목 생성 기준

다음 항목은 결정 보드에 올라간다. D*는 사용자/PM/현업/기획/운영 등 권한 있는 결정 필요자가 실제로 선택해야 하는 경우에만 만들고, 결정 없이 문서·입력 보강으로 해소되는 차단은 A* 또는 T*로 처리한다.

| 조건 | 상단 처리 |
|---|---|
| self-review `사용자 확인 필요: 필요` | D* 생성 + 반영 작업이 필요하면 A* 생성 |
| `원문 정의 부재`가 기능 동작·입력 항목·상태 전이에 영향을 주고 사용자 결정이 필요함 | D* + A* 생성 |
| `원문 정의 부재`가 릴리즈를 막지만 문서 보강만으로 해소 가능함 | A* 생성 + `[릴리즈 차단]` badge + 차단 사유 한 줄. 독립 추적 필요 시에만 T* 생성 |
| fetch 실패로 핵심 사용자 흐름·권한·상태 정의가 누락되고 사용자에게 대체 출처·접근 권한 요청이 필요함 | D* 생성 + `[릴리즈 차단]` badge + 차단 사유 한 줄. 독립 추적 필요 시에만 T* 생성 |
| fetch 실패가 릴리즈를 막지만 재시도·connector 변경 같은 작업으로 해소 가능함 | A* 생성 + `[릴리즈 차단]` badge + 차단 사유 한 줄. 독립 추적 필요 시에만 T* 생성 |
| 문서 본문에 `[TBD]`가 있고 릴리즈/구현 판정을 막으며 정책 선택이 필요함 | D* 생성 + `[릴리즈 차단]` badge + 차단 사유 한 줄. 독립 추적 필요 시에만 T* 생성 |
| 문서 본문에 `[TBD]`가 있고 릴리즈/구현 판정을 막지만 결정 항목에 이미 연결됨 | 별도 T* 반복 없이 연결 D*/A*에 `릴리즈 차단` 표시 + 차단 사유 한 줄 |
| `라벨 미매핑`이 상태·권한·데이터 변경·외부 인터페이스·재고/금액/수량·사용자 입력 필수값·기능 동작 판단을 막음 | 사용자 선택 필요 시 D*, 문서/입력 보강만 필요 시 A*. 릴리즈 차단이면 연결 D*/A*에 `[릴리즈 차단]` badge와 차단 사유 한 줄을 붙이고, 독립 추적 필요 시에만 T* 생성 |
| 후속 과제 또는 non-MVP로 명시된 TBD | 아니오. 산출 본문의 `미결 사항`, `발견 요약`, 또는 `입력 제외 요약`에 유지 |
| 단순 포맷 노이즈·기계적 안정화 | 아니오 |

### 6.2 `planning-format` 결정 보드 표시 모드

| 상황 | 결정 보드 처리 |
|---|---|
| 사용자 확인 필요 또는 릴리즈 차단 항목 있음 | `## 결정 보드` 출력. `첫 화면 요약`과 세 subsection을 `지금 결정해야 할 항목 → 릴리즈 차단 항목 → 바로 수정할 문서 작업` 순서로 표시하고 없는 subsection은 `없음`으로 압축 |
| 사용자 확인 필요 없음 + 릴리즈 차단 항목 없음 | `## 결정 보드` 생략. 0.2.9의 `정책서 → 기능설계서 → 검증 피드백` 순서 유지 |
| `--no-self-review` 사용 | self-review 기반 F* 승격은 수행하지 않음. 입력 제외의 `fetch 실패`, `원문 정의 부재`, `라벨 미매핑`, 명시 `[TBD]`가 릴리즈 차단 기준에 해당할 때만 결정 보드 출력 |
| 후속 과제/non-MVP TBD만 있음 | 결정 보드 생략. 산출 본문의 미결 또는 입력 제외 요약에 유지 |
| fetch 실패가 있지만 핵심 사용자 흐름·권한·상태·입력 항목에 영향 없음 | 결정 보드 생략. 출처 요약과 상세 추적에만 유지 |

### 6.3 Zone 관리 `planning-format` 예시

```markdown
## 결정 보드

범례: D=결정, A=문서/구현 작업, R=검토 발견 원본(상세용), T=릴리즈 차단
읽는 순서: 오늘 결정 → 릴리즈 차단 확인 → 바로 수정 → 상세 추적

### 첫 화면 요약

- 오늘 결정: D1 메모 필드 등록/수정 허용 여부
- 릴리즈 차단: 없음
- 바로 수정(결정 불필요): 없음
- 결정 후 반영: A1 메모 입력 항목 정의

### 지금 결정해야 할 항목

- D1 [P1] 메모 필드 등록/수정 허용 여부 — PM/현업

#### D1 [P1] 메모 필드 등록/수정 허용 여부

- 결정 질문: Zone 등록·수정 화면에서 메모 입력을 허용할 것인가?
- 선택지: 1) 선택 입력으로 허용, 2) 상세 화면에만 표시, 3) MVP 제외
- 초안 추천(확정 필요): 선택 입력, 최대 200자. 등록·수정·상세에 동일 노출
- 결정 필요자: PM/현업
- 반영 위치: 기능설계서 §4.1·§4.2·§4.3
- 연결: 관련 발견 1건 (상세 추적의 결정 보드 연결 맵에서 D1로 확인)

### 릴리즈 차단 항목

없음

### 바로 수정할 문서 작업

- A1 [D1 대기] 메모 입력 항목 정의 — PM/현업

#### A1 [기능설계][D1 대기][Open] 메모 입력 항목 정의

- 연결: D1, 관련 발견 1건 (상세 추적의 결정 보드 연결 맵에서 A1로 확인)
- 대상: 기능설계서 §4
- 작업: 메모 입력 항목을 등록·수정 항목에 추가하거나 제외 사유 명시
- 완료 조건: 메모 필드 허용 여부, UI, 최대 길이, 저장/상세 노출 규칙이 한 곳에 정의됨
- 검증 방법:
  - Given Zone 등록 또는 수정 화면에서 메모 입력이 허용될 때
  - When 사용자가 최대 길이를 초과해 저장을 시도하면
  - Then 저장이 차단되고 상세 화면에는 저장된 허용 길이 내 메모만 표시된다
- 담당/결정 필요자: PM/현업
```

## 7. `planning-review` 출력 계약

0.2.10부터 `planning-review` 기본 출력은 다음 순서를 따른다.

````markdown
# planning-review: [기능명]

- 판정: [통과 / 조건부 통과 / 수정 필요 / 검토 필요 / 비교 불가]
- 검증 신뢰도: [충분 / 제한적 / 낮음] — [이유]
- 입력: [사람이 읽는 요약]
- 점검 축: [활성 축만 표시. 예: 검증가능성, 영향 분석]
- 발견: P0 N건, P1 N건, P2 N건

---

## 결정 보드

[범례 / 첫 화면 요약 / 지금 결정해야 할 항목 / 릴리즈 차단 항목 / 바로 수정할 문서 작업]

## 결론

[1~3문장 bottom line]

## 최우선 수정 항목

[아래 내용은 기존 형식 호환을 위한 요약입니다. 실제 판단과 실행 순서는 위 결정 보드를 기준으로 보세요.]

[0.2.9 호환용 요약. 필드: ID / 우선순위 / 항목 / 이유 / 권장 처리. P0/P1 D* 또는 A*를 짧게 재표시. 없으면 없음]

## 작업 백로그

[아래 내용은 기존 형식 호환을 위한 요약입니다. 실제 판단과 실행 순서는 위 결정 보드를 기준으로 보세요.]

[0.2.9 호환용 요약. 필드: ID / 유형 / 대상 / 작업 / 완료 조건. 결정 보드 A*와 결정 보드에 승격하지 않은 P2/SSOT 보강 작업을 짧게 재표시. 없으면 없음]

## 발견 요약

[P0/P1 중심 요약. P2는 압축]

## 검증 범위와 한계

[입력/SSOT/본문 가져오기 실패/비활성 축]

## 출처 요약

[압축 출처]

## 상세 추적

[조건 충족 시 full 입력 출처, SSOT 출처, 원시 발견]
````

0.2.9의 `## 최우선 수정 항목`과 `## 작업 백로그`는 0.2.10에서도 top-level heading 이름을 정확히 유지한다. 괄호나 접미사를 heading에 붙이지 않는다. 기본 사용자 화면의 의미상 source of truth는 `## 결정 보드`이며, 두 legacy 섹션은 호환용 요약이다. 각 섹션 첫 줄에는 `[아래 내용은 기존 형식 호환을 위한 요약입니다. 실제 판단과 실행 순서는 위 결정 보드를 기준으로 보세요.]`를 붙여 중복 본문이 아니라 legacy consumer용 projection임을 알린다. `## 최우선 수정 항목`은 P0/P1 D* 또는 A*를 `ID / 우선순위 / 항목 / 이유 / 권장 처리` 필드로 짧게 재표시한다. `## 작업 백로그`는 결정 보드 A*와, 결정 보드에는 올리지 않았지만 후속 실행이 필요한 P2/SSOT 보강 A*를 `ID / 유형 / 대상 / 작업 / 완료 조건` 필드로 짧게 재표시한다. 사용자-facing legacy summary에는 원시 R*/F* ID를 직접 노출하지 않고, 원본 mapping은 structured mapping과 상세 추적에 둔다. 두 섹션은 최소 0.2.x 동안 유지하며, 제거가 필요하면 별도 breaking PRD에서 다룬다.

### 7.1 결정 항목 ID

`planning-review`는 원시 finding ID와 별도로 결정 항목 ID를 만든다.

| ID | 의미 | 예 |
|---|---|---|
| `D*` | 사용자/PM/현업/기획/운영 등 권한 있는 결정 필요자가 결정해야 하는 항목 | D1 외부 시스템 미참조 정의 |
| `R*` | 검증 finding 원본 | R2-1, R3-1 |
| `A*` | 수정 작업 백로그 | A1 정책서·기능설계서 반영 |
| `T*` | 독립적으로 추적해야 하는 릴리즈 차단 항목 | T1 자동 Inactive 전환 조건 구현 판정 불가 |

규칙:

- `D*`는 외부 사용자, PM/현업, 기획, 운영 등 권한 있는 결정 필요자의 판단이 필요한 항목에만 만든다. P0/P1이라도 문서 수정만으로 해소되는 경우에는 `D*` 없이 `A*`로 표시한다.
- `D*` 카드는 `결정 질문`과 `선택지`를 포함한다. 선택지는 원문 또는 finding에서 도출 가능한 범위로 제한하며, 불충분하면 `선택지: 확정 필요`로 표시한다.
- 하나의 `D*`는 여러 `R*`를 연결할 수 있다.
- 하나의 `A*`는 하나 이상의 `D*` 또는 `R*`를 연결할 수 있다.
- 하나의 `T*`는 하나 이상의 `D*`, `A*`, `R*`를 연결할 수 있다.
- `T*`는 릴리즈 차단 사유가 D*/A*에 충분히 표시되지 않을 때만 별도 생성한다. 차단 사유가 특정 D*/A*에 이미 연결되면 별도 T*를 반복하지 않고 해당 D*/A* 제목에 `[릴리즈 차단]` badge를 붙이고 `릴리즈 차단 항목` subsection에 한 줄 사유를 남긴다.
- `T*` 카드는 `위치`, `차단 이유`, `해소 조건`, `연결`을 포함한다.
- ID는 prefix별로 1부터 연속 부여한다. 예: D1, D2와 A1, A2는 서로 독립된 sequence다.
- `## 작업 백로그` 호환용 요약에만 표시되는 P2/SSOT 보강 A*는 결정 보드 A*의 마지막 번호 뒤에 이어서 부여한다. 결정 보드 A*가 없으면 `## 작업 백로그` 등장 순서대로 A1부터 시작한다.
- `R*` 원시 finding은 하단 상세 추적에서 유지한다.
- 상단 결정 보드는 `D*`, `A*`, `T*`를 중심으로 보여준다.
- 상단 결정 보드의 `연결` 필드에서는 원시 R*/F* ID를 직접 나열하지 않고 `관련 발견 N건 (상세 추적에서 해당 D*/A* ID로 확인)`으로 접는다. 원시 ID는 `발견 요약`, `상세 추적`, structured mapping에 유지한다.

### 7.2 동일 원인 finding 병합

같은 원인과 같은 수정 방향을 가진 finding은 상단에서 하나로 묶는다.

| 병합 대상 | 병합 기준 | 상단 표시 |
|---|---|---|
| R2 검증가능성 + R3 외부 의존 | 같은 계약 부재가 구현 판정과 외부 영향 모두를 유발 | 하나의 D*와 A*로 표시 |
| R1 SSOT 충돌 + R3 영향 분석 | 같은 기준 문서 변경 필요 | R1을 주 finding으로 두고 R3는 연결 finding으로 표시 |
| 여러 P2 동기화 권고 | 같은 운영 워크플로로 해소 가능 | 하나의 A*로 묶고 P2 상세는 발견 요약에 압축 |

병합은 원시 finding을 삭제하지 않는다. `## 상세 추적`에는 축별 원시 발견을 유지한다.

### 7.3 Zone 관리 `planning-review` 예시

```markdown
## 결정 보드

범례: D=결정, A=문서/구현 작업, R=검토 발견 원본(상세용), T=릴리즈 차단
읽는 순서: 오늘 결정 → 릴리즈 차단 확인 → 바로 수정 → 상세 추적

### 첫 화면 요약

- 결론: 자동 비활성 전환 계약과 이동 통제 결과가 미정이라 수정 필요
- 오늘 결정: D1 외부 시스템 미참조 정의, D2 상태 필드 처리, D3 DEFECT → OUTBOUND 허용 여부
- 릴리즈 차단: D1 - WCS 플래그 효과 미정으로 자동 전환 QA 불가
- 바로 수정(결정 불필요): A2 이동 성공 결과 정의
- 결정 후 반영: A1 외부 시스템 정의, A3 상태 변경 경로, 외 1건

### 지금 결정해야 할 항목

- D1 [P0][릴리즈 차단] 외부 시스템 미참조의 정의 — PM/현업
- D2 [P1] 수정 화면의 상태 필드 처리 — 기획
- D3 [P1] DEFECT → OUTBOUND 이동 허용 여부 — 운영

#### D1 [P0][릴리즈 차단] 외부 시스템 미참조의 정의

- 결정 질문: Closing Planned → Inactive 자동 전환에서 WCS 연동 여부 플래그 ON을 외부 참조 중으로 볼 것인가?
- 선택지: 1) ON = 외부 참조 중, 2) 별도 외부 참조 테이블로 판단, 3) MVP에서는 WCS 참조 조건 제외
- 초안 추천(확정 필요): MVP에서는 WCS 연동 여부 플래그 ON = 외부 참조 중으로 간주
- 결정 필요자: PM/현업
- 반영 위치: 정책서 §6·§9, 기능설계서 §5
- 연결: 관련 발견 2건 (상세 추적의 결정 보드 연결 맵에서 D1로 확인)

#### D2 [P1] 수정 화면의 상태 필드 처리

- 결정 질문: Zone 수정 화면에서 상태 라디오를 직접 수정 가능하게 둘 것인가?
- 선택지: 1) 표시 전용, 2) 전용 액션 버튼으로만 전환, 3) 라디오 유지 + 금지 전이 비활성화
- 초안 추천(확정 필요): 상태는 표시 전용, 전환은 전용 액션으로만 처리
- 결정 필요자: 기획
- 반영 위치: 기능설계서 §4.2·§5
- 연결: 관련 발견 1건 (상세 추적의 결정 보드 연결 맵에서 D2로 확인)

#### D3 [P1] DEFECT → OUTBOUND 이동 허용 여부

- 결정 질문: DEFECT 출발, OUTBOUND 도착 이동을 허용할 것인가?
- 선택지: 1) 허용, 2) 차단, 3) 특정 권한/작업 유형에서만 허용
- 초안 추천(확정 필요): 허용/차단 중 하나를 명시. 정책 미정이면 기본값을 만들지 않고 결정 필요로 표시
- 결정 필요자: 운영
- 반영 위치: 정책서 §9.1
- 연결: 관련 발견 1건 (상세 추적의 결정 보드 연결 맵에서 D3로 확인)

### 릴리즈 차단 항목

D1에 연결됨 - WCS 플래그 효과 미정으로 자동 전환 QA 불가. 별도 T* 반복 항목 없음.

### 바로 수정할 문서 작업

- A1 [D1 대기] 외부 시스템 미참조 정의 반영 — PM/현업
- A2 [즉시 수정] Zone 간 이동 성공 결과 정의 — 기획
- A3 [D2 대기] 상태 변경 경로 정리 — 기획
- A4 [D3 대기] DEFECT → OUTBOUND 이동 행 추가 — 운영

#### A1 [정책+기능설계][D1 대기][Open] 외부 시스템 미참조 정의 반영

- 연결: D1, 관련 발견 2건 (상세 추적의 결정 보드 연결 맵에서 A1로 확인)
- 대상: 정책서 §6·§9, 기능설계서 §5
- 작업: 외부 시스템 미참조 정의와 WCS 플래그 연결 명시
- 완료 조건: 두 문서에 같은 전환 보류 규칙이 반영됨
- 검증 방법:
  - Given Zone이 Closing Planned이고 WCS 연동 플래그가 ON일 때
  - When 나머지 자동 전환 조건이 모두 충족되어도
  - Then Zone은 Inactive로 전환되지 않고 보류 사유가 기록된다
- 담당/결정 필요자: PM/현업

#### A2 [기능설계][즉시 수정][Open] Zone 간 이동 성공 결과 정의

- 연결: 관련 발견 1건 (상세 추적의 결정 보드 연결 맵에서 A2로 확인)
- 대상: 기능설계서 §5
- 작업: Zone 간 이동 성공 결과 정의
- 완료 조건: 재고 레코드 변경, 이동 이력, 응답 신호가 명시됨
- 검증 방법:
  - Given 허용된 Zone 간 이동 요청이 성공할 때
  - When 이동 처리가 완료되면
  - Then 재고 레코드의 Zone 필드와 이동 이력이 갱신되고 성공 응답에 이동 이력 ID가 포함된다
- 담당/결정 필요자: 기획

#### A3 [기능설계][D2 대기][Open] 상태 변경 경로 정리

- 연결: D2, 관련 발견 1건 (상세 추적의 결정 보드 연결 맵에서 A3로 확인)
- 대상: 기능설계서 §4.2·§5
- 작업: 상태 필드를 표시 전용 또는 전용 액션 처리로 정리
- 완료 조건: Active → Inactive 직접 전이 경로가 문서에서 제거됨
- 검증 방법:
  - Given Active Zone 수정 화면에 진입했을 때
  - When 사용자가 상태를 Inactive로 직접 변경하려 하면
  - Then 상태 필드는 표시 전용이거나 전용 액션만 제공되어 직접 전이가 불가능하다
- 담당/결정 필요자: 기획

#### A4 [정책서][D3 대기][Open] DEFECT → OUTBOUND 이동 행 추가

- 연결: D3, 관련 발견 1건 (상세 추적의 결정 보드 연결 맵에서 A4로 확인)
- 대상: 정책서 §9.1
- 작업: DEFECT → OUTBOUND 허용/차단 행 추가
- 완료 조건: 모든 Zone Type 이동 조합의 기대값이 명시됨
- 검증 방법:
  - Given 출발 Zone Type이 DEFECT이고 도착 Zone Type이 OUTBOUND일 때
  - When 이동 통제 모듈이 매트릭스를 평가하면
  - Then 정책서 §9.1의 명시 행에 따른 허용/차단 결과를 반환한다
- 담당/결정 필요자: 운영
```

### 7.4 `planning-review` 결정 보드 표시 모드

| 상황 | 결정 보드 처리 |
|---|---|
| P0/P1 finding 있음 | 외부 결정 필요 항목은 D*, 문서 수정만 필요한 항목은 A*로 표시. top-level `## 최우선 수정 항목`, `## 작업 백로그`도 호환용 요약으로 유지 |
| P2-only review | 결정 항목은 `없음`. P2 작업은 `## 작업 백로그` 호환용 요약과 `## 발견 요약`에 압축하고, 릴리즈 차단과 직접 연결된 P2만 결정 보드 A*로 승격 |
| SSOT-only low confidence + R2/R3 finding 없음 | 결정 항목은 `없음`. SSOT 보강 작업은 `## 작업 백로그` 호환용 요약에 표시하고 판정은 0.2.9 규칙에 따라 `비교 불가` 유지 |
| `--axes ac`처럼 SSOT 비활성 | SSOT 보강 작업을 만들지 않음 |
| 후속 과제/non-MVP TBD만 있음 | 결정 항목은 `없음`. 발견 요약 또는 검증 범위와 한계에 압축 |

### 7.5 병합 키와 정렬

상단 병합은 선택 사항이 아니라 기본 동작이다. 다음 키가 모두 같으면 같은 원인 finding으로 본다.

- 같은 문서 위치 또는 같은 정책/기능 개념을 가리킨다.
- 같은 미정 계약, 충돌 값, 또는 관찰 불가 조건에서 비롯된다.
- 같은 결정 또는 같은 문서 수정으로 해소된다.

병합하면 대표 우선순위는 연결 finding 중 가장 높은 우선순위를 사용한다. ID는 `D*`, `A*`, `T*` prefix별로 상단 출력 등장 순서에 따라 1부터 연속 부여한다. 같은 prefix와 같은 우선순위 안에서는 P0/P1, 릴리즈 차단, 입력 등장 순서, 연결 finding ID 순서로 정렬한다.

## 8. 차단 항목 등급화

0.2.10부터 `[TBD]`, `fetch 실패`, `원문 정의 부재`, `라벨 미매핑`은 다음 등급으로 분류한다.

| 등급 | 의미 | 상단 노출 |
|---|---|---|
| `릴리즈 차단` | 구현·QA·운영 판정을 막는 미정 항목 | 결정 보드 `릴리즈 차단 항목`에 표시 |
| `결정 필요` | 출시 전 확정이 바람직하지만 임시 정책이나 non-MVP 제외가 가능 | `지금 결정해야 할 항목` 또는 발견 요약에 표시 |
| `후속 과제` | 문서가 명시적으로 후속과제/non-MVP로 제외 | 상단에는 count만, 산출 본문의 미결 사항 또는 상세 추적에 유지 |
| `추적 로그` | fetch 실패, 입력 제외, 라벨 미매핑 등 감사 추적 | 출처/입력 제외/상세 추적에 유지 |

릴리즈 차단 판단 기준:

- 상태 전이, 권한, 데이터 변경, 외부 인터페이스, 재고/금액/수량 변경, 사용자 입력 필수값에 직접 영향을 준다.
- 정책서와 기능설계서가 서로 다른 구현 경로를 열어둔다.
- QA가 성공/실패 기준을 쓸 수 없다.
- 운영자가 수행 여부를 판단할 수 없다.

후속 과제로 명시된 항목은 상단을 오염시키지 않는다. 단, 후속 과제라고 적혀 있어도 현재 MVP 동작의 필수 조건이면 `릴리즈 차단`으로 올린다.

릴리즈 차단 항목의 출력 규칙:

- 사용자 선택이 필요한 차단은 D*를 만들고 D* 제목에 `[릴리즈 차단]`을 붙인다.
- 문서 또는 입력 보강만 필요한 차단은 A*를 만들고 필요하면 T*로 별도 추적한다.
- 특정 D*/A*로 충분히 해소 조건을 설명할 수 있으면 별도 T*를 만들지 않는다.
- 별도 T*를 만들지 않더라도 `릴리즈 차단 항목` subsection에는 차단 사유와 연결 D*/A*를 한 줄로 남긴다.

## 9. 검증 가능한 AC 문장화

P0/P1 finding 또는 그와 연결된 작업 백로그는 최소 1개 이상의 검증 문장을 포함해야 한다.

권장 형식:

```markdown
- 검증 방법:
  - Given Zone이 Closing Planned이고 WCS 연동 플래그가 ON일 때
  - When 나머지 자동 전환 조건이 모두 충족되어도
  - Then Zone은 Inactive로 전환되지 않고 보류 사유가 기록된다
```

표 안에 넣기 길면 `검증 방법` 셀에는 짧은 요약을 쓰고, 같은 항목의 카드/필드 목록에 Given/When/Then을 풀어 쓴다.

검증 문장 작성 규칙:

- 상태 전이는 시작 상태, 트리거, 종료 상태를 포함한다.
- 데이터 변경은 변경되는 필드와 관찰 가능한 이력 또는 응답을 포함한다.
- 권한은 역할, 허용/차단 행위, 사용자에게 보이는 결과를 포함한다.
- 외부 인터페이스는 외부 시스템명, 참조 플래그/ID, 실패 또는 보류 조건을 포함한다.
- `테스트 작성 가능`, `테스트 케이스 작성 가능`, `체크리스트 작성 가능`처럼 가능 여부만 말하는 문장은 P0/P1 검증 방법으로 인정하지 않는다. 실제 관찰 신호가 없으면 `구현/QA 차단` 사유로 올린다.

## 10. 사용자-facing 용어

상단 결정 보드에서는 내부 검증 용어를 그대로 노출하지 않는다.

| 내부/기술 용어 | 상단 권장 표기 |
|---|---|
| `R2 Acceptance Criteria` | 검증가능성 |
| `R3 deps` | 영향 분석 |
| `AC Blocker` | 구현/QA 차단 |
| `SSOT corpus` | SSOT 기준 문서 묶음 |
| `placeholder` | 본문 없는 자리표시자 |
| `fetch failed` | 본문 가져오기 실패 |
| `Action Backlog` | 작업 백로그 |
| `ssot, ac, deps` | 기준 문서 일치성, 검증가능성, 영향 분석 |

원시 finding ID와 내부 축 이름은 `발견 요약`과 `상세 추적`에서 병기할 수 있다.

`planning-review` 상단의 `점검 축`은 실제 활성화된 축만 한국어로 표시한다. 예를 들어 `--axes ac` 호출은 `점검 축: 검증가능성`으로 표시하고, 비활성 축은 `검증 범위와 한계`에만 적는다.

## 11. 호환성

| 영역 | 0.2.9 → 0.2.10 |
|---|---|
| `planning-format` 기본 화면 출력 | 사용자 확인 필요/릴리즈 차단 항목이 있으면 정책서·기능설계서 전에 `결정 보드`를 출력 |
| `planning-review` 기본 화면 출력 | 결정 보드를 추가하고 D*/R*/A* 연결 체계를 도입. 0.2.9 parser 호환을 위해 top-level `## 최우선 수정 항목`과 `## 작업 백로그` 유지 |
| 상세 추적 | 0.2.9와 동일하게 하단 유지 |
| 저장 파일 | 변경 없음. `planning/` 아래 canonical 정책서·기능설계서 저장 |
| SSOT corpus | 변경 없음. 독립 `SSOT` token 폴더명 기준과 `planning/**` 제외 유지 |
| downstream parser | `## 결정 보드`가 새 wrapper heading으로 추가됨. 정책서/기능설계서 추출기는 `## 결정 보드`를 산출 본문으로 오인하면 안 됨 |

### 11.1 readable projection parser 영향

0.2.10 화면 출력에서는 `## 결정 보드`가 `## 정책서`보다 앞에 올 수 있다.

parser 규칙:

1. wrapper heading은 줄 시작의 정확한 H2만 인정한다. 예: `## 결정 보드`, `## 정책서`, `## 기능설계서`, `## 결론`. CRLF는 LF로 정규화하고, 파일 첫 BOM은 무시하며, trailing whitespace는 제거한다. leading space, closing hash(`## 결정 보드 ##`), H3 이하 heading은 wrapper로 인정하지 않는다.
2. fenced code block 안, blockquote 안, 리스트 하위에 있는 `## 결정 보드` 문자열은 wrapper heading으로 보지 않는다. fenced code block은 backtick fence와 tilde fence를 모두 포함한다.
3. 닫히지 않은 fenced code block이 있으면 이후 heading은 wrapper로 인정하지 않고 `readable projection boundary ambiguous` warning을 남긴다.
4. `planning-format`에서 첫 `## 정책서`보다 앞의 첫 번째 `## 결정 보드`만 report metadata로 취급한다.
5. `planning-review`에서 첫 `## 결론`보다 앞의 첫 번째 `## 결정 보드`만 review report metadata로 취급한다.
6. 같은 metadata 영역에 추가 `## 결정 보드`가 있으면 duplicate decision board로 보고 해당 line부터 다음 인정된 wrapper H2 직전까지 body에서 제외하며 `readable projection boundary ambiguous` warning을 남긴다.
7. 정책서 본문은 여전히 첫 `## 정책서` wrapper heading 다음 줄에서 시작한다.
8. 기능설계서 본문은 여전히 첫 `## 기능설계서` wrapper heading 다음 줄에서 시작한다.
9. 정책서·기능설계서 본문 종료 경계는 0.2.9와 동일하게 다음 wrapper heading 중 먼저 등장하는 항목이다: `## 기능설계서`, `## 검증 피드백`, `## 출처 요약`, `## 입력 제외 요약`, `## 상세 추적`, `## 결론`, `## 최우선 수정 항목`, `## 작업 백로그`, EOF.
10. `## 결정 보드`는 정책서·기능설계서 본문 경계로 사용하지 않는다.
11. 생성된 정책서·기능설계서 본문 내부에서는 `## 결정 보드`를 top-level H2로 쓰지 않는다. 같은 의미의 본문 heading이 필요하면 `### 결정 보드 관련 정책`처럼 H3 이하를 사용한다.
12. `## 결정 보드`가 metadata 위치가 아닌 곳에 나타나면 invalid wrapper sentinel로 감지한다. parser는 해당 `## 결정 보드` line부터 다음 인정된 wrapper H2 직전까지를 정책서·기능설계서 body에서 제외하고 `readable projection boundary ambiguous` warning을 남긴다. 다음 wrapper가 없으면 EOF 직전까지 제외한다.
13. duplicate/misplaced `## 결정 보드`의 모든 warning 문자열은 `readable projection boundary ambiguous`로 고정한다.
14. legacy consumer가 `## 결정 보드`와 `## 작업 백로그` 호환용 요약을 모두 읽는 경우, 같은 A* ID는 `## 결정 보드`를 우선하고 호환용 요약을 중복 count하지 않는다.
15. 항목 없음 표현은 해당 subsection heading 아래 본문을 정확히 `없음`으로 둔다. `지금 결정해야 할 항목: 없음`처럼 heading과 값을 한 줄에 합치지 않는다.

## 12. 구현 영향 범위

- `skills/planning-format/SKILL.md` — 출력 순서에 조건부 `결정 보드` 삽입 규칙 추가.
- `skills/planning-format/references/output-contract.md` — `결정 보드` 섹션, 사용자 확인 필요 항목 상단 승격, 차단 항목 등급화 규칙 추가.
- `skills/planning-format/references/self-review-rules.md` — F* 피드백을 D*/A*/T* 결정 보드 항목으로 승격하는 기준 추가.
- `skills/planning-format/references/exclusion-rules.md` — `원문 정의 부재`, `fetch 실패`, `라벨 미매핑`의 릴리즈 차단/후속/추적 분류 기준 추가.
- `skills/planning-format/references/conversion-rules.md` — 결정 보드 카드 표시 우선, 5열 이상/60자 이상 긴 셀 분해 기준 재사용, `## 결정 보드` reserved wrapper heading 추가.
- `skills/planning-review/SKILL.md` — 기본 출력 구조를 결정 보드 우선으로 변경.
- `skills/planning-review/references/ac-rules.md` — P0/P1 finding의 검증 문장 생성 요구 추가.
- `skills/planning-review/references/deps-rules.md` — 같은 원인 finding 병합과 외부 인터페이스 결정 항목 생성 기준 추가.
- `skills/planning-review/references/ssot-rules.md` — SSOT 한계가 decision board에 올라갈 조건과 그렇지 않은 조건 명시.
- `planning-kit/docs/planning-format-workflow.md` — 단일 응답 출력 다이어그램에 `결정 보드` 노드 추가.
- `planning-kit/docs/planning-review-workflow.md` — Step 4/5에 D*/A* grouping과 decision board 출력 추가.
- `planning-kit/docs/diagram/*.html`, `planning-kit/docs/diagram/*.png` — workflow 문서 다이어그램을 갱신하는 경우 versioned diagram 산출물 재생성.
- `planning-kit/docs/prd/README.md` — 0.2.10 chain row 추가.
- `planning-kit/README.md` 또는 release note — 사용자-facing 출력 변경 안내 추가.
- `planning-kit/.codex-plugin/plugin.json`, `planning-kit/.claude-plugin/plugin.json`, `.agents/plugins/marketplace.json` — release 구현 시 version `0.2.10`과 `결정 보드`/`decision board` description token 갱신.

## 13. 수용 기준

1. `planning-format`에서 사용자 확인 필요 항목이 1건 이상 있거나 릴리즈 차단 항목이 있으면 기본 출력은 헤더 요약 다음 `## 결정 보드`를 포함한다.
2. `planning-format`에서 사용자 확인 필요 항목과 릴리즈 차단 항목이 모두 없으면 `## 결정 보드`를 생략하고 0.2.9의 정책서 우선 순서를 유지한다.
3. `planning-format`에서 `## 결정 보드`를 출력하면 범례, `읽는 순서`, `첫 화면 요약`, `지금 결정해야 할 항목`, `릴리즈 차단 항목`, `바로 수정할 문서 작업` subsection을 이 순서대로 출력한다. `읽는 순서`는 `오늘 결정 → 릴리즈 차단 확인 → 바로 수정 → 상세 추적`으로 표시한다.
4. 항목이 없는 subsection은 heading 아래 본문을 정확히 `없음`으로 표시한다.
5. `planning-format`의 정책서 본문은 여전히 `## 정책서` 아래에 있고, 기능설계서 본문은 `## 기능설계서` 아래에 있다.
6. `planning-review` 기본 출력은 헤더 요약 다음 `## 결정 보드`를 포함한다.
7. `planning-review`의 `첫 화면 요약`은 `결론`, `오늘 결정`, `릴리즈 차단`, `바로 수정(결정 불필요)`, `결정 후 반영` 순서로 최대 5줄까지 표시한다.
8. `D*`는 사용자/PM/현업/기획/운영 등 권한 있는 결정 필요자의 판단이 필요한 항목에만 만든다.
9. P0/P1이라도 문서 수정만으로 해소되는 finding은 `D*` 없이 `A*`로 표시할 수 있다.
10. `D*` 카드는 `결정 질문`, `선택지`, `초안 추천(확정 필요)`, `결정 필요자`, `반영 위치`, `연결`을 포함한다.
11. `A*` 상세 record는 `ID`, `연결`, `유형`, `의존성`, `대상`, `작업`, `완료 조건`, `검증 방법`, `담당/결정 필요자`, `상태`를 포함한다. 상단 카드에서는 `유형`, `의존성`, `상태`를 제목 badge로 압축할 수 있으며, 연결 D*가 없으면 `[즉시 수정]`, 연결 D*가 있으면 `[D1 대기]`처럼 표시한다.
12. P0/P1 작업의 `검증 방법`은 시작 상태, 트리거, 결과, 관찰 가능한 데이터·이력·응답 중 해당 축에 맞는 신호를 포함한다.
13. P0/P1 검증 방법이 `테스트 작성 가능` 같은 가능성 문장만 포함하면 실패로 본다.
14. P0/P1 finding에 관찰 가능한 신호가 없거나 해당 축의 필수 요소를 충족하지 못해 검증 문장을 만들 수 없으면 그 자체를 별도 `구현/QA 차단` 사유로 표시한다.
15. 같은 문서 위치/같은 정책 개념/같은 해소 작업을 공유하는 `R2-*`와 `R3-*` finding은 상단 결정 보드에서 하나의 `D*` 또는 `A*`로 묶는다.
16. 병합하지 않아야 하는 finding은 서로 다른 결정 필요자, 서로 다른 반영 위치, 서로 다른 완료 조건 중 하나 이상을 가진다.
17. `T*` 카드는 `위치`, `차단 이유`, `해소 조건`, `연결`을 포함한다.
18. `D*`, `A*`, `T*` ID는 prefix별로 상단 출력 등장 순서에 따라 1부터 연속 부여한다.
19. 같은 prefix와 같은 우선순위 안에서는 P0/P1, 릴리즈 차단, 입력 등장 순서, 연결 finding ID 순서로 정렬한다.
20. 원시 finding ID는 삭제되지 않고 `planning-review`의 `발견 요약`, `상세 추적`, structured mapping에서 확인 가능하다. `planning-format`의 원시 F* ID는 `검증 피드백`, `상세 추적`, structured mapping에서 확인 가능하다. 상단 결정 보드의 `연결` 필드에서는 원시 R*/F* ID를 `관련 발견 N건 (상세 추적의 결정 보드 연결 맵에서 해당 D*/A* ID로 확인)`으로 접어 표시한다.
21. `[TBD]`, `fetch 실패`, `원문 정의 부재`, `라벨 미매핑`은 `릴리즈 차단`, `결정 필요`, `후속 과제`, `추적 로그` 중 하나로 분류된다. `라벨 미매핑`이 상태·권한·데이터 변경·외부 인터페이스·재고/금액/수량·사용자 입력 필수값·기능 동작 판단을 막으면 릴리즈 차단으로 승격한다.
22. 릴리즈 차단 항목은 결정 보드에 표시되며, 이미 D*/A*에 연결된 경우 별도 T*로 반복하지 않고 연결된 D*/A*에 `릴리즈 차단` 표시와 차단 사유 한 줄을 붙인다.
23. 후속 과제로 명시된 TBD는 현재 구현 판정을 막지 않는 한 결정 보드에 펼치지 않는다.
24. 사용자 결정이 필요한 차단은 D*로, 문서/입력 보강만 필요한 차단은 A*로 처리한다. T*는 D*/A*에 충분히 연결되지 않는 독립 차단 항목에만 별도 생성한다.
25. 상단 결정 보드에는 connector 세부 status, full source URL table, full SSOT corpus table을 출력하지 않는다.
26. 상단 결정 보드에는 `SSOT corpus`, `fetch`, `deps`, `AC Blocker`를 단독 표기로 쓰지 않고, 각각 `SSOT 기준 문서 묶음`, `본문 가져오기`, `영향 분석`, `구현/QA 차단`으로 표시한다.
27. `planning-review` 상단 `점검 축`은 실제 활성 축만 한국어로 표시한다. 비활성 축은 `검증 범위와 한계`에만 표시한다.
28. `planning-review`에서 `R2-1 외부 시스템 미참조 미정의`와 `R3-1 WCS 플래그 연결 계약 부재`가 같은 원인일 경우 하나의 결정 항목으로 묶인다.
29. R1 SSOT 충돌과 R3 영향 분석이 같은 기준 문서 변경으로 해소되면 하나의 D*/A*로 묶는다.
30. 여러 P2 동기화 권고가 같은 운영 워크플로로 해소되면 하나의 A*로 묶는다.
31. Zone 관리 review 예시에서 상단 결정 보드는 `외부 시스템 미참조 정의`, `수정 화면 상태 필드`, `DEFECT → OUTBOUND 이동 허용 여부`를 먼저 보여준다.
32. Zone 관리 review 예시의 작업 백로그는 즉시 수정 가능한 A*와 결정 후 반영할 A*를 의존성 badge로 구분하고, 각 항목마다 완료 조건, 검증 방법, 담당/결정 필요자를 포함한다.
33. `planning-review`는 top-level `## 최우선 수정 항목`과 `## 작업 백로그` heading 이름을 정확히 유지한다.
34. `## 최우선 수정 항목` 호환용 요약은 첫 줄에 `[아래 내용은 기존 형식 호환을 위한 요약입니다. 실제 판단과 실행 순서는 위 결정 보드를 기준으로 보세요.]`를 두고 `ID / 우선순위 / 항목 / 이유 / 권장 처리` 필드를 포함한다.
35. `## 작업 백로그` 호환용 요약은 첫 줄에 `[아래 내용은 기존 형식 호환을 위한 요약입니다. 실제 판단과 실행 순서는 위 결정 보드를 기준으로 보세요.]`를 두고 `ID / 유형 / 대상 / 작업 / 완료 조건` 필드를 포함하며, 결정 보드 A*와 결정 보드에 승격하지 않은 P2/SSOT 보강 A*를 포함할 수 있다.
36. readable projection parser는 줄 시작의 정확한 H2 wrapper heading만 경계로 인정한다.
37. wrapper H2는 CRLF 정규화, 첫 BOM 제거, trailing whitespace 제거 후 판정하며 leading space와 closing hash는 허용하지 않는다.
38. backtick/tilde fenced code block, blockquote, 리스트 하위의 `## 결정 보드` 문자열은 wrapper heading으로 보지 않는다.
39. `planning-format`에서 첫 `## 정책서`보다 앞의 첫 번째 `## 결정 보드`만 report metadata로 취급한다.
40. `planning-review`에서 첫 `## 결론`보다 앞의 첫 번째 `## 결정 보드`만 review report metadata로 취급한다.
41. 정책서·기능설계서 본문 종료 경계는 0.2.9 wrapper heading과 EOF를 유지한다.
42. 생성된 정책서·기능설계서 본문 내부에서는 `## 결정 보드`를 top-level H2로 쓰지 않는다.
43. metadata 위치가 아닌 곳의 `## 결정 보드`와 metadata 영역의 두 번째 이후 `## 결정 보드`는 invalid wrapper sentinel로 감지하고, 해당 line부터 다음 인정된 wrapper H2 직전 또는 EOF 직전까지 body에서 제외한다.
44. duplicate/misplaced `## 결정 보드`와 unclosed fenced code block의 warning 문자열은 `readable projection boundary ambiguous`로 고정한다.
45. 0.2.9 이하 산출물 입력은 계속 읽을 수 있다. `## 결정 보드`가 없는 입력은 legacy로 처리한다.
46. legacy consumer가 결정 보드와 호환용 요약을 모두 읽으면 같은 ID는 결정 보드를 우선하고 호환용 요약을 중복 count하지 않는다.
47. `## 작업 백로그` 호환용 요약에만 표시되는 P2/SSOT 보강 A*는 결정 보드 A* 마지막 번호 이후에 이어 부여한다. 결정 보드 A*가 없으면 작업 백로그 등장 순서대로 A1부터 부여한다.
48. `planning-format --save` 저장 파일 구조와 저장 경로는 0.2.9와 동일하며 canonical 저장 파일에는 top-level `## 결정 보드`가 포함되지 않는다.
49. `planning/**`과 `.planning-kit/**`은 계속 SSOT corpus 근거가 될 수 없다.
50. 결정 보드는 기본적으로 카드/필드 목록으로 표시한다. 물리적 Markdown 표는 5열 이하이고 모든 셀이 60자 이하일 때만 사용할 수 있다.
51. `60자`는 Markdown link URL, backtick, 강조 기호를 제거한 표시 문자열 기준으로 계산한다.
52. 카드/필드 목록으로 분해할 때 필드명과 값은 보존한다.
53. 1280x800 데스크톱 첫 화면에서는 헤더 요약, `첫 화면 요약`, D* 제목 목록이 보인다.
54. 모바일 폭에서는 결정 보드가 가로 스크롤 없이 카드/필드 목록으로 줄바꿈된다.
55. 상단 결정 보드는 결정 항목 최대 3개, 작업 항목 최대 5개까지만 펼치고 초과분은 발견 요약/상세 추적 참조로 압축한다. 첫 화면 요약의 각 줄은 최대 2개 ID와 `외 N건`까지만 표시한다.
56. `결정 필요자`를 알 수 없으면 임의 개인명을 만들지 않고 `PM/현업`을 기본값으로 둔다. D* 결정 필요자는 `사용자`, `PM/현업`, `기획`, `운영` 중 하나 또는 조합으로 표시한다. A* 담당/결정 필요자는 여기에 `개발`, `QA`를 추가로 허용한다.
57. 추천안이 정책 결정을 포함하면 컬럼 또는 필드명을 `초안 추천(확정 필요)`로 표시한다. 사용자 승인 전 추천안을 canonical 본문에 확정 반영하지 않는다.
58. P2-only review에서 릴리즈 차단 항목이 없으면 결정 보드의 해당 subsection은 `없음`으로 표시하고, P2 작업은 top-level `## 작업 백로그` 호환용 요약과 `## 발견 요약`에 압축한다.
59. `검증 신뢰도: 낮음`의 원인이 SSOT 0건뿐이고 R2/R3 finding이 없으면 결정 보드에는 결정 항목을 만들지 않고, SSOT 보강 작업은 top-level `## 작업 백로그` 호환용 요약에 표시하며, 판정은 0.2.9 규칙에 따라 `비교 불가`를 유지한다.
60. `--axes ac`처럼 SSOT가 비활성인 호출은 SSOT 보강 작업을 결정 보드나 작업 백로그에 만들지 않는다.
61. self-review `사용자 확인 필요: 필요` F*는 D*로 승격하고, 반영 작업이 필요하면 A*를 생성하며, raw F* ID는 상단에서 접고 `검증 피드백`, `상세 추적`, structured mapping에 유지한다.
62. `planning-format --no-self-review`에서는 self-review 기반 F* 승격을 수행하지 않는다.
63. `planning-format --no-self-review`라도 입력 제외의 `fetch 실패`, `원문 정의 부재`, `라벨 미매핑`, 명시 `[TBD]`가 릴리즈 차단 기준에 해당하면 결정 보드를 출력한다.
64. `planning-format --no-self-review`이고 non-blocking trace만 있으면 결정 보드를 출력하지 않는다.
65. `planning-format` 결정 보드의 `첫 화면 요약`은 `오늘 결정`, `릴리즈 차단`, `바로 수정(결정 불필요)`을 기본으로 표시하고, 결정 의존 작업이 있으면 `결정 후 반영`을 추가한다.
66. `planning-format`에서 결정 보드를 출력하지 않을 때 상단 검증 줄은 `사용자 확인 필요 없음`을 명시한다.
67. `planning-review` 상세 추적에는 `결정 보드 연결 맵`을 포함하고 D*/A*/T*와 원시 R*/F* ID의 mapping을 사람이 읽을 수 있게 보존한다.
68. release note 또는 README에는 0.2.10의 상단 결정 보드 추가와 legacy parser 주의사항이 포함된다.
69. release 구현 시 `planning-kit/.codex-plugin/plugin.json`, `planning-kit/.claude-plugin/plugin.json`, `.agents/plugins/marketplace.json` 각각의 version은 `0.2.10`이고 description은 `결정 보드` 또는 `decision board` token을 포함한다.
70. workflow 문서나 Mermaid/HTML/PNG diagram을 수정하는 release 구현에서는 `planning-format-workflow`와 `planning-review-workflow` 다이어그램에 결정 보드 노드가 반영된 산출물을 재생성한다.

## 14. 최소 검증 fixture

각 fixture는 최소한 `input`, `args`, `expected_present`, `expected_absent`, `expected_mapping`, `expected_section_order`, `expected_legacy_summary_rows`를 가진다. 원시 R*/F* ID는 상단 decision board와 사용자-facing legacy summary에서 숨기고 상세 추적에는 유지해야 하므로 fixture는 `expected_scoped_absent.decision_board`, `expected_scoped_absent.legacy_summary`, `expected_scoped_present.detail_trace`를 지원한다. parser fixture는 추가로 `expected_boundary_result`를 가지며, 최소 필드는 `extracted_policy_contains`, `extracted_policy_absent`, `extracted_feature_contains`, `extracted_feature_absent`, `excluded_ranges`, `warnings`다. `expected_boundary_result.warnings` 값은 모든 duplicate/misplaced decision board 케이스에서 `readable projection boundary ambiguous`로 고정한다.

대표 golden expectation:

```yaml
fixture: Zone 관리 planning-review
args: ["planning-review", "policy-url", "feature-url"]
expected_present:
  - "범례: D=결정, A=문서/구현 작업, R=검토 발견 원본(상세용), T=릴리즈 차단"
  - "읽는 순서: 오늘 결정 → 릴리즈 차단 확인 → 바로 수정 → 상세 추적"
  - "D1 [P0][릴리즈 차단] 외부 시스템 미참조의 정의"
  - "A1 [정책+기능설계][D1 대기][Open] 외부 시스템 미참조 정의 반영"
  - "연결: 관련 발견 2건 (상세 추적의 결정 보드 연결 맵에서 D1로 확인)"
  - "아래 내용은 기존 형식 호환을 위한 요약입니다. 실제 판단과 실행 순서는 위 결정 보드를 기준으로 보세요."
  - "릴리즈 차단: D1 - WCS 플래그 효과 미정으로 자동 전환 QA 불가"
expected_absent:
  - "지금 결정해야 할 항목: 없음"
  - "테스트 케이스 작성 가능"
expected_scoped_absent:
  decision_board:
    - "R2-1"
    - "R3-1"
  legacy_summary:
    - "R2-1"
    - "R3-1"
expected_scoped_present:
  detail_trace:
    - "결정 보드 연결 맵"
    - "D1 -> R2-1, R3-1"
    - "R2-1 / P0 / 검증가능성 / 외부 시스템 미참조 미정의"
    - "R3-1 / P1 / 영향 분석 / WCS 플래그 연결 계약 부재"
expected_mapping:
  D1: ["R2-1", "R3-1"]
  A1: ["D1", "R2-1", "R3-1"]
  A2: ["R2-2"]
  A3: ["D2", "R2-3"]
  A4: ["D3", "R2-4"]
  T: []
expected_section_order:
  - "## 결정 보드"
  - "## 결론"
  - "## 최우선 수정 항목"
  - "## 작업 백로그"
  - "## 발견 요약"
  - "## 검증 범위와 한계"
expected_legacy_summary_rows:
  - "D1/A1 외부 시스템 미참조 정의"
  - "A2 Zone 간 이동 성공 결과 정의"
```

대표 parser boundary expectation:

```yaml
fixture: duplicate decision board inside policy
args: ["planning-review", "legacy-output.md"]
expected_boundary_result:
  extracted_policy_contains:
    - "정상 정책 본문"
  extracted_policy_absent:
    - "오염된 결정 보드 본문"
  extracted_feature_contains:
    - "정상 기능설계 본문"
  extracted_feature_absent:
    - "오염된 결정 보드 본문"
  excluded_ranges:
    - from_heading: "## 결정 보드"
      to_before_heading: "## 기능설계서"
      reason: "duplicate/misplaced decision board"
  warnings:
    - "readable projection boundary ambiguous"
```

대표 release metadata expectation:

```yaml
fixture: release metadata
expected_metadata:
  - path: "planning-kit/.codex-plugin/plugin.json"
    version_jsonpath: "$.version"
    expected_version: "0.2.10"
    description_jsonpath: "$.description"
    description_contains_any: ["결정 보드", "decision board"]
  - path: "planning-kit/.claude-plugin/plugin.json"
    version_jsonpath: "$.version"
    expected_version: "0.2.10"
    description_jsonpath: "$.description"
    description_contains_any: ["결정 보드", "decision board"]
  - path: ".agents/plugins/marketplace.json"
    entry_selector: "$.plugins[?(@.id=='planning-kit')]"
    version_jsonpath: "$.version"
    expected_version: "0.2.10"
    description_jsonpath: "$.description"
    description_contains_any: ["결정 보드", "decision board"]
```

| Fixture | 검증 목적 |
|---|---|
| Zone 관리 `planning-format` | 메모 필드 누락 F5-1이 D1/A1로 승격되고 `첫 화면 요약`에 오늘 결정·릴리즈 차단·바로 수정(결정 불필요)·결정 후 반영이 순서대로 표시되는지 확인 |
| Zone 관리 `planning-review` | R2-1/R3-1 병합, D*/R*/A* 연결, 결정 질문·선택지·Given/When/Then 검증 방법 포함 확인 |
| P0 없는 P2-only review | 결정 보드의 결정 subsection은 `없음`, P2 작업은 legacy `## 작업 백로그`와 `## 발견 요약`에 압축되는지 확인. expected absent: `#### D`, `#### T` |
| SSOT-only low confidence | R2/R3 finding이 없으면 판정은 `비교 불가`, SSOT 보강 A*는 legacy `## 작업 백로그`에만 나타나는지 확인. expected absent: decision board A*, D*, T* |
| `--axes ac` review | `점검 축: 검증가능성`만 표시하고 SSOT 보강 작업을 만들지 않는지 확인 |
| 릴리즈 차단 항목 | 상태 전이·외부 인터페이스 TBD 또는 입력 제외가 D*/A*/T* 또는 연결된 D*/A*의 `릴리즈 차단` 표시로 올라오는지 확인 |
| 후속 과제 TBD | non-MVP/후속과제 항목이 결정 보드에 펼쳐지지 않고 산출 본문 미결 또는 상세 추적에 유지되는지 확인 |
| `planning-format --no-self-review` 차단 입력 | self-review F* 없이도 릴리즈 차단 `원문 정의 부재`, `라벨 미매핑`, 명시 `[TBD]`가 D*/A*로 승격되는지 확인 |
| `planning-format --no-self-review` non-blocking fetch | 핵심 사용자 흐름·권한·상태·입력 항목에 영향 없는 fetch 실패가 결정 보드를 만들지 않는지 확인 |
| `planning-format --no-self-review` 후속 TBD | 후속 과제/non-MVP TBD만 있을 때 결정 보드를 만들지 않는지 확인 |
| 입력 제외 등급화 | `fetch 실패`, `원문 정의 부재`, `라벨 미매핑`이 릴리즈 차단/결정 필요/후속 과제/추적 로그로 각각 분류되는지 확인 |
| 검증 문장화 | P0/P1 finding마다 관찰 가능한 Given/When/Then 또는 동등 문장이 있는지 확인 |
| 검증 문장 실패 | P0/P1 검증 방법이 `테스트 작성 가능`만 포함하면 fixture가 실패하는지 확인 |
| 검증 문장 생성 불가 | 관찰 신호가 부족한 finding이 `구현/QA 차단` 사유로 표시되는지 확인 |
| 카드형 표시 | 5열 초과 또는 표시 문자열 60자 초과 셀이 있는 결정 보드가 카드/필드 목록으로 분해돼도 필드명과 값이 보존되는지 확인 |
| 모바일 카드 표시 | 작은 폭에서 결정 보드가 가로 스크롤 없이 줄바꿈되고 D*/A* 카드가 6개 필드 이하로 접히는지 확인 |
| 0.2.9 legacy 입력 | 결정 보드 없는 0.2.9 산출물도 review 입력으로 계속 처리되는지 확인 |
| 0.2.8 fenced code 입력 | code fence 안의 `## 결정 보드` 문자열을 wrapper로 오인하지 않는지 확인 |
| blockquote heading 입력 | blockquote 안의 `## 결정 보드` 문자열을 wrapper로 오인하지 않는지 확인 |
| list child heading 입력 | 리스트 하위의 `## 결정 보드` 문자열을 wrapper로 오인하지 않는지 확인 |
| tilde fence 입력 | tilde code fence 안의 `## 결정 보드` 문자열 처리 기준을 fixture expected boundary result로 고정 |
| unclosed fence 입력 | 닫히지 않은 code fence 안의 `## 결정 보드` 처리 기준을 fixture expected boundary result로 고정 |
| `.planning-kit/**` SSOT 제외 | `.planning-kit/**` 문서가 SSOT corpus 근거로 선택되지 않는지 확인 |
| reserved heading invalid case | 정책서·기능설계서 본문 내부 top-level `## 결정 보드`를 wrapper 오염으로 감지하는지 확인 |
| duplicate decision board before policy | 정책서 전 metadata 영역에 두 번째 `## 결정 보드`가 나오면 본문 병합 없이 `readable projection boundary ambiguous` warning을 남기는지 확인 |
| duplicate decision board inside policy | 정책서 내부 두 번째 `## 결정 보드`를 body에서 제외하고 `readable projection boundary ambiguous` warning을 남기는지 확인 |
| invalid decision board exclusion range | misplaced/duplicate `## 결정 보드` line부터 다음 인정된 wrapper H2 직전까지 body에서 제외되는지 확인 |
| misplaced decision board after feature | `## 결정 보드`가 `## 기능설계서` 뒤에 잘못 배치돼도 기능설계서 본문에 병합하지 않는지 확인 |
| misplaced decision board between policy and feature | `## 결정 보드`가 `## 정책서`와 `## 기능설계서` 사이에 잘못 배치돼도 정책서 본문에 병합하지 않는지 확인 |
| invalid none expression | `### 지금 결정해야 할 항목: 없음`을 exact-none contract 위반으로 감지하는지 확인 |
| 0.2.9 planning-format no 검증 피드백 | `## 검증 피드백` 없이 `## 출처 요약`이 바로 오는 legacy 입력에서 기능설계서 body가 올바르게 종료되는지 확인 |
| 0.2.9 planning-review standalone | `## 결정 보드` 없이 `## 결론`으로 시작하는 legacy review를 정상 파싱하는지 확인 |
| save canonical no board | `planning-format --save` canonical 정책서·기능설계서 파일에 top-level `## 결정 보드`가 없는지 확인 |
| legacy review headings | `planning-review`가 top-level `## 최우선 수정 항목`과 `## 작업 백로그` heading 이름을 정확히 유지하는지 확인 |
| legacy summary fields | 최우선 수정 항목과 작업 백로그 호환용 요약이 각각 요구 필드를 포함하는지 확인 |
| legacy summary dedupe | 같은 A* ID가 결정 보드와 `## 작업 백로그`에 동시에 있으면 결정 보드를 우선하고 중복 count하지 않는지 확인 |
| legacy-only A* numbering | P2/SSOT 보강 A*가 결정 보드 A* 마지막 번호 이후에 이어 부여되는지 확인 |
| R1+R3 병합 | 같은 기준 문서 변경으로 해소되는 R1/R3 finding이 하나의 D*/A*로 병합되는지 확인 |
| 병합 negative | 결정 필요자·반영 위치·완료 조건이 다른 finding은 병합하지 않는지 확인 |
| ID 정렬 | D*/A*/T* ID가 prefix별 우선순위와 등장 순서에 따라 1부터 연속 부여되는지 확인 |
| release metadata | release 구현 시 `planning-kit/.codex-plugin/plugin.json`, `planning-kit/.claude-plugin/plugin.json`, `.agents/plugins/marketplace.json` 각각의 version이 `0.2.10`이고 description에 `결정 보드` 또는 `decision board` token이 포함되는지 확인 |
| workflow diagram | workflow diagram 산출물에 `결정 보드` node label이 포함되고 HTML/PNG가 함께 갱신되는지 확인 |
| 추천안/확정값 분리 | 정책 추천이 `초안 추천(확정 필요)`로 표시되고 canonical 본문에 확정 반영되지 않는지 확인 |
| 결정 필요자 fallback | 개인명을 알 수 없을 때 역할 단위 담당/결정 필요자가 표시되는지 확인 |
| 용어 정리 | 상단 결정 보드가 내부 축 이름보다 한국어 업무 표현을 우선하는지 확인 |
