---
name: colosseum-design
description: Use when Colosseum(콜로세움) 브랜드 화면·UI·목업·프로토타입을 만들 때 — CL Blue·Pretendard·Material Symbols 고정 DS로 self-contained HTML. 트리거 — "디자인/UI/화면 만들어줘", "콜로세움 브랜드로". B2B 물류 web-admin·PDA. 브랜드 미정이면 ui-design-intelligence.
user-invocable: true
---

# Colosseum Design System Skill

Read `GUIDE.md` in this folder first — it is the canonical entry point and contains:
- Content fundamentals (voice, tone, casing, microcopy)
- Visual foundations (color, type, density, spacing, borders, radii, shadows, motion, hover/press states)
- Iconography (Material Symbols Outlined, fill / weight / size rules, Figma → code mapping)
- File index

Then explore as needed:

- **`colors_and_type.css`** — canonical tokens: foundation palette (clblue / natural / gray / accents), semantic variables (`--color-background-primary`, `--color-text-heading`, `--color-icon-data`, etc.), typography scale (display / headline / title / subtitle / body / caption), and component utility classes. Always link this first.
- **`fonts/`** — Pretendard Variable + Bold + Black (woff2). Auto-loaded by the CSS.
- **`assets/`** — official CI logo (`colosseum-logo.svg`) and alternate. **Do not** redraw or recolor. Minimum 24px, GNB 32–40px.
- **`preview/`** — design-system review cards: swatches, type specimens, component clusters. Useful as worked examples of how tokens compose.
- **`ui_kits/web-admin/`** — click-thru recreation of the WMS / OMS console. `index.html` is the demo; individual `.jsx` files are composable components (TopBar, Sidebar, StatCard, DataTable, OrderDetailDrawer, Primitives). Copy these as starting points for any web admin surface.
- **`references/craft/`** — 범용 UI 장인 규칙(브랜드 무관): typography·color·anti-ai-slop·**state-coverage**·**form-validation**·accessibility·laws-of-ux·animation·rtl. `references/craft/GUIDE.md`에 surface type별 로드 표. **AI 티·미완성 상태를 막는 핵심 층.**
- **`references/spec-to-screens.md`** — 정책서·기능정의서 → 화면 세트 도출 + 완결성 체크리스트. **리스트 한 장만 만드는 실패를 막는다.**
- **`references/components-admin.md`** — Form·Modal·Drawer·Tab·Tag·Toast·Empty/Loading/Error 패턴(콜로 토큰). UI 킷의 미정의 컴포넌트를 메운다.
- **`examples/wms-zone-console.html`** — admin CRUD 화면 **품질 기준 레퍼런스**(LNB·리스트·생성/수정 슬라이드오버·상태변경 모달·드로어·toast·empty 포함). 새 admin 화면은 이 구조·밀도를 모방한다.
- **`tools/lint.mjs`** — `node tools/lint.mjs <html>`로 산출물 anti-slop/브랜드 자가검사(daemon 없는 환경의 P0 체크).

## How to use this skill

**If creating visual artifacts** (slides, mocks, throwaway prototypes, marketing screens, investor decks):
1. Copy the assets you need out of `assets/` and `fonts/` into the new project.
2. Link `colors_and_type.css` and the Material Symbols CDN at the top of the HTML.
3. Build static HTML (plus inline React + Babel if interactive) following the visual foundations.
4. Match the UI kit components for density — SM is the default (32px height, 14px text).

**If working on production code:**
1. `colors_and_type.css` 토큰을 직접 쓰거나 CSS 변수/Tailwind config로 복사.
2. UI 킷 JSX는 스펙으로만 참조 — 접근성·상태관리는 직접 보강.
3. Material Symbols는 Google Fonts CDN. air-gapped면 같은 `@font-face`로 로컬 호스팅.

## 기능정의서·정책서로 화면 만들 때 (워크플로우 — 반드시 따른다)

정책서/기능정의서/스펙으로 화면을 만들 땐 **리스트 한 장만 뽑지 마라.** 다음 순서로:

1. **화면 세트 도출** — `references/spec-to-screens.md`로 권한 테이블(C/R/U/D)·상태 전이표·생성 규칙·예외 기준을 전수해 필요한 화면·모달 목록을 먼저 만든다 (리스트 + 생성/수정 폼 + 상세 + 상태변경 모달 + 예외 흐름).
2. **craft 로드** — surface type에 맞는 `references/craft/`를 읽는다. admin CRUD = `typography` + `color` + `anti-ai-slop` + `state-coverage` + `form-validation` + `accessibility-baseline` + `laws-of-ux`. (표: `references/craft/GUIDE.md`)
3. **레퍼런스 모방** — `examples/wms-zone-console.html`의 구조·밀도·상태 처리를 기준으로 삼고, `references/components-admin.md`의 Form/Modal/Drawer 패턴을 쓴다. 토큰은 `colors_and_type.css`.
4. **5상태 적용** — 각 리스트/폼/상세에 `state-coverage`의 5상태(loading/empty/error/populated/edge). populated만 그리지 마라.
5. **자가점검** — 산출 전 `spec-to-screens.md`의 완결성 체크리스트 + `anti-ai-slop` P0 통과. 가능하면 `node tools/lint.mjs <html>` 실행.

> 정책서의 `[미확정]`/`(Non-MVP)`는 지어내지 말고 "미정의/추후" 라벨로 명시한다.

## Hard rules — do not violate

- Korean is the primary language. UI copy uses `-세요` polite imperative. No banmal. No emoji in production.
- Default component size is **SM** (32px / 14px / 12px padding). `h-8` not `h-10`.
- Default font weight is **Medium (500)**, not Regular (400). Semibold (600) is not used.
- Primary brand color is `#005BF6` (CL Blue). Never use it as a page background, never add gradients to UI chrome. The only gradient in the system lives inside the logo.
- Icons are **Material Symbols Outlined**, filled only for active / selected state. Icon size is tied to component height (18px for SM).
- Borders are 1px solid `#CACACA` (or 20% black on PDA). Default radius is **6px**. No scale transforms on press.
- PDA (handheld) screens require 44px minimum hit targets, 24px minimum icon size, and one-handed operation (bottom-anchored primary actions).

## If invoked without guidance

사용자에게 묻는다: 무엇을(surface: web admin/PDA/marketing/slides), 어느 시장(KR/JP/US — 패턴 상이), 어느 충실도(sketch/hi-fi/production). 그 뒤 전문 디자이너로서 HTML 또는 프로덕션 코드를 산출한다.

## Known gaps (flag to user if encountered)

- Pretendard JP·슬라이드 템플릿 미동봉 — JP/슬라이드 생성 전 사용자에게 알린다.
- Form/Modal/Drawer/Tab/Tag/Toast/Empty·Loading·Error는 `references/components-admin.md`에 정의. Pagination/Breadcrumb/Dropdown/Skeleton/Avatar는 미정의 — UI 킷 기본값 사용(권위 스펙 아님).
