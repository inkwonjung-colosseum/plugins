---
name: planning-review
description: "planning-format 산출물(정책서·기능설계서 두 본문)을 외부 SSOT corpus 충돌·acceptance criteria 검증가능성·의존 영향 분석 3축으로 점검할 때 사용한다. 직전 turn의 planning-format 출력, 디렉터리·파일 경로, raw markdown 텍스트, 1개 이상의 URL 입력을 모두 받는다. 1개 파일 입력은 same-folder companion read로 같은 폴더 sibling 파일을 non-recursive 수집해 정책서·기능설계서 쌍을 식별한다."
argument-hint: "[<URL... | 정책서·기능설계서 경로 | 디렉터리 | raw markdown>] [--ssot-include <glob>] [--axes <list>] [--no-input-fetch] [--no-input-image] [--no-ssot-fetch] [--no-ssot-image]"
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
| `--ssot-include <glob>` | (없음) | SSOT token 폴더 후보 안에서 corpus를 좁히는 glob. 기본 후보는 폴더명에 독립 `SSOT` token이 있는 하위 폴더 안의 Markdown만이다. `planning/**`과 `.planning-kit/**`은 항상 제외한다. glob이 SSOT 폴더 경계 밖만 가리키면 결과는 0건이며 상세 추적에 제외 사유를 남긴다. R1·R3 corpus 공유. |
| `--axes <list>` | `ssot,ac,deps` | 점검 축 콤마 구분. 빈 값이면 sanity check. |
| `--no-input-fetch` | off | review 대상 입력 수집 단계의 URL root fetch + 본문 URL fetch + connector fallback 봉쇄. 파일/텍스트/디렉터리 본문 자체는 읽는다. |
| `--no-input-image` | off | review 대상 입력 이미지 multimodal 호출 0건. URL fetch는 진행하되 image content-type 응답은 본문 합류하지 않는다. |
| `--no-ssot-fetch` | off (즉 link follow 활성) | SSOT corpus *.md 본문 안 외부 URL fetch + connector fallback 봉쇄. 매칭 file 본문만 corpus에 들어간다. |
| `--no-ssot-image` | off (즉 image multimodal 활성) | SSOT corpus 본문 안 이미지 참조·fetch image content-type 응답 multimodal 호출 0건. URL fetch는 그대로 (`--no-ssot-fetch`와 독립). |

옵션 범위:

- `--no-input-fetch` / `--no-input-image`는 review 대상 본문을 만드는 input collection에만 적용.
- `--no-ssot-fetch` / `--no-ssot-image`는 R1/R3 SSOT corpus link follow에만 적용.
- `--no-ssot-fetch`는 입력 URL fetch를 막지 않는다. `--no-input-fetch`는 SSOT corpus link follow를 막지 않는다.

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

이 변경은 단일 파일 입력의 편의 확장이다. `planning-review`가 새 정책서·기능설계서를 생성하거나, 같은 폴더 밖의 파일을 자동 탐색하거나, SSOT corpus를 review 대상 본문으로 승격하지 않는다.

#### Step 1.1.2 planning-format 저장 산출물 입력 (0.2.9)

`planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 디렉터리를 입력으로 받으면 해당 폴더의 `*정책서*.md`와 `*기능설계서*.md` 파일명을 우선 후보로 인식한다. 파일명으로 확정할 수 없으면 H1/H2의 `정책서`/`기능설계서` heading을 fallback으로 사용한다.

저장 파일 중 하나만 입력받아도 same-folder companion read로 같은 폴더의 짝 파일을 찾아야 한다. 0.2.8 이하 `.planning-kit/**` 저장 산출물은 review 입력으로 계속 읽을 수 있지만, `.planning-kit/**`과 `planning/**`은 모두 SSOT corpus 근거가 될 수 없다.

#### Step 1.2 input collection (0.2.6)

`planning-format` Step 1~5와 같은 URL 판별, URL·이미지 추출, 재귀 fetch, connector fallback, image multimodal, 통합 본문 합류 룰을 사용한다.

- URL 분기의 모든 URL은 depth 0 root input source다.
- 모든 분기 공통으로 본문에서 markdown link/autolink, HTML `href`/`src`/`img`, plain URL, markdown image, data URI를 추출한다. self-anchor·`mailto:`/`tel:`/`javascript:`/`blob:`·non-http scheme은 제외.
- input fetch queue는 `planning-format` 0.2.5 결정성 룰을 따른다: push 시점 normalize, depth BFS, 같은 depth 안 markdown link → HTML href/src → plain URL 발견 순서, dequeue된 visited 미포함 URL은 100% fetch 시도, 실패도 visited 등록 + 출처 행 기록.
- depth·pages·body·fanout cap은 두지 않는다. cycle·중복은 input visited set으로만 막는다.
- fetch 진입 직전 `../planning-format/references/connector-routing.md`를 1회 Read 적재한다. 1차 WebFetch + connector fallback·인증 휴리스틱·MCP 카탈로그·Google Workspace tool 시퀀스·gid/range·status 표기를 그대로 공유한다.
- input visited set은 SSOT visited set과 별도다. 같은 URL이 input source와 SSOT corpus link에 동시에 등장해도 `## 입력 출처`와 `## SSOT 출처`에 각각 나타날 수 있다.
- `--no-input-fetch` ON이면 input fetch queue 전체를 봉쇄한다. 입력이 URL뿐이면 review 대상 본문을 만들 수 없으므로 §sanity check 메시지를 출력한다.
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

통합 입력 본문에서 정책서·기능설계서·입력 제외 §을 분리한다.

1. 저장 경로가 있으면 화면 projection보다 `--save` 파일을 우선한다.
2. 0.2.9 unsaved 화면 출력은 readable projection으로 취급한다. 정책서 본문은 첫 `## 정책서` wrapper heading 다음 줄에서 시작해 다음 `## 기능설계서` wrapper heading 직전에서 끝난다.
3. 기능설계서 본문은 첫 `## 기능설계서` wrapper heading 다음 줄에서 시작해 `## 검증 피드백`, `## 출처 요약`, `## 입력 제외 요약`, `## 상세 추적` 중 가장 먼저 나오는 wrapper heading 직전에서 끝난다.
4. wrapper heading은 줄 시작에 있는 정확한 heading만 인정한다. 들여쓰기된 heading, blockquote 안 heading, fenced code block 안 heading은 경계로 보지 않는다.
5. 경계가 둘 이상으로 해석되거나 한쪽 본문을 확정할 수 없으면 임의 병합하지 않고 `검증 범위와 한계` 또는 sanity check에 `readable projection 경계 불명확`을 남긴다.
6. `# 정책서` / `## 정책서` 헤더 → 정책서 본문, `# 기능설계서` / `## 기능설계서` 헤더 → 기능설계서 본문. 0.2.8 이하 코드 펜스 안 헤더도 읽기 호환으로 반복 처리한다.
7. `## 입력 제외 항목` 또는 0.2.9 `## 입력 제외 요약`/`## 상세 추적` 안의 입력 제외 항목을 입력 제외 § 본문으로 분리한다. 부재해도 sanity check 아님.
8. source title/path/URL label이 `정책서`, `policy`, `정책`, `기능설계서`, `feature`, `design`, `spec` 중 하나를 명확히 가리키면 source 단위 fallback 배정.
9. 1개 파일 입력의 companion read source는 title/path/H1/본문 헤더와 입력 파일의 기능명/stem/domain 유사도로 후보를 좁힌다.
10. 위 절차 후 정책서·기능설계서 둘 다 확보하지 못하면 sanity check.

source 단위 fallback은 명확한 1:1 신호일 때만 사용한다. 두 source가 모두 같은 종류로 추정되거나 둘 다 불명확하면 fallback하지 않는다.
companion read에서 여러 기능의 정책서·기능설계서 후보가 섞여 있고 입력 파일 기준으로 1쌍을 확정할 수 없으면 fallback하지 않고 sanity check로 종료한다.

분리 결과는 메모리에만. `--axes` 활성 무관 분리 단계는 항상 시도.

| 케이스 | 메시지 |
|---|---|
| conversation 모드 + 직전 planning-format 출력 없음 | `직전 turn에서 planning-format 출력을 찾을 수 없습니다. 경로 또는 markdown을 인자로 주세요.` |
| URL 입력 + `--no-input-fetch` | `입력 URL fetch가 --no-input-fetch로 봉쇄되어 정책서·기능설계서 본문을 식별할 수 없습니다. 파일/markdown 입력을 주거나 --no-input-fetch를 제거하세요.` |
| URL root 모두 본문 합류 실패 | `모든 review 입력 URL fetch 실패. 첫 번째 사유: <status 또는 error>` |
| URL root 모두 인증 게이트 + fallback 실패 | `모든 review 입력 URL이 로그인 필요로 보입니다. connector/MCP fallback도 인증되지 않았습니다.` + `필요한 connector: <Atlassian / Figma / Google Drive / Slack / Notion / ...>` |
| 단일 파일 companion read 후보 모호 | `같은 폴더에서 정책서·기능설계서 1쌍을 확정할 수 없습니다. 리뷰할 두 파일을 명시하거나 기능별 폴더로 분리하세요.` |
| 본문 식별 실패 | `정책서·기능설계서 두 본문을 식별할 수 없습니다. URL 본문에 # 정책서 / # 기능설계서 헤더를 두거나, 정책서·기능설계서가 구분되는 별도 링크/파일로 주세요.` |
| 한쪽 본문 비어 있음 | `<정책서 또는 기능설계서>가 비어 있습니다. 입력 URL/파일이 planning-format 산출물인지 확인하세요.` |
| `--axes` 빈 값 | `--axes에 점검 축을 1개 이상 지정하세요. (ssot, ac, deps)` |

### Step 2: 검증 축 점검

`--axes` 활성 축만 main 단일 패스. 각 축은 reference 적재 후 그대로 따른다.

**sub-§ 인식 (0.2.4)**: R1·R2·R3 모두 산출물 부모 § + sub-§(`### N.M ... 보조 표`) 본문을 함께 점검 대상으로 본다. 절차 detail은 각 reference 그대로 — 부모 § 룰을 sub-§ 본문에 자연 확장.

| 축 | 키 | 적재 reference | 발견 sub-category |
|---|---|---|---|
| R1. SSOT 충돌 | `ssot` | `references/ssot-rules.md` | (단일) |
| R2. Acceptance Criteria 검증가능성 | `ac` | `references/ac-rules.md` | 정량성 / 상태 / 행위자 / 결과 관찰 |
| R3. 의존·영향 분석 | `deps` | `references/deps-rules.md` | 정책 변경 / 상태 전이 / 권한·역할 / 외부 의존 (발견·권고 분류) |

R1·R3 corpus 공유 (`--ssot-include`). R2는 input collection 이후 분리된 본문 자체만 본다.

#### R1 link follow (0.2.2)

R1 활성 OR R3 활성 + 매칭 ≥1 + `--no-ssot-fetch` off → 매칭 *.md 본문 안 URL·이미지를 fetch + connector fallback으로 corpus body에 합류. 절차·visited set·sanity check·출처 list 형식 모두 `references/ssot-rules.md` §R1.4·§R1.5. connector lookup은 `../planning-format/references/connector-routing.md` 공유 적재. `--no-ssot-image` ON이면 image content-type 합류 skip (URL fetch는 별도).

입력 URL source 자체는 SSOT corpus가 아니다. input fetch는 review 대상 본문 생성용이고, SSOT fetch는 비교 corpus 확장용이다.

#### R3 입력 제외 § 보조 신호 (0.2.2)

R3 활성 + Step 1 분리 성공 시 카테고리별 가중치. 절차·신호 카테고리·헤더 카운트 K 산출 모두 `references/deps-rules.md` §R3.2.1.

### Step 3: 발견 합산 + 우선순위/작업화

같은 발견이 두 축에 걸치면 한 번만 기록. 축 중복 제거 우선순위: **R1 > R3 > R2**.

발견은 기본 출력 전에 P0/P1/P2로 재정렬한다.

| 우선순위 | 의미 | 기본 매핑 |
|---|---|---|
| P0 | 구현/운영 판정을 결정할 수 없어 기능 동작이 비결정적 | R1 또는 R2의 핵심 결정 불가, R3 외부 영향 중 운영 차단 |
| P1 | 정책/기능 문서 간 범위 충돌 또는 외부 시스템 영향이 큼 | R1 충돌, R2 검증 불가, R3 발견 |
| P2 | 후속 SSOT 보강, cross-link, 변경 워크플로 권고 | R3 권고, SSOT 보강 작업 |

작업 백로그는 발견을 그대로 나열하기 전에 수정 작업 단위로 묶는다. 항목 ID는 `A1`, `A2` 형식이다.

| 유형 | 설명 |
|---|---|
| `문서 수정` | 정책서·기능설계서 본문을 직접 고쳐야 함 |
| `정책 결정` | 담당자/도메인 owner가 값을 결정해야 함 |
| `SSOT 보강` | 본문 없는 자리표시자(placeholder) 또는 부재한 기준 문서를 작성/보강해야 함 |
| `외부 인터페이스` | WCS/API/시트 등 외부 의존 계약을 명시해야 함 |
| `동기화 워크플로` | 시트·정책서·기능설계서 동시 갱신 절차가 필요함 |

모든 기본 발견 ID는 `R1-1`, `R2-1`, `R3-1` 형식이다. 같은 출력 안에서만 stable하면 된다.

### Step 4: 판정과 검증 신뢰도

검증 신뢰도:

| 신뢰도 | 조건 |
|---|---|
| `충분` | review 대상 본문이 충분하고, 활성 축에 필요한 비교 대상/증거가 실질 본문을 포함하며, 활성 축을 정상 평가했다. |
| `제한적` | review 대상 본문은 충분하고 활성 축을 평가했지만 일부 SSOT 파일이 placeholder이거나 특정 외부 link follow가 실패해 증거 범위가 일부 제한된다. |
| `낮음` | 활성 핵심 축을 평가할 비교 대상 대부분이 비어 있거나, 입력 fetch 실패로 review 대상 본문 일부만 확보했다. `ssot` 축 활성 + SSOT 기준 문서 묶음 0건 또는 모두 placeholder이면 `낮음`. |

판정 우선순위:

1. `수정 필요`: P0 또는 P1 발견이 1건 이상 있다.
2. `비교 불가`: 요청한 핵심 축이 증거 부족으로 판단 불가다. 예: `--axes ssot`인데 SSOT 기준 문서 묶음이 모두 placeholder.
3. `검토 필요`: P0/P1은 없고, 핵심 축이 판단 가능하며, P2 권고가 있거나 외부 결정이 필요한 항목이 있다.
4. `조건부 통과`: P0/P1/P2 발견이 없고, 활성 축은 평가됐지만 검증 신뢰도가 `제한적`이다.
5. `통과`: P0/P1/P2 발견이 없고, 검증 신뢰도가 `충분`이다.

신뢰도는 활성 축 기준으로 판단한다. 예를 들어 `--axes ac`만 활성인 경우 SSOT corpus 부재는 신뢰도 산정에 영향을 주지 않는다. `낮음`이고 P0/P1/P2 발견이 0건이면 최종 판정은 `비교 불가`다. `낮음`이더라도 P0/P1 발견이 있으면 `수정 필요`다.

## 출력 포맷

````markdown
# planning-review: [기능명]

- 판정: [통과 / 조건부 통과 / 수정 필요 / 검토 필요 / 비교 불가]
- 검증 신뢰도: [충분 / 제한적 / 낮음] — [이유]
- 입력: [사람이 읽는 요약]
- 점검 축: [ssot, ac, deps]
- 발견: P0 N건, P1 N건, P2 N건

---

## 결론

[1~3문장 bottom line]

## 최우선 수정 항목

[P0/P1만 기본 노출. 없으면 `없음`]

## 작업 백로그

[작업 단위 backlog. 없으면 `없음`]

## 발견 요약

[축별 count + high-signal finding only]

## 검증 범위와 한계

[입력/SSOT 기준 문서 묶음/본문 없는 자리표시자/본문 가져오기 실패/비활성 축 요약]

## 출처 요약

[기본 압축 출처]

## 상세 추적

[조건 충족 시 full 입력 출처표 / full SSOT 출처표 / 축별 원시 발견 목록]
````

규칙:

- 최종 출력은 반드시 `# planning-review: [기능명]`으로 시작한다.
- 최종 출력 앞에 fetch 진행 문장, project scan 진행 문장, "분석 결과를 정리합니다" 같은 로그를 쓰지 않는다.
- 전체 리포트를 ` ```markdown ` 또는 ` ```text ` 코드 펜스로 감싸지 않는다.
- `결론`은 발견 상세보다 먼저 온다.
- `최우선 수정 항목`은 P0/P1만 기본 노출한다. P0/P1이 없으면 빈 표가 아니라 `없음`을 쓴다.
- 작업 단위가 없으면 `## 작업 백로그`에는 빈 표가 아니라 `없음`을 쓴다.
- P2만 있는 경우 `## 최우선 수정 항목`은 `없음`, `## 작업 백로그`와 `## 발견 요약`에는 P2 관련 작업/요약을 압축 표시한다.
- full 입력 출처표, full SSOT 출처표, 축별 원시 발견 목록은 조건 충족 시 하단 `## 상세 추적` 섹션으로 이동한다.
- `## 상세 추적`은 조건 충족 시 `## 출처 요약` 뒤에 둔다.
- R3 발견·권고 항목이 입력 제외 § 보조 신호로 만들어진 경우 `근거` 줄에 입력 제외 § cross-reference 표시.

### 상세 추적 조건

| 조건 | 처리 |
|---|---|
| P0/P1 발견이 1건 이상 | 축별 원시 발견 목록 포함 |
| SSOT 기준 문서 묶음이 0건이거나 모두 placeholder | SSOT 후보/제외/placeholder 경로 요약 포함, 기본 상단 `검증 범위와 한계`에도 원인 표시 |
| `--ssot-include`가 SSOT 폴더 경계 밖만 가리켜 후보가 0건 | include glob, 제외 사유, 경계 밖 매칭 수 포함 |
| input fetch 실패, 인증 실패, 본문 미사용 출처가 1건 이상 | full 입력 출처표 포함 |
| SSOT link follow 실패, 인증 실패, 본문 미사용 출처가 1건 이상 | full SSOT 출처표 포함 |

### 출처 요약

```markdown
## 출처 요약

| 구분 | 건수 | 성공 | 실패 | 본문 사용 | 비고 |
|---|---:|---:|---:|---:|---|
| 입력 URL | 2 | 2 | 0 | 2 | 정책서, 기능설계서 |
| 입력 이미지 | 0 | 0 | 0 | 0 | 없음 |
| SSOT Markdown | 6 | 6 | 0 | 0 | 모두 placeholder |
| SSOT 외부 링크 | 0 | 0 | 0 | 0 | 링크 없음 |
```

connector 세부(`via Atlassian connector`)는 기본 출력에서 숨긴다. 실패나 인증 문제만 `비고`에 짧게 남긴다.

### 상세 입력 출처

input fetch 또는 input image 처리 1건 이상이고 상세 추적 조건을 충족할 때만 `## 상세 추적` 안에 둔다.

```markdown
### 입력 출처

root 입력: R개
재귀 fetch: 성공 K개 / 실패 J개 (cap 없음)
이미지: 성공 M개 / 실패 L개

| # | 출처 종류 | URL/경로 | origin | 상태 | 본문 사용 |
|---|---|---|---|---|---|
| 1 | 입력 root URL | https://wiki.example/policy/order-cancel | — | 200 (via WebFetch) | O |
| 2 | 입력 root URL | https://docs.example/feature/order-cancel | — | 200 (via Google Drive connector — read_file_content) | O |
| 3 | 입력 자식 URL | https://figma.com/design/... | 입력 출처 2 | 인증 필요 (Figma MCP 미인증) | X |
```

### 상세 SSOT 출처

link follow 1건 이상이거나 SSOT 0건/all-placeholder/경계 밖 include 조건을 충족할 때 `## 상세 추적` 안에 둔다. 표 형식은 `references/ssot-rules.md` §R1.5를 따른다.

### 축별 원시 발견 목록

```markdown
### SSOT 충돌
1. [제목]
   - 위치: [정책서/기능설계서 §섹션] vs [SSOT 파일 §섹션]
   - 근거: "[변환 본문 인용]" vs "[SSOT 인용]"
   - 영향: [한 줄]
   - 제안: [최소 수정 또는 확인 조건]

### 검증가능성
1. [제목]
   - 카테고리: [정량성 / 상태 / 행위자 / 결과 관찰]
   - 우선순위: [P0 / P1]
   - 위치: [정책서/기능설계서 §섹션]
   - 근거: "[변환 본문 인용]"
   - 영향: [한 줄]
   - 제안: [최소 수정]

### 영향 분석
1. [제목]
   - 분류: [발견 / 권고]
   - 우선순위: [P1 / P2]
   - 카테고리: [정책 변경 / 상태 전이 / 권한·역할 / 외부 의존]
   - 위치: [정책서/기능설계서 §섹션]
   - 영향 후보: [SSOT 파일 path list]
   - 근거: "[변환 본문 인용]" + (선택) "[SSOT 인용 또는 입력 제외 § cross-reference]"
   - 영향: [한 줄]
   - 제안: [후속 검토 조건]
```

## 참고 파일

- `references/ssot-rules.md` — R1 SSOT 충돌 점검 절차·SSOT token 폴더 corpus 경계·placeholder 판정·link follow·출처 list.
- `references/ac-rules.md` — R2 4 sub-category 기준 + P0/P1 우선순위 기본값.
- `references/deps-rules.md` — R3 4 sub-category 기준 + 발견/권고 P1/P2 기본값 + 입력 제외 § 보조 신호 + backlog grouping 신호.
- `../planning-format/references/connector-routing.md` — input fetch와 SSOT link follow에서 공유 적재. 인증 게이트 휴리스틱·MCP 카탈로그·호스트 매핑·Google Workspace tool 시퀀스·gid/range·fallback·status 표기.
- `../planning-format/references/conversion-rules.md` — input image multimodal·통합 본문 합류 룰을 공유 참조.

변환·자체 품질 점검·`--save`는 `planning-format` 스킬에서 별도 처리. 자세한 절차는 `skills/planning-format/SKILL.md`.
