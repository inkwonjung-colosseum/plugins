# labor-mgmt 도메인 참조

## 활용 시점

- 설계 자문: engineered standards, UPH 목표, 인센티브 산식, shift planning, indirect/direct ratio 정책 수립
- 코드·정책 리뷰: `labor`, `lms`, `uph`, `lines_per_hour`, `engineered_standard`, `sah`, `most`, `mtm`, `shift`, `incentive`, `attendance` 식별자가 보일 때
- 운영·디버깅: 생산성 격차, 인센티브 분쟁, indirect 노동 증가, shift 인력 부족, 결근율 상승
- 사용자 발화 예: "UPH 산식", "engineered standard", "인센티브", "shift 배정", "indirect 비율"

## 점검 포인트

1. **engineered standard 수립** — MOST/MTM 분석 vs 시간 동작 연구(time study), SKU·위치·디바이스별 표준 시간(SAH) 매트릭스? 갱신 주기?
2. **UPH/lines per hour** — 분모(actual work hours) 정의(휴게·교육·미팅 제외), 분자 측정 시점, 카테고리별 분리 보고?
3. **direct vs indirect ratio** — direct(픽·팩·로딩) vs indirect(replenishment·청소·이동) 분류, 목표 비율, 자동 분류 방법?
4. **인센티브 산식** — 목표 대비 N% 초과 시 단가 가산? cap·floor·품질 페널티(error·shorts) 차감 조건?
5. **shift planning** — 수요예측 기반 인력 계산(`forecast_volume / target_uph × adjustment_factor`), 정규/일용/파견 비율, 핀치 타임 인력 보강?
6. **결근·이탈률 KPI** — no-show 율, 30/60/90일 이탈률, 사유 분류(휴직·이직·해고·기타)?
7. **작업 표준 거버넌스** — 표준 변경 승인 워크플로, 노조·근로자 대표 협의, change log audit?
8. **개인 라벨 vs 그룹 라벨** — 익명 그룹 라벨(팀별 UPH)만 노출 정책 vs 개인 라벨 노출 시 인사노무 리스크 검토?
9. **온보딩·교육 ramp-up** — 신규 인력 1주/4주 목표 UPH, 멘토 매칭, 미달 시 코칭 절차?
10. **자동화 도입 시 노동 영향 분석** — 인력 전환·재배치 계획, indirect→direct 전환, 인력 감축 시 노사 협의?

## 응답 형식

- 질문 → 표준 산식·인센티브 정책·shift 운영
- 리뷰 → 약점·위험·수정 제안 (필요 시 `file:line`)
- 인사노무 분쟁 위험 별도 강조 (개인 라벨·인센티브 불공정·shift 강제)

## Hand-off

- 안전·재해·OSHA/KOSHA → `warehouse-safety`
- KPI(UPH·indirect 비율) 정의 → `logistics-kpi`
- 자동화 비율·MHE 영향 → `wcs-mhe`
- engineered standard 적용 위치 → `slotting-putaway`/`wave-pick-strategy`
