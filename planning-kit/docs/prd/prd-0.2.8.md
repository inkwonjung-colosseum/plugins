# planning-kit PRD 0.2.8

> 0.2.7 기반 incremental PRD. `planning-format` 보조 표 헤더에서 0.2.4에 도입된 backlink 메타데이터(`(§N row M)`)를 제거한다. 보조 표 제목은 문서 독자가 읽는 결정 문서 표면이므로 내부 추적 정보를 노출하지 않는다. 필요한 추적 정보는 `## 입력 제외 항목`의 `구조 변환` 처리 줄로 이동한다. 본 PRD 외 기존 `planning-format` / `planning-review` / `ssot-audit` 명세는 [`prd-0.2.7.md`](./prd-0.2.7.md) 이하 chain 그대로.
>
> 핵심 변경: 보조 표 헤더는 `### 5.1 Zone Type별 정책 보조 표`처럼 용도명만 남긴다. `### 5.1 Zone Type별 정책 보조 표 (§5 row 7~11)` 같은 헤더 backlink는 신규 출력에서 금지한다.

## 1. 변경 요약

1. **보조 표 헤더 backlink 제거** — `### N.M [용도] 보조 표 (§N row K)` 형식을 폐기하고 `### N.M [용도] 보조 표`만 출력한다.
2. **추적 정보 위치 이동** — 부모 §/row 추적이 필요한 경우 `## 입력 제외 항목`의 `구조 변환` 항목 `처리` 줄에 `본문 위치`와 `부모 위치`를 함께 기록한다.
3. **보조 표 내부 주석 행 금지** — 표 첫 행, HTML comment, 숨김 row로 backlink를 옮기지 않는다.
4. **legacy read 호환 유지** — `planning-review`와 self-review는 기존 0.2.4~0.2.7 산출물의 legacy backlink 헤더도 보조 표로 인식할 수 있어야 한다.
5. **신규 출력 검증 강화** — 0.2.8 이후 `planning-format` 신규 출력에서 보조 표 헤더에 `(§N row M)` 패턴이 남으면 자체 검증 syntax 발견으로 처리한다.

## 2. 동기

0.2.4에서 보조 표가 부모 §의 어느 row에서 분해됐는지 추적하기 위해 헤더 backlink를 도입했다.

```markdown
### 4.1 [용도] 보조 표 (§4 row 3)
```

이 정보는 변환 과정의 내부 추적에는 유용하지만, 정책서·기능설계서 본문에서는 다음 문제가 있다.

- 독자에게 불필요한 메타데이터가 문서 제목으로 노출된다.
- Confluence, Google Docs, Obsidian 등으로 복사할 때 문서 목차에 `row` 정보가 그대로 남는다.
- 제목이 길어져 보조 표의 실제 의미보다 생성 과정이 더 눈에 띈다.
- 다운스트림 파서가 heading title과 내부 추적 주석을 분리해야 한다.

기존 planning-kit 정책은 "정책서·기능설계서 본문은 결정문서로 깨끗하게 유지하고, 추적 정보는 출처·입력 제외 §이 담당한다"이다. 보조 표 헤더 backlink는 이 원칙과 충돌한다.

## 3. 비목표

- 보조 표 번호 체계(`§N.1`, `§N.1.1`, max-depth=3)는 변경하지 않는다.
- 보조 표 생성 판단, 컬럼 set 결정, list 분해/합류 판단은 변경하지 않는다.
- `## 출처` deep link 형식은 변경하지 않는다.
- `## 입력 제외 항목` 블록 자체를 숨기거나 제거하지 않는다.
- `--save` 결과 파일에 내부 추적 메타데이터를 저장하지 않는다.
- 기존 0.2.4~0.2.7 문서를 자동 마이그레이션하지 않는다.
- `planning-review` 입력 호환성을 깨지 않는다.

## 4. 보조 표 헤더 출력 규칙

### 4.1 신규 헤더 형식

0.2.8부터 `planning-format`이 새로 생성하는 보조 표 헤더는 다음 형식만 허용한다.

```markdown
### 4.1 [용도] 보조 표
```

예:

```markdown
### 5.1 Zone Type별 정책 보조 표
```

금지:

```markdown
### 5.1 Zone Type별 정책 보조 표 (§5 row 7~11)
### 5.1 Zone Type별 정책 보조 표 (§5)
### 5.1.1 하위 Zone 정책 보조 표 (§5.1 row 2)
```

### 4.2 보조 표 식별 기준

보조 표 식별은 trailing backlink가 아니라 heading 번호와 제목 구조로 판단한다.

- heading level: `###`
- 번호: `N.M` 또는 `N.M.K` 또는 `N.M.K.L`
- 제목: `[용도] 보조 표`

정규식 관점의 신규 출력 기준:

```text
^###\s+\d+(?:\.\d+){1,3}\s+.+보조 표$
```

legacy 입력 호환 기준:

```text
^###\s+\d+(?:\.\d+){1,3}\s+.+보조 표(?:\s+\(§[^)]*\))?$
```

신규 생성은 첫 번째 기준만 따른다. 읽기/검증은 두 번째 기준도 허용한다.

## 5. 추적 정보 이동

### 5.1 `구조 변환` 처리 줄 확장

0.2.8부터 보조 표 분해가 발생하면 `## 입력 제외 항목`의 `구조 변환` 항목에 다음 정보를 기록할 수 있다.

| 필드 | 의미 |
|---|---|
| 본문 위치 | 실제 생성된 보조 표 위치. 예: `정책서 §5.1`, `기능설계서 §4.1` |
| 부모 위치 | 보조 표 분해가 발생한 부모 § 또는 부모 row. 예: `정책서 §5 row 7~11`, `기능설계서 §4 row 3` |

처리 줄 형식:

```markdown
- 처리: 구조 분해 (본문 위치: 정책서 §5.1 / 부모 위치: 정책서 §5 row 7~11)
```

양쪽 문서에 모두 분해가 있으면 문서별로 병렬 표기한다.

```markdown
- 처리: 구조 분해 (본문 위치: 정책서 §5.1 / 부모 위치: 정책서 §5 row 7~11; 본문 위치: 기능설계서 §4.1 / 부모 위치: 기능설계서 §4 row 3)
```

row 식별이 안 되면 부모 §까지만 남긴다.

```markdown
- 처리: 구조 분해 (본문 위치: 정책서 §5.1 / 부모 위치: 정책서 §5)
```

### 5.2 저장 결과와 화면 출력

`--save`는 기존처럼 정책서·기능설계서 본문만 저장한다. `## 입력 제외 항목`은 화면 output only이므로, 부모 row 추적 정보도 저장 파일에는 들어가지 않는다.

이것은 의도된 동작이다. 저장되는 결정 문서에는 내부 변환 추적 메타데이터를 남기지 않는다.

## 6. 자체 검증 보강

0.2.8 이후 신규 `planning-format` 출력에서 다음 패턴이 발견되면 `syntax` 발견으로 기록한다.

```text
^###\s+\d+(?:\.\d+){1,3}\s+.+보조 표\s+\(§[^)]*\)$
```

발견 형식:

```markdown
1. 보조 표 헤더에 내부 backlink가 남아 있음
   - 카테고리: syntax
   - 위치: 정책서 §5.1
   - 근거: "### 5.1 Zone Type별 정책 보조 표 (§5 row 7~11)"
   - 영향: 내부 추적 메타데이터가 결정 문서 제목으로 노출됨
   - 제안: 헤더에서 괄호 backlink를 제거하고, 필요한 경우 입력 제외 항목의 구조 변환 처리 줄에 부모 위치를 기록
```

legacy 문서를 `planning-review`가 읽는 경우에는 발견으로 강제하지 않는다. 본 검증은 `planning-format` 신규 출력 self-review에만 적용한다.

## 7. 호환성

| 영역 | 0.2.7 → 0.2.8 |
|---|---|
| `planning-format` 신규 출력 | 보조 표 헤더에서 `(§N row M)` backlink 제거 |
| `planning-format --save` | 저장 파일이 더 깔끔해짐. 입력 제외/출처는 기존처럼 저장하지 않음 |
| `planning-review` 읽기 | legacy backlink 헤더와 신규 clean 헤더 모두 인식 |
| self-review | 신규 출력에 legacy backlink가 남으면 syntax 발견 |
| 다운스트림 파서 | heading title에서 backlink를 파싱하던 로직은 더 이상 신규 출력에 의존하면 안 됨 |
| PRD chain | 0.2.8 incremental. 기존 0.2.7 이하 명세 유지 |

## 8. 호출 시나리오

### 8.1 신규 clean header

입력 표 셀 list가 이질적이라 정책서 §5에서 보조 표로 분해된 경우:

```markdown
## 5. 정책 상세

| 항목 | 정책 |
|---|---|
| Zone Type | §5.1 참조 |

### 5.1 Zone Type별 정책 보조 표

| 순번 | 항목 | 정책 | 비고 |
|---:|---|---|---|
| 1 | INBOUND | 입고 작업 영역 | [TBD] |
```

### 8.2 추적 정보는 입력 제외 항목에 기록

```markdown
## 입력 제외 항목

1. Zone Type list 구조 분해
   - 카테고리: 구조 변환
   - 위치: 직접 입력
   - 인용: "INBOUND / STORAGE / OUTBOUND / RETURN / DEFECT"
   - 처리: 구조 분해 (본문 위치: 정책서 §5.1 / 부모 위치: 정책서 §5 row 7~11)
   - 설명: 단일 셀에 넣으면 정책 차이가 묻히므로 보조 표로 분해함
```

## 9. 대안 검토

| 대안 | 채택 여부 | 이유 |
|---|---|---|
| backlink 완전 제거 | 부분 채택 | 결정 문서 본문에서는 완전 제거한다. 단, 화면 output의 입력 제외 항목에는 추적 정보를 남길 수 있다. |
| 보조 표 내 주석 행으로 이동 | 비채택 | 표 데이터에 내부 메타데이터가 섞이고, Markdown source·복사본·파서에 계속 노출된다. |
| HTML comment로 숨김 | 비채택 | 렌더링에서는 숨을 수 있지만 source에는 남아 내부 추적 정보 노출 문제가 유지된다. |
| `--debug-trace` 옵션 추가 | 비채택 | 이번 변경은 출력 기본값 정리다. 별도 디버그 모드는 후속 후보로 남긴다. |
| 기존 backlink 유지 | 비채택 | 결정 문서 본문을 깨끗하게 유지한다는 기존 출력 정책과 충돌한다. |

## 10. 구현 영향 범위

- `skills/planning-format/references/conversion-rules.md` — §5.3을 clean header 규칙으로 변경. backlink는 헤더 금지로 이동.
- `skills/planning-format/references/exclusion-rules.md` — `구조 변환` 처리 줄에 `본문 위치` + `부모 위치` 형식 추가.
- `skills/planning-format/references/self-review-rules.md` — 신규 출력에서 legacy backlink 헤더를 syntax 발견으로 잡는 체크 추가.
- `skills/planning-format/references/output-contract.md` — 보조 표 예시와 설명에서 backlink 괄호 제거.
- `skills/planning-format/SKILL.md` — Step 6 요약과 참고 파일 설명에서 `헤더 backlink` 표현 제거 또는 0.2.8 clean header로 교체.
- `skills/planning-review/references/*` — 필요 시 보조 표 heading parser 설명을 legacy/new dual-read로 보강.
- `planning-kit/README.md` — 0.2.8 호환성/결과 형태 요약 반영.
- `planning-kit/.claude-plugin/plugin.json` / `.codex-plugin/plugin.json` — release 구현 시 version 0.2.8.
- `.claude-plugin/marketplace.json` / `.agents/plugins/marketplace.json` — release 구현 시 planning-kit version 갱신.
- `docs/prd/README.md` — 0.2.8 row 추가.

## 11. 수용 기준

1. `planning-format` 신규 출력의 모든 보조 표 헤더가 `### N.M [용도] 보조 표` 형식이며 `(§N row M)` 괄호가 없다.
2. 보조 표 번호 순차 부여와 max-depth=3 룰은 유지된다.
3. `구조 변환` 입력 제외 항목은 생성된 보조 표 위치를 `본문 위치`로 기록한다.
4. 부모 row를 식별할 수 있으면 `부모 위치`에 `§N row M` 또는 `§N row M~K`를 기록한다.
5. 부모 row를 식별할 수 없으면 `부모 위치`에 부모 §만 기록한다.
6. `--save`로 저장되는 정책서·기능설계서에는 backlink 메타데이터가 없다.
7. `planning-review`는 legacy `### N.M ... 보조 표 (§N row M)` 헤더와 신규 `### N.M ... 보조 표` 헤더를 모두 보조 표로 인식한다.
8. self-review는 신규 출력에 legacy backlink 헤더가 남으면 syntax 발견을 낸다.
9. `docs/prd/README.md`가 0.2.8을 최신 incremental PRD로 안내한다.

## 12. 용어

- **clean header**: 내부 추적 괄호 없이 독자가 읽는 제목만 남긴 보조 표 헤더.
- **legacy backlink header**: 0.2.4~0.2.7에서 사용한 `### N.M [용도] 보조 표 (§N row M)` 형식.
- **본문 위치**: 실제 보조 표가 생성된 정책서·기능설계서 위치.
- **부모 위치**: 보조 표 분해가 발생한 부모 § 또는 부모 row 위치.

그 외 용어는 0.2.7 §19 / 0.2.6 §17 / 0.2.5 §17 그대로.

## 13. 참고 파일

- `docs/prd/prd-0.2.7.md` — 본 PRD의 베이스.
- `docs/prd/prd-0.2.4.md` — legacy backlink 도입 근거.
- `skills/planning-format/references/conversion-rules.md` — 현재 backlink 규칙 위치.
- `skills/planning-format/references/exclusion-rules.md` — 구조 변환 처리 줄 위치.
- `skills/planning-format/references/output-contract.md` — 출력 블록과 보조 표 출력 예시.
- `skills/planning-format/references/self-review-rules.md` — syntax 검증 보강 대상.
- `docs/prd/prd-0.2.8.md` — 본 문서.
