---
name: review-code
description: "Review code changes for bugs, regressions, design risks, missing tests, and maintainability issues. Use when the user asks for a code review, PR review, diff review, working-tree review, or asks Codex to inspect changes before merging or committing."
---

# Review Code

## Overview

Review with a bug-finding stance. Prioritize concrete behavioral risks over style opinions, and ground every finding in repository evidence.

## Workflow

1. Identify the review scope from the user request, the active git diff, a PR branch, or specific files.
2. Inspect relevant code paths before judging a change. Use `rg`, `git diff`, tests, and nearby call sites to understand behavior.
3. Look first for correctness bugs, data loss, security regressions, broken public contracts, race conditions, performance cliffs, and missing migration or compatibility work.
4. Check whether tests cover the changed behavior. Treat missing tests as a finding only when the risk is meaningful and testable.
5. Avoid broad refactors or formatting comments unless they hide a real risk.
6. If asked only for review, do not edit files. If asked to fix findings, make surgical changes and verify them.

## Output

Lead with findings ordered by severity. For each finding, include a tight file and line reference, the risk, and the scenario that triggers it.

Use this shape:

- Findings
- Open questions or assumptions
- Brief summary only after findings

If no issues are found, say that clearly and mention any residual test or scope gaps.

## Verification

When fixes are requested, run the narrowest meaningful tests first, then broader tests when shared behavior is touched. Report commands run and any tests that could not be run.
