# Query Guide — Python 없이 CSV 조회하기

원본 ui-ux-pro-max는 `search.py`가 BM25로 CSV를 랭킹했다. 이 skill은 **엔진을 안 가져왔다.**
대신 **Grep으로 후보 행을 좁히고 Read로 전체 행을 읽어** Claude가 직접 추론한다.

> 모든 경로는 skill 루트 기준 `data/<name>.csv`.
> grep은 대소문자 무시(`-i`) + OR(`\|`)를 적극 쓴다. 0건이면 키워드를 바꿔 재시도.

---

## 1. 제품유형 → 추천 (시작점)

**`products.csv`** — `No, Product Type, Keywords, Primary Style Recommendation, Secondary Styles, Landing Page Pattern, Dashboard Style, Color Palette Focus, Key Considerations`

```bash
grep -i "fintech\|crypto\|trading" data/products.csv
# → 1,SaaS (General),"app, b2b...",Glassmorphism + Flat Design,...,Hero + Features + CTA,...,Trust blue + accent contrast,...
```

여기서 `Primary Style Recommendation`·`Color Palette Focus`·`Landing Page Pattern`을 다음 단계 키워드로 쓴다.

## 2. 추론 룰 (생성기의 두뇌)

**`ui-reasoning.csv`** — `No, UI_Category, Recommended_Pattern, Style_Priority, Color_Mood, Typography_Mood, Key_Effects, Decision_Rules, Anti_Patterns, Severity`

```bash
grep -i "saas\|dashboard" data/ui-reasoning.csv
# Style_Priority = "Glassmorphism + Flat Design"  → styles.csv 검색어
# Anti_Patterns  = "Excessive animation + Dark mode by default"  → 산출 금지 목록
# Decision_Rules = JSON: {"if_data_heavy": "add-glassmorphism"} → 조건부 분기
```

`Decision_Rules`는 JSON. 조건(if_*)을 읽고 사용자 맥락에 맞는 가지를 택한다.

## 3. 스타일

**`styles.csv`** — `Style Category, Type, Keywords, Primary Colors, Effects & Animation, Best For, Do Not Use For, Light Mode ✓, Dark Mode ✓, Performance, Accessibility, AI Prompt Keywords, CSS/Technical Keywords, Implementation Checklist, Design System Variables`

```bash
grep -i "glassmorphism\|flat design" data/styles.csv
```

`Effects & Animation`·`CSS/Technical Keywords`·`Implementation Checklist`를 그대로 구현 지침으로.

## 4. 색 팔레트

**`colors.csv`** — `Product Type, Primary, On Primary, Secondary, On Secondary, Accent, On Accent, Background, Foreground, Card, Card Foreground, Muted, Muted Foreground, Border, Destructive, On Destructive, Ring, Notes` (shadcn 토큰 형식)

```bash
grep -i "saas\|fintech" data/colors.csv
# 각 hex → CSS 변수로 매핑: Primary→--color-primary, Accent→--color-accent ...
```

`Notes`에 WCAG 조정 이력 있음(예: "Accent adjusted from #F97316 for WCAG 3:1"). 그대로 신뢰.

## 5. 폰트

**`typography.csv`**(페어링) — `Font Pairing Name, Category, Heading Font, Body Font, Mood/Style Keywords, Best For, Google Fonts URL, CSS Import, Tailwind Config, Notes`

```bash
grep -i "elegant\|luxury\|modern" data/typography.csv
# CSS Import 행을 <head>에 그대로 붙인다.
```

**`google-fonts.csv`**(개별 1923종) — `Family, Category, Stroke, Classifications, Keywords, Styles, Variable Axes, Subsets, Designers, Popularity Rank, Trending Rank, Is Noto, ..., Google Fonts URL`

```bash
# 한국어 지원 가변폰트 인기순 후보
grep -i "korean" data/google-fonts.csv | grep -i "variable"
# 특정 패밀리 확인
grep -i "^Pretendard\|^Inter," data/google-fonts.csv
```

대용량이라 **반드시 grep으로 먼저 좁혀라.** 통째 Read 금지(728K).

## 6. 랜딩 구조

**`landing.csv`** — `Pattern Name, Keywords, Section Order, Primary CTA Placement, Color Strategy, Recommended Effects, Conversion Optimization`

```bash
grep -i "hero\|social-proof\|pricing" data/landing.csv
# Section Order 를 페이지 골격으로.
```

## 7. 차트 (대시보드/데이터 시각화)

**`charts.csv`** — `Data Type, Keywords, Best Chart Type, Secondary Options, When to Use, When NOT to Use, Data Volume Threshold, Color Guidance, Accessibility Grade, Accessibility Notes, A11y Fallback, Library Recommendation, Interactive Level`

```bash
grep -i "trend\|comparison\|proportion\|funnel" data/charts.csv
# When NOT to Use 를 반드시 확인 (예: pie는 5개 초과 카테고리 금지)
```

## 8. 아이콘

**`icons.csv`** — `Category, Icon Name, Keywords, Library, Import Code, Usage, Best For, Style`

```bash
grep -i "navigation\|action\|status" data/icons.csv
# Library = Lucide/Heroicons. Import Code 그대로 사용. 이모지 금지.
```

## 9. UX 규칙 (리뷰·자가점검)

**`ux-guidelines.csv`** — `Category, Issue, Platform, Description, Do, Don't, Code Example Good, Code Example Bad, Severity`

```bash
grep -i "accessibility\|contrast\|focus\|touch\|keyboard" data/ux-guidelines.csv
```

Category(10종): Accessibility, Touch & Interaction, Performance, Style Selection, Layout & Responsive, Typography & Color, Animation, Forms & Feedback, Navigation Patterns, Charts & Data. Severity(CRITICAL/HIGH/MEDIUM/LOW)로 우선순위.

---

## 전체 design system 조립 예 ("fintech 대시보드")

```bash
grep -i "fintech\|finance" data/products.csv        # 1) 카테고리·1차 스타일
grep -i "fintech\|finance\|saas" data/ui-reasoning.csv  # 2) 패턴·Style_Priority·anti-pattern
grep -i "glassmorphism\|minimal" data/styles.csv    # 3) 스타일 효과·체크리스트
grep -i "fintech\|finance" data/colors.csv          # 4) 색토큰
grep -i "professional\|modern\|trust" data/typography.csv  # 5) 폰트
grep -i "real-time\|trend\|comparison" data/charts.csv     # 6) 대시보드 차트
grep -i "data\|trust" data/ux-guidelines.csv        # 7) 점검 규칙
```

→ 결과를 읽고 **패턴 + 스타일 + 색(CSS변수) + 폰트(CSS Import) + 차트 + anti-pattern**을 하나로 요약해 산출. BM25 점수는 없으니 후보 여러 개를 비교해 Claude가 최종 선택한다.
