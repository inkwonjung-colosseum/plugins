---
name: plan-publish
description: "Publish a confirmed plan-draft output to Confluence through discovered MCP tools after stale, review, parent, and final-confirmation gates."
---

# plan-publish

`/planning-team-kit:plan-draft`으로 생성한 초안을 Confluence에 실제 반영하는 스킬.

## 호출

- Claude Code: `/planning-team-kit:plan-publish`
- Codex: `$plan-publish`

## 사전 조건

현재 대화에 `/planning-team-kit:plan-draft`이 생성한 초안이 있어야 한다.

## MCP 도구

MCP tool discovery로 현재 세션에서 사용 가능한 Confluence 쓰기 도구와 schema를 찾는다. 세부 매핑은 `references/publish-runbook.md`를 따른다.

- 신규 페이지: `createConfluencePage`
- 기존 수정: `updateConfluencePage`
- 두 도구를 찾을 수 없으면 Confluence MCP 연결 상태를 확인하라고 안내하고 중단한다.
- 도구 schema에 없는 인자를 추측해서 보내지 않는다.
- 예: 현재 Atlassian 도구가 `cloudId`, `spaceId`, `body`, `contentFormat`를 요구하면 그 schema를 우선한다.

## confluence-lock.json

경로: `confluence/confluence-lock.json`

구조:
```json
{
  "lockfile_version": 2,
  "last_export": "YYYY-MM-DDTHH:MM:SS+00:00",
  "orgs": {
    "{site_url}": {
      "spaces": {
        "{space_id}": {
          "pages": {
            "{page_id}": {
              "title": "문서 제목",
              "version": 1,
              "export_path": "export/source/path/파일명.md",
              "attachments": {}
            }
          }
        }
      }
    }
  }
}
```

## 동작 순서

### 1. Stale 체크
`confluence-lock.json`의 `last_export` 확인.
- 7일 이상 경과 → 경고 출력 후 계속 여부 확인
- 경고 메시지: "⚠️ 로컬 문서가 N일 전 데이터입니다. Confluence가 그 사이 변경됐을 수 있어요. 계속할까요? (yes / 취소)"

### 2. Review gate 체크

현재 대화의 `plan-draft` 초안과 이후 대화 내용을 확인한다.

다음 중 하나라도 있으면 `review-required` 상태로 판단한다.
- `Publish gate: review-required`
- `[미정]`
- `[가정]`
- 기존 Confluence 내용과의 충돌 경고

`review-required` 상태이면 아래 조건 중 하나가 충족되어야 다음 단계로 진행한다.
1. 현재 대화에 `/planning-team-kit:plan-review` 또는 `$plan-review` 결과가 있고 verdict가 `pass` 또는 `conditional pass`이다.
2. 사용자가 남은 `[미정]`, `[가정]`, 충돌 경고를 인지하고도 publish하겠다고 명시적으로 확인한다.

조건이 충족되지 않으면 MCP를 호출하지 않고 중단한다.

경고 메시지:
```
⚠️ publish 전에 review가 필요합니다

사유: [미정] / [가정] / 충돌 경고

먼저 /planning-team-kit:plan-review 를 실행하거나,
남은 항목을 인지하고도 반영하려면 "review 없이 publish 진행"이라고 명시해 주세요.
```

### 3. 신규 문서 parent 확정

신규 문서일 때만 수행한다.

1. `/planning-team-kit:plan-draft` 초안의 `위치`에서 parent export path를 계산한다.
   - 예: `<문서그룹>/<문서영역>/[문서].md` → `<선택한 export source root>/<문서그룹>/<문서영역>.md`
2. `references/publish-runbook.md`의 parent lookup 절차에 따라 path normalization 후 `confluence/confluence-lock.json`의 모든 org/space pages에서 parent 후보를 찾는다.
3. parent 후보가 정확히 1개이면 해당 page의 `site_url`, `space_id`, `page_id`, `title`, `export_path`를 사용한다.
4. parent 후보가 없음 또는 중복이면 추측하지 않는다. 사용자에게 parent page의 `page_id 또는 URL`을 요청하고, 확인된 값으로만 진행한다.

### 4. 최종 확인 화면 출력

**신규 문서:**
```
📄 Confluence에 새 페이지를 만듭니다

제목: [문서 제목]
위치: [상위 페이지 경로]
상위 페이지: [parent_title]
상위 페이지 ID: [parent_id]
상위 export_path: [parent_export_path]
Confluence site: [site_url]
Space ID: [space_id]

반영하시겠어요? (yes / 취소)
```

**기존 문서 수정:**
```
✏️ Confluence 페이지를 수정합니다

파일: [export_path]
페이지 ID: [page_id] (현재 버전: N → N+1)
Confluence site: [site_url]
Space ID: [space_id]

변경 내용:
[기존] ...
[변경] ...

반영하시겠어요? (yes / 취소)
```

### 5. 기획자 yes 확인 후 MCP 호출

**신규:**
```
createConfluencePage(
  cloudId: "{discovered_cloud_id}",
  spaceId: "{confirmed_space_id}",
  parentId: "{parent_page_id}",
  title: "{문서 제목}",
  body: "{마크다운 내용}",
  contentFormat: "markdown"
)
```

**수정:**
```
updateConfluencePage(
  cloudId: "{discovered_cloud_id}",
  pageId: "{page_id}",
  title: "{문서 제목}",
  body: "{수정된 마크다운 내용}",
  contentFormat: "markdown",
  includeBody: false
)
```

### 6. 완료 출력

```
✅ Confluence 반영 완료

페이지: [제목]
URL: {confirmed_site_url}/wiki/spaces/{confirmed_space_id}/pages/{page_id}

로컬 export는 직접 수정하지 않았습니다.
최신 내용을 반영하려면 Confluence export를 다시 실행하세요.

Claude Code:
/confluence-export-kit:export-org
/confluence-export-kit:index-export

Codex:
$export-org
$index-export
```

## 규칙

- 기획자 yes 확인 없이 MCP를 호출하지 않는다
- `[미정]`, `[가정]`, 충돌 경고가 남아 있으면 review 결과 또는 명시적 override 확인 없이 MCP를 호출하지 않는다
- MCP 호출 실패 시 에러 내용을 그대로 출력하고 중단한다. 재시도는 기획자 확인 후
- exported Markdown은 Confluence의 read-only snapshot으로 취급한다
- publish 성공 후에도 `confluence/confluence-lock.json`과 exported Markdown을 직접 수정하지 않는다
- 최신 로컬 문서가 필요하면 완료 화면의 export 재실행 안내를 따른다
