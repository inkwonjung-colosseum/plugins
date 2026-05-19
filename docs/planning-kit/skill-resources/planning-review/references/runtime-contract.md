---
name: planning-review
description: "planning-format 산출물(정책서·기능설계서 두 본문)을 외부 기준 문서 묶음 충돌·acceptance criteria 검증가능성·의존 영향 분석 3축으로 점검하고, 결론과 검토 결과를 먼저 출력해야 할 때 사용한다. 직전 turn의 planning-format 본문 출력, 0.2.14 저장 파일 handoff, 디렉터리·파일 경로, 붙여 넣은 Markdown 원문, 1개 이상의 URL 입력을 모두 받는다. 1개 파일 입력은 same-folder companion read로 같은 폴더 sibling 파일을 non-recursive 수집해 정책서·기능설계서 쌍을 식별한다."
argument-hint: "[<URL... | 정책서·기능설계서 경로 | 디렉터리 | 붙여 넣은 Markdown 원문>] [--ssot-include <glob>] [--no-input-fetch] [--no-input-image] [--no-ssot-fetch] [--no-ssot-image]"
---

# planning-review

## 인자

위치 인자:

- **0개** = conversation 참조 모드. 직전 turn의 `planning-format` 출력에서 두 본문 추출.
- **1개 이상이고 모든 비어 있지 않은 토큰이 `^https?://`** = URL 분기. 모든 URL을 depth 0 root input source로 fetch한다. 다중 URL 허용.
- **1개 (디렉터리)** = `정책서*.md` + `기능설계서*.md` 자동 검색. 디렉터리 안 지원 이미지 파일도 input image queue 시드.
- **1개 (파일)** = same-folder companion read. 입력 파일의 parent directory에서 sibling 파일을 non-recursive로 함께 읽고, 정책서·기능설계서 쌍을 식별한다. 이미지 확장자면 input image queue 단독 시드.
- **2개 non-URL path** = `<정책서> <기능설계서>` 또는 역순 (헤더/파일명으로 자동 식별).
- **그 외** = raw markdown 텍스트 분기. URL 토큰과 비-URL 토큰이 섞이면 `planning-format`처럼 텍스트 분기로 본다. 텍스트 안 plain URL은 공통 URL 추출 단계에서 input fetch queue에 시드된다.

`file://` / `ftp://` / `mailto:` / scheme 없는 입력은 URL 분기 아님.

| 인자 | 기본값 | 설명 |
|---|---|---|
| `--ssot-include <glob>` | (없음) | SSOT 표시 폴더 후보 안에서 기준 문서 묶음을 좁히는 glob. 기본 후보는 폴더명에 독립 `SSOT` 표시가 있는 하위 폴더 안의 Markdown만이다. `planning/**`과 `.planning-kit/**`은 항상 제외한다. glob이 SSOT 폴더 경계 밖만 가리키면 결과는 0건이며 상세 추적에 제외 사유를 남긴다. R1·R3가 같은 기준 문서 묶음을 공유한다. |
| `--no-input-fetch` | off | review 대상 입력 수집 단계의 URL root 본문 가져오기 + 본문 URL 가져오기 + 연결 대체 경로 봉쇄. 파일/텍스트/디렉터리 본문 자체는 읽는다. |
| `--no-input-image` | off | review 대상 입력 이미지 multimodal 호출 0건. URL 가져오기는 진행하되 image content-type 응답은 본문 합류하지 않는다. |
| `--no-ssot-fetch` | off (즉 link follow 활성) | 기준 문서 묶음 *.md 본문 안 외부 URL 가져오기 + 연결 대체 경로 봉쇄. 매칭 file 본문만 기준 문서 묶음에 들어간다. |
| `--no-ssot-image` | off (즉 image multimodal 활성) | 기준 문서 묶음 본문 안 이미지 참조·image content-type 응답 multimodal 호출 0건. URL 가져오기는 그대로 (`--no-ssot-fetch`와 독립). |

옵션 범위:

- `--no-input-fetch` / `--no-input-image`는 review 대상 본문을 만드는 input collection에만 적용.
- `--no-ssot-fetch` / `--no-ssot-image`는 R1/R3 기준 문서 외부 링크 처리에만 적용.
- `--no-ssot-fetch`는 입력 URL 가져오기를 막지 않는다. `--no-input-fetch`는 기준 문서 외부 링크 처리를 막지 않는다.

## 동작 시퀀스

### Step 1: 입력 dispatch + input collection + sanity check

토큰/입력 형태에 따라 분기 → input collection → 통합 입력 본문 구성 → 본문 분리 → 빈 본문 검사. 식별 실패 시 sanity check 메시지 출력 후 종료.

#### Step 1.1 입력 dispatch

분기 우선순위:

```
1. 0개                                      → conversation 참조 모드
2. URL 패턴 (1개 이상 토큰, 모두 https?://) → URL 분기
3. 1개 디렉터리 경로                       → 디렉터리 분기
4. 1개 파일 경로                           → 파일 분기 (same-folder companion read, 이미지 확장자면 image queue 단독 시드)
5. 2개 non-URL path                         → 두 파일 분기
6. 그 외                                    → 텍스트 분기
```

#### Step 1.1.1 same-folder companion read (0.2.7)

1개 파일 입력은 해당 파일만 읽는 분기가 아니다. 사용자가 정책서 또는 기능설계서 파일 하나만 지정해도, 같은 폴더 안의 sibling 파일을 함께 읽어 정책서·기능설계서 쌍을 구성한다.

동작 규칙:

1. 입력 파일의 parent directory를 companion scan 범위로 잡는다.
2. scan 범위는 **non-recursive**다. 하위 폴더는 읽지 않는다.
3. 같은 폴더의 모든 읽을 수 있는 UTF-8 텍스트 파일과 planning-kit 지원 이미지 파일을 input collection에 추가한다.
4. 숨김 파일, binary, dependency/build/cache 성격 파일은 읽지 않는다. 판단 기준은 `../planning-format/references/exclusion-rules.md`와 디렉터리 입력의 기본 제외 관례를 따른다.
5. source title/path/H1/본문 헤더로 `정책서`와 `기능설계서` 후보를 식별한다.
6. 입력 파일과 같은 기능명/stem/domain으로 보이는 후보를 우선한다.
7. 후보가 1쌍으로 확정되면 두 본문을 함께 리뷰한다.
8. 같은 폴더에 여러 기능의 정책서·기능설계서가 섞여 있고 1쌍으로 좁힐 수 없으면 임의 병합하지 않고 sanity check로 종료한다.
9. 같은 폴더를 모두 읽었는데도 한쪽 본문만 있으면 기존처럼 한쪽 본문 비어 있음 또는 본문 식별 실패 메시지로 종료한다.

이 변경은 단일 파일 입력의 편의 확장이다. `planning-review`가 새 정책서·기능설계서를 생성하거나, 같은 폴더 밖의 파일을 자동 탐색하거나, 기준 문서 묶음을 review 대상 본문으로 승격하지 않는다.

#### Step 1.1.2 planning-format 저장 산출물 입력 (0.2.9)

`planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 디렉터리를 입력으로 받으면 해당 폴더의 `*정책서*.md`와 `*기능설계서*.md` 파일명을 우선 후보로 인식한다. 파일명으로 확정할 수 없으면 H1/H2의 `정책서`/`기능설계서` heading을 fallback으로 사용한다.

저장 파일 중 하나만 입력받아도 same-folder companion read로 같은 폴더의 짝 파일을 찾아야 한다. 0.2.8 이하 `.planning-kit/**` 저장 산출물은 review 입력으로 계속 읽을 수 있지만, `.planning-kit/**`과 `planning/**`은 모두 기준 문서 근거가 될 수 없다.

#### Step 1.1.3 planning-format 기본 저장 출력 handoff (0.2.14)

0개 인자 conversation 참조 모드에서 직전 `planning-format` 0.2.14 기본 저장 성공 출력에 `## 저장 파일`이 있으면, 그 블록의 path만 handoff 후보로 읽는다.

허용 형식:

- `- 정책서: <path>`
- `- 기능설계서: <path>`
- `- [정책서](<path>)`
- `- [기능설계서](<path>)`

처리 규칙:

1. `## 저장 파일` heading 뒤의 선택적 빈 줄 다음에 나오는 줄 시작 bullet만 인정한다.
2. 정책서 path 1개와 기능설계서 path 1개가 정확히 1개 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 저장 폴더를 가리켜야 한다.
3. 두 파일은 같은 폴더 바로 아래 canonical 파일이어야 한다. 정책서 파일은 `*_정책서.md`, 기능설계서 파일은 `*_기능설계서.md` 형식이다.
4. 파일이 존재하고 읽기 가능하면 두 파일을 review 대상 본문으로 읽는다.
5. 후보가 0개, 2개 이상, 서로 다른 폴더, 파일 없음, 파일명 역할 식별 실패이면 임의 선택하지 않고 sanity check로 종료한다.
6. `## 저장 파일`이 있더라도 `## 정책서`와 `## 기능설계서` 본문이 함께 있으면 본문을 우선한다. 이는 `--no-save` 또는 저장 실패 fallback의 결과 손실 방지 경로다.
7. 직전 출력의 `## 체크해야 할 항목`, `## 출처/누락 요약`, `## 상세 추적`, `## 저장 실패 상세`는 review 대상 본문에 합류하지 않는다.
8. `planning/**`은 계속 기준 문서 묶음 근거에서 제외한다. 저장 파일은 review 대상 입력이지 SSOT 근거가 아니다.
9. 임의 텍스트 안 경로, 여러 후보 경로, 최근 폴더 자동 선택은 하지 않는다.

#### Step 1.2 input collection (0.2.6)

`planning-format` Step 1~5와 같은 URL 판별, URL·이미지 추출, 재귀 fetch, connector fallback, image multimodal, 통합 본문 합류 룰을 사용한다.

- URL 분기의 모든 URL은 depth 0 root input source다.
- 모든 분기 공통으로 본문에서 markdown link/autolink, HTML `href`/`src`/`img`, plain URL, markdown image, data URI를 추출한다. self-anchor·`mailto:`/`tel:`/`javascript:`/`blob:`·non-http scheme은 제외.
- input fetch queue는 `planning-format` 0.2.5 결정성 룰을 따른다: push 시점 normalize, depth BFS, 같은 depth 안 markdown link → HTML href/src → plain URL 발견 순서, dequeue된 visited 미포함 URL은 100% fetch 시도, 실패도 visited 등록 + 출처 행 기록.
- depth·pages·body·fanout cap은 두지 않는다. cycle·중복은 input visited set으로만 막는다.
- fetch 진입 직전 `../planning-format/references/connector-routing.md`를 1회 Read 적재한다. 1차 WebFetch + connector fallback·인증 휴리스틱·MCP 카탈로그·Google Workspace tool 시퀀스·gid/range·status 표기를 그대로 공유한다.
- input visited set은 기준 문서 visited set과 별도다. 같은 URL이 input source와 기준 문서 link에 동시에 등장해도 `## 입력 출처`와 `## 기준 문서 출처`에 각각 나타날 수 있다.
- `--no-input-fetch` ON이면 input fetch queue 전체를 봉쇄한다. 입력이 URL뿐이면 review 대상 본문을 만들 수 없으므로 sanity check 메시지를 출력한다.
- input image queue는 5경로(이미지 파일 인자, 디렉터리 이미지, markdown image/HTML img, fetch `image/*`, inline data URI)를 따른다. `--no-input-image` ON이면 image multimodal 0건이며 image content-type 응답은 본문 합류하지 않는다.
- fetch·image 처리가 1건 이상이면 `## 입력 출처` 블록에 root URL, 자식 URL, 입력 이미지 행을 모두 기록한다. 실패 행도 포함한다.
- fetch·image 처리가 끝나면 source 단위 헤더로 concat한다.
- 1개 파일 입력의 companion read에서 추가된 sibling 텍스트/이미지도 source 단위 헤더로 concat한다. 입력 파일은 source 우선순위 1순위이며, 같은 기능명/stem/domain sibling만 정책서·기능설계서 후보로 우선한다.

```markdown
=== [입력 출처 1] URL: https://wiki.example/policy/order-cancel ===
...

=== [입력 출처 2] URL: https://docs.example/feature/order-cancel ===
...
```

Google Sheets gid/range, connector deep link anchor, metadata only 상태 등은 `planning-format`과 동일하게 부연한다.

#### Step 1.3 본문 분리

통합 입력 본문에서 정책서·기능설계서·입력 제외 섹션을 분리한다.

1. `## 저장 파일`만 있고 `## 정책서`와 `## 기능설계서` 본문이 없으면 Step 1.1.3 저장 파일 handoff를 먼저 시도한다.
2. 저장 경로가 있더라도 `## 정책서`와 `## 기능설계서` 본문이 함께 있으면 본문을 우선한다.
3. 0.2.10~0.2.13 unsaved 화면 출력은 readable projection으로 취급한다. legacy 상단 metadata heading은 report metadata이며 정책서·기능설계서 본문이 아니다.
4. wrapper heading은 줄 시작의 정확한 H2만 인정한다. CRLF는 LF로 정규화하고, 파일 첫 BOM은 무시하며, trailing whitespace는 제거한다. leading space, closing hash, H3 이하 heading은 wrapper로 인정하지 않는다.
5. backtick/tilde fenced code block 안, blockquote 안, 리스트 하위의 wrapper 문자열은 wrapper heading으로 보지 않는다. 닫히지 않은 fenced code block이 있으면 이후 heading은 wrapper로 인정하지 않고 `readable projection boundary ambiguous` warning을 남긴다.
6. legacy metadata heading이 같은 metadata 영역에 중복되거나 정상 위치 밖에 나타나면 해당 line부터 다음 인정된 wrapper H2 직전 또는 EOF까지 body에서 제외하고 warning 문자열은 정확히 `readable projection boundary ambiguous`로 남긴다.
7. 정책서 본문은 첫 `## 정책서` wrapper heading 다음 줄에서 시작한다.
8. 기능설계서 본문은 첫 `## 기능설계서` wrapper heading 다음 줄에서 시작한다.
9. 정책서·기능설계서 본문 종료 경계는 다음 wrapper heading 중 먼저 등장하는 항목이다: `## 기능설계서`, `## 저장 파일`, `## 체크해야 할 항목`, `## 출처/누락 요약`, `## 출처 요약`, `## 입력 제외 요약`, `## 상세 추적`, `## 저장 실패 상세`, `## 결론`, `## 검토 결과`, legacy review/report heading, EOF.
11. 경계가 둘 이상으로 해석되거나 한쪽 본문을 확정할 수 없으면 임의 병합하지 않고 `검증 범위와 한계` 또는 sanity check에 `readable projection boundary ambiguous`를 남긴다.
12. `# 정책서` / `## 정책서` 헤더 → 정책서 본문, `# 기능설계서` / `## 기능설계서` 헤더 → 기능설계서 본문. 0.2.8 이하 코드 펜스 안 헤더도 읽기 호환으로 반복 처리한다.
13. `## 입력 제외 항목` 또는 0.2.9 `## 입력 제외 요약`/`## 상세 추적` 안의 입력 제외 항목을 입력 제외 섹션 본문으로 분리한다. 부재해도 sanity check 아님.
14. source title/path/URL label이 `정책서`, `policy`, `정책`, `기능설계서`, `feature`, `design`, `spec` 중 하나를 명확히 가리키면 source 단위 fallback 배정.
15. 1개 파일 입력의 companion read source는 title/path/H1/본문 헤더와 입력 파일의 기능명/stem/domain 유사도로 후보를 좁힌다.
16. 위 절차 후 정책서·기능설계서 둘 다 확보하지 못하면 sanity check.

위치 parser는 legacy 입력 `정책서 §5.1`, `기능설계서 §7`, `§5.1 보조 표`, `sub-§`, `입력 제외 §`를 각각 clean display 위치와 같은 section id로 normalize한다. 내부 matching에는 숫자 chain을 써도 되지만, 사용자에게 다시 출력할 때는 `정책서 5.1`, `기능설계서 7`, `5.1 보조 표`, `보조 표`, `입력 제외 섹션`으로 렌더링한다.

source 단위 fallback은 명확한 1:1 신호일 때만 사용한다. 두 source가 모두 같은 종류로 추정되거나 둘 다 불명확하면 fallback하지 않는다.
companion read에서 여러 기능의 정책서·기능설계서 후보가 섞여 있고 입력 파일 기준으로 1쌍을 확정할 수 없으면 fallback하지 않고 sanity check로 종료한다.

분리 결과는 메모리에만. 세 검토 축의 실행 여부와 무관하게 분리 단계는 항상 시도한다.

| 케이스 | 메시지 |
|---|---|
| conversation 모드 + 직전 planning-format 출력 없음 | `직전 turn에서 planning-format 출력을 찾을 수 없습니다. 경로 또는 markdown을 인자로 주세요.` |
| URL 입력 + `--no-input-fetch` | `입력 URL fetch가 --no-input-fetch로 봉쇄되어 정책서·기능설계서 본문을 식별할 수 없습니다. 파일/markdown 입력을 주거나 --no-input-fetch를 제거하세요.` |
| URL root 모두 본문 합류 실패 | `모든 review 입력 URL fetch 실패. 첫 번째 사유: <status 또는 error>` |
| URL root 모두 인증 게이트 + fallback 실패 | `모든 review 입력 URL이 로그인 필요로 보입니다. connector/MCP fallback도 인증되지 않았습니다.` + `필요한 connector: <Atlassian / Figma / Google Drive / Slack / Notion / ...>` |
| 단일 파일 companion read 후보 모호 | `같은 폴더에서 정책서·기능설계서 1쌍을 확정할 수 없습니다. 리뷰할 두 파일을 명시하거나 기능별 폴더로 분리하세요.` |
| 본문 식별 실패 | `정책서·기능설계서 두 본문을 식별할 수 없습니다. URL 본문에 # 정책서 / # 기능설계서 헤더를 두거나, 정책서·기능설계서가 구분되는 별도 링크/파일로 주세요.` |
| 한쪽 본문 비어 있음 | `<정책서 또는 기능설계서>가 비어 있습니다. 입력 URL/파일이 planning-format 산출물인지 확인하세요.` |
### Step 2: 검증 축 점검

SSOT 충돌, acceptance criteria 검증가능성, 의존·영향 분석을 main 단일 패스로 함께 실행한다. 축별 reference는 필요한 순간 적재하되 public 출력은 하나의 리뷰 결과로 합친다. 축 단위 부분 리뷰 옵션은 공개 계약이 아니다.

**보조 표 인식 (0.2.4)**: R1·R2·R3 모두 산출물 상위 섹션 + 보조 표(`### N.M ... 보조 표`) 본문을 함께 점검 대상으로 본다. 절차 detail은 각 reference 그대로 — 상위 섹션 룰을 보조 표 본문에 자연 확장.

| 축 | 키 | 적재 reference | 발견 sub-category |
|---|---|---|---|
| R1. SSOT 충돌 | `ssot` | `references/ssot-rules.md` | (단일) |
| R2. Acceptance Criteria 검증가능성 | `ac` | `references/ac-rules.md` | 정량성 / 상태 / 행위자 / 결과 관찰 |
| R3. 의존·영향 분석 | `deps` | `references/deps-rules.md` | 정책 변경 / 상태 전이 / 권한·역할 / 외부 의존 (발견·권고 분류) |

R1·R3 corpus 공유 (`--ssot-include`). R2는 input collection 이후 분리된 본문 자체만 본다.

#### R1 link follow (0.2.2)

R1 활성 OR R3 활성 + 매칭 ≥1 + `--no-ssot-fetch` off → 매칭 *.md 본문 안 URL·이미지를 fetch + connector fallback으로 corpus body에 합류. 절차·visited set·sanity check·출처 list 형식 모두 `references/ssot-rules.md` R1.4·R1.5. connector lookup은 `../planning-format/references/connector-routing.md` 공유 적재. `--no-ssot-image` ON이면 image content-type 합류 skip (URL fetch는 별도).

입력 URL source 자체는 기준 문서 묶음이 아니다. input fetch는 review 대상 본문 생성용이고, 기준 문서 외부 링크 처리는 비교 근거 확장용이다.

#### R3 입력 제외 섹션 보조 신호 (0.2.2)

R3 활성 + Step 1 분리 성공 시 카테고리별 가중치. 절차·신호 카테고리·헤더 카운트 K 산출 모두 `references/deps-rules.md` R3.2.1.

### Step 3: 발견 합산 + 우선순위/작업화

같은 발견이 두 축에 걸치면 한 번만 기록. 축 중복 제거 우선순위: **R1 > R3 > R2**.

발견은 기본 출력 전에 P0/P1/P2로 재정렬한다.

| 우선순위 | 의미 | 기본 매핑 |
|---|---|---|
| P0 | 구현/운영 판정을 결정할 수 없어 기능 동작이 비결정적 | R1 또는 R2의 핵심 결정 불가, R3 외부 영향 중 운영 차단 |
| P1 | 정책/기능 문서 간 범위 충돌 또는 외부 시스템 영향이 큼 | R1 충돌, R2 검증 불가, R3 발견 |
| P2 | 후속 SSOT 보강, cross-link, 변경 워크플로 권고 | R3 권고, SSOT 보강 작업 |

수정 작업은 발견을 그대로 나열하기 전에 작업 단위로 묶는다. 항목 ID는 `A1`, `A2` 형식이다. 외부 결정 필요 항목은 `D*`, 독립 출시 전 해결 필요 추적은 `T*`, 원시 발견은 `R*`로 분리한다.

| 유형 | 설명 |
|---|---|
| `문서 수정` | 정책서·기능설계서 본문을 직접 고쳐야 함 |
| `정책 결정` | 담당자/도메인 owner가 값을 결정해야 함 |
| `SSOT 보강` | 본문 없는 문서 또는 부재한 기준 문서를 작성/보강해야 함 |
| `외부 인터페이스` | WCS/API/시트 등 외부 의존 계약을 명시해야 함 |
| `동기화 워크플로` | 시트·정책서·기능설계서 동시 갱신 절차가 필요함 |

모든 기본 발견 ID는 `R1-1`, `R2-1`, `R3-1` 형식이다. 같은 출력 안에서만 stable하면 된다.

#### Step 3.1 체크리스트 항목화 (0.2.14)

`planning-review`는 발견을 먼저 결론과 검토 결과로 요약하고, 미확정·누락·보강점은 마지막 `## 체크해야 할 항목`에 모은다. 신규 public 출력에서 상단 실행 projection heading은 출력하지 않는다.

ID 의미:

| ID | 의미 |
|---|---|
| `D*` | 사용자/PM/현업/기획/운영 등 권한 있는 주체가 결정해야 하는 항목 |
| `R*` | 검증 finding 원본 (`R1-*`, `R2-*`, `R3-*`) |
| `A*` | 수정 작업 |
| `T*` | 독립적으로 추적해야 하는 출시 전 해결 필요 항목 |

규칙:

- `D*`는 권한 있는 주체의 판단이 필요한 항목에만 만든다. P0/P1이라도 문서 수정만으로 해소되는 경우에는 `D*` 없이 `A*`로 표시한다.
- `D*`는 `확인할 것`, `선택지`, `초안 추천(확정 필요)`, `반영 위치`, `연결`을 보존한다. 특정 승인 주체가 원문에 명시된 경우만 `승인/확인 주체`를 추가한다.
- `A*` 상세 record는 `ID`, `연결`, `유형`, `의존성`, `대상`, `작업`, `완료 조건`, `검증 방법`, `상태`를 보존한다. 담당 추정은 하지 않는다.
- `T*`는 `위치`, `차단 이유`, `해소 조건`, `연결`을 보존한다. 차단 사유가 D*/A*에 충분히 표시되면 별도 T*를 반복하지 않고 관련 checklist 항목의 `이유`에 `[출시 전 해결 필요]`를 남긴다.
- D*/A*/T* ID는 prefix별로 1부터 연속 부여한다. 같은 prefix와 같은 우선순위 안에서는 P0/P1, 출시 전 해결 필요 여부, 입력 등장 순서, 연결 finding ID 순서로 정렬한다.
- 기본 `## 검토 결과`와 checklist에서는 원시 R* ID를 직접 나열하지 않고, 필요하면 `관련 발견 N건 (상세 추적의 체크리스트 연결 맵 참조)`처럼 접는다. 원시 R* ID는 `## 상세 추적`에 유지한다.
- 결정 항목은 최대 3개, 작업 항목은 최대 5개까지만 펼친다. 초과분은 `그 외 N건은 상세 추적 참조`로 압축한다.
- 추천안이 정책 결정을 포함하면 필드명을 `초안 추천(확정 필요)`로 쓰고, 사용자 승인 전 정책서·기능설계서 canonical 본문에 확정값처럼 반영하지 않는다.

병합:

- 같은 문서 위치 또는 같은 정책/기능 개념, 같은 미정 계약/충돌 값/관찰 불가 조건, 같은 결정 또는 같은 문서 수정으로 해소되는 finding은 하나의 D* 또는 A*로 묶는다.
- `R2-*` 검증가능성과 `R3-*` 영향 분석이 같은 외부 인터페이스 계약 부재에서 비롯되면 하나의 D*/A*로 표시한다.
- `R1-*` SSOT 충돌과 `R3-*` 영향 분석이 같은 기준 문서 변경으로 해소되면 하나의 D*/A*로 표시한다.
- 여러 P2 동기화 권고가 같은 운영 워크플로로 해소되면 하나의 A*로 묶는다.
- 서로 다른 승인/확인 주체, 서로 다른 반영 위치, 서로 다른 완료 조건 중 하나 이상을 가진 finding은 병합하지 않는다.

특수 상황:

- P2-only review에서 출시 전 해결 필요 항목이 없으면 결론은 `검토 필요` 또는 `조건부 통과`로 두고, P2 작업은 `## 검토 결과`와 `## 체크해야 할 항목 > 문서 보강 필요`에 압축한다.
- `검증 신뢰도: 낮음`의 원인이 기준 문서 묶음 0건 또는 모두 본문 없는 문서뿐이고 R2/R3 finding이 없으면 D*를 만들지 않는다. SSOT 보강 A*는 `## 체크해야 할 항목 > 문서 보강 필요`에만 표시하고 판정은 `비교 불가`를 유지한다.
- 기준 문서 묶음이 없어 SSOT 비교가 불가능하면 SSOT 보강 작업은 `## 체크해야 할 항목`에만 표시하고, R2/R3 판단과 섞어 충돌 발견처럼 보이지 않게 한다.
- 0.2.14 신규 public 출력에서는 legacy top-level backlog summary를 만들지 않는다.

### Step 4: 판정과 검증 신뢰도

검증 신뢰도:

| 신뢰도 | 조건 |
|---|---|
| `충분` | review 대상 본문이 충분하고, 활성 축에 필요한 비교 대상/증거가 실질 본문을 포함하며, 활성 축을 정상 평가했다. |
| `제한적` | review 대상 본문은 충분하고 활성 축을 평가했지만 일부 기준 문서가 본문 없는 문서이거나 특정 외부 link follow가 실패해 증거 범위가 일부 제한된다. |
| `낮음` | 활성 핵심 축을 평가할 비교 대상 대부분이 비어 있거나, 입력 fetch 실패로 review 대상 본문 일부만 확보했다. `ssot` 축 활성 + 기준 문서 묶음 0건 또는 모두 본문 없는 문서이면 `낮음`. |

판정 우선순위:

1. `수정 필요`: P0 또는 P1 발견이 1건 이상 있다.
2. `비교 불가`: 핵심 비교 근거가 증거 부족으로 판단 불가다. 예: 기준 문서 묶음이 모두 본문 없는 문서이고 R2/R3에서도 판단 가능한 발견이 없다.
3. `검토 필요`: P0/P1은 없고, 핵심 축이 판단 가능하며, P2 권고가 있거나 외부 결정이 필요한 항목이 있다.
4. `조건부 통과`: P0/P1/P2 발견이 없고, 활성 축은 평가됐지만 검증 신뢰도가 `제한적`이다.
5. `통과`: P0/P1/P2 발견이 없고, 검증 신뢰도가 `충분`이다.

신뢰도는 통합 리뷰 전체 기준으로 판단한다. 기준 문서 묶음 부재는 신뢰도를 낮출 수 있지만, R2/R3에서 실질 발견이 있으면 그 발견을 판정에 반영한다. `낮음`이고 P0/P1/P2 발견이 0건이면 최종 판정은 `비교 불가`다. `낮음`이더라도 P0/P1 발견이 있으면 `수정 필요`다.

## 출력 포맷

````markdown
# [기능명] 검토 결과

- 판정: [통과 / 조건부 통과 / 수정 필요 / 검토 필요 / 비교 불가]
- 검증 신뢰도: [충분 / 제한적 / 낮음] — [이유]
- 입력: [사람이 읽는 요약]
- 점검 축: [활성 축만 한국어로 표시. 예: 기준 문서 일치성, 검증가능성, 영향 분석]
- 발견: P0 N건, P1 N건, P2 N건

---

## 결론

[1~3문장 bottom line]

---

## 검토 결과

[우선순위별 발견 요약. P0/P1/P2가 있으면 원인, 영향, 반영 위치를 사람이 읽는 문장으로 압축]

---

## 체크해야 할 항목

### 결정 필요

[없음 또는 결정 항목]

### 문서 보강 필요

[없음 또는 문서 보강 항목]

### 출처/누락 참고

[없음 또는 근거 한계]

---

## 검토 근거 요약

[근거 부족, 비활성 축, 입력/기준 문서 출처 압축]

## 상세 추적

[조건 충족 시 full 입력 출처표 / full 기준 문서 출처표 / 축별 원시 발견 목록 / 체크리스트 연결 맵]
````

규칙:

- 최종 출력은 반드시 `# [기능명] 검토 결과`로 시작한다.
- 최종 출력 앞에 fetch 진행 문장, project scan 진행 문장, "분석 결과를 정리합니다" 같은 로그를 쓰지 않는다.
- 전체 리포트를 ` ```markdown ` 또는 ` ```text ` 코드 펜스로 감싸지 않는다.
- 출력 라벨은 `검증 신뢰도`를 유지한다. `검토 근거 수준`은 입력 alias나 향후 표현 후보로만 허용하며, parser는 두 라벨을 같은 metadata field로 normalize할 수 있어야 한다.
- 헤더 요약 다음에는 항상 `## 결론`이 온다. 그 다음 `## 검토 결과`가 온다.
- `## 결론`은 발견 상세보다 먼저 온다.
- `## 검토 결과`는 우선순위별 발견과 영향, 반영 위치를 압축한다.
- `## 체크해야 할 항목`은 `결정 필요`, `문서 보강 필요`, `출처/누락 참고` subsection을 기본으로 한다.
- 항목이 없는 checklist subsection은 `없음`으로 표시한다.
- checklist 항목 제목은 `결정 필요 1`, `문서 보강 필요 1`, `출시 전 해결 필요 1`처럼 자연어 라벨을 먼저 쓴다.
- `결정 필요자`는 출력하지 않는다. 특정 승인 주체가 원문에 명시된 경우에만 `승인/확인 주체`를 쓴다.
- `## 검토 근거 요약`은 근거 부족, 비활성 축, 입력/기준 문서 출처를 압축한다.
- full 입력 출처표, full SSOT 출처표, 축별 원시 발견 목록은 조건 충족 시 하단 `## 상세 추적` 섹션으로 이동한다.
- `## 상세 추적`은 조건 충족 시 `## 검토 근거 요약` 뒤에 둔다.
- `## 상세 추적` 내부에서 `### 체크리스트 연결 맵`은 축별 원시 발견 목록과 입력/기준 문서 출처표보다 먼저 둔다.
- R3 발견·권고 항목이 입력 제외 섹션 보조 신호로 만들어진 경우 `근거` 줄에 입력 제외 섹션 cross-reference 표시.
- 상단 결과 영역에는 connector 세부 status, full source URL table, full 기준 문서 표, 원시 finding 전문을 출력하지 않는다.
- 상단 결과 영역에는 `SSOT corpus`, `fetch`, `deps`, `AC Blocker`를 단독 표기로 쓰지 않고, 각각 `기준 문서 묶음`, `본문 가져오기`, `영향 분석`, `구현/QA 차단`으로 표시한다.
- checklist는 카드/필드 목록을 기본으로 한다. Markdown 표는 5열 이하이고 모든 표시 문자열 셀이 60자 이하일 때만 쓴다. 60자는 link URL, backtick, 강조 기호를 제거한 표시 문자열 기준이다.
- 카드/필드 목록으로 분해할 때 필드명과 값은 보존한다.
- 0.2.11부터 최종 사용자 출력은 clean display를 사용한다. 섹션 기호를 출력하지 말고 `정책서 5.1`, `기능설계서 7`, `입력 제외 섹션`, `보조 표`처럼 사람이 읽는 위치 표기로 쓴다. 이 규칙은 결론, 검토 결과, 체크리스트, 검토 근거 요약, 상세 추적, 축별 원시 발견 목록 모두에 적용한다. 원문 직접 인용 안에 기호가 포함된 경우만 예외다.

### 최종 clean-display 정규화

최종 응답을 제출하기 직전에 전체 사용자-facing 출력(헤더 요약, 결론, 검토 결과, 체크리스트, 검토 근거 요약, 상세 추적)을 한 번 더 스캔한다. 원문 직접 인용 안에 실제로 들어 있는 문자를 제외하고 아래 legacy/내부 표현이 남아 있으면 반드시 치환한 뒤 응답한다.

| 남기면 안 되는 표현 | 최종 출력 표현 |
|---|---|
| `정책서 §6`, `정책서 §6·§9` | `정책서 6`, `정책서 6, 9` |
| `기능설계서 §5`, `기능설계서 §5.2~5.4` | `기능설계서 5`, `기능설계서 5.2~5.4` |
| `§10 참조`, `§5.1 보조 표` | `10 참조`, `5.1 보조 표` |
| `입력 제외 §`, `sub-§`, `부모 §` | `입력 제외 섹션`, `보조 표`, `상위 섹션` |
| `릴리즈 차단` | `출시 전 해결 필요` 또는 문맥상 `구현/QA 차단` |
| `SSOT corpus`, `SSOT token 폴더` | `기준 문서 묶음`, `SSOT 표시 폴더` |
| `SSOT 출처`, `SSOT Markdown`, `SSOT 외부 링크` | `기준 문서 출처`, `기준 문서 Markdown`, `기준 문서 외부 링크` |
| `placeholder`, `all-placeholder` | `본문 없는 문서`, `모두 본문 없는 문서` |
| `fetch`, `connector fallback`, `raw markdown` | `본문 가져오기`, `연결 대체 경로`, `붙여 넣은 Markdown 원문` |

검문 기준:

- `§`가 인용 밖에 1개라도 남으면 출력하지 않는다.
- 첫 화면 요약과 항목 제목은 `오늘 결정: D1`, `바로 수정: A1`, `P0 1건`처럼 원시 ID/등급을 먼저 쓰지 않는다.
- `## 상세 추적` 안에서도 같은 정규화를 적용한다. 상세 추적은 내부 로그가 아니라 사용자가 검토하는 감사 trail이다.
- 내부 reference의 legacy 호환 설명을 근거로 최종 출력에 legacy 표기를 재노출하지 않는다.

### 상세 추적 조건

| 조건 | 처리 |
|---|---|
| P0/P1 발견이 1건 이상 | 축별 원시 발견 목록 포함 |
| D*/A*/T*가 원시 R*를 접어 표시함 | `### 체크리스트 연결 맵` 포함 |
| 기준 문서 묶음이 0건이거나 모두 본문 없는 문서 | 기준 문서 후보/제외/본문 없는 문서 경로 요약 포함, 기본 상단 `검증 범위와 한계`에도 원인 표시 |
| `--ssot-include`가 SSOT 폴더 경계 밖만 가리켜 후보가 0건 | include glob, 제외 사유, 경계 밖 매칭 수 포함 |
| input fetch 실패, 인증 실패, 본문 미사용 출처가 1건 이상 | full 입력 출처표 포함 |
| 기준 문서 외부 링크 처리 실패, 인증 실패, 본문 미사용 출처가 1건 이상 | full 기준 문서 출처표 포함 |

### 검토 근거 요약

```markdown
## 검토 근거 요약

| 구분 | 건수 | 성공 | 실패 | 본문 사용 | 비고 |
|---|---:|---:|---:|---:|---|
| 입력 URL | 2 | 2 | 0 | 2 | 정책서, 기능설계서 |
| 입력 이미지 | 0 | 0 | 0 | 0 | 없음 |
| 기준 문서 Markdown | 6 | 6 | 0 | 0 | 모두 본문 없는 문서 |
| 기준 문서 외부 링크 | 0 | 0 | 0 | 0 | 링크 없음 |
```

connector 세부(`via Atlassian connector`)는 기본 출력에서 숨긴다. 실패나 인증 문제만 `비고`에 짧게 남긴다.

### 상세 입력 출처

입력 URL 가져오기 또는 input image 처리 1건 이상이고 상세 추적 조건을 충족할 때만 `## 상세 추적` 안에 둔다.

```markdown
### 입력 출처

root 입력: R개
재귀 본문 가져오기: 성공 K개 / 실패 J개 (cap 없음)
이미지: 성공 M개 / 실패 L개

| # | 출처 종류 | URL/경로 | origin | 상태 | 본문 사용 |
|---|---|---|---|---|---|
| 1 | 입력 root URL | https://wiki.example/policy/order-cancel | — | 200 (via WebFetch) | O |
| 2 | 입력 root URL | https://docs.example/feature/order-cancel | — | 200 (via Google Drive connector — read_file_content) | O |
| 3 | 입력 자식 URL | https://figma.com/design/... | 입력 출처 2 | 인증 필요 (Figma MCP 미인증) | X |
```

### 상세 기준 문서 출처

link follow 1건 이상이거나 기준 문서 0건/모두 본문 없는 문서/경계 밖 include 조건을 충족할 때 `## 상세 추적` 안에 둔다. 표 형식은 `references/ssot-rules.md` R1.5를 따른다.

### 체크리스트 연결 맵

D*/A*/T*가 원시 R*를 접어 표시하면 `## 상세 추적` 안에 사람이 읽을 수 있는 mapping을 보존한다.

```markdown
### 체크리스트 연결 맵

- D1 -> R2-1, R3-1
- A1 -> D1, R2-1, R3-1
- A2 -> R2-2
```

상단 결과와 체크리스트에는 원시 R* ID를 직접 노출하지 않는다. 원시 ID와 축/우선순위/제목은 아래 축별 원시 발견 목록에서 확인 가능해야 한다.

### 축별 원시 발견 목록

```markdown
### SSOT 충돌
1. [제목]
   - 위치: [정책서 5.1] vs [SSOT 파일 2]
   - 근거: "[변환 본문 인용]" vs "[SSOT 인용]"
   - 영향: [한 줄]
   - 제안: [최소 수정 또는 확인 조건]

### 검증가능성
1. [제목]
   - 카테고리: [정량성 / 상태 / 행위자 / 결과 관찰]
   - 우선순위: [P0 / P1]
   - 위치: [정책서 6 / 기능설계서 5]
   - 근거: "[변환 본문 인용]"
   - 영향: [한 줄]
   - 제안: [최소 수정]

### 영향 분석
1. [제목]
   - 분류: [발견 / 권고]
   - 우선순위: [P1 / P2]
   - 카테고리: [정책 변경 / 상태 전이 / 권한·역할 / 외부 의존]
   - 위치: [정책서 5.1]
   - 영향 후보: [SSOT 파일 path list]
   - 근거: "[변환 본문 인용]" + (선택) "[SSOT 인용 또는 입력 제외 섹션 cross-reference]"
   - 영향: [한 줄]
   - 제안: [후속 검토 조건]
```

## 참고 파일

- `references/ssot-rules.md` — R1 SSOT 충돌 점검 절차·`SSOT` 표시 폴더 기준 문서 경계·본문 없는 문서 판정·link follow·출처 list.
- `references/ac-rules.md` — R2 4 sub-category 기준 + P0/P1 우선순위 기본값.
- `references/deps-rules.md` — R3 4 sub-category 기준 + 발견/권고 P1/P2 기본값 + 입력 제외 섹션 보조 신호 + backlog grouping 신호.
- `../planning-format/references/connector-routing.md` — input fetch와 기준 문서 link follow에서 공유 적재. 인증 게이트 휴리스틱·MCP 카탈로그·호스트 매핑·Google Workspace tool 시퀀스·gid/range·연결 대체 경로·status 표기.
- `../planning-format/references/conversion-rules.md` — input image multimodal·통합 본문 합류 룰을 공유 참조.

변환·자체 품질 점검·`--save`는 `planning-format` 스킬에서 별도 처리. 자세한 절차는 `skills/planning-format/SKILL.md`.
