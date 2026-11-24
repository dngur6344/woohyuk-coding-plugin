# Woohyuk Coding Plugin

[English](README.md) | [한국어](README.ko.md)

아키텍처, 구현, 리뷰, 테스트와 근거 기반 문서화를 담당하는 8개의 전문 에이전트와 코드 리뷰, 대화형 변경사항 설명, Pencil 및 FigCraft 디자인 작업, 계획 수립과 실행, PR 준비, 배포 점검, 로컬 LLM 위키 검색 워크플로를 제공하는 개인용 Codex 플러그인입니다.

## 마켓플레이스 및 설치

이 저장소는 Codex 플러그인 마켓플레이스로 구성되어 있습니다. 카탈로그는 `.agents/plugins/marketplace.json`에 정의되어 있으며, 마켓플레이스 이름은 `woohyuk`, 플러그인 이름은 `woohyuk-coding-plugin`입니다.

GitHub 저장소를 Codex 플러그인 마켓플레이스로 추가한 뒤 플러그인을 설치합니다.

```bash
codex plugin marketplace add dngur6344/woohyuk-coding-plugin --ref main
codex plugin add woohyuk-coding-plugin@woohyuk
```

설치한 스킬이 로드되도록 새 Codex 세션을 시작합니다.

플러그인을 설치하거나 업그레이드할 때마다 `$woohyuk-install-subagents`를 다시 실행하여 현재 번들된 8개 역할을 `~/.codex/agents/` 아래에 설치합니다. 보고된 사용자 수정 충돌을 모두 검토하고, 보고된 역할 파일을 모두 교체하도록 승인한 경우에만 `--force`를 사용한 뒤 Codex를 다시 시작합니다. 이전 버전 설치는 이 과정을 거치지 않으면 기존에 설치한 역할 정의를 그대로 유지합니다. 플러그인 manifest는 커스텀 에이전트 TOML을 자동으로 업데이트하지 않습니다.

마켓플레이스와 플러그인이 정상적으로 등록되었는지 확인하려면 다음 명령을 실행합니다.

```bash
codex plugin marketplace list
codex plugin list --marketplace woohyuk
```

마켓플레이스 스냅샷을 갱신하고 최신 플러그인 버전을 설치하려면 다음 명령을 실행합니다.

```bash
codex plugin marketplace upgrade woohyuk
codex plugin add woohyuk-coding-plugin@woohyuk
```

## 스킬

- `$woohyuk-install-subagents`: 번들된 코드 및 문서화 역할 8개를 개인 또는 프로젝트 범위에 설치합니다.
- `$woohyuk-review-code`: diff, PR, 작업 트리 변경사항에서 구체적인 버그, 회귀, 테스트 누락을 검토합니다.
- `$woohyuk-explain-diff`: diff, 커밋, 브랜치, PR을 대화형 단일 HTML 문서로 설명합니다.
- `$woohyuk-pencil-design-implementation`: Pencil MCP 도구로 `.pen` 파일을 사용하고 디자인을 코드로 구현합니다.
- `$woohyuk-figcraft-cli`: 로컬 CLI로 FigCraft 앱의 네이티브 디자인을 생성·조회·수정·렌더링·내보내기하고, 요청한 경우에만 코드를 추출합니다.
- `$woohyuk-maintain-readme`: 저장소에 있는 근거를 바탕으로 README를 생성하거나 업데이트합니다.
- `$woohyuk-document-project-architecture`: `docs/` 아래에 구조화된 프로젝트 아키텍처 문서를 작성합니다.
- `$woohyuk-write-adr`: `docs/adr/` 아래에 Architecture Decision Record를 작성합니다.
- `$woohyuk-plan`: ADR, 아키텍처, README, 변경 기록 영향 판단을 포함한 활성 하위 목표 기반 구현 계획을 작성합니다.
- `$woohyuk-ralph`: 활성 계획을 구현 및 테스트하고 문서화 레인과 리뷰 관문을 거친 뒤 승인된 기록을 보관합니다.
- `$woohyuk-create-test-plan`: 변경사항과 위험 영역을 바탕으로 집중된 테스트 계획을 작성합니다.
- `$woohyuk-visual-qa`: 관련 뷰포트에서 렌더링된 프론트엔드의 시각적 QA를 수행합니다.
- `$woohyuk-public-release-check`: 저장소를 공개하기 전에 배포 준비 상태를 점검합니다.
- `$woohyuk-commit-message`: staged 또는 unstaged diff를 바탕으로 커밋 메시지를 작성합니다.
- `$woohyuk-prepare-pr`: PR 제목, 본문, 체크리스트, 위험 요소, 테스트 내용을 작성합니다.
- `$woohyuk-update-changelog`: 변경 기록과 릴리스 노트를 생성하거나 업데이트합니다.
- `$woohyuk-docs-consistency-check`: 오래되었거나 서로 모순되는 문서를 찾습니다.
- `$woohyuk-search-llm-wiki`: 로컬 LLM 위키에서 관련 지식을 검색하고 참조합니다.

## FigCraft CLI

`$woohyuk-figcraft-cli`는 Figma 자동화가 아니라 FigCraft 앱과 로컬 `.figcraft` 파일을 대상으로 합니다. FigCraft 앱과 `figcraft-cli`는 별도로 설치하며 플러그인에 포함하지 않습니다. 사용자가 지정한 실행 파일 경로를 우선 사용하고, 지정하지 않으면 `PATH`와 로컬 설치 경로를 찾습니다. 수동 설치 시 배포 폴더 전체를 `~/.local/opt/figcraft-cli/0.12.1/`에 보관하고 실행 파일을 `~/.local/bin/figcraft-cli`로 심볼릭 링크하는 구성을 권장합니다(macOS CLI 0.12.1에서 확인). `~/.local/bin`을 `PATH`에 포함한 뒤 `command -v figcraft-cli`와 `figcraft-cli --version`으로 확인합니다.

헤드리스 CLI 작업은 파일을 저장하며, FigCraft에서 이미 열린 탭을 자동으로 갱신하지는 않습니다. 수정 결과를 검증하는 동안 원본을 보존하고, 결과 파일을 FigCraft 앱에서 열어 확인할 수 있도록 구성했습니다. 공유·게시·실행 중인 앱 연결은 자동으로 활성화하지 않습니다.

## 전문 서브 에이전트

8개 역할은 생성 시 또는 `[agents].default_subagent_model`에 별도 모델을 지정하지 않으면 메인 세션의 모델을 상속합니다. 추론 수준은 역할별로 고정합니다.

| 역할 | 추론 수준 | 책임 |
| --- | --- | --- |
| `woohyuk-architect` | `xhigh` | 읽기 전용으로 아키텍처, 경계, 흐름, 위험과 구현 방향을 설계합니다. |
| `woohyuk-implementer` | `high` | 명확하게 할당받은 Ralph 소목표 하나를 구현합니다. |
| `woohyuk-reviewer` | `xhigh` | 읽기 전용으로 계획, 코드, 최종 문서를 검토합니다. |
| `woohyuk-tester` | `high` | 요구사항을 독립적으로 테스트하고 재현 가능한 통과 또는 실패 근거를 반환합니다. |
| `woohyuk-adr-documenter` | `high` | 최종 diff와 테스트 근거를 바탕으로 할당된 ADR 경로만 작성합니다. |
| `woohyuk-architecture-documenter` | `high` | 할당된 아키텍처 문서 경로만 업데이트합니다. |
| `woohyuk-readme-documenter` | `high` | 검증된 동작을 바탕으로 할당된 README 경로만 업데이트합니다. |
| `woohyuk-changelog-documenter` | `medium` | 할당된 변경 기록 또는 릴리스 노트 경로만 업데이트합니다. |

`$woohyuk-plan`은 `xhigh`를 사용하는 `woohyuk-architect`에게 코드베이스에 맞는 설계를 요청하고 메인 스레드에서 초안을 작성한 뒤 리뷰어에게 검증받습니다. 모든 계획은 ADR, 아키텍처, README, 변경 기록 레인마다 `Yes` 또는 `No`, 정확한 소유 경로, 근거 기반 이유, 예상 업데이트를 기록합니다. 계획 단계에서는 일반적으로 최종 문서를 작성하지 않습니다.

`$woohyuk-ralph`는 `high`를 사용하는 `woohyuk-implementer`로 구현합니다. 테스터가 `PASS`를 반환한 경우에만 각 코드 소목표를 진행하고, 마지막에는 실제 diff를 기준으로 네 문서화 레인을 다시 판단합니다. 필요한 문서 작성자는 용량이 허용되는 범위에서 병렬로 실행하며, 읽기 전용 리뷰어가 `DOC_REVIEW APPROVE`를 반환하면 완료된 작업 이력을 `docs/YYYY-MM-DD-feature-slug/worklog.md`에 보관합니다. 문서 결함은 관련 레인만 다시 실행하고, 확정된 코드 결함은 코드를 다시 열어 이전 문서 근거를 모두 무효화합니다.

검증 범위는 단계별로 나눕니다. 구현자는 변경 부분의 빠른 점검을, 독립 테스터는 소목표의 인수 조건 검증을, 전체 계획 검증은 통합 동작과 필수 광범위 검증을 담당합니다. 독립 검증된 결과는 관련 입력과 환경이 바뀌지 않은 경우에만 재사용하며, 필수 검증과 수행 시점을 임의로 생략하지 않습니다. 문서 리뷰에서는 제품 테스트를 다시 실행하지 않고 현재 검증 근거와 문서 내용의 일치 여부를 확인합니다.

각 에이전트는 별도의 모델 및 도구 작업을 수행하므로 설계, 테스트, 문서화, 리뷰 단계는 단일 에이전트 실행보다 토큰을 더 사용합니다. 코드 작성자는 한 번에 한 명만 실행합니다. 문서 경로 소유권은 전체 레인에서 서로 겹치지 않아야 하며, 공유 README나 인덱스는 레인 하나만 소유하고 그 레인의 예상 업데이트에 모든 교차 레인 내용을 포함합니다. 용량에 따라 서로 겹치지 않는 레인을 여러 병렬 배치로 나눌 수 있으며, 문서 작성자는 코드, 테스트, 활성 계획, 보관 계획을 수정할 수 없습니다.

## Codex CLI 상태 표시줄

Codex CLI 상태 표시줄 항목은 플러그인 manifest가 아니라 `~/.codex/config.toml`에서 설정합니다. 이 플러그인은 설정에 대한 참고 정보를 제공하며, 실제 하단 상태 표시줄은 `[tui]`에 다음과 같이 적용합니다.

```toml
[tui]
status_line = [ "model-with-reasoning", "current-dir", "context-used", "context-remaining", "five-hour-limit", "weekly-limit" ]
```

`context-used`는 현재 사용한 컨텍스트의 양을, `context-remaining`은 남아 있는 컨텍스트 용량을 표시합니다.

## 구조

```text
.agents/plugins/marketplace.json
.codex-plugin/plugin.json
README.md
README.ko.md
skills/
  woohyuk-install-subagents/
  woohyuk-review-code/
  woohyuk-explain-diff/
  woohyuk-pencil-design-implementation/
  woohyuk-figcraft-cli/
  woohyuk-maintain-readme/
  woohyuk-document-project-architecture/
  woohyuk-write-adr/
  woohyuk-plan/
  woohyuk-ralph/
  woohyuk-create-test-plan/
  woohyuk-visual-qa/
  woohyuk-public-release-check/
  woohyuk-commit-message/
  woohyuk-prepare-pr/
  woohyuk-update-changelog/
  woohyuk-docs-consistency-check/
  woohyuk-search-llm-wiki/
```

## 공개 저장소 참고사항

이 저장소는 `.agents/plugins/` 아래의 공개 마켓플레이스 카탈로그만 추적합니다. 그 밖의 로컬 Codex 상태, 환경 파일, 인증 정보, `.pen` 디자인 파일은 제외합니다.
