# Output Contract

`planning-format` 출력 포맷·헤더 줄 형식·`--save` 처리·`## 출처` list URL deep link·분기별 헤더 형식. SKILL.md Step 8~9 진입 시 1회 Read 적재.

## 1. 출력 블록 순서

```
변환 본문 (정책서 → 기능설계서) → 출처 → 입력 제외 → 자체 검증
```

- `## 입력 제외 항목`은 항상 출력 (0건 = `없음` 1줄). `--no-self-review`도 본 블록은 끄지 않는다.
- URL fetch + 이미지 모두 0건이면 `## 출처` 통째 생략.
- `--no-self-review`면 `## 자체 검증` 통째 생략.

정책서·기능설계서 본문은 ` ```markdown ... ``` ` 코드 펜스로 감싼다. 두 본문 안 `### N.M [용도] 보조 표` sub-§은 `conversion-rules.md` §5 list 분해 판단 결과로 부모 § 다음 줄에 동적 등장. 0.2.8부터 보조 표 헤더에는 `(§N row M)` 같은 내부 backlink를 붙이지 않는다. 부모 §/row 추적은 `## 입력 제외 항목`의 `구조 변환` 처리 줄에 둔다. 8/10 섹션 골격은 변경 없음.

## 2. 정상 출력 (변환 + 자체 검증)

````markdown
# [기능명]

- 입력 처리: [§3 분기별 헤더]
- 출처: [§3 출처 줄 — URL 1개일 때만 단일 URL 그대로]
- 미결 표기: [TBD] N개
- 입력 제외: [§4 카테고리 분포]
- 저장: [§3 저장 줄]

---

## 정책서

```markdown
[10 섹션 + (선택) 보조 표 sub-§ — `conversion-rules.md` §5 list 분해 판단 결과로 동적 등장]
```

---

## 기능설계서

```markdown
[8 섹션 + (선택) 보조 표 sub-§ — `conversion-rules.md` §5 list 분해 판단 결과로 동적 등장]
```

---

## 출처

(URL fetch·이미지 처리 1건 이상일 때만)

원본 입력: <"직접 입력" / "파일 N개" / "디렉터리 텍스트 N개" / "URL M개" / "이미지 I개">
재귀 fetch: 성공 N개 / 실패 K개 (cap 없음)

| # | depth | 출처 종류 | URL/경로 또는 위치 | 상태 | 본문 사용 |
|---|---|---|---|---|---|
| 0 | - | 원본 | 직접 입력 / 파일 / 디렉터리 / — | — | O (원본) |
| 1 | 0 | 인자 URL | <Confluence URL>#취소-정책 | 200 (via Atlassian MCP) | O |
| 2 | 1 | 자식 URL | <Sheets URL>#gid=0&range=C13 (출처: [#1] §line N) | 200 (via Google Drive connector — read_file_content) \| 범위 힌트: C13 | O |
| 3 | 1 | 자식 URL | <Google Doc URL>#heading=h.abc (출처: [#1] §line N) | 인증 필요 (Google Drive connector 미인증) | X |
| 4 | 0 | 인자 이미지 | path/diagram.png | image/png 1.2MB | O (multimodal) |

표 행 URL은 deep link 형식(§5). 입력 제외 § 5필드 위치 필드 markdown link URL과 동일.

---

## 입력 제외 항목

(항상 출력. 두 가지 케이스:)

**케이스 A — 0건**:

```
## 입력 제외 항목

없음
```

**케이스 B — ≥1건 (5필드 항목 list)** — `exclusion-rules.md` §4 그대로:

1. [한 줄 제목]
   - 카테고리: [`exclusion-rules.md` §1 11종 중 하나]
   - 위치: [출처 N](URL#anchor) [부연 plain text]
   - 인용: "[입력 원문 ≤80자]"
   - 처리: [`exclusion-rules.md` §5 처리 줄 형식]
   - 설명: [왜 본문에 안 넣었는지 한 줄]

---

## 자체 검증: [통과 | 발견 N건]

- 충실도: N건
- cross-bleed: N건
- 용어 일관성: N건
- 정책-기능 매핑: N건
- 누락: N건
- syntax: N건

### 발견 사항
(≥1건일 때만)
1. [제목]
   - 카테고리: [충실도 / cross-bleed / 용어 일관성 / 정책-기능 매핑 / 누락 / syntax] (F5 cross-ref면 sub: cross-ref-fetch / cross-ref-scope / cross-ref-tbd)
   - 위치: [정책서/기능설계서 §섹션 또는 line N. cross-ref면 양쪽 위치. sub-§은 §N.M row K 표기]
   - 근거: "[변환 본문 인용]"
   - 영향: [한 줄]
   - 제안: [최소 수정 또는 확인 조건]
````

규칙:
- 6 카테고리 모두 0건이면 `## 자체 검증: 통과`로만 + 카운트 줄.

## 3. 헤더 줄 형식

### 3.1 입력 처리 줄

```
URL 분기 (단일):           - 입력 처리: URL 1개 + 재귀 fetch N개 (MCP 경유 K개)
                          - 출처: <인자 URL>
URL 분기 (다중):           - 입력 처리: URL M개 + 재귀 fetch N개 (MCP 경유 K개)
                          - 출처: M개 (전체 list는 ## 출처 블록 참조)
텍스트/파일/디렉터리 + URL 추출: - 입력 처리: <원본 형태> + 추출 URL M개 (재귀 fetch N개) (MCP 경유 K개) + 이미지 I개
이미지 단독 인자:           - 입력 처리: 이미지 1개
URL·이미지 0건:            - 입력 처리: 직접 입력 / 파일 K개 / 디렉터리 텍스트 K개
```

규칙:
- `재귀 fetch N개`는 root 외 자식 URL fetch 성공 수. 0건이면 괄호 생략.
- `MCP 경유 K개`는 connector 합류 URL 수 합계. K=0이면 괄호 생략.
- `--no-fetch`/`--no-image`로 disable된 항목은 헤더에서 누락.

### 3.2 저장 줄

| 케이스 | 출력 |
|---|---|
| `--save` off | `- 저장: 화면 only` |
| `--save` 성공 (충돌 없음) | `- 저장: ./.planning-kit/<기능명>/정책서.md, ./.planning-kit/<기능명>/기능설계서.md` |
| `--save` 성공 (충돌 회피) | `- 저장: ./.planning-kit/<기능명>/정책서-2.md, ./.planning-kit/<기능명>/기능설계서-2.md (기존 파일 보존)` |
| `--save` 실패 | `- 저장: 실패 — <사유>. 본문은 화면 only로 반환.` |

## 4. 입력 제외 분포 줄

`exclusion-rules.md` §6 그대로. 11 카테고리 카운트:

```
- 입력 제외: N건 (다른 후보 K, 라벨 미매핑 L, 중복 M, 근거 부족 P, 포맷 노이즈 Q, 디테일 축약 R, 범위 외 S, 구조 변환 T, fetch 실패 U, 원문 정의 부재 V, 충돌 후보 W)
```

0건일 때 `- 입력 제외: 없음`.

## 5. `## 출처` list URL = deep link 형식 (0.2.4)

`## 출처` 표 행 URL = anchor 지원 source는 deep link 형식 저장:

| Source | URL 형식 | 비고 |
|---|---|---|
| WebFetch HTML | `URL#<heading-id>` (있으면) | `<h*> id="..."` parsing. 없으면 page-level. |
| Confluence | `URL#<heading-id>` | `connector-routing.md` §11.1 |
| Google Docs | `URL#heading=h.<digest>` | §11.2 |
| Google Slides | `URL#slide=id.<id>` | §11.3 |
| Notion | `URL#<block-id>` | §11.4 |
| Google Sheets | `URL#gid=<id>&range=<cell>` | §3.5 (기존) |
| Figma | `URL?node-id=<id>` | URL query 그대로 |
| Slack | thread 영구링크 | URL 자체 |
| Jira | page-level (`#comment-<id>` 가능) | summary·description 단위는 anchor 없음 |

추출 실패·미지원 source = page-level URL fallback. 표 행 URL = 입력 제외 § 위치 필드 markdown link URL과 동일.

### 5.1 출처 list `상태` 컬럼

표기 규칙은 `connector-routing.md` §7. 표는 visited 순서. 실패도 list에 포함. 실패 0건이면 표 아래 `모든 발견 링크·이미지 처리 성공` 한 줄.

### 5.2 다운스트림 파서

- 입력 제외 § 위치 필드: `\[출처 \d+\]\(<URL>\)(,\s*\[출처 \d+\]\(<URL>\))*` 패턴 인식.
- `## 출처` 표 URL: deep link 형식 (fragment 포함). page URL 필요 시 fragment 분리.

## 6. `--save` 처리 (Step 8 흡수)

### 6.1 저장 경로

```
./.planning-kit/<기능명-안전화>/정책서.md
./.planning-kit/<기능명-안전화>/기능설계서.md
```

`## 정책서` / `## 기능설계서` 코드 펜스 안 본문만 추출해 그대로 파일에 쓴다. 자체 검증 보고서·출처 list·입력 제외 §은 디스크 저장 안 함 (화면 only).

### 6.2 기능명 안전화

1. NFC normalize.
2. 경로 분리자 `/`, `\`, 컨트롤 문자 제거.
3. 양 끝 공백·`.` trim.
4. `..`/`-`로 시작 시 `_` prefix.
5. 64자 초과 시 자름.
6. 결과가 빈 문자열이면 `untitled-<8자 난수 hex>`.

기능명에 영문·한글·숫자·공백·`-`·`_`·괄호·대괄호·`.`·중간 점 등은 그대로 둔다.

### 6.3 collision

기존 파일 덮어쓰기 안 함. suffix `-2`/`-3`/... 시도. 99까지 모두 충돌이면 `--save` 실패. `--save-overwrite` 같은 강제 옵션은 없음.

```
./.planning-kit/<기능명>/정책서.md         (기존)
./.planning-kit/<기능명>/정책서-2.md       (신규)
```

### 6.4 저장 실패

본문 변환·자체 검증 결과는 화면에 그대로 출력하고 헤더 `저장:` 줄에 사유 1줄 표시. 호출 종료 사유 아님.
