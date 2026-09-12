---
name: woohyuk-install-subagents
description: "Install or update Woohyuk's ten custom Codex roles, including conditional GPT-6 Astra planning and implementation roles. Use when configuring the plugin's specialists, resolving a missing woohyuk-plan or woohyuk-ralph role, or choosing personal versus project installation."
---

# Install Woohyuk Subagents

## Overview

Install the ten bundled custom-agent TOML files into a Codex-supported agent directory. Default to personal installation so the roles work across projects. Never overwrite a customized role silently.

## Roles

- `woohyuk-architect`: read-only system and implementation design with `gpt-5.6-sol` at `xhigh`.
- `woohyuk-implementer`: scoped code implementation with `gpt-5.6-sol` at `xhigh`.
- `woohyuk-astra-architect`: read-only system and implementation design with `gpt-6-astra` at `medium`, selected only when the root session uses Astra.
- `woohyuk-astra-implementer`: scoped code implementation with `gpt-6-astra` at `medium`, selected only when the root session uses Astra.
- `woohyuk-reviewer`: read-only plan, code, and documentation review with `gpt-5.6-sol` at `xhigh`.
- `woohyuk-tester`: requirement-driven verification with `gpt-5.6-terra` at `high`.
- `woohyuk-adr-documenter`: scoped ADR updates with `gpt-5.6-sol` at `xhigh`.
- `woohyuk-architecture-documenter`: scoped architecture docs with `gpt-5.6-sol` at `xhigh`.
- `woohyuk-readme-documenter`: scoped README updates with `gpt-5.6-terra` at `high`.
- `woohyuk-changelog-documenter`: scoped changelog updates with `gpt-5.6-terra` at `medium`.

## Installation

Run from this skill directory.

Personal installation:

```bash
python3 scripts/install_agents.py --scope user
```

Project installation:

```bash
python3 scripts/install_agents.py --scope project --project-root <repo-root>
```

The glob-based installer validates every bundled TOML before writing. Identical installed files are left unchanged. Without `--force`, it reports every differing installed role and writes nothing. Use `--force` only after the user explicitly approves replacing all reported customizations.

## Verification

1. Confirm the installer reports all ten roles as installed or unchanged.
2. Parse the installed files as TOML.
3. Start a new Codex session so the custom roles are discovered.
4. Confirm the agent list includes all ten `woohyuk-*` roles before relying on named-role orchestration.

Do not edit `~/.codex/config.toml`; standalone files in the supported agent directories are sufficient.
