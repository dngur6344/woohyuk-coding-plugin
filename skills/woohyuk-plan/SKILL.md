---
name: woohyuk-plan
description: "Create the single active implementation plan at .woohyuk/plan.md before code changes. Use when the user asks for a plan, implementation plan, task breakdown, roadmap, or wants planning saved before coding. Uses the woohyuk-architect subagent for design and woohyuk-reviewer for plan validation, detects an existing active plan, and structures confirmed decisions, subgoals, verification, risks, assumptions, and result placeholders for Ralph."
---

# Write Active Implementation Plan

## Overview

Create one active implementation plan at `.woohyuk/plan.md` in the target repository. Use a read-only architect to shape the design and a separate read-only reviewer to validate the draft. Break work into small, verifiable subgoals so `$woohyuk-ralph` can execute one subgoal at a time. Do not create the dated `docs/` record during planning; Ralph creates it only after implementation and final verification succeed.

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

1. Spawn `woohyuk-architect` after implementation-affecting user decisions are confirmed. Give it a self-contained task containing the requirements, target repository, constraints, relevant evidence, and decisions. Ask for design boundaries, flow, risks, and suggested subgoals. Keep it read-only.
2. Synthesize the architect's evidence into the draft plan. The parent planner alone writes `.woohyuk/plan.md` with `status: draft` while review is pending.
3. Spawn `woohyuk-reviewer` in `PLAN_REVIEW` mode with the requirements and draft path. Require it to verify references, requirement coverage, subgoal independence, dependencies, and executable verification.
4. On `REVISE`, update the draft and resubmit it to the reviewer. Allow at most two revision rounds. If the second revision is not approved, set `status: blocked`, record the remaining review issues, and ask the user how to resolve them. On `BLOCKED`, do the same for the missing decision. Set `status: planned` only after `APPROVE`.
5. Wait for each specialist's result and incorporate evidence rather than copying its output blindly.

When spawning a named specialist, set `fork_turns: "none"` and provide a self-contained prompt instead of relying on inherited conversation context. If a named role is unavailable, use a generic read-only subagent with the same role contract and explicitly select these settings:

- Architect fallback: `gpt-5.6-sol`, `xhigh`.
- Reviewer fallback: `gpt-5.6-sol`, `xhigh`.

Mention the fallback and recommend `$woohyuk-install-subagents`; do not block planning solely because named roles have not been installed. If no subagent can run, the parent must execute the same architect and reviewer contracts, disclose that fallback, and must not mark the plan `planned` without completing the review contract.

## Workflow

1. Identify the target repository and read its local instructions first, including `AGENTS.md`, README files, package scripts, and nearby documentation relevant to the requested feature.
2. Apply the Active Plan Guard before drafting or writing a new plan.
3. Classify the goal size as `small`, `medium`, or `large` based on scope, uncertainty, touched areas, and verification cost.
4. Identify decision points that affect implementation direction, scope, architecture, UX, data shape, dependencies, compatibility, migration strategy, or verification.
5. Ask the user to decide required decision points before drafting the plan. Do not silently choose between meaningful alternatives.
6. Run the architect stage from Subagent Orchestration.
7. Break the goal into independently implementable and verifiable subgoals using repository evidence, confirmed decisions, and the architect's result. For trivial work, use one subgoal.
8. State low-risk assumptions in the plan only when they do not materially change implementation.
9. Derive a stable `feature_slug` in short kebab-case for Ralph's completed-plan archive.
10. Create `.woohyuk/` at the target repository root if needed.
11. Write the draft active plan to `.woohyuk/plan.md` with `status: draft`, then run the reviewer stage and revise as required. Change it to `planned` only after approval.
12. Do not implement code while using this skill unless the user explicitly asks for both planning and implementation.
13. In the final response, provide the active plan path, goal size, subgoal count, confirmed decisions, reviewer verdict, and main assumptions or open questions.

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

## Progress

Not started.

## Risks

- <Risk and mitigation>

## Open Questions

- <Question, or "None">

## Implementation Result

Not implemented yet.
```

## Quality Bar

- Keep the plan specific to the requested feature. Avoid generic checklists.
- Ask the user for implementation-affecting decisions instead of choosing silently.
- Make each subgoal independently implementable and independently verifiable.
- Do not let a subgoal depend on hidden context; include the file paths, commands, or decisions Ralph needs.
- Tie every subgoal to a verification signal. If verification is manual, describe exactly what must be observed.
- Include file paths when known, but do not invent paths before inspecting the repository.
- Preserve user changes and local dirty work; mention any relevant existing changes in the plan.
- Do not let the architect or reviewer edit repository files; the parent planner owns the active plan.
- Do not treat an architect recommendation as a confirmed user decision.
- Use `status: draft` while the new active plan is being reviewed and `status: planned` only after reviewer approval. `$woohyuk-ralph` owns later status changes, archival, and active-file cleanup.
