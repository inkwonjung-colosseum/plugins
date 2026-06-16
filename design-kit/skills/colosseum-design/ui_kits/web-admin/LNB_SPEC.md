# LNB (Local Navigation Bar) — Design Detail Spec

Source: Figma `WEB_CDS-2.0` node `8559-30683`, reverse-engineered from shipped reference image at `uploads/pasted-1776659020800-0.png`.

---

## Overall structure

| Property | Value |
|---|---|
| Width | **240px** fixed |
| Height | 100vh |
| Background | `#F6F7F9` (`gray.50` / page base — **not white**) |
| Right border | `1px solid #CACACA` (`gray.200`) |
| Font | Pretendard, 14px base |

The LNB is **the only chrome** — there is no top GNB. All global utilities (user, notifications, center switcher, global search) live inside the LNB.

---

## Vertical stack (top → bottom)

```
┌─────────────────────────────────┐  ─┐
│  [colo logo]  colo AI   [WMS]   │   │ Brand row            (56px tall)
├─────────────────────────────────┤   │
│  Jennifer B. Scott ▼     🔔³    │   │ User row             (40px tall)
├─────────────────────────────────┤   │
│  ╭──────────────────────────╮   │   │
│  │ Current center      ▼    │   │   │ Center selector      (60px tall)
│  │ 🏠 {Center name}         │   │   │
│  ╰──────────────────────────╯   │   │
├─────────────────────────────────┤   │ HEADER
│  ╭──────────────────────────╮   │   │
│  │ 🔍 검색           ⌘ K    │   │   │ Search input         (36px tall)
│  ╰──────────────────────────╯   │   │
├─────────────────────────────────┤   │
│  ╭─────────╮                    │   │
│  │ WH-Admin│                    │   │ Role chip            (28px tall)
│  ╰─────────╯                    │   │
├─────────────────────────────────┤  ─┘
│  title                          │
│  ▣ title                      ▾ │   SCROLL AREA
│    ▉▉▉▉▉▉▉▉▉▉▉ title            │   (flex:1, overflow-y:auto)
│    │  title                     │
│  ▣ title                      ▴ │
│    │  title                     │
│    │  title                     │
│    │  title                     │
│  …                              │
├─────────────────────────────────┤
│                       ⌘ + \ ⇥  │   FOOTER — collapse button
└─────────────────────────────────┘   (right-aligned, 44px tall)
```

---

## Brand row (56px)

- Padding: `14px 16px 10px`.
- Logo asset: `assets/colosseum-logo.svg` (official CI). Rendered at **28px height** to align with ColoAI / WMS badges.
  - Note: the CI logo is the full wordmark "colosseum" — in the LNB Figma frame it is shown as `colo AI` (a shortened brand mark used only for this product). **Use the full `colosseum-logo.svg`** per design instruction; the icon mark is part of that SVG.
- WMS product badge:
  - Size: `48×24`
  - Radius: `4px`
  - Background: `#FE842F`
  - Label: `WMS` · `font-weight: 700` · `font-size: 12px` · `color: #FFFFFF` · letter-spacing `0.02em`
  - Gap from wordmark: `8px`

## User row (40px)

- Padding: `4px 16px 12px`.
- Left: `Jennifer B. Scott` + `▼` (`expand_more`, 16px, `gray.500`). `color: gray.900 #29313D`, `font-weight: 600`, `font-size: 14px`. Click → user menu.
- Right: Bell icon button (`notifications`, 20px, `gray.600 #52627A`). Size `32×32`, radius `6px`.
  - Unread badge: absolute top-right, `#F94949` background, `#FFF` text, `min-width 14px`, `height 14px`, `border-radius 7px`, font `700 9px`.

## Center selector (60px)

- Padding: `0 12px 10px`.
- Card: **dark charcoal `#363637`** (not navy!), radius `8px`, padding `8px 12px 10px`.
- Top row: label `Current center` (white @ 60% alpha, `11px 500`) + `expand_more` icon (white @ 70%, 18px).
- Bottom row: `home` icon (white, 16px) + `{Center name}` (white, `13px 600`).

## Search input (36px)

- Padding: `0 12px 10px`.
- Input height `32px`, radius `6px`, border `1px solid #E0E0E2`, background `#FFF`.
- Leading: `search` icon, 16px, `gray.500 #767676`, at 12px from left edge.
- Trailing: two kbd chips `⌘` `K`, each 18px square, `1px #CACACA` border, radius `3px`, font `500 10px`, color `#767676`, gap `2px`.
- Placeholder: `"검색"` · `500 13px` · `color #767676`.

## Role chip (28px)

- Padding: `0 16px 12px`.
- Chip: inline-flex, height `22px`, padding `0 8px`, radius `4px`.
- Background `#E5F3FF` (sky 50), color `#005BF6` (clblue 500), font `600 12px`.

---

## Navigation tree

### Group title
- Padding `10px 12px 6px`.
- Font `500 12px`, color `#767676`, letter-spacing `0.01em`. Lowercase/Korean as-is, no uppercase transform.

### 1-depth item (collapsible section)
- Height **36px**, padding `0 12px`, radius `6px`.
- Layout: `[icon, 18px] [label, flex:1] [chevron, 18px]`, gap `10px`.
- Font `700 14px`. Icon `gray.600 #52627A`.
- States:

| State | Background | Icon | Label | Chevron |
|---|---|---|---|---|
| default | transparent | `#52627A` | `#29313D` | `#767676` |
| hover | `#D6ECFF` (clblue subtle) | `#005BF6` | `#005BF6` | `#005BF6` |
| has-active-child | transparent | `#005BF6` (FILL 1) | `#005BF6` | `#767676` |

Chevron: `expand_more` when collapsed, `expand_less` (or rotate 180°) when open. `transition: transform 250ms cubic-bezier(0.22, 1, 0.36, 1)` (easeOutQuint — Colosseum standard).

### 2-depth item (leaf)
- Height **32px**, padding `0 12px`, radius `6px`.
- Laid out inside a row that provides the left guide line:

```
[16px indent] [1px guide line] [8px gap] [pill button — flex:1, margin-right 8px]
```

- **Left guide line**: `1px` vertical line, `#E7EAEF`, spans the full height of the group's child list.
- **Selected indicator**: absolute-positioned `3px` wide pill on top of the guide line (same x-position), color `#005BF6`, top/bottom insets `4px`, radius `2px`. Only shown when this leaf is selected.
- Font `500 14px` default / `700 14px` selected. No left icon on leaves (leaf has only a label).
- States:

| State | Background | Label | Trailing action |
|---|---|---|---|
| default | transparent | `#29313D` | — |
| hover | `#E5F3FF` (sky 50) | `#005BF6` | `open_in_new` button (22×22, white bg, `1px #D6ECFF` border, radius `4px`, icon 16px `#005BF6`) |
| selected | `#005BF6` (clblue 500) | `#FFFFFF`, weight 700 | — |
| selected+hover | `#005BF6` | `#FFFFFF` | `open_in_new` button, icon `#FFFFFF` |

Note on "hideBar" variant visible in Figma state table: an `Only Figma` state — **not implemented in code**; it's a Figma-only helper to hide the left guide line while mocking up screens.

---

## Footer (44px)

- Top border: `1px solid #E7EAEF`.
- Padding: `10px`.
- Content: right-aligned. Single button:
  - Height `28px`, padding `0 8px`, radius `6px`, border `1px solid #CACACA`, background `#FFF`.
  - Content: kbd-styled text `⌘ + \` + `dock_to_right` icon (14px, `#767676`).
  - Font `500 11px`, color `#767676`.
  - Click → collapses LNB.

---

## Token mapping

| Usage | Token | Value |
|---|---|---|
| LNB surface | `color.background.secondary` | `#F6F7F9` |
| LNB border | `gray.200` | `#CACACA` |
| Selected background | `clblue.500` | `#005BF6` |
| Hover background (1-depth) | `sky.100` / `clblue.subtle` | `#D6ECFF` |
| Hover background (2-depth) | `sky.50` | `#E5F3FF` |
| Guide line + divider | `gray.100` | `#E7EAEF` |
| Group title / icon muted | `gray.500` | `#767676` |
| Body text | `gray.900` / `natural.800` | `#29313D` |
| Charcoal card (center) | custom (not in DS token set) | `#363637` |
| Notification red | `red.500` | `#F94949` |
| WMS orange badge | custom product-brand | `#FE842F` |

The charcoal card color `#363637` is **not** in the foundation palette — the Figma file introduces it as an LNB-specific accent. Flag for the design-system team to either (a) absorb as a new `gray.900` variant or (b) formally document as "LNB dark card".

---

## Behavior

- **Hover** fires on the 1-depth bar only (not the chevron area alone). Clicking anywhere on the bar toggles open/close.
- **Selection**: only leaf (2-depth) items are selectable. The parent group shows `has-active-child` state (icon turns blue, label stays dark) when one of its children is selected.
- **Scroll**: the nav region is the only scroll surface; the brand/user/center/search/role rows are pinned above it, the footer below it.
- **Collapse** (⌘+\): not visually specified in the provided reference — leave as stubbed button for now.
- **Keyboard**: ⌘K opens global search (no-op in this kit). Arrow keys should walk leaves (not implemented).
