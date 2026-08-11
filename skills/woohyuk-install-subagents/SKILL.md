---
name: woohyuk-install-subagents
description: "Install or update Woohyuk's architect, implementer, reviewer, and tester custom Codex subagent roles. Use when the user asks to configure the plugin's specialized agents, when woohyuk-plan or woohyuk-ralph reports that a named role is unavailable, or when choosing between personal ~/.codex/agents and project .codex/agents installation."
---

# Install Woohyuk Subagents

## Overview

Install the four bundled custom-agent TOML files into a Codex-supported agent directory. Default to personal installation so the roles work across projects. Never overwrite a customized role silently.

## Roles

- `woohyuk-architect`: read-only system and implementation design with `gpt-5.6-sol` at `xhigh`.
- `woohyuk-implementer`: scoped code implementation with `gpt-5.6-sol` at `xhigh`.
- `woohyuk-reviewer`: read-only plan and code review with `gpt-5.6-sol` at `xhigh`.
- `woohyuk-tester`: requirement-driven verification with `gpt-5.6-terra` at `high`.

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

The installer validates every bundled TOML before writing. Identical installed files are left unchanged. If an installed role differs, stop and show the conflicting paths; use `--force` only after the user explicitly approves replacing their customization.

## Verification

1. Confirm the installer reports all four roles as installed or unchanged.
2. Parse the installed files as TOML.
3. Start a new Codex session so the custom roles are discovered.
4. Confirm the agent list includes all four `woohyuk-*` roles before relying on named-role orchestration.

Do not edit `~/.codex/config.toml`; standalone files in the supported agent directories are sufficient.
