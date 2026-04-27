# COLO plugins

Claude Code와 Codex에서 사용할 플러그인을 한 저장소에서 관리하는 workspace입니다. 저장소 루트는 설치 가능한 단일 플러그인이 아니라 marketplace catalog이고, 실제 플러그인은 각 하위 디렉터리에서 자체 manifest, skills, docs, tests를 관리합니다. 현재 이 저장소는 Claude Code와 Codex용 manifest만 제공하며, Cowork용 plugin manifest나 marketplace catalog는 포함하지 않습니다.

## 빠른 시작

### Claude Code

GitHub repository marketplace를 추가한 뒤 필요한 플러그인을 설치합니다.

```bash
claude plugin marketplace add inkwonjung-colosseum/plugins
claude plugin install confluence-export-kit@inkwonjung-colosseum
claude plugin install planning-team-kit@inkwonjung-colosseum
claude plugin install diagram-design@inkwonjung-colosseum
```

로컬 checkout을 marketplace로 추가해서 개발 중인 버전을 확인할 수도 있습니다.

```bash
claude plugin marketplace add /absolute/path/to/colo-plugins
claude plugin marketplace update inkwonjung-colosseum
claude plugin list
```

현재 Claude Code CLI 기준으로 plugin 관리 명령은 `marketplace add`, `marketplace update`, `install`, `update`, `list`, `enable`, `disable`, `uninstall`, `validate`, `tag`입니다. 예전 문서에 있던 `claude plugin add ./<plugin-dir>` 형식은 사용하지 않습니다.

### Codex

Codex는 repo-local marketplace인 `.agents/plugins/marketplace.json`과 각 플러그인의 `.codex-plugin/plugin.json`을 기준으로 discovery합니다. 로컬 checkout을 marketplace로 추가한 뒤 Codex 앱에서 `/plugins`를 열어 필요한 플러그인을 설치/활성화합니다.

```bash
codex marketplace add /absolute/path/to/colo-plugins
```

스킬은 `$planning-intake`, `$planning-grill`, `$quality-review`, `$diagram-design` 같은 skill invocation으로 사용합니다.

### Cowork

현재 이 저장소에는 Cowork용 plugin 추가 방법이 없습니다. Cowork를 지원하려면 Cowork가 요구하는 manifest/catalog 형식을 먼저 확인한 뒤, Claude Code의 `.claude-plugin/` 및 Codex의 `.codex-plugin/`과 별도 지원 파일을 추가해야 합니다.

## 플러그인

| 플러그인 | 버전 | 목적 | 대표 스킬 | 문서 |
|---|---:|---|---|---|
| `confluence-export-kit` | `0.1.2` | Confluence export 및 local export-index workflow. auth/config 설정, page/space/org/page-with-descendants export, export 후 자동 색인, 로컬 Markdown 재색인을 다룹니다. | `set-config`, `show-config`, `export-page`, `export-page-with-descendant`, `export-space`, `export-org`, `index-export`, `help` | [README](./confluence-export-kit/README.md) |
| `planning-team-kit` | `0.1.1` | 기획 문서 품질 workflow. intake, optional stress-test, draft 생성, multi-agent 품질 검수까지 draft-only로 처리합니다. | `help`, `planning-intake`, `planning-grill`, `planning-drafts`, `quality-review` | [README](./planning-team-kit/README.md) |
| `diagram-design` | `1.0.0` | 기술/제품 다이어그램 제작 workflow. architecture, flowchart, sequence, ER, timeline 등 타입별 standalone HTML/SVG 다이어그램 생성을 안내합니다. | `diagram-design` | [README](./diagram-design/README.md) |

## 사용 문법

Claude Code는 플러그인 namespace를 붙인 slash command 형태를 사용합니다.

```text
/confluence-export-kit:set-config --api-key <api-key> --email <email>
/planning-team-kit:planning-intake
/planning-team-kit:planning-grill
/diagram-design:diagram-design
```

Codex는 설치된 플러그인의 skill invocation을 사용합니다.

```text
$set-config --api-key <api-key> --email <email>
$planning-intake
$planning-grill
$diagram-design
```

여러 플러그인이 같은 스킬 이름을 제공하는 경우에는 Codex의 플러그인 선택 UI에서 의도한 플러그인을 확인합니다.

## 저장소 구조

```text
colo-plugins/
├── .agents/
│   └── plugins/
│       └── marketplace.json        # Codex marketplace catalog
├── .claude-plugin/
│   └── marketplace.json            # Claude Code marketplace catalog
├── confluence-export-kit/
│   ├── .claude-plugin/plugin.json
│   ├── .codex-plugin/plugin.json
│   ├── skills/
│   ├── scripts/
│   ├── docs/
│   └── tests/
├── planning-team-kit/
│   ├── .claude-plugin/plugin.json
│   ├── .codex-plugin/plugin.json
│   ├── skills/
│   ├── schemas/
│   ├── snippets/
│   ├── docs/
│   └── tests/
├── diagram-design/
│   ├── .claude-plugin/plugin.json
│   ├── .codex-plugin/plugin.json
│   └── skills/
└── README.md
```

## Marketplace 파일

Claude Code catalog는 `.claude-plugin/marketplace.json`입니다. 각 entry는 plugin name, source directory, description, version, license, tags를 가집니다.

Codex catalog는 `.agents/plugins/marketplace.json`입니다. 각 entry는 `source.path`, `policy.installation`, `policy.authentication`, `category`를 가집니다.

새 플러그인을 추가할 때는 다음을 함께 맞춥니다.

1. Claude Code 지원: `<plugin>/.claude-plugin/plugin.json`
2. Codex 지원: `<plugin>/.codex-plugin/plugin.json`
3. Claude Code catalog: `.claude-plugin/marketplace.json`
4. Codex catalog: `.agents/plugins/marketplace.json`
5. 플러그인 README와 루트 README의 목록/설치 안내

## 검증

배포 전에는 manifest와 대표 플러그인을 검증합니다.

```bash
claude plugin validate ./.claude-plugin/marketplace.json
claude plugin validate ./confluence-export-kit
claude plugin validate ./planning-team-kit
claude plugin validate ./diagram-design
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
