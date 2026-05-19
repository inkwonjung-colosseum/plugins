# planning-kit PRD 0.2.4

> 0.2.3 기반 incremental PRD. 7개 변경 — (1~3) 0.2.3 sub-§ 도입 후속 정밀화 / (4~5) F·R 검증 축이 sub-§을 점검 대상으로 인식 / (6) SKILL.md 분해 (orchestration only + 3 reference lazy read) / (7) 입력 제외 § + 출처 list URL deep link 형식 + connector별 anchor 추출 / (8) 충돌 후보 카테고리 추가 (10 → 11). 본 PRD 외 명세는 [`prd-0.2.3.md`](./prd-0.2.3.md) 이하 chain 그대로.
>
> **Hotfix (PRD 외)**: 루트 `README.md`·`.claude-plugin/marketplace.json` planning-kit version `0.2.0` → `0.2.3` 동기화. 본 PRD release 시점 0.2.3으로 확정 후 0.2.4 bump.

## 1. 변경 요약

세 묶음:

**A. sub-§ 정밀화 (0.2.3 후속)**
1. 보조 표 번호 순차 부여 — 임의 letter 금지, 부모 § 안 순차(`§4.1`·`§4.2`), 다층은 도트 chain(`§4.1.1`).
2. 보조 표 헤더 backlink — `### 4.1 [용도] 보조 표 (§4 row 3)` 형태. 부모 § + row 위치 명시.
3. `구조 변환` 처리 줄에 sub-§ 위치 명시 — `구조 분해 (위치: 정책서 §5.1·§5.2 / 기능설계서 §4.1)`.

**B. 검증 sub-§ 인식**
4. planning-format F1·F2가 sub-§을 점검 대상으로 인식 (F6은 0.2.3 룰로 자연 catch — 변경 없음).
5. planning-review R1·R2·R3가 sub-§을 부모 § 일부로 corpus 비교·검증가능성·영향 분석에 포함.

**C. 명세·표현력**
6. `planning-format/SKILL.md` 분해 — orchestration only. 세부 룰 3개 신규 reference로 split: `conversion-rules.md` / `exclusion-rules.md` / `output-contract.md` (save 흡수).
7. **입력 제외 § + `## 출처` list URL = deep link 형식** — 위치 필드를 markdown link 형식으로(`[출처 3](URL#anchor)`). 정책서·기능설계서 본문은 변경 없음 (결정문서 깨끗 유지). 추적은 추적 §의 책임. connector별 anchor 추출 룰 추가 (Confluence·Google Docs·Slides·Notion 4종 신규, Sheets·Figma·Slack은 0.1.x부터 이미 지원).
8. 입력 제외 § 카테고리 11종으로 확장 — `충돌 후보` 신규, **#11 끝 배치** (기존 1~10 우선순위 변경 없음). 본문 충돌 표기는 `[TBD]` + 카테고리 cross-ref (marker 신설 X, 1종 정책 유지).

`planning-review` 동작 변경은 #5 sub-§ 인식 한정. 인자·corpus 처리·R1 link follow·R3 보조 신호 모두 0.2.3 그대로.

## 2. 동기

### 2.1 sub-§ 도입 후 정합성 (1~5)

0.2.3에서 보조 표 sub-§을 동적 추가했으나:

- 번호 placeholder가 `§N.x.y` 같은 임의 letter로 명시돼 운영 혼란.
- 보조 표가 부모 § 어느 row에서 분해됐는지 추적 불가.
- 입력 제외 § `구조 변환` 처리 줄이 부모 § 위치만 가리킴 — sub-§ 위치 누락.
- F1·F2 자체 검증, R1·R2·R3 외부 검증이 8/10 § 골격 가정. sub-§ 점검 대상 인식 명시 부재 → 보조 표 안 [TBD]·cross-bleed·비정량 표현 silently 통과.

### 2.2 SKILL.md 명세 밀도 (6)

`planning-format/SKILL.md` = 363 line (0.2.3 다이어트 후). 여전히 dispatch·fetch·multimodal·conversion·exclusion·self-review·save·output 8 도메인이 한 파일. orchestration + lazy read 구조가 attention 보존에 유리.

### 2.3 traceability·표현력 (7~8)

- 입력 제외 §·출처 list 행 URL이 page-level — 사람이 페이지 들어가서 keyword 검색해야 해당 § 도달. 즉 추적은 page 단위만 가능, 1-hop deep link 부재.
- 정책서·기능설계서 본문은 결정문서로 깨끗 유지가 정책. 본문 row마다 cite 다는 건 noise. 추적은 입력 제외 §·출처 list § 책임.
- 입력에서 같은 사실이 다른 값으로 등장 (ex `출처 3: 24시간 / 출처 7: 7일`) 시 main이 한 값을 silently 선택. 충돌 사실 자체가 본문에 안 드러남.

## 3. 비목표

- 입력·fetch·depth·page·body 모든 cap 도입 안 함 (cap 없음 정책 그대로).
- SSOT 신뢰도·connector·runtime 자동 관리 안 함 (사람·환경 책임).
- planning-review 인자·corpus·R1 link follow·R3 보조 신호 동작 변경 없음 (sub-§ 인식 외).
- marker 1종 정책 유지 (`[TBD-CONFLICT]` 등 신설 X).
- 다층 sub-§ depth cap 도입 안 함.
- F6 syntax lint 변경 없음 (0.2.3 룰이 sub-§ 자연 catch).
- reasoning phase 강제 prescriptive spec 없음 (SKILL.md §6 진입 직전 1줄 권고만).
- **정책서·기능설계서 본문 cite 도입 안 함** — 본문은 결정문서로 깨끗 유지. cite 옵션(`--with-evidence` 등) 신설 안 함. 출처 추적은 입력 제외 §·`## 출처` list § 책임.
- 후속 PRD 도입 항목: severity 분리·메타 JSON 자동 저장·긴 본문 row 분해·보조 표 컬럼 카탈로그·schema 공유·plugin contract test suite.

## 4. sub-§ 정밀화

### 4.1 보조 표 번호 순차

0.2.3 §6.2 list 분해 판단 룰에 번호 부여 명시 추가:

- 부모 § 안 보조 표 번호는 **순차 부여** — 첫 보조 표 = `§N.1`, 두 번째 = `§N.2`, ... `§N.M`.
- 다층 분해 시 도트 chain — `§4.1` 안 셀이 또 분해되면 `§4.1.1`, `§4.1.2`. 그 안이 또 분해되면 `§4.1.1.1` 식.
- 같은 부모 § 안 두 보조 표는 항상 다른 번호. 같은 번호 재사용 금지.
- 임의 letter (`§N.x`·`§N.x.y` placeholder) 사용 금지.

### 4.2 보조 표 헤더 backlink

보조 표 헤더 형식 확장:

```markdown
### 4.1 [용도] 보조 표 (§4 row 3)
```

- 괄호 안 `§N row M` = 부모 § 번호 + 분해 발생 row 위치.
- row 식별 못 하면 부모 §만 (`(§4)`).
- 다층 보조 표는 부모 보조 표 row 가리킴 (예: `(§4.1 row 2)`).

### 4.3 `구조 변환` 처리 줄에 sub-§ 위치

0.2.3 §6.5 처리 줄 형식 갱신:

| 카테고리 | `처리` 줄 형식 |
|---|---|
| `구조 변환` | `구조 분해 (위치: 정책서 §N1·§N1.1 / 기능설계서 §M1·§M2.1)` |

부모 § + sub-§ 모두 list. 분해 위치가 sub-§에만 있으면 sub-§ 단독 표기.

## 5. 검증 sub-§ 인식

### 5.1 planning-format 자체 검증 (F1·F2)

`references/self-review-rules.md` 갱신:

- **F1 섹션 충실도**: `[TBD]` 비율·빈 row·빈 § 점검에 sub-§(`### N.x ... 보조 표`) 본문 포함. 보조 표 헤더만 있고 row 0이면 빈 row 발견.
- **F2 라벨 cross-bleed**: 정책서 sub-§ 안 화면·동작 단어, 기능설계서 sub-§ 안 정책 단어 점검. 부모 § 룰 그대로 sub-§ 확장.

F3·F4·F5는 본문 의미 점검이라 sub-§ 자연 포함 (변경 명시 없음). F6은 기존 룰(`# 다음 첫 자식 ### 이상 = 점프`)이 `## §N → ### N.x` 정상 case를 자연 catch — 변경 없음.

### 5.2 planning-review 외부 검증 (R1·R2·R3)

`references/ssot-rules.md`·`ac-rules.md`·`deps-rules.md` 갱신:

- **R1 SSOT 충돌**: 산출물 부모 § + sub-§ 본문 모두 corpus 비교 대상. sub-§ 단독 발견 가능.
- **R2 AC 검증가능성**: 검증 대상 § 확장 — 정책서 §5·§6, 기능설계서 §5·§7 + **그 안 sub-§** 모두 포함.
- **R3 의존·영향 분석**: 변환 본문 정의 = 부모 § + sub-§ 합집합. 영향 후보 산출 키워드 추출에 sub-§ 본문도 포함.

### 5.3 발견 위치 표기

발견 형식의 `위치` 줄에 sub-§ 명시 가능:

```
- 위치: 정책서 §5.1 row 3 (보조 표 안)
```

기존 `정책서 §5` 표기와 호환. 부모 § + sub-§ + row 모두 식별되면 셋 다 표시.

## 6. SKILL.md 분해

### 6.1 분해 후 구조

`skills/planning-format/`:

```
SKILL.md                              # orchestration only (~120 line 목표)
templates/기능설계서.md
templates/정책서.md
references/
├── connector-routing.md              # 0.2.3 그대로
├── self-review-rules.md              # 0.2.4 §5.1 갱신
├── conversion-rules.md               # 신규 — multimodal·통합 본문·기능명·라벨 매핑·list 분해 판단·보조 표 번호·backlink
├── exclusion-rules.md                # 신규 — 11 카테고리·5필드·처리 줄(§4.3)·우선순위
└── output-contract.md                # 신규 — 출력 포맷·헤더 줄 형식·--save 처리·출처 list URL deep link·분기별 헤더
```

`save-contract`는 `output-contract.md`에 흡수 (filesystem 저장 = output 도메인). 4 → 3 reference로 압축.

### 6.2 SKILL.md 골격 (분해 후)

남는 것: 인자 표 + Step 1~9 high-level (각 1~3줄, lazy read 지시 포함) + 참고 파일.

빠지는 것 (lazy read):
- §4 multimodal·§5 통합 본문·§6.1 기능명·§6.2 변환 + list 분해 → `conversion-rules.md`.
- §6.3~§6.5 입력 제외 → `exclusion-rules.md`.
- §8 `--save` + §출력 포맷·§7.1~7.3 헤더 형식 → `output-contract.md`.

### 6.3 reasoning phase 권고 (1줄)

SKILL.md Step 6 변환 진입 직전 1줄:

> 큰 입력(통합 본문 ≥30 page 등) 시 indexing(claim 추출·도메인 grouping·충돌 grouping) → synthesis(두 본문) → exclusion → self-review 순 진행 권고. 강제 X — 작은 입력은 자유.

별도 phase spec § 없음. AI 자유 판단.

## 7. 입력 제외 § + 출처 list deep link

### 7.1 정책

`## 입력 제외 항목` 5필드 위치 필드 + `## 출처` list URL을 markdown link 형식으로 저장. 클릭 = 외부 source 특정 위치 1-hop 점프.

**정책서·기능설계서 본문은 변경 없음** — cite 옵션·본문 셀 link 도입 안 함. 본문은 결정문서로 깨끗 유지, 추적은 입력 제외 §·출처 list § 책임.

### 7.2 입력 제외 § 5필드 위치 형식 갱신

기존 (0.2.3):

```markdown
1. [한 줄 제목]
   - 카테고리: [§6.3 카테고리]
   - 위치: [입력 측 위치 — 파일명:라인 / "직접 입력" / "[출처 N] §섹션 또는 줄 N"]
   - 인용: "..."
   - 처리: ...
   - 설명: ...
```

신규 (0.2.4) — `위치` 필드를 markdown link 형식으로:

```markdown
1. 외부 위키 본문 누락
   - 카테고리: fetch 실패
   - 위치: [출처 3](https://confluence.../pages/123#취소-정책) 줄 42
   - 인용: "결제 24시간 내 취소"
   - 처리: 본문 미합류 (출처 list #3 참조)
   - 설명: ...

2. 주문 취소 가능 기간 충돌
   - 카테고리: 충돌 후보
   - 위치: [출처 3](https://confluence.../pages/123#취소-정책), [출처 7](https://docs.../edit#heading=h.xyz)
   - 인용: "24시간" / "7일"
   - 처리: 1순위 값 합류 (정책서 §5 / 기능설계서 §5), 나머지 추적 (24시간, 7일)
   - 설명: ...
```

규칙:
- 위치 필드 첫 부분 = `[출처 N](URL)` markdown link 1개 또는 복수 (콤마 구분).
- URL = `## 출처` list 행 URL (deep link 형식, §7.3).
- 입력 측 위치(파일명:라인) 추가 정보는 link 뒤 plain text로 (`[출처 3](URL) 줄 42`).
- 출처 미상·로컬 파일은 link 없이 plain text 그대로 (`./docs/draft/주문취소.md:15` / `"직접 입력"`).
- anchor 추출 실패 시 page-level URL fallback (link는 작동, 점프는 page 단위).

### 7.3 `## 출처` list URL = deep link 형식

기존: 행 URL이 page-level (`https://confluence.../pages/123`).

신규: anchor 지원 source는 deep link 형식 저장 (`https://confluence.../pages/123#취소-정책`).

`## 출처` 표 행 URL = 입력 제외 § 위치 필드 markdown link URL과 동일.

### 7.4 connector별 anchor 추출 (`connector-routing.md` §11 신규)

| Source | Anchor 형식 | 추출 방법 | 0.2.4 |
|---|---|---|---|
| Google Sheets | `URL#gid=<id>&range=<cell>` | URL fragment 그대로 (이미 §3.5) | ✓ 0.1.1 |
| Figma | `URL?node-id=<id>` | URL query 그대로 | ✓ 0.1.2 |
| Slack thread | thread 영구링크 | URL 자체 영구링크 | ✓ 0.1.2 |
| **Confluence** | `URL#<heading-id>` | Atlassian MCP body XHTML `<h1 id="..."`/`<h2 id="...">` 등 추출. 본문 합류 § heading id 매핑. | **신규** |
| **Google Docs** | `URL#heading=h.<digest>` | `read_file_content` 응답에서 heading anchor 추출. heading text → digest 매핑. | **신규** |
| **Google Slides** | `URL#slide=id.<id>` | slide ID를 응답에서 추출. | **신규** |
| **Notion** | `URL#<block-id>` | Notion connector 응답에서 block id 추출 (best-effort). | **신규** |
| Jira | page-level (anchor 없음) | summary·description 단위는 anchor 없음. comment ref 시 `#comment-<id>` 가능. | 부분 |
| 기타 (WebFetch HTML) | heading id 있으면 추출 | `<h*> id="..."` parsing. 없으면 page-level. | best-effort |

추출 실패·미지원 source = page-level URL fallback.

### 7.5 anchor 매칭 — 입력 제외 § 항목 단위

같은 source가 여러 항목 위치로 분산 인용될 때 각 항목별로 가장 가까운 anchor 사용. 매칭 우선순위:

1. 항목 인용 내용이 source 특정 § 본문에서 발췌된 명확한 경우 → 해당 § anchor.
2. 항목이 source 전체에 걸친 일반 정보 → page-level URL.
3. 매칭 불확실 → page-level URL.

main 판단. 강제 매핑 룰 없음.

### 7.6 다운스트림 파서

- 입력 제외 § 위치 필드: `\[출처 \d+\]\(<URL>\)(,\s*\[출처 \d+\]\(<URL>\))*` 패턴 인식.
- `## 출처` 표 URL: deep link 형식 (fragment 포함). page URL 필요 시 fragment 분리.

## 8. 충돌 후보 카테고리 (10 → 11)

### 8.1 카테고리 추가 (#11)

`exclusion-rules.md` 카테고리 표 #11:

| # | 카테고리 | 정의 |
|---|---|---|
| 11 | `충돌 후보` | 같은 사실(역할·상태·임계·권한)이 입력에서 ≥2 다른 값으로 등장. main이 1순위 값을 본문 합류, 나머지를 본 카테고리로 추적. 본문 셀에 1순위 미명확 시 `[TBD]` + 본 카테고리 cross-ref. |

### 8.2 우선순위 — #11 끝 배치

```
범위 외 > fetch 실패 > 구조 변환 > 디테일 축약 > 원문 정의 부재 >
다른 기능 후보 > 라벨 미매핑 > 중복 > 근거 부족 무시 > 포맷 노이즈 > 충돌 후보
```

기존 1~10 우선순위 변경 없음. `충돌 후보`는 끝 배치 — main 판단으로 다른 카테고리에 더 적합하면 그쪽 우선.

### 8.3 처리 줄 형식

| 카테고리 | `처리` 줄 |
|---|---|
| `충돌 후보` | `1순위 값 합류 (정책서 §N / 기능설계서 §M), 나머지 추적 (값 list)` |

본문 셀에 1순위 미명확 → `[TBD]` 표기 + 입력 제외 § cross-ref. marker 1종(`[TBD]`) 정책 유지.

### 8.4 헤더 분포

`- 입력 제외:` 줄 끝에 `충돌 후보 V` 추가:

```
- 입력 제외: N건 (다른 후보 K, ..., 원문 정의 부재 W, 충돌 후보 V)
```

## 9. SKILL.md / reference 갱신

| 파일 | 변경 |
|---|---|
| `skills/planning-format/SKILL.md` | orchestration only로 분해. Step 1~9 high-level + reasoning phase 1줄 권고 + 인자 표 (변경 없음) + 참고 파일. ~120 line. |
| `skills/planning-format/references/conversion-rules.md` | **신규**. multimodal·통합 본문·기능명·라벨 매핑·list 분해 판단(0.2.3) + 보조 표 번호 순차·backlink(§4). |
| `skills/planning-format/references/exclusion-rules.md` | **신규**. 11 카테고리(§8) + 5필드 (위치 필드 markdown link, §7.2) + 처리 줄(§4.3 갱신) + 우선순위 + marker 1종. |
| `skills/planning-format/references/output-contract.md` | **신규**. 출력 포맷·헤더 줄 형식·`--save`·`## 출처` list URL deep link 형식(§7.3)·분기별 헤더. |
| `skills/planning-format/references/self-review-rules.md` | F1·F2에 sub-§ 인식 룰 추가(§5.1). |
| `skills/planning-format/references/connector-routing.md` | §11 신규 — connector별 anchor 추출 룰 (Confluence·Docs·Slides·Notion 4종). Sheets·Figma·Slack은 기존 룰 인용만. |
| `skills/planning-format/templates/*` | 변경 없음. |
| `skills/planning-review/SKILL.md` | sub-§ 인식 명시 (§5.2). 인자·축·corpus·link follow 변경 없음. |
| `skills/planning-review/references/ssot-rules.md` / `ac-rules.md` / `deps-rules.md` | sub-§ 인식 절차. |
| `.codex-plugin/plugin.json` / `.claude-plugin/plugin.json` | version 0.2.3 → 0.2.4. description 1줄. |
| `README.md` | 입력 제외 § + 출처 list deep link 명시·11 카테고리·호환성·비교 표 헤더·파일 구조에 신규 reference 3종. |
| `docs/planning-format-workflow.md` | Step 6+7 mermaid에 sub-§ 인식 표시. |
| `docs/prd/README.md` | 0.2.4 row + 파일 list. |
| `docs/prd/prd-0.2.4.md` | 본 문서. |

추정 line 변동: SKILL.md 363 → ~120 (-243). 신규 reference 3종 합 ~250 (+250). 순 micro-positive, attention 부담 감소.

## 10. 호환성

### 10.1 0.2.3 → 0.2.4

- 출력 markdown **추가·micro-change** — 보조 표 헤더 backlink 괄호 추가, 입력 제외 § 위치 필드 markdown link 형식, `## 출처` list URL deep link 형식, `충돌 후보` 카테고리 추가. **정책서·기능설계서 본문 변경 없음** → micro-breaking 아님.
- **인자 변경 없음** — 신규 옵션 신설 안 함. 기존 인자·옵션 그대로.
- 카테고리 우선순위 — 기존 1~10 unchanged. 신규 #11 끝 배치 → 기존 분류 결과 영향 없음.
- marker 1종 정책 유지 — 다운스트림 파서 marker 변경 없음.
- 0.2.3 산출물 호환 — 임의 letter sub-§은 자동 catch 안 함 (재실행 시 자동 정정).
- `planning-review`가 sub-§을 corpus 비교에 포함 → 0.2.3 산출물 review 시 발견 카운트 약간 증가 가능.
- **출처 URL 형식 micro-change** — anchor 지원 source(Confluence·Docs·Slides·Notion) URL이 deep link 형식으로 저장. 기존 page URL 다운스트림 코드는 fragment 무시하면 정상 작동. 명시적 page URL 필요 시 fragment 분리 필요.
- **입력 제외 § 위치 필드 micro-change** — 기존 plain text → markdown link 형식. 다운스트림 파서: `\[출처 \d+\]\(<URL>\)` 패턴 인식.
- 다운스트림 파서 영향 종합: 보조 표 헤더 backlink 괄호 + 입력 제외 § 위치 필드 markdown link + 출처 list URL deep link fragment.

### 10.2 환경 의존성

변경 없음.

## 11. 검증 시나리오

PRD 검수 시점 main 트레이스:

1. **보조 표 순차 부여** — 같은 § 안 분해 2회 = `§4.1` + `§4.2`. 다층 = `§4.1.1`.
2. **보조 표 backlink** — `### 4.1 ... (§4 row 3)`. row 미식별 시 `(§4)`.
3. **`구조 변환` 처리 줄 sub-§** — `구조 분해 (위치: 정책서 §5.1·§5.2 / 기능설계서 §4.1)`.
4. **F1·F2 sub-§ 인식** — 보조 표 안 `[TBD]` 비율도 충실도 카운트, sub-§ 빈 row 발견. 정책서 보조 표 화면 단어 cross-bleed 발견.
5. **R1·R2·R3 sub-§ 인식** — sub-§ corpus 비교·검증가능성·영향 후보 모두 포함. 위치 표기 `§N.M row K`.
6. **입력 제외 § 위치 = Confluence anchor** — `[출처 3](URL#취소-정책) 줄 42`. 클릭 = page 특정 § 1-hop 점프. `## 출처` 표 행 URL도 동일.
7. **anchor 추출 실패** — page-level fallback. 위치 = `[출처 3](URL)` (fragment 없음). link 작동, page 단위 점프.
8. **Sheets/Figma/Slack 출처** — 기존 fragment 그대로 (`#gid=&range=` / `?node-id=` / 영구링크). 자동 deep link.
9. **로컬 파일 출처** — link 없이 plain text (`./docs/draft/주문취소.md:15`).
10. **충돌 후보 — 같은 claim 다른 값** — 1순위 본문 합류, 나머지 입력 제외 § `충돌 후보`로 추적. 본문 셀 1순위 미명확 시 `[TBD]` + cross-ref.
11. **헤더 입력 제외 분포 #11** — `충돌 후보 V` 카운트 표기 (0 = 누락).
12. **SKILL.md 분해 lazy read** — Step 6 진입 시 `conversion-rules.md` 적재. Step 8/9 시 `output-contract.md` 적재 (save 흡수).

## 12. 성공 기준

- 보조 표 번호 순차 부여 (letter X), 헤더 `(§N row M)` backlink 등장.
- `구조 변환` 처리 줄에 sub-§ 위치 명시.
- F1·F2 자체 검증, R1·R2·R3 외부 검증이 sub-§ 점검 대상 포함.
- `planning-format/SKILL.md` ~120 line, 신규 reference 3종 lazy read.
- 입력 제외 § 위치 필드 = markdown link 형식 (`[출처 N](URL#anchor)`). 1-hop 점프.
- `## 출처` list URL = deep link 형식 (anchor 지원 source).
- 정책서·기능설계서 본문은 cite 없이 0.2.3 그대로 (결정문서 깨끗 유지).
- Confluence·Docs·Slides·Notion source의 URL이 deep link 형식 — Sheets·Figma·Slack은 0.1.x 그대로.
- 입력 제외 § 11 카테고리 (`충돌 후보` #11 끝).
- marker 1종(`[TBD]`) 정책 유지.
- 인자·옵션·planning-review 동작·재귀 fetch·multimodal·sanity check 0.2.3 그대로 (sub-§ 인식 + connector anchor 추출 외). **신규 인자·옵션 0**.

## 13. 용어 추가

- **보조 표 backlink**: 보조 표 헤더 `### N.M [용도] 보조 표 (§N row K)` 괄호 부분. 부모 § + 분해 row 위치.
- **sub-§ 인식**: F1·F2·R1·R2·R3가 부모 § + sub-§ 본문 모두 점검·비교 대상으로 포함하는 정책. §5.
- **deep link 위치 형식**: 입력 제외 § 5필드 `위치` 필드 + `## 출처` list 행 URL = markdown link 형식 (`[출처 N](URL#anchor)`). 정책서·기능설계서 본문은 cite 없음 (결정문서 깨끗 유지).
- **anchor 추출**: `connector-routing.md` §11 룰. source별로 URL을 deep link 형식으로 저장 (Confluence heading id / Docs heading anchor / Slides slide id / Notion block id 등). 추출 실패 시 page-level URL fallback.
- **충돌 후보**: 입력 제외 § 카테고리 #11. 같은 사실 ≥2 다른 값. 1순위 합류, 나머지 추적.
- **conversion-rules / exclusion-rules / output-contract**: 0.2.4 신규 reference 3종. SKILL.md orchestration only로 분해 후 세부 룰 lazy read.

그 외 모든 용어는 0.2.3 §15 / 0.2.2 §14 그대로.

## 14. 참고 파일

- `skills/planning-format/SKILL.md` — orchestration only.
- `skills/planning-format/references/conversion-rules.md` — 신규.
- `skills/planning-format/references/exclusion-rules.md` — 신규 (11 카테고리).
- `skills/planning-format/references/output-contract.md` — 신규 (save 흡수).
- `skills/planning-format/references/self-review-rules.md` — F1·F2 sub-§ 인식.
- `skills/planning-review/SKILL.md` + 3 reference — sub-§ 인식.
- `.claude-plugin/plugin.json` / `.codex-plugin/plugin.json` — version 0.2.4.
- `README.md` — 옵션·11 카테고리·호환성.
- `docs/planning-format-workflow.md` — sub-§ 인식 표시.
- `docs/prd/README.md` — 0.2.4 row.
- `docs/prd/prd-0.2.4.md` — 본 문서.
