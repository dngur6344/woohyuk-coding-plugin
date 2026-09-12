---
name: woohyuk-plan
description: "Create the single active implementation plan at .woohyuk/plan.md before code changes. Use for implementation plans, task breakdowns, or roadmaps that Ralph can execute. Includes architect design, reviewer validation, verifiable subgoals, and required ADR, architecture, README, and changelog impact decisions."
---

# Write Active Implementation Plan

## Overview

Create one active implementation plan at `.woohyuk/plan.md` in the target repository. Use a read-only architect to shape the design and a separate read-only reviewer to validate the draft. Break work into small, verifiable subgoals and record the impact on ADR, architecture, README, and changelog documentation so `$woohyuk-ralph` can finish code and docs from explicit evidence. Do not create the dated `docs/` record during planning; Ralph creates it only after implementation, documentation review, and final verification succeed.

## Active Plan Guard

Check for `.woohyuk/plan.md` before planning new work.

- If the file does not exist, continue with the planning workflow.
- If it exists, read it and tell the user its title, status, and remaining subgoals. Do not overwrite or delete it silently.
- Ask the user to choose one of these actions:
  - Execute the existing plan with `$woohyuk-ralph` and do not create a new plan.
  - Discard the existing plan and create a new one. Explicitly confirm that its progress and unarchived results will be lost before deleting it.
  - Keep the existing plan and cancel the new planning request.
- Use an interactive selection tool when one is available. Otherwise, ask the same concise choices conversationally and wait for the answer.
- Keep exactly one active plan. Do not create alternate, numbered, dated, or backup plan files under `.woohyuk/`.

## Subagent Orchestration

Use both specialist roles for every new plan when multi-agent tools are available. They run sequentially because review depends on the draft.

1. Resolve the current root session model with the Model Routing rules below, then spawn the selected architect after implementation-affecting user decisions are confirmed. Give it a self-contained task containing the requirements, target repository, constraints, relevant evidence, and decisions. Ask for design boundaries, flow, risks, and suggested subgoals. Keep it read-only.
2. Synthesize the architect's evidence into the draft plan. The parent planner alone writes `.woohyuk/plan.md` with `status: draft` while review is pending.
3. Spawn `woohyuk-reviewer` in `PLAN_REVIEW` mode with the requirements and draft path. Require it to verify references, requirement coverage, subgoal independence, dependencies, executable verification, and every Documentation Impact rule below.
4. On `REVISE`, update the draft and resubmit it to the reviewer. Allow at most two revision rounds. If the second revision is not approved, set `status: blocked`, record the remaining review issues, and ask the user how to resolve them. On `BLOCKED`, do the same for the missing decision. Set `status: planned` only after `APPROVE`.
5. Wait for each specialist's result and incorporate evidence rather than copying its output blindly.

When spawning a named specialist, set `fork_turns: "none"` and provide a self-contained prompt instead of relying on inherited conversation context. If a named role is unavailable, use a generic read-only subagent with the same role contract and explicitly select these settings:

- Astra architect fallback: `gpt-6-astra`, `medium` when the resolved root model is exactly `gpt-6-astra`.
- Standard architect fallback: `gpt-5.6-sol`, `xhigh` for every other or unknown root model.
- Reviewer fallback: `gpt-5.6-sol`, `xhigh`.

Mention the fallback and recommend `$woohyuk-install-subagents`; do not block planning solely because named roles have not been installed. If no subagent can run, the parent must execute the same architect and reviewer contracts, disclose that fallback, and must not mark the plan `planned` without completing the review contract.

## Model Routing

Resolve the root session's actual model once before spawning the architect. Run `python3 ../woohyuk-install-subagents/scripts/resolve_current_model.py`, resolving the path relative to this skill directory.

- When it returns `status: detected` and `model: gpt-6-astra`, use `woohyuk-astra-architect` at `medium`.
- For every other model or `status: unknown`, use the existing `woohyuk-architect` at `gpt-5.6-sol`, `xhigh`.
- For an Astra specialist substitution, lower the equivalent GPT-5.6 Sol effort by two steps: `xhigh` becomes `medium`, and `high` becomes `low`.
- Keep `woohyuk-reviewer` at `gpt-5.6-sol`, `xhigh` in both profiles.
- Do not change the root session's effort or the effort of specialists that remain on non-Astra models.
- Do not infer the active model from `~/.codex/config.toml`; a session-level model selection may override that default.
- Record the selected profile and architect role in the final response.

## Workflow

1. Identify the target repository and read its local instructions first, including `AGENTS.md`, README files, package scripts, and existing ADR, architecture, README, and changelog conventions relevant to the requested feature.
2. Apply the Active Plan Guard before drafting or writing a new plan.
3. Classify the goal size as `small`, `medium`, or `large` based on scope, uncertainty, touched areas, and verification cost.
4. Identify decision points that affect implementation direction, scope, architecture, UX, data shape, dependencies, compatibility, migration strategy, or verification.
5. Ask the user to decide required decision points before drafting the plan. Do not silently choose between meaningful alternatives.
6. Run the architect stage from Subagent Orchestration.
7. Break the goal into independently implementable and verifiable subgoals using repository evidence, confirmed decisions, and the architect's result. For trivial work, use one subgoal.
8. Complete all four Documentation Impact rows from inspected repository evidence. Assign exact paths only when a lane is required and make path ownership pairwise-disjoint.
9. State low-risk assumptions in the plan only when they do not materially change implementation.
10. Derive a stable `feature_slug` in short kebab-case for Ralph's completed-plan archive.
11. Create `.woohyuk/` at the target repository root if needed.
12. Write the draft active plan to `.woohyuk/plan.md` with `status: draft`, then run the reviewer stage and revise as required. Change it to `planned` only after approval.
13. Do not implement code while using this skill unless the user explicitly asks for both planning and implementation. Never write final documentation during planning. The only planning-stage documentation exception is an explicitly required, confirmed architectural decision, which may be recorded as a `Proposed` ADR at an exact path.
14. In the final response, provide the active plan path, goal size, subgoal count, confirmed decisions, reviewer verdict, documentation impact summary, and main assumptions or open questions.

## Goal Sizing

Use these defaults:

- `small`: one focused code path or documentation change; usually 1 subgoal.
- `medium`: several files or one workflow with meaningful risk; usually 2-4 subgoals.
- `large`: cross-cutting behavior, migration, new architecture, or unclear dependencies; usually 4+ subgoals and more explicit risks.

Do not inflate plans with generic process steps. A subgoal must produce a concrete repository change or a concrete decision that unblocks implementation.

## Decision Handling

Ask the user when a decision would change what gets built or how it is built.

- Ask concise questions.
- Provide 2-3 concrete options when useful, including the tradeoff for each option.
- Use an interactive selection tool when available; otherwise ask conversationally.
- You may recommend an option, but the user makes the decision.
- Wait for the user's answer before writing a final plan when the decision affects implementation scope or direction.
- Record answered decisions in `## Decisions`.
- Use `## Open Questions` only for non-blocking questions or questions the user explicitly leaves unresolved.

## Naming

- Always use `.woohyuk/plan.md` for the active plan.
- Use the local date in `YYYY-MM-DD` format for `created` and `updated`. Run `date +%F` if the date is not already reliable.
- Derive `feature_slug` from the requested feature in short kebab-case.
- Korean slugs are acceptable when they are clearer for the project; replace whitespace with `-`.
- Keep `feature_slug` stable because Ralph uses it for `docs/YYYY-MM-DD-feature-slug/plan.md` after completion.

## Documentation Impact

Every plan must contain exactly one row for each lane: `ADR`, `Architecture`, `README`, and `Changelog`.

- `Required` is `Yes` or `No`.
- `Owned paths` is an exact repository-relative file list for `Yes`, or `None` for `No`. Do not use globs or directory-only ownership.
- `Reason` cites code, requirements, public behavior, or existing documentation conventions. A `No` needs affirmative evidence, not merely "not requested."
- `Expected update` states the content to add or change, or `None` for `No`.
- Paths must be pairwise-disjoint across required lanes. Assign a shared README, index, or release file to one lane only and mention any cross-lane content in that lane's expected update.

The reviewer must return `REVISE` when a lane is missing, a `No` is unsupported, a required lane lacks exact paths, or path ownership overlaps. Planning records expected final documentation; it does not write it except for the explicit `Proposed` ADR exception above.

## Plan Format

Use this structure unless the repository already has a stronger local convention:

```markdown
---
title: "<feature title>"
status: planned
created: YYYY-MM-DD
updated: YYYY-MM-DD
target_repo: "<repo path or name>"
goal_size: small|medium|large
feature_slug: "<feature-slug>"
---

# <feature title>

## Goal

<One or two sentences describing the outcome.>

## Assumptions

- <Assumption that affects implementation.>

## Decisions

- <Confirmed user decision, or "None">

## Scope

- <Included behavior or file area.>

## Out Of Scope

- <Explicit non-goal.>

## Current Evidence

- `<file>`: <Relevant observation.>

## Subgoals

- [ ] SG1: <Small objective>
  - Outcome: <Observable result>
  - Work: <Files or behavior expected to change>
  - Verify: <Concrete command or manual check>
  - Depends on: <None or SG id>

## Final Verification

- <Command or manual check that validates the whole goal>

## Documentation Impact

| Lane | Required | Owned paths | Reason | Expected update |
| --- | --- | --- | --- | --- |
| ADR | Yes or No | `<exact path>` or None | <Evidence-based reason> | <Expected update or None> |
| Architecture | Yes or No | `<exact path>` or None | <Evidence-based reason> | <Expected update or None> |
| README | Yes or No | `<exact path>` or None | <Evidence-based reason> | <Expected update or None> |
| Changelog | Yes or No | `<exact path>` or None | <Evidence-based reason> | <Expected update or None> |

## Progress

Not started.

## Risks

- <Risk and mitigation>

## Open Questions

- <Question, or "None">

## Documentation Result

Not run yet.

## Implementation Result

Not implemented yet.
```

## Quality Bar

- Keep the plan specific to the requested feature. Avoid generic checklists.
- Ask the user for implementation-affecting decisions instead of choosing silently.
- Make each subgoal independently implementable and independently verifiable.
- Do not let a subgoal depend on hidden context; include the file paths, commands, or decisions Ralph needs.
- Tie every subgoal to a verification signal. If verification is manual, describe exactly what must be observed.
- Include all four evidence-backed Documentation Impact rows and disjoint exact ownership before review.
- Include file paths when known, but do not invent paths before inspecting the repository.
- Preserve user changes and local dirty work; mention any relevant existing changes in the plan.
- Do not let the architect or reviewer edit repository files; the parent planner owns the active plan.
- Do not treat an architect recommendation as a confirmed user decision.
- Use `status: draft` while the new active plan is being reviewed and `status: planned` only after reviewer approval. `$woohyuk-ralph` owns later status changes, archival, and active-file cleanup.
