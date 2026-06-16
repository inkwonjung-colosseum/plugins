---
name: humanize-korean
description: Use when AI(ChatGPT·Claude)가 쓴 한글을 사람 글처럼 윤문할 때. 번역투·피동/접속사 남발·이모지 과다 등 40+ AI 티를 탐지해 의미는 두고 문체·리듬만 고친다. 트리거 — "AI 티 없애줘", "AI 윤문", "번역투 고쳐".
---

# Humanize Korean — AI 한글 티 제거 (단일 호출 자기완결판)

AI가 쓴 한글 텍스트의 "AI 티"를 **한 흐름 안에서** 탐지·윤문·자체검증까지 끝낸다. 별도 에이전트 없이 현재 세션이 룰북을 적재해 메모리에서 처리한다. ([epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai)의 `humanize-korean` v1.5 fast-path 인라인. 라이선스는 끝.)

## 철칙 (위반 시 즉시 롤백)

1. **의미 불변**: 사실·주장·수치·날짜·고유명사·인용문 100% 보존. 문체·리듬·표현만 손댄다.
2. **근거 기반**: `references/quick-rules.md`에 매핑 안 되는 구간은 건드리지 않는다.
3. **장르·register 유지**: 입력 장르·격식체에서 이탈 금지. AI 티는 문법·수사이지 격식 자체가 아니다.
4. **과윤문 금지**: 변경률 30% 초과 = 경고, 50% 초과 = 작업 중단·롤백.
5. **Do-NOT**: 고유명사·제품/모델/기관명, 수치·날짜·단위, 큰따옴표 안 직접 인용, 법률 조문, 수학·화학·통계 표기, 영어 약어(LLM·GPU·MCP·API 등) 원형 보존.

## 작업 흐름 (한 흐름)

먼저 컨텍스트 한 줄을 출력한다: `humanize-korean — 입력 {N}자 / 장르 {추정값} / 강도 {보수|기본|적극}`.

- **입력**: 프롬프트에 붙어 있으면 그대로, 파일 경로면 Read, "이 문단만"이면 그 범위만.
- **장르**: 첫 300자로 칼럼·리포트·블로그·공적 추정(사용자 명시 우선).
- **종료 조건**: 한글이 아니면 "한국어 텍스트만 처리 가능" 후 종료. 8,000자 초과면 "문단 청크로 순차 처리" 1줄 고지 후 청크 단위 진행.

이어서 `references/quick-rules.md`(기본 룰북 — S1·S2 패턴 + 처리 순서 + 자체검증 6항)를 Read해 다음을 수행한다:

1. **탐지** — 카테고리별 어휘·어미·구조·문장길이 통계로 매치를 `(ID, span, severity, fix)`로 보관. Do-NOT span 제외.
2. **윤문** — quick-rules 처리 순서대로 문단 단위 치환. 변경률 모니터링, 50% 임박 시 보류.
3. **자체검증** — quick-rules 6항 점검. 위반 edit 롤백 후 단계 2 부분 재실행(최대 1회). 미해결이면 출력하되 요약에 위반 명시.
4. **출력** — `references/output-contract.md`를 Read해 출력 위치·요약 블록·등급·후속·엣지를 처리(탐지·윤문엔 불필요).

강도 "적극" 또는 모호한 판정이면 `references/rewriting-playbook.md`, 전수 검토면 `references/ai-tell-taxonomy.md`를 추가 Read한다.

## 옵션 (인자 끝에 자연어로)

- `장르: 칼럼|리포트|블로그|공적` (생략 시 자동), `강도: 보수|기본|적극` (기본; "적극"이면 playbook·taxonomy 적재), `최소심각도: S1|S2|S3` (기본 S2).

## 참고 자료

- [`references/quick-rules.md`](references/quick-rules.md) — S1·S2 패턴 + 처리 순서 + 자체검증 (기본 룰북)
- [`references/output-contract.md`](references/output-contract.md) — 출력·요약·등급·후속·엣지
- [`references/ai-tell-taxonomy.md`](references/ai-tell-taxonomy.md) — 10분류 40+ 전수
- [`references/rewriting-playbook.md`](references/rewriting-playbook.md) — 카테고리별 레시피·장르별 허용 표

## 라이선스·귀속

본 스킬(SKILL.md·references)은 [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai)의 `humanize-korean`에서 이식했다. 원본 **MIT** (Copyright (c) 2026 epoko77-ai). planning-kit도 MIT로 배포하며 원 저작권·라이선스 표기를 유지한다.
