---
name: planning-format
description: "기획 초안(텍스트·파일·디렉터리·URL·이미지)을 정책서·기능설계서 두 본문으로 변환하고 같은 응답에서 자체 품질 검증까지 출력해야 할 때 사용한다. 외부 SSOT 충돌·acceptance criteria·의존 영향 분석은 planning-review 스킬에서 별도로 수행한다."
argument-hint: "<기획 초안 텍스트 | 파일 | 디렉터리 | URL [URL ...]> [--save] [--no-fetch] [--no-image] [--no-self-review]"
---

# planning-format

orchestration only. 세부 룰은 reference로 lazy read.

## 인자

위치 인자 1개 이상 (필수): 기획 초안 텍스트, 파일 경로, 디렉터리 경로, **1개 이상의 URL** 중 하나.

| 인자 | 기본값 | 설명 |
|---|---|---|
| `--save` | off | `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 아래 정책서 1개 + 기능설계서 1개를 저장한다. 저장 파일은 canonical Markdown 구조를 우선 보존하고, 화면 전용 카드/필드 목록 변환은 저장 파일에 강제하지 않는다. 저장 산출물은 review 대상 입력이 될 수 있지만 SSOT corpus 근거가 될 수 없다. 충돌·안전화는 `references/output-contract.md` 6. |
| `--no-fetch` | off | URL fetch + connector fallback 봉쇄. |
| `--no-image` | off | 이미지 multimodal 호출 0건. |
| `--no-self-review` | off | 자체 품질 검증 블록 출력 생략. **입력 제외 섹션은 끄지 않음** — 변환 결과 핵심 정보. |

## 동작 시퀀스

### Step 1: 입력 dispatch

분기 우선순위:

```
1. URL 패턴 (1개 이상 토큰, 모두 https?://) → URL 분기
2. 디렉터리 경로                              → 디렉터리 분기
3. 파일 경로                                  → 파일 분기 (이미지 확장자면 image queue 단독 시드)
4. 그 외                                      → 텍스트 분기
```

URL 토큰과 비-URL 토큰이 섞이면 텍스트 분기. `file://`/`ftp://`/`mailto:`/scheme 없는 입력은 URL 분기 아님.

분기 직후 **모든 분기 공통**으로 입력 본문에서 URL·이미지 참조를 추출해 fetch queue + image queue에 시드 (markdown link/autolink, HTML href/src/img, plain URL, markdown image, data URI). self-anchor·`mailto:`/`tel:`/`javascript:`/`blob:`은 제외. `--no-fetch`/`--no-image`면 해당 시드 skip.

### Step 2: 빈 입력 sanity check

통합 본문 0byte + 이미지 시드 0건 + URL 시드 0건이면:

```
입력 비어 있음. 기획 초안 텍스트 또는 경로를 인자로 주세요.
```

URL 분기 sanity check는 `references/connector-routing.md` 8.

### Step 3: 재귀 fetch + connector fallback

URL 한 개씩 dequeue → normalize → visited 검사 → fetch 시도 → 본문 합류 + 자식 URL/이미지 추출 → queue push. depth·pages·body 크기 cap 없음. visited set으로만 cycle 방지. `--no-fetch`면 3 전체 skip.

**fetch 시도 의무 (0.2.5)**: queue dequeue된 visited 미포함 URL은 **100% fetch 시도 강제**. 인증 미연결·매핑 없음·미인증 추정 등 사전 판단으로 시도 자체를 생략 금지. 시도 후 실패(인증 게이트·timeout·4xx/5xx·빈 본문·미지원 content-type)는 출처 list `상태` 컬럼에 사유 기록 + visited 등록. fetch 미시도 허용은 `--no-fetch` 단 1케이스. dequeue된 모든 URL은 출처 list 1행 차지 (행 누락 금지).

**queue 순서 BFS 강제 (0.2.5)**: depth N 모두 dequeue 완료 후 depth N+1 dequeue. 같은 depth 안에선 본문 발견 순서 유지 (markdown link → HTML href → plain URL). LIFO·우선순위 휴리스틱 금지. normalize는 queue push 시점에 1회. 출처 list `#` 번호 = BFS dequeue 순서.

self-anchor·`mailto:`/`tel:`/`javascript:`/`blob:`/scheme 없는 URL은 시드 단계에서 이미 제외 (Step 1).

fetch 진입 직전 1회 `references/connector-routing.md`를 Read 적재. WebFetch 1차 + connector fallback·인증 휴리스틱·MCP 카탈로그·호스트 매핑·Google Workspace tool 시퀀스·gid/range·status 표기·sanity check 메시지·**11 connector별 anchor 추출 (deep link)** 모두 거기에.

### Step 4: 이미지 multimodal 처리

`references/conversion-rules.md` 1을 (Step 6 진입 시 함께) 적재해 5경로 시드·지원 확장자·multimodal 해석·실패 사유 처리 따른다. `--no-image`면 4 전체 skip.

### Step 5: 통합 본문 합류

`conversion-rules.md` 2 그대로 — 출처 단위 헤더 + concat + Sheets gid·range 부연.

### Step 6: 변환

`references/conversion-rules.md` 1회 Read 적재. 적재 후:

- 3 기능명 추출 (1순위 1개).
- 4 두 템플릿 변환 — **라벨 매핑 결정 트리 (0.2.5)** + 양 매핑 분배 룰 + 10.2 측면별 분배표.
- 5 list 분해 판단 — 보조 표 번호 순차(`N.M`)·0.2.8 clean header(`### N.M [용도] 보조 표`)·**다층 재귀 max-depth cap = 3 (0.2.5)**. 상위 섹션/row 추적은 입력 제외 섹션 `구조 변환` 처리 줄에 기록. depth 4 진입 시 합류 유지 폴백.

본문 미합류 조각 라벨링은 `references/exclusion-rules.md` 1회 Read 적재 (1 11 카테고리·**2 결정 트리 (0.2.5)**·**3.1 모호성 트리거 + 3.2 16 어구 카탈로그 (0.2.5)**·4 5필드·5 처리 줄·6 헤더 분포·7 marker 1종).

> 큰 입력(통합 본문 ≥30 page 등) 시 indexing(claim 추출·도메인 grouping·충돌 grouping) → synthesis(두 본문) → exclusion → self-review 순 진행 권고. 강제 X — 작은 입력은 자유.

### Step 7: 자체 품질 검증

`--no-self-review`면 F1~F6 self-review만 skip한다. 이때도 `## 생성 결과 요약`, readable 화면 렌더링, 저장 경로, 출처/입력 제외 요약, 상세 추적 배치 규칙은 유지하고 `## 검증 피드백`은 출력하지 않는다.

그 외엔 `references/self-review-rules.md` 적재 후 6 카테고리(F1 충실도·F2 cross-bleed·F3 용어·F4 정책-기능 매핑·F5 누락·F6 syntax) **6패스 체크리스트 점검** — 카테고리당 1패스, 항목별 yes/no 검사(0.2.8 F6 legacy backlink 헤더 금지와 0.2.9 readable boundary 점검 포함). F1·F2는 보조 표(`### N.M ... 보조 표`) 본문도 점검. F5는 본문 누락 + cross-ref 3종(`cross-ref-fetch`·`cross-ref-scope`·`cross-ref-tbd`) 모두. 기준·체크리스트·예시·발견 형식 모두 reference 그대로.

체크리스트 □ 중 unchecked 1개 = 발견 1건. 발견은 `기계적 안정화`, `화면 전용 표시 변환`, `수정 제안 가능`, `사용자/외부 결정 필요` 중 하나로 분류한다.

- `기계적 안정화`는 의미를 바꾸지 않는 범위에서 canonical 본문과 저장 파일에 반영할 수 있다.
- `화면 전용 표시 변환`은 의미를 바꾸지 않는 범위에서 화면 렌더링에만 반영할 수 있다.
- `수정 제안 가능`과 `사용자/외부 결정 필요`는 사용자 승인 전 정책서·기능설계서 canonical 본문에 자동 반영하지 않는다.
- F2/F3/F4/F6 의미 변경 항목은 `## 검증 피드백`에 ID(`F2-1` 등), 위치, 문제, 영향, 제안, 사용자 확인 필요 여부를 남긴다.
- 6 카테고리 모두 0건이면 `## 검증 피드백`은 `없음`으로 출력한다.
- 0.2.10부터 `사용자/외부 결정 필요` F*와 출시 전 해결 필요 입력 제외 항목은 `references/output-contract.md` 2.1, `references/self-review-rules.md` 0.2.10, `references/exclusion-rules.md` 9에 따라 D*/A*/T* 결정 보드 항목 후보가 된다. `--no-self-review`에서는 F* 승격만 skip하고, 입력 제외의 `fetch 실패`, `원문 정의 부재`, `라벨 미매핑`, 명시 `[TBD]`가 출시 전 해결 필요 항목이면 결정 보드를 만들 수 있다.

외부 corpus·다른 *.md는 보지 않음 (planning-review가 처리).

### Step 8: `--save` 처리

`references/output-contract.md` 6 그대로 — `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 저장 경로·기능명 안전화·collision suffix·저장 실패 헤더 표기.

### Step 9: 통합 출력

`references/output-contract.md` Read (Step 8과 함께) — 1 블록 순서·2 정상 출력·3 헤더 줄·4 입력 제외/출처 요약·5 상세 추적·6 저장 계약 그대로 따른다.

최종 응답은 반드시 `# [기능명]`으로 시작한다. 그 앞에 fetch 진행 문장, connector fallback 진행 설명, "변환을 시작합니다" 같은 실행 로그를 쓰지 않는다.

0.2.12부터 기본 순서는 헤더 요약 → `## 생성 결과 요약` → `## 결정 보드`(조건부) → `## 정책서` → `## 기능설계서` → `## 검증 피드백`(self-review 실행 시) → `## 출처 요약` → `## 입력 제외 요약` → `## 상세 추적`(조건 충족 시)이다.

`## 생성 결과 요약`은 항상 `## 정책서`보다 먼저 출력한다. `## 결정 보드`가 필요한 경우에도 생성 결과 요약이 결정 보드보다 먼저 온다. 결정 보드가 없으면 `생성 결과 요약`의 `확인 필요`를 `없음`으로 쓴다.

사용자 확인 필요 항목 또는 출시 전 해결 필요 항목이 있으면 `## 생성 결과 요약` 바로 아래에 `## 결정 보드`를 출력한다. 사용자 확인 필요와 출시 전 해결 필요 항목이 모두 없으면 결정 보드를 생략하고, 상단 검증 줄과 `생성 결과 요약`에 확인 필요 없음 상태를 명시한다.

0.2.11부터 최종 사용자 출력과 `--save` 산출물은 clean display를 사용한다. 섹션 기호를 출력하지 말고 `정책서 5.1`, `기능설계서 7`, `입력 제외 섹션`, `보조 표`처럼 사람이 읽는 위치 표기로 쓴다. 원문 직접 인용 안에 기호가 들어 있는 경우를 제외하고, 생성 결과 요약·결정 보드·검증 피드백·입력 제외 요약·상세 추적에도 같은 규칙을 적용한다.

## 참고 파일

- `templates/기능설계서.md` — 8 섹션 표 골격.
- `templates/정책서.md` — 10 섹션 표 골격.
- `references/conversion-rules.md` — multimodal·통합 본문·기능명·라벨 매핑·list 분해 판단·보조 표 번호 순차·clean header (Step 4·5·6) + 4.1 라벨 매핑 결정 트리 + 4.2 양 매핑 분배 + 4.6 용어 표기 레이어 + 5.4 max-depth cap=3 (0.2.5) + 7 readable 화면 렌더링.
- `references/exclusion-rules.md` — 11 카테고리·5필드(위치 markdown link)·처리 줄·우선순위·헤더 분포·marker 1종 (Step 6) + 2 결정 트리 + 3.1 모호성 트리거 + 3.2 16 어구 (0.2.5).
- `references/output-contract.md` — 생성 결과 요약·readable 산출물 출력·헤더 줄·`--save` 처리·출처/입력 제외 요약·하단 상세 추적·`## 출처` list deep link·분기별 헤더 (Step 8·9).
- `references/self-review-rules.md` — 자체 품질 6 카테고리 (F1~F6) 점검 기준. F1·F2 보조 표 인식 (Step 7) + 항목별 체크리스트 6패스 (0.2.8 F6 legacy backlink 헤더 금지 포함) + 0.2.9 feedback-first 분류/출력 규칙.
- `references/connector-routing.md` — 인증 휴리스틱·MCP 카탈로그·호스트 매핑·Google Workspace tool 시퀀스·gid/range·fallback·status 표기·8 sanity check·11 connector별 anchor 추출 (Step 3) + 5 진입 조건 1차 WebFetch 시도 후 통일 (0.2.5).

외부 검증(SSOT 충돌·acceptance criteria·의존 영향)은 `planning-review` 스킬 별도 호출. 자세한 사용법은 `skills/planning-review/SKILL.md`.
