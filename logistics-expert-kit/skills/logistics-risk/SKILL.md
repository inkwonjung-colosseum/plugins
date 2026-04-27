---
name: logistics-risk
description: "Review operational risk in logistics policy, process, system, cutoff, SLA, or exception-handling changes."
argument-hint: "<변경안 또는 검토할 정책>"
---

# logistics-risk

물류 정책, 프로세스, 시스템 변경안의 운영 리스크와 전문 검토 게이트를 점검하는 스킬입니다.

## 호출

- Claude Code: `/logistics-expert-kit:logistics-risk <변경안>`
- Codex: `$logistics-risk <변경안>`

## 참조

먼저 `../../references/evidence-and-limits.md`와 `../../references/logistics-domain-map.md`를 읽습니다. 변경안의 흐름에 따라 창고, 운송, 재고, 풀필먼트, 반품 reference를 선택해 읽습니다. HS code, Incoterms, customs, import/export, dangerous goods, sanctions가 나오면 `../../references/cross-border-trade-and-customs.md`를 읽습니다.

## 동작 순서

1. 변경안이 영향을 주는 흐름, 시스템, 이해관계자, 고객 약속을 분리합니다.
2. 운영 리스크, 고객 영향, 비용 영향, 데이터 정합성, 예외 처리 누락을 점검합니다.
3. 법규, HS code, 제재, 위험물, Incoterms, SLA, 배상 조항, 계약 책임이 포함되면 `specialist-review-blocking`으로 표시합니다.
4. 결론은 "적용 가능"이 아니라 "검토 결과와 남은 게이트" 중심으로 작성합니다.

## 출력 형식

`../../templates/risk-review.md`의 형식을 따릅니다. 반드시 아래 항목을 구분합니다.

- 확인된 근거
- 일반 물류 원칙
- 가정
- 회사별 확인 필요

## 제한

리스크 식별과 검토 범위를 제공할 뿐 법률, 통관, 계약, 요율, SLA, 안전 관련 최종 의견을 내지 않습니다. blocking 게이트가 있으면 실행 권고보다 검토 필요성을 먼저 표시합니다.
