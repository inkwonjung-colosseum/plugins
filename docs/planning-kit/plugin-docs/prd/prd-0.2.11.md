# planning-kit PRD 0.2.11

> 0.2.10 기반 incremental PRD. 0.2.10은 결정 보드로 상단 가독성을 개선했지만, 실제 Zone 관리 출력에서는 `정책서 §5.1`, `§9.1 시나리오`, `입력 제외 §`, `sub-§` 같은 섹션 기호가 사용자 화면 전반에 남았다. 이 표기는 내부 reference 문서나 parser 구현에는 짧고 편하지만, PM/현업/기획/QA가 읽는 최종 결과에서는 기호 자체를 다시 해석해야 하므로 가독성을 떨어뜨린다.
>
> 핵심 변경: `planning-format`과 `planning-review`의 사용자-facing 출력, 생성 문서 본문, 상세 추적 표시에서는 `§` 기호를 쓰지 않는다. 섹션 위치는 `정책서 5.1`, `기능설계서 4.5`, `원문 9.1`, `입력 제외 섹션`, `보조 표`처럼 사람이 읽는 표현으로 렌더링한다. 기존 0.2.10 이하 산출물과 reference 문서에 남은 `§` 표기는 legacy 입력으로 계속 인식하되, 새 출력에는 재노출하지 않는다.

## 1. 변경 요약

1. **사용자 화면에서 섹션 기호 제거** — 최종 응답의 결정 보드, 정책서, 기능설계서, 검증 피드백, 출처 요약, 입력 제외 요약, 상세 추적에 `§` 기호를 출력하지 않는다.
2. **생성 문서 heading 정리** — 보조 표 heading은 `### 5.1 Zone Function 보조 표`처럼 번호만 사용한다. `### §5.1 ...`, `§5.1 참조` 형태는 신규 생성 금지다.
3. **위치 표기 표준화** — `정책서 §5.1`, `기능설계서 §7`, `출처 #1 §9.1`을 각각 `정책서 5.1`, `기능설계서 7`, `출처 1의 9.1`처럼 렌더링한다.
4. **용어 표기 표준화** — `입력 제외 §`, `미결 §`, `sub-§`, `부모 §` 같은 내부 축약어는 사용자-facing 출력에서 `입력 제외 섹션`, `미결 사항 섹션`, `보조 표`, `상위 섹션`으로 바꾼다.
5. **legacy 읽기 호환 유지** — `planning-review`와 downstream parser는 기존 산출물의 `§5.1`, `sub-§`, `입력 제외 §`를 계속 읽는다. 이 변경은 렌더링 규칙 변경이며 legacy parser 제거가 아니다.
6. **내부 문서 정리 기준 분리** — SKILL/reference 문서에 남은 `§`도 사용자 출력 템플릿·예시·규칙을 설명하는 줄에서는 제거한다. 단, legacy 호환 설명이나 과거 PRD 인용에는 제한적으로 남길 수 있다.

## 2. 동기

Zone 관리 v0.9 변환 결과에서 다음 문제가 확인됐다.

- `D1`/`D2`의 반영 위치가 `정책서 §5.1`, `기능설계서 §7`처럼 표시되어, 업무 담당자가 문서 번호와 기호를 함께 해석해야 했다.
- `상세 추적`과 `입력 제외 항목`에서 `§9.1 시나리오 1·2`, `입력 제외 §`, `미결 §` 같은 표현이 반복되어 결과 화면이 내부 로그처럼 보였다.
- 0.2.8에서 보조 표 heading의 legacy backlink는 제거했지만, 번호 자체와 참조 문구에는 `§`가 계속 남아 최종 화면의 정리는 끝나지 않았다.
- 기호는 parser 구현자에게는 짧지만, 기획/현업 공유 문서에서는 "이 아이콘이 꼭 필요한가"라는 질문을 만들 정도로 업무 언어가 아니다.

0.2.11의 목적은 섹션 추적 정보를 줄이는 것이 아니다. 같은 정보를 유지하되, 최종 화면에서는 기호 없는 자연어 위치 표기로 바꾸는 것이다.

## 3. 비목표

- 정책서·기능설계서의 섹션 번호 체계 자체를 없애지 않는다.
- `## 정책서`, `## 기능설계서`, `## 상세 추적` 같은 wrapper heading 계약을 바꾸지 않는다.
- `planning-review`가 legacy `§` 표기를 읽는 호환 로직을 제거하지 않는다.
- 과거 PRD 파일 전체에서 `§`를 일괄 삭제하지 않는다. 과거 PRD는 당시 계약 기록으로 남긴다.
- 원문 직접 인용 안에 포함된 `§` 기호를 의미 변경해 고치지 않는다. 단, 인용 밖의 위치/처리/설명 필드는 clean display를 사용한다.
- 링크 anchor나 URL fragment를 바꾸지 않는다. URL 자체에 필요한 기호나 encoding은 그대로 둔다.

## 4. 출력 원칙

### 4.1 기본 원칙

사용자-facing 출력에는 `§` 기호를 쓰지 않는다.

대상:

- `planning-format` 최종 응답 전체
- `planning-review` 최종 응답 전체
- `planning-format --save`로 생성되는 정책서·기능설계서 본문
- `planning-review`가 화면에 재표시하는 위치, 발견, 백로그, 상세 추적
- README와 사용 예시 중 실제 사용자 출력 예시

허용 예외:

- 원문 직접 인용 안에 실제로 들어 있는 `§`
- legacy 입력 호환을 설명하는 reference 문서의 "읽기 호환" 문맥
- 과거 PRD의 역사적 계약 설명
- regex, parser fixture, migration note처럼 기호 자체를 테스트 대상으로 설명하는 경우

허용 예외도 기본 사용자 화면에 노출되면 안 된다.

### 4.2 위치 표기 변환

| 기존 표기 | 신규 사용자-facing 표기 |
|---|---|
| `정책서 §5.1` | `정책서 5.1` |
| `기능설계서 §7` | `기능설계서 7` |
| `정책서 §5·§6` | `정책서 5, 6` |
| `정책서 §6·§9, 기능설계서 §5` | `정책서 6, 9 / 기능설계서 5` |
| `출처 #1 §9.1` | `출처 1의 9.1` |
| `입력 제외 §` | `입력 제외 섹션` |
| `미결 §` | `미결 사항 섹션` |
| `sub-§` | `보조 표` |
| `부모 §` | `상위 섹션` |
| `§5.1 참조` | `5.1 참조` |

규칙:

- 번호는 유지한다. `5.1` 자체는 섹션 식별자이므로 삭제하지 않는다.
- 문서명이 있으면 문서명과 번호를 함께 쓴다. 예: `정책서 5.1`.
- 문서명이 없고 원문 위치를 가리키면 `원문 9.1`, `출처 1의 9.1`처럼 쓴다.
- 여러 섹션은 `정책서 6, 9`처럼 쉼표로 묶는다. 서로 다른 문서는 `/`로 구분한다.
- `row`, `행`, `보조 표 안` 같은 세부 위치는 기호 없이 유지한다. 예: `정책서 5.1 row 3 (보조 표 안)`.

### 4.3 보조 표 heading

신규 `planning-format` 출력과 저장 파일의 보조 표 heading은 다음 형식만 허용한다.

```markdown
### 5.1 Zone Function 보조 표
### 4.5 귀속 로케이션 목록 보조 표
```

금지:

```markdown
### §5.1 Zone Function 보조 표
### 5.1 Zone Function 보조 표 (§5 row 7)
§5.1 Layer별 Zone Function 보조 표
```

보조 표를 본문에서 참조할 때도 `5.1 참조` 또는 `아래 5.1 보조 표 참조`로 쓴다.

### 4.4 상세 추적

상세 추적은 debug 정보가 아니라 사용자가 검토할 수 있는 감사 trail이다. 따라서 상세 추적에서도 `§` 기호를 쓰지 않는다.

예:

```markdown
### 입력 제외 항목

1. Zone Type 설정 시나리오 1·2 화면 기획 상세
   - 카테고리: 범위 외
   - 위치: 출처 1의 9.1
   - 인용: "Zone Type 설정 관리 > Zone Type 선택 ..."
   - 처리: 명시 제외 (정책서 2 / 기능설계서 2 참조)
   - 설명: 플랫폼 도메인 화면 기획으로 Tenant 도메인 Zone 관리 범위 밖이다.
```

상세 추적 안의 `처리` 줄도 같은 규칙을 따른다.

## 5. `planning-format` 변경

### 5.1 변환 본문

`planning-format`이 생성하는 정책서·기능설계서 본문에서 다음을 적용한다.

- section heading, 보조 표 heading, 본문 참조에 `§`를 쓰지 않는다.
- `정책서 5.1`, `기능설계서 4.5`, `5.1 참조`처럼 번호만 사용한다.
- `입력 제외 섹션`, `미결 사항 섹션`, `보조 표` 같은 자연어를 사용한다.
- 원문에 `§`가 포함된 직접 인용은 그대로 두되, 인용 밖 해설은 clean display로 작성한다.

### 5.2 결정 보드

결정 보드의 `반영 위치`, `대상`, `연결`, `릴리즈 차단 항목` 필드는 clean display를 사용한다.

예:

```markdown
- 반영 위치: 정책서 5.1, 6 / 기능설계서 7
- 대상: 기능설계서 4.5 Zone 상세 귀속 로케이션 목록 컬럼
- 연결: 관련 발견 2건 (상세 추적의 결정 보드 연결 맵에서 D1로 확인)
```

금지:

```markdown
- 반영 위치: 정책서 §5.1, §6 / 기능설계서 §7
- 대상: 기능설계서 §4.5 Zone 상세 귀속 로케이션 목록 컬럼
```

### 5.3 입력 제외 요약과 상세 추적

`본문 반영에 영향 있는 항목`, `원문 정의 부재 [TBD] 위치`, full 입력 제외 list의 `위치`, `처리`, `설명`은 모두 clean display를 사용한다.

예:

```markdown
- 원문 정의 부재 [TBD] 위치: 정책서 5.1 Refurbish ZN 재고 속성 / 기능설계서 4.5 귀속 로케이션 추가 컬럼
```

## 6. `planning-review` 변경

### 6.1 입력 parsing

`planning-review`는 다음 입력을 모두 같은 위치로 normalize한다.

| 입력 | normalize 결과 |
|---|---|
| `정책서 §5.1` | `정책서 5.1` |
| `정책서 5.1` | `정책서 5.1` |
| `§5.1 보조 표` | `5.1 보조 표` |
| `sub-§` | `보조 표` |

내부 matching에는 기존 section id를 써도 된다. 단, 사용자에게 다시 출력할 때는 clean display를 사용한다.

### 6.2 발견과 백로그

`위치`, `대상`, `완료 조건`, `검증 방법`, `반영 위치`에는 `§` 기호를 쓰지 않는다.

예:

```markdown
- 위치: 정책서 5.1 row 3 (보조 표 안) vs Product SSOT/zone.md 2
- 대상: 정책서 9.1 이동 통제 매트릭스
- 완료 조건: 정책서 9.1에 모든 Zone Type 이동 조합의 기대값이 명시됨
```

### 6.3 legacy summary

0.2.10에서 유지한 `## 최우선 수정 항목`, `## 작업 백로그` 호환용 요약도 clean display를 사용한다. legacy consumer 호환은 heading 이름과 구조로 보장하고, `§` 기호로 보장하지 않는다.

## 7. Reference 문서 정리 기준

SKILL.md와 references 문서는 다음 기준으로 정리한다.

| 문맥 | 처리 |
|---|---|
| 사용자 출력 템플릿 | `§` 제거 |
| 사용자 출력 예시 | `§` 제거 |
| 생성 문서 작성 규칙 | `§` 제거 |
| parser legacy 입력 호환 설명 | 제한적으로 허용 |
| 과거 버전과 비교하는 migration note | 제한적으로 허용 |
| regex/fixture에서 legacy 기호 자체를 테스트 | 제한적으로 허용 |
| PRD 0.2.10 이하 역사적 본문 | 변경 불필요 |

구현 시 `planning-kit/skills/**`에서 `§` 검색 결과가 남아도 실패로 보지 않는다. 다만 남은 항목은 위 표의 허용 문맥이어야 하며, 사용자-facing 출력 규칙이나 예시에 남아 있으면 실패다.

## 8. 호환성

변경 성격: incremental, 출력 markdown micro-breaking.

영향:

- downstream parser가 `정책서 §5.1` 문자열만 location으로 찾는 경우 `정책서 5.1`도 허용해야 한다.
- 사람이 읽는 화면에서는 더 자연스러워지지만, 기존 정규식 기반 location matcher는 두 표기를 모두 받도록 수정해야 한다.
- `planning-review`는 legacy `§` 입력을 계속 읽어야 하므로 기존 산출물 review는 깨지지 않는다.
- `--save` 산출물의 heading이 clean display로 바뀌어도 섹션 번호와 heading level은 유지되므로 문서 구조는 보존된다.

마이그레이션 규칙:

1. 읽기 단계: `§?(\d+(?:\.\d+)*)`를 모두 section id로 인식한다.
2. 내부 처리: section id는 숫자 chain으로 normalize한다.
3. 출력 단계: `§` 없이 `문서명 + 공백 + section id`로 렌더링한다.

## 9. 구현 대상

필수:

- `planning-kit/skills/planning-format/SKILL.md`
- `planning-kit/skills/planning-format/references/conversion-rules.md`
- `planning-kit/skills/planning-format/references/exclusion-rules.md`
- `planning-kit/skills/planning-format/references/output-contract.md`
- `planning-kit/skills/planning-format/references/self-review-rules.md`
- `planning-kit/skills/planning-review/SKILL.md`
- `planning-kit/skills/planning-review/references/ac-rules.md`
- `planning-kit/skills/planning-review/references/deps-rules.md`
- `planning-kit/skills/planning-review/references/ssot-rules.md`
- `planning-kit/README.md`
- `planning-kit/docs/prd/README.md`

선택:

- `planning-kit/docs/prd/fixtures/prd-0.2.10-fixtures.yml`의 display expectation을 0.2.11 fixture로 복제·갱신
- 예시 문서와 workflow 문서의 사용자 출력 예시 갱신

비대상:

- 0.2.10 이하 과거 PRD 본문 일괄 수정
- legacy input parser 제거

## 10. 수용 기준

### 10.1 Zone 관리 출력

Zone 관리 v0.9와 같은 입력에서 신규 `planning-format` 출력은 다음을 만족한다.

- 최종 사용자 응답에 `§` 기호가 없다. 단, 원문 직접 인용 안에 실제 기호가 있는 경우만 예외다.
- `D1` 반영 위치는 `정책서 5.1, 6 / 기능설계서 7`처럼 표시된다.
- `A1` 대상은 `기능설계서 4.5 Zone 상세 귀속 로케이션 목록 컬럼`처럼 표시된다.
- `§5.1 Layer별 Zone Function 보조 표` 대신 `### 5.1 Layer별 Zone Function 보조 표`가 나온다.
- `입력 제외 §` 대신 `입력 제외 섹션` 또는 `입력 제외 항목`이 나온다.
- `처리: 명시 제외 (정책서 §2 / 기능설계서 §2 참조)` 대신 `처리: 명시 제외 (정책서 2 / 기능설계서 2 참조)`가 나온다.

### 10.2 Review 호환

`planning-review`는 다음을 모두 통과해야 한다.

- legacy 입력 `정책서 §5.1`, `기능설계서 §7`, `sub-§`를 읽어 같은 위치로 매칭한다.
- 신규 clean 입력 `정책서 5.1`, `기능설계서 7`, `보조 표`도 같은 위치로 매칭한다.
- review 결과 출력에는 `§` 기호가 없다. 단, 원문 직접 인용 안은 예외다.
- `## 최우선 수정 항목`, `## 작업 백로그` heading은 유지된다.

### 10.3 Reference 정리

구현 후 검색 기준:

```text
rg -n "§" planning-kit/skills/planning-format planning-kit/skills/planning-review planning-kit/README.md
```

남은 항목은 다음 중 하나여야 한다.

- legacy 입력 호환 설명
- legacy bad example
- regex/fixture/migration note
- 과거 버전과의 비교 설명

사용자-facing 출력 템플릿, 신규 출력 예시, 생성 문서 작성 규칙에는 남으면 실패다.

## 11. 검증 계획

1. `planning-kit` skill/reference 문서에서 `§` 사용처를 분류한다.
2. 사용자-facing 출력 템플릿과 예시를 clean display로 바꾼다.
3. parser/read compatibility 문맥은 legacy 허용 문구로 좁힌다.
4. Zone 관리 예시를 기준으로 `planning-format` expected output을 점검한다.
5. legacy `§`가 포함된 0.2.10 산출물을 `planning-review` 입력으로 넣어 review가 깨지지 않는지 점검한다.
6. README PRD chain과 필요 시 fixture를 갱신한다.

## 12. 예시

### 12.1 변경 전

```markdown
- 반영 위치: 정책서 §5.1 RETURN Zone Function, §6 상태 처리, 기능설계서 §7 RETURN Zone 이동 완료 메시지
- 대상: 기능설계서 §4.5 Zone 상세 귀속 로케이션 목록 컬럼
- 위치: [출처 1] §9.1 시나리오 1, 2
- 처리: 명시 제외 (정책서 §2 / 기능설계서 §2 참조)
```

### 12.2 변경 후

```markdown
- 반영 위치: 정책서 5.1 RETURN Zone Function, 6 상태 처리 / 기능설계서 7 RETURN Zone 이동 완료 메시지
- 대상: 기능설계서 4.5 Zone 상세 귀속 로케이션 목록 컬럼
- 위치: 출처 1의 9.1 시나리오 1, 2
- 처리: 명시 제외 (정책서 2 / 기능설계서 2 참조)
```

## 13. 릴리즈 노트 초안

`planning-kit` 0.2.11은 사용자 화면과 생성 문서에서 `§` 섹션 기호를 제거합니다. 섹션 번호와 추적 정보는 유지하되 `정책서 5.1`, `기능설계서 7`, `입력 제외 섹션`처럼 읽기 쉬운 표기로 출력합니다. 기존 `§5.1` 표기를 포함한 0.2.10 이하 산출물은 계속 review 입력으로 사용할 수 있습니다.
