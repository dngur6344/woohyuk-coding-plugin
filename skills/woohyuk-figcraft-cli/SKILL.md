---
name: woohyuk-figcraft-cli
description: "Use the local figcraft-cli to inspect, create, edit, render, export, or convert designs for the FigCraft app, or extract layer code for requested implementation. Use when the user mentions FigCraft, figcraft-cli, or .figcraft files. Not for Figma app automation or Pencil .pen files."
---

# FigCraft CLI

Use FigCraft's native `.figcraft` documents and local CLI. The target application is FigCraft, not Figma. Do not route this workflow through Figma tools, Figma MCP, or a Figma account.

## Locate The CLI

1. Use the executable or installation directory supplied by the user; for a directory, look for `figcraft-cli` inside it.
2. Otherwise check `command -v figcraft-cli`, then `$HOME/.local/bin/figcraft-cli`, then look for `$HOME/.local/opt/figcraft-cli/*/figcraft-cli`. Ask for the location if missing or ambiguous; do not install or download another binary automatically.
3. Store the resolved executable in a shell variable and quote it on every invocation. Check `--version` and `--help` for the installed release before assuming commands or flags.

Known manual installation layout, verified on macOS with CLI 0.12.1: keep the full release under `$HOME/.local/opt/figcraft-cli/0.12.1/` and expose its executable through a symlink at `$HOME/.local/bin/figcraft-cli`. Keep `$HOME/.local/bin` on `PATH` so callers do not need a version-specific path.

```bash
FIGCRAFT_CLI="$HOME/.local/bin/figcraft-cli"
"$FIGCRAFT_CLI" --version
"$FIGCRAFT_CLI" --help
"$FIGCRAFT_CLI" commands --json --filter node.create
```

The binary and FigCraft app are separate local prerequisites, not plugin assets. Do not copy them, their fonts, or local preferences into the public plugin repository.

## Working Rules

- Default to local, headless file operations. A CLI invocation does not control the open FigCraft window or automatically refresh an already-open tab. Do not claim live synchronization.
- Inspect existing inputs with `info --json` before editing. Preserve the original until the new output has been validated, especially if the same document is open in FigCraft with unsaved changes. Do not force an overwrite to resolve a concurrent-edit warning.
- Discover command IDs and parameter shapes with `commands --json --filter TEXT`. Read only relevant registry entries rather than dumping the entire registry. Never invent IDs, parameters, template names, or result-reference syntax.
- Use JSON arrays or JSONL records shaped as `{"command": "node.create", "params": {...}}` with `run`. Use returned IDs or IDs from inspection; do not assume the IDs in another document match. Each invocation is a new headless session, so reopen saved state with `--in` when continuing work.
- Prefer the CLI command API over directly editing native archive contents. Review every JSON step result and the process exit status; stop on errors and do not assume an output was saved. Surface import, conversion, font, and export warnings.
- Confine file operations with `--automation-read-root` and `--automation-write-root` when supported by the installed release. Use existing, narrow input/output directories, not the whole home directory. These roots restrict file access, not network activity.
- Do not publish, share, join collaboration sessions, install FigCraft plugins, register an MCP server, or attach to a running app unless that action was requested. Do not send design files or server keys to remote services as part of ordinary local design work.
- `.fig` import is best effort and export is experimental in the verified release. Importing a file is not access to an online design or proof of round-trip fidelity. Use native `.figcraft` output unless the user requests another format; `.pen` remains outside this skill.

## Design Workflow

1. Identify the requested screen or change, input document, and intended output. Inspect repository conventions if the design belongs to a project. Ask about ambiguity that materially affects the result.
2. Inspect page/frame IDs and dimensions with `info --json`. For deeper inspection, query confirmed commands such as `node.get`, `inspect.properties`, and relevant style or variable commands through a read-only script with `run --in`.
3. Write a scoped command script. For a new design, start with `file.new` or a template discovered via `template.list`. Preserve editable frames, text, components, styles, and variables rather than flattening the screen into one image.
4. Execute the script and save to a deliberate output path. For edits, pass both `--in` and `--out`; use a separate output while validating rather than overwriting unrelated or unsaved work. If later commands need newly created IDs, inspect the results and continue from the saved output rather than guessing references.
5. Render the saved output to PNG and inspect it visually for clipping, text overflow, missing assets, and incorrect hierarchy. Use the required fonts; `--no-system-fonts` is useful for reproducible previews but must not silently replace a required font. Recheck `info --json` and relevant nodes after edits.
6. Export only the requested frames or assets. `export` normally writes one file per top-level frame into its output directory; use `--page` or `--node` when supported to bound the scope. `render` creates a page preview, not necessarily a single-frame export.
7. Hand off the native file for the FigCraft app. On macOS, when the user wants to open it and FigCraft is installed, use `open -a "FigCraft" "/absolute/path/to/design.figcraft"`. Do not use Figma as the viewer. If the input was already open, make clear which saved output to open; do not discard the app's unsaved state.

## Command Patterns

Resolve the executable and actual file paths first. Append the scoped automation roots to file-processing commands where supported.

```bash
"$FIGCRAFT_CLI" info "design.figcraft" --json
"$FIGCRAFT_CLI" run "changes.json" --in "design.figcraft" --out "design-updated.figcraft"
"$FIGCRAFT_CLI" run "create.json" --out "design.figcraft"
"$FIGCRAFT_CLI" render "design-updated.figcraft" -o "preview.png" --scale 2
"$FIGCRAFT_CLI" export "design-updated.figcraft" -o "assets/" --format svg
"$FIGCRAFT_CLI" convert "input.svg" "converted.figcraft"
```

## Code Handoff

Only implement application code when requested. Discover `inspect.code`, `inspect.componentCode`, or `variable.export` for supported languages and token exports. Treat generated code as reference, not a production-ready replacement: adapt it to the repository's existing components and tokens, then run focused checks and rendered UI verification. Do not change application code for a design-only request.

## Output

Report the CLI version used, native document path, relevant frames, exported files or code changes, validation performed, and unresolved warnings. Distinguish CLI rendering from verification in the FigCraft app; never claim app or code verification that was not performed.
