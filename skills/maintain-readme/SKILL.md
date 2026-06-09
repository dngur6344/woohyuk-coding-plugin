---
name: maintain-readme
description: "Create or update a repository README from project evidence. Use when the user asks to generate, refresh, rewrite, or repair README.md content, installation instructions, usage commands, environment setup, or project overview documentation."
---

# Maintain README

## Overview

Maintain README content from the repository as it exists, not from guesses. Prefer accurate, compact documentation over broad marketing copy.

## Workflow

1. Inspect existing README files, package manifests, lockfiles, build config, entrypoints, scripts, environment examples, tests, and docs.
2. Identify the intended audience from the repository shape: library, app, CLI, service, package, or monorepo.
3. Preserve accurate existing content unless it is stale or contradicted by code.
4. Add only sections supported by evidence. Do not invent badges, roadmap items, deployment targets, or credentials.
5. If setup or command behavior is unclear, state the assumption in the README or ask the user before encoding a risky claim.

## Recommended Sections

Use only sections that fit the project:

- Project purpose
- Features or scope
- Prerequisites
- Installation
- Configuration and environment variables
- Development commands
- Testing and quality checks
- Package or directory structure
- Deployment or release notes
- Troubleshooting

## Verification

Verify commands against actual manifest scripts before documenting them. When practical, run lightweight checks such as help commands, test discovery, or package manager script listing.

End by summarizing changed sections and any assumptions that remain.
