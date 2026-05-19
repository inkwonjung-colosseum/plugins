# planning-kit PRD 0.2.6

> 0.2.5 기반 incremental PRD. `planning-review` 입력 dispatch를 `planning-format` 입력 처리와 동등하게 확장한다. URL 1개 이상, 특히 정책서·기능설계서가 서로 다른 링크에 저장된 경우를 직접 입력으로 받을 수 있어야 한다. 본 PRD 외 명세는 [`prd-0.2.5.md`](./prd-0.2.5.md) 이하 chain 그대로.
>
> 핵심 변경: `planning-review`가 다중 URL 입력을 root input으로 fetch + 재귀 fetch + connector fallback + 이미지 multimodal 처리한 뒤, 통합 입력 본문에서 정책서·기능설계서·입력 제외 §을 분리한다. 입력 fetch 제어 옵션 `--no-input-fetch` / `--no-input-image`를 추가한다.

## 1. 변경 요약

1. **planning-review URL 다중 입력 허용** — `planning-review https://policy ... https://feature ...` 형태를 URL 분기로 처리한다. 모든 URL은 depth 0 root input source다.
2. **planning-format 입력 처리 parity** — `planning-review` 입력 dispatch는 `planning-format` Step 1~5와 같은 URL 판별, 본문 URL·이미지 추출, 재귀 fetch, connector fallback, image multimodal, 통합 본문 합류 규칙을 사용한다.
3. **입력 fetch와 SSOT fetch 분리** — 입력 URL fetch는 review 대상 본문을 만들기 위한 단계이고, 기존 R1/R3 SSOT corpus link follow는 외부 검증 corpus를 확장하기 위한 단계다. 두 단계는 별도 visited set과 별도 출처 블록을 가진다.
4. **입력 fetch 제어 옵션 추가** — `--no-input-fetch`는 review 입력 URL fetch를 봉쇄하고, `--no-input-image`는 review 입력 이미지 multimodal을 봉쇄한다. 기존 `--no-ssot-fetch` / `--no-ssot-image`는 SSOT corpus에만 적용한다.
5. **review 입력 출처 블록 추가** — 입력 URL fetch·이미지 처리가 1건 이상이면 `## 입력 출처` 블록을 출력한다. 기존 `## SSOT 출처`와 별개다.
6. **본문 식별 fallback 확장** — fetch된 각 root source의 title/path/URL label이 정책서·기능설계서를 명확히 가리키면, 헤더가 없어도 source 단위로 정책서/기능설계서 후보에 배정할 수 있다.

## 2. 동기

현재 `planning-format`은 다음 흐름을 지원한다.

```bash
/planning-kit:planning-format https://a.example/policy https://b.example/feature
```

각 URL은 root URL로 fetch되고, 본문 안 자식 링크도 재귀 fetch된다. 반면 `planning-review`는 0개, 디렉터리 1개, 파일 1개, raw markdown 1개, 파일 2개만 입력으로 받는다. 정책서와 기능설계서가 각각 Confluence, Google Docs, Notion, GitHub wiki 등 서로 다른 링크에 저장되면 review를 바로 실행할 수 없다.

사용자 기대는 단순하다.

```bash
/planning-kit:planning-review https://wiki.example/policy https://docs.example/feature
```

위 호출이 `planning-format`의 URL 입력처럼 동작해야 한다. fetch된 본문에서 정책서·기능설계서를 식별하고, 그 산출물을 대상으로 R1/R2/R3 review를 수행해야 한다.

## 3. 비목표

- `planning-review`가 변환을 수행하지 않는다. 입력 링크는 이미 작성된 정책서·기능설계서 산출물이어야 한다.
- 입력 root URL을 자동으로 SSOT corpus로 간주하지 않는다. 입력 URL은 review 대상이고, SSOT corpus는 기존 R1/R3 `*.md` 매칭 + SSOT link follow다.
- `--ssot-url` 같은 외부 SSOT URL 직접 주입 옵션은 도입하지 않는다. 후속 PRD 후보.
- fetch depth·pages·body·fanout cap을 도입하지 않는다. `planning-format`과 같은 cap 없음 정책 유지.
- connector 인증 자동 완료, retry/backoff, cache, session 간 reuse는 도입하지 않는다.
- `planning-format`의 변환·자체 검증 동작은 변경하지 않는다.
- `planning-review` 출력 발견 형식(R1/R2/R3 항목 구조)은 변경하지 않는다.

## 4. 입력 인자 규칙

### 4.1 기존 규칙

0.2.5 `planning-review` 위치 인자:

- 0개 = conversation 참조 모드.
- 1개 디렉터리 = `정책서*.md` + `기능설계서*.md` 자동 검색.
- 1개 파일 = 본문 안 두 섹션 자동 분리.
- 1개 raw markdown 텍스트 = 두 본문 자동 분리.
- 2개 = `<정책서> <기능설계서>` 또는 역순.
- 3개 이상 = sanity check.

### 4.2 신규 규칙

0.2.6 `planning-review` 위치 인자:

- 0개 = conversation 참조 모드. 기존 그대로.
- 1개 이상이고 모든 비어 있지 않은 토큰이 `^https?://` = URL 분기. **다중 URL 허용**.
- 1개 디렉터리 = 기존 디렉터리 분기.
- 1개 파일 = 기존 파일 분기. 이미지 확장자면 input image queue 단독 시드.
- 2개 non-URL path = 기존 두 파일 분기.
- 그 외 = raw markdown 텍스트 분기. URL 토큰과 비-URL 토큰이 섞이면 `planning-format`과 동일하게 텍스트 분기로 본다.

`file://` / `ftp://` / `mailto:` / scheme 없는 입력은 URL 분기 아님. 텍스트 분기 안 plain URL은 공통 URL 추출 단계에서 input fetch queue에 시드된다.

### 4.3 URL 분기 예시

```bash
/planning-kit:planning-review https://wiki.example/policy/order-cancel

/planning-kit:planning-review \
  https://wiki.example/policy/order-cancel \
  https://docs.example/feature/order-cancel

/planning-kit:planning-review \
  https://docs.google.com/document/d/<policyId>/edit \
  https://docs.google.com/document/d/<featureId>/edit \
  --axes ssot,deps
```

## 5. 입력 수집 단계

`planning-review`는 Step 1 본문 식별 전에 input collection 단계를 실행한다. 절차는 `planning-format` Step 1~5와 동일한 룰을 공유한다.

### 5.1 공통 추출

분기 직후 모든 입력 본문에서 URL·이미지 참조를 추출한다.

- markdown link
- autolink
- HTML `href` / `src` / `img`
- plain URL
- markdown image
- data URI

제외:

- self-anchor
- `mailto:`
- `tel:`
- `javascript:`
- `blob:`
- non-http scheme

### 5.2 재귀 fetch

input fetch queue는 `planning-format` 0.2.5와 같은 결정성 룰을 따른다.

- root URL은 depth 0.
- queue push 시점 normalize.
- depth N 모두 dequeue 후 depth N+1 dequeue.
- 같은 depth 안에서는 본문 발견 순서 유지: markdown link → HTML href/src → plain URL.
- dequeue된 visited 미포함 URL은 100% fetch 시도.
- 1차 WebFetch 의무.
- connector fallback은 `../planning-format/references/connector-routing.md`를 공유 적재.
- dequeue된 모든 URL은 `## 입력 출처` 1행 차지.
- 실패도 status 기록 + visited 등록.

### 5.3 이미지 처리

input image queue는 `planning-format` Step 4와 같은 5경로 시드를 따른다.

1. 인자 파일이 이미지 확장자.
2. 디렉터리 안 지원 이미지 파일.
3. 본문의 markdown image / HTML img.
4. fetch 응답이 `image/*` content-type.
5. inline `data:image/...;base64,...`.

`--no-input-image` ON이면 input image multimodal은 0건이다. 이 옵션은 SSOT image 처리와 무관하다.

### 5.4 통합 입력 본문 합류

fetch·image 처리가 끝나면 source 단위 헤더로 concat한다.

```markdown
=== [입력 출처 1] URL: https://wiki.example/policy/order-cancel ===
...

=== [입력 출처 2] URL: https://docs.example/feature/order-cancel ===
...
```

Google Sheets gid/range, connector deep link anchor, metadata only 상태 등은 `planning-format`과 동일하게 부연한다.

## 6. 본문 분리

input collection 후 `planning-review`는 통합 입력 본문에서 정책서·기능설계서·입력 제외 §을 분리한다.

### 6.1 분리 우선순위

1. `# 정책서` / `## 정책서` 헤더 → 정책서 본문.
2. `# 기능설계서` / `## 기능설계서` 헤더 → 기능설계서 본문.
3. `## 입력 제외 항목` 헤더 → 입력 제외 § 본문.
4. markdown 코드 펜스 안 헤더 → 펜스 안 본문에서 1~3 반복.
5. source title/path/URL label이 `정책서`, `policy`, `정책`, `기능설계서`, `feature`, `design`, `spec` 중 하나를 명확히 가리키면 source 단위 fallback 배정.
6. 위 절차 후 정책서·기능설계서 둘 다 확보하지 못하면 sanity check.

### 6.2 source 단위 fallback

다중 URL 입력에서 각 root URL이 별도 문서인 경우를 지원한다.

예:

| root source | title/path signal | 배정 |
|---|---|---|
| `https://wiki.example/policy/order-cancel` | URL path `policy` | 정책서 후보 |
| `https://docs.example/feature/order-cancel` | URL path `feature` | 기능설계서 후보 |
| Google Docs title `주문 취소 정책서` | title `정책서` | 정책서 후보 |
| Notion title `Order Cancel Feature Spec` | title `Feature Spec` | 기능설계서 후보 |

fallback은 명확한 1:1 신호가 있을 때만 사용한다. 두 source가 모두 같은 종류로 추정되거나 둘 다 불명확하면 fallback하지 않고 sanity check를 출력한다.

### 6.3 입력 제외 §

`planning-format` 산출물에서 가져온 `## 입력 제외 항목`은 기존 0.2.2 규칙대로 분리한다. 다중 URL에 입력 제외 §이 여러 개 있으면 발견 순서대로 concat한다. 같은 항목 dedup은 비목표다.

## 7. 옵션

### 7.1 신규 옵션

| 인자 | 기본값 | 설명 |
|---|---|---|
| `--no-input-fetch` | off | review 입력 본문 안 URL fetch + URL root fetch + connector fallback 봉쇄. 파일/텍스트 본문 자체는 읽지만 그 안 URL은 fetch하지 않는다. |
| `--no-input-image` | off | review 입력 이미지 multimodal 호출 0건. URL fetch는 그대로 진행하되 image content-type 응답은 본문 합류하지 않는다. |

### 7.2 기존 옵션과의 범위

| 옵션 | 적용 범위 |
|---|---|
| `--no-input-fetch` | review 대상 입력 수집 단계 |
| `--no-input-image` | review 대상 입력 이미지 처리 |
| `--no-ssot-fetch` | R1/R3 SSOT corpus link follow |
| `--no-ssot-image` | R1/R3 SSOT corpus image 처리 |

`--no-ssot-fetch`는 입력 URL fetch를 막지 않는다. `--no-input-fetch`는 SSOT corpus link follow를 막지 않는다.

### 7.3 URL 입력 + `--no-input-fetch`

입력이 URL뿐인데 `--no-input-fetch`가 켜져 있으면 review 대상 본문을 만들 수 없다.

출력:

```text
입력 URL fetch가 --no-input-fetch로 봉쇄되어 정책서·기능설계서 본문을 식별할 수 없습니다. 파일/markdown 입력을 주거나 --no-input-fetch를 제거하세요.
```

텍스트·파일·디렉터리 입력에서 본문 자체에 정책서·기능설계서가 이미 있으면 `--no-input-fetch` 상태에서도 review는 진행한다.

## 8. 출력 포맷

### 8.1 헤더 추가

`planning-review` 헤더에 `입력 처리` 줄을 추가한다.

```markdown
# planning-review: [기능명]

- 입력: [경로 list / URL list / "직전 planning-format 출력 (conversation)" / "직접 입력 markdown"]
- 입력 처리: URL root R개 + 입력 fetch 성공 K개 / 실패 J개 + 입력 이미지 M개 (cap 없음)
- 입력 제외 §: 분리 N건 (...)
- 점검 축: [ssot, ac, deps]
- SSOT corpus: 매칭 N개 + 외부 fetch 성공 K개 / 실패 J개 (총 시도 K+J건, cap 없음)
- SSOT 검색 키워드: [keyword1, keyword2, ...]
```

조건:

- conversation 모드에서 직전 `planning-format` 출력을 그대로 쓰고 input fetch가 0건이면 `입력 처리` 줄은 `conversation 본문 사용`으로 표기.
- 파일/디렉터리/raw markdown 본문만 사용하고 fetch/image가 0건이면 `입력 처리: local/raw 본문 사용`.
- input fetch 또는 input image가 1건 이상이면 성공/실패 카운트를 표기.

### 8.2 `## 입력 출처` 블록

input fetch·input image 처리가 1건 이상이면 `## 입력 출처` 블록을 출력한다. 위치는 `## 리뷰 결과` 다음, `## SSOT 출처` 앞이다.

```markdown
## 입력 출처

root 입력: R개
재귀 fetch: 성공 K개 / 실패 J개 (cap 없음)
이미지: 성공 M개 / 실패 L개

| # | 출처 종류 | URL/경로 | origin | 상태 | 본문 사용 |
|---|---|---|---|---|---|
| 1 | 입력 root URL | https://wiki.example/policy/order-cancel | — | 200 (via WebFetch) | O |
| 2 | 입력 root URL | https://docs.example/feature/order-cancel | — | 200 (via Google Drive connector — read_file_content) | O |
| 3 | 입력 자식 URL | https://figma.com/design/... | 입력 출처 2 | 인증 필요 (Figma MCP 미인증) | X |
| 4 | 입력 이미지 | ./diagram.png | 입력 출처 1 | image/png 0.4MB | O (multimodal) |
```

### 8.3 `## SSOT 출처`와의 관계

`## 입력 출처`와 `## SSOT 출처`는 동시에 출력될 수 있다.

출력 순서:

1. `## 리뷰 결과`
2. `## 입력 출처` (조건부)
3. `## SSOT 출처` (조건부)
4. `### SSOT 충돌`
5. `### 검증가능성`
6. `### 영향 분석`

## 9. visited set·cache

### 9.1 input visited set

input fetch는 한 호출 안에서 별도 visited set을 가진다.

- normalize: `connector-routing.md` §6 그대로.
- fragment 제거, trailing `/`, tracking query 제거, host lowercase, query key sort.
- 같은 normalize URL은 input fetch 안에서 1회만 fetch.

### 9.2 SSOT visited set

SSOT corpus link follow는 기존 0.2.2 visited set을 그대로 사용한다.

### 9.3 cross-set dedup

input visited set과 SSOT visited set은 의도적으로 분리한다. 같은 URL이 입력 root와 SSOT corpus link에 동시에 등장하면 두 출처 블록에 각각 나타날 수 있다.

이유:

- input URL은 review 대상 본문이다.
- SSOT URL은 비교 corpus다.
- 두 역할을 합치면 "입력 문서가 자기 자신과 SSOT 비교되는" 오해가 생긴다.

호출 간 cache는 여전히 도입하지 않는다.

## 10. R1/R2/R3 영향

### 10.1 R1 SSOT 충돌

R1은 input collection으로 확보된 정책서·기능설계서 본문을 기존 방식대로 SSOT corpus와 비교한다. 입력 URL source 자체는 SSOT corpus가 아니다.

R1 활성 또는 R3 활성 + SSOT 매칭 ≥1 + `--no-ssot-fetch` off 조건이면 기존 SSOT corpus link follow가 별도로 동작한다.

### 10.2 R2 Acceptance Criteria

R2는 input collection 이후 분리된 정책서·기능설계서 본문만 본다. 입력 fetch가 성공했는지 여부는 R2 기준을 바꾸지 않는다.

### 10.3 R3 의존·영향

R3은 기존처럼 R1 corpus를 공유한다. 입력 제외 § 보조 신호도 기존 0.2.2 규칙을 따른다.

입력 fetch 실패가 `planning-format` 산출물의 `## 입력 제외 항목`에 이미 기록되어 있으면 R3 보조 신호가 된다. 반대로 `planning-review` 입력 fetch 자체의 실패는 review 대상 본문 수집 실패/부분 실패일 뿐, 자동으로 R3 영향 후보가 되지 않는다.

## 11. sanity check

### 11.1 URL root 모두 실패

URL root가 모두 본문 합류 실패하면 review를 종료한다.

```text
모든 review 입력 URL fetch 실패. 첫 번째 사유: <status 또는 error>
```

모든 root가 인증 게이트이고 connector fallback도 실패하면:

```text
모든 review 입력 URL이 로그인 필요로 보입니다. connector/MCP fallback도 인증되지 않았습니다.
필요한 connector: <Atlassian / Figma / Google Drive / Slack / Notion / ...>
```

### 11.2 일부 root 실패

일부 root만 실패하면 종료하지 않는다. `## 입력 출처`에 실패 행을 기록하고, 확보된 본문으로 정책서·기능설계서 분리를 시도한다.

### 11.3 본문 식별 실패

input collection 후 정책서·기능설계서 둘 다 식별하지 못하면:

```text
정책서·기능설계서 두 본문을 식별할 수 없습니다. URL 본문에 # 정책서 / # 기능설계서 헤더를 두거나, 정책서·기능설계서가 구분되는 별도 링크/파일로 주세요.
```

한쪽만 식별하면:

```text
<정책서 또는 기능설계서>가 비어 있습니다. 입력 URL/파일이 planning-format 산출물인지 확인하세요.
```

### 11.4 image-only 입력

이미지 입력만 있고 multimodal 결과에서 정책서·기능설계서를 식별하지 못하면 §11.3 본문 식별 실패 메시지를 사용한다.

## 12. 호환성

| 영역 | 0.2.5 → 0.2.6 |
|---|---|
| `planning-format` 입력·출력 | 동일 |
| `planning-review` 0개 conversation 입력 | 동일 |
| `planning-review` 디렉터리 1개 입력 | 동일 + 본문 URL 추출 가능 |
| `planning-review` 파일 1개 입력 | 동일 + 본문 URL 추출 가능 |
| `planning-review` 파일 2개 입력 | 동일 + 본문 URL 추출 가능 |
| `planning-review` 다중 URL 입력 | 신규 허용 |
| `planning-review` 3개 이상 non-URL 입력 | raw markdown 텍스트 분기. 식별 실패 시 sanity check |
| `--no-ssot-fetch` / `--no-ssot-image` | 동일, SSOT에만 적용 |
| `--no-input-fetch` / `--no-input-image` | 신규 |
| 출력 헤더 | `입력 처리` 줄 추가 |
| 출력 블록 | `## 입력 출처` 조건부 추가 |
| R1/R2/R3 발견 형식 | 동일 |

출력 markdown은 micro-breaking이다. 다운스트림 파서가 `## 리뷰 결과` 바로 다음에 `## SSOT 출처` 또는 발견 sub-section이 온다고 가정하면 `## 입력 출처` 블록을 허용하도록 수정해야 한다.

## 13. 호출 시나리오

1. **정책서·기능설계서가 각각 URL**:
   ```bash
   /planning-kit:planning-review https://wiki/policy https://wiki/feature
   ```
   두 URL fetch → 통합 입력 본문 → 두 본문 분리 → R1/R2/R3 진행.

2. **root URL이 index이고 자식 링크에 산출물 존재**:
   ```bash
   /planning-kit:planning-review https://wiki/order-cancel-index
   ```
   index fetch → 자식 policy/feature URL 발견 → 재귀 fetch → 두 본문 분리.

3. **일부 URL 실패**:
   ```bash
   /planning-kit:planning-review https://wiki/policy https://private/feature
   ```
   policy 성공, feature 인증 실패. feature 본문 식별 실패면 sanity check. `## 입력 출처`에 feature 실패 행 포함.

4. **AC만 점검**:
   ```bash
   /planning-kit:planning-review https://wiki/policy https://wiki/feature --axes ac
   ```
   input fetch는 진행. R1/R3 비활성이므로 SSOT fetch는 진행하지 않음.

5. **입력 fetch 봉쇄**:
   ```bash
   /planning-kit:planning-review https://wiki/policy --no-input-fetch
   ```
   URL만으로는 본문 식별 불가 → sanity check.

6. **SSOT fetch만 봉쇄**:
   ```bash
   /planning-kit:planning-review https://wiki/policy https://wiki/feature --no-ssot-fetch
   ```
   input fetch는 진행. SSOT corpus는 매칭 `*.md` 본문만 사용.

7. **입력 이미지 봉쇄**:
   ```bash
   /planning-kit:planning-review https://wiki/policy --no-input-image
   ```
   URL fetch는 진행. image content-type과 이미지 참조 multimodal은 입력 본문에 합류하지 않음.

8. **텍스트 안 URL**:
   ```bash
   /planning-kit:planning-review "정책서: https://wiki/policy 기능설계서: https://wiki/feature"
   ```
   텍스트 분기지만 본문 URL 추출로 input fetch queue에 시드.

## 14. 대안 검토

| 대안 | 채택 여부 |
|---|---|
| URL 입력만 planning-review에 추가 | 비채택 — 파일/텍스트/디렉터리 본문 URL 추출과 image parity가 깨짐 |
| `planning-format` 입력 dispatch를 문서상 복제 | 비채택 — 룰 drift 위험. 공유 적재/공유 참조로 명시 |
| `--ssot-url`도 함께 도입 | 비채택 — 입력 URL과 SSOT URL 의미가 섞임. 후속 PRD 후보 |
| input visited set과 SSOT visited set 통합 | 비채택 — review 대상과 비교 corpus가 섞임 |
| `--no-fetch` 단일 옵션으로 input+SSOT 모두 봉쇄 | 비채택 — 기존 `--no-ssot-fetch`와 의미 충돌 |
| `--no-input-fetch`만 추가 | 비채택 — 이미지 입력을 끌 수 없어 `planning-format --no-image` parity가 불완전 |
| URL root 모두 실패해도 R1/R2/R3 계속 진행 | 비채택 — review 대상 본문이 없으면 검증 불가 |
| 입력 fetch 실패를 R3 보조 신호로 자동 승격 | 비채택 — `planning-review` 입력 수집 실패와 `planning-format` 입력 제외 § 의미가 다름 |

## 15. 마이그레이션

기존 호출은 그대로 동작한다.

- `/planning-kit:planning-review`
- `/planning-kit:planning-review ./.planning-kit/<기능명>/`
- `/planning-kit:planning-review ./정책서.md ./기능설계서.md`
- `/planning-kit:planning-review "## 정책서 ... ## 기능설계서 ..."`

신규 권장 호출:

```bash
/planning-kit:planning-review <정책서 URL> <기능설계서 URL>
```

다운스트림 파서 수정 필요:

- 헤더 `입력 처리:` 줄 허용.
- `## 입력 출처` 블록 허용.
- `## 입력 출처`와 `## SSOT 출처`를 별개 블록으로 인식.

## 16. 영향 범위

- `skills/planning-review/SKILL.md` — 인자 규칙 확장, input collection 단계 추가, 신규 옵션 `--no-input-fetch` / `--no-input-image`, 출력 헤더·블록 갱신.
- `skills/planning-review/references/ssot-rules.md` — input fetch와 SSOT fetch 분리 설명 보강. 기존 R1 link follow 동작은 유지.
- `skills/planning-format/references/connector-routing.md` — 변경 없음. `planning-review` input fetch에서도 공유 적재한다고 헤더 설명 보강 가능.
- `skills/planning-format/references/conversion-rules.md` — 변경 없음. image multimodal·통합 본문 합류 룰을 `planning-review` input collection에서 참조.
- `docs/planning-review-workflow.md` — 입력 dispatch·input fetch·본문 분리·출처 블록 다이어그램 갱신.
- `README.md` / `planning-kit/README.md` — `planning-review` 다중 URL 입력 예시와 옵션 표 갱신.
- `.claude-plugin/plugin.json` / `.codex-plugin/plugin.json` — version 0.2.5 → 0.2.6, description에 planning-review input parity 추가.
- `docs/prd/README.md` — 0.2.6 row 추가.

## 17. 용어

- **input collection**: `planning-review`가 review 대상 본문을 만들기 위해 입력 URL·파일·디렉터리·텍스트·이미지를 수집하고 통합 본문으로 합류시키는 단계.
- **input fetch**: input collection 안 URL fetch. review 대상 본문 생성용.
- **SSOT fetch**: R1/R3 SSOT corpus link follow. 비교 corpus 확장용.
- **input visited set**: input fetch 전용 visited set.
- **SSOT visited set**: SSOT fetch 전용 visited set.
- **입력 출처**: input collection에서 사용한 root URL, 자식 URL, 이미지, local path 출처 list.

그 외 용어는 0.2.5 §17 / 0.2.4 §13 / 0.2.2 §14 그대로.

## 18. 참고 파일

- `skills/planning-review/SKILL.md` — 본 PRD의 핵심 반영 대상.
- `skills/planning-review/references/ssot-rules.md` — SSOT fetch와 input fetch 경계 설명.
- `skills/planning-format/SKILL.md` — input dispatch·fetch parity 기준.
- `skills/planning-format/references/connector-routing.md` — input fetch·SSOT fetch 공통 connector lookup.
- `skills/planning-format/references/conversion-rules.md` — image multimodal·통합 본문 합류 룰.
- `docs/planning-review-workflow.md` — workflow 다이어그램 갱신 대상.
- `docs/prd/README.md` — PRD chain 갱신 대상.
- `docs/prd/prd-0.2.6.md` — 본 문서.
