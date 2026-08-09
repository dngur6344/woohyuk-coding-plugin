# Woohyuk Coding Plugin

[English](README.md) | [한국어](README.ko.md)

코드 리뷰, 대화형 변경사항 설명, Pencil 디자인 구현, 문서화, 구현 계획 수립과 실행, PR 준비, 변경 기록, 테스트 계획, 공개 배포 점검, 시각적 QA, 커밋 메시지 작성, 로컬 LLM 위키 검색을 위한 개인용 Codex 플러그인입니다.

## 마켓플레이스 및 설치

이 저장소는 Codex 플러그인 마켓플레이스로 구성되어 있습니다. 카탈로그는 `.agents/plugins/marketplace.json`에 정의되어 있으며, 마켓플레이스 이름은 `woohyuk`, 플러그인 이름은 `woohyuk-coding-plugin`입니다.

GitHub 저장소를 Codex 플러그인 마켓플레이스로 추가한 뒤 플러그인을 설치합니다.

```bash
codex plugin marketplace add dngur6344/woohyuk-coding-plugin --ref main
codex plugin add woohyuk-coding-plugin@woohyuk
```

설치한 스킬이 로드되도록 새 Codex 세션을 시작합니다.

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

- `$woohyuk-review-code`: diff, PR, 작업 트리 변경사항에서 구체적인 버그, 회귀, 테스트 누락을 검토합니다.
- `$woohyuk-explain-diff`: diff, 커밋, 브랜치, PR을 대화형 단일 HTML 문서로 설명합니다.
- `$woohyuk-pencil-design-implementation`: Pencil MCP 도구로 `.pen` 파일을 사용하고 디자인을 코드로 구현합니다.
- `$woohyuk-maintain-readme`: 저장소에 있는 근거를 바탕으로 README를 생성하거나 업데이트합니다.
- `$woohyuk-document-project-architecture`: `docs/` 아래에 구조화된 프로젝트 아키텍처 문서를 작성합니다.
- `$woohyuk-write-adr`: `docs/adr/` 아래에 Architecture Decision Record를 작성합니다.
- `$woohyuk-plan`: `docs/` 아래에 하위 목표 기반 구현 계획 문서를 작성합니다.
- `$woohyuk-ralph`: 저장된 계획의 하위 목표를 하나씩 구현하고 검증하며 완료할 때까지 실행합니다.
- `$woohyuk-create-test-plan`: 변경사항과 위험 영역을 바탕으로 집중된 테스트 계획을 작성합니다.
- `$woohyuk-visual-qa`: 관련 뷰포트에서 렌더링된 프론트엔드의 시각적 QA를 수행합니다.
- `$woohyuk-public-release-check`: 저장소를 공개하기 전에 배포 준비 상태를 점검합니다.
- `$woohyuk-commit-message`: staged 또는 unstaged diff를 바탕으로 커밋 메시지를 작성합니다.
- `$woohyuk-prepare-pr`: PR 제목, 본문, 체크리스트, 위험 요소, 테스트 내용을 작성합니다.
- `$woohyuk-update-changelog`: 변경 기록과 릴리스 노트를 생성하거나 업데이트합니다.
- `$woohyuk-docs-consistency-check`: 오래되었거나 서로 모순되는 문서를 찾습니다.
- `$woohyuk-search-llm-wiki`: 로컬 LLM 위키에서 관련 지식을 검색하고 참조합니다.

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
