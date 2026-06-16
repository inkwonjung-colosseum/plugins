> **콜로세움 적응 노트** — 이 파일은 open-design `craft/`(MIT, © Refero Design / refero_skill 가공분)에서 이식했다. 본문의 범용 토큰 예시는 colosseum-design 토큰으로 읽는다:
> `--accent`=`--clblue-500`(#005BF6) · `--bg`=`--color-background-gray-bg`(#F2F2F2) · `--surface`=#fff · `--fg`=`--color-text-data`(#464646) · `--muted`=`--color-text-description`(#767676) · `--border`=`--color-borders-outline`(#CACACA).
> 아이콘=Material Symbols Outlined · 폰트=Pretendard · **weight 600 금지**(콜로룰) · UI 크롬 그라데이션 금지 · 출력 카피는 한국어 `-세요`체.

# Color craft rules

Universal color rules applied on top of the active `DESIGN.md`. The
design system supplies the palette tokens; this file enforces how to
*use* them.

> Adapted from [refero_skill](https://github.com/referodesign/refero_skill)
> (MIT). All examples reference Open Design's standard tokens
> (`--bg`, `--surface`, `--fg`, `--muted`, `--border`, `--accent`).

## Palette structure

A coherent palette has four layers. Plan all four before writing any CSS.

| Layer | Share of pixels | 콜로 토큰 |
|---|---|---|
| **Neutrals** | 70–90% | gray/natural scale, `--color-background-*`, `--color-text-*`, `--color-borders-outline` |
| **Accent** (하나) | 5–10% | **`--clblue-500`(#005BF6) 단일** — 두 번째 accent 만들지 마라 |
| **Semantic** | 0–5% | `--green-500`/`--yellow-500`/`--red-500`/`--sky-400` (Tag variant: 성공/경고/위험/정보) |
| **Effect** | 0% | 그라데이션·글로우 — 콜로 UI 크롬엔 쓰지 않는다(로고만 예외) |

## Accent discipline

The single biggest readability failure in AI-generated UIs is accent
overuse. Hard caps:

- **At most 2 visible uses of `--accent` per screen.** Typical pair:
  one eyebrow / chip + one primary CTA. Or one accent card + one tab
  pill. Pick a pair, not a flood.
- Links count as accent; demote to `--fg` underline if you also have a
  CTA on the same screen.
- Hover/focus rings count as accent. Ration accordingly.

## Contrast minimums

Run these as gates, not goals:

| Pair | Minimum |
|---|---|
| Body text (≤16 px) on background | **4.5:1** |
| Large text (>18 px or 14 px bold) | **3:1** |
| UI components against adjacent surfaces | **3:1** |

When the brand color clashes (low-contrast indigo on light background is
common), darken the accent to a `600`-level shade for text use; reserve
the brand-bright variant for fills only.

## Light / Dark (콜로는 light-first)

콜로 admin은 light 단일이 기본. 순수 흑/백은 피한다(눈부심·진동).

| Token | Light (콜로 기본) | Dark (예외 시) |
|---|---|---|
| Background | `#F2F2F2`/`#f6f7f9` (not `#fff`) | `#15191f`(natural-900, not `#000`) |
| Foreground | `#1A1A1A`(gray-900, not 순수 `#000`) | `#f0f0f0` (not `#fff`) |

On dark surfaces, prefer **semi-transparent white borders** over solid
dark borders — a 1px `rgba(255,255,255,0.08)` reads as structure
without adding visual noise.

## Semantic color naming (콜로 2계층)

콜로는 **foundation(색조 이름) → semantic(용도 이름)** 2계층이다.
- foundation: `--clblue-500`, `--green-500` — 팔레트 정의용
- semantic: `--color-text-primary`, `--color-background-primary`, `--color-borders-outline` — 사용용

UI에서는 **semantic 토큰을 쓴다.** foundation/raw hex를 직접 쓰면 테마·중앙관리가 막힌다.

```css
/* good — semantic 사용 */
color: var(--color-text-primary);
border-color: var(--color-borders-outline);

/* bad — raw hex / foundation 직접 노출 */
color: #005BF6;
```

## Anti-defaults

- **Indigo `#6366f1`** (Tailwind `indigo-500`) is the most reliable
  AI-slop tell. The active `DESIGN.md` provides `--accent`; use it. If
  the brief truly needs indigo, make the user say so explicitly. If
  your `DESIGN.md` encodes indigo as `--accent`, that is intentional —
  the linter only flags hardcoded hex, so `var(--accent)` uses are
  unaffected even when the resolved color happens to be `#6366f1`.
- **Two-stop "trust" gradient** (purple → blue, blue → cyan, etc.) on a
  hero is the second most reliable tell. A flat surface + one
  type-driven hierarchy beats it every time.
- **Decorative gradients with no functional purpose**. Gradients should
  separate hierarchies (header → body, primary CTA → secondary), not
  decorate empty space.
