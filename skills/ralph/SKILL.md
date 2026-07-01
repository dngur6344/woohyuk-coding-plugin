---
name: ralph
description: "Implement saved implementation plan documents. Use when the user invokes Ralph, asks to execute a plan, points to docs/YYYY-MM-DD-*/plan.md, or wants a planned feature implemented. Reads the plan, implements only the scoped work, runs the planned verification, and marks the plan as implemented when complete."
---

# Ralph

## Overview

Implement a saved plan document and update that document with the implementation result. Ralph is execution-focused: read the plan, do the scoped work, verify it, then mark the plan complete only when the implementation is genuinely done.

## Plan Discovery

1. If the user provides a plan path, use that exact file.
2. Otherwise, look for `docs/*/plan.md` files and prefer the newest dated directory whose frontmatter `status` is not `implemented`.
3. If multiple plausible plans remain, ask the user which plan to execute.
4. If no plan exists, tell the user to create one with `$write-implementation-plan` or ask whether to create a plan first.

## Workflow

1. Read the plan document completely.
2. Read repository instructions and relevant files before editing, including `AGENTS.md`, README files, package scripts, and files named in the plan.
3. Check the working tree status. Do not revert unrelated user changes.
4. If the plan is stale or technically wrong, update the plan first or explain the mismatch before implementing.
5. Optionally set frontmatter `status: in-progress` before substantial edits.
6. Implement only the plan scope. Avoid adjacent refactors unless the plan or verification requires them.
7. Run the verification commands or checks listed in the plan. If a listed check cannot run, record why.
8. Mark checklist steps complete as they are implemented and verified.
9. When done, update the plan frontmatter:
   - `status: implemented`
   - `updated: YYYY-MM-DD`
   - `implemented_at: YYYY-MM-DD`
10. Replace or append `## Implementation Result` with the actual outcome.

## Implementation Result Format

Use this shape:

```markdown
## Implementation Result

Implemented on YYYY-MM-DD.

### Summary

- <What changed.>

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
- Add the blocker under `## Implementation Result`.
- State the exact user input, dependency, or external condition needed to proceed.

## Final Response

Summarize the implemented behavior, changed files, verification result, and plan path. Mention any checks that could not run.
