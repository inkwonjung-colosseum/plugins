---
name: planning-format
description: Use when a draft, file, folder, URL, or image must become Korean 정책서·기능설계서 — planning-level only, no implementation detail.
---

# planning-format

기획 입력 하나를 PM/기획자용 정책서 + 기능설계서로 변환한다. 정책·규칙·상태·역할과 기능 흐름·화면·동작을 기획 레벨에서 다룬다. 구현 상세(데이터 모델·API·NFR·테스트)와 PM 전략 장식(RACI·RICE·리스크·로드맵·페르소나·여정)은 다루지 않는다.

## Inputs

- Positional: text, file, directory, image, or `https?://` URLs. 옵션 없음.
- Mixed URL and non-URL tokens = text input. `file://`, `ftp://`, `mailto:`, scheme-less = not URL mode.

## Workflow

Dispatch → collect → fetch BFS → merge → convert via templates → self-review → save under `planning/[safe-feature-name]--YYYY-MM-DD-HHMMSS/`. Output starts with `# [feature-name]`. 저장은 항상 수행한다. 두 산출물은 기획 레벨에 머무르며 구현·전략 섹션을 만들지 않는다.

## Output Contract

- Save success: header → `## 저장 파일` → `## 체크해야 할 항목`.
- Save failure: both bodies + `## 저장 실패 상세`.
- `planning/**` is never SSOT evidence.

## Requirement IDs

`POL-`(정책 규칙)·`FUNC-`(기능 흐름·동작) 2종만 쓴다. 두 문서는 헤더 `관련 문서`와 inline 참조로 연결하며 별도 ID 컬럼·매트릭스를 만들지 않는다. 다른 prefix(BIZ/RSK/DEC/AC/DATA/API/NFR/TEST)는 쓰지 않는다.

## References

Load on demand by step:

- `references/runtime.md` — dispatch, 입력, URL fetch·connector, 저장, 출력 계약.
- `references/conversion.md` — 이미지·병합·기능명, 템플릿 매핑, 최소 추적성, 제외 추적, 메시지 가이드.
- `references/self-review.md` — 경량 검증 패스(R1-R5)와 AI 검증 제외 규칙.
- `templates/정책서.md` (11섹션), `templates/기능설계서.md` (1-7·10-11, 8·9 결번) — Step 7 변환 시 생성 대상.
