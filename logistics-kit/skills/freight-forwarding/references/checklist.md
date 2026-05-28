# freight-forwarding 도메인 참조

## 활용 시점

- 설계 자문: 해상/항공/복합 부킹 워크플로, B/L·AWB 발행, 사전신고 일정, 트랜스십·환적 정책 수립
- 코드·문서 리뷰: `ocean`, `air`, `fcl`, `lcl`, `awb`, `hawb`, `mawb`, `bill_of_lading`, `vgm`, `isf`, `ams`, `ens`, `transshipment`, `ula`, `baf`, `caf` 식별자/문서 등장 시
- 운영·디버깅: 사전신고 지연(과태료), VGM 누락(선적 거부), 트랜스십 손상, AWB 분실, demurrage 청구
- 사용자 발화 예: "해상 부킹", "AWB 발행", "B/L 발행", "VGM", "ISF 신고", "트랜스십"

## 점검 포인트

1. **해상 부킹** — 선사 schedule·CY/CFS 마감, FCL(20/40/40HC/45/RF) vs LCL(consolidator), space booking·shipping order(S/O)?
2. **항공 부킹** — 항공사 schedule, ULD(LD3/LD7/PMC), 일반 vs cool chain, MAWB ↔ HAWB 매핑, neutral AWB 정책?
3. **B/L 종류·발행** — Original / Sea Waybill / Telex Release / SWB·OBL, surrender·endorsement 정책, 분실 대응(LOI)?
4. **AWB 종류** — MAWB (forwarder ↔ airline) / HAWB (forwarder ↔ shipper), 발행권 IATA, e-AWB 도입 여부?
5. **VGM(verified gross mass)** — SOLAS 의무, 발행 SOP, 선적 cutoff 전 검증?
6. **ISF/AMS/ENS 사전신고** — 미국 ISF(24h before loading), AMS(부킹 후), EU ENS(24h before loading), 한국 적하목록 — 일정·필수항목·과태료?
7. **트랜스십·환적 라우팅** — 직항 vs 트랜스십 트레이드오프, 트랜스십 항만 위험 평가, 컨테이너 트래킹?
8. **incoterms-기반 책임 분기** — EXW/FCA/CPT/CIP/DAP/DPU/DDP — 누가 어느 단계까지 부담? CIF/CIP 보험 의무?
9. **demurrage/detention 시계** — 양하 후 자유시간(보통 7일), 도크 진입 후 추가, 일별 부과율, 운영자별 정책?
10. **부대비용 매트릭스** — BAF(유류 할증)·CAF(통화)·THC(터미널 핸들링)·CIC(컨테이너 불균형)·war risk·security·문서 비용?
11. **dangerous goods 모드별** — 해상 IMDG / 항공 IATA DGR / 도로 ADR / 철도 RID — 신고서·UN PI 매트릭스?
12. **컨테이너 추적·EDI** — 해운 IFTSTA / 항공 FFM/FWB/FHL/FSU, 도착지 통관 연계?
13. **inland transport leg** — 항만 → 내륙 트럭킹/드레이지, 컨테이너 반납 마감?

## 응답 형식

- 질문 → 부킹 워크플로·문서 표준·사전신고 일정
- 리뷰 → 약점·위험·수정 제안 (필요 시 `file:line`)
- 사전신고 지연·VGM 누락·B/L 분실 위험 별도 강조

## Hand-off

- HS·관세·incoterms → `logistics-compliance`/`fta-origin`
- 해상/항공 dangerous goods → `dangerous-goods`
- 운임/부대비용 정산 → `logistics-settlement`
- 컨테이너 추적·ETA → `track-trace`
- 보험·청구·subrogation → `cargo-claims-insurance`
- 야드·드레이지 → `yard-dock`
