# planning-kit PRD 0.2.5

> 0.2.4 기반 incremental PRD. 7개 변경 — (1~2) fetch·queue 결정성 / (3~7) 변환·라벨링·검증 결정성. 같은 입력 N회 실행 시 산출물 일치율을 ~1%(0.2.4) → ~25~39%(0.2.5)로 28~43배 끌어올린다 (영역 독립 가정 상한 39%, 상관 보수 추정 25~30%). 본 PRD 외 명세는 [`prd-0.2.4.md`](./prd-0.2.4.md) 이하 chain 그대로.
>
> 비목표 정책(cap 없음·marker 1종·본문 cite 없음·worker 없음)은 부분 조정 — list 분해 max-depth cap 1건 신설 외 모두 유지.

## 1. 변경 요약

**A. fetch·queue 결정성 (1~2)**

1. **fetch 시도 의무화** — queue dequeue된 visited 미포함 URL은 100% fetch 시도 강제. 사전 판단으로 시도 자체를 생략 금지. 시도 후 실패는 출처 list `상태` 컬럼 기록 + visited 등록. fetch 미시도 허용은 `--no-fetch` 단 1케이스.
2. **BFS 순서 강제** — depth N 모두 dequeue 완료 후 depth N+1 dequeue. 같은 depth 안에선 본문 발견 순서 유지. LIFO·우선순위 휴리스틱 금지.

**B. 변환·라벨링·검증 결정성 (3~7)**

3. **exclusion 11 카테고리 결정 트리** — `exclusion-rules.md` §2 우선순위에 결정 트리 명시. main 자유 판단을 if-elif chain으로 대체.
4. **모호성 강제 [TBD] 룰** — 원문 syntactic 결함(괄호 미닫힘·"…"·빈 list·공란 row)을 자동 [TBD] 단정 + `원문 정의 부재` 카테고리.
5. **list 분해 max-depth cap = 3** — `conversion-rules.md` §5.4 다층 분해에 cap 도입. cap 도달 시 합류 유지로 폴백.
6. **self-review F1~F6 체크리스트화** — `self-review-rules.md`에 점검 항목별 체크리스트 (yes/no 6 카테고리 × 26 항목, 6패스). 검출 누락 차단.
7. **라벨 매핑 룰 강화** — `conversion-rules.md` §4 라벨 매핑에 결정 트리 + 양 매핑 분배 룰.

`planning-review` 동작 변경 없음 (R1·R2·R3 그대로).

## 2. 동기

### 2.1 fetch 미시도 사례 (1)

0.2.4 같은 입력(Confluence URL 1개, 자식 URL 3개) 3회 실행 비교에서 fetch queue 처리 비결정성 식별:

| 런 | Confluence main | Figma board | Google Sheets | Confluence 공통가이드 |
|---|---|---|---|---|
| 1 | fetch 시도 | fetch 시도 → 실패 | fetch 성공 | fetch 성공 |
| 2 | fetch 시도 | fetch 시도 → 실패 | fetch 성공 | fetch 성공 |
| 3 | fetch 시도 | **fetch 미시도** | fetch 성공 | fetch 성공 |

Run 3가 Figma board URL을 dequeue 자체 안 함. SKILL.md Step 3 "URL 한 개씩 dequeue → fetch"가 main 판단으로 사전 skip 가능 (인증 미연결 추정 등). connector-routing.md §5 표는 "fetch 시도 후 실패" 정책이지만 dequeue 단계에서 LLM이 사전 판단 시 룰 우회.

### 2.2 queue 순서 비결정성 (2)

depth·발견 순서 명시 없음. 같은 입력에서 dequeue 순서가 다르면 fetch 시도 우선순위·timeout 분배·자식 URL 발견 시점 모두 달라짐. 출처 list `#` 번호 부여 순서도 비결정.

### 2.3 변환·라벨링·검증 비결정성 (3~7)

같은 3 Run 비교 결과:

| 영역 | Run 1 | Run 2 | Run 3 | 결정성 |
|---|---|---|---|---|
| TBD 개수 | 7 | 11 | 7 | ~50% |
| 입력 제외 건수 | 12 | 9 | 12 | ~40% |
| 자체 검증 발견 | 4 | 2 | 2 | ~50% |
| 보조 표 분해 깊이 | 2 | 4 | 3 sub-§ | ~50% |

LLM 자유 판단 영역 6곳 식별:

- list 분해 (이질·동질) — `conversion-rules.md` §5.5
- 기능명 1순위 — §3
- 충돌 후보 1순위 — `exclusion-rules.md` §1 #11
- anchor 매칭 — `connector-routing.md` §11.5
- F5.2.2 cross-ref-scope 키워드 grep — `self-review-rules.md`
- 라벨 매핑 경계 — `conversion-rules.md` §4

LLM이 "이 항목은 어느 카테고리?"를 매번 판단하면 동일 입력에서도 다른 라벨 부여. 결정 트리(if A then X, elif B then Y)는 입력 조각의 syntactic feature 기준으로 분류 → LLM stochasticity 영향 최소화.

### 2.4 비목표 정책 부분 조정

- **cap 없음 정책**: list 분해 max-depth 1건만 도입 (3). 그 외 fetch·body·input cap 유지.
- **marker 1종 정책**: `[TBD]` 1종 그대로. 모호성 룰도 `[TBD]` 사용.
- **본문 cite 없음 정책**: 변경 없음.

## 3. 비목표

- depth·pages·body·fanout cap 도입 안 함 (cap 없음 정책 그대로, list 분해 cap 1건만 예외).
- visited dedup 정책 변경 없음 — 같은 normalize URL 1회만 fetch.
- self-anchor·`mailto:`/`tel:`/`javascript:`/`blob:`/scheme 없는 URL 제외 룰 유지 (queue 시드 단계).
- 인증 실패 케이스 자동 복구 안 함 — 시도 + 실패 status 기록까지가 책임.
- 1회 호출 안 timeout·retry·backoff 변경 없음 (connector-routing.md §5 표 그대로).
- temperature 조정·model lock·cache 강제 등 LLM 자체 결정성 강화 안 함 (runtime 책임).
- marker 신설 안 함 (`[TBD-AMBIG]`·`[TBD-CONFLICT]` 등 X).
- planning-review 동작 변경 없음.
- 본문 cite·trace·dedup view 도입 안 함.
- 후속 PRD 도입 항목: trace 옵션·snapshot diff·regression test suite·meta JSON 자동 저장·fanout cap opt-in·429 backoff.

## 4. fetch 시도 의무화

### 4.1 룰

`SKILL.md` Step 3 강화:

- queue dequeue된 visited 미포함 URL은 **100% fetch 시도 강제**.
- 인증 미연결·매핑 없음·미인증 추정 등 사전 판단으로 시도 자체를 생략 **금지**.
- 시도 후 실패(인증 게이트·timeout·4xx/5xx·빈 본문·미지원 content-type)는 출처 list `상태` 컬럼에 사유 기록 + visited 등록.
- fetch 미시도 허용은 `--no-fetch` 단 1케이스.

### 4.2 1차 시도 = WebFetch 의무

`connector-routing.md` §5 케이스 표는 그대로. 단 모든 케이스의 진입 조건은 "1차 WebFetch 시도 후"로 통일. main이 §2 connector 카탈로그를 사전 평가해 "미연결" 판정해도 1차 WebFetch는 진행.

| 사전 판정 | 0.2.4 동작 | 0.2.5 동작 |
|---|---|---|
| connector 미연결 | 시도 생략 가능 | 1차 WebFetch 시도 강제. 인증 게이트면 status=`인증 필요 (<connector> 미연결)` |
| 매핑·추론 후보 0 + 인증 게이트 추정 | 시도 생략 가능 | 1차 WebFetch 시도 강제. 결과로 분류 |
| 미인증 connector | 시도 생략 가능 | 1차 WebFetch 시도 강제. 인증 게이트면 status=`인증 필요 (<connector> 미인증)` |

connector fallback도 §2 카탈로그가 인증된 후보를 반환하면 1회 시도. 미인증 fallback은 호출 안 함 (시도해도 실패 자명).

### 4.3 출처 list 기록 의무

모든 dequeue된 URL은 출처 list 1행 차지. status는 `200 (...)` / `인증 필요 (...)` / `timeout` / `4xx/5xx` / `빈 본문` 중 하나. **dequeue 후 행 누락 금지**.

## 5. BFS 순서 강제

### 5.1 룰

`SKILL.md` Step 3 강화:

- depth N 모두 dequeue 완료 후 depth N+1 dequeue.
- 같은 depth 안에선 본문 발견 순서 유지 (markdown link 등장 순서 → HTML href 순서 → plain URL 순서).
- LIFO·우선순위 휴리스틱 금지 (예: "Figma는 인증 무거우니 마지막에" 식 정렬 금지).

### 5.2 normalize 시점

dequeue 직전이 아니라 **queue push 시점**에 normalize. 같은 normalize 결과는 visited 검사로 1회만 fetch. self-anchor·mailto/tel/javascript/blob/non-http은 시드 단계에서 이미 제외.

### 5.3 출처 list `#` 번호 부여

BFS dequeue 순서가 곧 출처 list `#` 순서. depth 0 root URL이 #1·#2·..., depth 1 자식 URL이 그 다음.

## 6. exclusion 11 카테고리 결정 트리

### 6.1 룰

`exclusion-rules.md` §2 우선순위 chain을 결정 트리로 확장. 분기 순서 = 현 §2 우선순위 그대로.

```
입력 조각 X 라벨링:

1. X가 정책서 §2 / 기능설계서 §2 제외 범위 표 키워드 매칭
   → 범위 외

2. ELIF X가 외부 자원 인용·참조이고 출처 list 본문 사용=X
   → fetch 실패

3. ELIF X가 원문 단일 표·구조이고 본문에서 sub-§으로 분해
   → 구조 변환

4. ELIF X가 라벨 매핑은 됐으나 디테일 일부가 인접 도메인
   → 디테일 축약

5. ELIF X가 syntactic 결함 (괄호 미닫힘·"…"·빈 list·공란 row·16 어구)
   → 원문 정의 부재 (자동 [TBD] 본문 합류 + cross-ref)

6. ELIF X가 기능명 추출 후보 list 2위 이하
   → 다른 기능 후보

7. ELIF X가 입력에 ≥2회 등장 + 1회만 본문 합류
   → 중복

8. ELIF X가 추측·draft 메모·임시 작성
   → 근거 부족 무시

9. ELIF X가 cite·markup·metadata·꾸밈
   → 포맷 노이즈

10. ELIF X가 같은 사실에 대한 ≥2 다른 값 단정 인용
    → 충돌 후보

11. ELSE
    → 라벨 미매핑 (폴백 — 8/10 섹션 자리 없음 또는 위 분기 미커버)
```

11 분기 = 11 카테고리 1:1. 라벨 미매핑은 단일 폴백.

### 6.2 트리 진입 조건 (syntactic feature)

각 분기는 syntactic feature 또는 출처 list 행 기준. LLM 의미 해석 최소화:

| 분기 | 진입 조건 |
|---|---|
| `fetch 실패` | 출처 list 행 `본문 사용=X` + 입력 본문에 해당 URL 인용 substring |
| `범위 외` | 정책서/기능설계서 §2 제외 표 셀 텍스트 키워드 grep 매칭 |
| `원문 정의 부재` | 정규식 매칭 (`\([^)]*$` 괄호 미닫힘 / `…` 또는 `\.\.\.` / 빈 표 row / "확정 시 재정의" 등 16 어구) |
| `충돌 후보` | 같은 entity (역할·상태·임계·권한) ≥2 출처에서 다른 값 단정 |
| `구조 변환` | 본문 sub-§(`### N.M`)에 분산 |
| `디테일 축약` | 본문 매핑 row 존재 + 일부 디테일 누락 |
| `중복` | 같은 substring ≥2회 등장 + 1회만 본문 |
| `근거 부족 무시` | "추측" / "draft" / "임시" / "?" 표현 |
| `포맷 노이즈` | XML/HTML 태그·smartlink·metadata 패턴 |
| `다른 기능 후보` | 기능명 추출 후보 list 2위 이하 |

### 6.3 main override

트리 결과가 명백히 부적절하면 main이 override 가능. override 시 입력 제외 § `설명` 줄에 `(main override: <이유>)` 표기 의무.

## 7. 모호성 강제 [TBD] 룰

### 7.1 트리거 패턴

`exclusion-rules.md` 신규 §3.1 추가. 다음 syntactic 결함 발견 시 자동 처리:

| 패턴 | 정규식 / 검출 | 처리 |
|---|---|---|
| 괄호 미닫힘 | `\([^)]*$` (라인 끝) | 본문 셀 `[TBD]` + 카테고리 `원문 정의 부재` |
| 말줄임표 | `…` 또는 `\.\.\.` (확정 표현 끝) | 본문 셀 `[TBD]` |
| 공란 row | 표 셀 모두 빈 string | row 삭제 + 카테고리 `원문 정의 부재` |
| 빈 list | "다음과 같다" / "기본값으로 제공" + 후속 본문 부재 | `[TBD]` |
| "확정 시 재정의" / "추후 정의" / "TBD" / "별도 정의" / "추후 결정" | substring 매칭 | `[TBD]` + 미결 § 항목 |
| "[ ]" / "_____" / "—" 단독 | 셀 본문 | `[TBD]` |

### 7.2 본문 합류 규칙

검출된 본문 셀 = `[TBD]` 단정 (LLM 추론 단정 금지). 미결 § 항목 추가 + 입력 제외 § 항목 추가 + cross-ref.

```
본문 셀: [TBD]
↓ (cross-ref)
미결 § N: <항목 설명>. 원문 syntactic 결함: <패턴>. 입력 제외 § #M 참조.
↓ (cross-ref)
입력 제외 § #M: 카테고리 = 원문 정의 부재. 처리 = [TBD] 추적 (미결: 정책서 §10 #N).
```

### 7.3 16 어구 카탈로그

`exclusion-rules.md` 신규 §3.2 표:

| 어구 | 처리 |
|---|---|
| TBD / TODO / FIXME | `[TBD]` |
| 추후 정의 / 추후 결정 / 추후 협의 | `[TBD]` |
| 별도 정의 / 별도 협의 / 별도 확정 | `[TBD]` |
| 확정 시 재정의 / 확정 후 정의 | `[TBD]` |
| 미정 / 미확정 / 미결 | `[TBD]` |
| 기획 시 정의 / 작업 기획 시 구체화 | `[TBD]` |

main이 위 어구 발견 시 단정 추론 금지.

## 8. list 분해 max-depth cap

### 8.1 룰

`conversion-rules.md` §5.4 다층 분해에 cap 도입:

- max-depth = **3**. (`§N.M`·`§N.M.K`·`§N.M.K.L`까지 허용. `§N.M.K.L.P` 금지)
- depth 4 진입 시도 시 **합류 유지로 폴백**. 본 셀에 `[TBD]` 또는 짧은 list 단축.
- 폴백 시 입력 제외 § 항목 추가 — 카테고리 `디테일 축약`, 처리 `라벨 매핑은 정책서 §N.M / 기능설계서 §K.L, depth-cap 도달로 디테일 미합류`.

### 8.2 cap 근거

3 Run 비교에서 분해 깊이 1·2·3 모두 등장. 4 이상 발견 안 됨. cap 3 = 관측 최대값. 운영 가독성·테이블 너비 고려.

### 8.3 비목표 정책 호환

cap 없음 정책의 단일 예외. fetch·body·input cap 그대로 없음. cap 도입 사유 = 동일 입력에서 분해 깊이 일관성 확보 + 가독성. 후속 PRD에서 cap 조정·옵션화 검토 가능.

## 9. self-review F1~F6 체크리스트화

### 9.1 룰

`self-review-rules.md` 각 카테고리에 체크리스트 추가. main이 단일 LLM 패스로 "발견 있나요?"만 묻지 말고, 체크리스트 항목별 yes/no 답:

```
F1. 섹션 충실도
□ 정책서 §1~§10 각각 본문 row ≥1 있나
□ 기능설계서 §1~§8 각각 본문 row ≥1 있나
□ 보조 표 §N.M 각각 데이터 row ≥1 있나
□ 정책서 [TBD] / 본문 셀 비율 ≤50%
□ 기능설계서 [TBD] / 본문 셀 비율 ≤50%

F2. 라벨 cross-bleed
□ 정책서 §3~§10 본문에 "화면"/"버튼"/"입력 폼"/"클릭" 단어 부재
□ 기능설계서 §4~§7 본문에 "허용"/"금지"/"예외 승인" 단어 부재
□ 정책서 sub-§ 본문에 화면 동작 단어 부재
□ 기능설계서 sub-§ 본문에 정책 단어 부재

F3. 두 문서 간 용어 일관성
□ 역할명 표기 통일 (1 표기/entity)
□ 상태명 표기 통일
□ 권한명 표기 통일
□ 도메인 stem 통일

F4. 정책-기능 매핑
□ 정책서 §5 규칙 1개당 기능설계서 §5 또는 §7 매핑 ≥1
□ 정책서 §6 상태 전이 1개당 기능설계서 §5 액션 매핑 ≥1
□ 정책서 §7 권한 1개당 기능설계서 §6 행 매핑 ≥1
□ 정책서 `금지` 액션이 기능설계서 정상 흐름 부재

F5. 누락 핵심 정보
□ F5.1 본문 누락: 입력 명시 사실(역할·상태·기능명·수치 임계) 모두 본문/입력 제외 § 등장
□ F5.2.1 cross-ref-fetch: 출처 list `본문 사용=X` 행마다 입력 제외 § `fetch 실패` 항목 매칭
□ F5.2.2 cross-ref-scope: 정책서/기능설계서 §2 제외 표 키워드 → 입력 제외 § `범위 외` 항목 매칭
□ F5.2.3 cross-ref-tbd: 미결 § "원문 명시 없음" 등 어구 → 입력 제외 § `원문 정의 부재` 항목 매칭

F6. Markdown syntax lint
□ 코드 펜스 짝 맞음
□ 표 컬럼 수 일치
□ 헤더 레벨 점프 없음 (sub-§ 정상 case 제외)
□ 빈 인용 부호 없음
□ list marker 일관
```

### 9.2 발견 카운트

체크리스트 □ 중 unchecked 1개 = 발견 1건. 발견 0건 = 통과. 발견 ≥1건 = `발견 N건`. 0.2.4 발견 분포 헤더(`충실도 0건·cross-bleed 0건·...`) 그대로.

### 9.3 LLM 패스 횟수

체크리스트 26 항목을 6 카테고리 단위로 묶어 6패스 진행 (카테고리당 1패스). 0.2.4는 1패스 → 누락 가능. 0.2.5는 6패스 → 누락 차단. 추가 비용: 2~5초 (체크리스트 형식이 짧음).

## 10. 라벨 매핑 룰 강화

### 10.1 결정 트리

`conversion-rules.md` §4 라벨 매핑 1줄 가이드를 결정 트리로 확장:

```
입력 조각 X 매핑:

1. X가 화면·UI·필드·버튼·입력 폼·메시지·표시
   → 기능설계서

2. X가 사용자 흐름·트리거·액션·동작 시퀀스
   → 기능설계서

3. X가 권한·접근 통제·데이터 가시성
   → 양쪽 (정책서 §7 + 기능설계서 §6) — §10.2 분배 룰

4. X가 규칙·금지·허용·임계·조건 판단 기준
   → 정책서

5. X가 상태 전이·전환 트리거·상태 처리 기준
   → 정책서

6. X가 예외·승인·결정 권한·운영 대응 기준
   → 정책서

7. X가 외부 시스템 연동 정책·실패 대응
   → 정책서

8. X가 용어 정의·범위·원칙
   → 정책서

9. ELSE
   → 입력 제외 § `라벨 미매핑` 폴백
```

분기 3은 명시적 양 매핑(권한·접근 통제). §10.2 분배 룰은 분기 3 + 권한·연동·상태 영역에 적용.

### 10.2 양 매핑 분배 룰

권한·연동 등 양 매핑 가능 영역:

| 측면 | 정책서 위치 | 기능설계서 위치 |
|---|---|---|
| 권한 — 역할 책임·정책 의도 | §7 | — |
| 권한 — 화면 접근·액션 가능 여부 | — | §6 |
| 연동 — 정책·실패 시 업무 대응 | §9 | — |
| 연동 — 액션 트리거·메시지 | — | §5·§7 |
| 상태 — 전이 룰·조건 | §6 | — |
| 상태 — 화면 표시·전환 액션 | — | §3·§5 |

같은 entity가 두 문서 모두 등장 가능. 단 표현 측면 다름. F2 cross-bleed 룰은 그대로 — 정책서에 화면 단어 / 기능설계서에 정책 단어 금지.

### 10.3 매핑 충돌 처리

X가 트리 분기 ≥2 매칭 시:

- §10.1 트리 위쪽 우선 (1~8 순서).
- 분기 3 (권한·접근) 매칭 시 양 매핑 + §10.2 분배 룰.
- 1~8 모두 미해당 시 분기 9 폴백 (`라벨 미매핑`).

### 10.4 sub-§ 분배 시점

분배 결정은 §6.2 변환 시점에 1회. sub-§ 분해(§5)는 분배 후 적용. 같은 entity가 정책서 §7·기능설계서 §6 양쪽에 sub-§ 가질 수 있음 (예: §7.1 권한 매트릭스 vs §6.1 화면 접근 매트릭스).

## 11. 호환성

| 영역 | 0.2.4 → 0.2.5 |
|---|---|
| `--no-fetch`·`--no-image`·`--no-self-review`·`--save` | 동일 |
| visited dedup·시드 제외 룰 | 동일 |
| **fetch 시도 의무** | **신규 (queue dequeue → 100% 시도)** |
| **BFS 순서** | **신규 (depth + 발견 순서 강제)** |
| **list 분해 max-depth** | **신규 cap = 3** |
| depth·pages·body·fanout cap | 동일 (없음, list 분해만 예외) |
| marker 1종 정책 | 동일 (`[TBD]` 1종) |
| 11 카테고리 list | 동일 |
| **11 카테고리 우선순위** | **결정 트리화** (라벨 미매핑만 폴백으로 이동, 그 외 순서 그대로) |
| **모호성 처리** | **자동 [TBD] + 16 어구 카탈로그** |
| 자체 검증 6 카테고리 | 동일 |
| **자체 검증 패스 횟수** | **1패스 → 6패스 체크리스트** |
| **라벨 매핑** | **결정 트리화 + 양 매핑 분배 룰** |
| 출처 list 형식 | 동일 (deep link 0.2.4 유지) |
| 입력 제외 § 11 카테고리 | 동일 |
| timeout | 동일 — connector 호출당 30초 1회 |
| planning-review | 동일 |

기존 산출물 재실행 시 차이:
1. fetch 미시도가 사라짐 — 모든 발견 URL이 출처 list에 등장.
2. 출처 list `#` 번호 비결정성 해소.
3. 분해 깊이 4 산출물 → depth-3 cap 폴백 (디테일 축약 항목 추가).
4. exclusion 카테고리 분포 → 결정 트리 결과로 재라벨 가능.
5. 모호성 표현 → 자동 [TBD] 단정.
6. 자체 검증 발견 건수 → 체크리스트 6패스로 일반적으로 증가.
7. 라벨 매핑 모호 케이스 → 결정 트리 + 분배 룰.

## 12. 결정성 영향

### 12.1 정량 추정 (3 Run 비교 기준)

| 영역 | 0.2.4 | 0.2.5 | 개선 동인 |
|---|---|---|---|
| fetch 시도 | 70% | **100%** | §4 시도 의무 |
| 출처 list 순서 | 60% | **100%** | §5 BFS |
| 출처 list 항목 수 | 70% | **100%** | §4 기록 의무 |
| list 분해 깊이 | 50% | **85%** | §8 cap |
| exclusion 분류 | 40% | **80%** | §6 결정 트리 |
| 모호성 [TBD] | 50% | **95%** | §7 정규식 + 16 어구 |
| F1~F6 검출 | 50% | **75%** | §9 체크리스트 6패스 |
| 라벨 매핑 | 60% | **80%** | §10 결정 트리 + 분배 룰 |

### 12.2 전체 일치 확률 (영역 독립 가정)

- **0.2.4**: 0.7 × 0.6 × 0.7 × 0.5 × 0.4 × 0.5 × 0.5 × 0.6 ≈ **0.9%**
- **0.2.5**: 1.0 × 1.0 × 1.0 × 0.85 × 0.8 × 0.95 × 0.75 × 0.8 ≈ **39%**

0.9% → 39%. **약 43배 개선**.

**단서**: 위 곱셈은 8개 영역 독립 가정. 실제로는 영역 간 상관 존재 — fetch 영역 결정성이 exclusion `fetch 실패` 카테고리 결정성에 직결, 라벨 매핑 결정성이 exclusion `라벨 미매핑` 카테고리 결정성에 직결, list 분해 깊이가 exclusion `구조 변환` 위치에 직결. 상관 ≥0.3 가정 시 보수적 추정 = **~25~30%**. 39%는 상한, 25~30%는 하한. 어느 쪽이든 0.2.4 대비 28~43배 개선 범위.

### 12.3 100% 미달 잔여 비결정

- LLM 자체 stochasticity (temperature·sampling)
- 결정 트리 진입 조건 자체의 LLM 해석 (정규식·키워드 grep도 LLM이 매칭)
- 양 매핑 모호 케이스 main override
- 미결 § 항목 cross-ref 매칭

100% 결정성은 LLM 본질상 불가. 후속 PRD에서 trace 옵션·snapshot diff로 수동 verification 보강.

## 13. 검증·자체 검증 룰 영향

- F5.2 `cross-ref-fetch`: 입력 제외 § `fetch 실패` 항목 ↔ 출처 list 행 매칭. 0.2.5에서 모든 dequeue URL이 출처 list 행 가지므로 match 100% 보장. 누락 없음.
- F1·F2·F3·F4·F5·F6 체크리스트화로 검출 누락 차단.
- planning-review R1·R2·R3 동작 변경 없음.

## 14. 대안 검토

| 대안 | 채택 여부 |
|---|---|
| 발견 URL 자체에 cap (`--max-fanout N`) | 비목표 — cap 없음 정책. 후속 PRD 후보 |
| 사전 인증 평가 후 미인증 connector fallback skip 유지 | 채택 — 1차 WebFetch만 강제. fallback은 인증 후보만 시도 |
| BFS 대신 DFS | 비채택 — 발견 순서 추적 어려움. 출처 list 번호 부여 비결정 |
| queue 우선순위 (인증된 connector 우선) | 비채택 — 결정성·예측성 손상 |
| `--no-fetch` 외 fetch skip 옵션 추가 | 비채택 — 단일 봉쇄 옵션 정책 유지 |
| temperature=0 강제 | 비채택 — runtime 책임. main 모델 호출 외부 통제 불가 |
| trace 옵션 (`--trace`) 동시 도입 | 비채택 — 후속 PRD 후보 |
| snapshot diff 자동 비교 | 비채택 — regression test suite 후속 PRD |
| max-depth cap = 2 | 비채택 — 관측 최대 = 3. cap = 3이 안전 마진 |
| max-depth cap = ∞ | 비채택 — 동일 입력 깊이 일관성 확보 위해 cap 필요 |
| marker 신설 (`[TBD-AMBIG]`·`[TBD-CONFLICT]`) | 비채택 — marker 1종 정책 유지. 카테고리만 분리 |
| 자체 검증 패스 8 카테고리로 분리 | 비채택 — 6 카테고리 그대로. 패스 횟수만 증가 |
| 라벨 매핑 양 매핑 금지 | 비채택 — 권한·연동 자연스러운 양 매핑 영역 |

## 15. 마이그레이션

0.2.4 → 0.2.5 호출 스크립트·옵션·출력 형식 모두 호환. 변경된 행위:

1. `Run 3` 같은 fetch 미시도가 사라짐 — 모든 발견 URL이 출처 list에 등장.
2. dequeue 순서가 BFS + 발견 순서로 결정 — 출처 list `#` 번호 비결정성 해소.
3. 인증 미연결 connector도 1차 WebFetch 결과를 status로 기록.
4. 분해 깊이 4 산출물 → cap 폴백.
5. 카테고리 분류 → 결정 트리 결과.
6. 모호성 표현 → 자동 [TBD] 단정.
7. 자체 검증 → 6패스 체크리스트, 발견 건수 증가 가능.
8. 라벨 매핑 모호 케이스 → 결정 트리 + 분배 룰.

기존 산출물 재실행 시 출처 list 항목 수가 늘어날 수 있음 (이전 미시도 URL이 행으로 기록됨).

## 16. 영향 범위

- `skills/planning-format/SKILL.md` — Step 3 fetch 시도 의무 + BFS 명시. Step 6 진입 직전 결정 트리·모호성 룰·max-depth cap 적재. Step 7 진입 직전 6 카테고리 체크리스트 적재. 참고 파일 섹션 0.2.5 표기 추가.
- `skills/planning-format/references/connector-routing.md` — §5 케이스 표 진입 조건 통일 표기.
- `skills/planning-format/references/exclusion-rules.md` — `fetch 실패` 카테고리 정의에 "시도 후 실패만" 명시. §2 결정 트리 + 신규 §3.1 모호성 트리거 + §3.2 16 어구.
- `skills/planning-format/references/conversion-rules.md` — §4 라벨 매핑 결정 트리 + §5.4 max-depth cap.
- `skills/planning-format/references/self-review-rules.md` — F1~F6 각 카테고리 체크리스트 추가.
- `.claude-plugin/plugin.json` / `.codex-plugin/plugin.json` — version `0.2.4` → `0.2.5` + description·shortDescription 0.2.5 표기.
- `README.md` — 헤더 0.2.5 + 비교표 0.2.5 + reference list 0.2.5 표기.
- `docs/prd/README.md` — 9건 chain + 0.2.5 row.
- `docs/planning-format-workflow.md` — Step 3 fetch 시도·BFS·1차 WebFetch 의무 + 라벨 매핑 결정 트리 9 분기 + max-depth cap=3 + 카테고리 결정 트리 + 모호성 강제 [TBD] + F1~F6 체크리스트 mermaid.

## 17. 용어

- **fetch 시도 의무**: queue dequeue된 visited 미포함 URL은 1차 WebFetch + 인증된 connector fallback을 모두 1회 이상 시도해야 한다는 룰. 미시도 허용은 `--no-fetch` 단 1케이스.
- **BFS 강제**: depth N 모두 dequeue 후 depth N+1 dequeue. 같은 depth 안에선 본문 발견 순서.
- **결정 트리**: if-elif-else chain으로 분류 룰 명시. main 자유 판단 영역을 syntactic feature 진입 조건으로 룰화.
- **모호성 트리거**: 원문 syntactic 결함을 자동 [TBD]·`원문 정의 부재` 카테고리로 처리하는 정규식·키워드 패턴.
- **max-depth cap**: list 분해 다층 sub-§ 깊이 상한. 0.2.5 = 3.
- **체크리스트화**: 자체 검증 카테고리별 yes/no 항목 list. 단일 LLM 패스 → 6패스로 검출 누락 차단.
- **양 매핑 분배 룰**: 한 entity가 정책서·기능설계서 양쪽 등장 가능한 영역(권한·연동·상태)의 측면별 위치 분배표.

그 외 용어는 0.2.4 §13 / 0.2.3 §15 / 0.2.2 §14 그대로.

## 18. 참고 파일

- `skills/planning-format/SKILL.md` — Step 3 갱신 + Step 6 결정 트리·모호성 룰·max-depth cap 적재 + Step 7 체크리스트 적재 + 참고 파일 섹션 0.2.5 표기.
- `skills/planning-format/references/connector-routing.md` — §5 진입 조건 표기.
- `skills/planning-format/references/exclusion-rules.md` — `fetch 실패` 카테고리 정의 + §2 결정 트리 + §3.1·§3.2 신규.
- `skills/planning-format/references/conversion-rules.md` — §4 결정 트리 + §5.4 cap.
- `skills/planning-format/references/self-review-rules.md` — F1~F6 체크리스트.
- `.claude-plugin/plugin.json` / `.codex-plugin/plugin.json` — version 0.2.5 + description 0.2.5 표기.
- `README.md` — 헤더·비교표·reference list 0.2.5 표기.
- `docs/prd/README.md` — 0.2.5 row.
- `docs/planning-format-workflow.md` — Step 3·라벨 매핑·체크리스트·결정 트리·모호성 mermaid 갱신.
- `docs/prd/prd-0.2.5.md` — 본 문서.
