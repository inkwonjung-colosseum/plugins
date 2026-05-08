# formalize workflow

`/planning-kit:formalize` 한 호출의 전체 흐름을 다이어그램으로 정리한 문서. 동작 명세는 `skills/formalize/SKILL.md`, lookup data는 `skills/formalize/references/connector-routing.md`·`references/review-rules.md`에 있다 — 본 문서는 그 흐름을 시각화해 사용자·개발자가 한 화면에서 파악할 수 있게 한다.

## 1. 전체 시퀀스

```mermaid
flowchart TD
  A[인자 입력] --> B{Step 1: 분기 판별}
  B -->|모든 토큰 https?://| C[URL 분기]
  B -->|디렉터리 경로| D[디렉터리 분기]
  B -->|파일 경로| E[파일 분기]
  B -->|그 외| F[텍스트 분기]

  C --> G[본문 URL·이미지 추출<br/>모든 분기 공통]
  D --> G
  E --> G
  F --> G

  G --> H{Step 2: 빈 입력?}
  H -->|본문 0byte<br/>+ 이미지 0건<br/>+ URL 0건| H1["입력 비어 있음. ...<br/>한 줄 출력 후 종료"]
  H -->|아님| I[Step 3: 재귀 fetch + connector fallback]

  I --> J[Step 4: 이미지 multimodal 처리]
  J --> K[Step 5: 통합 본문 합류]
  K --> L[Step 6: 변환 + 자동 리뷰]
  L --> M[Step 7: 단일 응답 markdown 출력]
```

## 2. 입력 dispatch (Step 1)

```mermaid
flowchart LR
  IN[인자 토큰] --> T{모든 토큰<br/>^https?://}
  T -->|예 (1개)| URL1[단일 URL 분기]
  T -->|예 (2개+)| URLM[다중 URL 분기]
  T -->|아니오| P{경로?}
  P -->|디렉터리| DIR[디렉터리 분기<br/>UTF-8 텍스트 + 이미지 시드]
  P -->|파일 (이미지 확장자)| IMG[이미지 단독 시드]
  P -->|파일 (텍스트)| FILE[파일 분기]
  P -->|경로 아님| TXT[텍스트 분기]

  URL1 --> EXT[본문 URL·이미지 추출<br/>fetch queue + image queue 시드]
  URLM --> EXT
  DIR --> EXT
  IMG --> EXT
  FILE --> EXT
  TXT --> EXT
```

추출 패턴: markdown link / autolink / HTML href·src·img / plain URL / markdown image / data URI. 제외: self-anchor·`mailto:`/`tel:`/`javascript:`/`blob:`. `--no-fetch`/`--no-image`면 해당 시드 skip.

## 3. fetch 시퀀스 (Step 3)

URL 1개 처리 단위. WebFetch 1차 + connector fallback 2단 구조.

```mermaid
flowchart TD
  S[fetch 진입] --> CAT[references/connector-routing.md Read<br/>호출당 1회]
  CAT --> WF[WebFetch GET<br/>timeout 30초, redirect ≤5]
  WF --> CLS{응답 분류}

  CLS -->|200 OK + html/md/plain/xhtml| OK1[본문 추출 합류<br/>via=WebFetch]
  CLS -->|200 OK + image/*| OK2[image queue<br/>via=WebFetch]
  CLS -->|지원 안 하는 ct<br/>or 401/403<br/>or 인증 게이트 휴리스틱<br/>or 4xx/5xx<br/>or timeout/network error| FB[fallback 평가]

  FB --> M{매핑표 lookup<br/>원래 입력 호스트}
  M -->|적중| C1[connector 후보 산출]
  M -->|미적중| RT{런타임 추론}
  RT -->|tool 단서 일치| C1
  RT -->|매칭 없음| SK1[skip<br/>사유: 인증 필요<br/>connector 매핑 없음]

  C1 --> TRY[후보 순서대로 호출<br/>timeout 30초, 1회씩]
  TRY --> R{결과}
  R -->|1건 이상 성공| OK3[응답 텍스트 합류<br/>via=connector]
  R -->|모두 실패<br/>+ 1차 200 OK 정상| OK4[1차 본문 사용<br/>via=WebFetch]
  R -->|모두 실패<br/>+ 1차 인증 게이트| SK2[skip<br/>사유: 인증 필요<br/>connector 미인증]
  R -->|모두 실패<br/>+ 1차 4xx/5xx/timeout| SK3[skip<br/>사유: 1차 status·error]

  OK1 --> CHILD[자식 URL 추출<br/>visited queue push]
  OK3 --> CHILD
  OK4 --> CHILD
  CHILD --> NEXT[다음 round]
```

**핵심 포인트:**
- `references/connector-routing.md`는 fetch 진입 직전 1회 적재 (호스트 매핑표·인증 휴리스틱·fallback 케이스 표·sanity check 메시지·status 표기 모두 거기).
- 매핑 lookup 호스트는 **원래 입력된 URL의 호스트** (redirect 최종 호스트 X).
- connector 응답 본문도 자식 URL 추출 → "Confluence root → Figma 자식 → 본문 합류" 자동 동작.
- `--no-fetch`면 1차·fallback 모두 봉쇄.

## 4. 호스트 매핑표 (요약)

```mermaid
flowchart LR
  H[대상 URL 호스트] --> M{매핑 lookup}
  M -->|*.atlassian.net /wiki| A1[Atlassian MCP<br/>getConfluencePage]
  M -->|*.atlassian.net /browse| A2[Atlassian MCP<br/>getJiraIssue]
  M -->|figma.com| F1[Figma MCP<br/>get_design_context / get_figjam]
  M -->|docs/drive/sheets/slides<br/>.google.com| G1[Google Drive connector]
  M -->|*.slack.com /archives| S1[Slack MCP<br/>slack_read_thread / slack_read_channel]
  M -->|*.slack.com 그 외| S2[Slack MCP<br/>slack_read_canvas / slack_search ...]
  M -->|notion.so / *.notion.site| N1[Notion connector]
  M -->|매핑 외| RT[런타임 추론<br/>Linear / Intercom / Canva / Box / ...]
```

전체 매핑 detail은 `skills/formalize/references/connector-routing.md` §3.

## 5. URL 분기 sanity check (Step 3.4)

루트 URL이 **모두** 본문 합류 실패하면 호출 종료. 일부 root만 실패면 출처 list에 사유 기록 후 진행.

```mermaid
flowchart TD
  R[루트 URL 결과 종합] --> AS{모든 root 실패?}
  AS -->|일부만 실패| C[진행<br/>출처 list에 사유 기록]
  AS -->|모두 실패| W{사유 분류}

  W -->|http/https 외 scheme| W1[http(s) URL만 지원합니다.]
  W -->|모두 fetch 실패 4xx/5xx/timeout| W2[모든 URL fetch 실패. 첫 사유: ...]
  W -->|모두 인증 게이트<br/>+ connector 미인증/실패| W3[모든 URL이 로그인 필요.<br/>connector/MCP fallback도 미인증.<br/>필요한 connector: ...]
  W -->|모두 지원 안 하는 ct| W4[모든 URL이 지원 안 하는 content-type: ...]
  W -->|통합 본문 0byte| W5[통합 본문이 비어 있습니다.]

  W1 --> END[리뷰 블록 없이<br/>한 줄 + URL list 출력 후 종료]
  W2 --> END
  W3 --> END
  W4 --> END
  W5 --> END
```

## 6. 이미지 multimodal (Step 4)

```mermaid
flowchart TD
  Q[image queue] --> S[5경로 시드<br/>인자 / 디렉터리 / 본문 추출 / fetch image / data URI]
  S --> X{지원 확장자<br/>.png .jpg .gif .webp .bmp .heic .svg}
  X -->|예| MM[main이 자기 자신에 multimodal 해석 요청]
  X -->|아니오| F1[skip<br/>사유: 미지원 이미지 포맷]

  MM --> R{해석 결과}
  R -->|텍스트| MERGE["=== [출처 N] 이미지: ... === 헤더로 본문 합류"]
  R -->|빈 응답| F2[skip<br/>사유: 빈 해석 결과]
  R -->|read 실패| F3[skip<br/>사유: image read 실패]

  MERGE --> SS[SSOT 키워드 grep 대상에 포함<br/>단 키워드 list에 image 출처는 별도 표시 안 함]
```

`--no-image`면 §4 전체 skip. 이미지 실패는 호출 종료 사유 아님.

## 7. 변환 + 리뷰 (Step 6)

```mermaid
flowchart TD
  CB[통합 본문] --> NA[기능명 추출<br/>1순위 1개만]
  NA --> RD[templates/기능설계서.md + 정책서.md 병렬 Read]
  RD --> WR[main이 같은 턴에서<br/>두 본문 직접 작성<br/>저장 안 함]

  WR --> NORV{--no-review?}
  NORV -->|예| OUT[변환 본문만 출력]
  NORV -->|아니오| RV[references/review-rules.md Read]

  RV --> A[A. 자체 품질 점검<br/>충실도 / cross-bleed / 용어 / 매핑 / 누락]
  RV --> B[B. SSOT 충돌 점검<br/>키워드 grep → 매칭 파일 Read → 비교]

  A --> RES{발견}
  B --> RES
  RES -->|A 0건 + B 0건| PASS[리뷰 결과: 통과]
  RES -->|≥1건| FOUND[리뷰 결과: 발견 N건<br/>카테고리별 list]

  PASS --> OUT
  FOUND --> OUT
```

라벨 매핑:
- 화면·흐름·동작·입력 항목·권한·예외 메시지 → 기능설계서.
- 규칙·조건·예외 승인·역할 책임·상태 전이·연동 정책 → 정책서.

라벨 매핑 안 되는 조각·중복·근거 부족 조각은 입력 제외 추적으로. 근거 부족 셀은 inline `[TBD]`. marker `[TBD]` 1종만.

## 8. 단일 응답 출력 구조 (Step 7)

```mermaid
flowchart LR
  H[# 기능명<br/>입력 처리 / 출처 / 미결 / 입력 제외 카운트]
  H --> P[## 정책서<br/>10 섹션]
  P --> F[## 기능설계서<br/>8 섹션]
  F --> SR{URL fetch +<br/>이미지 처리<br/>≥ 1건?}
  SR -->|예| ST[## 출처 표]
  SR -->|아니오| EX
  ST --> EX{입력 제외 ≥ 1건?}
  EX -->|예| EXB[## 입력 제외 항목]
  EX -->|아니오| RV
  EXB --> RV
  RV{--no-review?}
  RV -->|아니오| RVB[## 리뷰 결과<br/>SSOT 검색 키워드 노출]
  RV -->|예| END[종료]
  RVB --> END
```

블록 순서: **변환 본문 → 출처 → 입력 제외 → 리뷰 결과**. 빈 블록은 통째 생략.

## 9. 출처 list status 분류

```mermaid
flowchart TD
  ST[상태 컬럼] --> S{종류}
  S -->|성공| OK
  S -->|실패| FAIL

  OK --> OK1[200 via WebFetch]
  OK --> OK2[200 via Atlassian MCP]
  OK --> OK3[200 via Figma MCP]
  OK --> OK4[200 via Google Drive connector]
  OK --> OK5[200 via Slack MCP]
  OK --> OK6[200 via Notion connector]
  OK --> OK7[image/png 1.2MB via Figma MCP]

  FAIL --> F1[인증 필요<br/>connector 미인증]
  FAIL --> F2[인증 필요<br/>connector 매핑 없음]
  FAIL --> F3[content-type video/mp4]
  FAIL --> F4[빈 본문 / 빈 해석 결과]
  FAIL --> F5[미지원 이미지 포맷 / image read 실패]
  FAIL --> F6[timeout / network error]
```

표 detail은 `references/connector-routing.md` §7.

## 10. 옵션 영향

```mermaid
flowchart TD
  OPT[옵션] --> O1[--ssot-include glob]
  OPT --> O2[--no-review]
  OPT --> O3[--no-fetch]
  OPT --> O4[--no-image]

  O1 --> E1[Step 6 SSOT corpus 범위 좁힘]
  O2 --> E2[Step 6 리뷰 단계 skip<br/>리뷰 결과 블록 통째 생략]
  O3 --> E3[Step 3 전체 봉쇄<br/>1차 WebFetch + connector fallback 모두 0건]
  O4 --> E4[Step 4 전체 skip<br/>multimodal 호출 0건]
```

## 11. 참고 파일

| 파일 | 역할 |
|---|---|
| `skills/formalize/SKILL.md` | 동작 시퀀스 골격 (Step 1~7) |
| `skills/formalize/references/connector-routing.md` | 인증 휴리스틱·MCP 카탈로그·호스트 매핑표·fallback 케이스 표·sanity check 메시지·status 표기 |
| `skills/formalize/references/review-rules.md` | 자동 리뷰 2축 (A. 자체 품질 / B. SSOT 충돌) 점검 기준 |
| `skills/formalize/templates/기능설계서.md` | 8 섹션 표 골격 |
| `skills/formalize/templates/정책서.md` | 10 섹션 표 골격 |
| `docs/prd/prd-0.1.0.md` ~ `prd-0.1.2.md` | PRD 시리즈 (0.1.2 = connector fallback) |
