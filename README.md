# COLO plugins

Claude Code, Claude Desktop/Cowork, Codex에서 사용할 플러그인을 한 저장소에서 관리하는 workspace입니다. 저장소 루트는 설치 가능한 단일 플러그인이 아니라 marketplace catalog이고, 실제 플러그인은 각 하위 디렉터리에서 자체 manifest, skills, docs를 관리합니다.

## 빠른 시작

### Claude Code

GitHub repository marketplace를 추가한 뒤 필요한 플러그인을 설치합니다. 플러그인 링크는 [https://github.com/inkwonjung-colosseum/plugins](https://github.com/inkwonjung-colosseum/plugins)입니다.

```bash
claude plugin marketplace add https://github.com/inkwonjung-colosseum/plugins
claude plugin install product-team-kit@inkwonjung-colosseum
claude plugin install planning-kit@inkwonjung-colosseum
claude plugin install diagram-design@inkwonjung-colosseum
claude plugin install logistics-expert-kit@inkwonjung-colosseum
claude plugin install ai-utility-kit@inkwonjung-colosseum
```

현재 Claude Code CLI 기준으로 plugin 관리 명령은 `marketplace add`, `marketplace update`, `install`, `update`, `list`, `enable`, `disable`, `uninstall`, `validate`, `tag`입니다. 예전 문서에 있던 `claude plugin add ./<plugin-dir>` 형식은 사용하지 않습니다.

### Codex

Codex App을 사용하는 경우 Microsoft Store에서 Windows 앱을 설치한 뒤, 앱에서 `/plugins` 또는 plugin/skill 설정 화면을 열어 필요한 플러그인을 설치/활성화합니다. 플러그인 링크는 [https://github.com/inkwonjung-colosseum/plugins](https://github.com/inkwonjung-colosseum/plugins)입니다.

스킬은 `$plan-format`, `$plan-review`, `$set-config`, `$planning-format`, `$planning-review`, `$ssot-audit`, `$diagram-design`, `$logistics-scope`, `$ai-grill` 같은 skill invocation으로 사용합니다.

### Cowork

Cowork는 Claude Desktop 앱에서 plugin을 설치합니다. 현재는 `Cowork` > `Customize`에서 public GitHub repo 링크를 입력해 플러그인을 추가하는 방식으로 운영합니다. 이 경로에서는 사용자 PC에 Git 설치가 필요하지 않습니다. 조직 catalog 방식은 추후 도입 예정입니다.

- Claude Desktop 다운로드: [https://claude.com/download](https://claude.com/download)
- Cowork plugin 사용 문서: [https://support.claude.com/en/articles/13837440-use-plugins-in-claude-cowork](https://support.claude.com/en/articles/13837440-use-plugins-in-claude-cowork)

## 플러그인

| 플러그인 | 버전 | 목적 | 대표 스킬 | 문서 |
|---|---:|---|---|---|
| `product-team-kit` | `0.7.5` | 기획 입력을 기능설계서와 정책서 초안으로 단일 패스 작성·자체 검증하며, `.product-team-kit/config.json`과 `CLAUDE.md`/`AGENTS.md` 안내 블록 설정, 단계별 lazy read, Product Docs SSOT 근거 기반 2축 점검(SSOT 충돌·용어 일관성)을 지원합니다. | `set-config`, `plan-format`, `plan-review` | [README](./product-team-kit/README.md) |
| `planning-kit` | `0.2.7` | 기획 초안(텍스트·파일·디렉터리·URL·이미지)을 정책서·기능설계서 두 본문으로 변환하고 자체 품질을 점검하는 `planning-format`, 산출물을 외부 SSOT 충돌·acceptance criteria·의존 영향 3축으로 검증하는 `planning-review`, 프로젝트 Markdown SSOT corpus 자체를 구조·내용 2축으로 감사하는 `ssot-audit` 세 스킬 구조. 0.2.7부터 `planning-review` 단일 파일 입력은 같은 폴더 sibling 파일을 non-recursive로 함께 읽고, `ssot-audit`는 v0.8 미만 문서 제외·외부 링크 cap 없음 follow·개선 backlog 화면 output을 제공합니다. | `planning-format`, `planning-review`, `ssot-audit` | [README](./planning-kit/README.md) |
| `diagram-design` | `1.0.3` | 기술/제품 다이어그램 제작 workflow. architecture, flowchart, sequence, ER, timeline 등 타입별 standalone HTML/SVG 다이어그램 생성을 안내합니다. | `diagram-design` | [README](./diagram-design/README.md) |
| `logistics-expert-kit` | `0.1.1` | 범용 물류 도메인 조언 도구. 물류 이슈 범위 정리, 운영 문제 진단, KPI 설계, 정책/프로세스 리스크 검토를 대화형으로 지원합니다. | `logistics-scope`, `logistics-diagnose`, `logistics-metrics`, `logistics-risk` | [README](./logistics-expert-kit/README.md) |
| `ai-utility-kit` | `0.1.1` | 한국어 우선 범용 AI 활용 도구. 계획 검토, 맥락 지도화, 회의록 정리, 용어 정리를 대화형으로 지원합니다. | `ai-grill`, `context-map`, `meeting-brief`, `term-clarifier` | [README](./ai-utility-kit/README.md) |

## 프로젝트 다이어그램

프로젝트 workflow 다이어그램은 `docs/diagrams/` 아래의 standalone HTML/SVG 파일로 관리합니다. `product-team-kit` 다이어그램 2개는 `docs/diagrams/product-team-kit-workflow.source.json`에서 생성하므로 HTML을 직접 수정하지 않고 `python3 docs/diagrams/render_product_team_kit_workflow.py --write`로 갱신합니다.

| 다이어그램 | 설명 |
|---|---|
| [`planning-confluence-document-workflow.html`](./docs/diagrams/planning-confluence-document-workflow.html) | Confluence export를 Product Docs Markdown 후보로 가져오는 보조 문서 운영 흐름 |
| [`product-team-kit-workflow.html`](./docs/diagrams/product-team-kit-workflow.html) | `set-config`, agent 안내 블록, `plan-format`, `plan-review`, lazy read, 저장 보류, 재검토 안내, 발행 준비, 팀 handoff를 요약한 generated overview |
| [`product-team-kit-workflow-analysis.html`](./docs/diagrams/product-team-kit-workflow-analysis.html) | 같은 source에서 생성한 상세 분석 view. set-config의 config·agent 안내 정렬, lazy read, 입력 보완, SSOT 근거 경계, 보수적 종료 조건, 발행 준비 경계를 함께 표시 |
| [`diagram-design-workflow.html`](./docs/diagrams/diagram-design-workflow.html) | `diagram-design`의 타입 선택, style guide gate, taste gate 기반 HTML/SVG 생성 흐름 |

## 사용 문법

Claude Code는 플러그인 namespace를 붙인 slash command 형태를 사용합니다.

```text
/product-team-kit:plan-format
/product-team-kit:plan-review
/product-team-kit:set-config
/planning-kit:planning-format
/planning-kit:planning-review
/planning-kit:ssot-audit
/diagram-design:diagram-design
/logistics-expert-kit:logistics-scope
/logistics-expert-kit:logistics-diagnose
/logistics-expert-kit:logistics-metrics
/logistics-expert-kit:logistics-risk
/ai-utility-kit:ai-grill
/ai-utility-kit:context-map
/ai-utility-kit:meeting-brief
/ai-utility-kit:term-clarifier
```

Codex는 설치된 플러그인의 skill invocation을 사용합니다.

```text
$plan-format
$plan-review
$set-config
$planning-format
$planning-review
$ssot-audit
$diagram-design
$logistics-scope
$logistics-diagnose
$logistics-metrics
$logistics-risk
$ai-grill
$context-map
$meeting-brief
$term-clarifier
```

여러 플러그인이 같은 스킬 이름을 제공하는 경우에는 Codex의 플러그인 선택 UI에서 의도한 플러그인을 확인합니다.

Claude Desktop Cowork는 설치된 plugin의 Skills를 UI에서 선택합니다. 입력창에서 `/`를 입력하거나 `+` 버튼을 눌러 `planning-format`, `planning-review`, `ssot-audit`, `diagram-design` 같은 스킬을 선택합니다.

## 저장소 구조

```text
colo-plugins/
├── .agents/
│   └── plugins/
│       └── marketplace.json        # Codex marketplace catalog
├── .claude-plugin/
│   └── marketplace.json            # Claude Code marketplace catalog
├── product-team-kit/
│   ├── .claude-plugin/plugin.json
│   ├── .codex-plugin/plugin.json
│   ├── agents/
│   ├── references/
│   ├── skills/
│   └── docs/
├── planning-kit/
│   ├── .claude-plugin/plugin.json
│   ├── .codex-plugin/plugin.json
│   ├── skills/
│   │   ├── planning-format/
│   │   ├── planning-review/
│   │   └── ssot-audit/
│   └── docs/
├── diagram-design/
│   ├── .claude-plugin/plugin.json
│   ├── .codex-plugin/plugin.json
│   ├── skills/
│   └── docs/
├── logistics-expert-kit/
│   ├── .claude-plugin/plugin.json
│   ├── .codex-plugin/plugin.json
│   ├── skills/
│   ├── references/
│   ├── templates/
│   └── docs/
├── ai-utility-kit/
│   ├── .claude-plugin/plugin.json
│   ├── .codex-plugin/plugin.json
│   ├── skills/
│   └── docs/
└── README.md
```

## Marketplace 파일

Claude Code catalog는 `.claude-plugin/marketplace.json`입니다. 각 entry는 plugin name, source directory, description, version, license, tags를 가집니다.

Codex catalog는 `.agents/plugins/marketplace.json`입니다. 각 entry는 `source.path`, `policy.installation`, `policy.authentication`, `category`를 가지며, version marker가 필요한 entry는 `version`을 함께 둡니다.

Cowork 조직 catalog 배포는 추후 도입 예정입니다.

새 플러그인을 추가할 때는 다음을 함께 맞춥니다.

1. Claude Code 지원: `<plugin>/.claude-plugin/plugin.json`
2. Codex 지원: `<plugin>/.codex-plugin/plugin.json`
3. Claude Code catalog: `.claude-plugin/marketplace.json`
4. Codex catalog: `.agents/plugins/marketplace.json`
5. Cowork public GitHub repo 링크 기반 설치 안내
6. 플러그인 README와 루트 README의 목록/설치 안내

## 검증

배포 전에는 manifest와 대표 플러그인을 검증합니다.

```bash
claude plugin validate ./.claude-plugin/marketplace.json
claude plugin validate ./product-team-kit
claude plugin validate ./planning-kit
claude plugin validate ./diagram-design
claude plugin validate ./logistics-expert-kit
claude plugin validate ./ai-utility-kit
```

generated 다이어그램 source를 바꾼 경우에는 HTML 산출물이 최신인지 확인합니다.

```bash
python3 docs/diagrams/render_product_team_kit_workflow.py --check
```

문서만 수정한 경우에도 Markdown diff에 공백 문제가 없는지 확인합니다.

```bash
git diff --check
```

## 작업 원칙

- 루트는 marketplace catalog이고, 기능 구현은 각 플러그인 디렉터리 안에서 관리합니다.
- 플러그인을 수정하기 전에는 해당 플러그인의 README와 `skills/*/SKILL.md`를 먼저 확인합니다.
- Claude Code와 Codex가 같은 `skills/`를 공유하므로, 스킬 설명과 manifest의 이름/버전/경로를 함께 갱신합니다.
- 설치법은 README 기억이 아니라 현재 `claude plugin --help`와 `claude plugin marketplace --help` 기준으로 확인합니다.
