# pharma-gdp-serialization 도메인 참조

## 활용 시점

- 자문: GDP 인증, qualification(IQ/OQ/PQ), MKT 계산, excursion 워크플로, serialization·aggregation 설계
- 코드·정책 리뷰: `gdp`, `gmp`, `gsp`, `iq`, `oq`, `pq`, `mkt`, `excursion`, `dscsa`, `eu_fmd`, `kims_k`, `serialization`, `aggregation`, `t3`, `epcis` 식별자/문서 등장 시
- 운영·감사: 일탈 보고 누락, qualification 기록 미흡, 직렬번호 충돌, 사용기한 추적 실패
- 사용자 발화 예: "GDP", "qualification", "MKT", "excursion review", "직렬화", "DSCSA", "약사법"

## 점검 포인트

1. **GDP 6대 원칙** — 품질관리·인력·시설/장비·문서화·운영·일탈관리 적용 매트릭스, 식약처 GDP 가이드 매핑?
2. **qualification IQ/OQ/PQ** — 시설/장비/시스템 IQ(설치)·OQ(작동)·PQ(성능) 프로토콜, 보관·운송 장비별 책임 정의?
3. **온도 mapping** — 창고·트럭·컨테이너 매핑 study(여름/겨울 4계절, 빈/만재), hot/cold spot 식별, sensor 배치 표준?
4. **MKT 계산** — `MKT = -ΔH/R / ln(Σ exp(-ΔH/RT_i)/n)` (ΔH=83.144 kJ/mol 표준), 사용 시점·기준 온도?
5. **excursion review board** — 일탈 발생 → 격리(quarantine) → 영향 평가(시간×온도·MKT·안정성 data) → 사용/폐기 결정, time bar?
6. **CAPA·재발 방지** — root cause·CAPA·effectiveness check, audit trail immutability?
7. **DSCSA(US)** — T3(transaction info/history/statement), unit-level serialization, EPCIS event, 2024 stabilization·2025 full enforcement?
8. **EU FMD** — 직렬번호 + tamper-evident, 약국 dispense 시점 verify, NMVS hub?
9. **KIMS-K(한국)** — 의약품 일련번호 보고 의무, 변환/포장 변경 시 재발급, RFID·바코드 표준?
10. **aggregation·hierarchy** — 단위(unit) → 카톤 → 팔레트 → 컨테이너 묶음 관계, sscc·gtin 기록, scan-once-claim-many?
11. **FEFO·quarantine·release** — 입고 후 격리(qc release 전), QC 승인 후 sellable, FEFO 강제, returns 격리?
12. **온도 일탈 운송 SOP** — pre-conditioning, dry-ice 추가, gel-pack 검증, alarm sla?
13. **반품·회수** — 일탈·결함 시 회수 분류(class I/II/III), 식약처 보고 시한, 폐기 입증·소각 인증서?

## MKT 산식 예시

```
T_i: i 시점 K 단위 온도
ΔH: 활성화 에너지 (83.144 kJ/mol 권장)
R: 가스 상수 (8.314 J/(mol·K))
MKT = -ΔH/R / ln(Σ_i e^{-ΔH/(R*T_i)} / n)
```

## 응답 형식

- 질문 → qualification·MKT·serialization 표준·근거 법령
- 리뷰 → 약점·법적 위험·CAPA 권고
- 환자 안전·법적 책임 위험 별도 강조

## Hand-off

- 일반 콜드체인 모니터링 → `cold-chain-monitor`
- 통관·HS·식약처 → `logistics-compliance`
- 회수(class I~III) → `recall-traceability`
- chain of custody → `chain-of-custody`
- 클레임·보험 → `cargo-claims-insurance`
- 마약류·향정 → `chain-of-custody`
