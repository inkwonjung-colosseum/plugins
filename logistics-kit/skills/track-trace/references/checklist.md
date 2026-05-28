# track-trace 도메인 참조

## 활용 시점

- 설계 자문: milestone 사전, status 정규화, ETA 모델, 알림 fan-out, exception 큐 정책 수립
- 코드·API 리뷰: `tracking`, `milestone`, `status_normalization`, `eta`, `exception`, `notification_channel`, `subscription`, `tracking_number` 식별자가 보일 때
- 운영·디버깅: 중복 이벤트로 잘못된 status, ETA 부정확, 알림 폭주, PII 노출
- 사용자 발화 예: "tracking 화면", "ETA 계산", "milestone", "알림 채널", "exception"

## 점검 포인트

1. **canonical milestone 사전** — order_created / picked / packed / handed_over_to_carrier / picked_up / in_transit / out_for_delivery / delivered / exception / RTS — 정의·발생 주체·필수/선택 매트릭스?
2. **multi-carrier status 정규화** — 캐리어별 status 코드를 canonical로 매핑, unknown은 raw 보존 + monitoring alert?
3. **이벤트 중복 제거** — `event_id`/`(tracking, status_code, occurred_at)` 기반 dedup, 순서 역전(out-of-order) 처리?
4. **ETA 모델** — 정적(SLA 기반) vs 동적(과거 실적·날씨·교통 ML), 재계산 트리거(milestone 발생·예상 초과)?
5. **알림 fan-out** — 채널 우선순위(앱 push → 카카오 → SMS → 이메일), 채널별 cool-down, opt-out 적용?
6. **exception queue** — 일탈(부재·파손·분실·지연) 격리 큐, CS 핸드오프, SLA tier별 즉시 알림?
7. **권한·PII 마스킹** — 화주(전체) vs 수하인(자신 건만) vs guest(부분), 수령인 이름·주소 마스킹 정책(`홍**`, `서울시 강남구 ***`)?
8. **공개 추적 페이지** — guest 접근 시 트래킹 번호+우편번호 등 2-factor, scraping 방지(rate limit·captcha)?
9. **webhook 구독** — 화주 시스템 webhook fan-out, 재시도·DLQ, 서명(HMAC)?
10. **history 시계열 표시** — 사용자 화면에 milestone 시계열·지도 노출 정책, 시간대(타임존) 표시?
11. **multi-leg 추적** — 화물 분할/병합 시 child tracking과 parent 매핑 표현?
12. **데이터 보존** — 추적 데이터 보존 기간(배송 완료 후 30/90/180일), 익명화·삭제 자동화?

## 응답 형식

- 질문 → milestone 표준·정규화 매트릭스·ETA 모델
- 리뷰 → 약점·위험·수정 제안 (필요 시 `file:line`)
- PII·권한 위험 별도 강조

## Hand-off

- 원천 이벤트 — 내부 → `logistics-event-schema`, 캐리어 → `carrier-edi`
- 컨슈머 멱등성·dedup → `logistics-idempotency`
- 라스트마일 POD/exception → `last-mile-delivery`
- 알림 PII·동의 → `data-privacy-logistics`
- ETA 정확도 KPI → `logistics-kpi`
