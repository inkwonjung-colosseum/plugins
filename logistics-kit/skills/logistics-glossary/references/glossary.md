# 표준 용어집

## 기본 운영

| 한국어 | 영어 | 일본어 | 비고 |
|---|---|---|---|
| 재고 | inventory (NOT stock) | 在庫 | stock은 주식 의미 회피 |
| 입고 | inbound / receiving | 入荷 | put-away는 *적치* |
| 출고 | outbound / shipping | 出荷 | shipment은 *건* 단위 |
| 피킹 | picking | ピッキング | |
| 패킹 | packing | 梱包 | |
| 적치 | put-away | 棚入れ | |
| 권역 | zone | 地域 | region과 구분 |
| 운임 | freight (NOT shipping fee) | 運賃 | 부대비용 제외 |
| 차주 | carrier driver | 運転手 | |
| 화주 | shipper | 荷主 | |
| 수하인 | consignee | 荷受人 | |
| 송하인 | shipper / consignor | 差出人 | |
| 안전재고 | safety stock | 安全在庫 | |
| 재주문점 | reorder point (ROP) | 発注点 | |
| 회전율 | inventory turnover | 在庫回転率 | annualized |
| 리드타임 | lead time | リードタイム | A/B 명시 |
| 적재율 | load factor | 積載率 | |
| 가용재고 | available to promise (ATP) | 引当可能在庫 | reserved 차감 |
| 예약 | reserved / allocated | 引当済 | |

## 운송·TMS

| 한국어 | 영어 | 일본어 | 비고 |
|---|---|---|---|
| 간선 | line-haul | 幹線 | |
| 라스트마일 | last-mile | ラストワンマイル | |
| 배차 | dispatch | 配車 | |
| 경로계획 | routing | ルーティング | |
| 차량 운행 문제 | VRP | VRP | 변형: VRPTW/VRPPD/CVRP/MDVRP |
| 부재배송 | failed delivery | 不在配達 | |
| 배송 슬롯 | delivery time slot | 配送スロット | |
| 수령 인증 | proof of delivery (POD) | 受取確認 | sign/photo/OTP |
| 픽업포인트 | locker / PUDO | コンビニ受取 | |
| 대금상환 | cash on delivery (COD) | 代引き | |
| 야드 | yard | 構内 | |
| 도크 어포인트먼트 | dock appointment | バース予約 | |
| 디텐션 | detention | デテンション | trailer 정체 |
| 디머리지 | demurrage | デマレージ | container 정체 |
| 추적 | track & trace | 追跡 | |
| 마일스톤 | milestone | マイルストン | tracking 사전 |
| 3PL/4PL/LSP | 3PL/4PL/LSP | 3PL/4PL/LSP | 위탁 단계 |
| CEP | courier·express·parcel | 宅配 | |

## 캐리어·EDI

| 한국어 | 영어 | 일본어 | 비고 |
|---|---|---|---|
| EDI 부킹 | EDI 204 (motor carrier load tender) | | 화주 → 캐리어 |
| EDI 응답 | EDI 990 (response to load tender) | | 캐리어 → 화주 |
| EDI 상태 | EDI 214 (shipment status) | | 캐리어 → 화주 |
| EDI 인보이스 | EDI 210 (freight details) | | 캐리어 → 화주 |
| EDI ASN | EDI 856 (ASN) | | 공급사 → 화주 |
| 라벨 ZPL | ZPL (Zebra programming language) | | Zebra 프린터 |
| Master AWB | MAWB | | forwarder ↔ airline |
| House AWB | HAWB | | forwarder ↔ shipper |
| 선하증권 | bill of lading (B/L) | 船荷証券 | |
| SeaWaybill | sea waybill (SWB) | | non-negotiable |
| VGM | verified gross mass | | SOLAS 의무 |
| FCL/LCL | full/less container load | FCL/LCL | 해상 |

## 통관·규제

| 한국어 | 영어 | 일본어 | 비고 |
|---|---|---|---|
| 통관 | customs clearance | 通関 | |
| HS코드 | HS code | HSコード | 국제 6자리 공통 |
| 관세 | tariff / duty | 関税 | |
| 인코텀즈 | Incoterms (2020) | インコタームズ | EXW/FOB/CIF/DAP/DDP |
| 위험물 | dangerous goods (DG) | 危険物 | UN class 1-9 |
| 식약처 | KFDA / MFDS | 食薬処 | 식품·의약품 |
| 개인통관고유부호 | personal customs clearance code (PCC) | | P+12자리 |
| 원산지 증명 | certificate of origin (C/O) | 原産地証明 | FTA |
| FTA | free trade agreement | FTA | KORUS/RCEP 등 |
| 사전신고 | advance manifest | 事前申告 | ISF/AMS/ENS |
| 보세창고 | bonded warehouse | 保税倉庫 | |
| AEO | authorized economic operator | AEO | 신뢰 통관 |
| 전략물자 | strategic items | 戦略物資 | dual-use |
| OFAC SDN | OFAC SDN list | OFAC | sanctions |

## 콜드체인·의약품

| 한국어 | 영어 | 일본어 | 비고 |
|---|---|---|---|
| 콜드체인 | cold chain | コールドチェーン | |
| 냉장 | chilled (2-8°C) | 冷蔵 | |
| 냉동 | frozen (-18°C 이하) | 冷凍 | |
| 일탈 | excursion | 逸脱 | TTI 적용 |
| 평균 동력 온도 | MKT (mean kinetic temperature) | MKT | |
| 우수 유통 관리 기준 | GDP (good distribution practice) | GDP | |
| 자격검증 | qualification (IQ/OQ/PQ) | 適格性評価 | |
| 직렬화 | serialization | シリアル化 | DSCSA/EU FMD/KIMS-K |
| 격리 | quarantine / hold | 隔離 | release 전 |
| HACCP | HACCP | HACCP | 식품 안전 |
| 회수 | recall | 回収 | class I/II/III |

## 계획·SCP

| 한국어 | 영어 | 일본어 | 비고 |
|---|---|---|---|
| 수요예측 | demand forecast | 需要予測 | |
| 예측 정확도 | forecast accuracy (MAPE/WMAPE) | 予測精度 | |
| 편향 | bias | バイアス | |
| 간헐 수요 | intermittent demand (Croston) | 間欠需要 | |
| 경제적 발주량 | EOQ | 経済的発注量 | |
| 다단계 재고 최적화 | MEIO (multi-echelon) | 多段階在庫最適化 | |
| ABC 분류 | ABC classification | ABC分析 | |
| S&OP | sales & operations planning | S&OP | 월간 cadence |
| IBP | integrated business planning | IBP | 재무 통합 |
| Bullwhip | bullwhip effect | ブルウィップ効果 | |
| 발주 | purchase order (PO) | 発注 | |
| 3-way match | 3-way match | 3面照合 | PO/GR/Invoice |
| FVA | forecast value add | FVA | 단계별 정확도 |

## 정확도·안전·품질

| 한국어 | 영어 | 일본어 | 비고 |
|---|---|---|---|
| 재고 정확도 | inventory record accuracy (IRA) | 在庫精度 | |
| 순환 카운트 | cycle count | サイクルカウント | |
| 블라인드 카운트 | blind count | 盲検 | 시스템 미공개 |
| 손실 | shrinkage | シュリンケージ | |
| 산업안전 | industrial safety (OSHA/KOSHA) | 産業安全 | |
| LOTO | lockout/tagout | LOTO | |
| 시업 전 점검 | pre-shift inspection | 始業前点検 | PIT |
| Near-miss | near-miss | ヒヤリハット | 사고 직전 |
| UPH | units per hour | UPH | 노동 생산성 |
| SAH | standard allowed hours | SAH | engineered |

## 플랫폼·이벤트

| 한국어 | 영어 | 일본어 | 비고 |
|---|---|---|---|
| 멱등성 | idempotency | 冪等性 | |
| 보상 트랜잭션 | compensation / saga | 補償トランザクション | |
| 이벤트 envelope | event envelope | イベントエンベロープ | |
| Outbox 패턴 | outbox pattern | アウトボックス | 이중 쓰기 방지 |
| Dead letter queue | DLQ | DLQ | |
| 회로 차단기 | circuit breaker | サーキットブレーカー | |
| 격벽 | bulkhead | バルクヘッド | 격리 |
| 다중 테넌시 | multitenancy | マルチテナンシー | 3PL/marketplace |
| Row-level security | RLS | 行レベルセキュリティ | |
| RPO / RTO | RPO / RTO | RPO / RTO | DR 목표 |
| Trace propagation | trace propagation (W3C) | トレース伝播 | OpenTelemetry |

## ESG·탄소

| 한국어 | 영어 | 일본어 | 비고 |
|---|---|---|---|
| 탄소 배출 | carbon emission | 炭素排出 | gCO₂e/tkm |
| 톤킬로미터 | tonne-kilometre (tkm) | トンキロ | |
| Scope 3 | Scope 3 | スコープ3 | cat 4/9 운송 |
| CBAM | carbon border adjustment | CBAM | EU |
| GLEC framework | GLEC framework | GLECフレームワーク | well-to-wheel |
| 회수 포장재 | reusable packaging | 通い箱 | deposit-refund |

## 개인정보·데이터

| 한국어 | 영어 | 일본어 | 비고 |
|---|---|---|---|
| 개인정보 | PII / personal data | 個人情報 | |
| 개인정보보호법 | PIPA | 個人情報保護法 | |
| 위탁(처리위탁) | processor / DPA | 委託 | |
| Cross-border 이전 | cross-border transfer (SCC) | 越境移転 | SCC/BCR |
| 마스킹 | masking | マスキング | 5년 후 |
| 정보주체 요청 | DSR (data subject request) | 開示請求 | GDPR 30일 |
| 침해 통지 | breach notification | 漏洩通知 | 72h GDPR |
