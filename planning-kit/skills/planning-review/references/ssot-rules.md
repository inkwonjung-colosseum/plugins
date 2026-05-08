# SSOT Rules (R1)

`planning-review`의 SSOT 충돌 점검 축(R1).

## 용어

- **SSOT corpus**: 현재 프로젝트 폴더 안 모든 `*.md` (`.git/`, `node_modules/` 자동 제외, `--ssot-include <glob>`로 좁힘). **외부 fetch 본문·multimodal 이미지 해석은 corpus 미포함** (외부·일회성).
- **확정 문장**: 변환 본문 중 `[TBD]`가 아닌 단정 표현.

## R1.1 corpus 추출 절차

1. 변환 본문에서 키워드 추출: 기능명·도메인 stem·역할명·상태명·권한명·정책 핵심어.
2. 프로젝트 폴더 `find . -name '*.md'` (`.git`/`node_modules` 제외, `--ssot-include`로 좁힘).
3. 키워드 `grep -l` 또는 `rg -l`로 본문 매칭 → 매칭 file 목록 확정.
4. 매칭 file을 `Read` 툴로 직접 읽음 (인덱스 스캔 단계 없음).

문서 종류·역할(정책/PRD/회의록/README) 구분 안 함. archive/old/draft 신호 file도 grep 매칭만으로 비교 대상에 포함 — 별도 분류 없음.

## R1.2 매칭 0건

- 매칭 file 0건 → R1 결과 `검증 대상 없음`. 출력 헤더에 `SSOT 매칭 파일 0개 (관련 Markdown 부재)`.
- 결과를 낮추지 않는다. R2·R3는 별도 진행.

## R1.3 매칭 ≥1건

- 변환 본문 확정 문장과 매칭 file 본문을 직접 비교.
- 같은 대상(역할·상태·정책 규칙·임계)이 양쪽에 있고 표기·결정·임계값이 어긋나면 발견.
- 같은 대상에 대해 SSOT가 침묵하면 발견 아님 (R3로 가능).
