# Craft references (콜로세움)

브랜드 무관 **범용 UI 장인 지식**. 각 파일은 한 차원(타이포·색·모션·상태…)의 조밀한 규칙집.
`colors_and_type.css`가 "어떤 색·폰트인가"를 정하면, craft는 그 위에 "유능한 디자이너가 적용하는
보편 규칙"을 더한다 (예: ALL CAPS는 브랜드와 무관하게 항상 ≥0.06em tracking).

## 3축 구조

| 축 | 범위 | 위치 |
|----|------|------|
| 브랜드(look) | 콜로 토큰·폰트·로고 | `colors_and_type.css`, `assets/` |
| 장인(craft) | 브랜드 무관 보편 규칙 | `references/craft/` (이 폴더) |
| 범위(scope) | 무슨 화면을 만드나 | `references/spec-to-screens.md` |

> open-design은 daemon이 craft를 주입한다. **콜로 design-kit은 daemon이 없으므로**
> `SKILL.md` 워크플로우가 surface type별로 "이 craft를 읽어라"를 명시한다.

## surface type별 로드 (SKILL.md가 지시)

| surface | 로드할 craft |
|---------|-------------|
| admin CRUD (리스트/폼/상세) | typography, color, anti-ai-slop, **state-coverage**, **form-validation**, accessibility-baseline, laws-of-ux |
| 대시보드 | typography, color, anti-ai-slop, state-coverage, accessibility-baseline, laws-of-ux |
| 모바일/PDA 플로우 | typography, color, state-coverage, form-validation, accessibility-baseline, animation-discipline |
| 마케팅/헤로 | typography, typography-hierarchy, color, anti-ai-slop |
| 긴 글/문서 | typography, typography-hierarchy, typography-hierarchy-editorial, color |
| 다국어(JP) 화면 | + rtl-and-bidi |

## 파일

| 파일 | 언제 |
|------|------|
| `typography.md` | 타입 쓰는 모든 화면 (콜로 weight 400/500/700, 600 금지) |
| `typography-hierarchy.md` | 위계가 의도적으로 느껴져야 하는 화면 |
| `typography-hierarchy-editorial.md` | 지속 독서 surface (긴 글/문서) |
| `color.md` | 스타일 있는 모든 화면 (accent ≤2, CL Blue 단일) |
| `anti-ai-slop.md` | AI 티 제거 — 마케팅·랜딩·모든 산출물 |
| `state-coverage.md` | 상태 있는 UI (대시보드/폼/리스트) — **5상태 강제** |
| `form-validation.md` | 폼 있는 화면 (로그인/설정/생성 폼) |
| `animation-discipline.md` | 모션 있는 화면 (콜로 `--ease-out-quint`) |
| `accessibility-baseline.md` | 인터랙티브 UI (포커스/라벨/키보드) |
| `laws-of-ux.md` | 인지 한계 닿는 구성 결정 (가격·대시보드·온보딩) |
| `rtl-and-bidi.md` | 다국어 (JP 발췌; 콜로는 KR/JP/EN) |

## 라이선스

craft 콘텐츠는 MIT 라이선스 [refero_skill](https://github.com/referodesign/refero_skill)
(© Refero Design)에서 open-design이 가공한 것을 콜로용으로 재이식했다. MIT. 상세는 루트 `NOTICE.md`.
