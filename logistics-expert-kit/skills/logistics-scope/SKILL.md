---
name: logistics-scope
description: "Frame a logistics issue by domain, flow, systems, available data, missing evidence, and the next analysis path."
argument-hint: "<물류 이슈 또는 질문>"
---

# logistics-scope

물류 이슈를 바로 해결하려고 하지 않고, 먼저 범위와 필요한 근거를 정리하는 intake 스킬입니다.

## 호출

- Claude Code: `/logistics-expert-kit:logistics-scope <물류 이슈>`
- Codex: `$logistics-scope <물류 이슈>`

## 참조

먼저 `../../references/evidence-and-limits.md`와 `../../references/logistics-domain-map.md`를 읽습니다. 창고, 운송, 재고, 풀필먼트, 반품 중 특정 흐름이 보이면 해당 reference도 읽습니다. HS code, Incoterms, customs, import/export, dangerous goods, sanctions가 나오면 `../../references/cross-border-trade-and-customs.md`를 읽습니다.

## 동작 순서

1. 사용자 입력에서 증상, 대상 흐름, 관련 시스템, 의사결정 목적을 분리합니다.
2. 창고, 운송, 재고, 풀필먼트, 반품, cross-border/trade/customs, 지표, 리스크 중 관련 영역을 표시합니다.
3. 제공된 정보와 없는 정보를 나눕니다.
4. 다음에 쓸 스킬이 `logistics-diagnose`, `logistics-metrics`, `logistics-risk` 중 무엇인지 추천합니다.

## 출력 형식

`../../templates/scope-brief.md`의 형식을 따릅니다. 반드시 아래 항목을 구분합니다.

- 확인된 근거
- 일반 물류 원칙
- 가정
- 회사별 확인 필요

## 제한

이 결과는 문제 범위 정의이며 운영 정책, 계약, 통관, 법규, 요율, SLA 판단이 아닙니다. 국가, 운송 모드, 화물 특성, 계약 조건, 고객 약속이 빠지면 `scope-incomplete`로 표시합니다.
