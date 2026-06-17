# Woohyuk Coding Plugin

Personal Codex plugin with workflows for code review, Pencil design implementation, documentation, PR preparation, changelogs, test planning, public release checks, visual QA, and commit messages.

## Skills

- `$review-code`: Review diffs, PRs, and working-tree changes for concrete bugs, regressions, and test gaps.
- `$pencil-design-implementation`: Use Pencil `.pen` files through Pencil MCP tools, then implement the design in code.
- `$maintain-readme`: Create or update README content from repository evidence.
- `$document-project-architecture`: Create structured project architecture documentation under `docs/`.
- `$write-adr`: Write Architecture Decision Records under `docs/adr/`.
- `$create-test-plan`: Create focused test plans from changes and risk areas.
- `$visual-qa`: Run rendered frontend visual QA across relevant viewports.
- `$public-release-check`: Check a repository before publishing it publicly.
- `$commit-message`: Draft commit messages from staged or unstaged diffs.
- `$prepare-pr`: Draft PR titles, bodies, checklists, risks, and testing notes.
- `$update-changelog`: Create or update changelog and release-note entries.
- `$docs-consistency-check`: Find stale or contradictory documentation.

## Codex CLI Status Line

Codex CLI status-line items live in `~/.codex/config.toml`, not in a plugin manifest. Keep this plugin as the reminder/reference point, but apply the actual footer through `[tui]`:

```toml
[tui]
status_line = [ "model-with-reasoning", "current-dir", "context-used", "context-remaining", "five-hour-limit", "weekly-limit" ]
```

Use `context-used` to see how full the current context is, and `context-remaining` to keep the remaining capacity visible.

## Structure

```text
.codex-plugin/plugin.json
skills/
  review-code/
  pencil-design-implementation/
  maintain-readme/
  document-project-architecture/
  write-adr/
  create-test-plan/
  visual-qa/
  public-release-check/
  commit-message/
  prepare-pr/
  update-changelog/
  docs-consistency-check/
```

## Public Repository Notes

This repository intentionally excludes local Codex state, marketplace files, environment files, credentials, and `.pen` design files.
