---
name: woohyuk-explain-diff
description: "Create a rich, interactive, self-contained HTML explanation of a code change. Use when the user asks to explain a diff, working-tree change, commit, branch comparison, pull request, or the surrounding system and wants a durable visual walkthrough with diagrams and a quiz."
---

# Explain Diff

Create one long-form HTML page that helps a reader understand both the system around a change and the change itself. Base every claim on repository evidence and write for readers who may be new to the project.

## Workflow

1. Resolve the exact change scope: working tree, staged diff, commit, commit range, branch comparison, or pull request. Inspect the repository first; ask the user only when multiple plausible scopes would materially change the result.
2. Gather the diff, changed-file summary, relevant history, and tests. Broadly inspect surrounding entry points, callers, data models, configuration, and documentation so the explanation covers the existing system rather than only the modified lines.
3. Form a coherent explanation before writing HTML. Group changes by responsibility or execution flow, not mechanically by file order.
4. Create a single self-contained HTML file with embedded CSS and JavaScript.
5. Validate the file structure, render it in a browser when browser tooling is available, and exercise the quiz interactions before reporting completion.

Do not modify the analyzed repository unless the user separately asks for code changes.

## Required Sections

Use a persistent or clearly visible table of contents that links to these top-level sections. Present them on one scrolling page; do not use tabs for the top-level structure.

### Background

Explain the existing system relevant to the change.

- Begin with a beginner-friendly foundation that experienced readers can skip.
- Narrow progressively toward the components, data, constraints, and execution path directly affected by the change.
- Distinguish repository evidence from inference. Do not invent behavior that the code does not support.

### Intuition

Explain the essence of the change before its implementation details.

- Use concrete toy data and realistic before/after examples.
- Show why the previous behavior was insufficient and how the new behavior changes the outcome.
- Reuse a small number of consistent diagram families throughout the page.
- Prefer simplified UI diagrams for user-facing changes and component/data-flow diagrams with example payloads for system changes.

### Code

Walk through the implementation at a high level.

- Organize the walkthrough around concepts, responsibilities, or runtime order.
- Connect each important code change back to the intuition and affected behavior.
- Include only the code excerpts needed to understand the change.
- Explain tests and safeguards alongside the behavior they verify.

### Quiz

Create exactly five medium-difficulty multiple-choice questions that test substantive understanding rather than trivia or gotchas.

- Provide plausible distractors.
- Let the reader select an answer and immediately learn whether it is correct.
- Show concise feedback explaining why the chosen answer is right or wrong.
- Keep the correct answer hidden until the reader interacts.
- Make the controls keyboard accessible and clearly expose their selected, correct, and incorrect states.

## HTML Requirements

- Save the file outside the code repository under `/tmp`.
- Prefix the filename with the current local date in `YYYY-MM-DD-` format and use a short filesystem-safe slug, for example `/tmp/2026-01-12-explanation-auth-cache.html`.
- Include all CSS and JavaScript in the file. Do not require external packages, fonts, scripts, stylesheets, images, or network access.
- Use semantic HTML, visible focus states, sufficient contrast, and responsive styling suitable for desktop and phone widths.
- Use section headers, smooth transitions, callouts for definitions and edge cases, and a readable visual hierarchy.
- Write clear, precise explanatory prose with concrete examples and smooth narrative flow, in the spirit of Martin Kleppmann's accessible technical writing.
- Build diagrams with semantic HTML and CSS. Do not use ASCII diagrams.
- Put every code excerpt in a `<pre><code>` block. Escape repository content before embedding it so code cannot become executable HTML.
- Define `white-space: pre` or `white-space: pre-wrap` for every code-block presentation path. Prefer a global `pre { white-space: pre-wrap; }` rule and ensure no more-specific rule overrides it incorrectly.
- Do not expose credentials, tokens, personal data, or other secrets found in repository content. Redact sensitive values without obscuring the behavior being explained.

## Validation

Before finishing:

1. Confirm the output is one HTML file under `/tmp` and its basename begins with today's local date.
2. Confirm `Background`, `Intuition`, `Code`, and `Quiz` exist and the table of contents links to them.
3. Confirm the quiz has exactly five questions, each with interactive correctness feedback.
4. Confirm all styles and scripts are embedded and no runtime network dependency exists.
5. Scan every code block and its applicable CSS. Confirm newlines are preserved with `white-space: pre` or `pre-wrap`.
6. Check that all inserted code and example data are HTML-escaped and that no sensitive values appear.
7. When browser tooling is available, open the page at desktop and phone widths, check for overflow or overlap, and answer at least one correct and one incorrect quiz option.

Report the absolute output path and summarize the change scope covered. Mention any part that could not be rendered or interactively verified.
