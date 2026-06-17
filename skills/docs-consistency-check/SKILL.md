---
name: docs-consistency-check
description: "Check project documentation for stale, contradictory, or unsupported claims. Use when the user asks to review README, docs, ADRs, changelogs, setup instructions, scripts, package descriptions, architecture docs, or release notes for consistency with each other and with repository evidence."
---

# Docs Consistency Check

## Overview

Find documentation drift before it misleads users or maintainers. Compare docs against the repository's actual files, scripts, config, and code paths.

## Workflow

1. Identify the documentation scope: README, `docs/`, ADRs, changelog, package metadata, setup docs, or all public docs.
2. Inspect docs alongside source-of-truth files such as package manifests, build scripts, route definitions, config, CI, tests, and entrypoints.
3. Look for contradictions in install commands, required versions, environment variables, directory names, feature claims, public API names, architecture descriptions, and release status.
4. Distinguish blockers from polish. Report only issues that can confuse usage, maintenance, release, onboarding, or review.
5. If asked to fix issues, edit the smallest affected docs and preserve existing style.
6. If claims cannot be verified from the repository, mark them as assumptions instead of rewriting them as facts.

## Output

Lead with findings ordered by impact. For each issue, include the conflicting files or source evidence, why it matters, and the recommended correction.

Use this shape:

- Findings
- Suggested fixes
- Checks performed
- Residual uncertainty

If no inconsistencies are found, say so and mention the scope checked.

## Verification

After fixes, re-check links, headings, command names, and source references touched by the edit.
