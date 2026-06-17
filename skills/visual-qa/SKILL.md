---
name: visual-qa
description: "Run frontend visual QA for local web apps and UI changes. Use when the user asks to visually verify a screen, compare implementation to a design, inspect responsive behavior, check screenshots, or catch overlap, clipping, blank states, spacing, typography, and interaction regressions."
---

# Visual QA

## Overview

Visually verify UI behavior with real rendering evidence. Use browser screenshots and responsive checks instead of judging only from source code.

## Workflow

1. Identify the target route, screen, component, or local URL. If unclear, inspect app scripts and routes before asking.
2. Start or reuse the local dev server when the app needs one.
3. Use the Codex Browser plugin when available. If browser tools are not loaded, call `tool_search` for in-app browser control.
4. Capture desktop and mobile viewport evidence for the affected UI. Include tablet or wide viewports when layout risk warrants it.
5. Check for blank screens, console/runtime errors, broken assets, overlapping text, clipped controls, horizontal scrolling, inaccessible focus states, and obvious design drift.
6. Interact with primary controls when the screen has states, menus, forms, modals, or navigation.
7. If issues are found and the user asked for fixes, make focused code changes and repeat the visual check.

## Reporting

Report:

- URL or route checked
- Viewports checked
- Screenshots or observations
- Issues found, with severity
- Fixes made, if any
- Remaining visual risk

Do not claim visual QA is complete without rendered evidence.

## Verification

Run the relevant typecheck, test, or build command when the visual fix touches code. Stop any long-running dev server only if it is no longer needed for the user.
