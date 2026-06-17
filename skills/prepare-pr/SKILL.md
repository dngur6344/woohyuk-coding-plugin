---
name: prepare-pr
description: "Prepare GitHub pull request content from repository changes. Use when the user asks for a PR title, PR body, pull request summary, review checklist, change explanation, risk section, testing notes, or wants Codex to prepare a branch for review."
---

# Prepare PR

## Overview

Draft PR content from the actual diff and repository context. Prefer precise reviewer-facing context over broad release-note prose.

## Workflow

1. Identify the PR scope from the current branch, staged changes, working tree diff, commit range, or user-provided files.
2. Inspect `git status`, `git diff`, recent commits, relevant tests, and docs touched by the change.
3. Separate what changed from why it changed. Include user-facing impact only when there is one.
4. Call out review risk, migration notes, compatibility concerns, and follow-up work when they are supported by the diff.
5. Include validation commands that were actually run. If none were run, write `Not run` with the reason.
6. Do not open or push a PR unless the user explicitly asks for that action.

## PR Body Shape

Use this structure unless the repository has a PR template:

- Summary
- Changes
- Testing
- Risk and rollout
- Review notes

If a PR template exists, preserve its headings and fill it with concise evidence from the diff.

## Output

Return a ready-to-paste title and body. Keep the title specific and under 80 characters when practical.

## Verification

If the user asks to create the PR, confirm branch, base, remote, staged scope, and authentication before pushing or opening anything.
