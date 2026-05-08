# planning-kit PRD 0.2.3

> 0.2.2 기반 incremental PRD. 단일 변경 — `planning-format` 표 셀 안 list 항목을 main이 매 케이스 판단해 보조 표(`§N.x`)로 분해하거나 합류 유지한다. 본 PRD에서 다루지 않는 명세는 [`prd-0.2.2.md`](./prd-0.2.2.md) 이하 chain 그대로.

## 1. 변경 요약

한 가지 변경:

- **planning-format §6.2에 list 분해 판단 sub-step 추가** — 한 셀에 list 항목 ≥2 합류 작성 시, main이 항목별 속성·동작·정책 ref 이질성을 평가해 분해/합류 결정. 분해 시 부모 § 안 sub-§(`§N.x`)로 보조 표 작성, 컬럼 set은 list 성격에 맞춰 main 결정. 동질 enum·동일 동작·동일 ref면 합류 유지.

룰 형식화 (Q-list·카운트·sub-check·헤더 메타라인) 의도적 배제. 판단 = main에 위임.

## 2. 동기

0.2.2까지 운영 패턴:

- 기능설계서 §4·§5, 정책서 §5·§6 등에서 입력 측이 list 형태(컬럼 list, Zone 종류 list, 권한 list)를 줄 때 한 셀에 slash·comma 합류 경향.
- AI 입장 lossless. 사람 입장 시각 파싱 비용↑ + 항목별 속성(타입·동작·ref) 추가 자리 부재.
- F1·F5 모두 catch 못함 → 사일런스 통과.

원인 = template skill 비대칭 (빈 row·빈 § 삭제 허용 / 신규 sub-§ 생성 명시 부재). main이 "신규 § 추가 안 하는 게 안전" 보수 default 선택.

판단 위임 (카운트 룰 X) 로 해결 — list 항목이 이질이면 분해, 동질이면 합류. 매 케이스 main 판단.

## 3. 비목표

- `planning-review`·connector·multimodal·재귀 fetch·입력 제외 § 동작 변경 없음.
- 카운트 기반 강제 분해 룰 미도입 (`≥3 자동` 등).
- 분해 판단 형식화 (Q1~Q4·체크리스트) 미도입. main 자유 판단.
- 보조 표 컬럼 set 표준 강제 안 함.
- 8/10 섹션 골격 변경 없음. 보조 §은 main이 작성 시 동적 추가만.
- F1~F6 sub-check 추가 없음. 작성 단계 판단 = main, 검증 단계 판단 = main이라 retro catch 별도 sub-check 무가치.
- 출력 헤더에 `보조 표:` 같은 메타라인 추가 안 함. 분해 결과는 본문 자체로 가시.
- 인자·옵션 추가 없음 (`--no-aux-table` 같은 봉쇄 옵션 X).
- template 가이드 코멘트 삽입 안 함. SKILL.md 룰 명시만으로 충분.

## 4. list 분해 판단

### 4.1 룰

```
한 셀에 list 항목 ≥2 합류 작성 시, main이 항목별 속성(타입)·동작(클릭/overlay/non-MVP)·정책 ref(§ cross-link)·검증·[TBD]·non-MVP 등 이질성을 평가한다. 이질이면 부모 § 안 sub-§(`§N.x`)로 보조 표 분해, 동질 enum·동일 동작·동일 ref면 합류 유지.
```

### 4.2 보조 표 형식

분해 결정 시 본 § 다음 줄에 `### N.x [용도] 보조 표` 헤더 + 표. 컬럼 set은 list 성격에 맞춰 main 결정. 권장 최소 컬럼 = `순번`·`항목`·`비고`. 본 셀에는 `§N.x 참조` 1행만 남김.

### 4.3 다층 분해

부모 § row 단위로 1차 분해된 표 안의 셀이 다시 list 합류면 같은 룰 재귀 적용. 즉 보조 표(`§5.1`) 안 셀이 다시 이질 list면 sub-보조 표(`§5.1.1`) 작성 가능. main 판단으로 깊이 결정. cap 없음.

### 4.4 예시

#### 분해 (Zone 조회 목록 컬럼 9종 — 이질)

```
체크박스 / Zone Code(clickable) / 존 이름 / Zone Type / 순서 / 연동 여부(non-MVP) / 귀속 로케이션 수(clickable) / 상태 / 수정 일시
```

→ 분해. clickable 2종·non-MVP 1종·타입 다양 → `§4.x` 보조 표 (`타입`·`동작 / 정책 ref`·`비고` 컬럼).

#### 합류 유지 (Zone Type enum — 동질)

```
INBOUND / STORAGE / OUTBOUND / RETURN / DEFECT
```

→ 합류 유지. 동질 enum, 동작·ref 동일.

#### 다층 분해 (정책서 §5 Zone 종류 — 2 layer)

§5 row 분해된 INBOUND row 안 `Dock ZN / RECEIVING ZN / BUFFER ZN / CROSS_DOCK ZN` 셀이 또 이질(BUFFER ZN = 출고 불가, RECEIVING ZN = 과/부족입고, CROSS_DOCK ZN = 가용 재고 제외) → §5.1 보조 표.

## 5. SKILL.md / reference 갱신

| 파일 | 변경 |
|---|---|
| `skills/planning-format/SKILL.md` | §6.2에 §4.1 룰 + §4.2 보조 표 형식 + §4.3 다층 명시. 출력 포맷 §의 본문 예시에 sub-§(`### N.x ... 보조 표`) 1 case 추가. |
| `.codex-plugin/plugin.json` / `.claude-plugin/plugin.json` | version 0.2.2 → 0.2.3. description에 "표 셀 list 분해 판단" 1줄. |
| `README.md` | 결과 형태 §에 sub-§ 보조 표 패턴 1줄. 호환성 §에 0.2.2 → 0.2.3 1줄. |
| `docs/prd/README.md` | 0.2.3 row 추가 (incremental, 베이스 0.2.2). |
| `docs/prd/prd-0.2.3.md` | 본 문서. |

추정 line 증가:
- `planning-format/SKILL.md`: ~15 line.
- README: ~5 line.
- `docs/prd/README.md`: ~1 line.

`planning-review` 측 0건. self-review-rules.md 0건. template 0건.

## 6. 호환성

- 0.2.2 → 0.2.3: 출력 markdown **추가만** (본문 안 sub-§). 기존 형식 변경·제거 없음 → micro-breaking 아님.
- `planning-review` 변경 없음. 0.2.3 산출물을 review에 입력 시 sub-§은 부모 § 안 내용 일부로 corpus 비교 대상에 자연 포함. R1·R3 변경 없음.
- 0.2.2 산출물(보조 § 부재) 호환성 그대로. 입력 측 합류 셀은 main이 변환 시 다시 판단.
- 다운스트림 파서: 부모 § 안 sub-§ 신규. 8/10 섹션 골격 파싱 코드는 sub-§을 child로 인식해야 함.

## 7. 검증 시나리오

PRD 검수 시점 main이 트레이스:

1. **이질 list 셀 → 분해**: §4.4 분해 예시 case (Zone 조회 목록 9종). 보조 표 `§4.x` 작성, 본 셀 `§4.x 참조`.
2. **동질 list 셀 → 합류 유지**: §4.4 합류 예시 case (Zone Type 5 enum). slash 합류 그대로. 보조 표 미작성.
3. **0.2.2 산출물 호환**: 보조 § 부재 입력 → main이 다시 판단해 분해 결정 시 새 sub-§ 추가, 합류 결정 시 그대로 유지. sanity check 아님.
4. **다층 분해**: §5 row 분해된 표 안 셀이 다시 이질 list → §5.1 + §5.1.1 sub-보조 표.

## 8. 성공 기준

- `planning-format`이 list 합류 셀 작성 시 항목 이질성을 매 케이스 판단해 분해/합류 결정한다.
- 분해 시 부모 § 안 sub-§(`§N.x`)에 보조 표 등장.
- 동질 enum·동일 동작·동일 ref는 합류 유지가 default.
- 카운트 기반 강제 분해 미발생.
- `planning-review`·connector·multimodal·재귀 fetch·입력 제외 § 동작 변경 없음.
- 인자 변경 없음. 출력 헤더 메타라인 추가 없음.

## 9. 용어 추가

- **list 분해 판단**: `planning-format` 변환 단계에서 한 셀에 list 항목 ≥2 합류 작성 시 항목 이질성을 평가해 분해/합류를 결정하는 절차. main 자유 판단.
- **보조 표**: 분해 결정 시 부모 § 안 sub-§(`§N.x`)로 작성하는 분리 표. 컬럼 set 가변. 다층 분해 가능.

그 외 모든 용어는 0.2.2 §14 그대로.

## 10. 참고 파일

- `skills/planning-format/SKILL.md` — §4.1·§4.2·§4.3 반영.
- `.claude-plugin/plugin.json` / `.codex-plugin/plugin.json` — version 0.2.3.
- `README.md` — 결과 형태·호환성 §.
- `docs/prd/README.md` — 0.2.3 row.
- `docs/prd/prd-0.2.3.md` — 본 문서.
