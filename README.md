# Woohyuk Coding Plugin

Personal Codex plugin with workflows for code review, interactive diff explanations, Pencil design implementation, documentation, implementation planning, plan execution, PR preparation, changelogs, test planning, public release checks, visual QA, commit messages, and local LLM wiki lookup.

## Installation

Add the GitHub repository as a Codex plugin marketplace, then install the plugin:

```bash
codex plugin marketplace add dngur6344/woohyuk-coding-plugin --ref main
codex plugin add woohyuk-coding-plugin@woohyuk
```

Start a new Codex session after installation so the bundled skills are loaded.

To refresh the marketplace and reinstall the latest plugin version:

```bash
codex plugin marketplace upgrade woohyuk
codex plugin add woohyuk-coding-plugin@woohyuk
```

## Skills

- `$woohyuk-review-code`: Review diffs, PRs, and working-tree changes for concrete bugs, regressions, and test gaps.
- `$woohyuk-explain-diff`: Explain a diff, commit, branch, or PR as an interactive self-contained HTML document.
- `$woohyuk-pencil-design-implementation`: Use Pencil `.pen` files through Pencil MCP tools, then implement the design in code.
- `$woohyuk-maintain-readme`: Create or update README content from repository evidence.
- `$woohyuk-document-project-architecture`: Create structured project architecture documentation under `docs/`.
- `$woohyuk-write-adr`: Write Architecture Decision Records under `docs/adr/`.
- `$woohyuk-plan`: Create subgoal-based implementation plan documents under `docs/`.
- `$woohyuk-ralph`: Implement saved plans one verified subgoal at a time until complete.
- `$woohyuk-create-test-plan`: Create focused test plans from changes and risk areas.
- `$woohyuk-visual-qa`: Run rendered frontend visual QA across relevant viewports.
- `$woohyuk-public-release-check`: Check a repository before publishing it publicly.
- `$woohyuk-commit-message`: Draft commit messages from staged or unstaged diffs.
- `$woohyuk-prepare-pr`: Draft PR titles, bodies, checklists, risks, and testing notes.
- `$woohyuk-update-changelog`: Create or update changelog and release-note entries.
- `$woohyuk-docs-consistency-check`: Find stale or contradictory documentation.
- `$woohyuk-search-llm-wiki`: Search and reference the local LLM wiki for relevant knowledge.

## Codex CLI Status Line

Codex CLI status-line items live in `~/.codex/config.toml`, not in a plugin manifest. Keep this plugin as the reminder/reference point, but apply the actual footer through `[tui]`:

```toml
[tui]
status_line = [ "model-with-reasoning", "current-dir", "context-used", "context-remaining", "five-hour-limit", "weekly-limit" ]
```

Use `context-used` to see how full the current context is, and `context-remaining` to keep the remaining capacity visible.

## Structure

```text
.agents/plugins/marketplace.json
.codex-plugin/plugin.json
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

## Public Repository Notes

This repository tracks only the public marketplace catalog under `.agents/plugins/`. It excludes other local Codex state, environment files, credentials, and `.pen` design files.
