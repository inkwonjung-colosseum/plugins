# design-kit

**Colosseum 브랜드 디자인 시스템을 Claude Code/Codex/Cursor에서 바로 쓰는 플러그인.**
설치 후 "디자인 만들어줘" 한 마디면 콜로세움코퍼레이션 브랜드(CL Blue `#005BF6` · Pretendard ·
절제된 엔터프라이즈 톤)로 self-contained HTML을 생성한다. daemon·MCP 서버·데스크톱 앱 없이 동작한다.

## 구조

```
design-kit/
├── skills/
│   ├── ui-design-intelligence/  # 범용 UI 지능 (브랜드 무관, ui-ux-pro-max MIT)
│   │   ├── SKILL.md             #   스타일·색·폰트·차트·UX 데이터 기반 추천
│   │   ├── data/*.csv           #   84스타일·160색·73폰트·1923구글폰트·25차트·98UX·161추론
│   │   └── references/query-guide.md  # Python 없이 Grep/Read로 CSV 조회하는 법
│   └── colosseum-design/    # Colosseum Design System 2.0 (브랜드 skill, 3층)
│       ├── SKILL.md         #   하드룰·voice + 워크플로우(정책서→화면)
│       ├── colors_and_type.css  # [브랜드층] 토큰: 색·타이포·간격·radius·shadow
│       ├── fonts/ · assets/ · ui_kits/ · preview/   # 폰트·CI로고·UI킷
│       ├── references/
│       │   ├── craft/       # [장인층] 범용 규칙 11종 (anti-ai-slop·state-coverage·
│       │   │                #   form-validation·color·typography·a11y·laws-of-ux…)
│       │   ├── spec-to-screens.md   # [범위층] 정책서→화면 세트 + 완결성 체크리스트
│       │   └── components-admin.md  # Form/Modal/Drawer/Tab/Tag/Toast 패턴
│       ├── examples/
│       │   └── wms-zone-console.html  # admin CRUD 품질 기준 레퍼런스
│       └── tools/lint.mjs   # anti-slop/브랜드 자가검사 (daemon-free)
└── NOTICE.md                # 라이선스 고지 (자사·refero MIT·Pretendard OFL·ui-ux-pro-max MIT)
```

**3층 설계** (open-design 구조 차용): 브랜드(look) × craft(범용 취향) × scope(무슨 화면).
craft 층은 MIT refero_skill을 콜로 토큰으로 재이식해 **AI 티·미완성 상태(populated만 그리기)·
폼 누락**을 막는다. `references/spec-to-screens.md`가 "리스트 한 장만 만드는 실패"를 차단한다.

## skill 2종 — 언제 뭘 쓰나

| skill | 언제 | 산출 |
|-------|------|------|
| **colosseum-design** | 콜로세움 브랜드 작업 (CL Blue·Pretendard·Material Symbols 고정) | 브랜드 일관 self-contained HTML |
| **ui-design-intelligence** | 브랜드 미정·외부·throwaway. 스타일/색/폰트를 **고르는 일**이 본질 | 데이터 기반 추천 design system |

두 skill은 **경계가 명확**하다. 콜로 화면 = colosseum-design 토큰만(색·폰트 고정). 범용 탐색 =
ui-design-intelligence(색·폰트 추천). **섞지 마라** — 색·폰트 추천은 콜로 단일 브랜드 lock과 충돌한다.
ui-design-intelligence는 ui-ux-pro-max(MIT)의 CSV DB를 가져오되 **Python 엔진은 제외**하고 Claude가
Grep/Read로 조회한다(zero-config 유지).

## 동작 방식

1. 사용자가 "화면/UI/디자인 만들어줘"라고 하면 `colosseum-design` skill이 트리거된다.
2. skill이 `colors_and_type.css` 토큰과 하드룰(한국어 우선 `-세요`체 · `#005BF6` ·
   Pretendard · 이모지 금지 · radius 6px · 컴포넌트 SM 등)을 적용한다.
3. 토큰을 인라인한 **self-contained HTML**을 생성한다. 폰트(Pretendard)·아이콘(Material Symbols)은
   CDN 또는 번들 woff2로 로드한다.

## 사용 예

```
콜로세움 브랜드로 주문 목록 화면 만들어줘
WMS 대시보드 목업 만들어줘
로그인 화면 PDA용으로 만들어줘
정산 내역 페이지 프로토타입 만들어줘
```

## 하드룰 (요약 — 상세는 SKILL.md)

- 한국어 우선, `-세요` 정중 명령체, 프로덕션 UI 이모지 금지
- primary `#005BF6`(CL Blue) — 페이지 배경·그라데이션 금지(로고만 예외)
- Pretendard, 본문 14px, 기본 weight Medium(500), 600 미사용
- 기본 컴포넌트 SM(32px), radius 6px, border 1px `#CACACA`
- 아이콘 = Material Symbols Outlined
- PDA: 44px 최소 터치 타겟, 한손 조작

## 제약

- **결과물 = HTML 파일.** 브라우저로 열면 렌더된다. 라이브 미리보기 기능은 없다.
- 폰트는 번들 woff2(오프라인) 또는 CDN(온라인) 둘 다 가능.

## 라이선스

`MIT` (자사 skill). 번들 Pretendard는 SIL OFL 1.1, CI 로고는 회사 자산이다. 상세는
[`NOTICE.md`](./NOTICE.md) 참조.
