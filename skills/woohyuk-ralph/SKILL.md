---
name: woohyuk-ralph
description: "Implement the active .woohyuk/plan.md until all scoped subgoals are complete. Use when the user invokes Ralph, asks to execute the active plan, or wants a planned feature implemented. Delegates each subgoal to woohyuk-implementer, requires woohyuk-tester verification before advancing, updates progress, archives the completed plan and result to docs/YYYY-MM-DD-feature-slug/plan.md, then removes the active plan."
---

# Ralph

## Overview

Implement the single active plan at `.woohyuk/plan.md`. Delegate each bounded subgoal to a code implementer, then require an independent tester to verify it before advancing. Keep the active file current throughout the work. After every subgoal and final verification succeed, preserve the finalized plan and implementation result under `docs/`, verify the archive, and remove the active file.

## Active Plan Discovery

1. Use `.woohyuk/plan.md` at the target repository root as the only executable plan.
2. If it does not exist, do not execute a historical `docs/*/plan.md` file. Tell the user to create an active plan with `$woohyuk-plan` first.
3. Treat `docs/YYYY-MM-DD-feature-slug/plan.md` files as completed historical records, not pending execution queues.

## Subagent Orchestration

Use these roles when multi-agent tools are available:

- `woohyuk-implementer`: the only agent allowed to edit product code for the current subgoal.
- `woohyuk-tester`: independently checks the implementation against the active plan and must not edit source code, tests, or the plan.

For each subgoal:

1. Spawn one implementer with a self-contained task containing the target repository, plan path, exact subgoal, owned files or behavior, repository instructions, relevant constraints, and planned verification. Wait for it to finish.
2. Inspect the returned scope and working-tree changes. If the implementer changed unrelated files, stop and resolve ownership before testing.
3. Spawn the tester with the target repository, active plan path, full relevant requirements, repository instructions and constraints, current subgoal, changed files, and exact verification criteria. Require `PASS`, `FAIL`, or `BLOCKED` plus reproducible evidence.
4. On `FAIL`, send the tester's evidence back to the same implementer when possible. Have it fix only the current subgoal, then run the tester again.
5. Allow at most three implementation-and-test attempts for a subgoal, counting the initial attempt. If the third tester verdict is still `FAIL`, set the active plan to `blocked`, preserve the failed evidence and incomplete subgoal, and ask the user for direction. Never accept the implementer's self-verification in place of tester evidence.
6. Keep only one code-writing agent active at a time. Testing may start only after that writer has finished, preventing shared-worktree conflicts.

After every subgoal passes, run the tester once more with the target repository, repository instructions, entire active plan, cumulative changed files, and `## Final Verification`. On `FAIL`, return the evidence to an implementer responsible for the affected scope, then rerun the tester. Allow at most three final implementation-and-test attempts, counting the initial final verification; if the third verdict is still `FAIL`, set the plan to `blocked` and preserve the evidence. Archive only after the final verdict is `PASS`.

When spawning a named specialist, set `fork_turns: "none"` and provide a self-contained prompt instead of relying on inherited conversation context. If a named role is unavailable, use a generic subagent with the same role contract and explicitly select these settings:

- Implementer fallback: `gpt-5.6-sol`, `xhigh`, workspace write.
- Tester fallback: `gpt-5.6-terra`, `high`; allow test artifacts but prohibit source edits.

Mention the fallback and recommend `$woohyuk-install-subagents`; do not abandon an active plan solely because named roles have not been installed.

## Workflow

1. Read `.woohyuk/plan.md` completely.
2. Read repository instructions and relevant files before editing, including `AGENTS.md`, README files, package scripts, and files named in the plan.
3. Check the working tree status. Do not revert unrelated user changes.
4. If the plan is stale, technically wrong, or lacks verifiable subgoals, update the active plan first or explain the mismatch before implementing.
5. Set frontmatter `status: in-progress` and update `updated` before substantial edits.
6. Build the execution queue from `## Subgoals`. If the plan only has `## Implementation Steps`, treat each unchecked item as a subgoal and normalize the plan when useful.
7. Execute exactly one open subgoal at a time through Subagent Orchestration. Do not start the next subgoal while the current subgoal is unverified.
8. For the current subgoal:
   - Have the implementer change only the work needed for that subgoal.
   - Have the tester run its `Verify` check and any focused regression scenarios warranted by the change.
   - If verification fails, return the evidence to the implementer, fix within the same subgoal scope, and have the tester rerun verification.
   - Repeat for at most three attempts until the subgoal passes, is proven obsolete by repository evidence, or is blocked. Treat a third `FAIL` as blocked and record all failure evidence.
9. Mark a subgoal complete only after the tester returns `PASS`. The tester must perform any required manual check with the available interaction tools; if it cannot perform the check, return `BLOCKED` rather than treating it as complete.
10. After each completed or blocked subgoal, update the active plan checklist and `updated`, then append a dated short note under `## Progress`.
11. Continue the loop until every required subgoal is complete.
12. Have the tester run `## Final Verification` against the whole plan after all subgoals are complete. If it fails, return to the relevant implementer scope, fix it, and have the tester rerun final verification, for at most three total final verification attempts. Treat a third `FAIL` as blocked and preserve the evidence.
13. When all subgoals and final verification are complete, update the active plan frontmatter:
    - `status: implemented`
    - `updated: YYYY-MM-DD`
    - `implemented_at: YYYY-MM-DD`
14. Replace or append `## Implementation Result` with the actual outcome.
15. Archive and clean up the active plan by following Completed Plan Archival. Do not report Ralph complete before archival succeeds.

## Loop Rule

Ralph's core loop is:

```text
pick next open subgoal
implementer changes only that subgoal
tester independently verifies that subgoal
if verification fails and fewer than three attempts ran: implementer fixes, tester verifies again
if the third verification fails: preserve evidence, mark the plan blocked, ask the user
if verification passes: mark subgoal complete and update .woohyuk/plan.md
move to the next subgoal
after all subgoals pass: tester runs final verification
archive the finalized plan, then remove the active plan
```

Never skip to a later subgoal because the earlier one is difficult. Never run multiple implementers against the shared worktree. Stop as blocked only when progress requires user input, missing credentials, unavailable external systems, a plan decision that cannot be safely made from repository evidence, or three evidence-backed implementation-and-test attempts fail for the same subgoal or final verification.

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
- `<manual scenario>`: passed

### Follow-ups

- <Remaining item, or "None">
```

## Completed Plan Archival

Archive only after all required subgoals and final verification pass.

1. Use the local completion date and the active plan's `feature_slug` to build `docs/YYYY-MM-DD-feature-slug/plan.md`.
2. If `feature_slug` is missing in an older active plan, derive it from the title and add it to the frontmatter before archiving.
3. If the target archive file already exists, do not overwrite it silently. Ask the user whether to update that record or use a distinct feature slug.
4. Create the dated directory and write the entire finalized active plan to its `plan.md`, including decisions, checked subgoals, progress, and `## Implementation Result`.
5. Verify that the archive exists and contains `status: implemented`, all required completed subgoals, and the final verification result.
6. Delete `.woohyuk/plan.md` only after the archive passes verification.
7. Remove `.woohyuk/` if it is empty. Preserve any other user files in that directory.

The archive is the durable implementation record. Never delete the active plan first, and never leave completion recorded only in `.woohyuk/plan.md`.

## Incomplete Or Blocked Work

Do not archive or delete the active plan when required work or verification is incomplete.

If blocked:

- Set `status: blocked` or leave the prior status if the plan convention requires it.
- Leave incomplete subgoals unchecked.
- Add the blocker under `## Implementation Result`.
- State the exact user input, dependency, or external condition needed to proceed.
- Keep `.woohyuk/plan.md` so Ralph can resume later.

## Final Response

Summarize the implemented behavior, completed subgoals, changed files, verification result, and archive path. Confirm that `.woohyuk/plan.md` was removed. Mention any checks that could not run.
