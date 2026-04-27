---
name: logistics-metrics
description: "Design and explain logistics KPIs, candidate formulas, interpretation rules, and metric tradeoffs."
argument-hint: "<지표 질문 또는 측정하려는 목표>"
---

# logistics-metrics

물류 KPI를 정의하고 계산식 후보, 해석 기준, tradeoff, 운영 적용 전 확인사항을 정리하는 스킬입니다.

## 호출

- Claude Code: `/logistics-expert-kit:logistics-metrics <지표 질문>`
- Codex: `$logistics-metrics <지표 질문>`

## 참조

먼저 `../../references/evidence-and-limits.md`, `../../references/logistics-domain-map.md`, `../../references/inventory.md`, `../../references/transportation.md`를 읽습니다. 풀필먼트나 반품 지표라면 `../../references/fulfillment-and-returns.md`도 읽습니다.

## 동작 순서

1. 사용자가 측정하려는 목표를 서비스, 속도, 비용, 생산성, 품질, 재고 건전성 중 하나 이상으로 분류합니다.
2. 지표별 계산식 후보를 제시하고 분모, 분자, 측정 시점, 제외 조건을 설명합니다.
3. 지표 간 tradeoff를 드러냅니다. 예: lead time 단축과 cost/order 증가, fill rate 개선과 overstock 증가.
4. 정산, 성과평가, vendor 평가에 쓰일 수 있으면 `policy-owner-review`로 표시합니다.

## 출력 형식

`../../templates/metrics-guide.md`의 형식을 따릅니다. 반드시 아래 항목을 구분합니다.

- 확인된 근거
- 일반 물류 원칙
- 가정
- 회사별 확인 필요

## 제한

지표 정의 후보를 제공할 뿐 회사의 공식 KPI, 정산 기준, 성과평가 기준을 대체하지 않습니다. 공식 적용 전에는 데이터 owner와 정책 owner 확인이 필요합니다.
