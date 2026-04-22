# Plugins 작업공간

[English](./README.md) | 한국어

이 저장소는 Claude Code 플러그인 marketplace 배포가 가능한 작업공간입니다. 각 플러그인 디렉터리는 매니페스트, 스킬, 훅, 스크립트, 문서를 자체적으로 관리하고, 저장소 루트의 `marketplace.json`이 배포 카탈로그 역할을 합니다.

## 빠른 시작

### marketplace 추가

```bash
# 로컬 클론 경로로 추가
claude plugin marketplace add /path/to/plugins

# 또는 호스팅된 URL로 추가
claude plugin marketplace add https://raw.githubusercontent.com/inkwonjung-colosseum/plugins/main/.claude-plugin/marketplace.json
```

### 플러그인 설치

```bash
# 사용 가능한 플러그인 목록 확인
claude plugin marketplace list

# 특정 플러그인 설치
claude plugin install confluence-export-kit
```

### 대안: 로컬 플러그인 직접 추가

```bash
claude plugin add ./confluence-export-kit
```

## 플러그인 디렉터리

| 플러그인 | 목적 | 문서 |
|---|---|---|
| `confluence-export-kit` | Confluence export 전용 플러그인: auth 설정, page-tree/keyword/label export, `confluence-markdown-exporter` bootstrap | [EN](./confluence-export-kit/README.en.md) / [KR](./confluence-export-kit/README.md) |
| `skeleton-plugin` | Codex와 Claude Code를 모두 지원하는 플러그인 제작 시작 템플릿 | [EN](./skeleton-plugin/README.en.md) / [KR](./skeleton-plugin/README.md) |

## 저장소 구조

```text
plugins/
├── .claude-plugin/
│   └── marketplace.json     # marketplace 카탈로그
├── confluence-export-kit/
│   ├── .claude-plugin/
│   │   └── plugin.json      # 플러그인 매니페스트
│   ├── commands/            # 슬래시 커맨드 (.md)
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
├── README.md
└── README.ko.md
```

## marketplace 구조

루트 `.claude-plugin/marketplace.json`이 사용 가능한 모든 플러그인을 카탈로그로 관리합니다. 각 항목은 플러그인 이름과 소스 디렉터리, 메타데이터를 매핑합니다.

```json
{
  "owner": "inkwonjung-colosseum",
  "plugins": [
    {
      "name": "confluence-export-kit",
      "source": "./confluence-export-kit",
      "description": "...",
      "version": "0.1.0"
    }
  ]
}
```

### 새 플러그인을 marketplace에 추가하기

1. `.claude-plugin/plugin.json`이 포함된 플러그인 디렉터리를 만듭니다.
2. `.claude-plugin/marketplace.json`에 항목을 추가합니다.
3. `claude plugin marketplace update inkwonjung-colosseum`으로 갱신합니다.

## 이 저장소에서 작업하는 방법

1. 작업할 플러그인 디렉터리로 이동합니다.
2. 매니페스트, 훅, 스킬, 스크립트를 수정하기 전에 해당 플러그인의 README를 먼저 읽습니다.
3. 플러그인별 상태와 에셋은 각 플러그인 디렉터리 안에 유지합니다.
4. 변경 후 배포 전에 `claude plugin add ./<plugin-dir>`로 테스트합니다.

## 메모

- 저장소 루트는 설치 가능한 플러그인이 아니라 marketplace 카탈로그입니다.
- `marketplace.json`은 정적 URL 호스팅으로 원격 배포가 가능합니다.
- `.claude-plugin/plugin.json`이 없는 디렉터리는 marketplace에서 인식되지 않습니다.

## 언어 메모

- 루트: `README.md` (영어), `README.ko.md` (한국어).
- `confluence-export-kit`: `README.en.md` (영어), `README.md` (한국어).
- `skeleton-plugin`: `README.en.md` (영어), `README.md` (한국어).
