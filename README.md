# Woohyuk Coding Plugin

[English](README.md) | [한국어](README.ko.md)

Personal Codex plugin with specialized architect, implementer, reviewer, and tester subagents plus workflows for code review, interactive diff explanations, Pencil design implementation, documentation, implementation planning, plan execution, PR preparation, changelogs, test planning, public release checks, visual QA, commit messages, and local LLM wiki lookup.

## Marketplace and Installation

This repository is a Codex plugin marketplace. Its catalog is defined in `.agents/plugins/marketplace.json` with the marketplace name `woohyuk` and the plugin name `woohyuk-coding-plugin`.

Add the GitHub repository as a Codex plugin marketplace, then install the plugin:

```bash
codex plugin marketplace add dngur6344/woohyuk-coding-plugin --ref main
codex plugin add woohyuk-coding-plugin@woohyuk
```

Start a new Codex session after installation so the bundled skills are loaded.

Run `$woohyuk-install-subagents` once to install the bundled custom roles under `~/.codex/agents/`, then start another Codex session so the roles are discovered. Plugin manifests do not automatically register custom Codex agent TOML files.

To confirm that the marketplace and plugin are available:

```bash
codex plugin marketplace list
codex plugin list --marketplace woohyuk
```

To refresh the marketplace snapshot and install the latest plugin version:

```bash
codex plugin marketplace upgrade woohyuk
codex plugin add woohyuk-coding-plugin@woohyuk
```

## Skills

- `$woohyuk-install-subagents`: Install the bundled architect, implementer, reviewer, and tester roles for personal or project use.
- `$woohyuk-review-code`: Review diffs, PRs, and working-tree changes for concrete bugs, regressions, and test gaps.
- `$woohyuk-explain-diff`: Explain a diff, commit, branch, or PR as an interactive self-contained HTML document.
- `$woohyuk-pencil-design-implementation`: Use Pencil `.pen` files through Pencil MCP tools, then implement the design in code.
- `$woohyuk-maintain-readme`: Create or update README content from repository evidence.
- `$woohyuk-document-project-architecture`: Create structured project architecture documentation under `docs/`.
- `$woohyuk-write-adr`: Write Architecture Decision Records under `docs/adr/`.
- `$woohyuk-plan`: Create the single active, subgoal-based implementation plan at `.woohyuk/plan.md`.
- `$woohyuk-ralph`: Implement the active plan one verified subgoal at a time, archive the completed record under `docs/`, and remove the active plan.
- `$woohyuk-create-test-plan`: Create focused test plans from changes and risk areas.
- `$woohyuk-visual-qa`: Run rendered frontend visual QA across relevant viewports.
- `$woohyuk-public-release-check`: Check a repository before publishing it publicly.
- `$woohyuk-commit-message`: Draft commit messages from staged or unstaged diffs.
- `$woohyuk-prepare-pr`: Draft PR titles, bodies, checklists, risks, and testing notes.
- `$woohyuk-update-changelog`: Create or update changelog and release-note entries.
- `$woohyuk-docs-consistency-check`: Find stale or contradictory documentation.
- `$woohyuk-search-llm-wiki`: Search and reference the local LLM wiki for relevant knowledge.

## Specialized Subagents

| Role | Model | Responsibility |
| --- | --- | --- |
| `woohyuk-architect` | `gpt-5.6-sol` / `xhigh` | Read-only architecture, boundaries, flow, risks, and implementation guidance. |
| `woohyuk-implementer` | `gpt-5.6-sol` / `xhigh` | Implement one explicitly owned Ralph subgoal at a time. |
| `woohyuk-reviewer` | `gpt-5.6-sol` / `xhigh` | Read-only plan and code review for correctness, executability, and verification gaps. |
| `woohyuk-tester` | `gpt-5.6-terra` / `high` | Independently test requirements and return reproducible pass or fail evidence. |

`$woohyuk-plan` asks the architect to propose a codebase-aligned design, writes the draft in the main thread, and has the reviewer validate it. `$woohyuk-ralph` assigns each subgoal to one implementer and advances only after the tester returns `PASS`; the tester also runs the final whole-plan verification.

Subagents perform separate model and tool work, so these workflows use more tokens than a single-agent run. Only one implementer writes to the shared worktree at a time.

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

## Public Repository Notes

This repository tracks only the public marketplace catalog under `.agents/plugins/`. It excludes other local Codex state, environment files, credentials, and `.pen` design files.
