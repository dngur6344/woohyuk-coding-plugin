---
name: commit-message
description: "Draft structured commit messages from staged changes, unstaged diffs, or a described change. Use when the user asks for a commit message, conventional commit, git commit title and body, Korean commit message, or help splitting and naming commits."
---

# Commit Message

## Overview

Write commit messages that describe the actual change and why it matters. Default to a summary line followed by detailed bullet points.

## Workflow

1. Inspect staged changes with `git diff --cached`. If nothing is staged, inspect `git diff` and say the message is based on unstaged changes.
2. Identify the primary intent, user-visible effect, implementation details, and any tests or docs changed.
3. If changes are unrelated, recommend splitting commits before drafting one combined message.
4. Use the repository's existing commit style when visible from recent history.
5. Match the user's language. If the request or repository convention is Korean, write the commit message in Korean.
6. If the user asks for Conventional Commits, use an appropriate type such as `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, or `build`, and still include a body unless the user asks for a title only.

## Output

Return a complete commit message by default:

```text
Summary line

- Detail explaining what changed and why
- Detail explaining important implementation or behavior impact
- Optional test, docs, migration, or follow-up note when relevant
```

Keep the summary line concise, but do not over-compress it into a vague title. Use 2-5 body bullets for meaningful changes. Omit body bullets only when the user explicitly asks for a short title or the change is truly trivial.

Prefer concrete phrases over generic ones:

```text
통합 어드민과 A 서비스 연동

- CORS 문제 해결을 통해 A 서비스가 안정적으로 통합 어드민을 호출할 수 있도록 구성
- SDK Import를 통해 일관된 기능을 할 수 있도록 구성
```

Avoid vague summaries like `update files`, `fix bug`, or `change logic`.

## Verification

Do not run `git commit` unless the user explicitly asks to commit. If committing is requested, use the final multi-line message exactly and confirm the staged scope first.
