# Output Contract

`planning-publish-confluence`는 report-first markdown을 출력한다. 최종 출력은 항상 `# planning-publish-confluence`로 시작한다.

## 1. 금지 입력 취소

```markdown
# planning-publish-confluence

- 결과: 발행 취소
- 이유: 0.2.13은 현재 context memory 안의 정책서·기능 설계서만 발행 대상으로 사용합니다.
- Confluence 변경: 없음

## 금지 입력

- 파일 경로, URL, 저장 산출물 경로, 옵션 인자는 지원하지 않습니다.
```

## 2. Context Gate 취소

```markdown
# planning-publish-confluence

- 결과: 발행 취소
- 이유: 현재 context memory에서 정책서·기능 설계서 두 본문을 명확히 식별할 수 없습니다.
- Confluence 변경: 없음

## 부족 항목

- 정책서 본문 없음
- 기능 설계서 경계 불명확
```

부족 항목은 최대 5개 bullet로 제한한다. 파일 경로, URL, 저장 산출물 경로를 달라는 재실행 안내는 출력하지 않는다.

## 3. 사용자 취소

```markdown
# planning-publish-confluence

- 결과: 발행 취소
- 이유: 사용자가 parent 선택 또는 최종 확인 단계에서 취소했습니다.
- Confluence 변경: 없음
```

## 4. 완료 출력

```markdown
# planning-publish-confluence

- 결과: Confluence 발행 완료
- Confluence 변경: 생성 3개, 업데이트 0개, 변경 없음 0개

## 생성/수정 페이지

| 문서 | 동작 | page id | version | URL |
|---|---|---:|---:|---|
| [기능명] v0.7 | 생성 | 123 | 1 | https://... |
| [기능명] 정책서 v0.7 | 생성 | 124 | 1 | https://... |
| [기능명] 기능 설계서 v0.7 | 생성 | 125 | 1 | https://... |

## 실패/스킵

- 없음

## 발행 정보

- parent: Product Team Space / SSOT
- 기능: [기능명]
- 발행 label: v0.7
- 문서 상태: SSOT 후보
- operation id: publish-YYYYMMDD-HHMMSS-[short-hash]

## Fingerprint

| 문서 | fingerprint |
|---|---|
| 정책서 | sha256:... |
| 기능 설계서 | sha256:... |

## 주의

- 발행 기준: 현재 context memory
- 문서 상태: SSOT 후보
- 화면 전용 section은 child page 본문에서 제외했습니다.
```

## 5. 부분 완료 출력

```markdown
# planning-publish-confluence

- 결과: 부분 완료
- Confluence 변경: 생성 1개, 업데이트 0개, 변경 없음 0개

## 성공 페이지

| 문서 | 동작 | page id | version | URL |
|---|---|---:|---:|---|
| [기능명] v0.7 | 생성 | 123 | 1 | https://... |

## 실패

- 실패 step: 정책서 readback
- 실패 page: [기능명] 정책서 v0.7
- 이유: content fingerprint mismatch
- 남은 write: 실행하지 않음

## 발행 정보

- parent: Product Team Space / SSOT
- 기능: [기능명]
- 발행 label: v0.7
- 문서 상태: SSOT 후보
- operation id: publish-YYYYMMDD-HHMMSS-[short-hash]

## 재개 기준

- 같은 operation id와 fingerprint가 확인되면 성공 page는 변경 없음으로 보고 남은 page만 재개할 수 있습니다.
- fingerprint가 다르면 새 발행 시도로 취급하고 최종 확인을 다시 받습니다.
```

## 6. 변경 없음 출력

```markdown
# planning-publish-confluence

- 결과: 변경 없음
- Confluence 변경: 생성 0개, 업데이트 0개, 변경 없음 3개

## 페이지

| 문서 | 동작 | page id | version | URL |
|---|---|---:|---:|---|
| [기능명] v0.7 | 변경 없음 | 123 | 2 | https://... |

## 실패/스킵

- 없음

## 발행 정보

- parent: Product Team Space / SSOT
- 기능: [기능명]
- 발행 label: v0.7
- 문서 상태: SSOT 후보
- operation id: publish-YYYYMMDD-HHMMSS-[short-hash]
```

## 7. 규칙

- 완료/부분 완료/변경 없음 출력은 `결과`와 `Confluence 변경` 다음에 URL 또는 실패/스킵 사유를 먼저 보여준다. parent 상세, fingerprint, operation id는 그 뒤에 둔다.
- 성공한 page와 실패한 page를 섞어 숨기지 않는다.
- 일부 실패가 있으면 결과를 `부분 완료`로 표시한다.
- 업데이트 결과에는 이전 version과 새 version을 함께 표시한다.
- `변경 없음` page는 생성/수정 count와 별도로 표시한다.
- 모든 생성/수정 page title에는 `v0.7`이 포함되어야 한다.
- readback 실패를 성공처럼 표현하지 않는다.
