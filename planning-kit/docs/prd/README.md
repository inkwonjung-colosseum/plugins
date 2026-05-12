# planning-kit PRD chain

planning-kit PRD 18건의 관계·읽는 순서·핵심 변경 1줄 요약을 한 문서로 가이드.

> 주의: `prd-0.2.14.md`는 0.2.13에서 0.2.14로 넘어가기 위한 목표 계약이다. runtime/설치 표면은 manifest, marketplace/cache 동기화와 검증 결과를 함께 확인해 판단한다.

## 읽는 순서

- **신규/구현자**: 본 README → `prd-0.2.14.md` → (필요 시) 역방향으로 상위 PRD 참고. 각 PRD 본문에 베이스가 명시돼 있어 chain 추적 가능.
- **기존 사용자**: 신규 PRD만 읽으면 충분 — 각 PRD가 incremental 베이스를 명시한다.

## PRD 관계도

| PRD | 관계 | 베이스 | 핵심 변경 (1줄) |
|---|---|---|---|
| 0.1.0 | base | (없음) | formalize 단일 스킬 — 텍스트·파일·디렉터리 입력 → 정책서·기능설계서 변환 + 자동 리뷰 (A·B축) |
| 0.1.1 | incremental | 0.1.0 | URL 분기·재귀 fetch·이미지 multimodal·SSOT 검색 키워드 노출 |
| 0.1.2 | incremental | 0.1.1 | connector fallback (Atlassian·Figma·Slack·Notion) + 인증 게이트 휴리스틱 |
| 0.2.0 | **breaking** | 0.1.2 | formalize 분할 → planning-format + planning-review. F6 markdown lint 추가. `--save` 옵션. Google Workspace 자원별 tool 시퀀스 |
| 0.2.1 | incremental | 0.2.0 | 입력 제외 § 카테고리 5 → 10종 + 항상 출력 + 처리 줄 + 헤더 분포 + F5 cross-ref 3종 |
| 0.2.2 | incremental | 0.2.1 | R1 SSOT corpus link follow + planning-review 입력 제외 § 인지 + Codex desc 압축 + README 비교표 갱신 + PRD chain 안내 |
| 0.2.3 | incremental | 0.2.2 | planning-format 표 셀 list 분해 판단 (main 자유 판단, Q-list·카운트 룰 X) + 부모 § 안 sub-§(`### N.x` 보조 표) 동적 추가, 다층 재귀 분해 지원 |
| 0.2.4 | incremental | 0.2.3 | sub-§ 정밀화(번호 순차 §N.1·§N.2 + 헤더 backlink + 구조 변환 처리 줄 sub-§ 위치) + F1·F2·R1·R2·R3 sub-§ 인식 + SKILL.md 분해(orchestration only + 3 reference lazy read) + 입력 제외 § 위치 markdown link + 출처 list URL deep link + Confluence·Docs·Slides·Notion anchor 추출 + 충돌 후보 카테고리(11종) |
| 0.2.5 | incremental | 0.2.4 | 결정성 강화 7 항목 — fetch 시도 의무화(`--no-fetch` 외 미시도 금지) + BFS 순서 강제(depth + 발견 순서) + exclusion 11 카테고리 결정 트리(라벨 미매핑 폴백) + 모호성 강제 [TBD](정규식 6 패턴 + 16 어구) + list 분해 max-depth cap=3 + self-review 6패스 26 항목 체크리스트 + 라벨 매핑 결정 트리 + 양 매핑 분배 룰. 같은 입력 일치율 0.9% → 25~39%로 28~43배 개선 |
| 0.2.6 | incremental | 0.2.5 | planning-review 입력 처리 parity — 다중 URL 입력 허용 + planning-format과 같은 input dispatch·재귀 fetch·connector fallback·image multimodal·통합 본문 합류 + `--no-input-fetch` / `--no-input-image` + `## 입력 출처` 블록. 입력 fetch와 SSOT corpus link follow는 별도 visited set·출처 블록으로 분리 |
| 0.2.7 | incremental | 0.2.6 | 신규 `ssot-audit` 스킬 — 프로젝트 전체 `*.md` + 외부 링크 follow corpus를 구조·내용 2축으로 감사하고 backlog를 화면 output only로 제공. `planning-review` 단일 파일 입력은 같은 폴더 sibling companion read로 정책서·기능설계서 쌍을 식별 |
| 0.2.8 | incremental | 0.2.7 | planning-format 보조 표 헤더 backlink 제거 — `### N.M [용도] 보조 표` clean header만 신규 출력하고, 부모 §/row 추적은 `## 입력 제외 항목`의 `구조 변환` 처리 줄로 이동. legacy backlink 헤더는 읽기 호환 유지 |
| 0.2.9 | incremental | 0.2.8 | planning-format + planning-review 출력 품질 개선 — 진행 로그 제거, readable 결정 문서 우선 출력, 자체 검증 피드백 우선, review 판정/신뢰도/액션 backlog 우선 출력, `--save` 경로 `planning/` 고정, `planning/**` SSOT 제외 |
| 0.2.10 | incremental | 0.2.9 | 상단 결정 보드 도입 — `planning-format`은 사용자 확인·릴리즈 차단 항목이 있을 때 조건부로, `planning-review`는 항상 `## 결정 보드`를 출력한다. 외부 결정 필요 P0/P1을 `D*` 결정 항목과 `A*` 실행 백로그로 묶고, 독립 차단은 필요 시 `T*`로 별도 추적. 결정 질문·선택지·완료 조건·검증 방법·담당/결정 필요자를 먼저 표시하고 원시 발견 ID는 상세 추적으로 내린다. `planning-review`의 top-level `## 최우선 수정 항목`·`## 작업 백로그`는 0.2.x 호환용 요약으로 유지 |
| 0.2.11 | incremental | 0.2.10 | 사용자-facing 섹션 기호 제거 — `planning-format`과 `planning-review`의 최종 화면, 생성 문서, 상세 추적에서 `§`를 쓰지 않고 `정책서 5.1`, `기능설계서 7`, `입력 제외 섹션`, `보조 표`처럼 clean display로 출력한다. legacy `§5.1` 입력은 계속 읽기 호환으로 유지한다 |
| 0.2.12 | incremental | 0.2.11 | 결과 인지성 개선 — `planning-format`은 본문 앞에 항상 `## 생성 결과 요약`을 출력해 문서 생성 결과·검증 상태·확인 필요·출처 영향을 먼저 보여주고, `planning-review`는 `## 결정 보드`를 유일한 실행 기준으로 선언해 legacy `## 최우선 수정 항목`·`## 작업 백로그`의 중복 상세를 최소화한다 |
| 0.2.13 | incremental | 0.2.12 | 신규 `planning-publish-confluence` 스킬 — 현재 context memory에 정책서·기능 설계서 두 본문이 모두 명확히 있을 때만 Product Team Space SSOT 하위에 `v0.7` label이 붙은 기능 container와 두 child page를 발행한다. 기본 SSOT parent를 제안하되 AskUserQuestion으로 parent URL 직접 입력과 취소를 지원하고, 중복 title과 최종 쓰기 확인을 강제한다 |
| 0.2.14 | incremental | 0.2.13 | `planning-format`·`planning-review` 결과 우선 출력 + `planning-publish-confluence` 저장 폴더 입력 — 신규 public 출력에서 상단 `생성 결과 요약`과 `결정 보드`를 제거한다. `planning-format`은 기본적으로 로컬 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/`에 저장하고 화면에는 `저장 파일`과 `체크해야 할 항목`만 보여준다. 정책서·기능설계서 전문을 화면에 펼치려면 파일 저장하지 않는 `--no-save`를 사용한다. `planning-review`는 바로 `결론`과 `검토 결과`를 보여준다. `planning-publish-confluence`는 무인자 context-body 발행을 유지하고, 명시적 저장 폴더 입력 시 canonical 정책서·기능설계서 두 파일만 읽는다. 미확정·누락·보강점은 하단 `체크해야 할 항목`으로 모으며, 기존 검증·출처·입력 제외 상세는 `출처/누락 요약`, `검토 근거 요약`, 조건부 `상세 추적`으로 재배치한다 |

## 호환성 요약

- **0.1.x → 0.2.0**: **breaking** (스킬 이름 변경 + 분할). 호출자 마이그레이션 필요 — `formalize` → `planning-format` + 선택적 `planning-review`.
- **그 외**: incremental, 출력 markdown micro-breaking 가능 (다운스트림 파서 영향 시 각 PRD 호환성 절 참조). 0.2.10부터 `## 결정 보드` wrapper heading이 추가되므로 parser는 첫 H2를 산출 본문으로 가정하지 말고 줄 시작의 정확한 `## 정책서`/`## 기능설계서` 경계를 찾아야 한다. legacy `planning-review`에서는 첫 `## 결론` 전의 첫 `## 결정 보드`만 metadata로 취급한다. fenced code block·blockquote·리스트 하위의 `## 결정 보드` 문자열은 wrapper로 취급하지 않는다. duplicate/misplaced decision board는 body에서 제외하고 `readable projection boundary ambiguous` warning으로 처리한다. 0.2.11부터 출력 위치 표기는 `정책서 5.1`과 같은 clean display가 기본이며, parser는 legacy `정책서 §5.1`과 clean display를 모두 읽어야 한다. 0.2.12부터 legacy `planning-format` 화면 출력의 `## 생성 결과 요약`은 메타데이터 영역으로 취급하고, legacy `planning-review` 호환용 섹션은 고정 위치가 아니라 heading 이름으로 찾아야 한다. 0.2.14 신규 `planning-format` 기본 저장 출력은 첫 H2가 `## 저장 파일`, `planning-format --no-save` 출력은 첫 H2가 `## 정책서`, 신규 `planning-review` 출력은 첫 H2가 `## 결론`이다. parser는 `## 저장 파일`, `## 체크해야 할 항목`, `## 출처/누락 요약`, `## 검토 결과`, `## 검토 근거 요약`, `## 상세 추적`을 정책서·기능설계서 본문 종료 boundary 또는 review report boundary로 인식해야 한다. 0.2.14부터 `planning-format`은 저장 기본값이며 `--no-save`만 화면 only 동작이다. legacy `--save`는 같은 저장 동작으로 허용한다. `planning-publish-confluence`는 명시적 저장 폴더 입력이 있을 때만 저장 파일을 읽고, URL·임의 `.md` 추론·여러 폴더 자동 선택은 거부한다. 최신 PRD가 release target인 경우 해당 PRD의 롤아웃 계획 완료 전까지 runtime 현재 계약으로 보지 않는다.

## PRD 파일

- [`prd-0.1.0.md`](./prd-0.1.0.md) — 0.1.0 base.
- [`prd-0.1.1.md`](./prd-0.1.1.md) — URL/재귀/이미지.
- [`prd-0.1.2.md`](./prd-0.1.2.md) — connector fallback.
- [`prd-0.2.0.md`](./prd-0.2.0.md) — 스킬 분할 (breaking).
- [`prd-0.2.1.md`](./prd-0.2.1.md) — 입력 제외 § 10종 + F5 cross-ref.
- [`prd-0.2.2.md`](./prd-0.2.2.md) — R1 link follow + 입력 제외 § R3 보조 신호.
- [`prd-0.2.3.md`](./prd-0.2.3.md) — 표 셀 list 분해 판단 + 보조 표 sub-§.
- [`prd-0.2.4.md`](./prd-0.2.4.md) — sub-§ 정밀화·SKILL 분해·deep link·11 카테고리.
- [`prd-0.2.5.md`](./prd-0.2.5.md) — 결정성 강화 7 항목 (fetch 의무·BFS·결정 트리·모호성 [TBD]·max-depth=3·6패스 체크리스트·라벨 매핑 트리).
- [`prd-0.2.6.md`](./prd-0.2.6.md) — planning-review 다중 URL 입력 + input fetch parity + 입력/SSOT fetch 분리.
- [`prd-0.2.7.md`](./prd-0.2.7.md) — ssot-audit 신규 스킬 + 구조/내용 품질 감사 + 개선 backlog 화면 출력 + planning-review 단일 파일 companion read.
- [`prd-0.2.8.md`](./prd-0.2.8.md) — 보조 표 헤더 backlink 제거 + 구조 변환 추적 정보 입력 제외 항목 이동 + legacy header 읽기 호환.
- [`prd-0.2.9.md`](./prd-0.2.9.md) — planning-format + planning-review 출력 개선: 진행 로그 제거, readable 결정 문서/report 우선 출력, 자체 검증 피드백 우선, 새 옵션 없이 추적 정보 하단 분리, `--save` 경로 `planning/` 고정, SSOT 폴더명 기반 corpus 제한.
- [`prd-0.2.10.md`](./prd-0.2.10.md) — planning-format + planning-review 상단 결정 보드: planning-format은 조건부, planning-review는 항상 출력. 첫 화면 요약, 지금 결정해야 할 항목, 바로 수정할 문서 작업, 릴리즈 차단 항목, 결정 질문, 선택지, 완료 조건, 검증 방법, 담당/결정 필요자 우선 표시. `## 결정 보드`는 산출 본문이 아닌 report metadata이며, legacy parser 호환을 위해 `planning-review`의 `## 최우선 수정 항목`과 `## 작업 백로그`는 유지한다.
- [`prd-0.2.11.md`](./prd-0.2.11.md) — 사용자-facing 섹션 기호 제거: 최종 화면, 생성 문서, 상세 추적에서 `§`를 출력하지 않고 clean display를 사용한다. 기존 `§` 입력은 `planning-review`와 downstream parser에서 계속 읽기 호환으로 유지한다.
- [`prd-0.2.12.md`](./prd-0.2.12.md) — `planning-format`은 `## 생성 결과 요약`으로 문서 결과·검증 상태·확인 필요·출처 영향을 본문 전에 보여주고, `planning-review`는 `## 결정 보드`를 실행 기준으로 단일화해 호환용 섹션의 중복 상세를 줄인다.
- [`prd-0.2.13.md`](./prd-0.2.13.md) — `planning-publish-confluence`는 현재 context memory의 정책서·기능 설계서 두 본문을 Product Team Space SSOT 하위 기능 container와 child page로 발행한다. 아직 확정 SSOT가 아니므로 Confluence title과 metadata에 `v0.7` label을 붙이며, AskUserQuestion으로 직접 parent URL 입력과 쓰기 전 최종 확인을 지원한다.
- [`prd-0.2.14.md`](./prd-0.2.14.md) — `planning-format`은 기본적으로 로컬 저장 후 화면에는 `저장 파일`과 `체크해야 할 항목`을 먼저 보여주고, `planning-review`는 결론과 검토 결과를 먼저 보여준다. `planning-publish-confluence`는 기존 context-body 발행과 명시적 저장 폴더 발행을 모두 지원하되, 저장 폴더에서는 canonical 정책서·기능설계서 두 파일만 읽는다. 신규 기본 저장 출력에서는 `planning-format`의 첫 H2가 `## 저장 파일`, `planning-format --no-save`에서는 첫 H2가 `## 정책서`, `planning-review`의 첫 H2가 `## 결론`이다. 하단 `체크해야 할 항목`에 `결정 필요`, `문서 보강 필요`, `출처/누락 참고` 또는 review 후속 행동을 모은다. legacy `결정 보드`는 읽기 호환으로만 유지한다.

## 검증 fixture

- [`fixtures/prd-0.2.10-fixtures.yml`](./fixtures/prd-0.2.10-fixtures.yml) — 0.2.10 결정 보드, parser boundary, legacy summary, release metadata, workflow diagram 기대값. 현재 저장소에는 fixture runner가 없으므로 PRD 0.2.10 14장의 golden expectation을 기계가 읽을 수 있는 데이터로 보관한다.
- [`fixtures/prd-0.2.12-fixtures.yml`](./fixtures/prd-0.2.12-fixtures.yml) — PRD 0.2.12 생성 결과 요약, 결정 보드 단일 실행 기준, parser boundary, legacy 호환 최소 표시, SSOT 부족 상태, 문서 hygiene 기대값.
- [`fixtures/prd-0.2.13-fixtures.yml`](./fixtures/prd-0.2.13-fixtures.yml) — PRD 0.2.13 `planning-publish-confluence` context memory gate, 금지 입력, 기본 parent preflight, `v0.7` title/label, 최종 확인, Confluence write/readback 기대값.
