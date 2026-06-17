---
name: public-release-check
description: "Check a repository or plugin before publishing it publicly. Use when the user asks whether a project is safe to open source, publish to GitHub, release publicly, share externally, or inspect for secrets, private files, local paths, generated caches, proprietary assets, and metadata that should not be public."
---

# Public Release Check

## Overview

Inspect a repository before public release with a practical leak-prevention stance. Focus on secrets, private data, local-only files, and misleading public metadata.

## Workflow

1. Confirm the release scope: whole repository, plugin directory, package, or selected files.
2. Inspect tracked and untracked files with `git status`, `git ls-files`, and `find` or `rg --files`.
3. Search for high-risk patterns: API keys, tokens, passwords, private keys, credentials, `.env`, personal paths, local caches, internal hostnames, unpublished assets, and proprietary design files.
4. Inspect config files such as `.mcp.json`, app config, CI config, package manifests, plugin manifests, and docs for accidental private references.
5. Check `.gitignore` coverage for generated output, local state, secrets, and design/source assets that should stay private.
6. Review README and metadata for public-facing accuracy.
7. If asked to fix issues, make surgical changes such as removing files from the index, adding ignore rules, or replacing local metadata.

## Common Denylist

Flag these unless the user explicitly says they are intended for publication:

- `.env`, `.env.*`, credentials, private keys, certificates, provisioning profiles
- `.codex/`, `.agents/`, marketplace files, local MCP overrides
- `.pen` files, client assets, screenshots of private products
- absolute local paths such as `/Users/...`
- access tokens, refresh tokens, API keys, webhooks, service account JSON
- generated caches, build output, logs, coverage, dependency folders

## Output

Lead with whether the repository appears publishable. Then list blockers, recommended cleanups, checks run, and residual risks.

## Verification

Run repository-specific validation after cleanup when available. Re-run the sensitive pattern search after any fix.
