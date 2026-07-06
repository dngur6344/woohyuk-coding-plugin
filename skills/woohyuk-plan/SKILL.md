---
name: woohyuk-plan
description: "Create implementation plan documents before code changes. Use when the user asks for a plan, implementation plan, task breakdown, roadmap, or wants planning saved under docs/ before coding. Creates docs/YYYY-MM-DD-feature-slug/plan.md with goal sizing, user-confirmed decisions, subgoals, per-subgoal verification, risks, assumptions, and implementation result placeholders for Ralph to execute."
---

# Write Implementation Plan

## Overview

Create a saved implementation plan in the target repository before coding. The plan must break work into small, verifiable subgoals so `$woohyuk-ralph` can execute one subgoal at a time until the full goal is complete.

## Workflow

1. Identify the target repository and read its local instructions first, including `AGENTS.md`, README files, package scripts, and nearby documentation relevant to the requested feature.
2. Classify the goal size as `small`, `medium`, or `large` based on scope, uncertainty, touched areas, and verification cost.
3. Break the goal into subgoals sized so each can be implemented and verified independently. For trivial work, use one subgoal.
4. Identify decision points that affect implementation direction, scope, architecture, UX, data shape, dependencies, compatibility, migration strategy, or verification.
5. Ask the user to decide required decision points before finalizing the plan. Do not silently choose between meaningful alternatives.
6. State low-risk assumptions in the plan only when they do not materially change implementation.
7. Create a directory under `docs/` named `YYYY-MM-DD-feature-slug`.
8. Create the plan document as `docs/YYYY-MM-DD-feature-slug/plan.md`.
9. Do not implement code while using this skill unless the user explicitly asks for both planning and implementation.
10. In the final response, provide the plan path, goal size, subgoal count, confirmed decisions, and main assumptions or open questions.

## Goal Sizing

Use these defaults:

- `small`: one focused code path or documentation change; usually 1 subgoal.
- `medium`: several files or one workflow with meaningful risk; usually 2-4 subgoals.
- `large`: cross-cutting behavior, migration, new architecture, or unclear dependencies; usually 4+ subgoals and more explicit risks.

Do not inflate plans with generic process steps. A subgoal must produce a concrete repository change or a concrete decision that unblocks implementation.

## Decision Handling

Ask the user when a decision would change what gets built or how it is built.

- Ask concise, numbered questions.
- Provide 2-3 concrete options when useful, including the tradeoff for each option.
- You may recommend an option, but the user makes the decision.
- Wait for the user's answer before writing a final plan when the decision affects implementation scope or direction.
- Record answered decisions in `## Decisions`.
- Use `## Open Questions` only for non-blocking questions or questions the user explicitly leaves unresolved.

## Directory Naming

- Use the local date in `YYYY-MM-DD` format. Run `date +%F` if the date is not already reliable.
- Derive `feature-slug` from the requested feature in short kebab-case.
- Korean slugs are acceptable when they are clearer for the project; replace whitespace with `-`.
- Prefer a stable, human-readable directory name over over-normalized wording.

Examples:

- `docs/2026-07-01-add-login-rate-limit/plan.md`
- `docs/2026-07-01-학생부-회의록-ingest/plan.md`

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
- Include file paths when known, but do not invent paths before inspecting the repo.
- Preserve user changes and local dirty work; mention any relevant existing changes in the plan.
- Use `status: planned` for new plans. `$woohyuk-ralph` is responsible for changing the status after implementation.
