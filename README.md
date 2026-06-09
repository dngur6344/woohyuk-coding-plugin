# Woohyuk Coding Plugin

Personal Codex plugin with workflows for code review, Pencil design implementation, README maintenance, and project architecture documentation.

## Skills

- `$review-code`: Review diffs, PRs, and working-tree changes for concrete bugs, regressions, and test gaps.
- `$pencil-design-implementation`: Use Pencil `.pen` files through Pencil MCP tools, then implement the design in code.
- `$maintain-readme`: Create or update README content from repository evidence.
- `$document-project-architecture`: Create structured project architecture documentation under `docs/`.

## Structure

```text
.codex-plugin/plugin.json
skills/
  review-code/
  pencil-design-implementation/
  maintain-readme/
  document-project-architecture/
```

## Public Repository Notes

This repository intentionally excludes local Codex state, marketplace files, environment files, credentials, and `.pen` design files.
