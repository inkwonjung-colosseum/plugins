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
| `--save` | off | `./.planning-kit/<기능명>/정책서.md`, `./.planning-kit/<기능명>/기능설계서.md` 두 파일에 본문 저장. 자체 검증 보고서·출처 list·입력 제외 §은 디스크 저장 안 함 (화면 only). 충돌·안전화는 `references/output-contract.md` §6. |
| `--no-fetch` | off | URL fetch + connector fallback 봉쇄. |
| `--no-image` | off | 이미지 multimodal 호출 0건. |
| `--no-self-review` | off | 자체 품질 검증 블록 출력 생략. **입력 제외 §은 끄지 않음** — 변환 결과 핵심 정보. |

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

URL 분기 sanity check는 `references/connector-routing.md` §8.

### Step 3: 재귀 fetch + connector fallback

URL 한 개씩 dequeue → normalize → visited 검사 → fetch → 본문 합류 + 자식 URL/이미지 추출 → queue push. depth·pages·body 크기 cap 없음. visited set으로만 cycle 방지. `--no-fetch`면 §3 전체 skip.

fetch 진입 직전 1회 `references/connector-routing.md`를 Read 적재. WebFetch 1차 + connector fallback·인증 휴리스틱·MCP 카탈로그·호스트 매핑·Google Workspace tool 시퀀스·gid/range·status 표기·sanity check 메시지·**§11 connector별 anchor 추출 (deep link)** 모두 거기에.

### Step 4: 이미지 multimodal 처리

`references/conversion-rules.md` §1을 (Step 6 진입 시 함께) 적재해 5경로 시드·지원 확장자·multimodal 해석·실패 사유 처리 따른다. `--no-image`면 §4 전체 skip.

### Step 5: 통합 본문 합류

`conversion-rules.md` §2 그대로 — 출처 단위 헤더 + concat + Sheets gid·range 부연.

### Step 6: 변환

`references/conversion-rules.md` 1회 Read 적재. 적재 후:

- §3 기능명 추출 (1순위 1개).
- §4 두 템플릿 변환 (라벨 매핑, 본문 미합류 조각은 입력 제외 §).
- §5 list 분해 판단 — 보조 표 번호 순차(`§N.M`)·헤더 backlink(`(§N row K)`)·다층 재귀.

본문 미합류 조각 라벨링은 `references/exclusion-rules.md` 1회 Read 적재 (§1 11 카테고리·§2 우선순위·§4 5필드·§5 처리 줄·§6 헤더 분포·§7 marker 1종).

> 큰 입력(통합 본문 ≥30 page 등) 시 indexing(claim 추출·도메인 grouping·충돌 grouping) → synthesis(두 본문) → exclusion → self-review 순 진행 권고. 강제 X — 작은 입력은 자유.

### Step 7: 자체 품질 검증

`--no-self-review`면 skip. 그 외엔 `references/self-review-rules.md` 적재 후 6 카테고리(F1 충실도·F2 cross-bleed·F3 용어·F4 정책-기능 매핑·F5 누락·F6 syntax) 단일 패스 점검. F1·F2는 sub-§(`### N.M ... 보조 표`) 본문도 점검. F5는 본문 누락 + cross-ref 3종(`cross-ref-fetch`·`cross-ref-scope`·`cross-ref-tbd`) 모두. 기준·예시·발견 형식 모두 reference 그대로.

6 카테고리 모두 0건이면 `통과`, ≥1건이면 `발견 N건`. 외부 corpus·다른 *.md는 보지 않음 (planning-review가 처리).

### Step 8: `--save` 처리

`references/output-contract.md` §6 그대로 — 저장 경로·기능명 안전화·collision suffix·저장 실패 헤더 표기.

### Step 9: 통합 출력

`references/output-contract.md` Read (Step 8과 함께) — §1 블록 순서·§2 정상 출력·§3 헤더 줄·§4 입력 제외 분포·§5 출처 list deep link 그대로 따른다.

## 참고 파일

- `templates/기능설계서.md` — 8 섹션 표 골격.
- `templates/정책서.md` — 10 섹션 표 골격.
- `references/conversion-rules.md` — multimodal·통합 본문·기능명·라벨 매핑·list 분해 판단·보조 표 번호 순차·backlink (Step 4·5·6).
- `references/exclusion-rules.md` — 11 카테고리·5필드(위치 markdown link)·처리 줄·우선순위·헤더 분포·marker 1종 (Step 6).
- `references/output-contract.md` — 출력 포맷·헤더 줄·`--save` 처리·`## 출처` list deep link·분기별 헤더 (Step 8·9).
- `references/self-review-rules.md` — 자체 품질 6 카테고리 (F1~F6) 점검 기준. F1·F2 sub-§ 인식 (Step 7).
- `references/connector-routing.md` — 인증 휴리스틱·MCP 카탈로그·호스트 매핑·Google Workspace tool 시퀀스·gid/range·fallback·status 표기·§8 sanity check·§11 connector별 anchor 추출 (Step 3).

외부 검증(SSOT 충돌·acceptance criteria·의존 영향)은 `planning-review` 스킬 별도 호출. 자세한 사용법은 `skills/planning-review/SKILL.md`.
