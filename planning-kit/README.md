# planning-kit (0.3.0)

기획 초안을 정책서·기능설계서로 정리하고, review, SSOT audit, Confluence 후보 발행까지 이어주는 4-skill 플러그인입니다. 0.3.0 runtime은 0.2.14의 결과 우선 출력과 저장 파일 handoff 계약을 유지하면서, SSOT corpus 진입 조건에 파일명 basename version cutoff `>= v0.8`(또는 버전 표기 없음)을 추가합니다. `v0.7` 이하 파일은 `버전 미달`로 별도 집계되고 corpus에서 제외됩니다.

## 현재 품질 상태

2026-05-19 기준 `plugin-eval` 정적 평가에서 플러그인과 4개 스킬 모두 `100/100`, 실패/경고 0건입니다.

- `planning-kit`: `100/100`
- `planning-format`: `100/100`
- `planning-review`: `100/100`
- `planning-publish-confluence`: `100/100`
- `ssot-audit`: `100/100`

검증도 함께 통과해야 최신 상태로 봅니다.

```bash
python3 -m unittest discover -s tests
python3 -m json.tool planning-kit/.claude-plugin/plugin.json >/dev/null
python3 -m json.tool planning-kit/.codex-plugin/plugin.json >/dev/null
claude plugin validate ./planning-kit
git diff --check
```

## 평가 메모

`plugin-eval analyze`의 정적 예산은 플러그인 manifest, `SKILL.md`, bundled reference의 패키지 비용만 봅니다. `plugin-eval benchmark`의 관찰 사용량은 Codex 실행 세션의 전체 시스템/도구/설치 플러그인/작업공간 맥락까지 포함하므로, 두 값은 같은 기준의 토큰 비용이 아닙니다. 기존 benchmark usage log를 `--observed-usage`로 강제 연결하면 이 전체 세션 비용 때문에 estimate drift가 발생할 수 있습니다.

벤치마크는 비용 절대값보다 시나리오별 성공 여부, 잘못된 파일 수정 여부, live write 차단 여부를 우선 신호로 봅니다. 점수 gate는 정적 `plugin-eval analyze`와 구조 검증 명령을 기준으로 판단합니다.

## Skills

| 스킬 | 목적 |
|---|---|
| `planning-format` | 입력을 정책서·기능설계서로 변환하고 기본 저장 파일과 체크해야 할 항목을 출력 |
| `planning-review` | 산출물을 기준 문서 일치성, 검증가능성, 영향 분석으로 통합 review |
| `planning-publish-confluence` | context 또는 명시 저장 폴더의 두 문서를 `v0.7` 후보로 발행하고 readback 검증 |
| `ssot-audit` | 독립 `SSOT` 표시 폴더 Markdown의 구조·내용과 backlog 감사 |

## planning-format

```text
/planning-kit:planning-format "주문 취소 정책 ..."
/planning-kit:planning-format ./docs/draft/주문취소.md --no-save
```

기본은 저장입니다. `--save`는 no-op alias이고, 저장하지 않으려면 `--no-save`를 사용합니다.

```markdown
# [기능명]
- 입력: ...
- 산출물: 정책서, 기능설계서
- 검증: 확인 필요 N건, 문서 보강 M건 / 확인 필요 없음
- 저장: planning/[안전기능명]--YYYY-MM-DD-HHMMSS/

## 저장 파일
- 정책서: planning/[안전기능명]--YYYY-MM-DD-HHMMSS/[안전기능명]_정책서.md
- 기능설계서: planning/[안전기능명]--YYYY-MM-DD-HHMMSS/[안전기능명]_기능설계서.md

## 체크해야 할 항목
...
```

`--no-save`와 저장 실패 fallback은 `## 정책서`, `## 기능설계서`, `## 체크해야 할 항목` 순서로 전문을 보여줍니다.

## planning-review

```text
/planning-kit:planning-review
/planning-kit:planning-review planning/Zone-관리--2026-05-12-120000/
```

인자 없음이면 직전 `planning-format` 출력의 `## 저장 파일`이 정확히 하나의 저장 폴더를 가리킬 때만 두 파일을 읽습니다. 출력은 `## 결론`, `## 검토 결과`, `## 체크해야 할 항목` 순서입니다.

## planning-publish-confluence

```text
/planning-kit:planning-publish-confluence planning/Zone-관리--2026-05-12-120000/
```

지원 입력은 인자 없음 context memory 또는 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 저장 폴더 1개입니다. URL, 임의 단일 `.md`, 여러 폴더, 중첩 planning 경로는 거부합니다. 쓰기 전 확인과 쓰기 후 readback을 유지합니다.

## ssot-audit

`planning/**`, `.planning-kit/**`, dependency/vendor/build/cache/generated 경로를 제외하고, 독립 `SSOT` 표시 폴더 Markdown만 감사합니다. 0.3.0부터 파일명 basename에서 추출한 버전이 cutoff `>= v0.8` 또는 버전 표기 없음만 corpus 후보입니다. `v0.7` 이하 파일은 `버전 미달`로 별도 집계되며 발견/권고 판단에서 제외됩니다. 버전 비교는 semantic compare(`v0.10 > v0.9`)로 동작합니다.

## SSOT 진입 게이트 요약

corpus 진입은 다음 세 조건을 모두 통과해야 합니다.

1. 폴더 path segment에 독립 `SSOT` token (공백·대괄호·소괄호·중괄호·underscore 단위 split, case-insensitive).
2. `planning/**`·`.planning-kit/**`·기본 제외 경로 밖.
3. 파일명 basename에서 `v(\d+)\.(\d+)` 마지막 매칭이 없거나, 매칭이 있으면 `(major, minor) >= (0, 8)`.

`planning-publish-confluence`의 publish label `v0.7`은 의도적으로 cutoff 미만이라 Confluence 발행 사본은 SSOT corpus로 승격되지 않습니다.
