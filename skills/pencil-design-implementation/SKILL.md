---
name: pencil-design-implementation
description: "Use Pencil .pen design files to create or modify app and website designs, inspect design variables and layout, export design assets, and implement the design in the current codebase. Use when the user mentions Pencil, .pen files, design-to-code, or asks Codex to turn a Pencil design into UI code."
---

# Pencil Design Implementation

## Overview

Use Pencil as the source of truth for design structure, variables, and visual QA, then implement the design with the repository's existing frontend patterns.

## Pencil Rules

- Treat `.pen` files as encrypted design documents. Never read, grep, cat, parse, or edit `.pen` files through filesystem tools.
- Use Pencil MCP tools only. If the tools are not loaded, call `tool_search` for `pencil .pen open_document get_editor_state`.
- Before reading or writing design nodes, call Pencil `get_editor_state` with schema loading enabled unless the schema was already loaded in the current conversation.
- If the user gives a `.pen` path, open it through Pencil `open_document` with the absolute path.
- Use `get_guidelines`, `get_variables`, `snapshot_layout`, `get_screenshot`, `batch_get`, `batch_design`, and `export_nodes` as appropriate for the task.

## Design Workflow

1. Open or inspect the active Pencil document.
2. Load variables and guidelines before designing or implementing.
3. Inspect selected frames or relevant nodes with bounded depth. Use `snapshot_layout` with `problemsOnly` when checking layout issues.
4. When modifying a design, prefer targeted `batch_design` changes and validate with screenshot or layout snapshots.
5. Export only the nodes needed for implementation or review.

## Implementation Workflow

1. Inspect the app stack and existing UI conventions before editing code.
2. Map Pencil variables to existing tokens, CSS variables, theme values, or component props where possible.
3. Reuse local components before creating new abstractions.
4. Keep implementation scoped to the requested screen or component.
5. Run the relevant formatter, typecheck, tests, and local visual verification. For web apps, open the local app in the browser when practical and inspect screenshots for overlap, blank states, and responsive layout.

## Output

Report the Pencil document or nodes used, code files changed, validation commands run, and any visual checks completed.
