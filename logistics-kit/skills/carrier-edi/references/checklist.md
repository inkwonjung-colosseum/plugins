# carrier-edi 도메인 참조

## 활용 시점

- 설계 자문: EDI 표준 메시지 매핑, 전송 채널 선택, 라벨 표준, status 정규화 정책 수립
- 코드·인터페이스 리뷰: `edi`, `204`, `214`, `990`, `210`, `856`, `as2`, `sftp`, `zpl`, `epl`, `label`, `webhook`, `carrier_api`, `tracking_number` 식별자/문서 등장 시
- 운영·디버깅: webhook 중복, label voiding 실패, status 코드 매핑 누락, EDI envelope 오류
- 사용자 발화 예: "EDI 연동", "ZPL 라벨", "carrier webhook", "tracking status 매핑", "ASN 856"

## 점검 포인트

1. **EDI 메시지 표준** — 204(부킹 요청) / 214(shipment status) / 990(부킹 응답·수락·거절) / 210(invoice) / 856(ASN) 매핑이 캐리어별로 정확? ISA/GS/ST envelope 버전(004010 vs 005010)?
2. **전송 채널** — AS2(서명/암호화·MDN) vs SFTP(키 관리·완료 파일 표시) vs REST API(인증·rate limit), 캐리어별 매칭과 fallback?
3. **라벨 생성/포맷** — ZPL(Zebra) / EPL / PDF / PNG, DPI(203/300/600), 라벨 사이즈(4×6) 표준, 캐리어 form 변경 대응?
4. **라벨 voiding/refund** — 미사용 라벨 24/48시간 내 void API 호출 정책, 환불 status 추적?
5. **webhook ingestion 멱등성** — `event_id` / `transaction_id` 기반 dedup, replay 안전, 재시도 시 응답 캐싱(2xx 반환만)?
6. **status code 정규화** — 캐리어별 status(in_transit / out_for_delivery / exception 등)을 canonical 코드로 매핑한 매트릭스 유지? unknown status fallback?
7. **EDI 거절 처리** — 990 reject 사유 코드 매트릭스, 재발행 자동 vs 수동?
8. **dim weight 계산** — 캐리어별 dim divisor(139·166·5000) 일치, 가산 시점·반올림?
9. **multi-carrier 추상화** — 카테고리(parcel / LTL / FTL / postal) 별 공통 인터페이스, 캐리어 specific 옵션 패스스루?
10. **EDI 보관 의무** — 송수신 원본 보관 7년·인증(GS1·VAN) 로그 immutability?
11. **rate API 호출 비용·캐싱** — quote API 호출 캐싱 TTL, rate-limit 백오프 정책?

## 응답 형식

- 질문 → 표준 메시지·전송 채널·라벨 포맷·status 매핑
- 리뷰 → 표준 위반·위험·수정 제안 (필요 시 `file:line`)
- 멀티 캐리어 추상화 권고는 별도 표기

## Hand-off

- 멱등성/dedup → `logistics-idempotency`
- 이벤트 envelope 표준 → `logistics-event-schema`
- 운임/accessorial 정산 → `logistics-settlement`
- 고객 노출 tracking → `track-trace`
- 위험물·식약처 라벨 → `dangerous-goods`/`logistics-compliance`
