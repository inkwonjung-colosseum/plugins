---
name: plan-review
description: "plan-format으로 작성한 정책서와 기능/화면설계서 묶음을 외부 발행 전에 Product Docs SSOT 충돌과 디자인·개발·QA·운영 착수 가능성 측면에서 검토하는 스킬."
argument-hint: "<초안 폴더 또는 기능설계서/정책서 파일경로>"
---

# plan-review

`/product-team-kit:plan-format`으로 저장한 초안 폴더 또는 기능설계서/정책서 파일을 발행 전에 검토하는 스킬이다. 템플릿 구조 검사가 아니라 Product Docs SSOT 충돌, 명확성, 용어 일관성, 디자인·개발·QA·운영 착수 가능성을 4축으로 점검하는 gate다.

Product Docs SSOT는 `<outputRoot>/`을 제외한 현재 프로젝트의 Markdown 문서 중 제품 정책, PRD/요구사항, 기능/화면 설계, 운영/QA 판단을 담은 문서와, 그 Markdown이 상대경로로 명시 참조한 로컬 resource만 포함한다. 코드, 설정 파일, 빌드 산출물, dependency/vendor, 외부 URL은 SSOT 근거에서 제외한다. `<outputRoot>/` 하위 파일은 검토 대상일 수 있지만 SSOT 근거로 사용하지 않는다.

`<outputRoot>`과 SSOT corpus 범위는 `../../references/config-contract.md`를 따라 결정한다. `outputRoot`의 default는 `planning`이며, `<outputRoot>/**`은 항상 SSOT exclude에 자동 포함된다. `ssot.include`가 지정되면 SSOT corpus를 그 glob 안으로 좁히고, 미지정/빈 배열이면 default `Product Team Space/Product Department/Colonova Product/_AI_ 정책서 & 기능설계서/**/*.md`를 사용한다. `ssot.exclude`는 default 제외(`.git/`, `vendor/`, `node_modules/`, `build/`, `dist/`, `.cache/`, `generated/`)에 누적한다.

판정 기준, 합성 규칙, 4축 점검 기준, 근거 패키지 형식은 `references/review-rules.md`를 단일 기준으로 따른다. 최종 출력 형식은 `references/output-format.md`를 따른다. 사람용 리포트 하나로 출력하며 별도 YAML manifest 블록은 사용하지 않는다.

## 호출

- Claude Code: `/product-team-kit:plan-review <초안 폴더 또는 기능설계서/정책서 파일경로>`
- Codex: `$plan-review <초안 폴더 또는 기능설계서/정책서 파일경로>`

예시:
- `/product-team-kit:plan-review planning/결제기능--YYYY-MM-DD-HHMMSS/`
- `/product-team-kit:plan-review planning/결제기능--YYYY-MM-DD-HHMMSS/결제기능_기능설계서.md`

## 암묵 호출 라우팅

다음 의도에서는 `plan-review`를 선택한다.

- 기존 기능설계서/정책서 초안 또는 초안 폴더 검토
- 발행 전 검토, 통과/조건부 통과/수정 필요 판정
- Product Docs SSOT 근거와 초안의 충돌, 누락, 착수 가능성 확인
- 이미 생성된 초안의 품질 평가

다음 의도에서는 `plan-review`를 선택하지 않는다.

- 기획 입력을 기능설계서와 정책서 초안으로 생성해야 하는 경우 → `plan-format`

사용자가 "정리하고 검토"를 함께 요청했지만 기능설계서/정책서 초안 경로가 아직 없으면 `plan-review`를 먼저 호출하지 않는다. 먼저 `plan-format`으로 초안을 저장한 뒤 저장 경로를 대상으로 검토한다.

## 사전 점검

1. `.product-team-kit/config.json` 존재 여부를 확인하고 `outputRoot`, `ssot.include`, `ssot.exclude`를 확정한다. 파일 없음, JSON 파싱 실패, `version` 미일치, `outputRoot` 검증 거부는 치명 설정 오류로 즉시 종료하고 `set-config` 사용을 안내한다. 비치명 검증 거부만 default fallback과 `[설정 경고]`로 처리한다.
2. 검토 대상이 기능설계서/정책서 초안 파일 또는 그 묶음 폴더인지 확인한다. 다른 문서 타입(상위설계서 등)이면 검토를 수행하지 않고 `output-format.md`의 `올바른 검토 대상이 아님` 템플릿으로 종료한다.
3. 입력이 폴더면 같은 폴더의 기능설계서와 정책서를 함께 검토 대상으로 잡는다. 입력이 단일 파일이면 같은 폴더에서 `plan-format` 산출 파일명인 `[안전기능명]_기능설계서.md` / `[안전기능명]_정책서.md`의 같은 stem을 우선해 짝문서를 찾는다.
4. 짝문서가 없으면 단일 검토를 진행하고 `검증 한계`에 `짝문서 없음`을 기록한다. 검토 대상이 명시적으로 다른 문서의 정책/기능 판단에 의존하면 분류를 `필수 수정` 또는 `발행 전 확인`으로 올린다.

## 4축 검토

각 축은 검토 대상 본문과 SSOT corpus를 직접 읽고 점검한다. 상세 기준은 `references/review-rules.md`의 `4축 점검 기준` 섹션을 따른다.

- **A. SSOT 충돌**: 초안 확정 문장 vs Product Docs SSOT current evidence.
- **B. 명확성**: `[미정]`/`[가정]`/`[확인 필요]`/`[충돌 후보]` markers 처리, 모호 문장, 결정 가능 수준.
- **C. 용어 일관성**: 역할명·상태명·권한명·화면명·도메인 stem 통일성.
- **D. 4역할 넘김 가능성**: design/development/qa/operations 각각이 대화 기억 없이 다음 업무 시작 가능 여부.

발견 사항은 분류(필수 수정 / 발행 전 확인 / 참고)와 함께 기록한다.

## 실행 순서

1. 사전 점검 완료. 입력 확정, config 확정, 문서 타입 검증.
2. 검토 대상에서 키워드(기능명, 정책명, 도메인, 역할명, 상태명, 권한명, 화면명, 핵심 조건·예외)를 추출한다.
3. SSOT corpus를 키워드로 좁혀 직접 읽는다. 외부 URL, 코드, 설정 파일은 읽지 않는다. 핵심 근거가 외부 URL뿐이면 `검증 한계`에 남긴다.
4. 4축(A·B·C·D)을 점검하고 발견 사항을 분류와 함께 만든다.
5. `references/review-rules.md`의 합성 규칙으로 dedup하고 보수 합성으로 결과를 결정한다.
6. `references/output-format.md`의 결과별 템플릿으로 사람용 리포트를 출력한다. 설정 경고가 있으면 `[설정 경고]` 블록을 한 번 추가한다.

현재 대화 컨텍스트는 근거가 아니다. 대화에서 알게 된 배경, 의도, 작성 당시 판단은 검토 대상 파일 또는 SSOT 근거에 없으면 근거 부족으로 본다.

## 규칙

- 검토 기준과 결과 경계는 `references/review-rules.md`만 따른다.
- 최종 출력은 `references/output-format.md`만 따른다. YAML manifest 블록은 사용하지 않는다.
- 수정이 필요한 경우 직접 수정하지 않는다. 필수 수정 항목만 제시한다.
- 외부 시스템에 직접 게시하지 않고 Product Docs SSOT Markdown 또는 팀 문서 export snapshot을 자동 수정하지 않는다.
- `<outputRoot>/` 산출물은 review target으로만 읽고 SSOT 근거로 승격하지 않는다.
- 읽은 근거, 읽지 않은 관련 후보, 제외 후보, 검증 한계를 최종 출력에 남긴다.
- 설정 파싱/검증 경고는 사용자 출력 하단에 `[설정 경고]` 블록 한 번으로 표기한다. 경고 포맷은 `../../references/config-contract.md`를 따른다.
