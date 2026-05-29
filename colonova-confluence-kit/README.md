# colonova-confluence-kit

ColoNova Engineering Confluence `8.8 ColoNova` 트리의 지속적 유지보수·최신화 관리 플러그인입니다. 1회성 게시/감사가 아니라, 살아있는 기준 문서를 최신 상태로 유지하고 트리를 반복 점검·갱신하는 운영 도구입니다.

기본 대상은 고정되어 있습니다.

- URL: `https://colosseum.atlassian.net/wiki/spaces/COLO/pages/933068815/8.8+ColoNova`
- root page ID: `933068815`

## Skills

| Skill | 목적 | 쓰기 권한 |
| --- | --- | --- |
| `colonova-folder-audit` | 하위 트리의 Archive 후보, 위치 불일치, 추출/전환 후보, 실행 큐를 read-only로 감사. stale 기준 문서 freshness/최신화 후보(`05`/`08`/`12` living standard, `07` 모니터링 SLO·threshold, Approved `02` Design Review), Pending supersession·Discussion closure incomplete·Under Review 정체(workflow stale)·신규 Subfolder drift 탐지, SSOT 대비 미생성 폴더 gap 식별. 리포트는 `colonova-audit-YYYY-MM-DD.md`로 저장돼 다음 실행의 prior report로 자동 연결(delta·overdue 점검) | 없음 |
| `colonova-doc-router-publisher` | 단건 초안 또는 소수 문서 패키지의 위치 추천, 유형별 템플릿 변환, 승인 후 Confluence 생성/업데이트(version pre-fetch·429 재시도)와 readback 검증. 기존 living standard 최신화·갱신(변경 이력 기록), 최신화 후보 큐 일괄 갱신(Batch Refresh), discussion→decision 종결, supersession 처리(inbound 링크 점검·limit cap 경고). 로컬 템플릿 11종: 시스템 분석, 시스템 디자인, Design Review, 회의록, 논의사항, 기술문서/ADR, 결정사항, 운영 가이드, 기술 참조, 솔루션, 스케쥴링 | 승인 후 가능 |

## Usage

- Claude Code: `/colonova-confluence-kit:colonova-folder-audit`
- Claude Code: `/colonova-confluence-kit:colonova-doc-router-publisher`
- Codex: `$colonova-folder-audit`
- Codex: `$colonova-doc-router-publisher`

또는 슬래시 커맨드 없이 자연어로 입력하면 적절한 skill이 자동 선택됩니다.

- "8.8 ColoNova 유지보수 해줘" → `colonova-folder-audit` 발동 후 최신화 후보 큐 생성 → 승인 시 `colonova-doc-router-publisher` 순서로 진행 (감사→갱신 전체 루프를 한 마디로 시작)
- "8.8 ColoNova 트리 스프린트 감사해줘" → `colonova-folder-audit`
- "05 기술문서 오래된 문서 최신화 후보 보여줘" → `colonova-folder-audit` (freshness)
- "이 초안을 ColoNova 적절한 폴더에 올려줘" → `colonova-doc-router-publisher`
- "감사 결과 page ID 12345 갱신해줘" → `colonova-doc-router-publisher` (update intent + page ID)

## 언제 어느 skill을 쓰나

| 상황 | Skill | 진입 예시 |
| --- | --- | --- |
| 새 문서를 올바른 폴더에 게시 | `colonova-doc-router-publisher` | "이 초안을 ColoNova 트리 적절한 폴더에 올려줘" |
| 기존 기준 문서를 갱신·최신화 (page ID 보유) | `colonova-doc-router-publisher` (update intent + page ID) | "page ID 12345 기준 문서를 최신 스펙으로 갱신해줘" |
| 트리 전체 또는 특정 폴더를 정기 점검 | `colonova-folder-audit` | "8.8 ColoNova 트리를 감사해줘" |
| 스프린트 마감 후 ColoNova 트리 전체 정리 | `colonova-folder-audit` | "스프린트 끝났는데 ColoNova 문서 상태 확인·정리해줘" |
| 오래된 stale 기준 문서를 찾아 갱신 후보 큐로 | `colonova-folder-audit` (freshness mode) | "05 기술문서 중 오래된 문서 최신화 후보를 보여줘" |
| folder-audit 최신화 후보 큐에서 page ID를 받아 실제 갱신 실행 | `colonova-doc-router-publisher` (update intent + page ID) | "Refresh required로 나온 page ID 12345를 갱신해줘" |
| 최신화 후보 큐 여러 page ID를 한 번에 일괄 갱신 | `colonova-doc-router-publisher` (Batch Refresh Flow) | "최신화 후보 큐에 나온 page ID 전부 순서대로 갱신해줘" |
| 구 기준 문서 SUPERSEDED 처리 완료 여부 점검 | `colonova-folder-audit` | "이번 스프린트에 superseded 처리 완료 안 된 구 페이지 있는지 확인해줘" |
| 결정사항 전환 후 논의사항 RESOLVED 처리 완료 여부 점검 | `colonova-folder-audit` | "결정사항으로 전환됐는데 RESOLVED 안 된 논의사항 있는지 확인해줘" |
| 장기 정체 Under Review Design Review 점검 | `colonova-folder-audit` | "02 시스템 디자인 Under Review 90일 넘은 DR 있는지 점검해줘" |
| 구 페이지 SUPERSEDED 처리 / 논의사항 RESOLVED 처리 실행 | `colonova-doc-router-publisher` | "page ID 12345 구 기준 문서 SUPERSEDED 처리해줘", "이 논의사항 RESOLVED로 종결해줘" |
| 결정사항 페이지 신규 작성 | `colonova-doc-router-publisher` (`templates/decision.md`) | "이 결정 내용을 08 결정사항에 정리해줘" |
| 운영 가이드 작성 또는 갱신 | `colonova-doc-router-publisher` (`templates/operating-guide.md`) | "이 절차를 12 운영 가이드 runbook으로 올려줘" |
| 솔루션 도입 검토·PoC 결과 작성/갱신 | `colonova-doc-router-publisher` (`templates/solution.md`) | "이 SaaS 도입 검토 결과를 10 솔루션에 정리해줘" |
| 로드맵·마일스톤 일정 작성/갱신 | `colonova-doc-router-publisher` (`templates/scheduling.md`) | "이 릴리즈 로드맵을 09 스케쥴링에 올려줘" |

슬래시 커맨드 없이 자연어로 입력해도 각 skill이 자동 선택됩니다. 예: "05 기술문서 stale 문서 최신화 후보 보여줘", "8.8 ColoNova 트리 스프린트 감사 실행해줘", "이 초안을 적절한 폴더에 올려줘".

### End-to-end 예시

복합 의도("유지보수 해줘", "최신화 해줘")는 먼저 `colonova-folder-audit`이 발동되어 감사 후 최신화 큐를 만들고, 사용자가 승인하면 `colonova-doc-router-publisher`로 page ID가 넘어갑니다.

1. 스프린트 감사 → 최신화 큐 → 갱신 실행 (3단계)
   - (1) "스프린트 끝났어. 8.8 ColoNova 트리 감사하고 오래된 기준 문서도 찾아줘" → `colonova-folder-audit` 발동(full-tree + freshness). 출력: `## 결론`(다음 감사 권장일 포함), `## 감사 메타`, `## 최신화 후보` 큐(page ID 포함), Archive/Tree Gap 큐.
   - (2) "최신화 후보에 나온 page ID 998877을 최신 스펙으로 갱신해줘" → `colonova-doc-router-publisher` 발동(update intent + page ID). 현재 페이지 읽기 → 변경 본문 + 변경 이력 row 제시 → 승인 게이트 → update → readback.
   - (3) supersession이 필요하면 같은 skill이 Supersession Flow로 구 페이지 SUPERSEDED 처리와 inbound 링크 점검까지 이어갑니다.
2. audit 없이 직접 publisher 진입 (1단계)
   - "이 기준 문서 최신화해줘. page ID 12345" → page ID + 갱신 의도가 명확하므로 `colonova-doc-router-publisher`가 곧장 update 경로로 진입합니다(감사 불필요).

## 정기 운영 패턴

지속 유지보수 도구로 다음 주기를 권장합니다.

- 스프린트 종료(약 2주)마다: `colonova-folder-audit` 전체 트리 감사 (Archive, 위치, Tree Gap; **Pending supersession·Discussion closure incomplete·Under Review DR workflow stale·신규 Subfolder 탐지 포함**). 이 주기 감사에서 supersession/closure 완료 여부와 정체된 Under Review DR도 함께 점검됩니다.
- 매월: `colonova-folder-audit` freshness 모드로 living standard(`05`, `08`, `12`), `07. 모니터링` SLO/threshold 페이지, Approved `02` Design Review stale 점검 → 후보를 `colonova-doc-router-publisher` 일괄 갱신(Batch Refresh) 또는 단건 update 경로로 갱신.
- 수시: 특정 폴더 spot-check, 또는 stale로 지목된 문서를 page ID와 함께 router-publisher에 전달.

broad 감사가 만든 로컬 Markdown 리포트를 다음 실행의 prior report로 넘기면 "이전 감사 대비 변화"(신규/해소/재등장/악화)를 비교할 수 있습니다.

### 주기 실행 자동화

위 주기를 사람의 기억에만 맡기지 말고 자동화하세요. `colonova-folder-audit`은 감사 완료 후 다음 권장일을 `/schedule`로 등록할지 직접 제안하며, Claude Code의 `/schedule` 스킬로 cron 기반 정기 실행을 등록할 수 있습니다.

- `/schedule` 발동 후 "매 스프린트 종료(2주)마다 colonova-folder-audit으로 8.8 ColoNova 트리 전체 감사 실행(Archive·위치·Tree Gap·Pending supersession·Discussion closure·Under Review DR 점검 포함)"이라고 입력하면 cron 등록까지 안내됩니다.
- 월간 freshness 점검은 "매월 1일 colonova-folder-audit freshness 모드로 living standard·07 모니터링·Approved DR stale 점검"으로 등록합니다.
- broad 감사 리포트는 `colonova-audit-YYYY-MM-DD.md`로 저장되며, 다음 실행 시 같은 디렉터리의 최신 파일이 prior report로 자동 선택되어 "이전 감사 대비 변화"와 overdue(권장일 경과) 점검이 작동합니다.

이렇게 하면 "지속적 유지보수"가 advisory를 넘어 실제 정기 실행 루프로 연결됩니다.

## 운영 경계

- `colonova-folder-audit`는 페이지를 이동, 수정, 아카이빙하지 않습니다. 실행 큐와 근거만 만듭니다. stale 기준 문서는 Archive가 아니라 `Refresh required` 후보로 분류합니다.
- `colonova-doc-router-publisher`는 게시 전 추천 parent, 제목, 문서 유형, 템플릿, 변환 본문을 먼저 보여줍니다.
- Confluence 생성 또는 업데이트는 사용자의 명시 승인 후에만 수행합니다.
- 생성 또는 수정 후에는 page ID readback으로 제목, 부모, 주요 섹션, 빈 본문 여부를 확인합니다.
- live 폴더 제목은 ` - ColoNova` suffix를 포함하며, parent는 page ID로 resolve합니다. `06. 장애 / Incident`는 분류표에 정의됐으나 live 미생성 상태로, 게시 전 폴더 생성 승인이 필요합니다.
- live Confluence root와 분류 가이드가 기준의 SSOT입니다.
