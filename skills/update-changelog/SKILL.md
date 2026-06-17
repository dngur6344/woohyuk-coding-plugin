---
name: update-changelog
description: "Create or update changelogs and release notes from repository changes. Use when the user asks to update CHANGELOG.md, draft release notes, summarize unreleased changes, prepare version notes, or classify changes as added, changed, fixed, deprecated, removed, security, or breaking."
---

# Update Changelog

## Overview

Maintain changelog entries from concrete repository changes. Keep entries useful to users and maintainers, not a raw commit dump.

## Workflow

1. Inspect existing changelog or release-note conventions before choosing a format.
2. Determine the change range from the user request, git diff, commit range, tag range, or staged changes.
3. Group changes by user-visible impact. Avoid listing internal-only churn unless it matters for upgrades or maintainers.
4. Preserve the repository's existing format. If no format exists, use a compact Keep a Changelog-style `Unreleased` section.
5. Call out breaking changes, migration steps, security fixes, and deprecations explicitly.
6. If asked to edit files, update `CHANGELOG.md` or the repository's existing release-note path. Otherwise return draft notes only.

## Entry Guidance

Prefer categories that fit the project:

- Added
- Changed
- Fixed
- Deprecated
- Removed
- Security
- Breaking Changes

Write entries in plain language. Link issue or PR numbers only when the repository already uses that style or the user provides them.

## Verification

Check date/version headings, duplicate entries, markdown formatting, and whether each changelog claim is supported by the inspected changes.
