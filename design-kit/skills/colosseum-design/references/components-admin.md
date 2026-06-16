# Admin 컴포넌트 패턴 (Form · Modal · Drawer · Tab)

> colosseum-design `SKILL.md`의 Known gaps가 자백한 미정의 컴포넌트(Modal/Table/Tab 등) +
> Form을 콜로 토큰으로 정의한다. `ui_kits/web-admin/`(DataTable/Sidebar/StatCard)을 보완한다.
> 모든 값은 `colors_and_type.css` 토큰. 기본 밀도 **SM**, radius 카드 8 / 컨트롤 6.

## 공통 토큰 빠른 참조

```
배경 page #f6f7f9 · surface #fff · border #CACACA(--color-borders-outline)
text 제목 #1A1A1A · 본문 #464646 · 보조 #767676 · primary #005BF6
컨트롤 높이 SM 32px · 입력 36px · 본문 14px · weight 500 기본(600 금지)
radius 카드 8 / 입력·버튼 6 / 태그 4 / pill 9999 · ease var(--ease-out-quint)
아이콘 Material Symbols Outlined · 포커스 border #005BF6 + 3px rgba(0,91,246,.12)
```

## Button

```
SM 32px / 6px radius / 13px / weight 500
primary  : bg #005BF6, hover #0742A7, disabled bg #CACACA
outline  : bg #fff, border 1px #CACACA, hover border #929292
ghost    : 투명, hover bg #f6f7f9
xs 26px / 4px radius (테이블 행 액션)
```
primary는 화면당 1개 권장(accent 규율, `craft/color.md`).

## Form (생성/수정)

- **레이아웃**: 슬라이드오버(우측 460px) 또는 페이지. 라벨은 **입력 위**(placeholder-only 금지).
- **필드**: `label`(12px/700) + 선택적 `*` 필수 표시 + `.ctl`(높이 36, border #CACACA, focus #005BF6) + hint(11px #767676).
- **불변 필드**: `disabled` + 회색 bg(#f6f7f9) + 라벨에 자물쇠 "변경 불가"(정책서 수정 불가 항목).
- **조건부 필드**: 타입 선택에 따라 활성/비활성 (예: 품온·DG는 INBOUND/STORAGE만).
- **검증**: `craft/form-validation.md` — blur 시 검증, 중복은 인라인 에러(빨강 hint), 에러 카피 `-세요`체.
- **에러 카피 예**: `유효한 이름을 입력하세요`, `이미 동일 센터에 존재하는 이름입니다`.

## Drawer (상세, 우측 슬라이드)

- width 420–460px, `transform:translateX(100%)→0`, `var(--ease-out-quint)` .2s.
- scrim `rgba(0,0,0,.14~.18)`, 클릭/Esc 닫기.
- head(코드 mono #005BF6 + 이름) · body(섹션별 kv 그리드) · foot(액션 버튼).
- 읽기 전용 정책은 `읽기 전용` 배지로 명시(상속값 변경 불가 표현).

## Modal (상태 변경·확인)

- 중앙 440px, `translate(-50%,-50%)`, scrim. radius 8, shadow `0 20px 50px rgba(0,0,0,.18)`.
- head(제목 16/700 + 대상) · body · foot(우측 정렬, 취소 outline + 확정 primary).
- **상태 변경**: 현재→선택 전이 표시, 허용 전이만 radio, 차단/자동은 비활성+안내, **사유 코드 select 필수**.
- **파괴적 확인**: `삭제하시겠습니까?` 같은 직접 질문 + 확정 버튼 danger(#f81616). 콜로는 물리삭제 대신 Inactive.

## Tab

```
밑줄형: 활성 탭 border-bottom 2px #005BF6 + text #005BF6 / 비활성 #767676
높이 40px, 14px, gap 24px, hover text #464646
```

## Tag (상태/타입 배지)

```
status 활성  : bg #dff7e2 text #289a3a   (green / 성공)
status 폐쇄예정: bg #fff1cc text #8a6400   (yellow / 경고)
status 비활성 : bg #DEDEDE text #767676    (gray)
status 위험  : bg #fff0f0 text #f81616    (red)
status 정보  : bg #e5f3ff text #1a95ff    (sky)
```
높이 22px, radius 4, 12px/700. 색만으로 의미 전달 금지 — 텍스트 라벨 병행(`craft/accessibility-baseline.md`).

## Toast

- 하단 중앙, `var(--natural-800)` bg, 13px, 성공 아이콘 green. 2.2s 자동 닫힘(hover 시 일시정지 — WCAG 2.2.1).
- 비파괴 확인은 `role="status"`(포커스 이동 안 함), 파괴/긴급은 `role="alertdialog"`.

## Empty / Loading / Error (state-coverage 적용)

- **Empty**: 56px 원형 아이콘(`search_off` 등) + 제목(15/700) + 설명(13 #767676) + CTA. 빈 화면 금지.
- **Loading**: skeleton(레이아웃 매칭) 또는 라벨 spinner. 0–300ms 무표시, 15s "예상보다 오래 걸립니다".
- **Error**: 무엇/왜/무엇을(복구 액션 버튼). 입력값 보존. 색만으로 표현 금지.

> 레퍼런스 구현: `examples/wms-zone-console.html` — 위 패턴(LNB·리스트·생성/수정 슬라이드오버·상태변경 모달·드로어·toast·empty)이 모두 들어 있다. 새 admin 화면은 이 구조·밀도를 모방하라.
