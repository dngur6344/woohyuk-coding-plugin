---
name: write-adr
description: "Write or update Architecture Decision Records in docs/adr/. Use when the user asks to record an architectural decision, compare options, explain why a technical direction was chosen, or document consequences, tradeoffs, and decision context."
---

# Write ADR

## Overview

Create short, evidence-backed Architecture Decision Records that explain a decision, the options considered, and the consequences for future maintainers.

## Workflow

1. Inspect the repository, existing docs, and existing `docs/adr/` records before choosing a filename or format.
2. If no ADR convention exists, create `docs/adr/NNNN-short-title.md` using the next zero-padded number.
3. Capture the decision that is actually being made. Do not turn implementation notes into an ADR unless a durable architectural choice exists.
4. Compare realistic alternatives. Include the simpler option when it was considered.
5. Keep claims tied to repository evidence, user context, or explicit assumptions.
6. Update docs indexes only when the repository already maintains one or the user asks for it.

## ADR Shape

Use this structure unless the repository already has a different ADR template:

- Title
- Status
- Context
- Decision
- Options Considered
- Consequences
- Follow-ups

Use `Proposed`, `Accepted`, `Superseded`, or `Deprecated` for status. Default to `Proposed` unless the user clearly says the decision is final.

## Verification

Check numbering, links, heading hierarchy, and whether the ADR records a decision rather than a generic design note. Report the created or updated ADR path.
