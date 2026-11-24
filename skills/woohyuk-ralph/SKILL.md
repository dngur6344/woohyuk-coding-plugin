---
name: woohyuk-ralph
description: "Execute the active .woohyuk/plan.md through scoped implementation, independent testing, evidence-backed parallel documentation, documentation review, and archival. Use when the user invokes Ralph or asks to implement the active plan."
---

# Ralph

## Overview

Execute the single active plan at `.woohyuk/plan.md`. Each code subgoal has one implementer and an independent tester. After whole-plan code verification, run the required ADR, architecture, README, and changelog lanes with exact ownership, then require read-only documentation approval before marking or archiving the plan as implemented.

The normal state machine is:

```text
planned -> in-progress -> code-verified -> documenting -> docs-review -> implemented
```

Any blocked condition retains the active plan. Only the parent running Ralph may edit `.woohyuk/plan.md` or its dated archive.

## Active Plan

1. Execute only `.woohyuk/plan.md` at the target repository root. Archived `docs/*/worklog.md` and legacy `docs/*/plan.md` files are not queues.
2. Read the complete plan, repository instructions, named files, package scripts, and relevant docs before changing status.
3. Check the working tree and preserve unrelated user changes.
4. Require verifiable subgoals plus all four Documentation Impact lanes. Normalize a legacy plan from repository evidence before implementation; stop for any unresolved implementation or documentation decision.
5. Set `status: in-progress` and update `updated` before code changes.

## Roles

- `woohyuk-implementer`: the only product-code writer for one current subgoal.
- `woohyuk-tester`: independent subgoal, affected-scope, and whole-plan verification.
- `woohyuk-adr-documenter`: uses `$woohyuk-write-adr`.
- `woohyuk-architecture-documenter`: uses `$woohyuk-document-project-architecture`.
- `woohyuk-readme-documenter`: uses `$woohyuk-maintain-readme`.
- `woohyuk-changelog-documenter`: uses `$woohyuk-update-changelog`.
- `woohyuk-reviewer`: read-only `DOC_REVIEW`.

Spawn every named role with `fork_turns: "none"` and a self-contained prompt containing the repository, active plan, confirmed requirements, repository instructions, exact task and owned paths, relevant diff, and verification evidence. Omit the model override so Codex can inherit the parent session's model. Wait for every result used by the state machine.

If a named role is unavailable, use a generic agent with the same contract and the settings below. Leave the model unspecified.

| Role | Effort | Access |
| --- | --- | --- |
| Implementer | `high` | workspace write |
| Tester | `high` | test artifacts only; no source, tests, or plan edits |
| ADR documenter | `high` | exact documentation paths only |
| Architecture documenter | `high` | exact documentation paths only |
| README documenter | `high` | exact documentation paths only |
| Changelog documenter | `medium` | exact documentation paths only |
| Reviewer | `xhigh` | read-only |

Disclose a fallback and recommend `$woohyuk-install-subagents`, but do not abandon an active plan only because a named role is unavailable.

## Verification Scope And Evidence

Before each handoff, assign checks by purpose:

- Implementer: quick changed-path tests, compilation, or smoke checks needed to catch implementation mistakes.
- Subgoal tester: independently validate the assigned acceptance criteria and directly affected regressions. Add negative, integration, or manual checks only for a concrete risk or coverage gap.
- Whole-plan tester: check cross-subgoal integration and final requirement coverage. Reserve broad builds and full suites for this stage unless earlier execution is required by repository instructions, the plan, or a specific risk.

User, repository, and plan-required checks remain mandatory. Do not silently defer a check past the stage where it is required or weaken an acceptance criterion to save time. Do not run the same command again solely because another stage has started.

The parent keeps compact evidence under `## Progress`: command or scenario, requirements covered, relevant working-tree inputs and environment, result, and accessible execution logs or artifacts. Include elapsed time when available. A commit ID alone does not identify uncommitted or untracked inputs.

Reuse a `PASS` only when an independent tester has validated the execution evidence and its relevant inputs and environment are unchanged. Inputs include covered source, tests, shared or transitive dependencies, and configuration or tooling. A summary saying "tests passed" is not reusable evidence. If relevance or freshness is uncertain, rerun the affected check.

Rerun for changed inputs or environment, a failure, stale or missing evidence, or a new requirement or uncovered risk. State the reason and use the smallest sufficient scope. Reusing evidence never replaces independent acceptance judgment.

## Code Loop

Execute one open subgoal at a time:

1. Give `woohyuk-implementer` the exact subgoal, scope, ownership, and quick checks from Verification Scope And Evidence.
2. Inspect its result and working-tree changes. Stop and resolve any out-of-scope change without reverting unrelated work.
3. Give a tester the subgoal requirements, changed files, reproducible acceptance criteria, and existing execution evidence. It must independently inspect the change and run acceptance checks not covered by current independently validated evidence; do not repeat implementer smoke checks solely to duplicate coverage.
4. On `FAIL`, return the evidence to the same implementer when possible, then retest. Allow at most three implementation-and-test attempts per subgoal, including the initial attempt.
5. Mark the subgoal complete only on tester `PASS`; update its checklist and evidence under `## Progress`, distinguishing executed and reused checks. A third `FAIL` or a tester `BLOCKED` blocks the plan.

Keep only one code writer active. A tester starts after that writer finishes and must perform required available manual checks rather than assuming success.

## Whole-Code Verification

After all subgoals pass, have the tester verify the entire plan and `## Final Verification`. This is whole-code-verification cycle 1. A cycle is one whole-plan tester run after the latest code state; allow at most three cycles total, including the initial one and all later runs caused by `DOC_REVIEW CODE_DEFECT`.

Map every requirement and final verification item to current evidence. Reuse valid independently verified subgoal results; run the remaining integration, end-to-end, and required broad checks against the final code state. A full suite need not run again if equivalent current evidence already covers it. Do not expand to unrelated project areas without a concrete risk or missing requirement coverage. The cycle limit is a retry ceiling, not a required number of successful runs.

- On whole-plan `FAIL`, reopen the owning subgoal, have an implementer fix it, test the affected scope, then run the next whole-plan cycle.
- On `BLOCKED`, or if cycle 3 does not pass, block the plan and retain the evidence.
- On `PASS`, set `status: code-verified`, record the cycle evidence, and continue to Documentation Impact Resolution.
- Every code edit invalidates prior documentation output and approval. Set `## Documentation Result` to `Not run yet.` and rerun every required documentation lane after the next whole-plan `PASS`.

## Documentation Impact Resolution

After each whole-plan `PASS`, reconcile the plan's four lanes against the actual final working-tree diff, including staged and untracked content, confirmed requirements, test evidence, and repository conventions. A planned `No` does not override evidence that the implementation made documentation stale.

For each of `ADR`, `Architecture`, `README`, and `Changelog`, retain:

- `Required: Yes|No`
- exact repository-relative `Owned paths`, or `None`
- an evidence-based `Reason`
- the `Expected update`, or `None`

Required paths must name files, not globs or bare directories. Make ownership globally pairwise-disjoint across every lane and batch before spawning writers. A shared README, index, or release file belongs to exactly one lane, whose Expected update must include all cross-lane content for that file. Never transfer or duplicate ownership to let another lane edit the same path.

Even when every lane is `No`, proceed to `DOC_REVIEW` so the reviewer validates the classification against the actual diff.

## Documentation Batch

Set `status: documenting` after impact resolution, including when every lane is `No`. The parent makes this plan edit before any batch baseline and does not edit the plan while writers run.

For required lanes:

1. Capture a pre-batch baseline: `git status --porcelain=v1 -uall`, the current `HEAD`, and content hashes for every already changed or untracked path plus every allocated path that exists. Preserve it with the batch evidence.
2. Spawn the required documenters in parallel as capacity permits. Each prompt must include its exact disjoint paths, the active plan, confirmed requirements, final implementation diff, whole-plan tester evidence, and repository instructions. A documenter may write only its allocation and may never edit code, tests, the active plan, or the dated plan archive.
3. Wait for all writers. A writer `BLOCKED` blocks the plan; do not substitute guessed documentation.
4. Compare post-batch status and hashes with the baseline. Verify that `HEAD` is unchanged, every writer-reported path is allocated, and no path outside the allocated union changed during the batch. If the check fails, block the plan, preserve the evidence, and do not silently revert files.
5. Run focused formatting, link, command, or document checks warranted by the changed docs.

Capacity limits may split globally disjoint lanes into multiple parallel batches; take a fresh baseline for each batch. Overlapping ownership is invalid and must be reassigned before spawning. When no lane is required, record the no-op documenting stage and continue directly to review.

## Documentation Review Loop

Set `status: docs-review`, then spawn `woohyuk-reviewer` in `DOC_REVIEW` mode with the complete plan, four lane decisions, confirmed requirements, final diff, whole-plan test evidence, writer results, changed docs, and ownership map.

Limit this review to documentation accuracy, ownership, and consistency with relevant implementation and current test evidence. When every lane is `No`, validate that classification without a broad product re-review. Do not rerun product builds or suites during documentation review; send any specific missing or stale evidence back to the parent for a scoped tester check. Documentation-only revisions require affected document checks, not another product-test cycle, unless product-test inputs change or a new implementation risk is found.

- `APPROVE`: replace `## Documentation Result` with an `APPROVE` result containing reviewed lanes, changed documentation paths, and verification evidence. Only now may Ralph mark the plan implemented.
- `REVISE`: rerun only the implicated documentation lanes. Run them concurrently when paths are disjoint, using a fresh baseline and the same containment checks, then resubmit all docs for review. Allow at most two revision rounds; if the third review still returns `REVISE`, block the plan.
- `CODE_DEFECT`: accept this only for implementation that conflicts with a confirmed requirement and requires an owning code subgoal, code path, requirement, and evidence. If three whole-code-verification cycles have already run, block before another code edit. Otherwise reopen that subgoal, set `status: in-progress`, use the implementer, test the affected scope, and run the next whole-code-verification cycle. Any code edit invalidates all documentation and approval; after `PASS`, recompute the lanes and rerun every required lane before a fresh review.
- `BLOCKED`: record the missing decision or external evidence, set `status: blocked`, and retain the active plan.

The reviewer must identify the owning lane, exact path, and evidence for every documentation finding. A stale, missing, or incorrect document is `REVISE`, never `CODE_DEFECT`. Reset the two-round documentation revision allowance after a code edit because all documentation evidence is invalidated.

## Completion And Archival

After and only after `DOC_REVIEW APPROVE`:

1. Set `status: implemented`, `updated: YYYY-MM-DD`, and `implemented_at: YYYY-MM-DD`.
2. Update `## Implementation Result` with the actual summary, completed subgoals, code and documentation files, tester evidence, documentation approval, and follow-ups.
3. Build `docs/YYYY-MM-DD-feature-slug/worklog.md`. If the path exists, ask before overwriting or choose a user-approved distinct slug.
4. Write the entire finalized plan, including the implementation and verification results, to the work log. The parent is the only archive writer.
5. Verify the archive contains `status: implemented`, all required checked subgoals, successful whole-plan verification, and `## Documentation Result` with `APPROVE`.
6. Delete `.woohyuk/plan.md` only after that verification passes; remove `.woohyuk/` only if empty.

Never mark `implemented`, set `implemented_at`, archive, or delete the active plan before documentation approval.

## Blocked Work

On a bounded-attempt exhaustion, ownership violation, unresolved decision, unavailable required evidence, writer `BLOCKED`, tester `BLOCKED`, or reviewer `BLOCKED`:

- set `status: blocked`;
- leave incomplete or reopened subgoals unchecked;
- record the exact evidence and required next action under `## Implementation Result`;
- retain `.woohyuk/plan.md` and do not archive.

## Final Response

Report completed subgoals, code and documentation files, whole-plan test cycles, executed versus reused checks and rerun reasons, documentation review verdict, archive path, and active-plan removal. Mention every check that could not run.
