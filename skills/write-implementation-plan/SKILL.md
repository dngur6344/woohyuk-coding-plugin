---
name: write-implementation-plan
description: "Create implementation plan documents before code changes. Use when the user asks for a plan, implementation plan, task breakdown, roadmap, or wants planning saved under docs/ before coding. Creates docs/YYYY-MM-DD-feature-slug/plan.md with status metadata, scope, assumptions, implementation steps, verification, risks, and out-of-scope notes."
---

# Write Implementation Plan

## Overview

Create a saved implementation plan in the target repository before coding. The plan must be concise enough to execute and structured enough for `$ralph` to implement later.

## Workflow

1. Identify the target repository and read its local instructions first, including `AGENTS.md`, README files, package scripts, and nearby documentation relevant to the requested feature.
2. State important assumptions in the plan. Ask the user only when ambiguity would materially change the implementation.
3. Create a directory under `docs/` named `YYYY-MM-DD-feature-slug`.
4. Create the plan document as `docs/YYYY-MM-DD-feature-slug/plan.md`.
5. Do not implement code while using this skill unless the user explicitly asks for both planning and implementation.
6. In the final response, provide the plan path and the main assumptions or open questions.

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
---

# <feature title>

## Goal

<One or two sentences describing the outcome.>

## Assumptions

- <Assumption that affects implementation.>

## Scope

- <Included behavior or file area.>

## Out Of Scope

- <Explicit non-goal.>

## Current Evidence

- `<file>`: <Relevant observation.>

## Implementation Steps

- [ ] <Step> -> verify: <Concrete check>

## Verification

- <Command or manual check>

## Risks

- <Risk and mitigation>

## Open Questions

- <Question, or "None">

## Implementation Result

Not implemented yet.
```

## Quality Bar

- Keep the plan specific to the requested feature. Avoid generic checklists.
- Tie each implementation step to a verification signal.
- Include file paths when known, but do not invent paths before inspecting the repo.
- Preserve user changes and local dirty work; mention any relevant existing changes in the plan.
- Use `status: planned` for new plans. `$ralph` is responsible for changing the status after implementation.
