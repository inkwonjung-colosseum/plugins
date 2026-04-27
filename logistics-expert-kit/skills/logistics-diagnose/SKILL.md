---
name: logistics-diagnose
description: "Diagnose logistics symptoms such as delay, mis-ship, inventory mismatch, stockout, cost increase, or returns increase."
argument-hint: "<증상 또는 문제 상황>"
---

# logistics-diagnose

물류 증상을 원인 후보, 확인 데이터, 확인 순서, 개선 방향 후보로 나누는 스킬입니다.

## 호출

- Claude Code: `/logistics-expert-kit:logistics-diagnose <증상>`
- Codex: `$logistics-diagnose <증상>`

## 참조

먼저 `../../references/evidence-and-limits.md`와 `../../references/logistics-domain-map.md`를 읽습니다. 증상에 따라 `warehouse-operations.md`, `transportation.md`, `inventory.md`, `fulfillment-and-returns.md`를 선택해 읽습니다. 통관 지연, 수출입 서류, HS code, Incoterms, 위험물, 제재 관련 증상이 있으면 `../../references/cross-border-trade-and-customs.md`도 읽습니다.

## 동작 순서

1. 증상을 창고, 운송, 재고, 풀필먼트, 반품 중 어디에서 발생했는지 분류합니다.
2. 단일 원인을 확정하지 않고 3-5개의 원인 후보를 우선순위로 제시합니다.
3. 각 원인 후보마다 확인할 데이터와 확인 순서를 붙입니다.
4. 귀책, 손해, 계약 위반, 보험, 통관 이슈가 나오면 `human-review-required`로 표시합니다.

## 출력 형식

`../../templates/diagnosis.md`의 형식을 따릅니다. 반드시 아래 항목을 구분합니다.

- 확인된 근거
- 일반 물류 원칙
- 가정
- 회사별 확인 필요

## 제한

원인 후보와 확인 절차를 제시할 뿐 귀책, 손해, 계약 위반, 패널티 여부를 확정하지 않습니다. 제공된 근거가 부족하면 결론보다 확인 순서를 우선합니다.
