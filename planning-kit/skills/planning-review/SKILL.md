---
name: planning-review
description: Use when 정책서 and 기능설계서 need external-SSOT, dependency, or logistics-domain review — planning-level only, never creates or auto-fixes docs.
---

# planning-review

`planning-format` 출력(정책서 + 기능설계서)을 검토하는 별도 호출 심층 리뷰어. 문서를 만들거나 고치지 않고 검토 결과만 낸다.

역할 경계 — 생성시 경량 자가검증과 구 무거운 구조 잔재 가드는 `planning-format`의 self-review가, SSOT 폴더 구조·위치·백로그 감사는 `ssot-audit`이, 물류 구현·심층 도메인은 `logistics-kit`이 담당한다. planning-review는 그 사이에서 완성된 2-doc 쌍을 외부 SSOT와 대조(R1)하고 문서 간 논리 완결성을 깊게(R2·R3) 본다.

## Inputs

- 인자 없음: 직전 `planning-format` 출력 또는 `## 저장 파일` 핸드오프(`planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 하나).
- `https?://` URL: 각 URL = 검토 소스 루트.
- 디렉터리 1개: 안에서 정책서+기능설계서를 찾는다.
- 파일 1개: 같은 폴더 동반 파일을 스캔해 짝을 식별.
- 비-URL 경로 2개: 파일명·헤딩으로 정책/기능 식별.
- 그 외: 붙여넣은 Markdown.
- 옵션: `--ssot-include`, `--no-input-fetch`, `--no-input-image`, `--no-ssot-fetch`, `--no-ssot-image`.
- SSOT 마커: `planning/**`·`.planning-kit/**` 제외. SSOT 표식 폴더는 파일명 버전 `>= v0.8` 이거나 버전 없을 때만 적격.

## Workflow

정책서 1개 + 기능설계서 1개를 식별한다. 모호하면 중단. SSOT 근거는 SSOT 표식 폴더만 (`planning/**` 절대 아님). R1+R2+R3을 한 패스로 돌리고, 물류 신호가 있으면 R4를 추가한다. 병합 우선순위 `R1 > R2 > R3 > R4`.

검토 대상은 린 정책서(1-11)·기능설계서(1-7·10-11, 번호 8·9 결번)다. "미결 사항" 섹션과 `(Non-MVP)` 항목은 검토 제외. 8·9 결번을 finding으로 잡지 않는다. 구 무거운 구조(AC Given-When-Then·NFR 수치·data/API/event 계약·F11/F12·RACI·Power×Interest·로드맵 DoR/DoD)는 검토 축이 아니며, 부재를 finding으로 만들지 않는다.

## Output Contract

- 순서: `# [기능명] 검토 결과` → `## 결론` → `## 검토 결과` → `## 체크해야 할 항목`.
- 코드펜스 래핑 금지. 진행 로그를 앞세우지 않는다.
- raw R* ID는 `## 상세 추적`에만.
- 깔끔한 표시 라벨만 — `SSOT corpus`·`fetch`·`connector fallback` 같은 내부어 노출 금지.

## References

Load on demand by step:

- `references/runtime.md` — 입력·옵션·dispatch·SSOT 마커·fetch·출력 계약.
- `references/review-axes.md` — R1 외부 SSOT 교차검증 · R2 링크·의존성 완결성 · R3 교차 일관성.
- `references/logistics-lens.md` — R4 물류 도메인 lens (A 상태·B 실패·C 식별자, signal-triggered).
