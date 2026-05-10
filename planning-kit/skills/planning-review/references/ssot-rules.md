# SSOT Rules (R1)

`planning-review`의 SSOT 충돌 점검 축(R1).

## 용어

- **SSOT corpus**: 현재 프로젝트 폴더 안 모든 `*.md` (`.git/`, `node_modules/` 자동 제외, `--ssot-include <glob>`로 좁힘) **+ 0.2.2부터 매칭 *.md 본문 안 외부 URL fetch 본문·이미지 해석 결과** (link follow 활성 시). 외부 fetch 본문은 `--no-ssot-fetch`로, 이미지 multimodal은 `--no-ssot-image`로 봉쇄 가능.
- **input collection**: 0.2.6부터 `planning-review`가 review 대상 본문을 만들기 위해 URL·파일·디렉터리·텍스트·이미지를 수집하는 단계. 입력 URL source 자체는 SSOT corpus가 아니다.
- **input fetch**: input collection 안 URL fetch. `--no-input-fetch`로 봉쇄하며, R1/R3 SSOT corpus link follow와 별도 visited set을 가진다.
- **SSOT fetch**: R1/R3 SSOT corpus link follow. `--no-ssot-fetch`로 봉쇄하며, input fetch와 별도 visited set·출처 블록을 가진다.
- **확정 문장**: 변환 본문 중 `[TBD]`가 아닌 단정 표현.
- **R1 link follow**: 매칭 *.md 본문 안 URL을 추출해 fetch + connector fallback으로 corpus body에 합류시키는 0.2.2 신규 절차 (§R1.4).

## R1.1 corpus 추출 절차

1. 변환 본문에서 키워드 추출: 기능명·도메인 stem·역할명·상태명·권한명·정책 핵심어.
2. 프로젝트 폴더 `find . -name '*.md'` (`.git`/`node_modules` 제외, `--ssot-include`로 좁힘).
3. 키워드 `grep -l` 또는 `rg -l`로 본문 매칭 → 매칭 file 목록 확정.
4. 매칭 file을 `Read` 툴로 직접 읽음 (인덱스 스캔 단계 없음).
5. **(0.2.2 신규)** 매칭 file 본문에서 URL·이미지 참조 추출 — markdown link / autolink / HTML href·src·img / plain URL / markdown image / data URI. self-anchor·`mailto:`/`tel:`/`javascript:`/`blob:` 제외. 이 추출은 SSOT corpus 확장용이며 0.2.6 input collection 추출과 독립이다.
6. **(0.2.2 신규)** 추출 URL을 fetch queue에 시드, 이미지를 image queue에 시드. `--no-ssot-fetch` ON이면 단계 5~8 skip.
7. **(0.2.2 신규)** 재귀 fetch + connector fallback — `../planning-format/references/connector-routing.md`를 1회 Read 적재해 그대로 사용. 인증 게이트 휴리스틱·MCP 카탈로그·호스트 매핑·Google Workspace tool 시퀀스·gid/range 처리·fallback 케이스 표·status 표기 모두 거기에 있다.
8. **(0.2.2 신규)** 이미지 multimodal 해석 — 지원 확장자·해석 프롬프트는 `planning-format` §4 그대로. `--no-ssot-image` ON이면 image content-type 응답 합류 안 함.
9. 외부 fetch 본문 + 이미지 해석 결과를 corpus body에 합류. visited set으로 cycle 방지. **cap 없음**.

문서 종류·역할(정책/PRD/회의록/README) 구분 안 함. archive/old/draft 신호 file도 grep 매칭만으로 비교 대상에 포함 — 별도 분류 없음.

## R1.2 매칭 0건

- 매칭 file 0건 → R1 결과 `검증 대상 없음`. 출력 헤더에 `SSOT 매칭 파일 0개 (관련 Markdown 부재)`.
- link follow 단계 진입 자체 없음 (corpus 자체 부재).
- 결과를 낮추지 않는다. R2·R3는 별도 진행.

## R1.3 매칭 ≥1건

- 변환 본문 확정 문장과 매칭 file 본문 + 외부 fetch 본문(link follow 활성 시)을 직접 비교.
- 같은 대상(역할·상태·정책 규칙·임계)이 양쪽에 있고 표기·결정·임계값이 어긋나면 발견.
- 같은 대상에 대해 SSOT가 침묵하면 발견 아님 (R3로 가능).
- **sub-§ 인식 (0.2.4)**: 산출물 부모 § + sub-§(`### N.M ... 보조 표`) 본문 모두 corpus 비교 대상. sub-§ 단독 발견 가능. 발견 위치 표기는 §R1.6.

## R1.6 발견 위치 표기 (0.2.4)

발견 형식의 `위치` 줄에 sub-§ 명시 가능:

```
- 위치: 정책서 §5.1 row 3 (보조 표 안)
```

기존 `정책서 §5` 표기와 호환. 부모 § + sub-§ + row 모두 식별되면 셋 다 표시. 부모 § 단독 가능.

## R1.4 link follow (0.2.2 신규)

### 트리거 조건

- **R1 활성 OR R3 활성** + **매칭 ≥1** + **`--no-ssot-fetch` off** → link follow 진입.
- R1 단독·R3 단독·둘 다 활성 모두 같은 link follow 단계 사용. corpus는 단일 set이라 어느 축이 트리거해도 양쪽이 같은 corpus를 본다.
- `--axes ac`만 활성(R1·R3 비활성) → link follow 진입 안 함.

### fetch queue 시드 형식

매칭 file이 `./docs/policy/order.md`이고 본문에 `자세한 내용은 https://wiki.example/policy/order-cancel 참조` 줄이 있으면:

```
seed_urls = [
  ("https://wiki.example/policy/order-cancel", origin="./docs/policy/order.md", line=N),
]
```

origin·line 필드는 출처 list 표기에만 사용 (§R1.5). fetch 동작 자체는 `planning-format` §3과 동일 — `connector-routing.md`를 그대로 따른다.

### visited set·cycle 방지

- visited set: SSOT corpus의 URL normalize key 집합. URL normalize는 `connector-routing.md` §6 그대로 — fragment 제거·trailing `/`·트래킹 query 제거·호스트 lowercase·query 키 정렬.
- visited set은 한 호출 내에서만 유효. `planning-format` 호출의 visited set, `planning-review` input fetch visited set과 별도 (호출 간 캐시 미공유). 호출 간 캐시는 후속 PRD.
- input visited set과 SSOT visited set은 의도적으로 cross-set dedup하지 않는다. 같은 URL이 입력 root와 SSOT corpus link에 동시에 등장하면 `## 입력 출처`와 `## SSOT 출처`에 각각 나타날 수 있다.
- 같은 URL이 여러 매칭 *.md에서 발견되면 1번만 fetch + 본문 합류. 출처 list에는 origin file 1번만 표시 (첫 발견).
- 매칭 *.md 자체 본문은 cycle 방지 대상 아님 (이미 corpus). follow URL이 매칭 *.md 자기 자신을 가리키면 skip.
- R1이 fetch한 본문에서 발견된 자식 link도 visited set으로만 제어 (cap 없음).

### sanity check

- 매칭 file ≥1 + link 0건 → 정상. corpus는 매칭 file 본문만.
- 매칭 file ≥1 + link N건 + fetch 모두 실패 → 정상 (corpus는 매칭 file 본문만, 출처 list에 사유). R1·R3 점검 진행.
- 외부 fetch 결과가 image content-type → `planning-format` §4와 동일하게 image queue로 라우팅, multimodal 해석.
- 루트 매칭 file이 모두 비어 있어도 호출 종료 안 함. R2는 별도 진행 (R2는 corpus 무관).

## R1.5 출처 list

link follow를 1건 이상 진행한 호출에서만 `## SSOT 출처` 블록 출력. R1·R3 모두 비활성·매칭 0건·`--no-ssot-fetch`·link 0건이면 통째 생략.

```markdown
## SSOT 출처

매칭 *.md: N개
재귀 fetch: 성공 K개 / 실패 J개 (cap 없음)

| # | 출처 종류 | URL/경로 | origin (.md file:line) | 상태 | 본문 사용 |
|---|---|---|---|---|---|
| 1 | 매칭 *.md | ./docs/policy/order.md | — | — | O |
| 2 | 자식 URL | https://wiki.example/policy/order-cancel | ./docs/policy/order.md:42 | 200 (via WebFetch) | O |
| 3 | 자식 URL | https://confluence.example/wiki/spaces/POL/pages/123 | ./docs/policy/order.md:58 | 200 (via Atlassian MCP) | O |
| 4 | 자식 이미지 | path/diagram.png | ./docs/policy/order.md:71 | image/png 0.4MB | O (multimodal) |
| 5 | 자식 URL | https://docs.google.com/.../edit?gid=... | ./docs/policy/order.md:88 | 인증 필요 (Google Drive connector 미인증) | X |
```

규칙:
- `매칭 *.md` 행은 항상 origin·상태 컬럼이 `—` (1차 corpus, fetch 안 함).
- `자식 URL` / `자식 이미지` 행은 origin 컬럼에 발견 위치 표시.
- 상태 표기는 `connector-routing.md` §7 그대로.
- 실패 행도 list 포함. 실패 0건이면 표 아래 `모든 corpus 외부 링크 처리 성공` 한 줄.
