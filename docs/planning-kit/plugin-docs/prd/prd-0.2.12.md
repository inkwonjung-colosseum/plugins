# planning-kit PRD 0.2.12

> 0.2.11 기반 incremental PRD. 0.2.10은 `결정 보드`로 실행 항목을 상단에 올렸고, 0.2.11은 사용자 화면에서 섹션 기호를 제거했다. 그러나 실제 Zone 관리 `planning-format`/`planning-review` 결과에서는 사용자가 여전히 "무엇이 생성됐는지", "무엇을 먼저 결정해야 하는지", "어느 섹션을 실행 기준으로 봐야 하는지"를 다시 해석해야 했다.
>
> 핵심 변경: 첫 화면에서 결과, 확인 필요, 다음 행동을 분리해 인지시키는 출력 계약을 추가한다. `planning-format`은 본문 전에 항상 `생성 결과 요약`을 먼저 보여주고, `planning-review`는 `결정 보드`를 실행 기준으로 단일화한다. 내부 ID와 상세 근거는 보존하되 첫 화면에서는 자연어 라벨을 우선한다.

## 1. 상태

| 항목 | 값 |
|---|---|
| PRD 상태 | 목표 계약. 실제 릴리즈 완료 전까지 runtime 현재 계약으로 간주하지 않는다. |
| 베이스 | 0.2.11 |
| 변경 성격 | incremental, 출력 markdown micro-breaking |
| 릴리즈 조건 | 13장 롤아웃 계획과 12장 검증 계획 완료 |
| 현재 runtime 주의 | manifest, README, marketplace/cache가 0.2.12로 동기화되기 전에는 설치 표면이 이전 버전일 수 있다. |

## 2. 변경 계약 요약

1. **`planning-format` 결과 먼저 표시** — 최종 응답 순서는 `헤더 → 생성 결과 요약 → 결정 보드(조건부) → 정책서 → 기능설계서`다. 결정 보드가 있어도 `생성 결과 요약`이 먼저 온다.
2. **`planning-review` 실행 기준 단일화** — `결정 보드`가 사람용 실행 기준이다. `최우선 수정 항목`과 `작업 백로그`는 heading 이름만 유지하고, 중복 상세를 담지 않는 호환 표시로 제한한다.
3. **첫 화면 자연어 라벨 고정** — 출력 표준은 `결정 N (Dn)`, `작업 N (An)`, `출시 전 해결 N (Tn)`, `차단 (P0)`이다. 단독 `D1`, `A1`, `P0`로 시작하는 첫 화면 항목은 금지한다.
4. **피드백 카드화** — `planning-format`의 `검증 피드백`은 카드/필드 목록을 기본으로 한다. 7열 이상 Markdown 표는 실패다.
5. **parser boundary 보강** — `생성 결과 요약`은 예약된 H2 메타데이터 영역이다. 정책서·기능설계서 본문으로 합류하면 실패다.
6. **fixture 필수화** — `prd-0.2.12-fixtures.yml`은 권장이 아니라 release gate다.
7. **롤아웃 명시** — skill/reference, README/workflow, fixture, manifest, marketplace/cache, rollback 기준을 같은 release 범위로 다룬다.

## 3. 문제와 범위

### 문제

- `planning-format`은 본문이 길어질수록 검증 상태와 출처 영향이 본문 뒤에 묻힌다.
- `planning-review`는 같은 D*/A* 정보를 `결정 보드`, `최우선 수정 항목`, `작업 백로그`에서 반복할 수 있다.
- `판정`, `검증 신뢰도`, `첫 화면 요약`, `결론`이 같은 판단을 다른 표현으로 반복할 수 있다.
- 첫 화면에서 내부 ID와 범례를 해석해야 하면 사용자가 결과를 읽기 전에 도구 규칙을 먼저 배워야 한다.
- SSOT 기준 문서 묶음이 없거나 본문 없는 문서뿐인 경우 `발견 0건`과 `비교 근거 부족`이 혼동될 수 있다.

### 비목표

- `## 정책서`, `## 기능설계서`, `## 결정 보드`, `## 최우선 수정 항목`, `## 작업 백로그` heading 이름을 제거하지 않는다.
- R1/R2/R3 판정 기준, 우선순위, 카테고리를 바꾸지 않는다. `ac-rules`, `deps-rules`, `ssot-rules` 변경은 출력 표시·용어·섹션 위치에만 한정한다.
- D*/A*/T*/R*/F* 원시 ID를 폐기하지 않는다. 첫 화면 단독 노출을 줄이고 상세 추적에 보존한다.
- `planning-format --save` 저장 파일에 화면용 요약, 결정 보드, 검증 피드백, 출처 요약, 상세 추적을 저장하지 않는다.
- 0.2.11 이하 과거 PRD 본문을 일괄 수정하지 않는다.

## 4. 공통 화면 계약

### 4.1 첫 화면 판독 순서

첫 화면은 사용자가 다음 순서로 읽을 수 있어야 한다.

1. 결과: 문서 생성 완료인지, 리뷰 판정인지, 비교 불가인지
2. 차단 여부: 출시 전 해결 필요, 결정 필요, 확인 필요
3. 다음 행동: 오늘 결정, 바로 수정, 후속 작업
4. 근거 위치: 피드백 카드, 발견 요약, 상세 추적

### 4.2 자연어 라벨

| 내부/기술 표현 | 첫 화면 표준 표현 |
|---|---|
| `D1` | `결정 1 (D1)` |
| `A1` | `작업 1 (A1)` |
| `T1` | `출시 전 해결 1 (T1)` |
| `P0` | `차단 (P0)` |
| `P1` | `중요 (P1)` |
| `P2` | `권고 (P2)` |
| `R2-1`, `F5-1` | 첫 화면 단독 노출 금지. `관련 근거 N건`으로 접고 상세 추적에 보존 |
| `SSOT corpus` | `기준 문서 묶음` |
| `SSOT token 폴더` | ``SSOT` 표시가 있는 기준 문서 폴더` |
| `placeholder` | `본문 없는 문서` |
| `raw markdown` | `붙여 넣은 Markdown 원문` |
| `fetch` | `본문 가져오기` |
| `connector fallback` | `연결된 서비스로 다시 확인` |
| `deps` | `영향 분석` |
| `AC Blocker` | `구현/QA 차단` |

금지어 적용 범위:

- 최종 출력 예시와 첫 화면 예시에만 강제한다.
- CLI 옵션 설명, migration/history, parser/reference 설명에서는 기술 용어를 사용할 수 있다.
- 사용자-facing 예시 안에서는 섹션 기호를 원문 직접 인용 외에 출력하지 않는다.

## 5. `planning-format` 계약

### 5.1 출력 순서

결정 보드가 있는 경우:

```markdown
# [기능명]

- 입력: ...
- 산출물: 정책서, 기능설계서
- 검증: ...
- 저장: ...

---

## 생성 결과 요약

[문서 결과 / 저장 / 검증 상태 / 확인 필요 / 출처 상태 / 입력 제외 상태 / 읽는 순서]

---

## 결정 보드

[첫 화면 요약 → 항목 목록 → 필요 시 상세]

---

## 정책서
...

## 기능설계서
...
```

결정 보드가 없는 경우:

```markdown
# [기능명]

[헤더 요약]

---

## 생성 결과 요약

[문서 결과 / 저장 / 검증 상태 / 확인 필요 / 출처 상태 / 입력 제외 상태 / 읽는 순서]

---

## 정책서
...
```

결정 보드 출력 조건:

- 확인 필요, 출시 전 해결 필요, 사용자/PM/현업 결정 항목 중 1건 이상 있으면 출력한다.
- 없으면 결정 보드는 생략하고 `생성 결과 요약`의 `확인 필요`를 `없음`으로 고정한다.

### 5.2 `생성 결과 요약`

필수 라벨은 다음 7개이며, 각각 정확히 1회 출력한다.

1. `문서 결과`
2. `저장`
3. `검증 상태`
4. `확인 필요`
5. `출처 상태`
6. `입력 제외 상태`
7. `읽는 순서`

규칙:

- non-empty bullet 기준 7줄 이하.
- continuation bullet 금지.
- `확인 필요`가 없으면 `확인 필요: 없음`으로 쓴다.
- `검증 상태`는 `피드백 없음`, `확인 필요`, `출시 전 해결 필요`, `검증 생략 (--no-self-review)` 중 하나로 시작한다.
- `생성 결과 요약`은 메타데이터 영역이며 저장 파일에 쓰지 않는다.

예:

```markdown
## 생성 결과 요약

- 문서 결과: 정책서와 기능설계서 생성 완료. 화면 본문은 읽기용 표시입니다.
- 저장: 없음 (--save 미사용)
- 검증 상태: 확인 필요 2건, 출시 전 해결 필요 1건
- 확인 필요: 결정 1 (D1) Refurbish 완료 후 재고 속성 / 작업 1 (A1) 귀속 로케이션 컬럼 보강
- 출처 상태: Figma 사용자 흐름 1건 본문 확인 실패, 기능설계서 사용자 흐름 누락 가능
- 입력 제외 상태: 총 21건, 결과 영향 3건은 결정 보드와 연결됨
- 읽는 순서: 생성 결과 요약 → 결정 보드 → 정책서 → 기능설계서 → 검증 피드백 → 상세 추적
```

### 5.3 검증 피드백

`## 검증 피드백` 기본 형식은 카드/필드 목록이다.

```markdown
### 피드백 1 (F5-1) Figma 사용자 흐름 다이어그램 미확인

- 위치: 기능설계서 3
- 구분: 누락
- 문제: Figma 사용자 흐름 다이어그램을 확인하지 못해 분기 누락 가능성이 있습니다.
- 영향: 기능설계서 사용자 흐름이 실제 다이어그램과 다를 수 있습니다.
- 제안: Figma를 직접 확인한 뒤 기능설계서 3을 보완합니다.
- 사용자 확인: 필요
- 본문 반영 여부: 미반영, 출처 확인 필요
- 결정 보드 연결: 결정 1 (D1)
```

규칙:

- 7열 이상의 Markdown 표는 실패다.
- 표는 5열 이하이고 모든 표시 문자열 셀이 60자 이하일 때만 허용한다.
- `planning-format` 결정 보드 범례는 `F=검증 피드백 원본`을 사용한다. `R*`는 `planning-review` 원시 발견 전용이다.
- 초과 항목 안내는 `검증 피드백`, `입력 제외 요약`, `상세 추적` 중 존재하는 섹션만 참조한다. `발견 요약` 참조는 실패다.

## 6. `planning-review` 계약

### 6.1 출력 순서

```markdown
# planning-review: [기능명]

- 판정: ...
- 검증 신뢰도: ...
- 입력: ...
- 점검 축: ...
- 발견: ...

---

## 결정 보드

[첫 화면 요약 → 항목 목록 → 필요 시 상세]

## 결론

[1~3문장]

## 발견 요약

[원인별 high-signal 요약]

## 검증 범위와 한계

[근거 부족과 비활성 축]

## 출처 요약

[압축 출처]

## 최우선 수정 항목

[최소 표시]

## 작업 백로그

[최소 표시]

## 상세 추적

[조건 충족 시]
```

라벨 호환:

- 0.2.12 출력은 기존 `검증 신뢰도` 라벨을 유지한다.
- `검토 근거 수준`은 향후 표현 후보 또는 입력 alias로만 허용한다.
- parser는 `검증 신뢰도`와 `검토 근거 수준`을 같은 metadata field로 읽을 수 있어야 한다.

### 6.2 결정 보드 첫 화면

```markdown
## 결정 보드

### 첫 화면 요약

- 결론: 수정 필요. 출시 전 해결 필요 1건과 중요 수정 3건이 있습니다.
- 오늘 결정: WCS 외부 참조 조건 확정 (결정 1 (D1))
- 출시 전 해결 필요: 결정 1 (D1) 해소 전 자동 비활성 전환 구현·QA 불가
- 바로 수정: Authority 수정 상태 조건 정합화 (작업 2 (A2))
- 다음 액션: 결정 1 (D1) 확정 후 작업 1 (A1)에 반영

범례: D=결정, A=작업, T=출시 전 해결, R=상세 근거
읽는 순서: 오늘 결정 → 출시 전 해결 필요 → 바로 수정 → 상세 근거
```

규칙:

- `첫 화면 요약`은 non-empty bullet 기준 최대 5줄.
- 각 줄은 `결론`, `오늘 결정`, `출시 전 해결 필요`, `바로 수정`, `다음 액션` 중 하나로 시작한다.
- `^- (D|A|T|R|F)\d+\b`, `^- P[0-2]\b` 패턴으로 시작하면 실패다.
- 긴 Given/When/Then은 첫 화면 요약에 쓰지 않는다.

### 6.3 호환 heading 최소 표시

`## 최우선 수정 항목`과 `## 작업 백로그` heading 이름은 0.2.x 호환을 위해 유지한다.

규칙:

- 두 섹션 첫 줄은 `요약: 실제 우선순위와 실행 순서는 위 결정 보드를 기준으로 확인하세요.`로 쓴다.
- 같은 ID는 `작업 1 (A1) - 결정 보드 참조`처럼 1줄로 표시한다.
- 각 섹션은 최대 5행을 기본으로 한다.
- 해당 섹션 안에 `선택지:`, `검증 방법:`, `완료 조건:`, `Given `, `When `, `Then `, 원시 `R\d+-\d+`가 있으면 실패다.
- 새 판단이나 새 항목을 이 섹션에서 처음 만들면 실패다.

### 6.4 SSOT 부족 상태

SSOT 기준 문서 묶음이 0건이거나 모두 본문 없는 문서인 경우:

- `발견 0건`을 `충돌 없음`처럼 쓰지 않는다.
- 첫 화면 또는 결론에 `비교 근거 부족`을 명시한다.
- 작업이 필요하면 `증거 보강 작업, 출시 전 해결 필요 아님`처럼 출시 차단 여부를 명확히 표시한다.
- `--axes ac`처럼 SSOT 축이 비활성인 경우에는 SSOT 보강 작업을 만들지 않는다.

## 7. Parser와 호환성

### 7.1 `생성 결과 요약` boundary

`## 생성 결과 요약`은 exact H2 wrapper로 예약한다.

규칙:

- 정상 위치는 헤더 요약 뒤, 첫 `## 정책서` 앞이다.
- `## 결정 보드`가 있으면 `생성 결과 요약` 뒤에 온다.
- 정상 위치 밖의 `## 생성 결과 요약`은 misplaced metadata로 보고 해당 line부터 다음 인정된 wrapper H2 직전까지 body에서 제외한다.
- 같은 metadata 영역에 두 번째 `## 생성 결과 요약`이 있으면 duplicate로 처리하고 warning 문자열은 `readable projection boundary ambiguous`로 남긴다.
- `생성 결과 요약` 내부의 code fence, blockquote, list child heading, heading-like text는 정책서·기능설계서 본문 추출에 포함하지 않는다.
- 정책서 본문은 첫 `## 정책서` wrapper heading 다음 줄에서 시작한다.

### 7.2 섹션 위치 호환

- `planning-review` parser는 0.2.10/0.2.11 구순서와 0.2.12 신순서를 모두 읽는다.
- `최우선 수정 항목`과 `작업 백로그`는 위치가 아니라 exact H2 heading map으로 찾는다.
- 같은 A*가 결정 보드와 호환 heading에 모두 있으면 결정 보드를 우선한다.
- 상세 추적 소비자는 H3 이름으로 `결정 보드 연결 맵`, `축별 원시 발견 목록`, `입력 출처`, `SSOT 출처`를 찾는다. 내부 순서나 table position에 의존하지 않는다.

### 7.3 ID normalize

출력 canonical:

- `결정 N (Dn)`
- `작업 N (An)`
- `출시 전 해결 N (Tn)`
- `차단 (P0)`, `중요 (P1)`, `권고 (P2)`

읽기 호환:

- `D1`, `D1 [P0]`, `A1`, `T1`, `R2-1`, `F5-1`
- `결정 1, D1`, `작업 1(A1)` 같은 0.2.12 초안 예시 drift도 같은 ID로 normalize할 수 있다. 신규 출력에는 쓰지 않는다.

## 8. 문서/예시 동기화

필수 갱신 대상:

- `planning-kit/README.md`
- `planning-kit/docs/planning-format-workflow.md`
- `planning-kit/docs/planning-review-workflow.md`
- `planning-kit/docs/planning-kit-workflow-guide.md`
- `planning-kit/docs/prd/README.md`
- `planning-kit/docs/prd/fixtures/prd-0.2.12-fixtures.yml`

규칙:

- README 첫 화면은 최신 PRD 핵심을 반영한다.
- workflow 문서의 최종 출력 예시는 0.2.11 clean display와 0.2.12 결과 인지 구조를 따른다.
- 금지어 검색은 최종 출력 예시와 첫 화면 예시에만 적용한다. CLI 옵션 설명, migration/history, reference 설명은 제외한다.
- PRD가 release target이면 root README, plugin manifest, marketplace metadata까지 version을 맞춘다.

## 9. 수정 대상 파일

필수:

- `planning-kit/skills/planning-format/SKILL.md`
- `planning-kit/skills/planning-format/references/output-contract.md`
- `planning-kit/skills/planning-format/references/self-review-rules.md`
- `planning-kit/skills/planning-review/SKILL.md`
- `planning-kit/skills/planning-review/references/ac-rules.md`
- `planning-kit/skills/planning-review/references/deps-rules.md`
- `planning-kit/skills/planning-review/references/ssot-rules.md`
- `planning-kit/README.md`
- `planning-kit/docs/planning-format-workflow.md`
- `planning-kit/docs/planning-review-workflow.md`
- `planning-kit/docs/planning-kit-workflow-guide.md`
- `planning-kit/docs/prd/README.md`
- `planning-kit/docs/prd/fixtures/prd-0.2.12-fixtures.yml`

release 시 추가:

- `planning-kit/.claude-plugin/plugin.json`
- `planning-kit/.codex-plugin/plugin.json`
- root `README.md`
- marketplace/cache 동기화 대상

검증 rule 파일 변경 제한:

- `ac-rules`, `deps-rules`, `ssot-rules`는 출력 표시, 용어, 섹션 위치만 변경한다.
- R1/R2/R3 판정 기준, 우선순위, finding 카테고리 변경은 0.2.12 범위 밖이다.

## 10. 수용 기준

### 10.1 `planning-format`

- `## 정책서` 전에 `## 생성 결과 요약`이 나온다.
- `생성 결과 요약`은 non-empty bullet 기준 7줄 이하이며 필수 라벨 7개가 각각 정확히 1회 나온다.
- 확인 필요가 없으면 `확인 필요: 없음`이 나온다.
- `## 검증 피드백`은 카드/필드 목록이 기본이다. 7열 이상 표가 나오면 실패다.
- `planning-format` 결정 보드 범례에서 원시 발견은 `F=검증 피드백 원본`으로 표시한다.
- 초과 항목 안내가 `발견 요약`을 참조하면 실패다.
- `--save` 저장 파일에는 `## 생성 결과 요약`, `## 결정 보드`, `## 검증 피드백`, `## 출처 요약`, `## 입력 제외 요약`, `## 상세 추적`이 없다.

### 10.2 `planning-review`

- `결정 보드` 안에서 `첫 화면 요약`이 범례보다 먼저 나온다.
- `첫 화면 요약`은 non-empty bullet 기준 최대 5줄이다.
- 각 bullet은 `결론`, `오늘 결정`, `출시 전 해결 필요`, `바로 수정`, `다음 액션` 중 하나로 시작한다.
- 첫 화면 bullet이 단독 `D1`, `A1`, `P0`로 시작하면 실패다.
- `최우선 수정 항목`과 `작업 백로그`는 `출처 요약` 뒤, `상세 추적` 앞에 나온다.
- 호환 heading 안에 `선택지:`, `검증 방법:`, `완료 조건:`, `Given `, `When `, `Then `, 원시 `R\d+-\d+`가 있으면 실패다.
- SSOT 기준 문서 묶음이 0건 또는 모두 본문 없는 문서이면 `충돌 없음`처럼 쓰지 않고 `비교 근거 부족`을 표시한다.
- `상세 추적` 내부에서 `결정 보드 연결 맵`이 축별 원시 발견 목록과 출처표보다 먼저 나온다.

### 10.3 문서/예시

- README 첫 문단이 최신 출력 계약을 설명한다.
- workflow 문서의 최종 출력 예시는 섹션 기호 없이 clean display를 사용한다.
- 최종 출력 예시와 첫 화면 예시에 단독 `D*`, `A*`, `P0/P1`, `SSOT corpus`, `token`, `raw`, `fetch`, `connector fallback`이 남으면 실패다.
- PRD chain README는 0.2.12를 target PRD로 안내하되, runtime release 여부는 1장의 상태와 13장의 롤아웃 조건으로 구분한다.

## 11. Fixture 계약

`planning-kit/docs/prd/fixtures/prd-0.2.12-fixtures.yml`은 필수 산출물이다.

각 fixture는 다음 필드를 가진다.

- `args`
- `input_fixture` 또는 `inline_input`
- `expected_section_order`
- `expected_present`
- `expected_absent`
- 필요 시 `expected_scoped_absent`
- 필요 시 `expected_saved_file_absent`
- 필요 시 `line_budget`

필수 fixture:

- `result_summary_exact_fields`: 필수 라벨 7개가 정확히 1회, 7줄 초과 실패.
- `result_summary_no_feedback`: `확인 필요: 없음`, `검증 상태: 피드백 없음`.
- `feedback_card_display_long_cells`: 7열 이상 표 실패, 카드 필드 존재.
- `save_canonical_no_result_summary`: 화면에는 요약 존재, 저장 파일에는 메타데이터 heading 부재.
- `parser_ignores_result_summary`: 요약 안 가짜 H2가 본문 추출을 오염시키지 않음.
- `legacy_sections_old_order`: 0.2.10/0.2.11 구순서 입력 읽기 호환.
- `legacy_sections_new_order`: 0.2.12 신순서 입력 읽기 호환.
- `id_label_normalization`: legacy ID와 신규 자연어 라벨이 같은 ID로 normalize.
- `detail_trace_reordered`: 상세 추적 연결 맵 우선 순서 확인.
- `review_legacy_sections_minimized`: 호환 heading scoped absence 검증.
- `review_ssot_missing_axes_matrix`: all axes, `--axes ac`, placeholder-only 분리.
- `doc_hygiene_clean_display`: 최종 출력 예시 금지어와 섹션 기호 검색.

## 12. 검증 계획

1. `prd-0.2.12-fixtures.yml` 작성 여부 확인.
2. fixture의 section order, present/absent, scoped absent, saved-file absent expectation 점검.
3. `claude plugin validate ./planning-kit`.
4. plugin manifest JSON parse.
5. `git diff --check -- planning-kit`.
6. 최종 출력 예시 금지어 검색.
7. `## 생성 결과 요약` boundary 오염 케이스 수동 확인.

## 13. 롤아웃 계획

1. skill/reference 업데이트
   - `planning-format` 출력 순서, 피드백 카드, parser boundary 반영
   - `planning-review` 출력 순서, 호환 heading 최소 표시, 상세 추적 순서 반영
2. README/workflow 업데이트
   - 최신 첫 화면 예시 반영
   - stale 0.2.10 중심 문구 제거 또는 migration/history로 이동
3. fixture 업데이트
   - 11장 필수 fixture 작성
4. version/release metadata 업데이트
   - `planning-kit/.claude-plugin/plugin.json`
   - `planning-kit/.codex-plugin/plugin.json`
   - root `README.md`
   - marketplace metadata
5. 설치본 동기화
   - marketplace copy
   - active cache copy
6. 검증
   - `claude plugin validate ./planning-kit`
   - manifest JSON parse
   - `git diff --check`
   - fixture/manual golden expectation 확인
7. rollback 기준
   - parser가 0.2.10/0.2.11 산출물을 읽지 못하면 release 중단
   - `## 생성 결과 요약`이 정책서·기능설계서 본문으로 합류하면 release 중단
   - README/manifest/marketplace version이 불일치하면 release 중단

## 14. 릴리즈 노트 초안

`planning-kit` 0.2.12는 결과 화면의 첫 인지성을 개선합니다. `planning-format`은 정책서·기능설계서 본문 전에 생성 결과와 검증 상태를 먼저 보여주고, `planning-review`는 결정 보드를 실행 기준으로 단일화해 호환 heading의 중복 상세를 줄입니다. 내부 ID와 상세 근거는 보존하되 첫 화면에서는 자연어 라벨과 다음 행동을 우선 표시합니다.
