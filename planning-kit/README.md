# planning-kit (0.2.9)

`planning-kit`은 기획 초안을 정책서·기능설계서로 정리하고, 그 산출물을 외부 기준과 비교하며, 선언된 SSOT 문서 묶음의 구조·내용 품질을 감사하는 플러그인입니다.

0.2.9의 핵심 변경은 출력 품질과 corpus 경계입니다. 기본 결과는 실행 로그가 아니라 사람이 바로 복사·검토할 산출물로 시작합니다. `planning-format --save`는 `planning/` 아래에 저장하고, `planning/**`과 `.planning-kit/**`은 SSOT 근거에서 항상 제외합니다. SSOT corpus는 폴더명에 독립 `SSOT` token이 있는 하위 폴더의 Markdown만 사용합니다.

Claude Code · Codex 양쪽에서 같은 `skills/`를 공유합니다.

---

## 빠른 시작

### Claude Code

```text
/planning-kit:planning-format 주문 취소 정책 정리해줘. 사용자가 결제 후 24시간 내 1회 취소 가능.
/planning-kit:planning-review
/planning-kit:ssot-audit
```

### Codex

```text
$planning-format 주문 취소 정책 정리해줘. 사용자가 결제 후 24시간 내 1회 취소 가능.
$planning-review
$ssot-audit
```

## 스킬

| 스킬 | 목적 |
|---|---|
| `planning-format` | 텍스트·파일·디렉터리·URL·이미지를 정책서와 기능설계서로 변환하고 F1~F6 자체 검증 피드백을 출력 |
| `planning-review` | planning-format 산출물을 SSOT 충돌, acceptance criteria 검증가능성, 의존 영향 3축으로 review |
| `ssot-audit` | 선언된 SSOT token 폴더 Markdown의 구조·내용 품질과 개선 백로그 감사 |

## planning-format

입력 예:

```text
/planning-kit:planning-format "주문 취소 정책 ..."
/planning-kit:planning-format ./docs/draft/주문취소.md
/planning-kit:planning-format ./docs/draft/입고기능/
/planning-kit:planning-format https://wiki.example/spec/order-cancel
/planning-kit:planning-format https://a.com/p1 https://b.com/p2
/planning-kit:planning-format ./diagrams/order-flow.png
/planning-kit:planning-format ./docs/draft/주문취소.md --save
```

기본 출력 순서:

```markdown
# [기능명]

- 입력: ...
- 산출물: 정책서, 기능설계서
- 검증: 피드백 N건, 사용자 확인 필요 M건
- 저장: 없음 (--save 미사용) / planning/[안전기능명]--YYYY-MM-DD-HHMMSS/

---

## 정책서
...

---

## 기능설계서
...

---

## 검증 피드백
...

## 출처 요약
...

## 입력 제외 요약
...

## 상세 추적
...
```

0.2.9 규칙:

- 최종 응답은 반드시 `# [기능명]`으로 시작하며 앞에 fetch 진행 로그를 쓰지 않습니다.
- 정책서·기능설계서는 기본 화면에서 코드 펜스로 감싸지 않고 일반 Markdown으로 렌더링합니다.
- 5열 이상 표나 긴 셀 표는 화면에서 카드/필드 목록으로 분해할 수 있습니다. 저장 파일은 canonical Markdown 구조를 우선 보존합니다.
- self-review에서 F2/F3/F4/F6 의미 변경 항목이 발견되어도 사용자 승인 전 본문에 조용히 반영하지 않고 `## 검증 피드백`에 먼저 올립니다.
- `--no-self-review` 사용 시 `- 검증: 생략 (--no-self-review)`를 표시하고 `## 검증 피드백`은 생략합니다.
- `--save`는 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 아래에 정책서 1개와 기능설계서 1개만 저장합니다.

`--save` 경로 예:

```text
planning/Zone-관리--2026-05-11-143000/
  Zone-관리_정책서.md
  Zone-관리_기능설계서.md
```

## planning-review

입력 예:

```text
/planning-kit:planning-review
/planning-kit:planning-review ./planning/Zone-관리--2026-05-11-143000/
/planning-kit:planning-review ./planning/Zone-관리--2026-05-11-143000/Zone-관리_정책서.md
/planning-kit:planning-review ./.planning-kit/legacy/정책서.md
/planning-kit:planning-review ./docs/주문-정책.md ./docs/주문-기능.md
/planning-kit:planning-review "## 정책서 ... ## 기능설계서 ..."
/planning-kit:planning-review https://wiki.example/policy/order-cancel https://docs.example/feature/order-cancel
/planning-kit:planning-review --axes ac
```

기본 출력 순서:

```markdown
# planning-review: [기능명]

- 판정: 통과 / 조건부 통과 / 수정 필요 / 검토 필요 / 비교 불가
- 검증 신뢰도: 충분 / 제한적 / 낮음 — 이유
- 입력: ...
- 점검 축: ssot, ac, deps
- 발견: P0 N건, P1 N건, P2 N건

---

## 결론
...

## 최우선 수정 항목
...

## 작업 백로그
...

## 발견 요약
...

## 검증 범위와 한계
...

## 출처 요약
...

## 상세 추적
...
```

0.2.9 규칙:

- 전체 report를 코드 펜스로 감싸지 않습니다.
- `판정`, `검증 신뢰도`, `결론`, `최우선 수정 항목`, `작업 백로그`가 축별 원시 발견보다 먼저 나옵니다.
- P0/P1 발견이 없으면 `## 최우선 수정 항목`은 빈 표가 아니라 `없음`을 표시합니다.
- 작업 단위가 없으면 `## 작업 백로그`도 `없음`을 표시합니다.
- SSOT 기준 문서 묶음이 0건이거나 모두 placeholder이면 R1 `0건`을 단순 `충돌 없음`으로 쓰지 않고 `비교 대상 본문 없음`과 낮은 신뢰도를 표시합니다.
- 직전 turn의 unsaved planning-format 화면 출력으로 review하면 검토 대상이 readable projection임을 `검증 범위와 한계`에 표시합니다.
- 0.2.8 이하 코드펜스 출력과 `.planning-kit/**` 저장 산출물은 review 입력으로 계속 읽을 수 있습니다.

판정 우선순위:

1. `수정 필요`: P0 또는 P1 발견이 1건 이상
2. `비교 불가`: 핵심 축을 증거 부족으로 판단할 수 없음
3. `검토 필요`: P2 권고나 외부 결정 항목만 있음
4. `조건부 통과`: 발견은 없지만 검증 신뢰도 제한적
5. `통과`: 발견 없고 검증 신뢰도 충분

## SSOT Corpus

`planning-review`와 `ssot-audit`는 같은 SSOT 경계 규칙을 사용합니다.

허용 예:

```text
Product Docs SSOT/**/*.md
[SSOT] 정책서/**/*.md
Confluence [SSOT] Export/**/*.md
Product_SSOT/**/*.md
```

제외 예:

```text
planning/**/*.md
.planning-kit/**/*.md
docs/**/*.md
README.md
planning-kit/docs/prd/**/*.md
planning-kit/skills/ssot-audit/**/*.md
docs/ssot-audit/**/*.md
ProductSSOT/**/*.md
```

규칙:

- `planning/**`과 `.planning-kit/**`은 항상 SSOT corpus에서 제외합니다.
- 폴더명 segment를 공백, 괄호, 대괄호, 중괄호, underscore로 나눴을 때 `SSOT` 독립 token이 있어야 합니다.
- 단순 substring은 허용하지 않습니다. `ProductSSOT`와 `ssot-audit`는 SSOT 폴더가 아닙니다.
- `--ssot-include`는 SSOT token 경계를 우회하지 못하고, 후보 안에서만 범위를 좁힙니다.
- SSOT token 폴더가 없으면 프로젝트 전체 Markdown으로 fallback하지 않습니다.

## ssot-audit

입력 예:

```text
/planning-kit:ssot-audit
/planning-kit:ssot-audit --ssot-include "Product Docs SSOT/**/*.md"
/planning-kit:ssot-audit --exclude "Product Docs SSOT/archive/**" --axes structure
/planning-kit:ssot-audit --no-follow-links --no-image
```

기본 출력 순서:

```markdown
# ssot-audit

- 감사 범위: SSOT token 폴더 Markdown N개
- 제외: planning/**, .planning-kit/**, 내부 plugin/skill 문서, SSOT token 밖 Markdown M개
- 분석 축: structure, content
- 외부 링크: 활성 / --no-follow-links
- 이미지: 활성 / --no-image
- placeholder: N개

---

## 결론
...

## SSOT 인벤토리
...

## 제외 요약
...

## 발견 및 권고
...

## 개선 백로그
...

## 상세 추적
...
```

SSOT token 폴더가 없으면 `감사 불가 — 선언된 SSOT token 폴더 없음`을 출력하고, 프로젝트 전체 Markdown으로 fallback하지 않습니다.

## 옵션 요약

### planning-format

| 옵션 | 동작 |
|---|---|
| `--save` | `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/`에 정책서·기능설계서 2개 파일 저장 |
| `--no-self-review` | F1~F6 self-review 생략. `## 검증 피드백` 섹션 생략 |
| `--no-fetch` | URL fetch와 connector fallback 봉쇄 |
| `--no-image` | 이미지 multimodal 처리 봉쇄 |

### planning-review

| 옵션 | 동작 |
|---|---|
| `--ssot-include <glob>` | SSOT token 후보 안에서 corpus를 좁힘 |
| `--axes <list>` | `ssot,ac,deps` 중 점검 축 선택 |
| `--no-input-fetch` | review 대상 입력 URL fetch 봉쇄 |
| `--no-input-image` | review 대상 입력 이미지 multimodal 봉쇄 |
| `--no-ssot-fetch` | SSOT corpus 외부 link follow 봉쇄 |
| `--no-ssot-image` | SSOT corpus 이미지 multimodal 봉쇄 |

### ssot-audit

| 옵션 | 동작 |
|---|---|
| `--ssot-include <glob>` | SSOT token 후보 안에서 corpus를 좁힘 |
| `--exclude <glob>` | 기본 제외에 추가해 corpus 후보 제외 |
| `--axes <list>` | `structure,content` 중 감사 축 선택 |
| `--no-follow-links` | SSOT Markdown 외부 link follow 봉쇄 |
| `--no-image` | 이미지 multimodal 처리 봉쇄 |

## 마이그레이션

0.2.8 이하에서 0.2.9로 넘어갈 때 확인할 내용:

- `planning-format --save` 신규 경로는 `.planning-kit/<기능명>/`이 아니라 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/`입니다.
- 0.2.8 이하 `.planning-kit/**` 산출물은 자동 이동하지 않지만, `planning-review` 입력으로는 계속 허용합니다.
- 신규 `planning/**`과 legacy `.planning-kit/**`은 모두 SSOT corpus 근거가 될 수 없습니다.
- SSOT 기준 문서를 쓰려면 폴더명에 독립 `SSOT` token이 있는 하위 폴더로 옮기거나 복제해야 합니다.
- `ssot-audit`는 기본적으로 선언된 SSOT token 폴더 내부 품질을 감사합니다. 프로젝트 전체 Markdown에서 SSOT 후보를 발굴하는 동작은 0.2.9 기본 동작이 아닙니다.
- 기본 화면 출력에서 정책서·기능설계서가 코드 펜스 없이 렌더링되므로, parser는 `## 정책서`/`## 기능설계서` wrapper heading과 `--save` 파일을 우선 사용해야 합니다.

## 구성

```text
planning-kit/
├── .claude-plugin/plugin.json
├── .codex-plugin/plugin.json
├── README.md
├── docs/
│   └── prd/
│       ├── README.md
│       └── prd-0.2.9.md
└── skills/
    ├── planning-format/
    │   ├── SKILL.md
    │   ├── templates/
    │   └── references/
    │       ├── conversion-rules.md
    │       ├── exclusion-rules.md
    │       ├── output-contract.md
    │       ├── self-review-rules.md
    │       └── connector-routing.md
    ├── planning-review/
    │   ├── SKILL.md
    │   └── references/
    │       ├── ssot-rules.md
    │       ├── ac-rules.md
    │       └── deps-rules.md
    └── ssot-audit/
        ├── SKILL.md
        └── references/
            ├── structure-rules.md
            ├── content-rules.md
            └── output-contract.md
```

## 검증

```bash
claude plugin validate ./planning-kit
git diff --check
```

릴리스 검증에는 README migration 문구, PRD chain row, plugin version bump, marketplace version bump 확인을 포함합니다.

## 라이선스

MIT
