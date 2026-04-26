# Plugins 작업공간

이 저장소는 Claude Code와 Codex 플러그인 배포가 가능한 작업공간입니다. 각 플러그인 디렉터리는 매니페스트, 스킬, 훅, 스크립트, 문서를 자체적으로 관리하고, 루트 `.claude-plugin/marketplace.json`과 `.agents/plugins/marketplace.json`이 플랫폼별 카탈로그 역할을 합니다.

## 빠른 시작

### Claude Code marketplace 추가

```bash
# GitHub 저장소로 추가
claude plugin marketplace add inkwonjung-colosseum/plugins

# 로컬 클론 경로로 추가
claude plugin marketplace add /path/to/plugins
```

### Claude Code 플러그인 설치

```bash
# 특정 플러그인 설치
claude plugin install confluence-export-kit@inkwonjung-colosseum
claude plugin install planning-team-kit@inkwonjung-colosseum
claude plugin install diagram-design@inkwonjung-colosseum

# 설치된 플러그인 목록 확인
claude plugin list
```

### Claude Code 대안: 로컬 플러그인 직접 추가

```bash
claude plugin add ./confluence-export-kit
claude plugin add ./planning-team-kit
claude plugin add ./diagram-design
```

### Codex marketplace 발견

Codex는 repo marketplace인 `.agents/plugins/marketplace.json`을 읽어 플러그인 목록을 표시할 수 있습니다. 각 Codex 플러그인은 자체 `.codex-plugin/plugin.json`을 가지고 있으며, marketplace entry는 `source.path`, `policy.installation`, `policy.authentication`, `category`를 명시합니다.

현재 Codex marketplace에 등록된 로컬 플러그인:

| 플러그인 | Codex 매니페스트 | source.path |
|---|---|---|
| `confluence-export-kit` | `confluence-export-kit/.codex-plugin/plugin.json` | `./confluence-export-kit` |
| `skeleton-plugin` | `skeleton-plugin/.codex-plugin/plugin.json` | `./skeleton-plugin` |
| `planning-team-kit` | `planning-team-kit/.codex-plugin/plugin.json` | `./planning-team-kit` |
| `diagram-design` | `diagram-design/.codex-plugin/plugin.json` | `./diagram-design` |

Codex에서 marketplace를 다시 읽은 뒤 플러그인을 설치/활성화하고, 각 플러그인의 스킬을 `$planning-intake`, `$quality-review`, `$diagram-design` 같은 Codex skill invocation으로 사용할 수 있습니다. 여러 플러그인이 같은 스킬 이름을 제공하는 경우, Codex의 플러그인 선택 UI에서 의도한 플러그인을 확인합니다.

## 플러그인 디렉터리

| 플러그인 | 목적 | 문서 |
|---|---|---|
| `confluence-export-kit` | Confluence export 전용 플러그인: auth 설정, page/space/org/page-with-descendants export, `confluence-markdown-exporter` bootstrap | [README](./confluence-export-kit/README.md) |
| `skeleton-plugin` | Codex와 Claude Code를 모두 지원하는 플러그인 제작 시작 템플릿 | [README](./skeleton-plugin/README.md) |
| `planning-team-kit` | 기획 문서 품질 플러그인: 정의/정렬, 문서 생성, multi-agent 품질 검수 | [README](./planning-team-kit/README.md) |
| `diagram-design` | 기술/제품 다이어그램 제작 플러그인: architecture, flowchart, sequence, ER, timeline 등 14종을 standalone HTML/SVG로 생성 | [README](./diagram-design/README.md) |

`planning-team-kit/snippets/`에는 재사용 가능한 의사결정 표와 source/assumption/confidence 블록이 포함됩니다.

## 저장소 구조

```text
plugins/
├── .agents/
│   └── plugins/
│       └── marketplace.json  # Codex marketplace 카탈로그
├── .claude-plugin/
│   └── marketplace.json     # marketplace 카탈로그
├── confluence-export-kit/
│   ├── .claude-plugin/
│   │   └── plugin.json      # 플러그인 매니페스트
│   ├── skills/              # 스킬 (폴더별 SKILL.md)
│   ├── scripts/             # 보조 스크립트
│   └── docs/                # 플러그인 문서
├── skeleton-plugin/
│   ├── .claude-plugin/
│   │   └── plugin.json      # 플러그인 매니페스트
│   ├── .codex-plugin/       # Codex 매니페스트 (선택)
│   ├── commands/
│   ├── skills/
│   ├── hooks/
│   ├── scripts/
│   └── assets/
├── planning-team-kit/
│   ├── .claude-plugin/
│   │   └── plugin.json      # 플러그인 매니페스트
│   ├── .codex-plugin/
│   │   └── plugin.json      # Codex 플러그인 매니페스트
│   ├── skills/              # planning workflow skills
│   │   └── planning-drafts/
│   │       └── templates/   # 기획 문서 템플릿
│   ├── schemas/             # 문서 구조 스키마
│   ├── snippets/            # 재사용 가능한 표/메타데이터 블록
│   ├── docs/                # 품질 기준과 예시
│   └── tests/               # 구조/회귀 테스트
├── diagram-design/
│   ├── .claude-plugin/
│   │   └── plugin.json      # Claude Code 플러그인 매니페스트
│   ├── .codex-plugin/
│   │   └── plugin.json      # Codex 플러그인 매니페스트
│   ├── skills/
│   │   └── diagram-design/  # 다이어그램 생성 스킬, 레퍼런스, HTML 템플릿
│   └── docs/screenshots/    # README 및 갤러리용 예시 이미지
└── README.md
```

## marketplace 구조

루트 `.claude-plugin/marketplace.json`은 Claude Code용 카탈로그입니다. 각 항목은 플러그인 이름과 소스 디렉터리, 메타데이터를 매핑합니다.

```json
{
  "name": "inkwonjung-colosseum",
  "owner": {
    "name": "inkwonjung-colosseum",
    "url": "https://github.com/inkwonjung-colosseum"
  },
  "metadata": {
    "description": "..."
  },
  "plugins": [
    {
      "name": "confluence-export-kit",
      "source": "./confluence-export-kit",
      "description": "...",
      "version": "0.2.1",
      "license": "MIT",
      "tags": ["confluence"]
    },
    {
      "name": "planning-team-kit",
      "source": "./planning-team-kit",
      "description": "...",
      "version": "0.1.0",
      "license": "MIT",
      "tags": ["planning", "documentation"]
    },
    {
      "name": "diagram-design",
      "source": "./diagram-design",
      "description": "...",
      "version": "1.0.0",
      "license": "MIT",
      "tags": ["diagrams", "svg", "architecture"]
    }
  ]
}
```

루트 `.agents/plugins/marketplace.json`은 Codex용 카탈로그입니다. Codex entry는 플러그인 디렉터리의 `.codex-plugin/plugin.json`을 로드할 수 있도록 `source.path`를 지정하고, 설치 정책과 카테고리를 함께 명시합니다.

```json
{
  "name": "inkwonjung-colosseum",
  "interface": {
    "displayName": "inkwonjung-colosseum plugins"
  },
  "plugins": [
    {
      "name": "planning-team-kit",
      "source": {
        "source": "local",
        "path": "./planning-team-kit"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

### 새 플러그인을 marketplace에 추가하기

1. Claude Code용이면 `.claude-plugin/plugin.json`이 포함된 플러그인 디렉터리를 만듭니다.
2. Codex용이면 `.codex-plugin/plugin.json`이 포함된 플러그인 디렉터리를 만듭니다.
3. Claude Code 카탈로그에는 `.claude-plugin/marketplace.json` 항목을 추가합니다.
4. Codex 카탈로그에는 `.agents/plugins/marketplace.json` 항목을 추가하고 `policy.installation`, `policy.authentication`, `category`를 명시합니다.
5. Claude Code는 `claude plugin marketplace update inkwonjung-colosseum`으로 갱신하고, Codex는 marketplace를 다시 읽어 설치/활성화 상태를 확인합니다.

## 이 저장소에서 작업하는 방법

1. 작업할 플러그인 디렉터리로 이동합니다.
2. 매니페스트, 훅, 스킬, 스크립트를 수정하기 전에 해당 플러그인의 README를 먼저 읽습니다.
3. 플러그인별 상태와 에셋은 각 플러그인 디렉터리 안에 유지합니다.
4. 변경 후 배포 전에 Claude Code는 `claude plugin add ./<plugin-dir>`로, Codex는 `.agents/plugins/marketplace.json`과 `<plugin-dir>/.codex-plugin/plugin.json`의 discovery metadata로 테스트합니다.

## 메모

- 저장소 루트는 설치 가능한 플러그인이 아니라 marketplace 카탈로그입니다.
- 루트 `.claude-plugin/marketplace.json`은 GitHub 저장소 또는 정적 URL로 배포 가능합니다.
- 루트 `.agents/plugins/marketplace.json`은 Codex가 읽는 repo marketplace 카탈로그입니다.
- `.claude-plugin/plugin.json`이 없는 디렉터리는 marketplace에서 인식되지 않습니다.
- `.codex-plugin/plugin.json`이 없는 디렉터리는 Codex 플러그인으로 인식되지 않습니다.
