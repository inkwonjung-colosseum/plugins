# Output Contract

`plan-format`의 사용자 출력 기준이다. step 1 strict-exit, step 2 gate, step 3 변환 결과를 확정한 뒤 아래 4 템플릿 중 하나를 사용한다.

## 공통 규칙

- 본 contract 템플릿은 종료 분기에서 1회만 출력한다. 실행 중 step 표시 외에 다른 사용자 출력 블록을 만들지 않는다.
- 기능설계서/정책서 본문(섹션 헤더, 표, admonition metadata 줄)은 절대 응답 텍스트에 출력하지 않는다. 본문은 Write 툴로 파일에만 기록한다. `[생성 요약]`은 1~3개 불릿으로 반영 범위만 짧게 남기고 본문 인용 금지.
- 0개 섹션은 통째로 생략한다. `없음`이나 빈 헤더를 출력하지 않는다.
- marker 정의·표기·합산 기준은 `../SKILL.md`의 `### Marker 4종`을 따른다.
- 저장 보류는 추가 기획 질문으로 돌리지 않고 부족 항목과 입력 제외 항목만 반환한다. 보강용 입력 템플릿은 만들지 않는다.
- 저장 실패는 추가 기획 질문으로 돌리지 않고 저장 환경과 남은 staging/target 경로 확인으로 안내한다.
- target folder가 이미 있으면 저장 보류가 아니라 저장 실패 또는 collision suffix 재시도 대상으로 기록한다.
- `../../../references/config-contract.md` 기준의 비치명 검증 경고가 1개 이상이면 모든 출력 템플릿(저장 완료/저장 보류/저장 실패) 가장 마지막 블록으로 `[설정 경고]`를 한 번 추가한다. 다른 섹션 다음에 위치한다. 경고가 없으면 블록을 출력하지 않는다. 본 contract가 위치 단일 소스다.
- "설정 없음" 템플릿은 strict-exit 응답이며 `[설정 경고]` 블록을 별도로 추가하지 않는다 (종료 사유 자체가 본문에 포함됨).

## 설정 없음 (strict-exit)

step 1에서 config 없음·파싱 실패·`version` 미일치·`outputRoot` 검증 거부 시 출력한다. 저장 폴더 미생성, gate 미수행.

```text
설정 없음 — plan-format을 실행하려면 config가 필요합니다
- 기대 경로: <project-root>/.product-team-kit/config.json
- 발견 결과: [파일 없음 | JSON 파싱 실패 | version 미일치 | outputRoot 검증 거부]
- 다음 단계:
  - Claude Code: /product-team-kit:set-config
  - Codex: $set-config
```

`발견 결과`는 단일 사유만 표기한다. 복수 사유가 있으면 가장 먼저 부딪힌 항목을 적는다.

## 저장 완료

```text
저장 완료
- 추출 기능명: [추출기능명]
- 안전기능명: [안전기능명]
- 초안 생성 가능: 예
- 문서 상태: 로컬 초안
- 팀 문서 반영 상태: 미반영
- 공식 팀 문서: 아니오
- 입력 처리: [직접 입력 / 파일 1개 / 디렉터리 텍스트 파일 N개 / 혼합 입력]
- 저장 경로:
  - [feature_doc_path]
  - [policy_doc_path]

[생성 요약]:
- 기능설계서: [주요 반영 범위 1~3개]
- 정책서: [주요 반영 범위 1~3개]

[검토 준비 상태]:
- 상태: [plan-review 필요 / 수동 확인 필요 / 초안 검토 가능]
- 이유: [[미정], [가정], [확인 필요], [충돌 후보], 원본 문서 피드백 중 남은 항목 기준 1~2줄]

[원본 문서 피드백] (N개):
- [유형]: [원문 기준 발견 문제] -> [정리/후속 확인 제안]

확인 필요 질문 (N개):
- [질문]: [결정 필요 이유]

[미확정·가정 항목] (N개):
| 문서 | 유형 | 섹션 | 내용 |
|------|------|------|------|
| 기능설계서 | [미정] | ... | 확인 필요 |
| 정책서 | [가정] | ... | ... |

[본문 제외 항목] (N개):
- [유형]: [읽었지만 기능설계서/정책서 본문 책임이 아니라 제외한 내용과 이유]

[읽기 제외 항목] (N개):
- [경로 또는 유형]: [읽기 실패, 바이너리, 권한 오류, 디코딩 실패 등 제외 이유]

다음 단계:
- Claude Code: /product-team-kit:plan-review [target_dir]/
- Codex: $plan-review [target_dir]/

[설정 경고] (N개):
- [경로 또는 키]: [거부 사유와 fallback 결과]
```

`[본문 제외 항목]`은 입력을 읽었지만 `excluded` 라벨, 선택되지 않은 기능 후보, 디자인/API/DB/QA/운영/개발 상세 등 기능설계서·정책서 본문 책임이 아니라 제외한 항목이다. `[읽기 제외 항목]`은 파일을 읽지 못해 제외한 항목이다. 저장 완료 템플릿에서는 기존 `[입력 제외 항목]` 블록을 사용하지 않는다.

## 저장 보류

step 2 gate 미통과 또는 step 4 main 자체 검증 실패 (빈 골격, 구조 불일치 retry 2회 fail 등) 시 출력한다. `이유` 필드 첫 머리에 발생 step과 분기명을 표기한 뒤 (예: `step 2 gate 미통과 — `, `step 4 검증 실패 — 빈 골격 — `, `step 4 검증 실패 — 구조 불일치 — `) 부족·실패 성격을 자유 텍스트로 이어 쓴다 (예: "제품·업무 판단 정보 부족", "디자인·개발 상세는 많지만 정책/기능 판단 정보 부족", "정책서 본문이 빈 골격 — policy 라벨 단편 부족", "읽기 대상 텍스트 전체 확인 불가", "단일 기능 범위 불명확").

```text
저장 보류
- 추출 기능명: [추출기능명]
- 초안 생성 가능: 아니오
- 입력 처리: [직접 입력 / 파일 1개 / 디렉터리 텍스트 파일 N개 / 혼합 입력]
- 이유: [입력만으로 기능설계서/정책서 초안을 만들기 부족한 성격을 한 줄로]

부족 항목:
- [항목]: [부족한 이유]

[제외된 상세 유형] (N개, 디자인/개발/QA/운영 heavy 입력일 때만):
- [디자인/API/DB/QA/운영/개발 작업 등]: [관찰 요약]

[입력 제외 항목] (N개):
- [경로 또는 유형]: [읽기 실패, 바이너리, 권한 오류, 디코딩 실패 등 제외 이유]

[설정 경고] (N개):
- [경로 또는 키]: [거부 사유와 fallback 결과]
```

`[제외된 상세 유형]` 블록은 입력의 주된 내용이 디자인·API·DB·QA·운영·개발 작업 분해일 때만 출력한다. 그 외 모든 부족 케이스는 생략한다.

## 저장 실패

step 3에서 staging folder 생성, 파일 write, verify, rename, collision suffix `--99` 도달 등 저장 환경 문제로 실패한 경우 출력한다.

```text
저장 실패
- 추출 기능명: [추출기능명]
- 안전기능명: [안전기능명]
- 초안 생성 가능: 예
- 저장 성공: 아니오
- 실패 단계: [folder | write | rename | cleanup | verify]
- 시도 폴더: [target_dir 또는 생성 전 실패]
- staging 폴더: [staging_dir 또는 생성 전 실패]
- target 폴더 상태: [not-created | exists-before-run | final-ready | verify-failed | unknown]
- staging 폴더 상태: [not-created | created | written | renamed | cleanup-deleted | cleanup-failed]
- 기능설계서 staging 상태: [not-started | written]
- 정책서 staging 상태: [not-started | written]
- 남은 파일 또는 폴더:
  - [경로]
- 이유: [짧은 실패 사유]
- 복구 참고: [남은 staging/target 경로 또는 실패한 parent 폴더 권한 확인]

다음 단계:
추가 기획 질문이 아니라 저장 환경과 남은 staging/target 경로를 확인한 뒤 다시 실행한다.

[설정 경고] (N개):
- [경로 또는 키]: [거부 사유와 fallback 결과]
```

`실패 단계`는 `folder` (collision suffix 소진 또는 staging folder 생성 실패), `write` (staging 파일 쓰기 실패), `rename` (staging folder를 target folder로 rename 실패), `cleanup` (실패 후 cleanup 실패), `verify` (파일 존재 또는 staging 잔여 검증 실패)만 사용한다. 정상 실패는 target folder 아래에 한쪽 final 문서만 남기지 않아야 한다. cleanup 실패나 애매한 rename 실패로 경로가 남으면 `남은 파일 또는 폴더`에 모두 남긴다.
