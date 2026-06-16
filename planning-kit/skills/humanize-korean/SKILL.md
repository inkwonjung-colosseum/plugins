---
name: humanize-korean
description: Use when AI(ChatGPT·Claude·Gemini)가 쓴 한글 텍스트를 사람이 쓴 글처럼 윤문할 때. 번역투·기계적 병렬·피동/접속사 남발·이모지/불릿 과다 등 10대 카테고리 40+ AI 티 패턴을 탐지해 내용은 그대로 두고 문체·리듬만 재작성한다. 트리거 — "AI 티 없애줘", "AI 윤문", "ChatGPT 문체", "번역투 고쳐", "humanize Korean". 기획 초안(정책서·기능설계서) 윤문에도 사용.
---

# Humanize Korean — AI 한글 티 제거 (단일 호출 자기완결판)

AI가 쓴 한글 텍스트의 "AI 티"를 **한 번의 작업 흐름 안에서** 탐지·윤문·자체검증까지 끝낸다. 별도 에이전트를 호출하지 않고, 이 SKILL.md를 읽은 현재 세션이 직접 룰북을 적재해 메모리 안에서 처리한다. ([epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai)의 `humanize-korean` v1.5 fast-path를 단일 자기완결 스킬로 인라인. 라이선스는 문서 끝.)

## 철칙 (Prime Directives — 위반 시 즉시 롤백)

1. **의미 불변**: 사실·주장·수치·날짜·고유명사·인용문은 원문과 100% 일치. 윤문은 문체·리듬·표현만 손댄다.
2. **근거 기반**: `references/quick-rules.md`에 매핑되지 않는 구간은 건드리지 않는다.
3. **장르 유지**: 입력 장르(칼럼·리포트·블로그·공적)에서 이탈 금지.
4. **register 보존**: 원문 격식체면 결과도 격식체. AI 티는 문법·수사이지 격식 자체가 아니다.
5. **과윤문 금지**: 변경률 30% 초과 = 경고, 50% 초과 = 작업 중단·롤백.
6. **Do-NOT list**: 고유명사·제품명·모델명·기관명, 수치·날짜·단위, 큰따옴표 안 직접 인용, 법률 조문, 수학·화학·통계 표기, 영어 약어(LLM·GPU·MCP·API 등) 원형 보존.

## Phase 0: 컨텍스트 확인

작업 시작 시 다음 한 줄을 먼저 출력한다.

```
humanize-korean — 입력 {N}자 / 장르 {추정값} / 강도 {보수|기본|적극}
```

- **입력 수집**: 텍스트가 프롬프트에 붙어 있으면 그대로 사용. 파일 경로면 Read. "이 문단만"이면 해당 범위만.
- **장르 추정**: 첫 300자로 칼럼·리포트·블로그·공적 중 추정(사용자 명시 시 우선).
- **8,000자 초과**: "장문은 문단 청크로 나눠 순차 처리" 1줄 고지 후 청크 단위로 진행.
- **한글이 아니면**: "한국어 텍스트만 처리 가능" 반환 후 종료.

## 작업 순서 (한 흐름 안에서)

### 단계 1: 룰북 적재
- `references/quick-rules.md`(S1·S2 핵심 + 자체검증 6항)를 Read해 룰 표를 내재화한다. **이것이 기본 룰북.**
- 풍부한 처방·장르별 허용 표가 필요하면 `references/rewriting-playbook.md`, 전수 패턴 분류가 필요하면 `references/ai-tell-taxonomy.md`를 추가 Read한다(강도 "적극" 또는 모호한 판정 시).

### 단계 2: 패턴 탐지 (메모리)
- A·D·H·I·J 카테고리: 어휘·어미 키워드 매칭
- C 카테고리: 문서 구조(헤딩·따옴표·불릿·연결어미 뒤 쉼표) 통계
- E 카테고리: 문장 길이 stdev
- 각 매치를 `(ID, span, severity, suggested_fix)`로 보관
- Do-NOT list 엄격 적용: 고유명사·수치·인용 span 제외

### 단계 3: 윤문 (메모리)
- 처리 순서: **D(관용구 삭제) → A → I → G → H → F → B → C·J → E**. (D를 먼저 하면 문장이 짧아져 후속 작업이 쉬워진다.)
- 문단 단위로 처리. 각 edit의 before/after를 누적.
- 변경률을 모니터링하고 50% 임박 시 후속 edit을 보류한다.

### 단계 4: 자체검증 (메모리)
`quick-rules.md`의 "자체검증 체크리스트" 6항을 점검한다.
1. 고유명사·수치·날짜·인용 100% 보존
2. 변경률 30% 이하 (50% 초과는 중단)
3. 장르 이탈 없음
4. register 보존
5. 잔존 S1 패턴 0건 (D-1~D-7, A-7, A-8, A-16, C-5, C-10, C-11, H-1, I-1, J-2)
6. 인공 표현 자제 (원문에 없던 비유·수사 임의 추가 금지)

위반 항목 발견 시 해당 edit 롤백 → 단계 3 부분 재실행 (**최대 1회**). 미해결이면 결과를 출력하되 요약에 위반 항목을 명시한다.

### 단계 5: 출력
`references/output-contract.md`를 Read해 출력 위치·요약 블록(HUMANIZE-SUMMARY)·응답 형식·등급 기준·후속 명령·엣지 케이스를 처리한다. 탐지·윤문(단계 2–3)에는 필요 없다.

## 옵션 (인자 끝에 자연어로)

- `장르: 칼럼|리포트|블로그|공적` — 생략 시 자동 추정
- `강도: 보수|기본|적극` — 기본값 "기본". "적극"이면 playbook·taxonomy까지 적재
- `최소심각도: S1|S2|S3` — 탐지 임계값, 기본값 S2

## 참고 자료

- [`references/quick-rules.md`](references/quick-rules.md) — S1·S2 핵심 패턴 + 자체검증 체크리스트 (기본 룰북, 단계 1에서 항상 적재)
- [`references/output-contract.md`](references/output-contract.md) — 출력 위치·요약 포맷·등급·후속·엣지 (단계 5에서 적재)
- [`references/ai-tell-taxonomy.md`](references/ai-tell-taxonomy.md) — 10대 분류 × 40+ 패턴 전수 (모호 판정·전수 검토 시)
- [`references/rewriting-playbook.md`](references/rewriting-playbook.md) — 카테고리별 치환 레시피·장르별 허용 표 (강도 적극 시)

## 라이선스·귀속

본 스킬(SKILL.md·references)은 [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai)의 `humanize-korean`에서 이식했다. 원본 라이선스 **MIT** (Copyright (c) 2026 epoko77-ai). planning-kit도 MIT로 배포되며, 원 저작권·라이선스 표기를 유지한다.
