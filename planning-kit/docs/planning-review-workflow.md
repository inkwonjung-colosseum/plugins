# planning-review workflow

`/planning-kit:planning-review` 한 호출의 전체 흐름을 다이어그램으로 정리한 문서. 동작 명세는 `skills/planning-review/SKILL.md`, lookup data는 `skills/planning-review/references/ssot-rules.md`·`ac-rules.md`·`deps-rules.md`와 `skills/planning-format/references/connector-routing.md`·`conversion-rules.md`에 있다.

본 스킬은 외부 검증만 수행. 변환·자체 품질 점검은 `planning-format`이 책임 — 자세한 변환 흐름은 `docs/planning-format-workflow.md`.

## 1. 전체 시퀀스

```mermaid
flowchart TD
  A[인자 입력] --> B{Step 1: 입력 dispatch}
  B -->|0개| BC[conversation 참조 모드]
  B -->|"1개+ URL"| BU[URL root 입력<br/>다중 URL 허용]
  B -->|"1개 (디렉터리)"| B1[정책서*.md + 기능설계서*.md 자동 검색]
  B -->|"1개 (파일)"| B2[파일 본문 + same-folder companion read<br/>또는 이미지 시드]
  B -->|"1개 (raw markdown)"| B3[헤더로 두 본문 + 입력 제외 § 자동 분리]
  B -->|"2개 (path)"| B4[정책서·기능설계서 식별]
  B -->|"그 외"| B5[raw markdown 텍스트 분기<br/>URL 혼합 입력 포함]

  BC --> IC[Step 1.2 input collection<br/>URL 추출·재귀 fetch·connector fallback·이미지 multimodal<br/>입력 visited set 별도]
  BU --> IC
  B1 --> IC
  B2 --> IC
  B3 --> IC
  B4 --> IC
  B5 --> IC
  IC --> C{본문 식별 성공?}
  C -->|아니오| CX[sanity check<br/>한 줄 메시지 + 종료]
  C -->|예| D[Step 2: 검증 축 점검]

  D --> R1{R1 ssot 활성?}
  D --> R2{R2 ac 활성?}
  D --> R3{R3 deps 활성?}

  R1 -->|예| RR1[references/ssot-rules.md<br/>키워드 추출 → grep 매칭 → Read 비교<br/>+ R1 link follow 0.2.2]
  R2 -->|예| RR2[references/ac-rules.md<br/>4 sub-category 점검]
  R3 -->|예| RR3[references/deps-rules.md<br/>4 sub-category 추론<br/>+ 입력 제외 § 보조 신호 0.2.2]

  RR1 --> M[Step 3: 발견 합산<br/>중복 제거 R1 > R3 > R2]
  RR2 --> M
  RR3 --> M

  M --> N{Step 4: 결과}
  N -->|모두 0건| PASS[리뷰 결과: 통과]
  N -->|≥1건| FOUND[리뷰 결과: 발견 N건]

  PASS --> OUT[Step 5: 단일 응답 markdown 출력<br/>+ ## 입력 출처 0.2.6<br/>+ ## SSOT 출처 0.2.2]
  FOUND --> OUT
```

## 2. 입력 dispatch (Step 1)

```mermaid
flowchart LR
  IN[인자 토큰] --> N{토큰 수}
  N -->|0| CV[conversation 참조 모드]
  N -->|1+ 모두 https?://| URL[URL 분기<br/>모든 URL depth 0 root]
  N -->|1| ONE{path? markdown?}
  N -->|2| TWO[두 path<br/>헤더로 정책/기능 식별]
  N -->|그 외| TXT2[raw markdown 텍스트<br/>URL 혼합 입력 포함]

  ONE -->|디렉터리| DIR[정책서*.md + 기능설계서*.md<br/>자동 검색]
  ONE -->|파일| FILE[same-folder companion read<br/>sibling 파일 non-recursive 수집<br/>이미지 파일이면 image queue]
  ONE -->|텍스트| TXT[raw markdown<br/>두 본문 자동 분리]

  CV --> CHK[직전 turn에서<br/>planning-format 출력 추출]
  CHK --> IC[공통 input collection<br/>본문 URL·이미지 추출]
  URL --> IC
  DIR --> IC
  FILE --> IC
  TXT --> IC
  TWO --> IC
  TXT2 --> IC
  IC --> EX{식별 성공?}
  EX -->|예| EXC[입력 제외 § 분리 시도<br/>0.2.2 / 부재해도 sanity check 아님]
  EXC --> OK[검증 진행]
  EX -->|아니오| SK[sanity check 한 줄]
```

공통 input collection(0.2.6):

- URL root와 본문 URL은 `planning-format` Step 1~5처럼 BFS 재귀 fetch한다. 1차 WebFetch는 필수이며 connector fallback은 `connector-routing.md`를 공유 적재한다.
- input visited set은 SSOT corpus link follow visited set과 분리한다.
- `--no-input-fetch`는 input collection URL fetch만 봉쇄한다. URL-only 입력이면 본문 식별 불가 sanity check로 종료한다.
- input image queue는 이미지 파일 인자, 디렉터리 이미지, markdown image/HTML img, fetch `image/*`, data URI 5경로를 쓴다. `--no-input-image`는 이 multimodal 처리만 봉쇄한다.

단일 파일 companion read(0.2.7):

- 입력 파일의 parent directory를 scan 범위로 잡고, 하위 폴더는 읽지 않는다.
- 같은 폴더의 읽을 수 있는 UTF-8 텍스트 파일과 지원 이미지 파일을 input collection에 추가한다.
- 숨김 파일, binary, dependency/build/cache 성격 파일은 읽지 않는다.
- source title/path/H1/본문 헤더와 입력 파일의 기능명/stem/domain 유사도로 정책서·기능설계서 후보를 좁힌다.
- 후보가 1쌍이면 리뷰하고, 여러 기능이 섞여 1쌍으로 확정할 수 없으면 sanity check로 종료한다.

## 3. 본문 분리 패턴

```mermaid
flowchart TD
  IN[통합 입력 본문] --> P1{"헤더 '# 정책서'<br/>또는 '## 정책서'?"}
  P1 -->|예| Q1[정책서 섹션 추출]
  P1 -->|아니오| P2{"코드 펜스<br/>markdown 펜스 블록?"}
  P2 -->|예| Q2[펜스 안 헤더로 식별]
  P2 -->|아니오| P4{"source title/path/URL label<br/>정책서·policy·feature·design·spec 등<br/>명확한 1:1 신호?"}
  P4 -->|예| Q4[source 단위 fallback 배정]
  P4 -->|아니오| P5{"companion read<br/>입력 파일 stem/domain 기준<br/>1쌍 확정?"}
  P5 -->|예| Q5[sibling source fallback 배정]
  P5 -->|아니오| FAIL[식별 실패<br/>sanity check]

  Q1 --> P3{"헤더 '# 기능설계서'<br/>또는 '## 기능설계서'?"}
  Q2 --> P3
  Q4 --> P3
  Q5 --> P3
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
  R1B --> R1L{매칭 ≥1<br/>+ R1 또는 R3 활성<br/>+ --no-ssot-fetch off?}
  R1L -->|예 0.2.2| R1LF[link follow<br/>매칭 *.md 본문 안 URL 추출<br/>→ fetch + connector fallback<br/>→ corpus body 합류<br/>cap 없음]
  R1L -->|아니오| R1C
  R1LF --> R1C[매칭 file + 외부 fetch 본문 Read 비교]
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
  R3A --> R3X[입력 제외 § 보조 신호 0.2.2<br/>fetch 실패 / 범위 외 / 구조 변환 / 디테일 축약]
  R3X --> R3B[영향 후보 file 산출]
  R3B --> R3C{단정 충돌?}
  R3C -->|예| R3D[발견]
  R3C -->|아니오| R3E[권고<br/>입력 제외 § 보조 신호 default 권고]
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
  H[# planning-review: 기능명<br/>입력 / 입력 처리 0.2.6 / 입력 제외 § 0.2.2 / 점검 축 / SSOT corpus / SSOT 검색 키워드]
  H --> RR[## 리뷰 결과<br/>통과 또는 발견 N건<br/>축별 카운트]
  RR --> IO{input fetch/image<br/>1건 이상?}
  IO -->|예 0.2.6| IOO[## 입력 출처<br/>root URL + 입력 자식 URL/이미지 표]
  IO -->|아니오| SO
  IOO --> SO{SSOT link follow<br/>1건 이상?}
  SO -->|예 0.2.2| SOO[## SSOT 출처<br/>매칭 *.md + 자식 URL/이미지 표]
  SO -->|아니오| S1
  SOO --> S1{R1 활성<br/>+ 발견 ≥1?}
  S1 -->|예| SS1[### SSOT 충돌 list]
  S1 -->|아니오| S2
  SS1 --> S2{R2 활성<br/>+ 발견 ≥1?}
  S2 -->|예| SS2[### 검증가능성 list]
  S2 -->|아니오| S3
  SS2 --> S3{R3 활성<br/>+ 발견 ≥1?}
  S3 -->|예| SS3[### 영향 분석 list<br/>입력 제외 § cross-ref 가능]
  S3 -->|아니오| FIN[출력 종료]
  SS3 --> FIN
```

규칙:
- 활성 안 한 축의 sub-section은 통째 생략.
- `입력 처리` 줄은 conversation 본문 사용, local/raw 본문 사용, 또는 URL root/fetch/image 카운트 중 하나로 표기.
- `SSOT 검색 키워드` 줄은 R1 활성 시에만.
- `SSOT corpus` 카운트 줄은 R1 또는 R3 활성 시에만 (corpus 공유). link follow 1건 이상이면 `매칭 N개 + 외부 fetch 성공 K개 / 실패 J개 (총 시도 K+J건, cap 없음)`.
- `입력 제외 §` 줄은 분리 성공 시 항상 (R3 활성 무관). R3 신호 K건 표기.
- `## 입력 출처` 블록은 input fetch 또는 input image 1건 이상일 때만, `## 리뷰 결과` 다음에 출력.
- `## SSOT 출처` 블록은 link follow 1건 이상 시도 시에만 (R1 또는 R3 트리거).

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
  OPT --> O3["--no-input-fetch 0.2.6"]
  OPT --> O4["--no-input-image 0.2.6"]
  OPT --> O5["--no-ssot-fetch 0.2.2"]
  OPT --> O6["--no-ssot-image 0.2.2"]

  O1 --> E1[R1·R3 corpus 범위 좁힘]
  O2 --> E2A[--axes ssot<br/>R1만 점검]
  O2 --> E2B[--axes ac<br/>R2만 점검<br/>link follow 진입 안 함]
  O2 --> E2C[--axes deps<br/>R3만 점검<br/>link follow 진입]
  O2 --> E2D[--axes ssot,ac<br/>R3 skip]
  O2 --> E2E[--axes 빈 값<br/>sanity check]
  O3 --> E3[input URL fetch 봉쇄<br/>URL-only 입력은 sanity check]
  O4 --> E4[input image multimodal 봉쇄<br/>URL fetch는 그대로]
  O5 --> E5[SSOT link follow 봉쇄<br/>매칭 *.md 본문만 corpus<br/>0.2.1 동등]
  O6 --> E6[SSOT image multimodal 봉쇄<br/>SSOT URL fetch는 그대로]
```

## 9. 참고 파일

| 파일 | 역할 |
|---|---|
| `skills/planning-review/SKILL.md` | 동작 시퀀스 골격 (Step 1~5) |
| `skills/planning-review/references/ssot-rules.md` | R1 SSOT 충돌 점검 절차·매칭·발견 형식 + link follow (0.2.2) + input/SSOT fetch 경계 (0.2.6) |
| `skills/planning-review/references/ac-rules.md` | R2 Acceptance Criteria 4 sub-category 기준 |
| `skills/planning-review/references/deps-rules.md` | R3 의존·영향 4 sub-category 기준 + 발견·권고 분류 + 입력 제외 § 보조 신호 (0.2.2) |
| `skills/planning-format/references/connector-routing.md` | input fetch와 SSOT link follow 공유 적재 — 인증 휴리스틱·MCP 카탈로그·Google Workspace tool 시퀀스·fallback 케이스 |
| `skills/planning-format/references/conversion-rules.md` | input image multimodal·통합 본문 합류 룰 공유 참조 |
| `docs/planning-format-workflow.md` | planning-format 변환·자체 검증 워크플로 |
| `docs/prd/prd-0.2.0.md` | 본 스킬 분할 + Google 라우팅 fix PRD |
| `docs/prd/prd-0.2.2.md` | R1 link follow + 입력 제외 § R3 보조 신호 PRD |
| `docs/prd/prd-0.2.6.md` | planning-review 다중 URL input collection parity PRD |
| `docs/prd/prd-0.2.7.md` | planning-review 단일 파일 companion read + ssot-audit PRD |
