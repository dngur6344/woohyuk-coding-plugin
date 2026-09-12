# Woohyuk Coding Plugin

[English](README.md) | [한국어](README.ko.md)

Personal Codex plugin with ten specialized agents for architecture, implementation, review, testing, and evidence-backed documentation, plus workflows for code review, interactive diff explanations, Pencil design implementation, planning, plan execution, PR preparation, release checks, and local LLM wiki lookup.

## Marketplace and Installation

This repository is a Codex plugin marketplace. Its catalog is defined in `.agents/plugins/marketplace.json` with the marketplace name `woohyuk` and the plugin name `woohyuk-coding-plugin`.

Add the GitHub repository as a Codex plugin marketplace, then install the plugin:

```bash
codex plugin marketplace add dngur6344/woohyuk-coding-plugin --ref main
codex plugin add woohyuk-coding-plugin@woohyuk
```

Start a new Codex session after installation so the bundled skills are loaded.

After installing or upgrading the plugin, rerun `$woohyuk-install-subagents` to install the current ten bundled roles under `~/.codex/agents/`. Review every reported customization conflict and use `--force` only when approving replacement of all reported role files, then restart Codex so the roles are rediscovered. Older installations otherwise retain their previously installed role definitions because plugin manifests do not automatically update custom-agent TOML files.

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

- `$woohyuk-install-subagents`: Install all ten bundled code and documentation roles for personal or project use.
- `$woohyuk-review-code`: Review diffs, PRs, and working-tree changes for concrete bugs, regressions, and test gaps.
- `$woohyuk-explain-diff`: Explain a diff, commit, branch, or PR as an interactive self-contained HTML document.
- `$woohyuk-pencil-design-implementation`: Use Pencil `.pen` files through Pencil MCP tools, then implement the design in code.
- `$woohyuk-maintain-readme`: Create or update README content from repository evidence.
- `$woohyuk-document-project-architecture`: Create structured project architecture documentation under `docs/`.
- `$woohyuk-write-adr`: Write Architecture Decision Records under `docs/adr/`.
- `$woohyuk-plan`: Create the active subgoal-based plan with required ADR, architecture, README, and changelog impact decisions.
- `$woohyuk-ralph`: Implement and test the active plan, run its documentation lanes and review gate, then archive the approved record.
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
| `woohyuk-astra-architect` | `gpt-6-astra` / `medium` | Plan-stage architect selected when the root session uses GPT-6 Astra. |
| `woohyuk-astra-implementer` | `gpt-6-astra` / `medium` | Ralph implementer selected when the root session uses GPT-6 Astra. |
| `woohyuk-reviewer` | `gpt-5.6-sol` / `xhigh` | Read-only plan, code, and final documentation review. |
| `woohyuk-tester` | `gpt-5.6-terra` / `high` | Independently test requirements and return reproducible pass or fail evidence. |
| `woohyuk-adr-documenter` | `gpt-5.6-sol` / `xhigh` | Write only assigned ADR paths from the final diff and test evidence. |
| `woohyuk-architecture-documenter` | `gpt-5.6-sol` / `xhigh` | Update only assigned architecture documentation paths. |
| `woohyuk-readme-documenter` | `gpt-5.6-terra` / `high` | Update only assigned README paths from verified behavior. |
| `woohyuk-changelog-documenter` | `gpt-5.6-terra` / `medium` | Update only assigned changelog or release-note paths. |

`$woohyuk-plan` asks the architect to propose a codebase-aligned design, writes the draft in the main thread, and has the reviewer validate it. When the root session's actual model is `gpt-6-astra`, it selects `woohyuk-astra-architect`; otherwise it retains `woohyuk-architect` on `gpt-5.6-sol`. Astra specialist substitutions use two lower reasoning levels than the equivalent GPT-5.6 Sol role (`xhigh` to `medium`, `high` to `low`). Every plan records `Yes` or `No`, exact owned paths, an evidence-based reason, and the expected update for ADR, architecture, README, and changelog lanes. The planner normally leaves final documentation to Ralph.

`$woohyuk-ralph` selects `woohyuk-astra-implementer` when the root session's actual model is `gpt-6-astra`; otherwise it retains `woohyuk-implementer` on `gpt-5.6-sol`. The same two-step-lower Astra reasoning policy applies to implementation. It advances each code subgoal only after tester `PASS`, then reconciles the four documentation lanes against the actual diff. Required documenters run in parallel as capacity permits, and the read-only reviewer must return `DOC_REVIEW APPROVE` before archival. Documentation defects rerun only implicated lanes; a confirmed code defect reopens code and invalidates all prior documentation evidence.

The routing helper reads the active session record identified by `CODEX_SESSION_ID` or `CODEX_THREAD_ID`. It does not use the default model in `~/.codex/config.toml`, because a session-level model selection may differ. If the active model cannot be resolved, both workflows use the existing GPT-5.6 roles.

Each agent performs separate model and tool work, so the architecture, test, documentation, and review passes use more tokens than a single-agent run. Only one implementer writes code at a time. Documentation paths are globally pairwise-disjoint: a shared README or index belongs to exactly one lane whose expected update includes all cross-lane content. Capacity may split disjoint lanes into multiple parallel batches, and no documenter may edit code, tests, the active plan, or its archive.

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
