# fta-origin 도메인 참조

## 활용 시점

- 자문: 협정별 원산지 규칙 결정, RVC·CTC·de-minimis 적용, C/O 발급·자기증명, 누적 활용
- 코드·정책 리뷰: `fta`, `rules_of_origin`, `roo`, `korus`, `rcep`, `usmca`, `eu_fta`, `rvc`, `ctc`, `de_minimis`, `cumulation`, `c_o`, `origin_declaration` 식별자/문서 등장 시
- 운영·감사: 원산지 위반·재분류·사후 검증 요청, C/O 거부, RVC 산정 오류
- 사용자 발화 예: "FTA 원산지", "KORUS", "RCEP", "RVC", "CTC", "C/O 발급"

## 점검 포인트

1. **협정별 규칙 비교** — KORUS / USMCA / RCEP / EU·UK / CPTPP / ASEAN / 한-중 — 동일 HS에 다른 규칙? 협정 우선순위?
2. **PSR 매트릭스(product specific rule)** — HS별 CTC(4·6 자리 변경) + RVC(BD·BU·NC 산식) + 가공기준?
3. **RVC 산식 매트릭스** — Build-Down `((TV - VNM)/TV)×100`, Build-Up `(VOM/TV)×100`, Net Cost `((NC - VNM)/NC)×100` — 협정별 선택?
4. **CTC 변경 기준** — CC(2자리) / CTH(4자리) / CTSH(6자리) 매트릭스, 비원산지 재료 분류 변경 여부?
5. **de-minimis(미소 기준)** — 비원산지 재료 비율 7~10% 면제(상이), 섬유는 별도, 적용 매트릭스?
6. **누적(cumulation)** — 양자 / 대각(diagonal) / 완전(full) 누적, 가능 협정 매트릭스?
7. **원산지 증명서** — 자율발급(self) vs 인증발급(approved) vs 기관발급(authority), 협정별 가능 형태?
8. **6 자리 HS 적용** — HS 6자리는 국제 공통, 7+자리는 국가별 — PSR 시 일관성?
9. **사후 검증(verification) 대응** — 외국 세관 verification 요청 시 응답 시한, 문서 보존 5년+?
10. **공급자 declaration·BOM tracing** — 다단계 BOM에서 원산지 재료 추적, 공급자 declaration 수집?
11. **operations not conferring origin** — 단순 가공·라벨링·재포장은 원산지 부여 불가, 회피 제도?
12. **품목별 특수규칙** — 농산물(WO 완전생산), 화학(별표·CRO), 자동차(부품 RVC), 섬유(yarn forward)?
13. **C/O system** — KORUS Korean C/O(KOTRA·세관), RCEP 자기증명, EU REX·EUR.1?

## 결정 트리

```
1. 협정 → 적용 가능한가? 직접운송 요건 충족?
2. 완전생산(WO)? 예 → 원산지 인정. 아니오 → 3.
3. PSR 확인 (CTC + RVC + 가공기준)?
4. CTC 적용? 비원산지 재료 분류 변경?
5. RVC 적용? Build-up/Build-down/Net-cost 계산?
6. de-minimis 적용?
7. 누적 활용 가능? 양자/대각/완전?
8. operations not conferring origin 회피?
9. C/O 발급 방법·문서·증빙 보존?
```

## 응답 형식

- 질문 → 협정별 규칙·산식·결정 트리
- 리뷰 → 적용 오류·시한·증빙 위험
- 사후 검증 시한·관세 추징 위험 별도 강조

## Hand-off

- HS·통관 신고 → `logistics-compliance`
- 제재·EAR·dual-use → `trade-sanctions`
- 국제 운송 부킹·B/L → `freight-forwarding`
- 관세 환급·분개 → `logistics-settlement`
- 식약처/KC/위험물 → `logistics-compliance`/`dangerous-goods`
- 탄소 CBAM CN-code → `sustainability-carbon`
