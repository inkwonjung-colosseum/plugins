# logistics-kit

물류 도메인(WMS/TMS/OMS/3PL) 상시 전문가 Skills 묶음. 설계 자문·코드 리뷰·운영 질의·규제 검토 등 도메인 전반에서 사용. Claude Code / Codex / Cursor 3개 플랫폼 지원.

- **버전:** `0.1.0`
- **라이선스:** MIT
- **작성자:** inkwonjung-colosseum
- **plugin-eval 점수:** 100/100 (플러그인) + 100/100 × 12 (모든 스킬)

## 포함 Skills

| Skill | 도메인 | 트리거 키워드 |
|---|---|---|
| `wms-inventory` | 창고관리 — 재고/입출고/피킹/패킹/lot/ATP 정합성 | 재고, 피킹, WMS, ATP, putaway |
| `tms-routing` | 운송관리 — 배차/라우팅/운임/권역/할증 | 배차, 운임, TMS, zone, VRP |
| `oms-fulfillment` | 주문/풀필먼트 — 주문 상태기계, SKU 마스터, 3PL 연동, 옴니채널 | 주문, OMS, SKU, 3PL, 옴니채널 |
| `returns-rma` | 반품/RMA — 환불 트리거, 검수 판정, 재입고, 교환 | 반품, RMA, 환불, 검수 |
| `logistics-compliance` | 통관·관세·HS코드·위험물·식약처·개인정보 | 통관, HS코드, 위험물, PCC |
| `cold-chain-monitor` | 콜드체인 — 온도 이력, TTI, 단절 감지, GDP | 콜드체인, 온도, 백신, reefer |
| `logistics-settlement` | 정산 — 차주/3PL 정산, SLA 보상, 분개 매핑 | 정산, SLA, 분개, debit note |
| `logistics-data-model` | ERD — 재고 트랜잭션, SCD, 이벤트 소싱, 감사 로그 | ERD, SCD, 이벤트 소싱, 파티셔닝 |
| `logistics-event-schema` | Kafka topic 명명, Outbox, 버전 호환성 | topic, outbox, CDC, Schema Registry |
| `logistics-idempotency` | API 멱등성, 컨슈머 dedup, 재시도 | 멱등성, Idempotency-Key, retry |
| `logistics-kpi` | OTIF·회전율·리드타임·picking accuracy 산식 | KPI, OTIF, 회전율, 리드타임 |
| `logistics-glossary` | 한/영/일 용어 정규화 (inventory/在庫/재고) | 용어, 용어집, glossary |

## 구조

```text
logistics-kit/
├── .claude-plugin/plugin.json     # Claude Code manifest
├── .codex-plugin/plugin.json      # Codex manifest (interface 포함)
├── README.md
└── skills/
    └── <skill-name>/
        ├── SKILL.md               # 슬림 frontmatter + 짧은 워크플로
        └── references/
            ├── checklist.md       # 활용 시점 + 도메인 점검 포인트 + 응답 형식
            ├── glossary.md        # (logistics-glossary) 표준 용어집
            └── formulas.md        # (logistics-kpi) 표준 KPI 산식
```

> 각 `SKILL.md`는 description에 `Use when [도메인 키워드] 설계/리뷰/운영` 패턴(한국어 키워드 우선)을 둔다. 본문은 6 라인 이하로 슬림하게 유지하고, 실제 점검 포인트·표준표는 `references/`에 위치(평가 시 deferred bucket으로 분류되어 token budget 절약).

## 활용 시나리오

- **설계 자문** — "재고 차감 시점 정책 어떻게 잡을까", "이벤트 envelope 표준 뭐 써야 해" 같은 도메인 설계 질문.
- **코드·스키마 리뷰** — PR diff·마이그레이션·API 변경에 대한 도메인 정합성 검토.
- **운영·디버깅** — 음수 재고, 이중 차감, 정산 차이, 콜드체인 일탈 알림 같은 인시던트 분석.
- **규제·감사 검토** — 통관·HS코드·식약처·개인정보·GDP 규정 적용 자문.
- **신규 멤버 온보딩** — 물류 도메인 용어·산식·표준 패턴 학습 (`logistics-glossary`, `logistics-kpi`).

## 사용

### Claude Code

```bash
claude plugin marketplace add https://github.com/inkwonjung-colosseum/plugins
claude plugin install logistics-kit@inkwonjung-colosseum
```

slash command:

```text
/logistics-kit:wms-inventory
/logistics-kit:tms-routing
/logistics-kit:oms-fulfillment
... (12개 전부)
```

### Codex

skill invocation:

```text
$wms-inventory
$tms-routing
$oms-fulfillment
...
```

### Cursor

Cursor Agent chat 내부에서:

```text
/add-plugin logistics-kit
```

## Skill 간 hand-off

스킬은 도메인별로 분리되어 있으며, 다른 도메인 검토가 필요할 때 cross-reference한다.

```text
wms-inventory ──┬─► tms-routing (배차/운임)
                ├─► returns-rma (반품 흐름)
                ├─► logistics-data-model (ERD)
                └─► logistics-idempotency (재고 차감 멱등성)

tms-routing ────┬─► logistics-settlement (운임 정산/분개)
                ├─► logistics-compliance (통관/HS)
                └─► logistics-kpi (OTIF/적재율)

oms-fulfillment ─┬─► wms-inventory
                 ├─► returns-rma
                 ├─► tms-routing
                 └─► logistics-idempotency (출고 지시 멱등성)

logistics-event-schema ──► logistics-idempotency (at-least-once)
logistics-data-model   ──► logistics-event-schema (event sourcing)
logistics-kpi          ──► logistics-settlement (보상금)
                        └─► localization-audit (타임존)
```

## 평가 점수

```text
$ plugin-eval analyze ./logistics-kit --format markdown
Score: 100/100
Grade: A
Risk: low
Checks: 0 fail, 0 warn, 0 info
Active budget: 1801 tokens (moderate)
Trigger cost: 179 tokens (moderate)
```

개별 Skill도 전부 100/100 (`plugin-eval analyze ./skills/<skill> --format json`).

## 확장

신규 Skill 추가 시:

1. `skills/<new-skill>/SKILL.md` — frontmatter description에 `Use when [도메인 키워드] 설계/리뷰/운영` 패턴 포함 (30~60자, trigger 토큰 절약).
2. `skills/<new-skill>/references/checklist.md` — 자동 트리거·체크리스트·출력 형식.
3. 본 README의 표·hand-off 다이어그램 갱신.
4. `plugin-eval analyze ./logistics-kit --format markdown` 으로 100/100 유지 확인.
5. 루트 카탈로그(`.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`, `.cursor-plugin/marketplace.json`)는 plugin 전체 entry만 관리하므로 신규 Skill만 추가 시 수정 불필요.
