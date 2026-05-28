# wcs-mhe 도메인 참조

## 활용 시점

- 설계 자문: WCS 작업 큐, AGV/AMR 라우팅, 소터 induction, AS-RS 보충, MES 브리지, fallback 시나리오 수립
- 코드·인터페이스 리뷰: `wcs`, `mhe`, `agv`, `amr`, `conveyor`, `sorter`, `induction`, `asrs`, `crane`, `mes`, `plc`, `opc_ua`, `traffic_manager` 식별자/프로토콜 등장 시
- 운영·인시던트: induction window 초과, AGV 충돌·교착, 소터 mis-sort, AS-RS 크레인 에러, PLC 통신 단절
- 사용자 발화 예: "WCS 연동", "AGV 작업 분배", "소터 induction", "AS-RS 보충", "MES hand-off"

## 점검 포인트

1. **작업 큐 모델** — task 우선순위(SLA tier·납기·존), 차단(blocking) vs 비차단 구분, 미할당 task TTL 정책?
2. **AGV/AMR 교통관리** — 중앙 traffic manager vs 분산 협상, lock zone, 우회 경로, 충돌 회피 알고리즘(예약·priority·time-based) 명시?
3. **컨베이어·소터 induction** — induction rate(units/hour) 캡, 정렬 윈도우(라벨 인식 거리), reject 라인 운영 정책? 잘못 induct 시 회수 워크플로?
4. **AS-RS 보충/회수** — dual command(저장+회수 결합) 적용? 크레인 작업 큐 분배·균등?
5. **MES↔WMS 브리지** — 작업 지시 envelope(`task_id`, `priority`, `due_at`, `payload`), ack/nack/heartbeat 주기, 멱등성 키는?
6. **PLC/OPC UA 프로토콜** — 통신 단절 시 재연결·재시도 전략? 실시간 상태 polling vs subscription?
7. **안전 인터록** — emergency stop, light curtain, lockout/tagout 신호가 작업 큐와 어떻게 연동(인터록 시 그 영역 task 즉시 보류)?
8. **fallback 시나리오** — 자동화 장애 시 수동 픽 전환 절차, 부분 장애(소터 1 lane 정지) 우회, 데이터 reconciliation?
9. **OEE/throughput 지표** — Availability × Performance × Quality, 정의·측정 위치·산정 주기?
10. **이벤트 발행** — task_started / completed / failed / aborted을 `logistics-event-schema` 표준 envelope로 발행? 후속 시스템(WMS/KPI/billing)으로 전파?

## 응답 형식

- 질문 → 표준 작업 큐 모델·hand-off 프로토콜·fallback 시나리오
- 리뷰 → 약점·위험·수정 제안 (필요 시 `file:line`)
- 안전 인터록 위반 위험은 별도 강조

## Hand-off

- 작업 지시 발화원 → `wms-inventory`/`wave-pick-strategy`
- 위치 할당 정책 → `slotting-putaway`
- 안전·LOTO·인터록 → `warehouse-safety`
- 이벤트 envelope 표준 → `logistics-event-schema`
- 멱등성·dedup → `logistics-idempotency`
