# COLO plugins

Claude Code, Claude Desktop/Cowork, Codex에서 사용할 플러그인을 한 저장소에서 관리하는 workspace입니다. 저장소 루트는 설치 가능한 단일 플러그인이 아니라 marketplace catalog이고, 실제 플러그인은 각 하위 디렉터리에서 자체 manifest, skills, docs를 관리합니다.

## 빠른 시작

### Claude Code

GitHub repository marketplace를 추가한 뒤 필요한 플러그인을 설치합니다. 플러그인 링크는 [https://github.com/inkwonjung-colosseum/plugins](https://github.com/inkwonjung-colosseum/plugins)입니다.

```bash
claude plugin marketplace add https://github.com/inkwonjung-colosseum/plugins
claude plugin install planning-kit@inkwonjung-colosseum
```

현재 Claude Code CLI 기준으로 plugin 관리 명령은 `marketplace add`, `marketplace update`, `install`, `update`, `list`, `enable`, `disable`, `uninstall`, `validate`, `tag`입니다. 예전 문서에 있던 `claude plugin add ./<plugin-dir>` 형식은 사용하지 않습니다.

### Codex

Codex App을 사용하는 경우 Microsoft Store에서 Windows 앱을 설치한 뒤, 앱에서 `/plugins` 또는 plugin/skill 설정 화면을 열어 필요한 플러그인을 설치/활성화합니다. 플러그인 링크는 [https://github.com/inkwonjung-colosseum/plugins](https://github.com/inkwonjung-colosseum/plugins)입니다.

스킬은 `$planning-format`, `$planning-review`, `$planning-publish-confluence`, `$ssot-audit` 같은 skill invocation으로 사용합니다.

### Cowork

Cowork는 Claude Desktop 앱에서 plugin을 설치합니다. 현재는 `Cowork` > `Customize`에서 public GitHub repo 링크를 입력해 플러그인을 추가하는 방식으로 운영합니다. 이 경로에서는 사용자 PC에 Git 설치가 필요하지 않습니다. 조직 catalog 방식은 추후 도입 예정입니다.

- Claude Desktop 다운로드: [https://claude.com/download](https://claude.com/download)
- Cowork plugin 사용 문서: [https://support.claude.com/en/articles/13837440-use-plugins-in-claude-cowork](https://support.claude.com/en/articles/13837440-use-plugins-in-claude-cowork)

## 플러그인

| 플러그인 | 버전 | 목적 | 대표 스킬 | 문서 |
|---|---:|---|---|---|
| `planning-kit` | `0.2.16` | 기획 초안을 정책서·기능설계서로 변환하고 기본 저장 파일과 체크해야 할 항목을 보여주는 `planning-format`, 결론·검토 결과를 먼저 보여주는 `planning-review`, 현재 context memory 또는 명시적 저장 폴더를 `v0.7` Confluence 후보 문서로 발행하는 `planning-publish-confluence`, 독립 `SSOT` 표시 폴더 Markdown만 감사하는 `ssot-audit` 네 스킬 구조. 전문을 화면에 펼치려면 `--no-save`를 사용합니다. | `planning-format`, `planning-review`, `planning-publish-confluence`, `ssot-audit` | [README](./planning-kit/README.md) |

## 사용 문법

Claude Code는 플러그인 namespace를 붙인 slash command 형태를 사용합니다.

```text
/planning-kit:planning-format
/planning-kit:planning-review
/planning-kit:planning-publish-confluence
/planning-kit:ssot-audit
```

Codex는 설치된 플러그인의 skill invocation을 사용합니다.

```text
$planning-format
$planning-review
$planning-publish-confluence
$ssot-audit
```

여러 플러그인이 같은 스킬 이름을 제공하는 경우에는 Codex의 플러그인 선택 UI에서 의도한 플러그인을 확인합니다.

Claude Desktop Cowork는 설치된 plugin의 Skills를 UI에서 선택합니다. 입력창에서 `/`를 입력하거나 `+` 버튼을 눌러 `planning-format`, `planning-review`, `planning-publish-confluence`, `ssot-audit` 같은 스킬을 선택합니다.

## 저장소 구조

```text
colo-plugins/
├── .agents/
│   └── plugins/
│       └── marketplace.json        # Codex marketplace catalog
├── .claude-plugin/
│   └── marketplace.json            # Claude Code marketplace catalog
├── planning-kit/
│   ├── .claude-plugin/plugin.json
│   ├── .codex-plugin/plugin.json
│   ├── skills/
│   │   ├── planning-format/
│   │   ├── planning-review/
│   │   ├── planning-publish-confluence/
│   │   └── ssot-audit/
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
claude plugin validate ./planning-kit
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
