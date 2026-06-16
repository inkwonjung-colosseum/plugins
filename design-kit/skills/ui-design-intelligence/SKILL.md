---
name: ui-design-intelligence
description: Use when 브랜드 미정(비콜로세움) 범용 UI·웹·앱 스타일·색·폰트·차트·UX를 데이터로 고를 때. 트리거 — "색/폰트 추천", "스타일 추천", "차트/랜딩 추천", "UX 점검". 84 스타일·160 팔레트·73 폰트·25 차트·98 UX CSV를 Grep 조회(Python 불필요). 콜로면 colosseum-design.
user-invocable: true
---

# UI Design Intelligence (브랜드 무관 범용)

제품 유형·톤·산업을 입력하면 **스타일 / 색 팔레트 / 폰트 페어링 / 랜딩 구조 / 차트 / UX 규칙**을 데이터로 추천하는 범용 디자인 지능. ui-ux-pro-max(MIT)의 지식 DB를 가져와 **콜로 zero-config 철학에 맞게 Python 엔진 없이** 동봉 CSV + Grep/Read로 조회한다.

## ⚠️ colosseum-design과의 경계 (먼저 읽어라)

| 상황 | 쓸 skill |
|------|---------|
| **콜로세움 브랜드** 화면·목업·프로토타입 (CL Blue·Pretendard·Material Symbols 고정) | **`colosseum-design`** |
| 브랜드 미정·외부 클라이언트·throwaway·스타일/색/폰트를 **고르는 일**이 본질 | **이 skill** |

- 이 skill은 **색·폰트·스타일을 추천**한다 → 콜로세움 단일 브랜드 lock과 정면 충돌. **콜로 작업엔 절대 쓰지 마라.**
- 둘을 섞지 마라. 콜로 화면 = colosseum-design 토큰만. 범용 탐색 = 이 skill.
- 모호하면 사용자에게 물어라: "콜로세움 브랜드입니까, 아니면 자유 디자인입니까?"

## 데이터 (Grep/Read 조회 대상)

`data/`에 CSV 10종. **Python·BM25 엔진은 가져오지 않았다.** 원본은 `search.py`가 BM25로 랭킹했지만, 여기선 **Claude가 Grep으로 후보를 좁히고 Read로 행을 읽어 직접 추론**한다.

| CSV | 행 | 무엇 | 핵심 컬럼 |
|-----|----|------|----------|
| `styles.csv` | 84 | UI 스타일(minimalism·glassmorphism·brutalism…) | Style Category, Keywords, Best For, Effects & Animation, Light/Dark Mode |
| `colors.csv` | 160 | 제품유형별 색 팔레트(shadcn 토큰 형식) | Product Type, Primary, Secondary, Accent, Background, Foreground, Destructive, Ring, Notes |
| `typography.csv` | 73 | 폰트 페어링(heading+body) | Font Pairing Name, Heading Font, Body Font, Mood/Style Keywords, Best For, Google Fonts URL, CSS Import |
| `google-fonts.csv` | 1923 | 개별 구글폰트 메타 | Family, Category, Classifications, Keywords, Subsets, Variable Axes, Popularity Rank |
| `ux-guidelines.csv` | 98 | UX 규칙(do/don't + 코드 예시) | Category, Issue, Platform, Do, Don't, Code Example Good/Bad, Severity |
| `charts.csv` | 25 | 차트 유형 선택 가이드 | Data Type, Best Chart Type, When to Use, When NOT to Use, Color Guidance, Library Recommendation |
| `products.csv` | 161 | 제품유형 → 스타일/팔레트/패턴 추천 | Product Type, Keywords, Primary Style Recommendation, Landing Page Pattern, Color Palette Focus |
| `landing.csv` | 34 | 랜딩 구조·CTA·전환 패턴 | Pattern Name, Keywords, Section Order, Primary CTA Placement, Conversion Optimization |
| `icons.csv` | 104 | 아이콘 추천(Lucide/Heroicons) | Category, Icon Name, Library, Import Code, Best For |
| `ui-reasoning.csv` | 161 | 제품 카테고리별 추론 룰(원본 생성기의 두뇌) | UI_Category, Recommended_Pattern, Style_Priority, Color_Mood, Typography_Mood, Anti_Patterns, Severity |

조회 문법·컬럼 전체·예시는 **`references/query-guide.md`** 참조.

## 워크플로우 (search.py 대체)

원본 `--design-system` 파이프라인을 grep으로 재현한다:

1. **제품 카테고리 파악** — `products.csv`에서 사용자 제품유형/키워드를 grep. (예: `grep -i "fintech\|crypto" data/products.csv`)
2. **추론 룰 적용** — `ui-reasoning.csv`에서 해당 UI_Category 행을 읽어 `Style_Priority`·`Color_Mood`·`Anti_Patterns`를 얻는다.
3. **각 차원 후보 선택**:
   - 스타일 → `styles.csv` (Style_Priority 키워드로 grep)
   - 색 → `colors.csv` (Product Type으로 grep)
   - 폰트 → `typography.csv` (Mood로 grep), 더 깊으면 `google-fonts.csv`
   - 랜딩 → `landing.csv`, 차트 → `charts.csv`
4. **조립** — 패턴 + 스타일 + 색토큰 + 폰트 + 효과 + anti-pattern을 하나의 design system으로 요약.
5. **적용** — 그 토큰으로 HTML/JSX/CSS 산출. 색은 CSS 변수(`--color-primary` 등)로 매핑.

> grep으로 0건이면 키워드를 바꿔 재시도(예: `playful neon` → `vibrant dark`). BM25 정밀 랭킹은 없으니 **여러 후보를 읽고 Claude가 판단**한다.

## UX 점검 (코드 리뷰 시)

기존 UI를 점검할 땐 `ux-guidelines.csv`를 Category로 grep:
`grep -i "accessibility\|touch\|animation\|navigation" data/ux-guidelines.csv` → Do/Don't + Severity로 지적.
Category 분류: Accessibility, Touch & Interaction, Performance, Style Selection, Layout & Responsive, Typography & Color, Animation, Forms & Feedback, Navigation, Charts & Data.

## 출력 규칙

- **스타일/색/폰트는 추천값**이다. 사용자 확정 전엔 "후보"로 제시.
- 색은 raw hex가 아니라 **semantic CSS 변수**로 매핑(`--color-primary`, `--color-accent`, `--color-destructive`…).
- 아이콘은 **SVG(Lucide/Heroicons)** — 이모지 금지. (콜로와 달리 Material Symbols 고정 아님.)
- 폰트는 Google Fonts CDN `CSS Import` 행을 그대로 링크.
- anti-pattern(`ui-reasoning.csv` / `ux-guidelines.csv`)을 산출 전 자가점검.

## 안 가져온 것 (의도적)

- **Python BM25 검색 엔진**(`search.py`/`core.py`/`design_system.py`) — zero-config 유지 위해 제외. grep으로 대체.
- **stack CSV**(react/vue/swiftui 등 16종), `react-performance`·`app-interface` — 필요해지면 추후 동봉.
- 원본의 `--persist` MASTER.md 생성기 — 필요하면 design system 요약을 직접 md로 저장하면 된다.

## 라이선스

데이터(CSV)·UX 규칙·추론 룰은 MIT [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)(© Next Level Builder)에서 가져왔다. 상세는 루트 `NOTICE.md` §5.
