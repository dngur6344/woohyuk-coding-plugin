---
name: document-project-architecture
description: "Create or update structured project architecture documentation under docs/. Use when the user asks to document the overall project, project purpose, runtime flow, package or module structure, package responsibilities, architecture diagram, or implementation overview."
---

# Document Project Architecture

## Overview

Create evidence-backed architecture documentation under `docs/` that helps a new engineer understand what the project is, how it runs, and how the packages fit together.

## Workflow

1. Inspect repository structure with `rg --files`, package manifests, entrypoints, config files, routing, build scripts, tests, and existing docs.
2. Identify the project purpose from actual code and user-facing artifacts. Avoid claims that are not supported by the repository.
3. Map the package, module, or directory structure. Explain responsibilities and important boundaries, not every file.
4. Trace the main runtime or request flow from entrypoint to core modules. For UI apps, include screen/component flow where relevant.
5. Create or update `docs/project-architecture.md` unless the repository has an existing architecture docs convention.
6. Keep changes scoped to documentation unless the user separately asks for code changes.

## Required Content

Include these sections when the repository provides enough evidence:

- Project purpose
- High-level architecture
- Runtime or interaction flow
- Package and directory structure
- Key packages, modules, and responsibilities
- Data flow or state management
- Build, test, and deployment flow
- Extension points and known boundaries

Use Mermaid diagrams only when they clarify a real flow or structure. Keep diagrams small enough to maintain by hand.

## Verification

Check links, headings, Mermaid syntax if used, and whether each architectural claim can be traced back to repository evidence.
