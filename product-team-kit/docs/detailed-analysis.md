# product-team-kit 상세 분석

작성일: 2026-05-07

## 1. 정체성

`product-team-kit`은 기획 입력을 로컬 초안 2종, 즉 기능설계서와 정책서로 생성하고, 팀 문서 반영 전에 Product Docs SSOT 근거로 검토하는 도구다. Claude Code와 Codex 양쪽을 지원하며, 현재 로컬 매니페스트 기준 버전은 `0.6.7`, 라이선스는 MIT다.

```text
set-config
  -> .product-team-kit/config.json
  -> CLAUDE.md / AGENTS.md product-team-kit 안내 블록

plan-format
  -> <outputRoot>/[안전기능명]--YYYY-MM-DD-HHMMSS/{기능설계서,정책서}.md
       ↓
plan-review
  -> 통과 / 조건부 통과 / 수정 필요 / 올바른 검토 대상이 아님
```

핵심 정체성은 "로컬 설정과 agent 안내", "기획 입력을 문서 초안으로 정리하는 formatter", "발행 전 검토 gate"의 분리다. `set-config`는 사용처 프로젝트의 설정과 agent 안내 블록을 갱신하고, `plan-format`은 생성 가능 여부를 먼저 판단한 뒤 초안을 저장하며, `plan-review`는 Product Docs SSOT 충돌, 명확성, 용어 일관성, downstream 착수 가능성을 4축으로 검토한다. 두 실행 스킬은 lazy read 원칙을 공유해 종료 분기에서 쓰지 않는 templates, references, SSOT corpus를 선행 read하지 않는다.

## 2. 구조

```text
.claude-plugin/plugin.json    # Claude 매니페스트
.codex-plugin/plugin.json     # Codex 매니페스트
agents/                       # plan-review B/C/D 내부 worker 정의
docs/                         # workflow, PRD, 기능 정의, 약관/정책
references/config-contract.md # 세 skill 공유 로컬 설정 계약
skills/set-config/
  SKILL.md
  agents/openai.yaml
skills/plan-format/
  SKILL.md                    # 3-step 본문 (config strict-exit + Gate First + 변환·저장 + 입력 dispatch + 분류 + marker)
  agents/openai.yaml
  templates/{기능설계서,정책서}.md
  references/                 # storage-contract, output-contract
skills/plan-review/
  SKILL.md
  agents/openai.yaml
  references/                 # review-rules, output-format
```

현재 `plan-format` references는 2개 (`storage-contract.md`, `output-contract.md`)이며, `plan-review` references는 2개 (`review-rules.md`, `output-format.md`)다. plan-format 템플릿 2개, 공유 `config-contract.md`, `set-config`까지 더하면 주요 계약/템플릿 표면은 8개다. 입력 dispatch·분류·marker는 `plan-format/SKILL.md`에 모여 있고, review 판정·출력은 `review-rules.md`와 `output-format.md`에 분리되어 있다.

## 3. 핵심 설계 원칙

- **Local config first**: 사용처 프로젝트 루트의 `.product-team-kit/config.json`으로 `outputRoot`와 SSOT corpus 범위를 조정하고, `CLAUDE.md`/`AGENTS.md` 안내 블록으로 agent가 이 범위를 먼저 확인하게 한다.
- **Strict-exit**: `plan-format`은 config가 없거나 핵심 검증에 실패하면 파일 생성 없이 종료하고 `set-config`를 안내한다.
- **Lazy read**: config 실패, gate 보류, unsupported input, SSOT 0건 같은 종료/우회 분기에서 쓰지 않는 파일은 읽지 않는다.
- **Gate First**: 변환 가능 판정 전 파일 생성 금지. 부족하면 질문 루프 없이 보류 출력만 반환한다.
- **No interview loop**: `plan-format`은 단일 패스다. 부족 항목만 출력하고 보강 템플릿은 만들지 않는다.
- **역할 분리**: `plan-format`은 formatter, `plan-review`는 validator다. `plan-format`은 SSOT 검증을 하지 않고, `plan-review`는 초안을 직접 수정하지 않는다.
- **좁은 Product Docs SSOT**: `<outputRoot>/`을 제외한 프로젝트 내 Markdown과 그 문서가 상대경로로 참조한 로컬 resource만 근거로 본다.
- **보수적 취합**: 최종 결과는 `수정 필요 > 조건부 통과 > 통과` 순서로 결정한다. `착수 전 보강 필요` 역할이 하나라도 있으면 `수정 필요`다.

## 4. set-config 동작

`set-config`는 cwd의 git root 또는 cwd를 기준으로 `.product-team-kit/config.json`을 만든다. 인자는 받지 않고, 각 키를 대화형으로 확인한다. config 저장 성공 후 같은 root의 `CLAUDE.md`와 `AGENTS.md` product-team-kit 관리 블록을 선택 없이 항상 생성·갱신한다.

| 키 | 처리 |
|---|---|
| `version` | 항상 `1`로 저장 |
| `outputRoot` | 단일 폴더명만 허용. 절대경로, `..`, 경로 구분자, 빈 문자열, 제어문자 거부 |
| `ssot.include` | 줄바꿈/콤마 입력을 배열로 저장. 빈 배열이면 key 제거 후 기본 `Product Team Space/Product Department/Colonova Product/_AI_ 정책서 & 기능설계서/**/*.md` 사용 |
| `ssot.exclude` | 줄바꿈/콤마 입력을 배열로 저장. 빈 배열이면 key 제거 |

검증 거부값은 저장하지 않고 같은 키에서 다시 입력받는다. config 저장은 `.product-team-kit/config.json.tmp`를 쓴 뒤 rename하는 atomic write다. 기존 config의 다른 키는 보존한다. `CLAUDE.md`와 `AGENTS.md`는 기존 사용자 내용을 보존하고 product-team-kit start/end 관리 블록만 replace 또는 append한다. marker가 한쪽만 있으면 해당 파일은 변경하지 않고 `agent-guide-write` 실패로 보고한다.

## 5. plan-format 동작

### Step 1 strict-exit

`<project-root>/.product-team-kit/config.json`을 읽어 다음 중 하나라도 해당하면 즉시 종료한다. 이 분기에서는 입력 본문, templates, storage contract를 읽지 않는다.

- 파일 없음
- JSON 파싱 실패
- `version` 미일치 또는 누락
- `outputRoot` 검증 거부

종료 출력은 종료 분기가 확정된 뒤 `output-contract.md`의 "설정 없음" 템플릿을 읽어 사용하고 `set-config`를 안내한다. 비치명 검증 거부 (unknown key, ssot 배열 element 비문자열)는 default fallback + `[설정 경고]`로 처리하고 step 2로 진행한다.

### Step 2 입력 dispatch와 Gate First

| 종류 | 처리 |
|---|---|
| 빈 입력 또는 최소 입력 | 정보 부족 보류 |
| 직접 텍스트 | 본문 그대로 사용 |
| 기존 파일 | UTF-8 텍스트로 읽기 |
| 기존 디렉터리 | 텍스트 파일 통합. 입력 크기 상한 없음 (검증 정확도 우선) |
| 없는 path-like 입력 | 직접 텍스트로 폴백 |
| 주제와 경로가 섞인 입력 | 주제와 경로를 모두 사용 |

Gate First 4 조건:

- 기능 목적 또는 기능명
- 적용 대상 또는 업무 범위
- 핵심 사용자 행동과 기대 결과
- 주요 조건/정책/제약

부서 경계 (디자인·API·DB·QA·운영·개발 작업 분해 heavy 입력이고 제품·업무 판단 정보 부족)도 보류 사유다. 기능설계서와 정책서 중 한쪽이 빈 골격에 가까우면 보류한다. 저장 보류에서는 `output-contract.md`만 읽고, templates와 `storage-contract.md`는 읽지 않는다.

### Step 3 변환·저장

dispatch → 단일 패스 작성 → 자체 검증 3단계로 작성한다. dispatch는 기능명, 안전기능명, 역할명, 용어, 입력 단편 라벨을 고정한다. 본문 작성 직전에만 기능설계서/정책서 templates를 읽고, main이 `feature`와 `both`의 사용자 결과·가능 행위는 기능설계서에, `policy`와 `both`의 판단 기준은 정책서에 배치한다. 작성 후 main은 헤더 일치, 빈 골격, 중복 항목, 라벨 cross-bleed, marker 합산을 자체 검증한다. 저장 절차에 들어갈 때만 `storage-contract.md`를 읽는다.

저장 계약:

- 저장 root는 config `outputRoot`이며 default는 `planning`이다.
- 안전기능명은 NFC 정규화, 공백의 하이픈 변환, 금지 문자 제거, 50자 또는 120 bytes char-boundary truncation을 적용한다.
- 저장 폴더는 `<outputRoot>/[안전기능명]--YYYY-MM-DD-HHMMSS/`다.
- timestamp는 Asia/Seoul 기준이다.
- 충돌 시 `--01` ~ `--99` suffix를 순차 시도한다.
- 두 파일은 같은 staging folder에 먼저 작성한다. 두 파일 존재 검증이 끝난 뒤 staging folder를 target folder로 rename하며, 실패 시 남은 staging/target 경로를 저장 실패 출력에 노출한다.

## 6. plan-review 동작

`plan-review`는 초안 폴더 또는 기능설계서/정책서 파일을 검토한다. 먼저 config를 확인하고, 치명 오류면 `output-format.md`만 읽어 종료한다. 폴더 입력이면 기능설계서와 정책서를 함께 읽고, 단일 파일 입력이면 같은 폴더에서 짝문서를 찾는다. 지원하지 않는 문서 타입이면 `review-rules.md`와 SSOT corpus를 읽지 않고 `올바른 검토 대상이 아님`으로 종료한다. 짝문서가 없으면 단일 검토를 진행하되 `검증 한계`에 남긴다.

Product Docs SSOT는 `<outputRoot>/`을 제외한 현재 프로젝트의 제품 정책, PRD/요구사항, 기능/화면 설계, 운영/QA 판단 Markdown과 그 Markdown이 상대경로로 참조한 로컬 resource다. `plan-review`는 검토 대상 본문만으로 핵심 섹션 `[미정]`, 빈 필수 섹션, `[충돌 후보]`가 과도하면 `수정 필요 (조기 판정)`으로 종료한다. 조기 판정이 아니면 검토 대상에서 키워드를 추출하고, 후보 파일 상위 20줄 인덱스로 archive/deprecated/낮은 버전/키워드 미매칭 문서를 제외한 뒤 핵심 후보만 전문으로 읽는다. 매칭이 0건이면 A축은 `검증 대상 없음`으로 처리하고, B/C/D축은 검토 대상 본문만으로 점검한다.

4축 점검:

| 축 | 확인 내용 |
|---|---|
| 조기 판정 | SSOT 탐색 전 핵심 판단 누락이 과도한지 |
| A. SSOT 충돌 | 초안 확정 문장과 current evidence 충돌 여부 |
| B. 명확성 | marker, 모호 조건, 상태·권한·예외 판단 가능성 |
| C. 용어 일관성 | 역할명, 상태명, 권한명, 화면명, 도메인 stem 통일성 |
| D. 4역할 넘김 가능성 | 디자인, 개발, QA, 운영이 대화 기억 없이 다음 업무를 시작할 수 있는지 |

점검 실행은 dispatch → main A축 점검 + 3 worker(B/C/D) 병렬 → merge 3단계다. dispatch가 검토 대상, 키워드, SSOT 후보를 고정하고 필요한 `review-rules.md` 섹션을 준비한다. A축 SSOT 충돌은 corpus를 보유한 main이 직접 점검하고, B/C/D worker는 검토 대상 본문과 자기 축 기준만 받아 발견 사항만 작성한다. main은 모든 발견 사항 dedup, 보수 합성, 결과 판정, 사람용 리포트 출력을 담당한다. 병렬 worker 호출이 불가능한 환경에서는 같은 결과 형식으로 단일 패스 fallback을 사용한다.

출력은 YAML manifest가 아니라 사람용 markdown 리포트 하나다. 상단에 판정, 한 줄 결론, 먼저 할 일, 역할별 착수 가능성, 기준 문서와의 충돌을 두고, 하단에 coverage, 읽은 근거, 읽지 않은 관련 후보, 제외 후보, 검증 한계, 상세 발견 항목을 둔다.

결과별 출력:

| 결과 | 추가 블록 |
|---|---|
| 통과 | 발행 준비 체크리스트 |
| 조건부 통과 | 발행 전 확인 항목 + 발행 준비 체크리스트 |
| 수정 필요 | 필수 수정 항목 + 재검토 안내 체크리스트 |
| 올바른 검토 대상이 아님 | 다음 행동 안내 |

## 7. 강점

- Strict-exit + Gate First + 단일 패스로 불완전 산출물과 의도 외 실행을 최소화한다.
- Lazy read 계약으로 config 실패, 저장 보류, SSOT 매칭 0건 같은 분기의 context 낭비와 예기치 않은 근거 확대를 줄인다.
- `set-config`로 프로젝트별 저장 위치와 SSOT corpus 범위를 조정하고, agent가 같은 SSOT 범위를 우선 조회하도록 `CLAUDE.md`/`AGENTS.md` 안내 블록을 남길 수 있다.
- 단일 SKILL.md에 입력 dispatch·분류·marker를 흡수해 cross-reference drift 위험을 낮췄다.
- staging folder rename + char-boundary safe-name truncation + `--99` collision bound로 한쪽 final 문서만 남는 실패 모드를 줄이고 저장 실패 모드를 명시한다.
- SSOT 범위가 좁고 명확해 "근거 없음" 거짓양성을 줄인다.
- 보수적 합성 규칙으로 false pass를 차단한다.
- 4 marker (`[미정]`/`[가정]`/`[확인 필요]`/`[충돌 후보]`) 정의가 plan-review 분류 규칙과 직결된다.
- 역할별 readiness를 design, development, QA, operations로 나눠 downstream 책임을 분담한다.

## 8. 약점과 리스크

1. Strict-exit으로 config 없는 신규 환경은 첫 실행에서 바로 실패한다. README와 set-config 안내가 가이드지만 초기 마찰은 남는다. 한 번 set-config를 실행하면 agent 안내 블록도 같이 생겨 이후 프로젝트 재진입 시 SSOT 경계 혼선은 줄어든다.
2. Markdown 전제가 강하다. 팀이 Notion 또는 Confluence를 쓰면 export snapshot만 SSOT 근거가 되므로 freshness risk가 자주 발생할 수 있다.
3. 단일 기능명 가정이 강하다. 디렉터리 입력에 여러 기능이 섞이면 첫 후보로 묶일 수 있고 다기능 분리 메커니즘이 없다.
4. Lazy read는 내부 references와 SSOT corpus를 늦게 읽게 하지만, Gate First를 위해 선택된 입력 자체는 끝까지 읽는다. 큰 PRD 모음을 넣으면 호출 환경의 메모리/시간 한계는 여전히 운영자가 책임진다.
5. Asia/Seoul timestamp가 고정되어 다른 timezone 팀에는 혼선이 있을 수 있다.
6. `plan-format`은 SSOT 검증을 하지 않기 때문에 SSOT와 충돌하는 항목이 `plan-review` 전까지 표면화되지 않고 재작업이 생길 수 있다.
7. 9섹션 템플릿은 작은 기능에는 과할 수 있다. 빈 섹션 제거 규칙이 완화 장치지만 진입장벽은 남는다.
8. `plan-review`가 직접 수정하지 않기 때문에 반복 수정과 재검토 루프를 사람이 수동 운영해야 한다.

## 9. 확장 포인트

- Multi-feature dispatcher: 디렉터리 입력을 기능 단위로 분리하고 N개 폴더를 생성한다.
- 외부 SSOT adapter: Notion, Confluence MCP 등 외부 source를 근거로 확장한다. 단 SSOT 근거 정의를 함께 확장해야 한다.
- `review -> repair -> re-review` 보조 흐름을 제공한다. 이 경우에도 Product Docs SSOT 자동 수정은 금지한다.
- Asia/Seoul 고정을 config 또는 host locale 기준으로 바꾼다.
- 문서 계약 회귀 테스트를 추가해 버전 drift, stale reference, 삭제된 출력 용어를 잡는다.

## 10. 한 줄 요약

`product-team-kit` 0.6.7은 `set-config` + `plan-format` + `plan-review`의 세 표면으로 정리됐다. set-config는 config와 agent 안내 블록을 함께 정렬하고, plan-format은 별도 작성 worker 없이 단일 패스 작성과 자체 검증을 수행하며, plan-review는 SSOT corpus를 main A축 점검에만 사용해 worker 입력 범위를 줄인다. 남은 핵심 리스크는 신규 config 마찰, Markdown SSOT 전제, 단일 기능명 가정이다.
