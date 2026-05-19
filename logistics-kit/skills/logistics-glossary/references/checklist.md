# logistics-glossary 도메인 참조

## 활용 시점

- 자문: 신규 용어 정의, 한/영/일 매핑, 코드 식별자 통일
- 코드·문서 리뷰: 용어 사전(`glossary.json`, `terms.md`), i18n 키 파일(en/ja/ko), API spec 등장 시
- 운영: 같은 개념의 변형 표기 누적, 다국어 번역 불일치
- 사용자 발화 예: "용어 통일", "stock vs inventory", "용어집", "용어 번역"

## 점검 포인트

1. **코드 식별자 일관성** — 같은 개념에 `stock_count` / `inventory_qty` / `qty_on_hand` 혼재? 한 가지로 통일.
2. **i18n 키** — 같은 영문 라벨이 ja/ko에 다른 단어로 번역되어 있지 않나?
3. **API 응답 필드** — `outbound_at` vs `shipped_at` vs `dispatch_time` 같은 변형 검출.
4. **신규 용어** — `glossary.md`에 없는 용어는 *추가 제안* 형태로 분리.

## 응답 형식

- 질문 → 표준 용어(→ `glossary.md`)·한/영/일 매핑·근거
- 리뷰 → 변형 표기 위치·권장 표준 용어
- 한/영/일 매핑 표 업데이트 제안은 별도 표기

## Hand-off

- i18n 키 네이밍 컨벤션 자체 → 프로젝트의 `i18n-key-guard` 스킬(있을 경우)로 위임
