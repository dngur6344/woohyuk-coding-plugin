---
name: ralph
description: "Implement saved implementation plan documents until all scoped subgoals are complete. Use when the user invokes Ralph, asks to execute a plan, points to docs/YYYY-MM-DD-*/plan.md, or wants a planned feature implemented. Reads the plan, executes one subgoal at a time, verifies it, retries failed subgoals, then proceeds only after the current subgoal is complete."
---

# Ralph

## Overview

Implement a saved plan document and update that document with the implementation result. Ralph is execution-focused: read the plan, execute each scoped subgoal, verify it, retry if verification fails, and mark the plan complete only when every required subgoal and final verification are done.

## Plan Discovery

1. If the user provides a plan path, use that exact file.
2. Otherwise, look for `docs/*/plan.md` files and prefer the newest dated directory whose frontmatter `status` is not `implemented`.
3. If multiple plausible plans remain, ask the user which plan to execute.
4. If no plan exists, tell the user to create one with `$write-implementation-plan` or ask whether to create a plan first.

## Workflow

1. Read the plan document completely.
2. Read repository instructions and relevant files before editing, including `AGENTS.md`, README files, package scripts, and files named in the plan.
3. Check the working tree status. Do not revert unrelated user changes.
4. If the plan is stale, technically wrong, or lacks verifiable subgoals, update the plan first or explain the mismatch before implementing.
5. Set frontmatter `status: in-progress` before substantial edits.
6. Build the execution queue from `## Subgoals`. If the plan only has `## Implementation Steps`, treat each checked item as a subgoal and normalize the plan when useful.
7. Execute exactly one open subgoal at a time. Do not start the next subgoal while the current subgoal is unverified.
8. For the current subgoal:
   - Implement only the work needed for that subgoal.
   - Run its `Verify` check or the matching planned verification.
   - If verification fails, diagnose, fix within the same subgoal scope, and rerun verification.
   - Repeat until the subgoal passes, is proven obsolete by repository evidence, or is blocked.
9. Mark a subgoal complete only after its verification passes or the plan explicitly allows a documented non-run/manual result.
10. After each completed or blocked subgoal, update the plan checklist and add a short progress note.
11. Continue the loop until every required subgoal is complete.
12. Run `## Final Verification` after all subgoals are complete. If final verification fails, return to the relevant subgoal, fix it, and rerun final verification.
13. When all subgoals and final verification are complete, update the plan frontmatter:
    - `status: implemented`
    - `updated: YYYY-MM-DD`
    - `implemented_at: YYYY-MM-DD`
14. Replace or append `## Implementation Result` with the actual outcome.

## Loop Rule

Ralph's core loop is:

```text
pick next open subgoal
implement only that subgoal
verify that subgoal
if verification fails: fix and verify again
if verification passes: mark subgoal complete and update the plan
move to the next subgoal
after all subgoals pass: run final verification
```

Never skip to a later subgoal because the earlier one is difficult. Stop as blocked only when progress requires user input, missing credentials, unavailable external systems, or a plan decision that cannot be safely made from repository evidence.

## Implementation Result Format

Use this shape:

```markdown
## Implementation Result

Implemented on YYYY-MM-DD.

### Summary

- <What changed.>

### Completed Subgoals

- [x] SG1: <Verified result>

### Changed Files

- `<path>`: <Reason>

### Verification

- `<command or check>`: passed
- `<command or check>`: not run, <reason>

### Follow-ups

- <Remaining item, or "None">
```

## Incomplete Or Blocked Work

Do not mark a plan as implemented when required work or verification is incomplete.

If blocked:

- Set `status: blocked` or leave the prior status if the plan convention requires it.
- Leave incomplete subgoals unchecked.
- Add the blocker under `## Implementation Result`.
- State the exact user input, dependency, or external condition needed to proceed.

## Final Response

Summarize the implemented behavior, completed subgoals, changed files, verification result, and plan path. Mention any checks that could not run.
