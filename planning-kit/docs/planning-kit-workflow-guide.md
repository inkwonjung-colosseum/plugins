# planning-kit 상세 workflow

> workflow 상세 설명 문서
> 최종 수정일: 2026-05-12
> 기준 버전: 0.2.14
> 대상: planning-kit 실행 담당, 기획/개발/디자인/QA/운영 리뷰어

---

## 1. 전체 workflow

`planning-kit`은 변환, 리뷰, 후보 발행 세 단계로 동작하고, 필요할 때 기준 문서 묶음 자체를 별도로 감사합니다.

```mermaid
flowchart LR
  A["기획 초안<br/>텍스트 / 파일 / URL / 이미지"] --> B["planning-format"]
  B --> C["저장 파일<br/>정책서 + 기능설계서"]
  B --> D["체크해야 할 항목"]
  C --> E["planning-review"]
  E --> F["결론"]
  E --> G["검토 결과"]
  E --> H["체크해야 할 항목"]
  C --> P["planning-publish-confluence<br/>명시적 저장 폴더"]
  F --> P
  G --> P
  P --> Q["Confluence<br/>[기능명] v0.7"]
  R["SSOT 표시 폴더"] --> S["ssot-audit"]
```

핵심 메시지:

- `planning-format`은 문서를 만들고 기본 저장 파일을 남깁니다.
- `planning-review`는 저장 파일 또는 두 본문을 기준 문서와 비교하고 결론/검토 결과를 먼저 보여줍니다.
- `planning-publish-confluence`는 context memory 또는 명시적 저장 폴더만 발행 후보로 사용합니다.
- 최종 v1.0 확정은 기획팀과 실무팀 리뷰 이후 Confluence `[SSOT]`에서 합니다.

## 2. planning-format 흐름

0.2.14부터 `planning-format`은 저장 기본값입니다. `--no-save`를 지정한 경우에만 저장하지 않고 정책서·기능설계서 전문을 화면에 펼칩니다.

```mermaid
flowchart LR
  A["입력 dispatch"] --> B["URL·이미지 추출"]
  B --> C["자료 수집"]
  C --> D["정책서·기능설계서 변환"]
  D --> E["F1~F6 자체 검증"]
  E --> F{"--no-save?"}
  F -->|"아니오"| G["planning/[안전기능명]--YYYY-MM-DD-HHMMSS/<br/>저장 파일 생성"]
  F -->|"예"| H["화면 본문 출력"]
  G --> I["## 저장 파일<br/>## 체크해야 할 항목"]
  H --> J["## 정책서<br/>## 기능설계서<br/>## 체크해야 할 항목"]
  G --> K{"저장 실패?"}
  K -->|"예"| L["본문 fallback<br/>## 저장 실패 상세"]
```

기본 저장 성공 출력은 `# [기능명]` 헤더 다음에 `## 저장 파일`, `## 체크해야 할 항목`만 둡니다. 저장 파일에는 체크리스트, 출처/누락 요약, 상세 추적, 저장 실패 상세를 쓰지 않습니다.

## 3. planning-review 흐름

0개 인자 실행에서는 직전 `planning-format` 출력에서 본문 또는 저장 파일 handoff를 찾습니다.

```mermaid
flowchart LR
  A["review 입력"] --> B{"입력 형태"}
  B -->|"인자 없음 + 본문"| C["context 본문 추출"]
  B -->|"인자 없음 + ## 저장 파일"| D["저장 파일 handoff"]
  B -->|"저장 폴더"| E["canonical 두 파일"]
  B -->|"파일 / URL / Markdown"| F["본문 수집·분리"]
  C --> G["정책서 + 기능설계서"]
  D --> G
  E --> G
  F --> G
  G --> H["R1 SSOT 충돌"]
  G --> I["R2 AC 검증가능성"]
  G --> J["R3 의존·영향"]
  H --> K["결론"]
  I --> K
  J --> K
  K --> L["검토 결과"]
  L --> M["체크해야 할 항목"]
```

저장 파일 handoff 허용 형식은 `- 정책서: <path>`, `- 기능설계서: <path>`, `- [정책서](<path>)`, `- [기능설계서](<path>)`입니다. 두 파일이 정확히 1개 `planning/[안전기능명]--YYYY-MM-DD-HHMMSS/` 폴더를 가리키지 않으면 임의 선택하지 않습니다.

## 4. planning-publish-confluence 흐름

```mermaid
flowchart LR
  A["입력"] --> B{"형태"}
  B -->|"인자 없음"| C["context memory gate"]
  B -->|"planning/[기능]--timestamp/"| D["저장 폴더 gate"]
  B -->|"그 외"| X["발행 취소"]
  C --> E["parent 선택"]
  D --> E
  E --> F["parent preflight"]
  F --> G["최종 확인"]
  G --> H["Confluence create/update"]
  H --> I["readback 검증"]
```

저장 폴더 입력은 repo root 기준 direct child만 허용합니다. `planning/foo/`, `planning/drafts/...`, 중첩 폴더, URL, 임의 `.md` 파일은 거부합니다. 저장 폴더에서 읽는 것은 canonical 정책서·기능설계서 두 파일뿐이며, `## 저장 파일`, `## 체크해야 할 항목`, `## 검토 결과`, `## 저장 실패 상세` 같은 report section은 child page body로 발행하지 않습니다.

## 5. SSOT 경계

`planning/**`과 `.planning-kit/**`은 review 대상 입력이나 발행 후보 입력으로는 사용할 수 있지만, 기준 문서 묶음 근거로는 쓰지 않습니다. 기준 문서 묶음은 폴더명에 독립 `SSOT` 표시가 있는 하위 폴더의 Markdown만 사용합니다.
