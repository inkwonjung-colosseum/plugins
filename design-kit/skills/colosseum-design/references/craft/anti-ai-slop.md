> **콜로세움 적응 노트** — 이 파일은 open-design `craft/`(MIT, © Refero Design / refero_skill 가공분)에서 이식했다. 본문의 범용 토큰 예시는 colosseum-design 토큰으로 읽는다:
> `--accent`=`--clblue-500`(#005BF6) · `--bg`=`--color-background-gray-bg`(#F2F2F2) · `--surface`=#fff · `--fg`=`--color-text-data`(#464646) · `--muted`=`--color-text-description`(#767676) · `--border`=`--color-borders-outline`(#CACACA).
> 아이콘=Material Symbols Outlined · 폰트=Pretendard · **weight 600 금지**(콜로룰) · UI 크롬 그라데이션 금지 · 출력 카피는 한국어 `-세요`체.

# Anti-AI-slop rules

Concrete, checkable rules that distinguish "designed by a human who has
shipped product" from "default LLM output." Several rules below are
auto-enforced by the daemon's `lint-artifact` linter — failing an
enforced rule is not a style preference, it is a regression. The
rest are guidance for agents and reviewers and are flagged inline as
"(guidance, not auto-checked)" so the contract with the linter stays
honest.

> Adapted from [refero_skill](https://github.com/referodesign/refero_skill)
> (MIT), tightened to match Open Design's lint surface.

## The seven cardinal sins

These are the patterns the linter blocks at P0 (must-fix):

1. **임의 hex accent — CL Blue 토큰을 안 씀** — Tailwind indigo(`#6366f1`,
   `#4f46e5`, `#8b5cf6`, `#7c3aed` 등)는 물론, 콜로 브랜드 외 임의 파랑/보라.
   콜로 accent는 **`#005BF6`(CL Blue) 단일**. `var(--clblue-500)` 또는 semantic
   토큰을 쓰고, 하드코딩 hex로 다른 색을 accent로 쓰지 마라.
2. **그라데이션 (UI 크롬)** — purple→blue 류 2-stop "trust" 그라데이션, mesh.
   콜로는 **UI 크롬에 그라데이션 금지**(로고만 예외). 단색 표면 + 타입 위계로 푼다.
3. **이모지를 아이콘으로** — `✨`, `🚀`, `🎯`, `⚡`, `🔥`, `💡`를
   `<h*>`, `<button>`, `<li>`, `class*="icon"`에. 콜로는 **프로덕션 UI 이모지 금지** —
   **Material Symbols Outlined**(Google Fonts CDN)를 `currentColor`로 쓴다.
4. **Pretendard 외 폰트 / system-ui 단독** — 제목·본문 모두 Pretendard. 하드코딩
   Inter / Roboto / `system-ui` 단독 금지. 콜로는 **serif를 쓰지 않는다**(위계는 크기·weight로).
5. **Rounded card with a colored left-border accent** — the canonical
   "AI dashboard tile" shape. Drop either the radius or the left
   border.
6. **Invented metrics** — "10× faster", "99.9% uptime", "3× more
   productive". Either pull from a real source or use a labelled
   placeholder.
7. **Filler copy** — `lorem ipsum`, `feature one / two / three`,
   `placeholder text`, `sample content`. An empty section is a design
   problem to solve with composition, not by inventing words.

## Soft tells (P1 — should fix)

- **Standard "Hero → Features → Pricing → FAQ → CTA" sequence with no
  variation** *(guidance, not auto-checked)*. This is the AI-template
  skeleton; introduce at least one unconventional section (testimonial
  wall as full-bleed quote, pricing as comparison-against-status-quo,
  an inline mini-product-demo).
- **External placeholder image CDNs** (`unsplash.com`, `placehold.co`,
  `placekitten.com`, `picsum.photos`). Fragile and obvious. 콜로는 중성 회색
  플레이스홀더 박스(`background:var(--gray-100)`) + Material Symbols 아이콘으로 대체.
- **More than ~12 raw hex values outside `:root`.** colors_and_type.css 토큰을
  안 쓴 것. CSS 변수(`var(--color-...)`)로 참조하라.
- **CL Blue(`#005BF6` / `var(--clblue-500)`)가 화면당 6회 이상.** 화면당 2회로
  제한(eyebrow/chip 1 + primary CTA 1 같은 페어).

## Polish tells (P2 — nice to fix)

- **Sections without `data-od-id`** — comment mode can't target them.
- **Decorative blob / wave SVG backgrounds** *(guidance, not
  auto-checked)* — meaningless geometry.
- **Perfect symmetric layout with no visual tension** *(guidance, not
  auto-checked)* — alternating density (one tight section, one
  breathing section) reads as intentional.

## How to add soul without breaking the rules

Aim for **~80% proven patterns + ~20% distinctive choice**. The 20%
should live in:

- One bold visual move — a typography choice, a single color decision,
  an unexpected proportion.
- Voice and microcopy — a button that says "Start tracking" beats one
  that says "Get started".
- One micro-interaction the user will remember — a button press that
  moves 2px, a number that counts up.
- One detail that could only have been put there by someone who used
  the product (a subtle kbd shortcut hint, a status badge with
  product-specific phrasing).

If a reviewer screenshots the artifact and someone outside the project
can identify which product it's from — you have soul. If not, you
shipped a template.
