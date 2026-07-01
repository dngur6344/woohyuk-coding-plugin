---
name: search-llm-wiki
description: "Search and reference Woohyuk's local LLM wiki for project, coding, prompt, model, architecture, and AI workflow knowledge. Use when the user mentions llm-wiki, LLM wiki, personal wiki, wiki notes, or asks Codex to find relevant information from ~/Desktop/woohyuk-llm-wiki."
---

# Search LLM Wiki

## Overview

Use the local LLM wiki as a knowledge source before answering or implementing when the user asks to reference it. Search narrowly, cite the local note paths used, and keep the final answer grounded in wiki evidence.

## Wiki Location

Resolve the wiki path in this order:

1. `$LLM_WIKI_PATH` when set.
2. `~/Desktop/woohyuk-llm-wiki` as the default path.

If the wiki path does not exist, tell the user the resolved path and stop instead of guessing from memory.

## Search Workflow

1. Start with high-signal files such as `index.md`, `README.md`, `wiki/README.md`, and `wiki/overview.md` when they exist.
2. Use `rg` for targeted keyword search across Markdown files.
3. Exclude app state, raw imports, and generated folders by default: `.obsidian/`, `.git/`, `raw/`, and binary assets.
4. Open only the most relevant notes needed for the current task. Do not bulk-read the whole wiki.
5. When multiple notes conflict, prefer the newest or more specific note only when the file content gives enough evidence; otherwise surface the conflict.
6. If the wiki does not contain enough information, say what was searched and what was missing.

## Answering

Reference the local notes used with file paths. Separate wiki-backed facts from your own inference.

Use this shape when the user asks for an answer from the wiki:

- Answer
- Wiki evidence
- Assumptions or gaps

## Editing Rules

Do not modify the wiki unless the user explicitly asks to update it. If editing is requested, inspect the wiki's own instructions such as `AGENTS.md` before changing files.
