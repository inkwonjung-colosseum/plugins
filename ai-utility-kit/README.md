# ai-utility-kit

`ai-utility-kit`은 Claude Code와 Codex에서 쓰는 한국어 우선 범용 AI 활용 플러그인입니다. 계획 검토, 맥락 지도화, 회의록 정리, 용어 정리를 대화형으로 지원합니다.

## 원칙

- **한국어 우선**: 기본 출력은 한국어입니다. 영어로 요청하면 영어로 답합니다.
- **범용 AI 활용**: 특정 회사, 제품, 도메인, 외부 서비스에 묶이지 않습니다.
- **대화형 결과**: v0.1은 로컬 파일 생성, Confluence/Jira/Slack 반영, 외부 API 호출을 포함하지 않습니다.
- **근거 구분**: 확인한 내용과 추정, 미정, 확인 필요 항목을 구분합니다.

## 스킬

| 스킬 | 목적 | 예시 |
|---|---|---|
| `ai-grill` | 계획, 아이디어, 설계를 한 질문씩 압박 검토 | `$ai-grill 이 기능 설계 허점 찾아줘` |
| `context-map` | 낯선 코드, 문서, 주제의 전체 구조와 읽는 순서 정리 | `$context-map 이 프로젝트 구조 먼저 파악해줘` |
| `meeting-brief` | 회의록, 통화 메모, 긴 채팅에서 회의 정보/요약/결정/논의/액션아이템 정리 | `$meeting-brief 이 회의록 정리해줘` |
| `term-clarifier` | 용어, 동의어, 애매한 표현, 개념 관계 정리 | `$term-clarifier 이 문서의 용어 정리해줘` |

## 사용 예

Claude Code:

```text
/ai-utility-kit:ai-grill 새 온보딩 정책 설계 검토해줘
/ai-utility-kit:context-map 이 코드 영역 전체 그림 알려줘
/ai-utility-kit:meeting-brief 아래 회의록에서 액션아이템 뽑아줘
/ai-utility-kit:term-clarifier "계정", "사용자", "멤버" 차이 정리해줘
```

Codex:

```text
$ai-grill 새 온보딩 정책 설계 검토해줘
$context-map 이 코드 영역 전체 그림 알려줘
$meeting-brief 아래 회의록에서 액션아이템 뽑아줘
$term-clarifier "계정", "사용자", "멤버" 차이 정리해줘
```

## 포함 범위

- 계획, 아이디어, 설계의 질문 기반 검토
- 코드, 문서, 프로젝트, 주제의 구조 파악
- 회의록, 통화 메모, 긴 채팅의 실행 가능한 회의록 정리
- 용어, 동의어, 모호한 표현, 개념 관계 정리

## 비범위

- 로컬 파일 생성 또는 수정
- Confluence, Jira, Slack, GitHub 등 외부 서비스 반영
- 법무, 보안, 컴플라이언스, 인사 판단의 최종 승인
- 특정 회사나 제품의 조직별 정책 확정
- 개발 전용 TDD, CI, 배포, Sentry, GitHub PR 자동화

## 구성

- `.claude-plugin/plugin.json` — Claude Code 플러그인 매니페스트
- `.codex-plugin/plugin.json` — Codex 플러그인 매니페스트
- `skills/` — 4개 대화형 AI 유틸리티 스킬
- `docs/` — privacy policy와 terms of service
- `tests/` — 구조 회귀 테스트

## 참고

이 플러그인은 [mattpocock/skills](https://github.com/mattpocock/skills)와 [ComposioHQ/awesome-codex-skills](https://github.com/ComposioHQ/awesome-codex-skills)의 여러 범용 skill 아이디어에서 영감을 받았습니다. 스킬 문구와 실행 규칙은 `ai-utility-kit` 목적에 맞게 새로 작성했습니다.

## 설치

### Claude Code

```bash
claude plugin marketplace add https://github.com/inkwonjung-colosseum/plugins
claude plugin install ai-utility-kit@inkwonjung-colosseum
```

### Codex

```bash
codex marketplace add https://github.com/inkwonjung-colosseum/plugins
```

marketplace 추가 후 Codex 앱의 `/plugins`에서 `ai-utility-kit`을 설치/활성화합니다.

## 검증

```bash
python3 -m unittest ai-utility-kit/tests/test_structure.py
claude plugin validate ./ai-utility-kit
```
