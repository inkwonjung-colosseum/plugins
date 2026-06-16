> **콜로세움 적응 노트** — 이 파일은 open-design `craft/`(MIT, © Refero Design / refero_skill 가공분)에서 이식했다. 본문의 범용 토큰 예시는 colosseum-design 토큰으로 읽는다:
> `--accent`=`--clblue-500`(#005BF6) · `--bg`=`--color-background-gray-bg`(#F2F2F2) · `--surface`=#fff · `--fg`=`--color-text-data`(#464646) · `--muted`=`--color-text-description`(#767676) · `--border`=`--color-borders-outline`(#CACACA).
> 아이콘=Material Symbols Outlined · 폰트=Pretendard · **weight 600 금지**(콜로룰) · UI 크롬 그라데이션 금지 · 출력 카피는 한국어 `-세요`체.

# Typography craft rules

Universal typography rules that apply on top of any `DESIGN.md`. The
active design system decides *which* fonts; this file decides *how* they
behave at every size.

> Adapted from [refero_skill](https://github.com/referodesign/refero_skill)
> (MIT) — distilled and re-tuned for Open Design's token system.

## Type scale

Use a multiplicative scale (1.2 or 1.25). Cap at 6–8 sizes per artifact.

| Role | 콜로 (px) | 토큰 |
|---|---|---|
| Display | 40 (드물게) | `--font-size-6xl` |
| H1 | 28–32 | `--font-size-4xl`/`5xl` |
| H2 | 24 | `--font-size-3xl` |
| H3 | 20–22 | `--font-size-xl`/`2xl` |
| Body | **14 (기본)** – 16 | `--font-size-sm`/`base` |
| Small | 13–14 | `--font-size-sm` |
| Caption | 12 | `--font-size-xs` |

> 콜로는 엔터프라이즈 고밀도 UI라 Display(40px+)는 마케팅·헤로에만. admin 화면 기본 본문은 **14px**.

## Line height (leading)

| Text size | Line height |
|---|---|
| Display / H1 (≥32 px) | `1.0`–`1.2` (tight) |
| Body (15–18 px) | `1.5`–`1.6` |
| Small (≤14 px) | `1.5` |

## Letter-spacing — the rule that makes or breaks craft

This is the single most-skipped rule in AI-generated design. **No
exceptions.**

| Context | Letter-spacing |
|---|---|
| Body text (14–18 px) | `0` (default) |
| Small text (11–13 px) | `0.01em` to `0.02em` (positive) |
| UI labels and button text | `0.02em` |
| **ALL CAPS** | **`0.06em` to `0.1em` (required)** |
| Headings 32 px+ | `-0.01em` to `-0.02em` |
| Display 48 px+ | `-0.02em` to `-0.03em` |

ALL CAPS without positive tracking looks cramped and amateur. Display
text without negative tracking looks loose and weak. These two failures
are the most reliable AI-slop tells.

The `0.06em` floor is not arbitrary: it is the empirical lower bound
that print and web typographers have converged on for uppercase
tracking (cf. Bringhurst's *Elements of Typographic Style* §3.2.7,
which recommends 5–10% of the em for caps; modern screen practice
rounds the lower end to 0.06em). Anything tighter and the counters
collide on screen; the upper bound `0.1em` keeps the word from
disintegrating into letters.

## Font pairing

- Maximum 2 typefaces per artifact (display + body, or one variable face
  used at multiple weights).
- Always declare a system fallback chain. If the active `DESIGN.md`
  ships a webfont URL, the fallback must still produce a coherent look.
- Never set `font-family: system-ui` alone on a heading — that is the
  textbook AI default; always pair it with an intentional first choice.

## Line length

Limit body copy to **50–75 characters** per line. In CSS:
`max-width: 65ch` is a safe default.

## Three-weight system (콜로세움)

콜로세움은 Pretendard로 정확히 3 weight만 쓴다. **600은 사용하지 않는다.**
- **Read** (400, Regular) — 보조 본문·캡션
- **Emphasize** (500, Medium) — 기본 본문·UI 라벨·내비게이션 (**콜로 기본 weight**)
- **Announce** (700, Bold) — 제목·강조·버튼 (600을 건너뛴다)

500이 기본값이다. 400은 약화, 700은 강조. 그 사이(600)는 쓰지 않는다.

## Common mistakes (lint these)

- ALL CAPS without `letter-spacing` ≥ `0.06em`.
- Display text (≥32 px) without negative tracking.
- More than 3 type sizes visible above the fold.
- Mixed serif and slab on the same screen without a clear role split.
- Body copy in `text-align: justify` (creates rivers; never use on the web).
