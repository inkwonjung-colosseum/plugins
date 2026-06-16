# planning-kit

기획 전문가가 즉시 쓸 수 있는 심층 인터뷰 + 정책서·기능설계서 생성 + 리뷰 + SSOT 감사 + Confluence 발행 + AI 한글 윤문 6-skill 플러그인입니다. 모호한 아이디어를 심층 인터뷰로 먼저 명확화하고, 입력 하나(텍스트·파일·폴더·URL·이미지)를 **기획 레벨** 정책서·기능설계서로 변환하고, 완성된 2-doc 쌍을 외부 SSOT·의존성 관점으로 검토하며, SSOT corpus를 감사하고, Confluence 후보로 발행합니다. Claude Code / Codex / Cursor 3개 플랫폼을 지원합니다.

- **버전:** `0.7.0`
- **라이선스:** MIT
- **작성자:** inkwonjung-colosseum
- **총 Skill 수:** 6 (인터뷰 1 + 생성 1 + 리뷰 1 + 감사 1 + 발행 1 + 윤문 1)

## 설계 원칙 — 린(lean) 기획 레벨

이 플러그인은 PM·기획자가 쓰는 **기획 레벨** 문서만 다룹니다. 구현 상세와 전략 장식은 의도적으로 담지 않습니다.

- 정책서: 정책 규칙·상태·역할·권한·예외·연동. 사업 케이스(KPI/OKR)·이해관계자·리스크 레지스터·로드맵 같은 전략 장식은 **다루지 않습니다**.
- 기능설계서: 화면·흐름·동작·메시지. 데이터 모델·API/이벤트 계약·NFR 수치·테스트 시나리오·페르소나/여정 같은 구현·UX 심화는 **다루지 않습니다** (개발자 몫).
- 요구사항 ID는 `POL-`(정책 규칙)·`FUNC-`(기능 흐름·동작) **2종만** 씁니다. 두 문서는 헤더 `관련 문서`와 inline 참조로 연결하며, 별도 ID 컬럼·매트릭스를 만들지 않습니다.

> 구현 상세·심층 도메인이 필요하면 `logistics-kit` 등 도메인 플러그인이 담당합니다. planning-kit은 그 앞단의 순수 기획 산출물에 집중합니다.

## Skills

| 스킬 | 목적 |
|---|---|
| `planning-interview` | 모호한 기획 아이디어를 소크라테스식 1문1답으로 명확화하고, 목표·정책·기능·성공기준 4차원 모호도를 점수화하며 기획 challenge 4모드로 가정을 압박해, 임계 이하면 명확도 리포트 + planning-format 핸드오프 제안 (문서 생성 안 함) |
| `planning-format` | 입력 하나를 기획 레벨 정책서·기능설계서로 변환하고 기본 저장 + 체크 항목을 출력 |
| `planning-review` | 완성된 2-doc 쌍을 외부 SSOT 교차검증(R1)·링크/의존성 완결성(R2)·교차 일관성(R3), 물류 신호 시 도메인 lens(R4)로 심층 리뷰 (생성·수정 안 함) |
| `planning-publish-confluence` | context 또는 저장 폴더의 두 문서를 `v0.7` 후보로 발행하고 쓰기 후 readback 검증 |
| `ssot-audit` | 독립 `SSOT` 표시 폴더 Markdown의 구조·내용과 backlog 감사 |
| `humanize-korean` | AI가 쓴 한글 텍스트의 번역투·AI 티(10 카테고리 40+ 패턴)를 사람 글처럼 윤문 (의미 불변) |

**파이프라인:** `planning-interview`(명확화) → `planning-format`(생성) → `planning-review`(검증) → `planning-publish-confluence`(발행). `ssot-audit`·`humanize-korean`은 독립 보조 스킬입니다.

## planning-interview

```text
/planning-kit:planning-interview "주문 취소 기능을 만들고 싶은데 아직 모호해"
/planning-kit:planning-interview "..." --threshold 0.15 --no-context
```

모호한 아이디어를 한 번에 한 질문으로 명확화하는 인터뷰어입니다. 매 라운드 가장 약한 차원(목표·정책·기능·성공기준)을 타겟해 가정을 드러내고, 답변마다 모호도를 채점해 투명하게 보여줍니다. `모호도 = 1 − (목표·0.25 + 정책·0.35 + 기능·0.25 + 성공기준·0.15)`이며 — 정책·규칙 비중이 가장 큽니다(기획의 핵심 산출물) — 기본 임계는 `0.2`입니다. 라운드가 깊어지면 기획 challenge 4모드(범위 축소 R3+·이해관계자 R5+·정책 충돌 R7+·엣지/예외 R9+)를 각 1회 주입해 가정을 압박합니다.

**산출물은 명확도 리포트뿐입니다** — 정책서·기능설계서를 만들지 않고, 모호도가 임계 이하면 `## 결론`·`## 명확도`·`## 합의된 결정`·`## 미결 사항`·`## 다음 단계`로 정리한 뒤 `planning-format` 호출을 제안합니다(자동 호출 안 함). 옵션: `--threshold <0~1>`, `--no-context`, `--max-rounds <n>`(기본 18).

> 개발자용 deep-interview에서 1문1답·4차원 점수·임계 게이트에 더해 challenge 모드를 **기획 도메인용 4종(범위 축소·이해관계자·정책 충돌·엣지/예외)으로 이식**했습니다. 단 수학적 topology gate·ontology 수렴추적·multi-component rotation·lateral review panel·auto-research/answer fragment의 무거운 머신은 의도적으로 제외한 **린 코어**입니다.

## planning-format

```text
/planning-kit:planning-format "주문 취소 정책 ..."
/planning-kit:planning-format ./docs/draft/주문취소.md
```

옵션은 없습니다. fetch·이미지 해석·자가검증·저장은 항상 수행하며, 산출물은 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/`에 무조건 저장됩니다.

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

저장 실패 fallback만 `## 정책서`, `## 기능설계서`, `## 체크해야 할 항목` 순서로 전문을 보여줍니다.

**템플릿 구조** — 정책서는 11섹션(목적·적용 범위·용어 정의·정책 원칙·세부 규칙(`POL-`)·상태 및 처리 기준·역할과 권한·예외 및 승인 기준·외부 연동 정책·미결 사항·AI 검증 제외 사항), 기능설계서는 1–7·10–11 섹션(개요·범위·사용자 흐름(`FUNC-`)·화면과 입력 항목·기능 동작·권한과 데이터 접근·예외와 메시지·미결 사항·AI 검증 제외 사항)으로 **8·9는 결번**입니다.

## planning-review

```text
/planning-kit:planning-review
/planning-kit:planning-review planning/Zone-관리--2026-05-12-120000/
```

인자 없음이면 직전 `planning-format` 출력의 `## 저장 파일`이 정확히 하나의 저장 폴더를 가리킬 때만 두 파일을 읽습니다. 정책서 1개 + 기능설계서 1개를 식별하고 모호하면 중단합니다. 옵션은 없으며 모든 동작이 기본 ON입니다 — SSOT 표식 폴더는 항상 R1 외부 교차검증 소스로 포함하고(적격 SSOT 없으면 R1 보류), 입력·SSOT 양쪽 URL fetch·이미지 해석을 항상 수행합니다. R1+R2+R3을 한 패스로 돌리고, 물류 신호가 있으면 R4를 추가합니다(병합 우선순위 `R1 > R2 > R3 > R4`). 출력은 `## 결론`, `## 검토 결과`, `## 체크해야 할 항목` 순서입니다.

"미결 사항" 섹션·`(Non-MVP)` 항목·8·9 결번은 검토 제외이며, 구 무거운 구조(GWT·NFR 수치·data/API/event 계약·RACI·로드맵 DoR/DoD)의 부재를 finding으로 만들지 않습니다.

## planning-publish-confluence

```text
/planning-kit:planning-publish-confluence planning/Zone-관리--2026-05-12-120000/
```

지원 입력은 인자 없음 context memory 또는 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 저장 폴더 1개입니다. URL, 임의 단일 `.md`, 여러 폴더, 중첩 planning 경로는 거부합니다. 쓰기 전 확인과 쓰기 후 readback을 유지합니다. publish label `v0.7`은 의도적으로 SSOT cutoff 미만이라 발행 사본은 SSOT corpus로 승격되지 않습니다.

## ssot-audit

`planning/**`, `.planning-kit/**`, dependency/vendor/build/cache/generated 경로를 제외하고, 독립 `SSOT` 표시 폴더 Markdown만 감사합니다. 파일명 basename에서 추출한 버전이 cutoff `>= v0.8`이거나 버전 표기가 없는 파일만 corpus 후보입니다. `v0.7` 이하 파일은 `버전 미달`로 별도 집계되며 발견/권고 판단에서 제외됩니다. 버전 비교는 semantic compare(`v0.10 > v0.9`)로 동작합니다. 옵션: `--ssot-include`, `--exclude`, `--axes <structure,content>`, `--no-follow-links`, `--no-image`.

## humanize-korean

```text
/planning-kit:humanize-korean ./planning/.../주문취소_정책서.md
```

AI(ChatGPT·Claude·Gemini)가 쓴 한글 텍스트의 "AI 티"를 한 번의 흐름 안에서 탐지·윤문·자체검증까지 끝내는 단일 자기완결 스킬입니다. 번역투·영어 인용 과다·기계적 병렬·관용구·피동태 남발·접속사 남발·리듬 균일성·이모지/불릿 과다 등 10대 카테고리 40+ 패턴을 다룹니다. **의미 불변**(사실·수치·날짜·고유명사·인용 100% 보존)을 철칙으로 하고, 변경률 30% 초과 시 경고·50% 초과 시 롤백합니다. 기획 산출물 초안의 AI 티를 다듬을 때도 사용합니다.

> [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai)의 `humanize-korean` v1.5 fast-path를 planning-kit용 단일 자기완결 스킬로 인라인한 것입니다. 원본의 strict 5인 파이프라인·웹 서비스·metric 엔진은 이식하지 않았습니다.

## SSOT 진입 게이트 요약

`ssot-audit` corpus 진입은 다음 세 조건을 모두 통과해야 합니다.

1. 폴더 path segment에 독립 `SSOT` token (공백·대괄호·소괄호·중괄호·underscore 단위 split, case-insensitive).
2. `planning/**`·`.planning-kit/**`·기본 제외 경로 밖.
3. 파일명 basename에서 `v(\d+)\.(\d+)` 마지막 매칭이 없거나, 매칭이 있으면 `(major, minor) >= (0, 8)`.

## 현재 품질 상태

2026-06-16 기준 `plugin-eval analyze` 정적 평가에서 0.7.0 플러그인과 6개 스킬(`planning-interview`·`planning-format`·`planning-review`·`planning-publish-confluence`·`ssot-audit`·`humanize-korean`)은 **모두** `100/100` (Grade A), 실패·경고·info 0건입니다. 직전 cost 경고 2건(`invoke_cost_tokens`·`trigger_cost_tokens` heavy)은 **스킬 6개를 그대로 둔 채** SKILL.md 본문을 `references/*`로 더 분리하고 manifest·description을 압축해 두 예산을 모두 `moderate` 밴드로 내려 해소했습니다. `description-trigger-weak` 같은 구조·트리거 결함은 0건입니다. 점수보다 파이프라인 완결성(명확화 앞단 확보)을 우선하는 원칙은 유지합니다.

두 예산은 baseline `moderate` 임계 바로 아래라 헤드룸이 크지 않습니다(trigger·invoke 각각 한 자릿수 토큰 여유). 스킬 본문을 키울 때는 상세를 SKILL.md에 인라인하지 말고 `references/*`로 옮겨 골격만 남겨야 다시 `heavy`로 넘어가지 않습니다.

`planning-interview`는 SKILL.md를 골격만 두고 인터뷰 루프·채점 공식·출력 계약을 `references/runtime.md`로 분리해 적재 비용을 억제했습니다.

0.7.0 lean 패스에서 해소한 경고: `invoke_cost_tokens`/`trigger_cost_tokens` heavy — `humanize-korean`·`planning-interview` SKILL.md 본문을 references로 더 분리(humanize 처리 순서를 `quick-rules.md`로 이전), `planning-review`·`planning-format` dispatch 상세를 runtime으로 위임, manifest `longDescription`·`defaultPrompt`와 스킬 description을 압축. 직전 0.5.0: `default-prompt-too-many`(4→3 정리), `humanize-korean:description-trigger-weak`, humanize-korean SKILL.md lean화.

3-플랫폼 일관성: `.claude-plugin`·`.codex-plugin`·`.cursor-plugin` 매니페스트는 name·version(`0.7.0`)·description·skills가 동일하고, 3개 marketplace catalog(`.claude-plugin`·`.cursor-plugin`·`.agents/plugins`)의 planning-kit 엔트리도 version·description이 일치합니다.

벤치마크: `.plugin-eval/benchmark.json`에 planning-kit 실제 태스크 3종(정책서·기능설계서 생성 must-pass / read-only SSOT 감사 / Confluence 발행 경계-거부)을 정의했습니다. `plugin-eval benchmark`는 실제 `codex exec`를 돌려 `.plugin-eval/runs/<timestamp>/`에 로그와 usage를 남기고, 그 usage를 `plugin-eval analyze --observed-usage`로 되먹여 정적 추정과 대조할 수 있습니다. 2026-06-16 실측에서 3개 시나리오 모두 `completed`(실패 shell 0건)였고, must-pass는 2-doc을 디스크에 생성, 감사·발행 경계 시나리오는 파일을 생성·수정하지 않고(발행은 URL 입력을 거부) live write를 차단했습니다.

`plugin-eval analyze`의 정적 예산은 manifest·`SKILL.md`·bundled reference의 패키지 비용만 봅니다. `plugin-eval benchmark`의 관찰 사용량은 Codex 실행 세션 전체 맥락을 포함하므로 두 값은 같은 기준이 아닙니다. 벤치마크는 비용 절대값보다 시나리오 성공 여부·잘못된 파일 수정 여부·live write 차단 여부를 우선 신호로 봅니다. 그래서 `analyze --observed-usage`는 관찰 input(세션 전체, 평균 ~219k 토큰)과 정적 활성 추정(~3.2k 토큰)의 큰 격차 때문에 `observed-usage-estimate-drift`를 의도적으로 표시합니다 — 이는 두 측정의 기준이 다르다는 신호이지 planning-kit 패키지 비용 결함이 아니며, planning-kit의 정식 점수는 plain `plugin-eval analyze`의 `100/100`(Grade A)입니다.

구조 검증:

```bash
python3 -m json.tool planning-kit/.claude-plugin/plugin.json >/dev/null
python3 -m json.tool planning-kit/.codex-plugin/plugin.json >/dev/null
python3 -m json.tool planning-kit/.cursor-plugin/plugin.json >/dev/null
claude plugin validate ./planning-kit
git diff --check
```
