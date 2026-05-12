# planning-kit (0.2.14)

`planning-kit`은 기획 초안을 정책서·기능설계서로 정리하고, 그 산출물을 외부 기준과 비교하며, Confluence `v0.7` 후보 문서로 발행하고, 선언된 SSOT 문서 묶음의 구조·내용 품질을 감사하는 플러그인입니다.

0.2.14의 핵심 변경은 결과 우선 화면과 저장 파일 handoff입니다.

- `planning-format`은 기본적으로 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 저장 파일을 만들고, 저장 성공 화면에는 `## 저장 파일`과 `## 체크해야 할 항목`만 보여줍니다.
- 화면에 정책서·기능설계서 전문을 펼치려면 `--no-save`를 사용합니다. 저장 실패 시에도 결과 손실을 막기 위해 `--no-save`와 같은 본문 포함 구조로 fallback 출력합니다.
- `planning-review`는 직전 `planning-format` 저장 성공 출력의 `## 저장 파일`이 정확히 1개 저장 폴더를 가리키면 canonical 정책서·기능설계서 두 파일을 읽어 review 대상 본문으로 사용합니다.
- `planning-review`의 신규 출력은 `## 결론`, `## 검토 결과`, `## 체크해야 할 항목` 순서입니다.
- `planning-publish-confluence`는 기존 context memory 발행을 유지하고, 명시적 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 저장 폴더 입력도 지원합니다. 저장 폴더에서는 canonical 정책서·기능설계서 두 파일만 읽습니다.
- `planning/**`과 `.planning-kit/**`은 review/publish 입력으로는 사용할 수 있지만 SSOT 근거에서는 항상 제외합니다.

Claude Code · Codex 양쪽에서 같은 `skills/`를 공유합니다.

## 빠른 시작

### Claude Code

```text
/planning-kit:planning-format 주문 취소 정책 정리해줘. 사용자가 결제 후 24시간 내 1회 취소 가능.
/planning-kit:planning-review
/planning-kit:planning-publish-confluence planning/주문-취소--2026-05-12-120000/
/planning-kit:ssot-audit
```

### Codex

```text
$planning-format 주문 취소 정책 정리해줘. 사용자가 결제 후 24시간 내 1회 취소 가능.
$planning-review
$planning-publish-confluence planning/주문-취소--2026-05-12-120000/
$ssot-audit
```

## 스킬

| 스킬 | 목적 |
|---|---|
| `planning-format` | 텍스트·파일·디렉터리·URL·이미지를 정책서와 기능설계서로 변환하고 기본 저장 파일과 체크해야 할 항목을 출력 |
| `planning-review` | planning-format 산출물을 SSOT 충돌, acceptance criteria 검증가능성, 의존 영향 3축으로 review하고 결론과 검토 결과를 먼저 출력 |
| `planning-publish-confluence` | 현재 context memory 또는 명시적 저장 폴더의 정책서·기능 설계서 두 본문을 `v0.7` Confluence 후보 문서로 발행하고 readback 검증 |
| `ssot-audit` | 선언된 `SSOT` 표시 폴더 Markdown의 구조·내용 품질과 개선 backlog 감사 |

## planning-format

입력 예:

```text
/planning-kit:planning-format "주문 취소 정책 ..."
/planning-kit:planning-format ./docs/draft/주문취소.md
/planning-kit:planning-format ./docs/draft/입고기능/
/planning-kit:planning-format https://wiki.example/spec/order-cancel
/planning-kit:planning-format https://a.com/p1 https://b.com/p2
/planning-kit:planning-format ./diagrams/order-flow.png
/planning-kit:planning-format ./docs/draft/주문취소.md --no-save
```

기본 저장 성공 출력:

```markdown
# [기능명]

- 입력: ...
- 산출물: 정책서, 기능설계서
- 검증: 확인 필요 N건, 문서 보강 M건 / 확인 필요 없음
- 저장: planning/[안전기능명]--YYYY-MM-DD-HHMMSS/

---

## 저장 파일

- 정책서: planning/[안전기능명]--YYYY-MM-DD-HHMMSS/[안전기능명]_정책서.md
- 기능설계서: planning/[안전기능명]--YYYY-MM-DD-HHMMSS/[안전기능명]_기능설계서.md

---

## 체크해야 할 항목
...
```

`--no-save` 출력은 `## 정책서`, `## 기능설계서`, `## 체크해야 할 항목` 순서로 전문을 화면에 펼칩니다. 기존 `--save`는 0.2.x 호환용 no-op alias로 허용되며 옵션이 없어도 같은 저장 동작입니다.

저장 경로 예:

```text
planning/Zone-관리--2026-05-12-120000/
  Zone-관리_정책서.md
  Zone-관리_기능설계서.md
```

## planning-review

입력 예:

```text
/planning-kit:planning-review
/planning-kit:planning-review ./planning/Zone-관리--2026-05-12-120000/
/planning-kit:planning-review ./planning/Zone-관리--2026-05-12-120000/Zone-관리_정책서.md
/planning-kit:planning-review ./docs/주문-정책.md ./docs/주문-기능.md
/planning-kit:planning-review "## 정책서 ... ## 기능설계서 ..."
/planning-kit:planning-review https://wiki.example/policy/order-cancel https://docs.example/feature/order-cancel
/planning-kit:planning-review --axes ac
```

0개 인자 실행 시 직전 `planning-format` 출력에서 본문을 찾습니다. 0.2.14 기본 저장 성공 출력처럼 본문이 없고 `## 저장 파일`만 있으면, 정책서와 기능설계서 path가 같은 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 폴더를 가리킬 때만 두 파일을 읽습니다. 후보가 0개, 2개 이상, 서로 다른 폴더, 누락 파일이면 임의 선택하지 않고 경로 명시를 요청합니다.

기본 출력 순서:

```markdown
# [기능명] 검토 결과

- 판정: 통과 / 조건부 통과 / 수정 필요 / 검토 필요 / 비교 불가
- 검증 신뢰도: 충분 / 제한적 / 낮음 — 이유
- 입력: ...
- 점검 축: 기준 문서 일치성, 검증가능성, 영향 분석
- 발견: P0 N건, P1 N건, P2 N건

---

## 결론
...

---

## 검토 결과
...

---

## 체크해야 할 항목
...
```

## planning-publish-confluence

입력 예:

```text
/planning-kit:planning-publish-confluence
/planning-kit:planning-publish-confluence planning/Zone-관리--2026-05-12-120000/
```

지원 입력:

- 인자 없음: 현재 context memory 안에서 정책서 1개와 기능 설계서 1개를 찾습니다.
- 저장 폴더 경로 1개: `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` direct child 폴더에서 `*_정책서.md`, `*_기능설계서.md` 두 파일만 읽습니다.

금지 입력:

- URL 또는 Confluence page URL
- 임의 단일 `.md` 파일
- 여러 저장 폴더
- `planning/foo/`, `planning/drafts/...`, `planning/여러/중첩/...`
- `planning/` 밖의 경로

기본 Confluence parent는 `https://colosseum.atlassian.net/wiki/spaces/PROD/pages/1767604270/SSOT`입니다. 실행 중 기본 parent 사용, 직접 parent URL 입력, 취소를 선택하고, Confluence write 전에는 target hierarchy, 신규/수정 page, `v0.7` label, content fingerprint를 최종 확인합니다. write 후에는 readback으로 page id, parent, version, fingerprint, 문서 종류 marker를 검증합니다.

## ssot-audit

`ssot-audit`는 현재 프로젝트의 독립 `SSOT` 표시 폴더 Markdown만 구조·내용 2축으로 감사합니다. `planning/**`, `.planning-kit/**`, dependency/vendor/build/cache/generated 경로는 기준 문서 근거에서 제외합니다.

## 검증

```bash
python3 -m unittest discover -s planning-kit/tests
python3 -m json.tool planning-kit/.claude-plugin/plugin.json
python3 -m json.tool planning-kit/.codex-plugin/plugin.json
claude plugin validate ./planning-kit
git diff --check
```
