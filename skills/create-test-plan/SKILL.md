---
name: create-test-plan
description: "Create focused test plans for code changes, features, bug fixes, or releases. Use when the user asks what to test, asks for a QA plan, wants test cases before implementation, or needs unit, integration, regression, manual, or edge-case coverage."
---

# Create Test Plan

## Overview

Design test coverage from the changed behavior and risk surface. Prefer a small, executable plan over exhaustive generic checklists.

## Workflow

1. Identify the change scope from the user request, git diff, issue, PR, or touched files.
2. Inspect the existing test framework, scripts, fixtures, and nearby tests before proposing new coverage.
3. Separate required tests from optional hardening. Tie every required test to a concrete risk.
4. Include manual checks only when automation is impractical or visual/user-flow confidence is needed.
5. If asked to write tests, implement the narrowest meaningful tests and run them.
6. If asked only for a plan, do not edit files unless the user requests a saved document.

## Plan Shape

Use this structure:

- Scope
- Risk areas
- Automated tests
- Manual checks
- Edge cases
- Regression checks
- Commands to run
- Out of scope

When saving a plan, prefer `docs/test-plan.md` or a more specific path the repository already uses.

## Verification

Verify test commands against actual package scripts or project tooling. Mention any tests that cannot run locally and why.
