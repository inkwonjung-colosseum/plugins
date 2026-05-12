# Confluence Page Contract

`planning-publish-confluence`의 Confluence parent, hierarchy, duplicate, update, write, readback 계약이다.

## 1. Parent

기본 parent URL:

```text
https://colosseum.atlassian.net/wiki/spaces/PROD/pages/1767604270/SSOT
```

표시 이름:

```text
Product Team Space / SSOT
```

parent 검증은 기본 parent와 직접 입력 parent 모두에 적용한다.

- URL은 `https://colosseum.atlassian.net/wiki/spaces/`로 시작한다.
- page id를 추출할 수 있다.
- page를 읽을 수 있다.
- page title, page id, current version, ancestor path를 확인한다.
- page가 archived/deleted 상태가 아니다.
- selected parent 아래 child page를 만들 권한이 있다.
- update target이 있으면 해당 page update 권한이 있다.

space key가 `PROD`가 아니면 최종 확인에 space key와 title을 명시하고, 사용자 확인 없이는 진행하지 않는다.

## 2. v0.7 Title Hierarchy

0.2.13 발행은 확정 SSOT가 아니므로 Confluence title과 metadata에 항상 `v0.7` 발행 label을 붙인다.

```text
[선택된 parent]
└── [기능명] v0.7
    ├── [기능명] 정책서 v0.7
    └── [기능명] 기능 설계서 v0.7
```

규칙:

- 발행 label은 `v0.7`로 고정한다.
- container page title은 `[기능명] v0.7`이다.
- policy child page title은 `[기능명] 정책서 v0.7`이다.
- feature child page title은 `[기능명] 기능 설계서 v0.7`이다.
- title에 `v0.7`이 빠지면 실패다.
- 기능명에 `/`, `\`, 줄바꿈, control character가 있으면 공백으로 정규화한다.
- title 앞뒤 공백은 제거하고, 연속 공백은 1개로 줄인다.

## 3. Container Body

container page는 긴 문서 본문을 복제하지 않는다.

필수 metadata:

- 기능명
- 발행 label: `v0.7`
- 문서 상태: `SSOT 후보`
- 정책서 child link
- 기능 설계서 child link
- 발행 일시
- 발행 도구: `planning-kit planning-publish-confluence`
- 발행 기준: `현재 context memory`
- operation id
- 정책서 content fingerprint
- 기능 설계서 content fingerprint
- target page id와 version (readback 후 갱신)

## 4. Child Body

child page에는 compact publish metadata block과 해당 문서 본문만 넣는다.

필수 metadata:

- 문서 종류: `정책서` 또는 `기능 설계서`
- 기능명
- 발행 label: `v0.7`
- 문서 상태: `SSOT 후보`
- 발행 일시
- 발행 도구: `planning-kit planning-publish-confluence`
- 발행 기준: `현재 context memory`
- content fingerprint
- operation id
- source 상태: `context memory`
- 검토 상태: context에 `planning-review` 통과/수정 필요 신호가 명확하면 반영, 없으면 `확인 불가`

## 5. Duplicate Lookup

쓰기 전 target hierarchy 기준으로 2단계 조회한다.

1. selected parent children에서 `[기능명] v0.7` container title 중복 확인.
2. container가 새로 생성될 예정이면 child title 중복은 preflight plan에서 `중복 없음`으로 표시.
3. container가 이미 있거나 update target이면 해당 container children에서 `[기능명] 정책서 v0.7`, `[기능명] 기능 설계서 v0.7` 중복 확인.
4. selected parent 바로 아래 정책서/기능 설계서 title 또는 `v0.7` 없는 unversioned title은 legacy flat-child collision으로 분류.
5. suffix 적용 후와 최종 write 직전에 같은 조회를 다시 수행해 race를 확인.

## 6. Duplicate Handling

같은 target 위치에 같은 title이 있으면 자동 덮어쓰기하지 않는다.

선택지:

| 선택지 | 동작 |
|---|---|
| 기존 페이지 업데이트 | 같은 target 위치의 같은 역할 page와 같은 `v0.7` label page만 full-body replacement로 업데이트 |
| 새 title로 생성 | title suffix를 입력받아 새 page 생성 |
| 취소 | Confluence 변경 없이 종료 |

`v0.7` 없는 unversioned page는 update target이 아니다.

page move는 0.2.13 범위 밖이다.

## 7. Update Preflight

기존 page update는 다음 preflight를 모두 최종 확인에 포함한다.

- page id
- page URL
- current version
- current parent title과 URL
- last updated
- page 역할 marker: `container`, `정책서`, `기능 설계서`
- 발행 label: `v0.7`
- 교체 범위: full-body replacement
- 기존 본문 fingerprint
- 새 본문 fingerprint

업데이트 직전 current version을 다시 읽고 preflight version과 다르면 version conflict로 취소한다.

금지:

- automatic merge
- blind overwrite
- append update
- unversioned page update
- parent page move

## 8. Write Order

쓰기 전 모든 page body를 memory에서 render하고 fingerprint를 계산한다.

Confluence page create/update 순서:

1. 최종 확인 후 parent와 update target page version을 다시 읽는다.
2. parent가 바뀌었거나 update target version이 preflight와 다르면 version conflict로 취소한다.
3. container page create/update.
4. container readback.
5. container readback 실패 시 child write 중단.
6. 정책서 child page create/update.
7. 정책서 readback 실패 시 기능 설계서 write 중단.
8. 기능 설계서 child page create/update.
9. 기능 설계서 readback.

## 9. Readback

각 readback은 다음을 확인한다.

- page id
- title (`v0.7` 포함)
- parent id
- version 증가 또는 신규 version
- operation id
- content fingerprint
- 문서 종류 marker
- 발행 label: `v0.7`

readback 없이 성공 처리하지 않는다.

## 10. Partial Failure

Confluence write는 transaction이 아니므로 자동 rollback/delete하지 않는다.

- 성공한 page는 삭제하지 않는다.
- 실패 이후 남은 write는 실행하지 않는다.
- 결과를 `부분 완료`로 표시한다.
- 성공 page URL, page id, version을 출력한다.
- 실패 page title, 실패 step, 실패 사유를 출력한다.
- 다음 실행에서 같은 operation id와 fingerprint가 확인되면 성공 page는 `변경 없음`으로 보고 남은 page만 재개할 수 있다.
- fingerprint가 다르면 자동 재개하지 않고 새 발행 시도로 취급해 최종 확인을 다시 받는다.
