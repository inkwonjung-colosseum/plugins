# Rerun Contract

`plan-draft`와 `plan-format`은 저장 보류 이후의 재실행 흐름을 이 계약으로 판단한다. 목적은 자동 `plan-format -> plan-draft -> plan-format -> plan-draft` ping-pong을 막고, 사용자가 다음 결정을 직접 고르게 하는 것이다.

## 재실행 상태

| 상태 | 의미 | 다음 행동 |
| --- | --- | --- |
| `normal-input` | 직접 텍스트, 일반 파일, 일반 디렉터리 입력 | 각 스킬의 일반 입력 규칙을 따른다 |
| `format-insufficient-hold` | `plan-format`이 일반 입력을 정보 부족으로 저장 보류함 | `plan-draft` 보완을 1회 안내할 수 있다 |
| `draft-artifact` | `plan-format` 입력이 `plan-draft` 산출 `_기획초안.md`임 | 같은 기획초안 폴더를 재사용한다 |
| `draft-from-format-hold` | 기획초안 안에 `plan-format` 저장 보류에서 온 재실행 맥락이 있음 | `plan-format` 재시도 대상으로 읽는다 |
| `format-after-draft-insufficient` | `plan-format`이 draft artifact 입력을 다시 정보 부족으로 판정함 | terminal hold. 자동 `plan-draft` 안내 금지 |
| `storage-failure` | timestamp, mkdir, write, rename, cleanup 실패 | 저장 환경과 partial artifact 확인 후 같은 스킬 재실행 |
| `existing-output-hold` | 대상 final 파일이 이미 있어 덮어쓸 수 없음 | 기존 산출물 확인 또는 명시적 새 run |

## 일반 정보 부족 hold

`plan-format`이 일반 입력을 정보 부족으로 저장 보류하면 출력에 다음 marker를 포함한다.

```text
재실행 상태: format-insufficient-hold
```

이 경우 `plan-format`은 `plan-draft` 보완을 안내할 수 있고, 복사 가능한 재실행 블록에도 같은 marker를 포함한다.

```text
$plan-draft "재실행 상태: format-insufficient-hold
기획 주제: [추출기능명]
원 입력 또는 원 입력 파일 경로: [파일 경로 또는 핵심 메모]
plan-format 저장 보류 사유: 입력만으로 기능설계서/정책서 초안을 만들기 부족함
부족 항목: [부족 항목 요약]
필요한 답변:
1. [부족 항목을 채우기 위한 질문 1]
2. [부족 항목을 채우기 위한 질문 2]
3. [부족 항목을 채우기 위한 질문 3]
답변:
1. [사용자 답변]
2. [사용자 답변]
3. [사용자 답변]"
```

## 기획초안 재실행 맥락

`plan-draft` 입력에 `재실행 상태: format-insufficient-hold` 또는 `plan-format 저장 보류 사유`가 있으면, 저장되는 기획초안 끝에 optional 섹션을 추가한다.

```md
## 11. 재실행 맥락

- 출처: plan-format 저장 보류
- 보류 사유: [plan-format 저장 보류 사유]
- 보완 대상 부족 항목: [부족 항목 요약]
- 자동 왕복 횟수: 1
```

일반 `plan-draft` 실행에는 이 섹션을 만들지 않는다. 이 섹션은 초안 내용의 SSOT 근거가 아니라 재실행 제어 metadata다.

## Terminal hold

`plan-format`이 `_기획초안.md` 또는 draft artifact 입력을 정보 부족으로 판정하면 `format-after-draft-insufficient` 상태로 종료한다. 이 상태에서는 자동 `plan-draft` 안내를 하지 않는다.

출력 형식:

```text
사용자 결정 필요
- 추출 기능명: [추출기능명]
- 초안 생성 가능: 아니오
- 재실행 상태: format-after-draft-insufficient
- 자동 재질문 중단: 예
- 이유: plan-draft 산출 기획초안 입력으로도 기능설계서/정책서 초안을 만들기 부족함

부족 항목:
- [항목]: [부족한 이유]

선택 가능한 다음 행동:
1. 부족 항목을 직접 채워 plan-format 재실행
2. 새 기획 인터뷰를 명시적으로 시작
3. 현재 입력으로 생성 범위를 줄여 다시 요청

바로 재실행 가능한 입력 블록:
$plan-format "기능명: [추출기능명]
이전 기획초안: [기획초안 경로]
보완한 부족 항목:
1. [부족 항목 1에 대한 직접 보완]
2. [부족 항목 2에 대한 직접 보완]
3. [부족 항목 3에 대한 직접 보완]
생성 범위 조정: [범위 축소 또는 유지]"
```

사용자가 명시적으로 새 기획 인터뷰를 요청하면 `plan-draft`를 다시 사용할 수 있다. 금지되는 것은 스킬이 자동으로 다시 `plan-draft`로 보내는 흐름이다.
