# planning-kit

기획 초안을 **정책서 + 기능설계서 두 본문**으로 변환하고, 같은 응답에서 **자동 리뷰**까지 한 번에 출력하는 단일 스킬 플러그인.

산출물은 **로컬 파일로 저장하지 않고 화면 output(응답 markdown)으로만 반환**한다. 사용자는 응답을 보고 직접 복사해 원하는 위치(Notion·Confluence·markdown 파일 등)에 붙여넣는다.

Claude Code · Codex 양쪽에서 동작한다.

---

## 빠른 시작

### Claude Code

```
/planning-kit:formalize 주문 취소 정책 정리해줘. 사용자가 결제 후 24시간 내 1회 취소 가능.
```

### Codex

```
$formalize 주문 취소 정책 정리해줘. 사용자가 결제 후 24시간 내 1회 취소 가능.
```

### 파일/디렉터리 입력

```
/planning-kit:formalize ./docs/draft/주문취소.md
/planning-kit:formalize ./docs/draft/입고기능/
```

디렉터리 입력은 안의 모든 UTF-8 텍스트 파일을 읽고 통합한 뒤 두 본문으로 분리한다.

---

## 결과 형태

한 응답에 다음을 모두 출력한다:

1. **정책서 본문** (10 섹션 markdown, 코드 펜스로 감싼 형태)
2. **기능설계서 본문** (8 섹션 markdown, 코드 펜스로 감싼 형태)
3. **입력 제외 항목** (변환 본문에 반영하지 않은 입력 조각이 있을 때만)
4. **리뷰 결과** (`통과` 또는 `발견 N건`)

자체 품질·SSOT 충돌 둘 다 0건이면 `## 리뷰 결과: 통과`. 어느 한쪽이라도 ≥1건이면 카테고리별 발견 list가 함께 표시된다.

---

## 옵션

| 옵션 | 동작 |
|---|---|
| `--ssot-include <glob>` | 리뷰 SSOT corpus를 좁힌다. default = 프로젝트 폴더 안 모든 `*.md` (`.git/`, `node_modules/` 자동 제외) |
| `--no-review` | 리뷰 단계 건너뛴다. 정책서·기능설계서 본문만 출력 |

예:

```
/planning-kit:formalize ./draft/취소정책.md --ssot-include "docs/policy/**/*.md"
/planning-kit:formalize ./draft/입고.md --no-review
```

---

## 자동 리뷰 2축

1. **본문 자체 품질 (Self-Review)** — 두 변환 본문 자체 점검
   - 섹션 충실도 ([TBD] 비율·빈 row·빈 섹션)
   - 라벨 cross-bleed (정책서 ↔ 기능설계서 내용 어긋남)
   - 두 문서 간 용어 일관성 (역할명·상태명·권한명·도메인 stem 통일)
   - 정책-기능 매핑 (정책서 규칙이 기능설계서 동작에 반영)
   - 누락 핵심 정보 (입력에는 있었지만 본문에 빠진 항목)
2. **SSOT 충돌** — 두 본문 확정 문장이 프로젝트 폴더 안 다른 `*.md`와 어긋나는지 점검. 문서 종류·역할(정책/PRD/회의록/README) 구분 없이 일괄 corpus.

상세 기준은 `skills/formalize/references/review-rules.md` 참조.

---

## 구성

```
planning-kit/
├── .claude-plugin/plugin.json
├── .codex-plugin/plugin.json
├── README.md
├── docs/
│   └── prd/
│       └── prd-0.1.0.md
└── skills/
    └── formalize/
        ├── SKILL.md
        ├── templates/
        │   ├── 기능설계서.md
        │   └── 정책서.md
        └── references/
            └── review-rules.md
```

---

## product-team-kit과의 차이

`planning-kit`은 기존 `product-team-kit`(`set-config` + `plan-format` + `plan-review` 3 스킬)의 흐름을 **`formalize` 단일 스킬**로 합친다. 차이 요점:

| 항목 | product-team-kit | planning-kit |
|---|---|---|
| Skill 수 | 3 | 1 |
| 변환·리뷰 호출 | 2번 (`plan-format` → `plan-review`) | 1번 (`formalize`) |
| Agent worker | 1 (terminology) | 0 |
| Reference 수 | 5 | 1 |
| Template 수 | 2 (정책서 + 기능설계서) | 2 (정책서 + 기능설계서) |
| 산출물 | 정책서 + 기능설계서 2 file (`<outputRoot>/.../*.md`) | 정책서 + 기능설계서 본문 화면 output (저장 안 함) |
| 파일 IO | mkdir + Write 호출 | 없음 |
| Config 파일 | `.product-team-kit/config.json` 필수 | 없음 (default + CLI 인자) |
| `CLAUDE.md`/`AGENTS.md` upsert | 항상 | 안 함 |
| Marker | 4종 + `해당 없음` fill | 1종 (`[TBD]`) |
| Gate First | 4 조건 + 2 문서 최소 검사 | 없음 (literal 빈 입력만 sanity check) |
| 빈 위치 보존 | row·셀 삭제 금지 | 삭제 허용 |
| 본문 검사 | 빈 골격/구조 일치 retry/중복/cross-bleed | 없음 |
| 저장 절차 | staging→write→verify→rename + collision `--01..99` | 없음 |
| 안전기능명 정규화 | 폴더명 안전화 (NFC, 특수문자 제거 등) | 없음 (출력 헤더용 raw 기능명만) |
| 출력 템플릿 | 4종 (설정없음/저장보류/저장완료/저장실패) | 2종 (변환+리뷰/보류) |
| 리뷰 축 | 2축 (SSOT 충돌 + 용어 일관성) | 2축 (자체 품질 + SSOT 충돌) |
| 리뷰 worker | B축 worker 분리 | main 단일 패스 |
| SSOT corpus 처리 | 인덱스 스캔 + version + archive 분류 | grep 매칭 후 직접 read |
| 검토 결과 | 3종 (통과/조건부/수정 필요) | 2종 (통과/발견 N건) |
| 출력 구조 | 2층 (상단 합의 + 하단 agent 원본) | 1층 |
| GFM cell escape | 단일 진실 소스 알고리즘 | 없음 (numbered list) |
| 진행 표시 | step header 시퀀스 통제 | 자유 |
| 추정 size | ~1850 line | ~500 line |

두 플러그인은 **별도 동작하며 병행 사용 가능**하다. `planning-kit`은 파일을 만들지 않으므로 `<outputRoot>` 충돌 같은 이슈가 없다.

---

## 라이선스

MIT
