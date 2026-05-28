# colonova-confluence-kit

ColoNova Engineering Confluence `8.8 ColoNova` 트리 전용 문서 운영 플러그인입니다.

기본 대상은 고정되어 있습니다.

- URL: `https://colosseum.atlassian.net/wiki/spaces/COLO/pages/933068815/8.8+ColoNova`
- root page ID: `933068815`

## Skills

| Skill | 목적 | 쓰기 권한 |
| --- | --- | --- |
| `colonova-folder-audit` | 하위 트리의 Archive 후보, 위치 불일치, 추출/전환 후보, 실행 큐를 read-only로 감사 | 없음 |
| `colonova-doc-router-publisher` | 단건 초안 또는 소수 문서 패키지의 위치 추천, 템플릿 변환, 승인 후 Confluence 생성/업데이트와 readback 검증 | 승인 후 가능 |

## Usage

- Claude Code: `/colonova-confluence-kit:colonova-folder-audit`
- Claude Code: `/colonova-confluence-kit:colonova-doc-router-publisher`
- Codex: `$colonova-folder-audit`
- Codex: `$colonova-doc-router-publisher`

## 운영 경계

- `colonova-folder-audit`는 페이지를 이동, 수정, 아카이빙하지 않습니다. 실행 큐와 근거만 만듭니다.
- `colonova-doc-router-publisher`는 게시 전 추천 parent, 제목, 문서 유형, 템플릿, 변환 본문을 먼저 보여줍니다.
- Confluence 생성 또는 업데이트는 사용자의 명시 승인 후에만 수행합니다.
- 생성 또는 수정 후에는 page ID readback으로 제목, 부모, 주요 섹션, 빈 본문 여부를 확인합니다.
- live Confluence root와 분류 가이드가 기준의 SSOT입니다.
