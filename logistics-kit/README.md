# logistics-kit

물류 도메인 전반 — WMS/TMS/OMS/3PL 운영, 공급망 계획(SCP), 규제·콜드체인·위험물, 플랫폼·데이터 엔지니어링 — 4계층 상시 전문가 Skills 묶음. 설계 자문·코드 리뷰·운영 질의·규제 검토 등 도메인 전반에서 사용. Claude Code / Codex / Cursor 3개 플랫폼 지원.

- **버전:** `0.2.0`
- **라이선스:** MIT
- **작성자:** inkwonjung-colosseum
- **총 Skill 수:** 50 (운영 8 + WMS/OMS 코어 4 + 운송 6 + 계획 5 + 규제 11 + 플랫폼·데이터 11 + 횡단 5)

## 도메인 계층

| 계층 | 범위 | 대표 Skills |
|---|---|---|
| 운영 (operations) | WMS·재고·피킹·창고 자동화·야드·정확도·노동·안전 | `wms-inventory`, `slotting-putaway`, `wave-pick-strategy`, `wcs-mhe`, `yard-dock`, `inventory-accuracy`, `labor-mgmt`, `cross-dock-kitting`, `warehouse-safety` |
| 주문·반품 | OMS·풀필먼트·반품·RMA | `oms-fulfillment`, `returns-rma` |
| 운송 (transportation) | TMS·VRP·rating·EDI·라스트마일·추적·국제 운송 | `tms-routing`, `vrp-rating-engine`, `carrier-edi`, `last-mile-delivery`, `track-trace`, `freight-forwarding` |
| 공급망 계획 (SCP) | 수요예측·재고 최적화·S&OP·발주·네트워크 | `demand-forecast`, `inventory-planning`, `sop-ibp`, `procurement-po`, `network-design` |
| 규제·콜드체인·위험물 | 통관·HS·FTA·DGR·sanctions·GDP·HACCP·회수·CoC·claims·ESG·PII | `logistics-compliance`, `dangerous-goods`, `trade-sanctions`, `pharma-gdp-serialization`, `haccp-food-safety`, `recall-traceability`, `chain-of-custody`, `cargo-claims-insurance`, `sustainability-carbon`, `fta-origin`, `data-privacy-logistics`, `cold-chain-monitor` |
| 정산·KPI·용어 | 정산·회계·KPI·용어집 | `logistics-settlement`, `logistics-kpi`, `logistics-glossary` |
| 플랫폼·데이터 | 이벤트·멱등성·ERD·saga·관측성·테넌시·채널·DR·bulk·locale·MDM·resilience·API | `logistics-event-schema`, `logistics-idempotency`, `logistics-data-model`, `logistics-saga`, `logistics-observability`, `logistics-multitenancy`, `channel-sync`, `logistics-dr`, `bulk-operations`, `localization-audit`, `mdm-reference-data`, `resilience-patterns`, `api-design-logistics` |

## 전체 Skill 목록

### 운영 (8)

| Skill | 도메인 | 트리거 키워드 |
|---|---|---|
| `wms-inventory` | WMS 재고·차감·ATP·lot·예약 vs 가용 | 재고, 피킹, WMS, ATP, putaway |
| `slotting-putaway` | 슬로팅·putaway·replenishment·ABC/golden zone | 슬로팅, ABC, golden zone, replenishment |
| `wave-pick-strategy` | wave/batch/cluster·pick path·voice/RF/PTL | wave, batch pick, voice, pick path |
| `wcs-mhe` | WCS·AGV/AMR·컨베이어·소터·AS-RS·MES | WCS, AGV, AMR, 컨베이어, 소터 |
| `yard-dock` | YMS·도크 어포인트먼트·gate·detention | 도크, YMS, detention, gate |
| `inventory-accuracy` | IRA·cycle count·blind count·shrinkage | IRA, cycle count, shrinkage |
| `labor-mgmt` | LMS·UPH·engineered standard·shift·인센티브 | UPH, engineered standard, LMS |
| `cross-dock-kitting` | cross-dock·flow-through·kit BOM·VAS | cross-dock, kit, VAS |
| `warehouse-safety` | 창고 안전·PIT·LOTO·near-miss·OSHA/KOSHA | 안전, LOTO, PIT, near-miss |

### 주문·반품 (2)

| Skill | 도메인 | 트리거 키워드 |
|---|---|---|
| `oms-fulfillment` | OMS·주문 상태기계·SKU·옴니채널·3PL | 주문, OMS, SKU, 3PL, 옴니채널 |
| `returns-rma` | 반품·RMA·검수·재입고·교환·역물류 | 반품, RMA, 환불, 검수 |

### 운송 (6)

| Skill | 도메인 | 트리거 키워드 |
|---|---|---|
| `tms-routing` | TMS·배차·라우팅·운임·권역·할증 | 배차, 운임, TMS, zone, VRP |
| `vrp-rating-engine` | VRP 변형·solver·dim weight·accessorial·fuel index | VRPTW, OR-Tools, dim weight, accessorial |
| `carrier-edi` | EDI 204/214/990/210/856·AS2/SFTP·라벨·webhook | EDI, ZPL, webhook, AS2 |
| `last-mile-delivery` | 시간대 슬롯·POD·재시도·locker·COD·새벽배송 | 라스트마일, POD, 슬롯, locker |
| `track-trace` | milestone·multi-carrier status 정규화·ETA·알림 | 추적, ETA, milestone |
| `freight-forwarding` | 해상·항공·FCL/LCL·AWB·B/L·ISF/AMS | 해상, 항공, AWB, B/L, FCL |

### 공급망 계획 (5)

| Skill | 도메인 | 트리거 키워드 |
|---|---|---|
| `demand-forecast` | 수요예측·Croston/Holt-Winters/ARIMA·MAPE/WMAPE/FVA | 수요예측, MAPE, Croston, FVA |
| `inventory-planning` | 안전재고·ROP·EOQ·(s,S)·ABC-XYZ·MEIO | 안전재고, ROP, EOQ, MEIO |
| `sop-ibp` | S&OP·IBP·월간 cadence·consensus·scenario | S&OP, IBP, consensus, scenario |
| `procurement-po` | PO·ASN·3-way match·supplier scorecard·dual sourcing | PO, ASN, 3-way match, MOQ |
| `network-design` | facility location·sourcing·postponement·DRP·modal mix | 네트워크 설계, p-median, postponement |

### 규제·콜드체인·위험물 (12)

| Skill | 도메인 | 트리거 키워드 |
|---|---|---|
| `logistics-compliance` | 통관·HS·Incoterms·식약처·KC·PCC·개인정보 | 통관, HS코드, PCC |
| `dangerous-goods` | UN·class·PG·IMDG/IATA/ADR·리튬·LQ/EQ·segregation | 위험물, UN, IATA DGR, 리튬 |
| `trade-sanctions` | OFAC SDN·EU·UN·전략물자·EAR/ITAR·denied party | OFAC, 전략물자, EAR, ITAR |
| `pharma-gdp-serialization` | GDP·IQ/OQ/PQ·MKT·excursion·DSCSA/EU FMD/KIMS-K | GDP, MKT, IQ/OQ/PQ, DSCSA |
| `haccp-food-safety` | HACCP·CCP·allergen·원산지·halal/kosher·소비기한 | HACCP, CCP, allergen, 원산지 |
| `recall-traceability` | 회수·mock recall·one-up-one-down·lot genealogy·class I/II/III | 회수, mock recall, lot genealogy |
| `chain-of-custody` | 봉인·controlled substance·주류·담배·마약류·고가품 | 봉인, controlled substance, 주류 |
| `cargo-claims-insurance` | COGSA/CMR/Hague-Visby/Montreal·subrogation·time bar | cargo claim, COGSA, CMR, 보험 |
| `sustainability-carbon` | GLEC·tkm·Scope 3·CBAM·EU ETS·회수 포장 | 탄소, GLEC, CBAM, Scope 3 |
| `fta-origin` | KORUS/RCEP/USMCA·RVC/CTC/de-minimis·C/O | FTA, KORUS, RCEP, RVC, CTC |
| `data-privacy-logistics` | PIPA/GDPR·수하인 PII·SCC·DSR·마스킹 | PIPA, GDPR, PII, DSR |
| `cold-chain-monitor` | 콜드체인·온도 이력·TTI·MKT·reefer·excursion | 콜드체인, 온도 일탈, reefer |

### 정산·KPI·용어 (3)

| Skill | 도메인 | 트리거 키워드 |
|---|---|---|
| `logistics-settlement` | 차주·3PL·SLA·debit/credit note·CBAM levy·channel 수수료 | 정산, SLA, 분개, 3PL contract |
| `logistics-kpi` | OTIF·fill rate·UPH·MAPE·SLO·SLA·KPI 산식 단일 소스 | KPI, OTIF, 회전율, 리드타임 |
| `logistics-glossary` | 한/영/일 용어·코드 식별자·API 필드 통일 | 용어, glossary, 번역 |

### 플랫폼·데이터 (11)

| Skill | 도메인 | 트리거 키워드 |
|---|---|---|
| `logistics-data-model` | ERD·SCD·이벤트 소싱·tenant_id·snapshot·CDC | ERD, SCD, 이벤트 소싱 |
| `logistics-event-schema` | topic·envelope·outbox·Schema Registry·DLQ·replay | topic, outbox, CDC, schema registry |
| `logistics-idempotency` | API 멱등성·dedup·exactly-once·reconciliation | 멱등성, retry, dedup |
| `logistics-saga` | orchestration·choreography·TCC·보상·state machine | saga, TCC, 보상 트랜잭션 |
| `logistics-observability` | SLO/SLI/error budget·trace·structured log·alert | SLO, trace, alert, error budget |
| `logistics-multitenancy` | 3PL·marketplace tenant 격리·RLS·quota·noisy neighbor | 테넌시, RLS, quota |
| `channel-sync` | Shopify·Amazon·Coupang·네이버·oversell guard·rate-limit | 옴니채널, channel, oversell |
| `logistics-dr` | RPO/RTO·snapshot·region failover·event replay | RPO, RTO, DR, failover |
| `bulk-operations` | bulk/mass·chunking·throttling·partial failure·progress | bulk, mass, CSV import |
| `localization-audit` | 타임존·KST cutoff·통화·환율·단위·휴일·i18n | KST cutoff, 환율, 휴일 |
| `mdm-reference-data` | tariff·zone·HS·calendar·effective date·supersession | MDM, 운임표, effective date |
| `resilience-patterns` | circuit breaker·bulkhead·timeout·hedged·retry budget | circuit breaker, bulkhead, retry |
| `api-design-logistics` | REST/gRPC/GraphQL·async·webhook·pagination·HMAC | API, webhook, HMAC, pagination |

## 구조

```text
logistics-kit/
├── .claude-plugin/plugin.json     # Claude Code manifest
├── .codex-plugin/plugin.json      # Codex manifest (interface 포함)
├── .cursor-plugin/plugin.json     # Cursor manifest
├── README.md
├── BACKLOG.md
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

- **설계 자문** — "재고 차감 시점 정책 어떻게 잡을까", "VRPTW solver 어떤 게 좋아", "saga 보상 흐름 짤 때" 같은 도메인 설계 질문.
- **코드·스키마 리뷰** — PR diff·마이그레이션·API 변경에 대한 도메인 정합성·통합·플랫폼 정합성 검토.
- **운영·디버깅** — 음수 재고, 이중 차감, oversell, 정산 차이, 콜드체인 일탈, retry-storm 같은 인시던트 분석.
- **규제·감사 검토** — 통관·HS·식약처·GDP·DGR·sanctions·PIPA/GDPR·CBAM 등 규정 적용 자문.
- **계획·전략** — 수요예측 모델 선택, 안전재고·ROP·EOQ, S&OP cadence, 네트워크 재설계.
- **신규 멤버 온보딩** — 물류 도메인 용어·산식·표준 패턴 학습 (`logistics-glossary`, `logistics-kpi`, `localization-audit`).

## 사용

### Claude Code

```bash
claude plugin marketplace add https://github.com/inkwonjung-colosseum/plugins
claude plugin install logistics-kit@inkwonjung-colosseum
```

slash command:

```text
/logistics-kit:wms-inventory
/logistics-kit:slotting-putaway
/logistics-kit:demand-forecast
/logistics-kit:dangerous-goods
/logistics-kit:logistics-saga
... (50개 전부)
```

### Codex

skill invocation:

```text
$wms-inventory
$slotting-putaway
$demand-forecast
$dangerous-goods
$logistics-saga
...
```

### Cursor

Cursor Agent chat 내부에서:

```text
/add-plugin logistics-kit
```

## Skill 간 hand-off (요약)

운영·계획·운송·규제·플랫폼 4 계층 간 횡단 hand-off 표준화.

```text
[계획]                    [운영]                       [운송]
demand-forecast ─────► inventory-planning ─────► wms-inventory ─────► oms-fulfillment ─────► tms-routing
                                │                       │                                       │
                                ▼                       ▼                                       ▼
                          procurement-po          slotting-putaway                       vrp-rating-engine
                                │                  wave-pick-strategy                          │
                                ▼                  wcs-mhe                                    ▼
                          freight-forwarding       yard-dock                          carrier-edi · last-mile-delivery
                                                   inventory-accuracy
                                                   labor-mgmt
                                                   cross-dock-kitting
                                                   warehouse-safety

[규제]                                            [플랫폼·데이터]
logistics-compliance ─┬─► fta-origin              logistics-event-schema ──► logistics-saga
                      ├─► trade-sanctions          logistics-idempotency  ──► resilience-patterns
                      ├─► dangerous-goods          logistics-data-model   ──► logistics-multitenancy
                      ├─► pharma-gdp-serialization channel-sync           ──► api-design-logistics
                      ├─► cold-chain-monitor       logistics-observability──► logistics-dr
                      ├─► haccp-food-safety        bulk-operations
                      ├─► recall-traceability      mdm-reference-data
                      ├─► chain-of-custody         localization-audit
                      ├─► cargo-claims-insurance
                      ├─► sustainability-carbon
                      └─► data-privacy-logistics

[횡단]
logistics-kpi ──┬─► logistics-settlement
                ├─► logistics-observability
                └─► localization-audit

logistics-glossary ── 모든 skill
```

## 확장

신규 Skill 추가 시:

1. `skills/<new-skill>/SKILL.md` — frontmatter description에 `Use when [도메인 키워드] 설계/리뷰/운영` 패턴 포함 (30~60자, trigger 토큰 절약).
2. `skills/<new-skill>/references/checklist.md` — 자동 트리거·체크리스트·출력 형식.
3. 본 README의 표·hand-off 다이어그램 갱신.
4. `plugin-eval analyze ./logistics-kit --format markdown` 으로 점수 유지 확인.
5. 루트 카탈로그(`.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`, `.cursor-plugin/marketplace.json`)는 plugin 전체 entry만 관리하므로 신규 Skill만 추가 시 수정 불필요.
