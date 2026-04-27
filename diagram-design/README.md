# diagram-design

`diagram-design`은 Claude Code와 Codex 양쪽에서 쓰는 기술/제품 다이어그램 제작 플러그인입니다. 아키텍처, 플로우차트, 시퀀스, ER/data model 같은 다이어그램을 하나의 독립 실행형 HTML 파일로 만들고, 내부에는 CSS와 inline SVG를 포함합니다.

## 목적

이 플러그인은 빠르게 도형을 많이 배치하는 도구가 아니라, 읽는 사람이 실제로 이해할 수 있는 절제된 다이어그램을 만들도록 돕는 디자인 가이드입니다. 타입별 레이아웃 규칙, 복잡도 예산, 색/타이포그래피 토큰, 출력 전 체크리스트를 함께 제공합니다.

## 지원 범위

- 기술/제품 다이어그램을 standalone HTML + inline SVG로 생성
- 프로젝트 브랜드에 맞춘 색상, 폰트, 토큰 기반 스타일 가이드 적용
- 첫 사용 시 기본 스타일을 그대로 쓸지, 웹사이트에서 브랜드 토큰을 추출할지 확인하는 style guide gate
- 타입별 reference 문서와 예시 HTML 템플릿 제공
- light, dark, full editorial 변형 템플릿 제공
- annotation callout과 선택형 sketchy variant 제공

## 비범위

- Mermaid, PlantUML, Graphviz 같은 DSL 렌더러 대체
- 대규모 복잡 시스템 전체를 한 장에 압축
- 자동 PNG/PDF export 파이프라인
- 외부 디자인 도구 또는 문서 시스템에 자동 게시
- 사용자의 최종 구조 판단 대행

## 지원 다이어그램

| 보여주려는 것 | 타입 |
|---|---|
| 시스템 컴포넌트와 연결 | Architecture |
| 조건과 분기 흐름 | Flowchart |
| 시간 순서 메시지 | Sequence |
| 상태와 전이 | State machine |
| 엔티티, 필드, 관계 | ER / data model |
| 시간축 이벤트 | Timeline |
| 역할/부서별 프로세스 handoff | Swimlane |
| 2축 포지셔닝 또는 우선순위 | Quadrant |
| 포함 관계와 범위 | Nested |
| 부모-자식 계층 | Tree |
| 추상화 레이어 | Layer stack |
| 집합 간 겹침 | Venn |
| 단계형 계층 또는 funnel | Pyramid / funnel |

`quadrant`에는 컨설팅 스타일 2x2 scenario matrix 예시도 포함되어 있습니다.

## Start Here

처음 쓰는 경우 `diagram-design` 스킬을 호출해 만들고 싶은 다이어그램의 목적, 독자, 포함할 요소를 알려주면 됩니다.

Claude Code:

```text
/diagram-design:diagram-design
```

Codex:

```text
$diagram-design
```

## 기본 워크플로우

1. 만들려는 설명이 다이어그램으로 더 잘 전달되는지 확인합니다.
2. 적합한 다이어그램 타입을 고릅니다.
3. 해당 타입의 `references/type-*.md` 규칙을 읽습니다.
4. 프로젝트의 `references/style-guide.md`가 기본 토큰인지 확인합니다.
5. 기본 토큰이면 브랜드 스타일 적용 여부를 사용자에게 먼저 묻습니다.
6. 가장 가까운 `assets/template*.html` 또는 `assets/example-*.html`을 바탕으로 standalone HTML을 만듭니다.
7. 출력 전 taste gate로 복잡도, 색상 강조, 화살표 라벨, legend 위치, 4px grid를 확인합니다.

## 디자인 원칙

- 핵심 노드와 연결만 남깁니다.
- 강조색은 최대 1-2개 요소에만 씁니다.
- 한 장의 다이어그램은 기본적으로 9개 노드 이하를 목표로 합니다.
- 관계가 레이아웃만으로 분명하면 화살표를 줄입니다.
- 사람에게 읽히는 이름은 sans, 포트/URL/명령 같은 기술 정보는 mono를 씁니다.
- legend는 다이어그램 안에 띄우지 않고 하단 strip으로 배치합니다.

## 출력 형식

생성 결과는 하나의 `.html` 파일입니다.

- CSS는 HTML 안에 포함
- SVG는 inline으로 포함
- 외부 이미지는 사용하지 않음
- JavaScript 없이 최신 브라우저에서 렌더링
- Google Fonts 링크만 외부 의존성으로 허용

## 포함된 구성

- `.claude-plugin/plugin.json` — Claude Code 플러그인 매니페스트
- `.codex-plugin/plugin.json` — Codex 플러그인 매니페스트
- `skills/diagram-design/SKILL.md` — 다이어그램 제작 스킬의 핵심 지침
- `skills/diagram-design/references/style-guide.md` — 색상, 폰트, 토큰 기준
- `skills/diagram-design/references/onboarding.md` — 웹사이트 기반 브랜드 스타일 추출 흐름
- `skills/diagram-design/references/type-*.md` — 다이어그램 타입별 규칙
- `skills/diagram-design/references/primitive-*.md` — annotation, sketchy 변형 규칙
- `skills/diagram-design/assets/template*.html` — light, dark, full editorial 템플릿
- `skills/diagram-design/assets/example-*.html` — 타입별 예시 HTML

## 설치

### Claude Code

```bash
claude plugin marketplace add inkwonjung-colosseum/plugins
claude plugin install diagram-design@inkwonjung-colosseum
```

로컬 개발 중에는 저장소 루트를 marketplace로 추가한 뒤 이 플러그인을 설치합니다.

```bash
claude plugin marketplace add /absolute/path/to/colo-plugins
claude plugin install diagram-design@inkwonjung-colosseum
```

### Codex

Codex에서는 이 플러그인 폴더를 로컬 marketplace 또는 개인 플러그인 경로에 배치한 뒤 `/plugins`에서 설치합니다. 이 플러그인은 `.codex-plugin/plugin.json`과 동일한 `skills/` 디렉터리를 사용합니다.

## 사용 예

```text
# Claude Code
/diagram-design:diagram-design
내 SaaS의 인증, API, DB, 외부 결제 연동을 보여주는 아키텍처 다이어그램을 만들어줘.
```

```text
# Codex
$diagram-design
이 주문 처리 흐름을 결제 성공/실패 분기가 보이는 flowchart로 만들어줘.
```

## 메모

- 기본 스타일 가이드가 그대로 남아 있으면, 첫 다이어그램 생성 전에 브랜드 스타일 적용 여부를 확인해야 합니다.
- 복잡도가 높으면 overview와 detail 다이어그램으로 나누는 쪽을 우선합니다.
- 생성된 HTML은 문서, 블로그, 슬라이드, 제품 설명 페이지에 붙여 넣기 쉬운 형태를 목표로 합니다.
