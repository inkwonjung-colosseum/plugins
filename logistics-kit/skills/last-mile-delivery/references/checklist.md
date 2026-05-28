# last-mile-delivery 도메인 참조

## 활용 시점

- 설계 자문: 시간대 슬롯 booking, POD 표준, 부재 재시도 SLA, locker/PUDO, COD/age-verification 정책 수립
- 코드·API 리뷰: `slot`, `delivery_window`, `pod`, `signature`, `otp`, `failed_delivery`, `redelivery`, `locker`, `pudo`, `pickup_point`, `cod`, `age_verification` 식별자가 보일 때
- 운영·디버깅: 슬롯 oversell, 부재 재시도 폭증, POD 누락, COD 미수, locker 만적, 새벽배송 cutoff 위반
- 사용자 발화 예: "시간대 배송", "부재 재시도", "POD 사진", "OTP 인증", "택배 locker", "성인 인증", "COD"

## 점검 포인트

1. **슬롯 모델** — capacity 계산 단위(드라이버×시간×구간 stops), oversell 방지, 동적 가격(peak 가산) 적용?
2. **슬롯 booking API** — quote → hold(TTL) → confirm 패턴 멱등성? hold 만료 시 자동 해제?
3. **POD 표준** — 서명(eSign) / 사진(GPS·timestamp) / OTP(SMS·kakao) / 비대면 사진 위치 — SLA tier별 요구 매트릭스?
4. **부재 처리** — 1차 부재 후 재시도 SLA(24/48h), 최대 N회, 후 RTS(return to sender) 정책? 알림 채널(SMS·앱·전화)?
5. **locker/PUDO** — locker 용량(small/medium/large), 보관기간(72h), 미수령 시 회수, picking 인증(코드/QR/생체)?
6. **attended vs unattended** — 비대면 정책(문 앞·경비실·택배함) 분기, 화주별 옵션 vs 수하인 옵션 우선순위?
7. **COD(대금상환)** — 현장 결제 수단(현금·카드·간편결제), 위변조 방지, 회수 정산 cycle, 미수 대응?
8. **age-verification** — 주류·담배·R등급 콘텐츠 신분증 확인, 본인 일치 검증 절차, 거절 시 회수?
9. **도서산간/제주/오지** — 우편번호·좌표 기반 분기, 운임 가산·일정 지연 안내?
10. **새벽배송 cutoff** — 주문 마감 → 출고 → 도크 → 배송 cutoff 체인, breaking 시 alert?
11. **failed-delivery 사진 증빙** — 사유 코드(주소 불명·부재·수령 거부), 사진+GPS 자동 캡처 의무?
12. **first-attempt delivery rate KPI** — 1차 성공율, 슬롯 정확도, on-time delivery 분해 보고?

## 응답 형식

- 질문 → 표준 슬롯 모델·POD 매트릭스·재시도 SLA
- 리뷰 → 약점·위험·수정 제안 (필요 시 `file:line`)
- 분쟁 위험(미수령·파손) 별도 강조

## Hand-off

- 라우팅·VRP 솔버 → `vrp-rating-engine`
- 추적 노출·ETA → `track-trace`
- 캐리어 라벨/EDI → `carrier-edi`
- OTD/1차 성공율 KPI → `logistics-kpi`
- 클레임·보험 → `cargo-claims-insurance`
- 개인정보(수하인 PII) → `data-privacy-logistics`
