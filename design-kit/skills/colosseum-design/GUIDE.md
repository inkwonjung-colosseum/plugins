# Colosseum Design System 2.0

> **Korean / English bilingual system.** Enterprise B2B logistics platform built by Colosseum Corporation (콜로세움코퍼레이션). Covers WMS (Warehouse Management), TMS (Transportation Management), OMS (Order Management), and PMS (Parcel Management).

This design system supports Colosseum's core business model — a volume-brokerage platform where **FD (Field Directors)** operate partner warehouses on behalf of shippers. The system is optimized for three deeply specific environments:

1. **Web / Desktop admin** — shippers, operations managers, FDs reviewing data.
2. **PDA / handheld** — warehouse workers with gloves on, standing, one-handed.
3. **Multi-region** — Korea, US (CCPA), Japan (Pretendard JP, Daiwa Corporation feedback loop).

Primary language: Korean. UI copy is Korean-first, with JP + EN as secondary.

---

## Sources

- **`Design_system/`** (local codebase, read-only) — full design-system specification:
  - `DS_01_Philosophy.md` — principles, 3-second rule, one-hand operation, 44px targets
  - `DS_02_Token_Foundation.md` — color palette, typography, spacing, radius, shadow
  - `DS_03_Semantic_Tokens.md` — background/text/icon/border semantic mapping
  - `DS_04_Component_Tokens.md` — Button, Input, Tag, Toast, Card token tables
  - `DS_05_Component_Specs.md` — sizes (XS / **SM default** / MD / LG / XL), CSS
  - `DS_06_UX_Policy.md` — Empty-State-First, PDA rules, region-specific patterns
  - `DS_07_Development.md` — anti-patterns, Tailwind mapping, accessibility
  - `DS_08_Brand_and_Gaps.md` — logo rules, known gaps (Table, Modal, Nav still TBD)
  - `DS_09_Icon_Convention.md` — Material Symbols Outlined as official icon system
  - `2.0/foundation.json`, `semantic-token.json`, `component_token.json` — raw tokens
  - `2.0/tailwind.config.js`, `2.0/Button.jsx`, `2.0/Input.jsx` — reference code
  - `2.0/colosseum-original-logo.svg` — canonical logo
- **`uploads/`** — `PretendardVariable.woff2`, `Pretendard-Bold.woff2`, `Pretendard-Black.woff2`, `colosseum_ci.svg` (official CI)

---

## CONTENT FUNDAMENTALS

**Language.** Korean-first. All UI labels, error messages, and instructions are written in Korean. JP is secondary with Pretendard JP; EN is technical / regional. Tone switches per market: Korea expects speed + density, US expects explicit user action (Empty-State-First), Japan expects "현장 친화적이고 직관적인" warmth (field-friendly + intuitive).

**Voice.** Imperative, location-first, positive-framed. The system speaks to operators under time pressure.

- **Location before action.** "어디로 갈지" precedes "무엇을 할지." E.g. *"A-02 구역으로 이동하세요"* (Go to zone A-02) comes before *"5개 피킹"* (Pick 5 items).
- **Positive reframing of errors.** Not "No data" → instead *"검색 조건을 입력하세요"* (Enter search criteria). Error messages describe the recovery, not the failure: *"유효한 이메일을 입력하세요"* (Please enter a valid email).
- **Formal polite "-세요" ending.** Uses `-하세요` / `-세요` (polite imperative), never banmal. No "you vs I" distinction — Korean drops the subject. English translations use "you" naturally.
- **No emoji in production UI.** Emoji appear only in internal design docs as markers (🔴 🟡 🟢 for priority, ⭐ for defaults, ⚠️ for warnings, ✅ / ❌ for do/don't). Production UI uses Material Symbols, not emoji.
- **Number-led status labels.** Logistics statuses are short nouns: 신규 / 처리중 / 출고대기 / 출고완료 / 배송중 / 반품요청 / 취소. Each maps 1:1 to a Tag variant (Positive, Warning, Safe, Danger, etc.).
- **3-second rule.** Any screen must communicate its core info within 3 seconds. Dense, scannable, high-contrast.

**Casing.** Korean has no case. English used in the system is **lowercase for tokens** (`clblue.500`, `color.background.primary`) and **Title Case for UI labels** (`Primary`, `Outline`, `Destructive`). Abbreviations stay ALL-CAPS (WMS, TMS, FD, PDA, SKU, GNB).

**Microcopy examples.**
- Button: `저장` / `취소` / `검색` / `필터` — one or two syllables.
- Empty-state CTA: `검색 조건을 입력하세요` → primary action: `검색`.
- Destructive confirm: `삭제하시겠습니까?` (Do you want to delete?) not "Are you sure?"
- Success toast: `저장되었습니다` (Saved) — past tense, confirmation.
- PDA scan success: `스캔 완료` (Scan complete) + audible tone + color flash.

---

## VISUAL FOUNDATIONS

**The mood.** Enterprise, high-density, technical. Think Bloomberg Terminal meets a warehouse floor. Fast, quiet, legible under bright fluorescent lights. Not playful, not friendly in a consumer way — **friendly in a "this will not get me in trouble at 2am" way**.

**Color.**
- **CL Blue #005BF6** is the single brand primary. Used sparingly: CTA, active tab, selected row, selected icon. Never as page background.
- **Natural (warm gray)** for titles and headings — `natural.700 #3e4a5c`.
- **Gray (neutral gray)** for body text and dividers — `gray.700 #464646` for body, `gray.200 #CACACA` for 1px borders. Gray scale is **contrast-calibrated** — gray.500 is the AA cutoff, gray.700 is AAA.
- **Accent colors map to logistics states**, not decoration: Red=Danger/Cancel, Orange=Negative/Return, Yellow=Warning/Pending, Green=Safe/Complete, Sky=Info/In-transit, Purple=Stable/Special, Pink=Highlight. Every accent has a Subtle (tinted bg) and Solid (PDA, high-contrast) pair.
- **No gradients on UI chrome.** The only gradient in the system is inside the logo itself (clblue 600 → 800).

**Type.** Pretendard (Variable). Korean-optimized but excellent Latin + JP coverage. Default body is **14px / 500 weight** — note the default is **Medium, not Regular** (400 failed field-visibility tests under warehouse lighting). Headings are 700 Bold. **600 Semibold is explicitly not used** — fragmentation control. Letter-spacing is 0 across the board (no tracking adjustments).

**Density.** Component default is the **SM size** — 32px height, 14px text, 12px horizontal padding. This is the *base*, not a compact variant. Most B2B systems call this "Small"; Colosseum calls it default because warehouse/ops screens are information-dense.

**Spacing.** 4px base grid. `spacing.3` (12px) and `spacing.4` (16px) do 80% of the work.

**Background.** `gray.50 #F2F2F2` is the page base. Cards and inputs are white. No textures, no patterns, no photographic backgrounds in the admin UI. Only the login / marketing surfaces use photographic imagery.

**Borders.** 1px solid `gray.200 #CACACA` is default. **PDA-specific rule**: in the field, borders use `rgba(0,0,0,0.2)` (20% black) instead of solid gray — reduces visual fatigue under bright light.

**Radius.** **6px is the default for buttons and cards.** 4px for inputs. 2px for chips. 8px for modals. Full-radius (9999px) only for avatars and dot indicators. The 6px default is deliberately firm (not soft/playful).

**Shadows.** Tailwind-standard elevation scale. `shadow.base` for cards, `shadow.md` for dropdowns, `shadow.lg` for modals, `shadow.2xl` for overlays. **Shadows are subtle** — max 25% opacity even on the heaviest. No colored shadows, no glows.

**Transparency / blur.** Used only for overlays: `opacity-bk78` (78% black) for snackbars, `opacity-wt90` (90% white) for light tooltips on dark UI. No frosted-glass effects.

**Animation.** Minimal. **All interactive transitions use `easeOutQuint` = `cubic-bezier(0.22, 1, 0.36, 1)`** — Colosseum's single standard easing. Durations are tokenized: `--duration-fast` 150ms (micro — chip, toast), `--duration-base` 250ms (default — hover, focus, tab change, chevron rotate), `--duration-slow` 400ms (progress bar, modal enter). No bounces, no spring physics, no stagger. **Motion should not slow down a shift worker.** Respect `prefers-reduced-motion`.worker.**

**Hover / press states.**
- Primary button: hover darkens to `clblue.600 #044ECE`, press to `clblue.700 #0742A7`. No scale change.
- Outline/Text/Secondary: hover adds `opacity-bk4` or `opacity-bk12` black tint. No color shift.
- Cards: hover border → primary + background → `sky.50`. No lift.
- No press-shrink (active:scale-95) anywhere — alien to the system.

**Focus.** Single shared ring: `2px solid rgba(57, 195, 239, 0.7)` with 2px offset. Keyboard-only (`:focus-visible`), never on mouse click.

**Layout rules.**
- GNB (Global Nav): fixed top, logo 32-40px height anchored left, clickable → home.
- LNB (Local Nav): fixed left sidebar on desktop.
- 12-column grid intended but not formally specified (known gap in DS_08).
- Content max-width handled at the page level, not globally.
- **Empty State First** is a layout constraint, not just a state — tables render empty by default in US-region deployments.

**Imagery tone.** Warm whites and true blues when present. No stock photography in admin UI. Logistics illustrations (when they appear, e.g. empty states) should be flat line style, single color, minimal — think Material Symbols scaled up, not decorative illustrations.

---

## ICONOGRAPHY

**Official icon system: Google Material Symbols — Outlined variant.**

**Why:** ~60% 1:1 naming match with Colosseum's Figma file, 2,500+ icons cover the logistics domain, variable-font axes (weight / grade / fill / optical size), Apache 2.0 licensed.

**Delivery:** CDN via Google Fonts (no local icon font file required, no sprite). Loaded in every surface with:

```html
<link rel="stylesheet"
  href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
```

**Usage pattern — HTML:**
```html
<span class="material-symbols-outlined" style="font-size:18px;">dashboard</span>
```

**Usage pattern — React:**
```tsx
<span className="material-symbols-outlined" style={{ fontSize: 18 }}>warehouse</span>
```

**Fill rule.** Outlined (`FILL: 0`) is the default for all UI. Filled (`FILL: 1`) is reserved for **selected / active states** — e.g. an active nav item, a selected tab.

**Weight.** 400 default, 500 for emphasis (headers, active), 300 for disabled.

**Size scale** (tied to component heights):
| Use | Icon | Component height |
|---|---|---|
| XS (compact) | 16px | 24px |
| **SM (default)** | **18px** | **32px** |
| MD (emphasis) | 20px | 40px |
| LG (large) | 24px | 48px |
| XL (hero) | 24px | 56px |
| PDA minimum | 24px | — |

**Color.** Uses the icon semantic tokens from `colors_and_type.css`: `--color-icon-static` / `-data` / `-primary` / `-disabled` / `-white`, plus status colors red/orange/yellow/green/sky/clblue/purple.

**Figma → code mapping.** The Figma file uses `data-name` attributes on vector nodes; DS_09 specifies a three-step fallback: exact match → custom mapping table → closest Material Symbol + code comment. Key custom mappings:

| Figma `data-name` | Material Symbol |
|---|---|
| `chevron_down` | `expand_more` |
| `chevron_up` | `expand_less` |
| `deployed` | `package_2` |
| `inventory_line` | `inventory_2` |
| `inbound` | `move_to_inbox` |
| `outbound` | `outbox` |
| `description_line` | `description` |

**Logistics-domain icons** (recommended): `qr_code_scanner` (barcode), `shopping_basket` (picking), `package` (packing), `location_on` (location), `pallet`, `assignment_return` (return), `forklift`, `shelves`, `warehouse`.

**Emoji:** **Not used in production UI.** Emoji appear only in internal design documentation as markers (🔴 🟡 🟢 ⭐ ⚠️ ✅ ❌). All UI status indicators use Material Symbols or colored Tag components.

**Unicode chars as icons:** Not used. No `→` / `×` / `✓` in text — always wrap in a Material Symbol.

**Custom SVGs:** Only when Material Symbols has no suitable match. Canvas 24×24 with 2px padding, 2px stroke, 2px corner rounding, `currentColor` fill, `viewBox="0 0 24 24"`. Stored in `Design_system/2.0/icons/custom/` with `snake_case.svg` names.

**Brand logo:**
- Canonical: `assets/colosseum-logo.svg` (CI, 280×44, pure black wordmark + 3-tone blue icon).
- Alternate: `assets/colosseum-logo-original.svg` (175×48, from Design_system/2.0).
- **Never modify** proportion, color, or surrounding elements. Minimum 24px height. GNB 32–40px. Login max 120px.

---

## File Index

```
/
├── GUIDE.md                         this file (canonical entry)
├── SKILL.md                         Agent Skills-compatible entry point
├── colors_and_type.css              ⭐ ALL tokens + typography classes (link this)
├── fonts/
│   ├── PretendardVariable.woff2
│   ├── Pretendard-Bold.woff2
│   └── Pretendard-Black.woff2
├── assets/
│   ├── colosseum-logo.svg           official CI (primary)
│   └── colosseum-logo-original.svg  alternate wordmark
├── preview/                         design-system review cards (swatches, specimens)
├── ui_kits/
│   └── web-admin/                   WMS/TMS/OMS/PMS web console UI kit
│       ├── GUIDE.md
│       ├── index.html               interactive demo
│       └── *.jsx                    individual components
└── slides/                          (none — no slide template was provided)
```

**Link order for new artifacts:**
1. `<link rel="stylesheet" href="colors_and_type.css">`
2. Material Symbols CDN (see Iconography section)
3. Pretendard is auto-loaded by the CSS file (from `fonts/`).

---

## Caveats

- **Pretendard only** is provided. Pretendard JP (required for Japanese market per DS_06 §12.3) is **not included**. Flag to user if generating JP interfaces.
- **Iconography uses Material Symbols from the Google Fonts CDN** — not bundled as a local asset. Requires internet access at runtime.
- **Missing-by-spec components** (from DS_08): Table/DataGrid, Modal, Tab, Pagination, Breadcrumb, Dropdown Menu, Skeleton, Avatar are **not formally tokenized** — our UI kit provides reasonable implementations consistent with the defined tokens, but they are not authoritative.
- **No slide template was provided**, so `slides/` is not generated.
