# NOTICE — design-kit 구성요소 고지

## 1. colosseum-design (자사 자산)

`skills/colosseum-design/`은 Colosseum Corporation(콜로세움코퍼레이션)의 내부 디자인 시스템 2.0이다.
디자인 가이드·토큰·UI 킷·CI 로고를 포함한다. CI 로고(`assets/`)는 회사 자산이며 재색·재드로우·외부
배포를 제한한다.

## 2. craft 레퍼런스 (MIT — refero_skill © Refero Design)

`skills/colosseum-design/references/craft/`의 범용 장인 규칙(typography·color·anti-ai-slop·
state-coverage·form-validation·accessibility-baseline·animation-discipline·laws-of-ux·
rtl-and-bidi·typography-hierarchy·typography-hierarchy-editorial)은 MIT 라이선스
[refero_skill](https://github.com/referodesign/refero_skill)(© Refero Design)을
[nexu-io/open-design](https://github.com/nexu-io/open-design)(Apache-2.0)이 가공한 것을
**콜로세움 토큰·하드룰에 맞게 재이식**했다.

**적용한 변경**: 각 파일 상단에 "콜로세움 적응 노트"(토큰 매핑) 추가, `typography`/`color`/
`anti-ai-slop`은 콜로 weight(400/500/700, 600 금지)·CL Blue accent·Material Symbols·Pretendard로
재작성, 출력 카피를 한국어 `-세요`체로 명시. 원저작권은 Refero Design에 귀속(MIT). MIT 전문은
refero_skill 저장소 참조.

## 3. 번들 폰트 — Pretendard (SIL Open Font License 1.1)

`skills/colosseum-design/fonts/`의 Pretendard(Variable/Bold/Black)는 orioncactus/Pretendard,
SIL OFL 1.1 라이선스다. <https://github.com/orioncactus/pretendard>

## 4. 런타임 CDN 의존 (출력 HTML)

이 skill로 만든 HTML은 다음을 CDN에서 로드할 수 있다(브라우저 온라인 필요):
- **Pretendard** — jsDelivr, SIL OFL 1.1
- **Material Symbols Outlined** — Google Fonts, Apache-2.0

완전 오프라인이 필요하면 `colosseum-design/fonts/`의 woff2를 출력 프로젝트로 복사하고
`@font-face` 경로를 맞춘다.

## 5. ui-design-intelligence 데이터 (MIT — ui-ux-pro-max-skill © Next Level Builder)

`skills/ui-design-intelligence/data/`의 CSV 10종(styles·colors·typography·google-fonts·
ux-guidelines·charts·products·landing·icons·ui-reasoning)과 `references/query-guide.md`의
조회 규칙은 MIT 라이선스
[ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
(© 2024 Next Level Builder)의 `src/ui-ux-pro-max/data/`에서 가져왔다.

**적용한 변경**: 원본의 Python BM25 검색 엔진(`search.py`·`core.py`·`design_system.py`)·stack
CSV·플랫폼 템플릿은 **가져오지 않았다**(콜로 zero-config 철학 유지). CSV 데이터는 원본 그대로이며,
조회는 Claude의 Grep/Read로 대체했다. 이 skill은 **브랜드 무관 범용**으로 colosseum-design의 단일
브랜드 lock과 분리된다. 원저작권은 Next Level Builder에 귀속(MIT). MIT 전문은 원본 저장소 참조.
