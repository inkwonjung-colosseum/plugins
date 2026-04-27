# logistics-expert-kit

`logistics-expert-kit`은 Claude Code와 Codex에서 쓰는 범용 물류 전문가 플러그인입니다. 창고, 운송, 재고, 풀필먼트, 반품, 지표, 운영 리스크를 일반 물류 원칙으로 구조화하고, 사용자가 제공한 정보와 가정을 분리해 대화형 조언을 제공합니다.

## 원칙

- **범용 물류 지식**: 특정 회사나 시스템 설정을 전제로 하지 않습니다.
- **근거 구분**: 확인된 근거, 일반 물류 원칙, 가정, 회사별 확인 필요를 분리합니다.
- **검토 게이트**: 법규, 통관, 계약, 요율, SLA, 귀책, 패널티는 최종 판단하지 않습니다.
- **대화형 조언**: v0.1은 로컬 파일 생성, Confluence/Jira 반영, 실시간 운임/API 조회를 포함하지 않습니다.

## 스킬

| 스킬 | 목적 | 예시 |
|---|---|---|
| `logistics-scope` | 물류 이슈 범위, 관련 흐름, 필요한 데이터, 다음 분석 방향 정리 | `$logistics-scope 출고 지연 원인을 보고 싶어` |
| `logistics-diagnose` | 지연, 오출고, 재고 차이, 품절, 운임 증가, 반품 증가 원인 후보와 확인 순서 제시 | `$logistics-diagnose 최근 반품률이 늘었어` |
| `logistics-metrics` | KPI 정의, 계산식 후보, 해석 기준, 지표 간 tradeoff 정리 | `$logistics-metrics OTIF랑 fill rate 차이 설명해줘` |
| `logistics-risk` | 정책, 프로세스, 시스템 변경안의 운영 리스크와 검토 게이트 제시 | `$logistics-risk 당일 출고 cutoff를 늦추려 해` |

## 사용 예

Claude Code:

```text
/logistics-expert-kit:logistics-scope 출고 지연이 자주 발생해
/logistics-expert-kit:logistics-diagnose 재고 차이가 커졌어
/logistics-expert-kit:logistics-metrics OTIF 지표 설계해줘
/logistics-expert-kit:logistics-risk 위험물 해외배송 프로세스 바꾸려 해
```

Codex:

```text
$logistics-scope 출고 지연이 자주 발생해
$logistics-diagnose 재고 차이가 커졌어
$logistics-metrics OTIF 지표 설계해줘
$logistics-risk 위험물 해외배송 프로세스 바꾸려 해
```

## 포함 범위

- 창고 운영: 입고, 적치, 보충, 피킹, 패킹, 출고, 재고실사
- 운송: 운송 모드, carrier, lead time, cutoff, 배송 상태, 비용 구조
- 재고: 안전재고, 재주문점, 품절, 과재고, allocation, cycle count
- 풀필먼트와 반품: 주문 생애주기, split shipment, backorder, RMA, 회수, 검수
- 국제운송/무역/통관 질문 구조화: origin/destination, Incoterms, HS code, 위험물, 통관 서류, specialist gate
- 지표: OTIF, fill rate, lead time, picking accuracy, inventory accuracy, cost/order
- 리스크: 병목, 예외 처리, 데이터 정합성, 고객 영향, 전문 검토 필요 조건

## 비범위

- 특정 회사의 정책, 계약, 요율, SLA 확정
- 국가별 법규, 통관, 위험물, 제재, HS code 최종 판단
- 실시간 운임 조회, carrier API 호출, route optimization, demand forecasting
- WMS/TMS/OMS/ERP 상세 구현 설계
- Confluence/Jira 자동 반영 또는 로컬 문서 파일 생성

## 구성

- `.claude-plugin/plugin.json` — Claude Code 플러그인 매니페스트
- `.codex-plugin/plugin.json` — Codex 플러그인 매니페스트
- `skills/` — 4개 대화형 물류 스킬
- `references/` — 공통 물류 판단 기준과 안전 경계
- `templates/` — 스킬별 권장 출력 형식
- `docs/` — privacy policy와 terms of service
- `tests/` — 구조 회귀 테스트

## 설치

### Claude Code

```bash
claude plugin marketplace add https://github.com/inkwonjung-colosseum/plugins
claude plugin install logistics-expert-kit@inkwonjung-colosseum
```

### Codex

```bash
codex marketplace add https://github.com/inkwonjung-colosseum/plugins
```

marketplace 추가 후 Codex 앱의 `/plugins`에서 `logistics-expert-kit`을 설치/활성화합니다.

## 검증

```bash
python3 -m unittest logistics-expert-kit/tests/test_structure.py
claude plugin validate ./logistics-expert-kit
```
