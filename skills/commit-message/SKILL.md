---
name: commit-message
description: "Draft commit messages from staged changes, unstaged diffs, or a described change. Use when the user asks for a commit message, conventional commit, terse git commit title, commit body, or help splitting and naming commits."
---

# Commit Message

## Overview

Write commit messages that describe the actual change and why it matters. Prefer precise, reviewable messages over broad summaries.

## Workflow

1. Inspect staged changes with `git diff --cached`. If nothing is staged, inspect `git diff` and say the message is based on unstaged changes.
2. Identify the primary intent, user-visible effect, and any tests or docs changed.
3. If changes are unrelated, recommend splitting commits before drafting one combined message.
4. Use the repository's existing commit style when visible from recent history.
5. If the user asks for Conventional Commits, use an appropriate type such as `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, or `build`.

## Output

For a simple change, return one commit subject. For broader changes, return:

- Subject
- Body bullets explaining why and what changed
- Optional test note

Keep the subject under 72 characters when practical. Use imperative mood and avoid vague subjects like `update files`.

## Verification

Do not run `git commit` unless the user explicitly asks to commit. If committing is requested, show or use the final message exactly and confirm the staged scope first.
