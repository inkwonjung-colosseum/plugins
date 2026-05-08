# planning-review workflow

`/planning-kit:planning-review` 한 호출의 전체 흐름을 다이어그램으로 정리한 문서. 동작 명세는 `skills/planning-review/SKILL.md`, lookup data는 `skills/planning-review/references/ssot-rules.md`·`ac-rules.md`·`deps-rules.md`에 있다.

본 스킬은 외부 검증만 수행. 변환·자체 품질 점검은 `planning-format`이 책임 — 자세한 변환 흐름은 `docs/planning-format-workflow.md`.

## 1. 전체 시퀀스

```mermaid
flowchart TD
  A[인자 입력] --> B{Step 1: 입력 dispatch}
  B -->|0개| BC[conversation 참조 모드]
  B -->|"1개 (디렉터리)"| B1[정책서*.md + 기능설계서*.md 자동 검색]
  B -->|"1개 (파일)"| B2[헤더로 두 섹션 자동 분리]
  B -->|"1개 (raw markdown)"| B3[헤더로 두 본문 자동 분리]
  B -->|"2개 (path)"| B4[정책서·기능설계서 식별]
  B -->|3개+| BX["sanity check<br/>'추가 인자는 받지 않습니다'"]

  BC --> C{본문 식별 성공?}
  B1 --> C
  B2 --> C
  B3 --> C
  B4 --> C
  C -->|아니오| CX[sanity check<br/>한 줄 메시지 + 종료]
  C -->|예| D[Step 2: 검증 축 점검]

  D --> R1{R1 ssot 활성?}
  D --> R2{R2 ac 활성?}
  D --> R3{R3 deps 활성?}

  R1 -->|예| RR1[references/ssot-rules.md<br/>키워드 추출 → grep 매칭 → Read 비교]
  R2 -->|예| RR2[references/ac-rules.md<br/>4 sub-category 점검]
  R3 -->|예| RR3[references/deps-rules.md<br/>4 sub-category 추론]

  RR1 --> M[Step 3: 발견 합산<br/>중복 제거 R1 > R3 > R2]
  RR2 --> M
  RR3 --> M

  M --> N{Step 4: 결과}
  N -->|모두 0건| PASS[리뷰 결과: 통과]
  N -->|≥1건| FOUND[리뷰 결과: 발견 N건]

  PASS --> OUT[Step 5: 단일 응답 markdown 출력]
  FOUND --> OUT
```

## 2. 입력 dispatch (Step 1)

```mermaid
flowchart LR
  IN[인자 토큰] --> N{토큰 수}
  N -->|0| CV[conversation 참조 모드]
  N -->|1| ONE{path? markdown?}
  N -->|2| TWO[두 path<br/>헤더로 정책/기능 식별]
  N -->|3+| FAIL[sanity check]

  ONE -->|디렉터리| DIR[정책서*.md + 기능설계서*.md<br/>자동 검색]
  ONE -->|파일| FILE[본문 안 두 섹션<br/>자동 분리]
  ONE -->|텍스트| TXT[raw markdown<br/>두 본문 자동 분리]

  CV --> CHK[직전 turn에서<br/>planning-format 출력 추출]
  CHK --> EX{식별 성공?}
  DIR --> EX
  FILE --> EX
  TXT --> EX
  TWO --> EX
  EX -->|예| OK[검증 진행]
  EX -->|아니오| SK[sanity check 한 줄]
```

## 3. 본문 분리 패턴

```mermaid
flowchart TD
  IN[입력 markdown] --> P1{"헤더 '# 정책서'<br/>또는 '## 정책서'?"}
  P1 -->|예| Q1[정책서 섹션 추출]
  P1 -->|아니오| P2{"코드 펜스<br/>markdown 펜스 블록?"}
  P2 -->|예| Q2[펜스 안 첫 헤더로 식별]
  P2 -->|아니오| FAIL[식별 실패<br/>sanity check]

  Q1 --> P3{"헤더 '# 기능설계서'<br/>또는 '## 기능설계서'?"}
  Q2 --> P3
  P3 -->|예| OK[두 본문 확보 → 검증 진행]
  P3 -->|아니오| EMPTY[한쪽 본문 없음<br/>sanity check]
```

## 4. 검증 축 (Step 2)

```mermaid
flowchart LR
  T[--axes list] --> R1[R1. SSOT 충돌]
  T --> R2[R2. Acceptance Criteria 검증가능성]
  T --> R3[R3. 의존·영향 분석]

  R1 --> R1A[키워드 추출<br/>기능명·도메인·역할·상태·권한]
  R1A --> R1B[프로젝트 *.md grep<br/>--ssot-include 적용]
  R1B --> R1C[매칭 file Read 비교]
  R1C --> R1D{충돌?}
  R1D -->|예| R1E[발견 list]
  R1D -->|아니오| R1F[검증 대상 없음 또는 통과]

  R2 --> R2A[정책서 §5·§6 +<br/>기능설계서 §5·§7<br/>확정 문장 점검]
  R2A --> R2B{4 sub-category}
  R2B -->|정량성| R2X[비정량 부사 + 임계값 부재]
  R2B -->|상태| R2Y[전이 시작·종료·트리거 부재]
  R2B -->|행위자| R2Z[주어 부재]
  R2B -->|결과 관찰| R2W[검증 신호 부재]

  R3 --> R3A[corpus 매칭<br/>R1 키워드 + 상태·권한 grep]
  R3A --> R3B[영향 후보 file 산출]
  R3B --> R3C{단정 충돌?}
  R3C -->|예| R3D[발견]
  R3C -->|아니오| R3E[권고]
```

## 5. 발견 합산 (Step 3)

```mermaid
flowchart TD
  ALL[R1·R2·R3 발견 list] --> DUP{같은 발견<br/>여러 축에 걸침?}
  DUP -->|예| PR{우선순위}
  DUP -->|아니오| KEEP[모두 유지]

  PR -->|R1 > R3 > R2| KEEP1[보수적인 쪽으로 1회만 기록]
  KEEP --> SUM[발견 합계 산출]
  KEEP1 --> SUM
  SUM --> RES{발견 ≥ 1?}
  RES -->|아니오| PASS[통과]
  RES -->|예| FND[발견 N건]
```

## 6. 단일 응답 출력 (Step 5)

```mermaid
flowchart LR
  H[# planning-review: 기능명<br/>입력 / 점검 축 / SSOT corpus / SSOT 검색 키워드]
  H --> RR[## 리뷰 결과<br/>통과 또는 발견 N건<br/>축별 카운트]
  RR --> S1{R1 활성<br/>+ 발견 ≥1?}
  S1 -->|예| SS1[### SSOT 충돌 list]
  S1 -->|아니오| S2
  SS1 --> S2{R2 활성<br/>+ 발견 ≥1?}
  S2 -->|예| SS2[### 검증가능성 list]
  S2 -->|아니오| S3
  SS2 --> S3{R3 활성<br/>+ 발견 ≥1?}
  S3 -->|예| SS3[### 영향 분석 list]
  S3 -->|아니오| FIN[출력 종료]
  SS3 --> FIN
```

규칙:
- 활성 안 한 축의 sub-section은 통째 생략.
- `SSOT 검색 키워드` 줄은 R1 활성 시에만.
- `SSOT corpus` 카운트 줄은 R1 또는 R3 활성 시에만 (corpus 공유).

## 7. R1 vs R3 차이

```mermaid
flowchart LR
  D[변환 본문 확정 문장 + SSOT corpus] --> Q{어긋남 종류}
  Q -->|같은 대상의 표기·결정·임계값 어긋남| R1[R1. SSOT 충돌]
  Q -->|이 변경이 들어가면<br/>다른 SSOT도 같이 손봐야| R3[R3. 의존·영향]

  R1 --> EX1["예: 정책서 '관리자는 30일 보관' vs SSOT '60일 보관'"]
  R3 --> EX2[예: 정책서 §6 상태 전이 추가<br/>→ status-machine.md 보강 필요]
```

R1·R3 모두 SSOT corpus를 보지만 관점이 다르다. 같은 발견이 양쪽에 걸리면 R1로 1회만 기록 (R1이 더 단정적).

## 8. 옵션 영향

```mermaid
flowchart TD
  OPT[옵션] --> O1[--ssot-include glob]
  OPT --> O2[--axes list]

  O1 --> E1[R1·R3 corpus 범위 좁힘]
  O2 --> E2A[--axes ssot<br/>R1만 점검]
  O2 --> E2B[--axes ac<br/>R2만 점검]
  O2 --> E2C[--axes deps<br/>R3만 점검]
  O2 --> E2D[--axes ssot,ac<br/>R3 skip]
  O2 --> E2E[--axes 빈 값<br/>sanity check]
```

## 9. 참고 파일

| 파일 | 역할 |
|---|---|
| `skills/planning-review/SKILL.md` | 동작 시퀀스 골격 (Step 1~5) |
| `skills/planning-review/references/ssot-rules.md` | R1 SSOT 충돌 점검 절차·매칭·발견 형식 |
| `skills/planning-review/references/ac-rules.md` | R2 Acceptance Criteria 4 sub-category 기준 |
| `skills/planning-review/references/deps-rules.md` | R3 의존·영향 4 sub-category 기준 + 발견·권고 분류 |
| `docs/planning-format-workflow.md` | planning-format 변환·자체 검증 워크플로 |
| `docs/prd/prd-0.2.0.md` | 본 스킬 분할 + Google 라우팅 fix PRD |
