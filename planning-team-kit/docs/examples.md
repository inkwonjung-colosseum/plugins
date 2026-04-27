# planning-team-kit Examples

## 신규 정책서

```text
$plan-draft 주문 취소 정책 만들어줘
```

예상 흐름:

1. 로컬 Confluence export에서 관련 정책서, 상위 설계서, 최근 결정사항을 확인한다.
2. 기존 문서가 없으면 선택한 export source의 hierarchy와 유사 문서 위치를 기준으로 신규 위치를 제안한다.
3. 취소 가능 상태, 후속 작업 상태, 외부 연동 동기화 같은 부족한 조건을 한 번에 하나씩 질문한다.
4. 정책서 템플릿으로 초안을 만든다.

초안에 `[미정]`, `[가정]`, 충돌 경고가 있으면 출력에 `Publish gate: review-required`가 포함된다.

## 초안 검토

```text
$plan-review
```

검토 관점:

- 근거: 기존 Confluence 문서와 충돌하는지 확인한다.
- 범위: 결정해야 할 정책과 예외가 빠졌는지 확인한다.
- 실행: 개발팀이 구현에 필요한 상태, 조건, 예외를 이해할 수 있는지 확인한다.

결과는 `pass`, `conditional pass`, `수정 필요` 중 하나다.

## Confluence 반영

```text
$plan-publish
```

publish는 바로 쓰지 않는다. 먼저 local export stale 여부, review gate, 신규 parent page, 기존 page version을 확인한다.

초안에 `[미정]`, `[가정]`, 충돌 경고가 있으면 다음 중 하나가 필요하다.

- `$plan-review` 결과가 `pass` 또는 `conditional pass`
- 사용자의 명시적 확인: `review 없이 publish 진행`

마지막으로 사용자가 `yes`를 입력해야 MCP write가 실행된다.

## 기존 문서 수정

```text
$plan-draft 입고 신청 기능 설계서 업데이트해야 해
```

유사한 기존 문서가 있으면 `confluence/confluence-lock.json`에서 `page_id`, `version`, `export_path`를 확인하고 수정 모드로 출력한다. 변경 내용은 `[기존]`과 `[변경]` 형태로 보여준다.
