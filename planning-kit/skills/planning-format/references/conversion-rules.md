# Conversion Rules

`planning-format` 변환 단계 (SKILL.md Step 4~6) 세부 룰. SKILL.md는 orchestration only이므로 multimodal 처리·통합 본문 합류·기능명 추출·라벨 매핑·list 분해 판단·보조 표 번호 부여·backlink는 모두 본 reference에 있다. SKILL.md Step 6 진입 시 1회 Read 적재.

## 1. 이미지 multimodal 처리 (Step 4)

지원 확장자: `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.bmp`, `.heic`, `.svg`. 크기·개수 cap 없음, resize 안 함. `.svg`는 raw XML + multimodal 해석 둘 다 시도.

이미지 시드 5경로:
1. 인자 파일 (이미지 확장자).
2. 디렉터리 안 지원 이미지 파일.
3. 본문 추출(markdown image / HTML img / 상대 경로 resolve).
4. fetch 응답이 image content-type일 때.
5. 본문 안 inline `data:image/...;base64,...` URI.

각 이미지에 대해 main이 multimodal 해석 — 안의 텍스트(라벨·캡션) 옮기고 다이어그램·플로우·화면 요소를 글로 기술. 추측은 `추정:` 접두. 결과는 `=== [출처 N] 이미지: <파일명 또는 URL> ===` 헤더와 함께 본문 합류.

실패(`미지원 이미지 포맷`/`image read 실패`/`빈 해석 결과`)는 출처 list에 사유 기록, 호출 종료 사유 아님.

## 2. 통합 본문 합류 (Step 5)

출처 단위로 `=== [출처 N] <원본 입력 / URL / 이미지 경로> ===` 헤더를 붙여 concat. 텍스트·파일·디렉터리 분기는 원본 입력이 항상 `[출처 0]`. URL 분기는 인자 URL이 `[출처 1..M]`. 자식 URL·이미지 해석은 visited 순서. 출처 헤더 자체는 변환 본문에 들어가지 않는다 (입력 마커일 뿐).

Google Sheets는 `connector-routing.md` §3.5 헤더 형식(gid·range 부연) 그대로.

## 3. 기능명 추출 (Step 6.1)

- URL 분기 (단일): 인자 URL의 페이지 `<title>` 또는 첫 `<h1>`.
- URL 분기 (다중): 첫 인자 URL title 우선.
- 텍스트·파일·디렉터리 분기: 입력에 명시된 주제 → 파일명 stem → 디렉터리명 → 본문 반복 제목 → 첫 핵심 명사구.

여러 기능 후보가 있으면 1순위 1개만. 그 외는 입력 제외 추적에 `다른 기능 후보` 사유로.

## 4. 두 템플릿 변환 (Step 6.2)

`templates/기능설계서.md` (8 섹션) + `templates/정책서.md` (10 섹션) Read 후 main이 같은 턴에 두 본문 작성.

라벨 매핑:
- 화면·흐름·동작·입력 항목·권한·예외 메시지 → 기능설계서.
- 규칙·조건·예외 승인·역할 책임·상태 전이·연동 정책 → 정책서.

**변환 본문(정책서·기능설계서)에 합류하지 않은 모든 입력 조각**은 `exclusion-rules.md` 11 카테고리 중 1개로 라벨링해 입력 제외 §에 기록 (라벨 미매핑·중복·범위 외·구조 변환·fetch 실패·원문 정의 부재·충돌 후보 등 사유 무관 catch-all). 근거 부족 셀은 inline `[TBD]`. 빈 row·빈 섹션 삭제 허용. **marker는 `[TBD]` 1종만** (`[미정]`/`[가정]`/`[확인 필요]`/`[충돌 후보]`/`해당 없음` 사용 금지).

## 5. list 분해 판단 (Step 6.2 sub-step)

### 5.1 룰

한 셀에 list 항목 ≥2 합류 작성 시, main이 항목별 속성(타입)·동작(클릭/overlay/non-MVP)·정책 ref(§ cross-link)·검증·[TBD]·non-MVP 등 이질성을 평가한다. 이질이면 부모 § 안 sub-§(`### N.x [용도] 보조 표`)로 분해(본 셀엔 `§N.x 참조` 1행만, 컬럼 set은 list 성격에 맞춰 main 결정, 권장 최소 = `순번`·`항목`·`비고`), 동질 enum·동일 동작·동일 ref면 합류 유지.

### 5.2 보조 표 번호 순차 부여 (0.2.4)

- 부모 § 안 보조 표 번호는 **순차 부여** — 첫 보조 표 = `§N.1`, 두 번째 = `§N.2`, ... `§N.M`.
- 다층 분해 시 도트 chain — `§4.1` 안 셀이 또 분해되면 `§4.1.1`, `§4.1.2`. 그 안이 또 분해되면 `§4.1.1.1` 식.
- 같은 부모 § 안 두 보조 표는 항상 다른 번호. 같은 번호 재사용 금지.
- 임의 letter (`§N.x`·`§N.x.y` placeholder) 사용 금지.

### 5.3 보조 표 헤더 backlink (0.2.4)

보조 표 헤더 형식:

```markdown
### 4.1 [용도] 보조 표 (§4 row 3)
```

- 괄호 안 `§N row M` = 부모 § 번호 + 분해 발생 row 위치.
- row 식별 못 하면 부모 §만 (`(§4)`).
- 다층 보조 표는 부모 보조 표 row 가리킴 (예: `(§4.1 row 2)`).

### 5.4 다층 분해

보조 표 안 셀이 다시 list 합류면 같은 룰 재귀 (`§N.M.K`). main 판단으로 깊이 결정. cap 없음.

### 5.5 예시

#### 분해 (Zone 조회 목록 컬럼 9종 — 이질)

```
체크박스 / Zone Code(clickable) / 존 이름 / Zone Type / 순서 / 연동 여부(non-MVP) / 귀속 로케이션 수(clickable) / 상태 / 수정 일시
```

→ 분해. clickable 2종·non-MVP 1종·타입 다양 → `§4.1` 보조 표 (`타입`·`동작 / 정책 ref`·`비고` 컬럼).

#### 합류 유지 (Zone Type enum — 동질)

```
INBOUND / STORAGE / OUTBOUND / RETURN / DEFECT
```

→ 합류 유지. 동질 enum, 동작·ref 동일.

#### 다층 분해 (정책서 §5 Zone 종류 — 2 layer)

§5 row 분해된 INBOUND row 안 `Dock ZN / RECEIVING ZN / BUFFER ZN / CROSS_DOCK ZN` 셀이 또 이질(BUFFER ZN = 출고 불가, RECEIVING ZN = 과/부족입고, CROSS_DOCK ZN = 가용 재고 제외) → §5.1 보조 표 (1차) + §5.1.1 보조 표 (다층).

판단 형식화(Q-list·체크리스트·카운트 룰) 없음 — main 자유 판단.

## 6. 8/10 섹션 골격

8/10 섹션 골격은 변경 없음. sub-§(`### N.M ... 보조 표`)만 동적 추가.
