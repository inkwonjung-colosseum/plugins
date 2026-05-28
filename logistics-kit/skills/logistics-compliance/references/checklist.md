# logistics-compliance 도메인 참조

## 활용 시점

- 설계 자문: HS코드 분류, Incoterms 책임 분기, 위험물 SKU 마스터, 식약처/KC 인증 흐름
- 코드·정책 리뷰: `hs_code`, `customs`, `tariff`, `incoterms`, `imdg`, `un_number`, `dangerous_goods`, `pcc`, `origin`, `kc_certification` 식별자가 보일 때
- 운영·규제 검토: 통관 거부, 인증 누락, 개인정보 보관 기간 위반
- 사용자 발화 예: "통관", "수출입 신고", "위험물 분류", "식약처 등록", "개인통관고유부호", "원산지 증명"

## 점검 포인트

1. **HS코드** — 상품 분류가 외부 마스터(관세청)와 sync? 분류 변경 effective date 처리?
2. **Incoterms** — EXW/FOB/CIF/DDP 중 어느 단계에서 위험·비용·관세가 어디로 넘어가는지 코드와 정책서가 일치?
3. **위험물** — UN번호·class·PG(포장그룹)가 SKU master 필수 항목? 위험물 SKU 운송 가능 차량 제약?
4. **식약처/KC** — 식품·의약품·전기용품 인증번호 필수. 미인증 SKU 판매 차단 로직?
5. **개인통관고유부호(PCC)** — 해외직구 시 PCC 형식 검증(P + 12자리), 1인당 면세 한도($150) 누적?
6. **개인정보** — 수하인 정보 보관기간(5년), 배송 완료 후 마스킹 정책, 위탁사 접근 권한?
7. **원산지 증명(C/O)** — FTA 협정 활용 시 원산지 결정 기준 자동 판정 가능? 깊은 결정 트리는 `fta-origin` 위임.
8. **위험물 segregation·DGR 깊이** — IMDG/IATA/ADR 모드별 분리·LQ·리튬 PI는 `dangerous-goods` 위임
9. **제재 스크리닝 (denied party)** — OFAC SDN/EU/UN/전략물자, end-use/end-user 검증은 `trade-sanctions` 위임
10. **식약처 인증 워크플로** — 의약품 GDP·DSCSA·KIMS-K(직렬화)는 `pharma-gdp-serialization`, 식품 HACCP은 `haccp-food-safety` 위임
11. **개인정보(PIPA/GDPR)** — 수하인 PII·SCC·DSR은 `data-privacy-logistics` 위임
12. **회수·식약처/FDA 보고** — recall class·시한·보고는 `recall-traceability` 위임
13. **국제 운송 사전신고** — ISF/AMS/ENS·B/L·AWB는 `freight-forwarding` 위임
14. **chain of custody** — 주류·담배·마약류·controlled substance는 `chain-of-custody` 위임
15. **AEO/C-TPAT** — 신뢰통관 자격, 갱신 주기, 혜택 매트릭스

## 응답 형식

- 질문 → 표준 규정·근거 법령·실무 패턴
- 리뷰 → 규정 위반 위험·근거 법령·수정 방향
- 외부 마스터(관세청 등) 동기화 권고는 별도 표기

## Hand-off

- 운임/관세 정산·분개 → `logistics-settlement`
- KPI 통계 → `logistics-kpi`
- 위험물 운송 차량 제약 → `tms-routing`/`dangerous-goods`
- FTA 원산지 결정 트리 → `fta-origin`
- 제재 스크리닝·EAR/ITAR → `trade-sanctions`
- 의약품 GDP·serialization → `pharma-gdp-serialization`
- 식품 HACCP → `haccp-food-safety`
- 회수·class 결정 → `recall-traceability`
- chain of custody → `chain-of-custody`
- 국제 운송·B/L → `freight-forwarding`
- PII·PIPA·GDPR → `data-privacy-logistics`
- 탄소 CBAM → `sustainability-carbon`
