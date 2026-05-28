# inventory-accuracy 도메인 참조

## 활용 시점

- 설계 자문: cycle count 빈도, blind count 정책, 차이 사유 코드 체계, 조정 승인 한도, shrinkage 분개 정책 수립
- 코드·정책 리뷰: `cycle_count`, `blind_count`, `inventory_record_accuracy`, `ira`, `shrinkage`, `variance`, `adjustment`, `recount`, `count_team` 식별자가 보일 때
- 운영·감사: 재고 차이 누적, 조정 승인 누락, shrinkage 분개 불일치, blind count 오염
- 사용자 발화 예: "재고 차이", "cycle count 빈도", "blind count", "shrinkage 분개", "IRA 산식"

## 점검 포인트

1. **IRA 산식** — `correct_locations / counted_locations` (위치 기준) vs `correct_units / counted_units` (수량 기준)? 보고 단위 통일?
2. **ABC 기반 cycle count 빈도** — A: 월 1+회 / B: 분기 / C: 반기 표준안과 실제 매칭? high-value SKU 별도 빈도?
3. **blind count 절차** — 카운터에게 시스템 수량 미공개? 1차 카운트 후 2차 recount 트리거 조건(차이 N% 이상)?
4. **차이 사유 코드(reason code)** — picking 오류 / putaway 오류 / 도난·분실 / 파손 / 시스템 오류 / 시점 차이 매트릭스, 사유별 후속 조치?
5. **조정 승인 한도** — 금액·수량별 승인 권한(supervisor / manager / director), 분개 자동 게시 여부?
6. **shrinkage 분개** — 분실/파손/조정의 차변/대변 계정 매핑, 부가세 처리, 보험 청구 분기?
7. **감사 로그 immutability** — 조정 이력이 audit table에 누가/언제/사유와 함께 영구 기록되나? hard delete 금지 정책?
8. **차이 root cause 분석 워크플로** — 패턴 분석(특정 위치/SKU/시프트), CAPA 조치, 재발 방지 검증?
9. **통계적 샘플링** — population 모집단 대비 신뢰수준 95% 표본 크기 정의? 정밀도 ±N%?
10. **wall-to-wall(전수) count 정책** — 연 1회 vs cycle 의존? 외부감사 요구 시 절차?

## 응답 형식

- 질문 → 표준 산식·승인 한도·root cause 매트릭스
- 리뷰 → 약점·위험·수정 제안 (필요 시 `file:line`)
- 회계 분개 매핑 권고는 별도 표기

## Hand-off

- 재고 트랜잭션 자체 → `wms-inventory`
- shrinkage 분개·보험 청구 → `logistics-settlement`
- IRA·shrinkage KPI 정의 → `logistics-kpi`
- 감사 로그 모델 → `logistics-data-model`
- 사유 lot/serial 추적 → `recall-traceability`
