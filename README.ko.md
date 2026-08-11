# Woohyuk Coding Plugin

[English](README.md) | [한국어](README.ko.md)

전문 설계자, 코드 작성자, 리뷰어, 테스터 서브 에이전트와 코드 리뷰, 대화형 변경사항 설명, Pencil 디자인 구현, 문서화, 구현 계획 수립과 실행, PR 준비, 변경 기록, 테스트 계획, 공개 배포 점검, 시각적 QA, 커밋 메시지 작성, 로컬 LLM 위키 검색 워크플로를 제공하는 개인용 Codex 플러그인입니다.

## 마켓플레이스 및 설치

이 저장소는 Codex 플러그인 마켓플레이스로 구성되어 있습니다. 카탈로그는 `.agents/plugins/marketplace.json`에 정의되어 있으며, 마켓플레이스 이름은 `woohyuk`, 플러그인 이름은 `woohyuk-coding-plugin`입니다.

GitHub 저장소를 Codex 플러그인 마켓플레이스로 추가한 뒤 플러그인을 설치합니다.

```bash
codex plugin marketplace add dngur6344/woohyuk-coding-plugin --ref main
codex plugin add woohyuk-coding-plugin@woohyuk
```

설치한 스킬이 로드되도록 새 Codex 세션을 시작합니다.

`$woohyuk-install-subagents`를 한 번 실행하여 번들된 커스텀 역할을 `~/.codex/agents/` 아래에 설치한 후, 역할이 탐색되도록 Codex 세션을 다시 시작합니다. 플러그인 manifest만으로는 커스텀 Codex 에이전트 TOML이 자동 등록되지 않습니다.

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

- `$woohyuk-install-subagents`: 번들된 설계자, 코드 작성자, 리뷰어, 테스터 역할을 개인 또는 프로젝트 범위에 설치합니다.
- `$woohyuk-review-code`: diff, PR, 작업 트리 변경사항에서 구체적인 버그, 회귀, 테스트 누락을 검토합니다.
- `$woohyuk-explain-diff`: diff, 커밋, 브랜치, PR을 대화형 단일 HTML 문서로 설명합니다.
- `$woohyuk-pencil-design-implementation`: Pencil MCP 도구로 `.pen` 파일을 사용하고 디자인을 코드로 구현합니다.
- `$woohyuk-maintain-readme`: 저장소에 있는 근거를 바탕으로 README를 생성하거나 업데이트합니다.
- `$woohyuk-document-project-architecture`: `docs/` 아래에 구조화된 프로젝트 아키텍처 문서를 작성합니다.
- `$woohyuk-write-adr`: `docs/adr/` 아래에 Architecture Decision Record를 작성합니다.
- `$woohyuk-plan`: `.woohyuk/plan.md`에 하나의 활성 하위 목표 기반 구현 계획을 작성합니다.
- `$woohyuk-ralph`: 활성 계획의 하위 목표를 하나씩 구현하고 검증한 뒤 완료 기록을 `docs/`에 보관하고 활성 계획을 삭제합니다.
- `$woohyuk-create-test-plan`: 변경사항과 위험 영역을 바탕으로 집중된 테스트 계획을 작성합니다.
- `$woohyuk-visual-qa`: 관련 뷰포트에서 렌더링된 프론트엔드의 시각적 QA를 수행합니다.
- `$woohyuk-public-release-check`: 저장소를 공개하기 전에 배포 준비 상태를 점검합니다.
- `$woohyuk-commit-message`: staged 또는 unstaged diff를 바탕으로 커밋 메시지를 작성합니다.
- `$woohyuk-prepare-pr`: PR 제목, 본문, 체크리스트, 위험 요소, 테스트 내용을 작성합니다.
- `$woohyuk-update-changelog`: 변경 기록과 릴리스 노트를 생성하거나 업데이트합니다.
- `$woohyuk-docs-consistency-check`: 오래되었거나 서로 모순되는 문서를 찾습니다.
- `$woohyuk-search-llm-wiki`: 로컬 LLM 위키에서 관련 지식을 검색하고 참조합니다.

## 전문 서브 에이전트

| 역할 | 모델 | 책임 |
| --- | --- | --- |
| `woohyuk-architect` | `gpt-5.6-sol` / `xhigh` | 읽기 전용으로 아키텍처, 경계, 흐름, 위험과 구현 방향을 설계합니다. |
| `woohyuk-implementer` | `gpt-5.6-sol` / `xhigh` | 명확하게 할당받은 Ralph 소목표 하나를 구현합니다. |
| `woohyuk-reviewer` | `gpt-5.6-sol` / `xhigh` | 읽기 전용으로 계획과 코드를 검토하여 정확성, 실행 가능성, 검증 누락을 찾습니다. |
| `woohyuk-tester` | `gpt-5.6-terra` / `high` | 요구사항을 독립적으로 테스트하고 재현 가능한 통과 또는 실패 근거를 반환합니다. |

`$woohyuk-plan`은 설계자에게 코드베이스에 맞는 설계를 요청하고 메인 스레드에서 초안을 작성한 뒤 리뷰어에게 검증받습니다. `$woohyuk-ralph`는 각 소목표를 한 명의 코드 작성자에게 할당하고 테스터가 `PASS`를 반환한 경우에만 다음 목표로 진행하며, 마지막에는 전체 계획을 다시 검증합니다.

서브 에이전트는 각각 별도의 모델 및 도구 작업을 수행하므로 단일 에이전트 실행보다 토큰을 더 사용합니다. 공유 작업 트리에서는 한 번에 한 명의 코드 작성자만 작업합니다.

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
